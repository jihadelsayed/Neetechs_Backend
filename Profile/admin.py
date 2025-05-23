"""Admin configurations for the Profile app.

This file registers the models from the Profile app with the Django admin interface,
allowing administrators to manage user profile sections like experience,
studies, skills, and interests.
"""
from django.contrib import admin

# Register your models here.
from .models import Erfarenhet,Studier,Kompetenser_intyg,Intressen

# Register the Intressen model with the admin site.
admin.site.register(Intressen)
# Register the Kompetenser_intyg model with the admin site.
admin.site.register(Kompetenser_intyg)
# Register the Studier model with the admin site.
admin.site.register(Studier)
# Register the Erfarenhet model with the admin site.
admin.site.register(Erfarenhet)