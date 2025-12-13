from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

User = get_user_model()


class PublicUserSerializer(serializers.ModelSerializer):
    email_confirmed = serializers.SerializerMethodField()
    has_password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "email_confirmed",
            "phone",
            "has_password",
            "username",
            "handle",
            "display_name",
            "first_name",
            "last_name",
            "site_id",
            "is_creator",
            "profile_completed",
        ]

    def get_email_confirmed(self, obj) -> bool:
        if not obj.email:
            return False
        return EmailAddress.objects.filter(email__iexact=obj.email, verified=True).exists()

    def get_has_password(self, obj) -> bool:
        return obj.has_usable_password()
