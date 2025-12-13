from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers.auth import SetHandleSerializer
from ..serializers.public import PublicUserSerializer

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["accounts-me"])
class SetHandleView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SetHandleSerializer

    def post(self, request):
        s = self.get_serializer(data=request.data, context={"request": request})
        s.is_valid(raise_exception=True)

        request.user.handle = s.validated_data["handle"]
        request.user.save(update_fields=["handle"])

        return Response(
            {
                "detail": "Handle updated",
                "user": PublicUserSerializer(request.user, context={"request": request}).data,
            },
            status=200,
        )
