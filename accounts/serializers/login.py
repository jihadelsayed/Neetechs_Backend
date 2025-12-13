from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from allauth.account.models import EmailAddress

from ..models import User


class PhoneOrEmailLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        raw_identifier = (attrs.get("identifier") or "").strip()
        password = (attrs.get("password") or "").strip()

        if not raw_identifier or not password:
            raise serializers.ValidationError({"detail": _("Both fields are required.")})

        is_email_login = "@" in raw_identifier
        identifier = raw_identifier.lower() if is_email_login else raw_identifier

        # Authenticate via your custom backend (email OR phone).
        user = authenticate(
            request=self.context.get("request"),
            username=identifier,  # kept for backend compatibility
            password=password,
        )

        if not user:
            # If credentials failed, check if account exists but has no password
            try:
                user_obj = (
                    User.objects.get(email__iexact=identifier)
                    if is_email_login
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

        # Require verified email ONLY when logging in via email.
        if is_email_login:
            if user.email and not EmailAddress.objects.filter(email__iexact=user.email, verified=True).exists():
                raise serializers.ValidationError({"detail": _("Email is not verified.")})

        attrs["user"] = user
        return attrs
