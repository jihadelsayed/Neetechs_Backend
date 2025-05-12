# knox_allauth/views_otp.py

import random
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Neetechs import settings
from knox_allauth.models import CustomUser

from datetime import timedelta
from knox_allauth.twilio_utils import send_sms_otp
from knox.models import AuthToken
from datetime import timedelta
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from hashlib import sha256


class SendPhoneOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({"detail": "Phone number is required."}, status=400)

        hashed_email = sha256(phone.encode()).hexdigest()[:10]
        placeholder_email = f"{hashed_email}@neetechs.sms"

        user, created = CustomUser.objects.get_or_create(
            phone=phone,
            defaults={"email": placeholder_email, "name": "PhoneUser"}
        )


        otp = str(random.randint(100000, 999999))
        user.phone_otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        # 🔥 Replace this with real SMS send
        print(f"Mock OTP for {phone}: {otp}")
        if settings.DEBUG:
            print(f"[MOCK OTP] to {phone}: {otp}")
        else:
            send_sms_otp(phone, otp)


        return Response({"detail": "OTP sent successfully."}, status=200)


class VerifyPhoneOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')

        ip = request.META.get('REMOTE_ADDR')
        device_id = request.headers.get('X-Device-ID', '')

        attempt_key = f"otp_attempts_{ip}_{device_id}"
        attempts = cache.get(attempt_key, 0)

        if attempts >= 5:
            return Response({"detail": "Too many failed attempts. Try again in 1 hour."}, status=429)

        try:
            user = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        if not user.phone_otp or user.phone_otp != otp:
            cache.set(attempt_key, attempts + 1, timeout=3600)
            return Response({"detail": "Invalid OTP."}, status=400)

        if timezone.now() - user.otp_created_at > timedelta(minutes=5):
            return Response({"detail": "OTP expired."}, status=400)

        cache.delete(attempt_key)

        user.phone_otp = None
        user.otp_created_at = None
        user.save()

        token = AuthToken.objects.create(user)[1]
        return Response({
            "token": token,
            "user": {
                "id": user.id,
                "phone": user.phone,
                "email": user.email,
                "name": user.name
            }
        }, status=200)

