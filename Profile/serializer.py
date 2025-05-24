from allauth.account.models import EmailAddress
from rest_framework import serializers

from knox_allauth.models import CustomUser
from Service.models import ModelCategory, ModelSubCategory

from .models import Erfarenhet, Intressen, Kompetenser_intyg, Studier


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes essential CustomUser profile data, including timestamps for
    category/subcategory updates and email confirmation status.
    """
    member_since = serializers.DateTimeField(format='%Y-%m-%d')
    CategoryLastupdate = serializers.SerializerMethodField('get_CategorysLastupdate')
    SubcategoryLastupdate = serializers.SerializerMethodField('get_SubCategorysLastupdate')
    emailConfirmed = serializers.SerializerMethodField('get_emailConfirmed')

    class Meta:
        model = CustomUser
        # Specifies the fields to include in the serialized output.
        fields = ('id', 'stripeCustomerId', 'emailConfirmed', 'subscriptionType', 'name','CategoryLastupdate', 'SubcategoryLastupdate', 'email', 'first_name', 'phone', 'site_id', 'is_creator', 'bio', 'rating', 'members',
		          'followers', 'earning', 'profession', 'picture_medium', 'picture_small', 'picture_tag', 'location', 'address1', 'address2', 'zip_code', 'city', 'state', 'country', 'member_since', 'picture','Facebook_link','twitter','profile_completed','Linkdin_link','sms','othersSocialMedia','about')
	
    def get_CategorysLastupdate(self, obj):
        """Retrieves the timestamp of the most recently updated ModelCategory."""
        try:
            # Corrected variable name and exception type
            category_last_update = ModelCategory.objects.all().latest('updatedAt').updatedAt
        except ModelCategory.DoesNotExist:
            category_last_update = None
        return category_last_update

    def get_emailConfirmed(self, obj):
        """Checks if the user's email address is verified."""
        try:
            # Corrected variable name and exception type
            email_confirmed = EmailAddress.objects.get(email=obj.email).verified
        except EmailAddress.DoesNotExist: # Corrected exception type
            email_confirmed = None
        return email_confirmed
                
    def get_SubCategorysLastupdate(self, obj):
        """Retrieves the timestamp of the most recently updated ModelSubCategory."""
        try:
            # Corrected variable name and exception type
            subcategory_last_update = ModelSubCategory.objects.all().latest('updatedAt').updatedAt
        except ModelSubCategory.DoesNotExist: # Corrected exception type
            subcategory_last_update = None
        return subcategory_last_update

class IntressenSerializer(serializers.ModelSerializer):
    """
    Serializes Intressen (Interest) model instances, including the user's site_id.
    """
    site_id = serializers.SerializerMethodField() # Custom field to include user's site_id.
    def get_site_id(self, obj):
        """Retrieves the site_id of the user associated with this interest."""
        return obj.username.site_id
    class Meta:
        model = Intressen
        # Specifies the fields to include in the serialized output.
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name')

class Kompetenser_intygSerializer(serializers.ModelSerializer):
    """
    Serializes Kompetenser_intyg (Skill/Certificate) model instances,
    including the user's site_id.
    """
    site_id = serializers.SerializerMethodField() # Custom field to include user's site_id.
    def get_site_id(self, obj):
        """Retrieves the site_id of the user associated with this skill/certificate."""
        return obj.username.site_id
    class Meta:
        model = Kompetenser_intyg
        # Specifies the fields to include in the serialized output.
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name')

class StudierSerializer(serializers.ModelSerializer):
    """
    Serializes Studier (Study) model instances, including the user's site_id.
    """
    site_id = serializers.SerializerMethodField() # Custom field to include user's site_id.
    def get_site_id(self, obj):
        """Retrieves the site_id of the user associated with this study entry."""
        return obj.username.site_id
    class Meta:
        model = Studier
        # Specifies the fields to include in the serialized output.
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name', 'plats', 'content', 'started_at', 'ended_at', 'degree')
        #read_only_fields = ('id',) # This line is commented out, review if read_only_fields are needed.


class ErfarenhetSerializer(serializers.ModelSerializer):
    """
    Serializes Erfarenhet (Experience) model instances, including the user's site_id.
    """
    site_id = serializers.SerializerMethodField() # Custom field to include user's site_id.
    def get_site_id(self, obj):
        """Retrieves the site_id of the user associated with this experience entry."""
        return obj.username.site_id
        
    class Meta:
        model = Erfarenhet
        # Specifies the fields to include in the serialized output.
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name', 'plats', 'content', 'started_at', 'ended_at','company')
    
class AllProfileInfoSerializer(serializers.ModelSerializer):
    """
    Provides a comprehensive serialization of a CustomUser's profile,
    embedding their interests, skills, studies, and experiences directly in the output.
    Also includes category update timestamps and email confirmation status.
    """
    Intressen = serializers.SerializerMethodField()
    Kompetenser_intyg = serializers.SerializerMethodField()
    Studier = serializers.SerializerMethodField()
    Erfarenhet = serializers.SerializerMethodField()
    member_since = serializers.DateTimeField(format='%Y-%m-%d')
    CategoryLastupdate = serializers.SerializerMethodField('get_CategorysLastupdate') # Name should ideally be get_category_last_update
    SubcategoryLastupdate = serializers.SerializerMethodField('get_SubCategorysLastupdate') # Name should ideally be get_subcategory_last_update
    emailConfirmed = serializers.SerializerMethodField('get_emailConfirmed')

    class Meta:
        model = CustomUser
        # Specifies all fields to be included for a comprehensive profile view.
        fields = ('id', 'stripeCustomerId', 'emailConfirmed', 'subscriptionType', 'Intressen', 'Kompetenser_intyg', 'Studier', 'Erfarenhet', 'CategoryLastupdate', 'SubcategoryLastupdate', 'email', 'name', 'first_name', 'phone', 'site_id', 'is_creator', 'bio', 'rating', 'members',
		          'followers', 'earning', 'profession', 'picture_medium', 'picture_small', 'picture_tag', 'location', 'address1', 'address2', 'zip_code', 'city', 'state', 'country', 'member_since', 'picture','Facebook_link','twitter','profile_completed','Linkdin_link','sms','othersSocialMedia','about')

    def get_Intressen(self, obj):
        """Retrieves and serializes the user's interests."""
        # .filter() returns a queryset, which doesn't raise DoesNotExist.
        # If no interests are found, an empty list will be serialized, which is the desired behavior.
        intressen = Intressen.objects.filter(username=obj.id)
        return IntressenSerializer(intressen, many=True).data

    def get_emailConfirmed(self, obj):
        """Checks if the user's email address is verified."""
        # NOTE: This method is duplicated from ProfileSerializer. Consider refactoring.
        try:
            email_confirmed = EmailAddress.objects.get(email=obj.email).verified
        except EmailAddress.DoesNotExist:
            email_confirmed = None
        return email_confirmed

    def get_Kompetenser_intyg(self, obj):
        """Retrieves and serializes the user's skills/certificates."""
        kompetenser_intyg = Kompetenser_intyg.objects.filter(username=obj.id)
        return Kompetenser_intygSerializer(kompetenser_intyg, many=True).data

    def get_Studier(self, obj):
        """Retrieves and serializes the user's studies."""
        studier = Studier.objects.filter(username=obj.id)
        return StudierSerializer(studier, many=True).data

    def get_Erfarenhet(self, obj):
        """Retrieves and serializes the user's work experiences."""
        erfarenheter = Erfarenhet.objects.filter(username=obj.id)
        return ErfarenhetSerializer(erfarenheter, many=True).data

    def get_CategorysLastupdate(self, obj): # Name should ideally be get_category_last_update
        """Retrieves the timestamp of the most recently updated ModelCategory."""
        # NOTE: This method is duplicated from ProfileSerializer. Consider refactoring.
        try:
            category_last_update = ModelCategory.objects.all().latest('updatedAt').updatedAt
        except ModelCategory.DoesNotExist:
            category_last_update = None
        return category_last_update
            
    def get_SubCategorysLastupdate(self, obj): # Name should ideally be get_subcategory_last_update
        """Retrieves the timestamp of the most recently updated ModelSubCategory."""
        # NOTE: This method is duplicated from ProfileSerializer. Consider refactoring.
        try:
            subcategory_last_update = ModelSubCategory.objects.all().latest('updatedAt').updatedAt
        except ModelSubCategory.DoesNotExist:
            subcategory_last_update = None
        return subcategory_last_update
