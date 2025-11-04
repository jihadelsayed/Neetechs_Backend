"""URL patterns for profile resources under /api/v1/profile/."""
from django.urls import path

from .views import (
    AllProfileInfoAPIView,
    ErfarenhetAPIView,
    ErfarenhetsListAPIView,
    ErfarenhetsPostAPIView,
    IntressenAPIView,
    IntressensListAPIView,
    IntressensPostAPIView,
    Kompetenser_intygAPIView,
    Kompetenser_intygsListAPIView,
    Kompetenser_intygsPostAPIView,
    ProfileAPIView,
    ProfilesListAPIView,
    StudierAPIView,
    StudiersListAPIView,
    StudiersPostAPIView,
)

urlpatterns = [
    path("profiles/", ProfilesListAPIView.as_view(), name="profiles-list"),
    path("<str:site_id>/", ProfileAPIView.as_view(), name="profile-detail"),
    path("all/<str:site_id>/", AllProfileInfoAPIView.as_view(), name="profile-all"),
    path("certifications/", Kompetenser_intygsListAPIView.as_view(), name="certifications-list"),
    path("certifications/create/", Kompetenser_intygsPostAPIView.as_view(), name="certifications-create"),
    path("certifications/<int:id>/", Kompetenser_intygAPIView.as_view(), name="certifications-detail"),
    path("interests/", IntressensListAPIView.as_view(), name="interests-list"),
    path("interests/create/", IntressensPostAPIView.as_view(), name="interests-create"),
    path("interests/<int:id>/", IntressenAPIView.as_view(), name="interests-detail"),
    path("studies/", StudiersListAPIView.as_view(), name="studies-list"),
    path("studies/create/", StudiersPostAPIView.as_view(), name="studies-create"),
    path("studies/<int:id>/", StudierAPIView.as_view(), name="studies-detail"),
    path("experience/", ErfarenhetsListAPIView.as_view(), name="experience-list"),
    path("experience/create/", ErfarenhetsPostAPIView.as_view(), name="experience-create"),
    path("experience/<int:id>/", ErfarenhetAPIView.as_view(), name="experience-detail"),
]
