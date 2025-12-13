from rest_framework import serializers
from .public import PublicUserSerializer


class AuthResponseSerializer(serializers.Serializer):
    token = serializers.CharField(
        help_text="Knox authentication token"
    )
    user = PublicUserSerializer(
        help_text="Authenticated user (public fields only)"
    )
