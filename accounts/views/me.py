from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from ..serializers.public import PublicUserSerializer

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["accounts-me"])
class MeView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PublicUserSerializer

    def get_object(self):
        return self.request.user
