from django.urls import path

from .views import HomeSliderAPIView,HomeContainersAPIView


urlpatterns = [
    path('api/home/list/HomeSlider', HomeSliderAPIView.as_view()),
    
    path('api/home/list/HomeContainers', HomeContainersAPIView.as_view()),
    path('github-webhook', HomeContainersAPIView.as_view()),

]