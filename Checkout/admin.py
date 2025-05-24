"""Admin configurations for the Checkout app.

This file registers Checkout app models with the Django admin interface,
allowing administrators to manage them.
"""
from django.contrib import admin
from .models import ServiceOrder
# Register your models here.
# Register the ServiceOrder model with the admin site.
admin.site.register(ServiceOrder)