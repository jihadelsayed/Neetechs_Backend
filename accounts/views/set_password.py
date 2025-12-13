from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from knox.models import AuthToken


from ..serializers.auth import SetPasswordSerializer
from ..serializers.public import PublicUserSerializer
from ..utils.knox import create_knox_token
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["accounts-security"])
class SetPasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password"]

        user = request.user
        user.set_password(password)
        user.save(update_fields=["password"])

        # Invalidate all existing tokens (critical)
        AuthToken.objects.filter(user=user).delete()

        # Issue a fresh token so the client keeps a valid session
        token = create_knox_token(user)

        return Response(
            {
                "detail": "Password set successfully.",
                "token": token,
                "user": PublicUserSerializer(user, context={"request": request}).data,
            },
            status=200,
        )
