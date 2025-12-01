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
            "thumbnail",
            "stripe_price_id",
            "bullets",
            "whatsInside",
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
        ]
