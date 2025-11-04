"""Central DRF router viewsets for versioned API endpoints."""
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from Category.models import ModelCategory
from Category.serializers import CategorySerializer
from Service.models import ServicePost
from Service.api.serializers import ServicePostSerializer
from chat.viewsets import ThreadViewSet  # existing chat viewset
from knox_allauth.models import CustomUser
from Profile.serializer import ProfileSerializer
from home.models import HomeSliderMoudel, HomeContainersModel
from home.serializer import HomeSliderSerializer, HomeContainersSerializer


class ReadOnlyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Helper mixin for read-only resources."""

    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViewSet(ReadOnlyViewSet):
    queryset = ModelCategory.objects.all()
    serializer_class = CategorySerializer


class ServicePostViewSet(ReadOnlyViewSet):
    queryset = ServicePost.objects.all().order_by("-createdAt")
    serializer_class = ServicePostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "title",
        "site_id",
        "beskrivning",
        "slug",
        "city",
        "state",
        "country",
        "underCategory",
        "category",
        "status",
        "bedomning",
        "updatedAt",
        "pris",
        "tillganligFran",
        "tillganligTill",
        "employee__site_id",
    ]
    search_fields = ["title", "beskrivning", "slug", "city", "state", "country"]
    ordering_fields = ["createdAt", "updatedAt", "pris"]


class ProfileViewSet(ReadOnlyViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "site_id",
        "profession",
        "city",
        "state",
        "country",
    ]
    search_fields = ["first_name", "site_id", "profession", "city", "state", "country"]
    ordering_fields = ["first_name", "date_joined"]


class HomeSliderViewSet(ReadOnlyViewSet):
    queryset = HomeSliderMoudel.objects.all()
    serializer_class = HomeSliderSerializer


class HomeContainersViewSet(ReadOnlyViewSet):
    queryset = HomeContainersModel.objects.all()
    serializer_class = HomeContainersSerializer


# Re-export the chat thread viewset for router registration convenience.
ChatThreadViewSet = ThreadViewSet
