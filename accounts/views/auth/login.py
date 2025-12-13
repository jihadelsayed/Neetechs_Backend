from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from dj_rest_auth.views import LoginView

from ...serializers.public import PublicUserSerializer
from ...utils import create_knox_token


class KnoxLoginView(LoginView):
    permission_classes = [AllowAny]

    def get_response(self):
        """
        Return a stable auth response:
        { "token": "...", "user": {...} }

        We generate the token ourselves to avoid relying on dj-rest-auth's internal
        token tuple shape (self.token[1]).
        """
        token = create_knox_token(None, self.user, None)

        return Response(
            {
                "token": token,
                "user": PublicUserSerializer(self.user, context={"request": self.request}).data,
            },
            status=200,
        )
