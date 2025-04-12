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
    if request.method == "POST":
        try:
            subprocess.run(["/bin/bash", "/var/www/Neetechs_Script/deploy.sh"], check=True)
            return JsonResponse({"status": "deployment started"})
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"detail": "Method not allowed"}, status=405)