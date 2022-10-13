from django.contrib import admin

# Register your models here.
from .models import ModelComments,ServicePost, ModelState, ModelCountry, ModelCategory,ModelSubCategory

admin.site.register(ServicePost)
admin.site.register(ModelSubCategory)
admin.site.register(ModelCountry)
admin.site.register(ModelState)
admin.site.register(ModelCategory)

admin.site.register(ModelComments)