from allauth.account.models import EmailAddress
from rest_framework import serializers

from knox_allauth.models import CustomUser
from Service.models import ModelCategory, ModelSubCategory

from .models import Erfarenhet, Intressen, Kompetenser_intyg, Studier


class ProfileSerializer(serializers.ModelSerializer):
    member_since = serializers.DateTimeField(format='%Y-%m-%d')
    CategoryLastupdate = serializers.SerializerMethodField('get_CategorysLastupdate')
    SubcategoryLastupdate = serializers.SerializerMethodField('get_SubCategorysLastupdate')
    emailConfirmed = serializers.SerializerMethodField('get_emailConfirmed')

    class Meta:
        model = CustomUser
       # fields = ('id', 'email', 'name', 'phone', 'site_id', 'is_creator', 'bio', 'rating', 'members',
		#          'followers', 'earning', 'profession', 'location', 'member_since', 'picture','Facebook_link','Linkdin_link')
        fields = ('id', 'stripeCustomerId', 'emailConfirmed', 'subscriptionType', 'name','CategoryLastupdate', 'SubcategoryLastupdate', 'email', 'first_name', 'phone', 'site_id', 'is_creator', 'bio', 'rating', 'members',
		          'followers', 'earning', 'profession', 'picture_medium', 'picture_small', 'picture_tag', 'location', 'address1', 'address2', 'zip_code', 'city', 'state', 'country', 'member_since', 'picture','Facebook_link','twitter','profile_completed','Linkdin_link','sms','othersSocialMedia','about')
	
    def get_CategorysLastupdate(self, obj):
        try:
            CategoryLastupdate = ModelCategory.objects.all().latest('updatedAt').updatedAt #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
        except CategoryLastupdate.DoesNotExist:
            CategoryLastupdate = None
        return CategoryLastupdate
    def get_emailConfirmed(self, obj):
        try:
            emailConfirmed = EmailAddress.objects.get(email=obj.email).verified #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
        except emailConfirmed.DoesNotExist:
            emailConfirmed = None
        return emailConfirmed
                
    def get_SubCategorysLastupdate(self, obj):
        try:
            SubcategoryLastupdate = ModelSubCategory.objects.all().latest('updatedAt').updatedAt #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
        except SubcategoryLastupdate.DoesNotExist:
            SubcategoryLastupdate = None
        return SubcategoryLastupdate

class IntressenSerializer(serializers.ModelSerializer):
    site_id = serializers.SerializerMethodField(source="site_id.site_id")
    def get_site_id(self, obj):
        return obj.username.site_id
    class Meta:
        model = Intressen
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name')

class Kompetenser_intygSerializer(serializers.ModelSerializer):
    site_id = serializers.SerializerMethodField(source="site_id.site_id")
    def get_site_id(self, obj):
        return obj.username.site_id
    class Meta:
        model = Kompetenser_intyg
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name')

class StudierSerializer(serializers.ModelSerializer):
    site_id = serializers.SerializerMethodField(source="site_id.site_id")
    def get_site_id(self, obj):
        return obj.username.site_id
    class Meta:
        model = Studier
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name', 'plats', 'content', 'started_at', 'ended_at', 'degree')
        #read_only_fields = ('id',)


class ErfarenhetSerializer(serializers.ModelSerializer):
    site_id = serializers.SerializerMethodField(source="site_id.site_id")
    def get_site_id(self, obj):
        return obj.username.site_id
        
    class Meta:
        model = Erfarenhet
        fields = ('id','site_id','username', 'Added_at', 'updated_at', 'name', 'plats', 'content', 'started_at', 'ended_at','company')
    
class AllProfileInfoSerializer(serializers.ModelSerializer):
    Intressen = serializers.SerializerMethodField()
    Kompetenser_intyg = serializers.SerializerMethodField()
    Studier = serializers.SerializerMethodField()
    Erfarenhet = serializers.SerializerMethodField()
    member_since = serializers.DateTimeField(format='%Y-%m-%d')
    CategoryLastupdate = serializers.SerializerMethodField('get_CategorysLastupdate')
    SubcategoryLastupdate = serializers.SerializerMethodField('get_SubCategorysLastupdate')
    emailConfirmed = serializers.SerializerMethodField('get_emailConfirmed')

    class Meta:
        model = CustomUser
        fields = ('id', 'stripeCustomerId', 'emailConfirmed', 'subscriptionType', 'Intressen', 'Kompetenser_intyg', 'Studier', 'Erfarenhet', 'CategoryLastupdate', 'SubcategoryLastupdate', 'email', 'name', 'first_name', 'phone', 'site_id', 'is_creator', 'bio', 'rating', 'members',
		          'followers', 'earning', 'profession', 'picture_medium', 'picture_small', 'picture_tag', 'location', 'address1', 'address2', 'zip_code', 'city', 'state', 'country', 'member_since', 'picture','Facebook_link','twitter','profile_completed','Linkdin_link','sms','othersSocialMedia','about')
    def get_Intressen(self, obj):
        try:
            Intresse = Intressen.objects.filter(username=obj.id) #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
        except Intresse.DoesNotExist:
            Intresse = None
        return IntressenSerializer(Intresse, many=True).data
    def get_emailConfirmed(self, obj):
        try:
            emailConfirmed = EmailAddress.objects.get(email=obj.email).verified #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
        except emailConfirmed.DoesNotExist:
            emailConfirmed = None
        return emailConfirmed
    def get_Kompetenser_intyg(self, obj):
        try:
            Kompetenser_inty = Kompetenser_intyg.objects.filter(username=obj.id) #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
        except Kompetenser_inty.DoesNotExist:
            Kompetenser_inty = None
        return Kompetenser_intygSerializer(Kompetenser_inty, many=True).data

    def get_Studier(self, obj):
        try:
            Studie = Studier.objects.filter(username=obj.id) #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
        except Studie.DoesNotExist:
            Studie = None
        return StudierSerializer(Studie, many=True).data

    def get_Erfarenhet(self, obj):
        try:
            Erfarenhe = Erfarenhet.objects.filter(username=obj.id) #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
        except Erfarenhe.DoesNotExist:
            Erfarenhe = None
        return ErfarenhetSerializer(Erfarenhe, many=True).data
    def get_CategorysLastupdate(self, obj):
        try:
            CategoryLastupdate = ModelCategory.objects.all().latest('updatedAt').updatedAt #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
        except CategoryLastupdate.DoesNotExist:
            CategoryLastupdate = None
        return CategoryLastupdate
            
    def get_SubCategorysLastupdate(self, obj):
        try:
            SubcategoryLastupdate = ModelSubCategory.objects.all().latest('updatedAt').updatedAt #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
        except SubcategoryLastupdate.DoesNotExist:
            SubcategoryLastupdate = None
        return SubcategoryLastupdate
