from django.contrib import admin
from .models import Tree

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "is_public", "slug", "created_at")
    search_fields = ("title", "owner__email")
    list_filter = ("is_public",)
