"""Serializers used by authentication API views."""
from rest_framework import serializers

from Profile.serializer import ProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CurrentUserSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        ref_name = "CurrentUser"
        fields = ProfileSerializer.Meta.fields


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

    def validate_handle(self, value):
        value = value.lower()

        reserved = {"admin", "support", "api", "auth", "login", "register", "me"}
        if value in reserved:
            raise serializers.ValidationError("This handle is reserved.")

        user = self.context["request"].user
        if User.objects.filter(handle=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Handle already taken.")

        return value