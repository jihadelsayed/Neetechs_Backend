import stripe
from allauth.account.models import EmailAddress
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from knox_allauth.models import CustomUser
from Neetechs import settings
from Profile.serializer import ProfileSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup, send_email_confirmation
from allauth.socialaccount.providers.facebook.views import \
    FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from dj_rest_auth.views import LoginView
from django.conf import settings

from .serializer import KnoxSerializer, UserSerializer
from .utils import create_knox_token

from .serializer_register import PhoneOrEmailRegisterSerializer

class KnoxLoginView(LoginView):
    permission_classes = [AllowAny]
    def get_response(self):
        serializer_class = self.get_response_serializer()

        data = {
            'user': self.user,
            'token': self.token[1]
        }
        serializer = serializer_class(instance=data, context={'request': self.request})

        return Response(serializer.data, status=200)


class KnoxRegisterView(RegisterView):
    permission_classes = [AllowAny]
    serializer_class = PhoneOrEmailRegisterSerializer


    def perform_create(self, serializer):
        # Create a Stripe customer for the new user.
        # Uses the provided email, or a placeholder if email is not available (e.g., phone registration).
        phone_number = self.request.data.get('phone')
        customer_email = self.request.data.get('email')
        if not customer_email:
            if phone_number:
                customer_email = f"no-email-{phone_number}@neetechs.com"
            else:
                # Fallback if neither email nor phone is provided, though this case might be handled by serializer validation.
                customer_email = f"no-email-anonymous@{settings.DEFAULT_DOMAIN or 'neetechs.com'}"


        customer = stripe.Customer.create(
            email=customer_email,
            payment_method='pm_card_visa',  # Sets 'pm_card_visa' as a default payment method.
            invoice_settings={
                'default_payment_method': 'pm_card_visa', # Ensures future invoices use this payment method.
            },
        )

        user = serializer.save(self.request)
        self.token = create_knox_token(None, user, None)
        identifier = self.request.data.get('email') or self.request.data.get('phone')
        instance = CustomUser.objects.filter(email=identifier).first() or CustomUser.objects.filter(phone=identifier).first()

        # Create a mutable copy of request.data to add stripeCustomerId
        profile_data = self.request.data.copy()
        profile_data['stripeCustomerId'] = customer.id
        # If 'name' is not provided, it can be defaulted from 'first_name' here or handled by model's pre_save.
        # profile_data['name'] = profile_data.get('first_name')

        # Update the user's profile with the stripeCustomerId and other potential data.
        serializer1 = ProfileSerializer(instance,data=profile_data, partial=True)
        if serializer1.is_valid():
            serializer1.save()
        complete_signup(self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None, signal_kwargs={'sociallogin': None})
        return user

    
class SocialLoginView_(SocialLoginView):
    """
    Customized SocialLoginView to include the Knox token directly in the login response.
    This is useful for client-side applications that need both user details and the
    authentication token immediately after a successful social login.
    It extends the standard SocialLoginView from dj_rest_auth.
    """
    permission_classes = [AllowAny]
    def get_response(self):
        serializer_class = self.get_response_serializer()
        
        data = {
            'user': self.user,
            'token': self.token[1]
        }
        serializer = serializer_class(instance=data, context={'request': self.request})

        return Response(serializer.data, status=200)

class FacebookLogin(SocialLoginView_):
    adapter_class = FacebookOAuth2Adapter

class GoogleLogin(SocialLoginView_):
    permission_classes = [AllowAny]
    adapter_class = GoogleOAuth2Adapter
    #callback_url = settings.GOOGLE_AUTH_CALLBACK_URL
    #client_class = OAuth2Client
    # The following commented-out 'login' method provides an example of how one might
    # override the default social login behavior. This could be used to explicitly
    # enable session-based authentication alongside token authentication,
    # especially if `REST_SESSION_LOGIN` is set to True in Django settings.
    # It's kept here for future reference or potential customization needs.
    # def login(self):
    #     self.user = self.serializer.validated_data['user']
    #     self.token, created = self.token_model.objects.get_or_create(
    #             user = self.user)
    #     if getattr(settings, 'REST_SESSION_LOGIN', True): # Check if session login is enabled
    #         if not hasattr(self.user, 'backend'): # Ensure user has a backend attribute
    #             self.user.backend = 'django.contrib.auth.backends.ModelBackend'
    #         login(self.request, self.user) # Perform session login

class EmailConfirmation(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        # Attempt to retrieve the user by the provided email.
        user = get_object_or_404(CustomUser, email=request.data['email'])
        # Check if the user's email address is already verified.
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            # If email is already verified, inform the user.
            return Response({'message': 'This email is already verified. Try to login and logout again to refresh the app.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If not verified, attempt to send a confirmation email.
            try:
                send_email_confirmation(request, user=user)
                return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)
            except APIException:
                # Handle cases where email sending might fail or user does not exist (though get_object_or_404 should catch this).
                return Response({'message': 'This email does not exist, please create a new account'}, status=status.HTTP_403_FORBIDDEN)