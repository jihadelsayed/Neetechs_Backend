"""Router configuration for tree resources under /api/v1/trees/."""
from rest_framework.routers import DefaultRouter

from .views import TreeViewSet

app_name = "trees"

router = DefaultRouter()
router.register("", TreeViewSet, basename="trees")

urlpatterns = router.urls
