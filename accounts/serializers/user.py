from rest_framework import serializers
from allauth.account.models import EmailAddress

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Legacy-compatible user serializer.

    IMPORTANT:
    - This stays inside accounts ONLY for backwards compatibility.
    - Cross-app Profile/Service aggregation does NOT belong here.
    - If you need the "full profile payload", build it in the Profile app instead.
    """

    # Keep legacy keys so old clients don't break
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
        # NOTE: depth=1 removed on purpose (slow + unpredictable)
        fields = (
            "id",
            "email",
            "emailConfirmed",
            "name",
            "first_name",
            "last_name",
            "phone",
            "username",
            "handle",
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
            # legacy aggregates (kept but now safe)
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
            "username",
            "handle",
            "stripe_customer_id",
        )

    # ---- Derived fields ----
    def get_emailConfirmed(self, obj):
        # Safe, single query
        return (
            EmailAddress.objects.filter(email__iexact=obj.email, verified=True).exists()
            if obj.email
            else False
        )

    # ---- Legacy aggregate stubs ----
    # These used to pull data from other apps. That does not belong in accounts.
    # Keep keys for compatibility; return empty/None to avoid slow cross-app coupling.
    def get_Interest(self, obj):
        return []

    def get_CompetenceCertificate(self, obj):
        return []

    def get_Study(self, obj):
        return []

    def get_Experience(self, obj):
        return []

    def get_Categories(self, obj):
        return []

    def get_subCategories(self, obj):
        return []

    def get_CategoryLastupdate(self, obj):
        return None

    def get_SubcategoryLastupdate(self, obj):
        return None


class KnoxSerializer(serializers.Serializer):
    """
    Legacy wrapper. Prefer using PublicUserSerializer + explicit auth responses.
    Kept so older code importing KnoxSerializer doesn't break.
    """
    token = serializers.CharField()
    user = UserSerializer()
