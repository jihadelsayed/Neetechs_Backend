"""Serializers used by authentication API views."""
from rest_framework import serializers

from Profile.serializer import ProfileSerializer


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
