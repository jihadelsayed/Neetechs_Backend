from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from allauth.account.models import EmailAddress
from django.http.response import JsonResponse
from rest_framework.exceptions import APIException
from knox_allauth.models import CustomUser
from Profile.serializer import ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from Neetechs import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

from allauth.account.utils import complete_signup, send_email_confirmation
from allauth.account import app_settings as allauth_settings

from .serializer import KnoxSerializer, UserSerializer
from .utils import create_knox_token


from django.conf import settings


class KnoxLoginView(LoginView):

    def get_response(self):
        serializer_class = self.get_response_serializer()

        data = {
            'user': self.user,
            'token': self.token[1]
        }
        serializer = serializer_class(instance=data, context={'request': self.request})

        return Response(serializer.data, status=200)


class KnoxRegisterView(RegisterView):
    def get_response_data(self, user):
        return KnoxSerializer({'user': user, 'token': self.token[1]}).data
    def get_object(self,email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist as e:
            return Response( {"error":"Given Profile was not found."},status=404)

    def perform_create(self, serializer):
        customer = stripe.Customer.create(
            email=self.request.data['email'],
            payment_method='pm_card_visa',
            invoice_settings={
                'default_payment_method': 'pm_card_visa',
            },
        )
        user = serializer.save(self.request)
        self.token = create_knox_token(None, user, None)
        instance = self.get_object(self.request.data['email'])
        #if not self.request.data._mutable:
         #   self.request.data._mutable = True
        data =self.request.data
        #_mutable = self.request.data._mutable
        #self.request.data._mutable = True
        data['stripeCustomerId'] = customer.id
        data['name'] = data['first_name']
       # self.request.data._mutable = False
        #self.request.data._mutable = _mutable

        
        serializer1 = ProfileSerializer(instance,data=data, partial=True)
        if serializer1.is_valid():
            serializer1.save()
        complete_signup(self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None, signal_kwargs={'sociallogin': None})
        return user

    
class SocialLoginView_(SocialLoginView):

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
    adapter_class = GoogleOAuth2Adapter
    #callback_url = settings.GOOGLE_AUTH_CALLBACK_URL
    #client_class = OAuth2Client
    # Try overriding social login
    # see: https://www.bountysource.com/issues/10278183-social-rest-auth-with-rest_session_login-true
    # def login(self):
    #     self.user = self.serializer.validated_data['user']
    #     self.token, created = self.token_model.objects.get_or_create(
    #             user = self.user)
    #     if getattr(settings, 'REST_SESSION_LOGIN', True):
    #         if not hasattr(self.user, 'backend'):
    #             self.user.backend = 'django.contrib.auth.backends.ModelBackend'
    #         login(self.request, self.user)

class EmailConfirmation(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        user = get_object_or_404(CustomUser, email=request.data['email'])
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            return Response({'message': 'This email is already verified. Try to login and logout again to refresh the app.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                send_email_confirmation(request, user=user)
                return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)
            except APIException:
                return Response({'message': 'This email does not exist, please create a new account'}, status=status.HTTP_403_FORBIDDEN)