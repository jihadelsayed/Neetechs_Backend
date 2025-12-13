"""Serializers used by authentication / accounts API views."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class EmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SendPhoneOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=32)


class VerifyPhoneOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=32)
    otp = serializers.CharField(max_length=6, min_length=4)


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6,
        write_only=True,
        style={"input_type": "password"},
    )


class SetHandleSerializer(serializers.Serializer):
    handle = serializers.SlugField(min_length=3, max_length=40)

    def validate_handle(self, value: str) -> str:
        value = (value or "").strip().lower()

        reserved = {
            "admin", "support", "api", "auth",
            "login", "register", "me",
            "accounts", "payments", "checkout",
            "digital-products",
        }
        if value in reserved:
            raise serializers.ValidationError("This handle is reserved.")

        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not getattr(user, "id", None):
            raise serializers.ValidationError("Authentication required.")

        if User.objects.filter(handle=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Handle already taken.")

        return value
