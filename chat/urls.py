"""Chat API URLs exposed under /api/v1/chat/."""
from django.urls import include, path
from rest_framework import routers

from chat.viewsets import MessageAPIView, MessagesAPIView, ThreadViewSet
from chat.views import ThreadView

app_name = "chat"

router = routers.DefaultRouter()
router.register("thread", ThreadViewSet)

urlpatterns = [
    path("<str:username>/", ThreadView.as_view(), name="thread-by-username"),
    path("", include(router.urls)),
    path("messages/<str:site_id>/", MessagesAPIView.as_view(), name="messages"),
    path("message/<int:id>/", MessageAPIView.as_view(), name="message-detail"),
]
