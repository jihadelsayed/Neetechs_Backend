"""Admin configurations for the Service app.

This file registers the models from the Service app with the Django admin interface,
allowing administrators to manage service posts, categories, locations, and comments.
"""
from django.contrib import admin

# Register your models here.
from .models import ModelComments,ServicePost, ModelState, ModelCountry, ModelCategory,ModelSubCategory

# Register ServicePost and related models
admin.site.register(ServicePost)

# Register category models
admin.site.register(ModelCategory)
admin.site.register(ModelSubCategory)

# Register location models
admin.site.register(ModelCountry)
admin.site.register(ModelState)

# Register comments model
admin.site.register(ModelComments)