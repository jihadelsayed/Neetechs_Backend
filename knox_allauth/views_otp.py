# knox_allauth/views_otp.py

import random
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox_allauth.models import CustomUser

from rest_framework.authtoken.models import Token
from datetime import timedelta

class SendPhoneOTP(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({"detail": "Phone number is required."}, status=400)

        user, created = CustomUser.objects.get_or_create(phone=phone)

        otp = str(random.randint(100000, 999999))
        user.phone_otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        # 🔥 Replace this with real SMS send
        print(f"Mock OTP for {phone}: {otp}")

        return Response({"detail": "OTP sent successfully."}, status=200)

class VerifyPhoneOTP(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')

        try:
            user = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        if not user.phone_otp or user.phone_otp != otp:
            return Response({"detail": "Invalid OTP."}, status=400)

        if timezone.now() - user.otp_created_at > timedelta(minutes=5):
            return Response({"detail": "OTP expired."}, status=400)

        user.phone_otp = None
        user.save()

        token = Token.objects.get_or_create(user=user)[0]
        return Response({"token": token.key, "user_id": user.id}, status=200)
