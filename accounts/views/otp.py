import logging
import random
import hashlib
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import User
from ..twilio_utils import send_sms_otp
from ..serializers.auth import SendPhoneOTPSerializer, VerifyPhoneOTPSerializer

logger = logging.getLogger(__name__)

OTP_TTL_SECONDS = 5 * 60          # 5 minutes
OTP_COOLDOWN_SECONDS = 60         # 60s before resend
OTP_MAX_ATTEMPTS = 5              # per phone+ip+device
OTP_LOCK_SECONDS = 60 * 60        # 1 hour lock after too many attempts


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def get_client_ip(request) -> str:
    """
    Works behind proxies if you pass X-Forwarded-For.
    Make sure your proxy sets it and you trust it.
    """
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        # left-most is original client in standard setups
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR") or ""


class SendPhoneOTP(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendPhoneOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"].strip()

        # cooldown per phone
        cooldown_key = f"otp:cooldown:{phone}"
        if cache.get(cooldown_key):
            return Response(
                {"detail": "OTP already sent. Wait a bit before requesting another."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        # create/get user for this phone
        # keep your placeholder email approach for now (we can improve later)
        placeholder_email = f"{_sha256_hex(phone)[:10]}@neetechs.sms"
        user, _ = User.objects.get_or_create(
            phone=phone,
            defaults={"email": placeholder_email, "username": (_sha256_hex(phone)[:12])},
        )

        otp = f"{random.randint(100000, 999999)}"
        user.phone_otp_hash = _sha256_hex(f"{phone}:{otp}:{getattr(settings,'SECRET_KEY','')}")
        user.otp_expires_at = timezone.now() + timedelta(seconds=OTP_TTL_SECONDS)
        user.save(update_fields=["phone_otp_hash", "otp_expires_at"])

        # start cooldown
        cache.set(cooldown_key, 1, timeout=OTP_COOLDOWN_SECONDS)

        if getattr(settings, "DEBUG", False):
            logger.warning("[MOCK OTP] to %s: %s", phone, otp)
        else:
            sid = send_sms_otp(phone, otp)
            if not sid:
                # If Twilio failed, allow retry sooner (don’t punish user)
                cache.delete(cooldown_key)
                return Response(
                    {"detail": "Failed to send OTP. Try again."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

        return Response({"detail": "OTP sent successfully."}, status=200)


class VerifyPhoneOTP(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyPhoneOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"].strip()
        otp = serializer.validated_data["otp"].strip()

        ip = get_client_ip(request)
        device_id = (request.headers.get("X-Device-ID") or "").strip()[:64]  # cap size

        # lock + attempts key
        lock_key = f"otp:lock:{phone}:{ip}:{device_id}"
        if cache.get(lock_key):
            return Response(
                {"detail": "Too many failed attempts. Try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        attempts_key = f"otp:attempts:{phone}:{ip}:{device_id}"
        attempts = int(cache.get(attempts_key, 0))

        if attempts >= OTP_MAX_ATTEMPTS:
            cache.set(lock_key, 1, timeout=OTP_LOCK_SECONDS)
            cache.delete(attempts_key)
            return Response(
                {"detail": "Too many failed attempts. Try again in 1 hour."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        if not user.phone_otp_hash or not user.otp_expires_at:
            cache.set(attempts_key, attempts + 1, timeout=OTP_LOCK_SECONDS)
            return Response({"detail": "Invalid OTP."}, status=400)

        if timezone.now() > user.otp_expires_at:
            # expire & force resend
            user.phone_otp_hash = None
            user.otp_expires_at = None
            user.save(update_fields=["phone_otp_hash", "otp_expires_at"])
            return Response({"detail": "OTP expired."}, status=400)

        expected = _sha256_hex(f"{phone}:{otp}:{getattr(settings,'SECRET_KEY','')}")
        if expected != user.phone_otp_hash:
            cache.set(attempts_key, attempts + 1, timeout=OTP_LOCK_SECONDS)
            return Response({"detail": "Invalid OTP."}, status=400)

        # success: clear otp + attempts
        cache.delete(attempts_key)
        cache.delete(lock_key)

        user.phone_otp_hash = None
        user.otp_expires_at = None
        user.save(update_fields=["phone_otp_hash", "otp_expires_at"])

        # use Knox, not knox.models.AuthToken directly if you want consistent token style
        from knox.models import AuthToken
        token = AuthToken.objects.create(user)[1]

        return Response(
            {
                "token": token,
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "email": user.email,
                    "display_name": user.display_name,
                    "username": user.username,
                },
                "has_password": user.has_usable_password(),
            },
            status=200,
        )
