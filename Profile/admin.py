"""Admin configurations for the Profile app.

This file registers the models from the Profile app with the Django admin interface,
allowing administrators to manage user profile sections like experience,
studies, skills, and interests.
"""
from django.contrib import admin

# Register your models here.
from .models import Experience,Study,CompetenceCertificate,Interest

# Register the Interest model with the admin site.
admin.site.register(Interest)
# Register the CompetenceCertificate model with the admin site.
admin.site.register(CompetenceCertificate)
# Register the Study model with the admin site.
admin.site.register(Study)
# Register the Experience model with the admin site.
admin.site.register(Experience)