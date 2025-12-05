
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers.auth import SetPasswordSerializer

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

        return Response({"detail": "Password set successfully."}, status=200)
