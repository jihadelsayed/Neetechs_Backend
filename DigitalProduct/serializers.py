from rest_framework import serializers
from .models import DigitalProduct, DigitalProductCategory


class DigitalProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalProductCategory
        fields = ["id", "name", "slug"]


class DigitalProductListSerializer(serializers.ModelSerializer):
    category = DigitalProductCategorySerializer(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = DigitalProduct
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "price",  # we'll add property below
            "category",
            "thumbnail_url",
            "version",
        ]

    def get_thumbnail_url(self, obj):
        if obj.thumbnail and hasattr(obj.thumbnail, "url"):
            return obj.thumbnail.url
        return None


class DigitalProductDetailSerializer(serializers.ModelSerializer):
    category = DigitalProductCategorySerializer(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = DigitalProduct
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "price",
            "category",
            "thumbnail_url",
            "version",
            "stripe_price_id",
        ]

    def get_thumbnail_url(self, obj):
        if obj.thumbnail and hasattr(obj.thumbnail, "url"):
            return obj.thumbnail.url
        return None
