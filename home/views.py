from rest_framework.permissions import IsAuthenticatedOrReadOnly
from knox.auth import TokenAuthentication
from .models import HomeSliderMoudel,HomeContainersModel
from .serializer import HomeSliderSerializer,HomeContainersSerializer

from django_filters.rest_framework import DjangoFilterBackend#,SearchFilter,OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination


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

