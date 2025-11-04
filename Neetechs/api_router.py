"""Central DRF router viewsets for versioned API endpoints."""
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from Category.models import ModelCategory
from Category.serializers import CategorySerializer
from Service.models import ServicePost
from Service.api.serializers import (
    ServicePostCreateSerializer,
    ServicePostSerializer,
    ServicePostUpdateSerializer,
)
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
    lookup_field = "name"
<<<<<<< Updated upstream
    lookup_value_regex = "[^/]+"
=======
    lookup_value_regex = r"[^/]+"
>>>>>>> Stashed changes


class ServicePostViewSet(viewsets.ModelViewSet):
    queryset = ServicePost.objects.all().order_by("-createdAt")
    serializer_class = ServicePostSerializer
    lookup_field = "slug"
    lookup_value_regex = r"[^/]+"
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_serializer_class(self):
        if self.action == "create":
            return ServicePostCreateSerializer
        if self.action in {"update", "partial_update"}:
            return ServicePostUpdateSerializer
        return ServicePostSerializer

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(employee=request.user)
        read_serializer = ServicePostSerializer(instance, context=self.get_serializer_context())
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _ensure_owner(self, instance: ServicePost) -> None:
        if instance.employee != self.request.user:
            raise PermissionDenied("You don't have permission to modify this service.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        self._ensure_owner(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        read_serializer = ServicePostSerializer(instance, context=self.get_serializer_context())
        return Response(read_serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self._ensure_owner(instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewSet(ReadOnlyViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "site_id"
    lookup_value_regex = "[^/]+"
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
