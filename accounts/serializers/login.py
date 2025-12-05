
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from allauth.account.models import EmailAddress

from ..models import User


class PhoneOrEmailLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        identifier = attrs.get("identifier")
        password = attrs.get("password")

        if not identifier or not password:
            raise serializers.ValidationError({"detail": _("Both fields are required.")})

        user = authenticate(
            request=self.context.get("request"),
            username=identifier,
            password=password,
        )

        if not user:
            # If credentials failed, check if account exists but has no password
            try:
                user_obj = (
                    User.objects.get(email__iexact=identifier)
                    if "@" in identifier
                    else User.objects.get(phone=identifier)
                )
                if not user_obj.has_usable_password():
                    raise serializers.ValidationError(
                        {"detail": _("This user has no password. Login via phone OTP, then set a password.")}
                    )
            except User.DoesNotExist:
                pass
            raise serializers.ValidationError({"detail": _("Invalid phone/email or password.")})

        if not user.is_active:
            raise serializers.ValidationError({"detail": _("This account is inactive.")})

        # Optional: require verified email if email is present
        if user.email and not EmailAddress.objects.filter(email__iexact=user.email, verified=True).exists():
            raise serializers.ValidationError({"detail": _("Email is not verified.")})

        attrs["user"] = user
        return attrs
