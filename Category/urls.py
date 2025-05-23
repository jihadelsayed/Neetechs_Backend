"""URL patterns for the Category app.

This file defines the URL routing for the Category application, mapping
URL paths to their corresponding views.
"""
from django.urls import path
from .views import CategoryByNameViewSet

app_name = 'Category' # Defines the application namespace for URLs.


urlpatterns = [ # List of URL patterns for the category app.
    # Maps URLs like /categories/SomeCategoryName/ to the CategoryByNameViewSet.
    # (Assuming these URLs are included under a '/categories/' prefix in the main urls.py)
    path('<str:name>/', CategoryByNameViewSet.as_view(), name='Category_list_by_name'),
]