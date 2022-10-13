from django.urls import path, include
from .views import (ProfilesAPIView,ProfileAPIView,
Kompetenser_intygAPIView, IntressenAPIView, StudierAPIView, ErfarenhetAPIView,
Kompetenser_intygsPostAPIView, IntressensPostAPIView, StudiersPostAPIView, ErfarenhetsPostAPIView,
StudiersListAPIView,IntressensListAPIView,ErfarenhetsListAPIView,ProfilesListAPIView,Kompetenser_intygsListAPIView,AllProfileInfoAPIView
)
from rest_framework import routers


urlpatterns = [
    path('api/profiles/', ProfilesListAPIView.as_view()),
	path('api/profile/<str:site_id>/', ProfileAPIView.as_view()),
	path('api/allprofileinfo/<str:site_id>/', AllProfileInfoAPIView.as_view()),

    path('api/profile/list/Kompetenser_intygs', Kompetenser_intygsListAPIView.as_view()),
    path('api/profile/post/Kompetenser_intygs', Kompetenser_intygsPostAPIView.as_view()),
	path('api/profile/Kompetenser_intyg/<int:id>/', Kompetenser_intygAPIView.as_view()),
    
    path('api/profile/list/Intressens', IntressensListAPIView.as_view()),
    path('api/profile/post/Intressens', IntressensPostAPIView.as_view()),
	path('api/profile/Intressen/<int:id>/', IntressenAPIView.as_view()),

    path('api/profile/list/Studiers', StudiersListAPIView.as_view()),
    path('api/profile/post/Studiers', StudiersPostAPIView.as_view()),
	path('api/profile/Studier/<int:id>/', StudierAPIView.as_view()),

    path('api/profile/list/Erfarenhets', ErfarenhetsListAPIView.as_view()),
    path('api/profile/post/Erfarenhets', ErfarenhetsPostAPIView.as_view()),
	path('api/profile/Erfarenhet/<int:id>/', ErfarenhetAPIView.as_view()),
]