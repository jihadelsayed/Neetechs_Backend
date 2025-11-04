"""API URL patterns for Service helpers under the versioned namespace."""
from django.urls import path

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
    api_is_employee_of_servicepost,
    servicesListAPIView,
)

app_name = "service_api"

urlpatterns = [
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
]
