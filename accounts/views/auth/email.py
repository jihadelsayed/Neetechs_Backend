from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from drf_spectacular.utils import extend_schema


from ...serializers.auth import EmailConfirmationSerializer

User = get_user_model()

@extend_schema(tags=["accounts-security"])
class EmailConfirmation(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailConfirmationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].strip()
        email_lc = email.lower()

        # Always return a generic response to prevent email enumeration.
        # We intentionally do not reveal:
        # - whether the user exists
        # - whether the email is already verified
        # - whether sending succeeded
        generic = {"detail": "If this email exists, a confirmation email has been sent."}

        # Find a matching user without revealing existence
        user = User.objects.filter(email__iexact=email_lc).first()
        if not user:
            return Response(generic, status=status.HTTP_200_OK)

        # If already verified, still return generic (no leaks)
        if EmailAddress.objects.filter(user=user, email__iexact=email_lc, verified=True).exists():
            return Response(generic, status=status.HTTP_200_OK)

        # Try send; swallow errors to avoid leaks
        try:
            send_email_confirmation(request, user=user)
        except Exception:
            pass

        return Response(generic, status=status.HTTP_200_OK)
