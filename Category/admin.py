"""Admin configurations for the Category app.

This file is used to register Category models with the Django admin interface,
allowing administrators to manage categories.
"""
from django.contrib import admin

from .models import ModelCategory

# Register your models here.
# Register the ModelCategory with the admin site to make it manageable.
admin.site.register(ModelCategory)
