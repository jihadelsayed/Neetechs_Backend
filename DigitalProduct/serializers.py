from rest_framework import serializers
from .models import DigitalProduct, DigitalProductBundle


class DigitalProductListSerializer(serializers.ModelSerializer):
    bullets = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    whatsInside = serializers.ListField(
        source="whats_inside",
        child=serializers.CharField(),
        required=False
    )

    class Meta:
        model = DigitalProduct
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "thumbnail",
            "file",
            "stripe_price_id",
            "version",
            "is_active",
            "created_at",
            "updated_at",
            "bullets",
            "whatsInside",
                        "price",
            "badge",
        ]


class DigitalProductDetailSerializer(serializers.ModelSerializer):
    bullets = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    whatsInside = serializers.ListField(
        source="whats_inside",
        child=serializers.CharField(),
        required=False
    )
    faqs = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )
    class Meta:
        model = DigitalProduct
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "thumbnail",
            "file",
            "stripe_price_id",
            "version",
            "is_active",
            "created_at",
            "updated_at",
            "bullets",
            "whatsInside",
            "faqs",
            "price",
            "badge",
        ]
