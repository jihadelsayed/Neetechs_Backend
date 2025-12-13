from rest_framework import serializers
from .public import PublicUserSerializer


class AuthResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = PublicUserSerializer()
