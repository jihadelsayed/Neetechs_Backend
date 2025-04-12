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
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def github_webhook(request):
    # Secret header check
    secret_token = request.headers.get("X-DEPLOY-SECRET")
    print(settings.GITHUB_WEBHOOK_SECRET)
    if secret_token != settings.GITHUB_WEBHOOK_SECRET:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    if request.method == "POST":
        try:
            subprocess.run(["bash", "/var/www/Neetechs_Script/deploy.sh"], check=True)
            return JsonResponse({"status": "deployment triggered"})
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"detail": "Method not allowed"}, status=405)
# اللهم صلي على سيدنا محمد