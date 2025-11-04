"""API URL patterns for the Service app (v1)."""
from django.urls import path
from rest_framework.decorators import api_view

from Neetechs.api_router import ServicePostViewSet
from Service.api.views import (
    ApiServiceListView,
    CategoryViewSet,
    CityViewSet,
    CommentsViewSet,
    CountryViewSet,
    DisLikesViewSet,
    LikesViewSet,
    PostLikesAPIView,
    StateViewSet,
    SubCategoryViewSet,
    api_create_service_view,
    api_delete_service_view,
    api_detail_service_view,
    api_is_employee_of_servicepost,
    api_update_service_view,
    servicesListAPIView,
)

app_name = "services"

service_collection_view = ServicePostViewSet.as_view({"get": "list"})


@api_view(["GET", "POST"])
def services_collection(request, *args, **kwargs):
    """List services (GET) or create a service (POST)."""
    if request.method == "POST":
        return api_create_service_view(request)
    return service_collection_view(request, *args, **kwargs)


@api_view(["GET", "PUT", "DELETE"])
def services_detail(request, slug, *args, **kwargs):
    """Retrieve, update, or delete a service post."""
    if request.method == "GET":
        return api_detail_service_view(request, slug=slug)
    if request.method == "PUT":
        return api_update_service_view(request, slug=slug)
    return api_delete_service_view(request, slug=slug)


urlpatterns = [
    path("", services_collection, name="collection"),
    path("featured/", ApiServiceListView.as_view(), name="featured"),
    path("filters/search/", servicesListAPIView.as_view(), name="filters-search"),
    path("filters/category/", CategoryViewSet.as_view(), name="filters-category"),
    path("filters/sub_category/", SubCategoryViewSet.as_view(), name="filters-sub-category"),
    path("filters/country/", CountryViewSet.as_view(), name="filters-country"),
    path("filters/state/", StateViewSet.as_view(), name="filters-state"),
    path("filters/city/", CityViewSet.as_view(), name="filters-city"),
    path("filters/comments/", CommentsViewSet.as_view(), name="filters-comments"),
    path("filters/likes/", LikesViewSet.as_view(), name="filters-likes"),
    path("filters/dislikes/", DisLikesViewSet.as_view(), name="filters-dislikes"),
    path("search/", servicesListAPIView.as_view(), name="search"),
    path("list/", ApiServiceListView.as_view(), name="list"),
    path("likes/toggle/", PostLikesAPIView.as_view(), name="likes-toggle"),
    path("<slug:slug>/is-employee/", api_is_employee_of_servicepost, name="is-employee"),
    path("reactions/", PostLikesAPIView.as_view(), name="reactions"),
    path("<slug:slug>/ownership/", api_is_employee_of_servicepost, name="ownership"),
    path("<slug:slug>/", services_detail, name="detail"),
]
