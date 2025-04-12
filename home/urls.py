from django.urls import path

from .views import HomeSliderAPIView,HomeContainersAPIView, github_webhook


urlpatterns = [
    path('api/home/list/HomeSlider', HomeSliderAPIView.as_view()),
    
    path('api/home/list/HomeContainers', HomeContainersAPIView.as_view()),
    path("github-webhook/", github_webhook, name="github-webhook"),

]