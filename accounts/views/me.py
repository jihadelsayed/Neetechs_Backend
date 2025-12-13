from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from ..serializers.public import PublicUserSerializer


class MeView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PublicUserSerializer

    def get_object(self):
        return self.request.user
