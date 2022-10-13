from django.contrib import admin

# Register your models here.
from .models import Erfarenhet,Studier,Kompetenser_intyg,Intressen

admin.site.register(Intressen)
admin.site.register(Kompetenser_intyg)
admin.site.register(Studier)
admin.site.register(Erfarenhet)