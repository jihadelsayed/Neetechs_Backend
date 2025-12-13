from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from ...serializers.public import PublicUserSerializer


class SocialLoginView_(SocialLoginView):
    permission_classes = [AllowAny]

    def get_response(self):
        return Response(
            {
                "token": self.token[1],
                "user": PublicUserSerializer(self.user, context={"request": self.request}).data,
            },
            status=200,
        )


class FacebookLogin(SocialLoginView_):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView_):
    adapter_class = GoogleOAuth2Adapter
