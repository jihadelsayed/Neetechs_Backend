# knox_allauth/serializer_register.py

from rest_framework import serializers
from knox_allauth.models import CustomUser
from django.contrib.auth.password_validation import validate_password

class PhoneOrEmailRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'password', 'name']
        extra_kwargs = {
            'email': {'required': False},
            'phone': {'required': False},
        }

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('phone'):
            raise serializers.ValidationError("You must provide either email or phone.")

        if attrs.get('email') and CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already in use.")
        if attrs.get('phone') and CustomUser.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError("Phone number already in use.")

        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
