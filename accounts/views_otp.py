
import logging
import random
from hashlib import sha256
from datetime import timedelta

from django.utils import timezone
from django.core.cache import cache
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from knox.models import AuthToken
from django.conf import settings

from .models import User
from .twilio_utils import send_sms_otp
from .serializers.auth import SendPhoneOTPSerializer, VerifyPhoneOTPSerializer

logger = logging.getLogger(__name__)


class SendPhoneOTP(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendPhoneOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]

        hashed_email = sha256(phone.encode()).hexdigest()[:10]
        placeholder_email = f"{hashed_email}@neetechs.sms"

        user, _ = User.objects.get_or_create(
            phone=phone,
            defaults={"email": placeholder_email, "name": "PhoneUser"},
        )

        otp = f"{random.randint(100000, 999999)}"
        user.phone_otp = otp
        user.otp_created_at = timezone.now()
        user.save(update_fields=["phone_otp", "otp_created_at"])

        if getattr(settings, "DEBUG", False):
            logger.warning("[MOCK OTP] to %s: %s", phone, otp)
        else:
            try:
                send_sms_otp(phone, otp)
            except Exception as e:
                logger.error("Failed to send OTP to %s: %s", phone, e)

        return Response({"detail": "OTP sent successfully."}, status=200)


class VerifyPhoneOTP(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyPhoneOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        otp = serializer.validated_data["otp"]

        ip = request.META.get("REMOTE_ADDR")
        device_id = request.headers.get("X-Device-ID", "")
        attempt_key = f"otp_attempts_{ip}_{device_id}"
        attempts = cache.get(attempt_key, 0)

        if attempts >= 5:
            return Response({"detail": "Too many failed attempts. Try again in 1 hour."}, status=429)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        if not user.phone_otp or user.phone_otp != otp:
            cache.set(attempt_key, attempts + 1, timeout=3600)
            return Response({"detail": "Invalid OTP."}, status=400)

        if user.otp_created_at and (timezone.now() - user.otp_created_at > timedelta(minutes=5)):
            return Response({"detail": "OTP expired."}, status=400)

        cache.delete(attempt_key)

        user.phone_otp = None
        user.otp_created_at = None
        user.save(update_fields=["phone_otp", "otp_created_at"])

        token = AuthToken.objects.create(user)[1]

        return Response(
            {
                "token": token,
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "email": user.email,
                    "name": user.name,
                },
                "has_password": user.has_usable_password(),
            },
            status=200,
        )
