
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from allauth.account.models import EmailAddress

class PhoneOrEmailLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        identifier = attrs.get("identifier")
        password = attrs.get("password")

        if not identifier or not password:
            raise serializers.ValidationError({"detail": _("Both fields are required.")})

        user = authenticate(request=self.context.get("request"), username=identifier, password=password)

        if not user:
            raise serializers.ValidationError({"detail": _("Invalid phone/email or password.")})

        if not user.is_active:
            raise serializers.ValidationError({"detail": _("This account is inactive.")})

        if user.email and not EmailAddress.objects.filter(email=user.email, verified=True).exists():
            raise serializers.ValidationError({"detail": _("Email is not verified.")})

        attrs["user"] = user
        return attrs

from allauth.account.models import EmailAddress
from Profile.models import Erfarenhet, Intressen, Kompetenser_intyg, Studier
from Profile.serializer import ErfarenhetSerializer, IntressenSerializer, Kompetenser_intygSerializer, StudierSerializer
from Service.api.serializers import CategorySerializer, SubCategorySerializer
from rest_framework import serializers

from dj_rest_auth.serializers import UserDetailsSerializer

from .models import CustomUser as User
from Service.models import ModelCategory,ModelSubCategory


class UserSerializer(serializers.ModelSerializer):
	Intressen = serializers.SerializerMethodField()
	Kompetenser_intyg = serializers.SerializerMethodField()
	Studier = serializers.SerializerMethodField()
	Erfarenhet = serializers.SerializerMethodField()
	Categories = serializers.SerializerMethodField()
	subCategories = serializers.SerializerMethodField()
	CategoryLastupdate = serializers.SerializerMethodField('get_CategorysLastupdate')
	SubcategoryLastupdate = serializers.SerializerMethodField('get_SubCategorysLastupdate')
	emailConfirmed = serializers.SerializerMethodField('get_emailConfirmed')

	class Meta:
		depth = 1
		model = User
		depth = 1
		 #Add the other columns from the model when required
		fields = ('id', 'email', 'emailConfirmed', 'Intressen', 'Categories', 'subCategories', 'Kompetenser_intyg', 'Studier', 'Erfarenhet', 'stripeCustomerId', 'subscriptionType', 'name', 'first_name', 'CategoryLastupdate', 'SubcategoryLastupdate', 'phone', 'site_id', 'is_creator', 'bio', 'rating', 'members',
		          'followers', 'picture_medium', 'picture_small', 'picture_tag', 'earning', 'profession', 'location', 'address1', 'address2', 'zip_code', 'city', 'state', 'country', 'member_since', 'picture','Facebook_link','profile_completed','Linkdin_link','sms','othersSocialMedia','about')
		read_only_fields = ['email', 'rating', 'members', 'followers', 'earning', 'member_since',]
		
	def get_CategorysLastupdate(self, obj):
		CategoryLastupdate = ModelCategory.objects.all().latest('updatedAt').updatedAt #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		print(CategoryLastupdate)
		return CategoryLastupdate
	def get_emailConfirmed(self, obj):
		emailConfirmed = EmailAddress.objects.get(email=obj.email).verified #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		print(emailConfirmed)
		return emailConfirmed

	def get_SubCategorysLastupdate(self, obj):
		SubcategoryLastupdate = ModelSubCategory.objects.all().latest('updatedAt').updatedAt #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		#print(SubcategoryLastupdate)
		return SubcategoryLastupdate

	def get_Intressen(self, obj):
		Intresse = Intressen.objects.filter(username=obj.id) #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		#print(Intresse)
		return IntressenSerializer(Intresse, many=True).data

	def get_Categories(self, obj):
		Category = ModelCategory.objects.all() #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		#print(Intresse)
		return CategorySerializer(Category, many=True).data
	def get_subCategories(self, obj):
		SubCategory = ModelSubCategory.objects.all() #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		#print(Intresse)
		return SubCategorySerializer(SubCategory, many=True).data

	def get_Kompetenser_intyg(self, obj):
		Kompetenser_inty = Kompetenser_intyg.objects.filter(username=obj.id) #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		#print(SubCategorys)
		return Kompetenser_intygSerializer(Kompetenser_inty, many=True).data
	def get_Studier(self, obj):
		Studie = Studier.objects.filter(username=obj.id) #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		#print(SubCategorys)
		return StudierSerializer(Studie, many=True).data
	def get_Erfarenhet(self, obj):
		Erfarenhe = Erfarenhet.objects.filter(username=obj.id) #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		#print(SubCategorys)
		return ErfarenhetSerializer(Erfarenhe, many=True).data

class KnoxSerializer(serializers.Serializer):
    """
    Serializer for Knox authentication.
    """
    token = serializers.CharField()
    user = UserSerializer()

# class	 UserSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = User

#We need UserDetailsSerializer class