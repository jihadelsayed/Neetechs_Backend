"""Home app API endpoints scoped under /api/v1/home/."""
from django.urls import path

from .views import HomeContainersAPIView, HomeSliderAPIView, github_webhook

app_name = "home"

urlpatterns = [
    path("slider/", HomeSliderAPIView.as_view(), name="slider"),
    path("containers/", HomeContainersAPIView.as_view(), name="containers"),
    path("github-webhook/", github_webhook, name="github-webhook"),
]
