from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from accounts.serializers import AuthResponseSerializer

from ...serializers.public import PublicUserSerializer
from ...utils.knox import create_knox_token
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
@extend_schema(
    responses={200: AuthResponseSerializer},
    tags=["accounts-auth"],
)
class SocialLoginView_(SocialLoginView):
    permission_classes = [AllowAny]

    def get_response(self):
        try:
            token = create_knox_token(self.user)
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Social login provider not configured (missing SocialApp/Site)."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {
                "token": token,
                "user": PublicUserSerializer(self.user, context={"request": self.request}).data,
            },
            status=200,
        )


class FacebookLogin(SocialLoginView_):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView_):
    adapter_class = GoogleOAuth2Adapter
