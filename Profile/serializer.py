from allauth.account.models import EmailAddress
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from accounts.models import User
from Service.models import ModelCategory, ModelSubCategory

from .models import Experience, Interest, CompetenceCertificate, Study


class ProfileSerializerBase(serializers.ModelSerializer):
    """
    Shared serializer setup for profile payloads.

    Keeps the existing camelCase field names in API responses but maps them to the
    snake_case model fields.
    """

    member_since = serializers.DateTimeField(format="%Y-%m-%d", allow_null=True)
    CategoryLastupdate = serializers.SerializerMethodField()
    SubcategoryLastupdate = serializers.SerializerMethodField()
    emailConfirmed = serializers.SerializerMethodField()

    stripeCustomerId = serializers.CharField(
        source="stripe_customer_id", allow_blank=True, allow_null=True, read_only=True
    )
    subscriptionType = serializers.CharField(
        source="subscription_type", allow_blank=True, allow_null=True, read_only=True
    )
    Facebook_link = serializers.CharField(
        source="facebook_link", allow_blank=True, allow_null=True, read_only=True
    )
    Linkdin_link = serializers.CharField(
        source="linkedin_link", allow_blank=True, allow_null=True, read_only=True
    )
    othersSocialMedia = serializers.CharField(
        source="other_social_media", allow_blank=True, allow_null=True, read_only=True
    )

    @extend_schema_field(serializers.DateTimeField(allow_null=True))
    def get_CategoryLastupdate(self, obj):
        """Timestamp of the most recently updated category."""

        try:
            category_last_update = ModelCategory.objects.latest("updatedAt").updatedAt
        except ModelCategory.DoesNotExist:
            category_last_update = None
        return category_last_update

    @extend_schema_field(serializers.DateTimeField(allow_null=True))
    def get_SubcategoryLastupdate(self, obj):
        """Timestamp of the most recently updated sub-category."""

        try:
            subcategory_last_update = ModelSubCategory.objects.latest("updatedAt").updatedAt
        except ModelSubCategory.DoesNotExist:
            subcategory_last_update = None
        return subcategory_last_update

    @extend_schema_field(serializers.BooleanField(allow_null=True))
    def get_emailConfirmed(self, obj):
        """Whether the user's primary email is verified via allauth."""

        try:
            email_confirmed = EmailAddress.objects.get(email=obj.email).verified
        except EmailAddress.DoesNotExist:
            email_confirmed = None
        return email_confirmed


class ProfileSerializer(ProfileSerializerBase):
    """
    Serializes essential User profile data.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "stripeCustomerId",
            "emailConfirmed",
            "subscriptionType",
            "name",
            "CategoryLastupdate",
            "SubcategoryLastupdate",
            "email",
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
            "picture_medium",
            "picture_small",
            "picture_tag",
            "location",
            "address1",
            "address2",
            "zip_code",
            "city",
            "state",
            "country",
            "member_since",
            "picture",
            "Facebook_link",
            "twitter",
            "profile_completed",
            "Linkdin_link",
            "sms",
            "othersSocialMedia",
            "about",
        )

class InterestSerializer(serializers.ModelSerializer):
    """
    Serializes Interest (Interest) model instances, including the user's site_id.
    """
    site_id = serializers.SerializerMethodField() # Custom field to include user's site_id.
    @extend_schema_field(serializers.CharField())
    def get_site_id(self, obj):
        """Retrieves the site_id of the user associated with this interest."""
        return obj.username.site_id
    class Meta:
        model = Interest
        # Specifies the fields to include in the serialized output.
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name')

class CompetenceCertificateSerializer(serializers.ModelSerializer):
    """
    Serializes CompetenceCertificate (Skill/Certificate) model instances,
    including the user's site_id.
    """
    site_id = serializers.SerializerMethodField() # Custom field to include user's site_id.
    @extend_schema_field(serializers.CharField())
    def get_site_id(self, obj):
        """Retrieves the site_id of the user associated with this skill/certificate."""
        return obj.username.site_id
    class Meta:
        model = CompetenceCertificate
        # Specifies the fields to include in the serialized output.
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name')

class StudySerializer(serializers.ModelSerializer):
    """
    Serializes Study (Study) model instances, including the user's site_id.
    """
    site_id = serializers.SerializerMethodField() # Custom field to include user's site_id.
    @extend_schema_field(serializers.CharField())
    def get_site_id(self, obj):
        """Retrieves the site_id of the user associated with this study entry."""
        return obj.username.site_id
    class Meta:
        model = Study
        # Specifies the fields to include in the serialized output.
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name', 'plats', 'content', 'started_at', 'ended_at', 'degree')
        #read_only_fields = ('id',) # This line is commented out, review if read_only_fields are needed.


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Serializes Experience (Experience) model instances, including the user's site_id.
    """
    site_id = serializers.SerializerMethodField() # Custom field to include user's site_id.
    @extend_schema_field(serializers.CharField())
    def get_site_id(self, obj):
        """Retrieves the site_id of the user associated with this experience entry."""
        return obj.username.site_id
        
    class Meta:
        model = Experience
        # Specifies the fields to include in the serialized output.
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name', 'plats', 'content', 'started_at', 'ended_at','company')
    
class AllProfileInfoSerializer(ProfileSerializerBase):
    """
    Provides a comprehensive serialization of a User's profile,
    embedding their interests, skills, studies, and experiences directly in the output.
    Also includes category update timestamps and email confirmation status.
    """
    Interest = serializers.SerializerMethodField()
    CompetenceCertificate = serializers.SerializerMethodField()
    Study = serializers.SerializerMethodField()
    Experience = serializers.SerializerMethodField()

    class Meta:
        model = User
        # Specifies all fields to be included for a comprehensive profile view.
        fields = ('id', 'stripeCustomerId', 'emailConfirmed', 'subscriptionType', 'Interest', 'CompetenceCertificate', 'Study', 'Experience', 'CategoryLastupdate', 'SubcategoryLastupdate', 'email', 'name', 'first_name', 'phone', 'site_id', 'is_creator', 'bio', 'rating', 'members',
		          'followers', 'earning', 'profession', 'picture_medium', 'picture_small', 'picture_tag', 'location', 'address1', 'address2', 'zip_code', 'city', 'state', 'country', 'member_since', 'picture','Facebook_link','twitter','profile_completed','Linkdin_link','sms','othersSocialMedia','about')

    @extend_schema_field(serializers.ListSerializer(child=InterestSerializer()))
    def get_Interest(self, obj):
        """Retrieves and serializes the user's interests."""
        # .filter() returns a queryset, which doesn't raise DoesNotExist.
        # If no interests are found, an empty list will be serialized, which is the desired behavior.
        interest = Interest.objects.filter(username=obj.id)
        return InterestSerializer(interest, many=True).data

    @extend_schema_field(serializers.ListSerializer(child=CompetenceCertificateSerializer()))
    def get_CompetenceCertificate(self, obj):
        """Retrieves and serializes the user's skills/certificates."""
        competence_intyg = CompetenceCertificate.objects.filter(username=obj.id)
        return CompetenceCertificateSerializer(competence_intyg, many=True).data

    @extend_schema_field(serializers.ListSerializer(child=StudySerializer()))
    def get_Study(self, obj):
        """Retrieves and serializes the user's studies."""
        study = Study.objects.filter(username=obj.id)
        return StudySerializer(study, many=True).data

    @extend_schema_field(serializers.ListSerializer(child=ExperienceSerializer()))
    def get_Experience(self, obj):
        """Retrieves and serializes the user's work experiences."""
        experienceer = Experience.objects.filter(username=obj.id)
        return ExperienceSerializer(experienceer, many=True).data
