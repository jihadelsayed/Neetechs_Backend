from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from dj_rest_auth.views import LoginView

from ...serializers.public import PublicUserSerializer


class KnoxLoginView(LoginView):
    permission_classes = [AllowAny]

    def get_response(self):
        return Response(
            {
                "token": self.token[1],
                "user": PublicUserSerializer(self.user, context={"request": self.request}).data,
            },
            status=200,
        )
