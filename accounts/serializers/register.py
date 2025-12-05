
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from ..models import User


class PhoneOrEmailRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["email", "phone", "password", "name"]
        extra_kwargs = {
            "email": {"required": False, "allow_null": True, "allow_blank": True},
            "phone": {"required": False, "allow_null": True, "allow_blank": True},
            "name": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate(self, attrs):
        email = (attrs.get("email") or "").strip()
        phone = (attrs.get("phone") or "").strip()

        if not email and not phone:
            raise serializers.ValidationError({"detail": "Provide either email or phone."})

        if email and User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({"detail": "Email already in use."})

        if phone and User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"detail": "Phone number already in use."})

        attrs["email"] = email or None
        attrs["phone"] = phone or None
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.get("email")
        name = validated_data.get("name")
        phone = validated_data.get("phone")
        return User.objects.create_user(email=email, password=password, name=name, phone=phone)
