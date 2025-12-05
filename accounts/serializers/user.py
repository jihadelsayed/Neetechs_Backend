
from rest_framework import serializers
from django.utils import timezone

from allauth.account.models import EmailAddress

from ..models import User as User

# Optional imports from other apps (guarded so this file doesn't explode if they aren't installed yet)
try:
    from Profile.serializer import (
        ExperienceSerializer,
        InterestSerializer,
        CompetenceCertificateSerializer,
        StudySerializer,
    )
    from Profile.models import (
        Experience,
        Interest,
        CompetenceCertificate,
        Study,
    )
except Exception:
    ExperienceSerializer = InterestSerializer = CompetenceCertificateSerializer = StudySerializer = None
    Experience = Interest = CompetenceCertificate = Study = None

try:
    from Service.models import ModelCategory, ModelSubCategory
    from Service.api.serializers import ServiceCategorySerializer, SubCategorySerializer
except Exception:
    ModelCategory = ModelSubCategory = None
    ServiceCategorySerializer = SubCategorySerializer = None


class UserSerializer(serializers.ModelSerializer):
    # Derived / related data
    emailConfirmed = serializers.SerializerMethodField()
    Interest = serializers.SerializerMethodField()
    CompetenceCertificate = serializers.SerializerMethodField()
    Study = serializers.SerializerMethodField()
    Experience = serializers.SerializerMethodField()
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
            "Interest",
            "CompetenceCertificate",
            "Study",
            "Experience",
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

    def get_Interest(self, obj):
        if not (Interest and InterestSerializer):
            return []
        qs = Interest.objects.filter(username=obj.id)
        return InterestSerializer(qs, many=True).data

    def get_CompetenceCertificate(self, obj):
        if not (CompetenceCertificate and CompetenceCertificateSerializer):
            return []
        qs = CompetenceCertificate.objects.filter(username=obj.id)
        return CompetenceCertificateSerializer(qs, many=True).data

    def get_Study(self, obj):
        if not (Study and StudySerializer):
            return []
        qs = Study.objects.filter(username=obj.id)
        return StudySerializer(qs, many=True).data

    def get_Experience(self, obj):
        if not (Experience and ExperienceSerializer):
            return []
        qs = Experience.objects.filter(username=obj.id)
        return ExperienceSerializer(qs, many=True).data

    def get_Categories(self, obj):
        if not (ModelCategory and ServiceCategorySerializer):
            return []
        qs = ModelCategory.objects.all()
        return ServiceCategorySerializer(qs, many=True).data

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
