import logging
import secrets
import hashlib
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import Throttled

from drf_spectacular.utils import extend_schema

from accounts.throttles import OTPThrottle
from accounts.serializers import PublicUserSerializer

from ..twilio_utils import send_sms_otp
from ..serializers.auth import SendPhoneOTPSerializer, VerifyPhoneOTPSerializer
from ..utils.knox import create_knox_token

logger = logging.getLogger(__name__)
User = get_user_model()

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
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR") or ""


def enforce_otp_cooldown(phone: str, seconds: int = OTP_COOLDOWN_SECONDS):
    key = f"otp:cooldown:{phone}"
    if cache.get(key):
        raise Throttled(detail="OTP already sent. Wait before requesting another.")
    cache.set(key, 1, timeout=seconds)


def _placeholder_email_for_phone(phone: str) -> str:
    # Safe + consistent placeholder domain (never a real domain)
    return f"{_sha256_hex(phone)[:10]}@phone.neetechs.invalid"


def _otp_hash(phone: str, otp: str) -> str:
    # Including SECRET_KEY is fine; just make sure it stays stable per environment.
    secret = getattr(settings, "SECRET_KEY", "")
    return _sha256_hex(f"{phone}:{otp}:{secret}")


@extend_schema(tags=["accounts-security"])
class SendPhoneOTP(GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = SendPhoneOTPSerializer
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"].strip()

        # Cooldown: blocks rapid resend (plus OTPThrottle is still in place)
        enforce_otp_cooldown(phone, OTP_COOLDOWN_SECONDS)

        # Create/get user for this phone (phone-based account)
        user, _ = User.objects.get_or_create(
            phone=phone,
            defaults={
                "email": _placeholder_email_for_phone(phone),
                "username": _sha256_hex(phone)[:12],
            },
        )

        # Secure OTP generation
        otp = f"{secrets.randbelow(900000) + 100000}"

        user.phone_otp_hash = _otp_hash(phone, otp)
        user.otp_expires_at = timezone.now() + timedelta(seconds=OTP_TTL_SECONDS)
        user.save(update_fields=["phone_otp_hash", "otp_expires_at"])

        if getattr(settings, "DEBUG", False):
            logger.warning("[MOCK OTP] to %s: %s", phone, otp)
        else:
            sid = send_sms_otp(phone, otp)
            if not sid:
                # Undo cooldown so user can retry
                cache.delete(f"otp:cooldown:{phone}")
                return Response(
                    {"detail": "Failed to send OTP. Try again."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

        return Response({"detail": "OTP sent successfully."}, status=status.HTTP_200_OK)


@extend_schema(tags=["accounts-security"])
class VerifyPhoneOTP(GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = VerifyPhoneOTPSerializer
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"].strip()
        otp = serializer.validated_data["otp"].strip()

        ip = get_client_ip(request)
        device_id = (request.headers.get("X-Device-ID") or "").strip()[:64]

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
                {"detail": "Too many failed attempts. Try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        # Do NOT leak whether phone exists (no enumeration)
        user = User.objects.filter(phone=phone).first()
        if not user:
            cache.set(attempts_key, attempts + 1, timeout=OTP_TTL_SECONDS)
            return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.phone_otp_hash or not user.otp_expires_at:
            cache.set(attempts_key, attempts + 1, timeout=OTP_TTL_SECONDS)
            return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() > user.otp_expires_at:
            # Expired: clear OTP; allow immediate resend by clearing cooldown + attempts
            user.phone_otp_hash = None
            user.otp_expires_at = None
            user.save(update_fields=["phone_otp_hash", "otp_expires_at"])

            cache.delete(f"otp:cooldown:{phone}")
            cache.delete(attempts_key)
            cache.delete(lock_key)

            return Response({"detail": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)

        expected = _otp_hash(phone, otp)
        if not secrets.compare_digest(expected, user.phone_otp_hash):
            cache.set(attempts_key, attempts + 1, timeout=OTP_TTL_SECONDS)
            return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # Success: clear otp + attempts/lock
        cache.delete(attempts_key)
        cache.delete(lock_key)

        user.phone_otp_hash = None
        user.otp_expires_at = None
        user.save(update_fields=["phone_otp_hash", "otp_expires_at"])

        token = create_knox_token(user)

        return Response(
            {
                "token": token,
                "user": PublicUserSerializer(user).data,
                "has_password": user.has_usable_password(),
            },
            status=status.HTTP_200_OK,
        )
