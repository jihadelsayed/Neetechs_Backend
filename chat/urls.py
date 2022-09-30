from django.urls import path, include
from chat.views import ThreadView
from chat.viewsets import MessageAPIView,MessagesAPIView,ThreadViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('thread', ThreadViewSet)
#router.register('message', MessageAPIView)

urlpatterns = [
    path('chat/<str:username>/', ThreadView.as_view()),
	path('api/chat/', include(router.urls)),
	path('api/chat/messages/<str:site_id>/', MessagesAPIView.as_view()),
	path('api/chat/message/<int:id>/', MessageAPIView.as_view()),
    #path('api/chat/threads/<str:site_id>/', ThreadsAPIView.as_view()),
    #path('api/chat/threads/', ThreadViewSet()),

]