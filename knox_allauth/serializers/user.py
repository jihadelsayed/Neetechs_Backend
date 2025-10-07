
from rest_framework import serializers
from django.utils import timezone

from allauth.account.models import EmailAddress

from ..models import CustomUser as User

# Optional imports from other apps (guarded so this file doesn't explode if they aren't installed yet)
try:
    from Profile.serializer import (
        ErfarenhetSerializer,
        IntressenSerializer,
        Kompetenser_intygSerializer,
        StudierSerializer,
    )
    from Profile.models import (
        Erfarenhet,
        Intressen,
        Kompetenser_intyg,
        Studier,
    )
except Exception:
    ErfarenhetSerializer = IntressenSerializer = Kompetenser_intygSerializer = StudierSerializer = None
    Erfarenhet = Intressen = Kompetenser_intyg = Studier = None

try:
    from Service.models import ModelCategory, ModelSubCategory
    from Service.api.serializers import CategorySerializer, SubCategorySerializer
except Exception:
    ModelCategory = ModelSubCategory = None
    CategorySerializer = SubCategorySerializer = None


class UserSerializer(serializers.ModelSerializer):
    # Derived / related data
    emailConfirmed = serializers.SerializerMethodField()
    Intressen = serializers.SerializerMethodField()
    Kompetenser_intyg = serializers.SerializerMethodField()
    Studier = serializers.SerializerMethodField()
    Erfarenhet = serializers.SerializerMethodField()
    Categories = serializers.SerializerMethodField()
    subCategories = serializers.SerializerMethodField()
    CategoryLastupdate = serializers.SerializerMethodField()
    SubcategoryLastupdate = serializers.SerializerMethodField()

    class Meta:
        model = User
        depth = 1
        fields = (
            "id",
            "email",
            "emailConfirmed",
            "name",
            "first_name",
            "phone",
            "site_id",
            "is_creator",
            "bio",
            "rating",
            "members",
            "followers",
            "earning",
            "profession",
            "location",
            "address1",
            "address2",
            "zip_code",
            "city",
            "state",
            "country",
            "member_since",
            "picture",
            "picture_medium",
            "picture_small",
            "picture_tag",
            "facebook_link",
            "twitter",
            "linkedin_link",
            "other_social_media",
            "profile_completed",
            "stripe_customer_id",
            "subscription_type",
            "about",
            # related/derived
            "Intressen",
            "Kompetenser_intyg",
            "Studier",
            "Erfarenhet",
            "Categories",
            "subCategories",
            "CategoryLastupdate",
            "SubcategoryLastupdate",
        )
        read_only_fields = (
            "email",
            "rating",
            "members",
            "followers",
            "earning",
            "member_since",
            "site_id",
        )

    # ---- Derived fields ----
    def get_emailConfirmed(self, obj):
        return EmailAddress.objects.filter(email__iexact=obj.email, verified=True).exists() if obj.email else False

    def get_Intressen(self, obj):
        if not (Intressen and IntressenSerializer):
            return []
        qs = Intressen.objects.filter(username=obj.id)
        return IntressenSerializer(qs, many=True).data

    def get_Kompetenser_intyg(self, obj):
        if not (Kompetenser_intyg and Kompetenser_intygSerializer):
            return []
        qs = Kompetenser_intyg.objects.filter(username=obj.id)
        return Kompetenser_intygSerializer(qs, many=True).data

    def get_Studier(self, obj):
        if not (Studier and StudierSerializer):
            return []
        qs = Studier.objects.filter(username=obj.id)
        return StudierSerializer(qs, many=True).data

    def get_Erfarenhet(self, obj):
        if not (Erfarenhet and ErfarenhetSerializer):
            return []
        qs = Erfarenhet.objects.filter(username=obj.id)
        return ErfarenhetSerializer(qs, many=True).data

    def get_Categories(self, obj):
        if not (ModelCategory and CategorySerializer):
            return []
        qs = ModelCategory.objects.all()
        return CategorySerializer(qs, many=True).data

    def get_subCategories(self, obj):
        if not (ModelSubCategory and SubCategorySerializer):
            return []
        qs = ModelSubCategory.objects.all()
        return SubCategorySerializer(qs, many=True).data

    def get_CategoryLastupdate(self, obj):
        if not ModelCategory or not ModelCategory.objects.exists():
            return None
        return ModelCategory.objects.latest("updatedAt").updatedAt

    def get_SubcategoryLastupdate(self, obj):
        if not ModelSubCategory or not ModelSubCategory.objects.exists():
            return None
        return ModelSubCategory.objects.latest("updatedAt").updatedAt


class KnoxSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()
