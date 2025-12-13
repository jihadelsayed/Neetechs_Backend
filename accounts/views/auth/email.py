from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from allauth.account.utils import send_email_confirmation

from ...serializers.auth import EmailConfirmationSerializer

User = get_user_model()


class EmailConfirmation(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailConfirmationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = get_object_or_404(User, email=email)

        if user.emailaddress_set.filter(verified=True).exists():
            return Response(
                {"message": "This email is already verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            send_email_confirmation(request, user=user)
            return Response({"message": "Email confirmation sent"}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(
                {"message": "This email does not exist, please create a new account"},
                status=status.HTTP_403_FORBIDDEN,
            )
