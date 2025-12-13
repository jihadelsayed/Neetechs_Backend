from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers import PublicUserSerializer

class MeView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PublicUserSerializer

    def get(self, request):
        return Response(self.get_serializer(request.user).data, status=200)
