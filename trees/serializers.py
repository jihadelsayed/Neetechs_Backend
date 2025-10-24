from rest_framework import serializers
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from .models import Tree

User = get_user_model()

class TreeSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Tree
        fields = ("id", "title", "description", "slug", "is_public", "created_at", "owner", "owner_email")
        read_only_fields = ("id", "slug", "created_at", "owner")

    def _unique_slug(self, base: str) -> str:
        base = slugify(base) or "tree"
        slug = base
        i = 2
        while Tree.objects.filter(slug=slug).exists():
            slug = f"{base}-{i}"
            i += 1
        return slug

    def create(self, validated_data):
        # owner injected in the viewset; fallback here only if someone calls serializer directly
        owner = self.context.get("owner") or validated_data.get("owner")
        if not owner:
            owner = User.objects.order_by("id").first()
        title = validated_data.get("title", "Untitled")
        validated_data["slug"] = self._unique_slug(title)
        validated_data["owner"] = owner
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Regenerate slug if title changes
        if "title" in validated_data and validated_data["title"] != instance.title:
            validated_data["slug"] = self._unique_slug(validated_data["title"])
        # owner is read-only from API
        validated_data.pop("owner", None)
        return super().update(instance, validated_data)
