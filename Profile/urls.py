"""URL patterns for the Profile app, handling routes for user profiles
and their detailed sections like experience, studies, skills, and interests.
"""
from django.urls import path, include
from .views import (ProfilesAPIView,ProfileAPIView,
Kompetenser_intygAPIView, IntressenAPIView, StudierAPIView, ErfarenhetAPIView,
Kompetenser_intygsPostAPIView, IntressensPostAPIView, StudiersPostAPIView, ErfarenhetsPostAPIView,
StudiersListAPIView,IntressensListAPIView,ErfarenhetsListAPIView,ProfilesListAPIView,Kompetenser_intygsListAPIView,AllProfileInfoAPIView
)
from rest_framework import routers


# Defines the URL routes for the Profile app's API endpoints.
urlpatterns = [
    # Lists all user profiles with filtering capabilities.
    path('profiles/', ProfilesListAPIView.as_view()),
    # Retrieve, update, or delete a specific user profile by site_id.
	path('profile/<str:site_id>/', ProfileAPIView.as_view()),
    # Retrieve all combined profile information for a specific user by site_id.
	path('allprofileinfo/<str:site_id>/', AllProfileInfoAPIView.as_view()),

    # Lists all Kompetenser_intyg (skills/certificates) entries.
    path('profile/list/Kompetenser_intygs', Kompetenser_intygsListAPIView.as_view()),
    # Create a new Kompetenser_intyg (skill/certificate) entry.
    path('profile/post/Kompetenser_intygs', Kompetenser_intygsPostAPIView.as_view()),
    # Retrieve, update, or delete a specific Kompetenser_intyg (skill/certificate) by its ID.
	path('profile/Kompetenser_intyg/<int:id>/', Kompetenser_intygAPIView.as_view()),
    
    # Lists all Intressen (interests) entries.
    path('profile/list/Intressens', IntressensListAPIView.as_view()),
    # Create a new Intressen (interest) entry.
    path('profile/post/Intressens', IntressensPostAPIView.as_view()),
    # Retrieve, update, or delete a specific Intressen (interest) by its ID.
	path('profile/Intressen/<int:id>/', IntressenAPIView.as_view()),

    # Lists all Studier (studies) entries.
    path('profile/list/Studiers', StudiersListAPIView.as_view()),
    # Create a new Studier (study) entry.
    path('profile/post/Studiers', StudiersPostAPIView.as_view()),
    # Retrieve, update, or delete a specific Studier (study) by its ID.
	path('profile/Studier/<int:id>/', StudierAPIView.as_view()),

    # Lists all Erfarenhet (experience) entries.
    path('profile/list/Erfarenhets', ErfarenhetsListAPIView.as_view()),
    # Create a new Erfarenhet (experience) entry.
    path('profile/post/Erfarenhets', ErfarenhetsPostAPIView.as_view()),
    # Retrieve, update, or delete a specific Erfarenhet (experience) by its ID.
	path('profile/Erfarenhet/<int:id>/', ErfarenhetAPIView.as_view()),
]