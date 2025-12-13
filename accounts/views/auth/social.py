from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from ...serializers.public import PublicUserSerializer
from ...utils import create_knox_token


class SocialLoginView_(SocialLoginView):
    permission_classes = [AllowAny]

    def get_response(self):
        token = create_knox_token(None, self.user, None)
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
