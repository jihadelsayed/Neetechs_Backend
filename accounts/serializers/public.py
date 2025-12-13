from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone",
            "username",
            "handle",
            "display_name",
            "first_name",
            "last_name",
            "site_id",
            "is_creator",
            "profile_completed",
        ]
