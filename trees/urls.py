# apps/trees/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TreeViewSet

router = DefaultRouter()
router.register(r"trees", TreeViewSet, basename="trees")

urlpatterns = [ path("", include(router.urls)) ]
