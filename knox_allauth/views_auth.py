
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from dj_rest_auth.views import LoginView
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup, send_email_confirmation
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from .models import CustomUser
from .utils import create_knox_token
from .serializers.user import KnoxSerializer
from .serializers.register import PhoneOrEmailRegisterSerializer
from Profile.serializer import ProfileSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class KnoxLoginView(LoginView):
    permission_classes = [AllowAny]

    def get_response(self):
        serializer_class = KnoxSerializer
        data = {"user": self.user, "token": self.token[1]}
        serializer = serializer_class(instance=data, context={"request": self.request})
        return Response(serializer.data, status=200)


class KnoxRegisterView(RegisterView):
    permission_classes = [AllowAny]
    serializer_class = PhoneOrEmailRegisterSerializer

    def perform_create(self, serializer):
        phone_number = self.request.data.get("phone")
        customer_email = self.request.data.get("email") or (
            f"no-email-{phone_number}@neetechs.com" if phone_number else f"no-email-anonymous@{getattr(settings,'DEFAULT_DOMAIN','neetechs.com')}"
        )

        customer = stripe.Customer.create(
            email=customer_email,
            payment_method="pm_card_visa",
            invoice_settings={"default_payment_method": "pm_card_visa"},
        )

        user = serializer.save(self.request)
        token = create_knox_token(None, user, None)

        identifier = self.request.data.get("email") or self.request.data.get("phone")
        instance = CustomUser.objects.filter(email=identifier).first() or CustomUser.objects.filter(phone=identifier).first()

        profile_data = self.request.data.copy()
        profile_data["stripeCustomerId"] = customer.id

        if instance:
            ps = ProfileSerializer(instance, data=profile_data, partial=True)
            if ps.is_valid():
                ps.save()

        complete_signup(self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None, signal_kwargs={"sociallogin": None})
        self.token = (None, token)
        return user


class SocialLoginView_(SocialLoginView):
    permission_classes = [AllowAny]

    def get_response(self):
        serializer_class = KnoxSerializer
        data = {"user": self.user, "token": self.token[1]}
        serializer = serializer_class(instance=data, context={"request": self.request})
        return Response(serializer.data, status=200)


class FacebookLogin(SocialLoginView_):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView_):
    permission_classes = [AllowAny]
    adapter_class = GoogleOAuth2Adapter


class EmailConfirmation(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = get_object_or_404(CustomUser, email=request.data.get("email"))
        if user.emailaddress_set.filter(verified=True).exists():
            return Response({"message": "This email is already verified. Try to login and logout again to refresh the app."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            send_email_confirmation(request, user=user)
            return Response({"message": "Email confirmation sent"}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"message": "This email does not exist, please create a new account"}, status=status.HTTP_403_FORBIDDEN)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
