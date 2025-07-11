# اللهم صلي على سيدنا محمد
from django.conf import settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from knox.auth import TokenAuthentication
from .models import HomeSliderMoudel,HomeContainersModel
from .serializer import HomeSliderSerializer,HomeContainersSerializer

from django_filters.rest_framework import DjangoFilterBackend#,SearchFilter,OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination

import subprocess
from django.http import JsonResponse


class HomeSliderAPIView(ListAPIView):
    queryset = HomeSliderMoudel.objects.all()
    serializer_class = HomeSliderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

class HomeContainersAPIView(ListAPIView):
    queryset = HomeContainersModel.objects.all()
    serializer_class = HomeContainersSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination
 
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import subprocess

@csrf_exempt
@api_view(["POST"])
@authentication_classes([])  # disable all auth
@permission_classes([AllowAny])  # allow any request
def github_webhook(request):
    secret_token = request.headers.get("X-DEPLOY-SECRET")

    if secret_token != settings.GITHUB_WEBHOOK_SECRET:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        subprocess.run(["bash", "/var/www/Neetechs_Script/deploy.sh"], check=True)
        return JsonResponse({"status": "Deployment triggered"})
    except subprocess.CalledProcessError as e:
        return JsonResponse({"error": str(e)}, status=500)

