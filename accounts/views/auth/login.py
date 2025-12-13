from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from dj_rest_auth.views import LoginView

from drf_spectacular.utils import extend_schema
from ...serializers.login import LoginRequestSerializer
from ...serializers.public import PublicUserSerializer
from ...utils.knox import create_knox_token

from accounts.serializers import AuthResponseSerializer





@extend_schema(
    request=LoginRequestSerializer,
    responses={200: AuthResponseSerializer},
    tags=["accounts-auth"],
)
class KnoxLoginView(LoginView):
    permission_classes = [AllowAny]
    serializer_class = LoginRequestSerializer  # IMPORTANT: help spectacular

    def get_response(self):
        token = create_knox_token(None, self.user, None)
        return Response(
            {"token": token, "user": PublicUserSerializer(self.user, context={"request": self.request}).data},
            status=200,
        )
