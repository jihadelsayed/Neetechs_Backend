from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser as User



@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('site_id','name', 'phone', 'is_admin', 'profession', 'profile_completed', 'picture', 'picture_medium', 'picture_small', 'picture_tag','sms','Facebook_link','Linkdin_link','othersSocialMedia')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name' , 'phone'),
        }),
    )
    list_display = ('email', 'name', 'is_staff')
    search_fields = ('email', 'name',)
    ordering = ('email',)
from django.apps import AppConfig


class KnoxAllauthConfig(AppConfig):
    name = 'knox_allauth'
    def ready(self):
    	import knox_allauth.signals
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            if username.isdigit():  # assume it's a phone number
                user = UserModel.objects.get(phone=username)
            else:
                user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'phone')

class UserLoginForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
import os
import random
import string
from binascii import hexlify

from django.contrib.auth.models import (  # # A new class is imported. ##
    AbstractUser, BaseUserManager)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from imagekit.models.fields import ProcessedImageField
from datetime import date # Added for age calculation
from imagekit.processors import ResizeToFill  # , ResizeToFill


def _createHash():
    """This function generate 10 character long hash"""
    return hexlify(os.urandom(5)).decode()


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, name=None, phone=None,**extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        #a_string = self.normalize_email(email)
        #split_string = a_string.split("@", 1)

        site_id = ''.join(random.SystemRandom()
                            .choice(string.ascii_letters + string.digits) 
                            for _ in range(10))
        if_exist_already = CustomUser.objects.filter(site_id=site_id).count() > 0
        # Loop to ensure site_id is unique. Regenerates a 10-character site_id if a collision occurs.
        while if_exist_already:
            site_id = ''.join(random.SystemRandom()
                                .choice(string.ascii_letters + string.digits) 
                                for _ in range(10)) # Ensure site_id is 10 characters
            if_exist_already = CustomUser.objects.filter(site_id=site_id).count() > 0
        user = self.model(email=email, name=name, phone=phone, site_id=site_id,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, name, phone, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, name, phone, **extra_fields)

    def create_superuser(self, email, password, phone, name=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, phone, name, **extra_fields)

def upload_path(instance, filname):
    """
    Generates the upload path for user profile pictures.

    Args:
        instance: The CustomUser instance.
        filname: The original filename of the uploaded picture.

    Returns:
        A string representing the upload path.
    """
    return '/'.join(['pictures/', str(instance.site_id)+'.'+filname.split('.')[-1]])



class CustomUser(AbstractUser):
    # Defines the available subscription options for users.
    # 'groundplan': Basic, free plan.
    # 'premiumplanmonthly': Premium plan with monthly billing.
    # 'premiumplanyearly': Premium plan with yearly billing.
    SubscriptionOptions= (
        ('groundplan','GroundPlan'),
        ('premiumplanmonthly','premiumplanMonthly'),
        ('premiumplanyearly','PremiumPlanYearly'),
    )
    username = models.CharField(
            _('username'),
            default=_createHash,
            max_length=150,
            unique=True,
            help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
            error_messages={
                'unique': _("A user with that username already exists."),
            },
        )
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'),max_length=50)
    first_name = models.CharField(_('name'),max_length=50)
    #name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    sms = models.CharField(max_length=15, blank=True, null=True)
    site_id = models.CharField(default=_createHash,max_length=50)  # Unique identifier for the user's site or profile.
    is_admin = models.BooleanField(default=False)  # Designates whether the user has admin privileges.
    is_creator = models.BooleanField(default=False)  # Designates whether the user is a content creator.
    profile_completed = models.BooleanField(default=False)  # Indicates if the user has completed their profile.
    bio = models.CharField(max_length=500)  # A short biography of the user.
    rating = models.DecimalField(default=0, decimal_places=1, max_digits=2,  # User's rating, typically on a scale of 1-5.
                                    validators=[MaxValueValidator(5),MinValueValidator(1)])
    members = models.IntegerField(default=0)  # Number of members associated with the user (e.g., in a group or community).
    followers = models.IntegerField(default=0)  # Number of followers the user has.
    earning = models.IntegerField(default=0)  # User's earnings, if applicable.
    profession = models.CharField(max_length=100)  # User's profession.
    location = models.CharField(max_length=50) #Name of city, change it to location maybe? # User's location (e.g., city).
    member_since = models.DateTimeField(default=timezone.now, null=True) #Do something about it # Date when the user registered.
    picture = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70},upload_to=upload_path, null=False, blank=False, default='ProfileDefaultImage.png')
  #  picture_medium = models.ImageField(upload_to=upload_path, null=False, blank=False, default='ProfileDefaultImage.png')
   # picture_small = models.ImageField(upload_to=upload_path, null=False, blank=False, default='ProfileDefaultImage.png')
    #picture_tag = models.ImageField(upload_to=upload_path, null=False, blank=False, default='ProfileDefaultImage.png')
    #picture_large = ProcessedImageField(format='PNG',source='picture', processors=[ResizeToFill(512, 512)], options={'quality': 70},upload_to=upload_path, null=False, blank=False, default='ProfileDefaultImage.png')
    picture_medium = ProcessedImageField(format='PNG', processors=[ResizeToFill(256, 256)], options={'quality': 70},upload_to=upload_path, blank=False, default='ProfileDefaultImage.png')
    picture_small = ProcessedImageField(format='PNG', processors=[ResizeToFill(128, 128)], options={'quality': 70},upload_to=upload_path, blank=False, default='ProfileDefaultImage.png')
    picture_tag = ProcessedImageField(format='PNG', processors=[ResizeToFill(28, 28)], options={'quality': 70},upload_to=upload_path, blank=False, default='ProfileDefaultImage.png')
 
    address1 = models.CharField(verbose_name="Address line 1", max_length=1024, blank=True, null=True)
    address2 = models.CharField(verbose_name="Address line 2", max_length=1024, blank=True, null=True)
    zip_code = models.CharField(verbose_name="Postal Code", max_length=12, blank=True, null=True)
    city = models.CharField(verbose_name="Municipality", max_length=1024, blank=True, null=True)
    state = models.CharField(verbose_name="County", max_length=1024, blank=True, null=True)
    country = models.CharField(verbose_name="Country", max_length=1024, blank=True, null=True) # Corrected typo "contry" to "Country"
    facebook_link = models.CharField(blank=True, null=True,help_text="User's Facebook profile link",max_length=120)
    twitter = models.CharField(blank=True, null=True,help_text="User's Twitter profile link",max_length=120)
    linkedin_link = models.CharField(blank=True, null=True,help_text="User's LinkedIn profile link",max_length=120)
    other_social_media = models.CharField(blank=True, null=True,help_text="User's other social media link",max_length=120)
    stripe_customer_id = models.CharField(blank=True, null=True,help_text="Stripe Customer ID for billing",max_length=120)
    subscription_type = models.CharField(max_length=20, # Increased max_length to accommodate longer values like 'premiumplanmonthly'
        default="groundplan", verbose_name="Subscription type")


    date_of_birth = models.DateField(verbose_name="Date of birth", blank=True, null=True)
    about = models.TextField(verbose_name='About me', max_length=120, default='The user did not put any thing yet')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    def __str__(self):
        return f"email={self.email} site_id={self.site_id}"
    phone_otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    @property
    def age(self):
        """
        Calculates the user's current age based on their date_of_birth.
        Returns None if date_of_birth is not set.
        """
        if not self.date_of_birth:
            return None
        today = date.today()
        born = self.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    objects = UserManager()





def pre_save_service_post_receiever(sender, instance, *args, **kwargs):
    """
    Ensures that the 'name' field is populated before saving a CustomUser instance.

    If the 'name' field is empty, it defaults to the value of the 'first_name' field.
    This function is connected to the pre_save signal of the CustomUser model
    to automatically populate the 'name' field if it's not provided.
    """
    if not instance.name:
        instance.name = instance.first_name
pre_save.connect(pre_save_service_post_receiever, sender=CustomUser)
# knox_allauth/serializer_register.py

from rest_framework import serializers
from knox_allauth.models import CustomUser
from django.contrib.auth.password_validation import validate_password

class PhoneOrEmailRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'password', 'name']
        extra_kwargs = {
            'email': {'required': False},
            'phone': {'required': False},
        }

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('phone'):
            raise serializers.ValidationError("You must provide either email or phone.")

        if attrs.get('email') and CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already in use.")
        if attrs.get('phone') and CustomUser.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError("Phone number already in use.")

        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

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
			raise serializers.ValidationError({"detail": "Both fields are required."})

		user = authenticate(request=self.context.get("request"), username=identifier, password=password)

		if not user:
			# Check if user exists but has no password set
			from knox_allauth.models import CustomUser
			try:
				user_obj = CustomUser.objects.get(email=identifier) if "@" in identifier else CustomUser.objects.get(phone=identifier)
				if not user_obj.has_usable_password():
					raise serializers.ValidationError({"detail": "This user has no password. Please login via phone and set a password."})
			except CustomUser.DoesNotExist:
				pass  # continue to default error

			raise serializers.ValidationError({"detail": "Invalid phone/email or password."})

		if not user.is_active:
			raise serializers.ValidationError({"detail": "This account is inactive."})

		# Optional: if email needs to be verified before login
		if user.email and not EmailAddress.objects.filter(email=user.email, verified=True).exists():
			raise serializers.ValidationError({"detail": "Email is not verified."})

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

from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_signed_up
from .models import CustomUser as User

# @receiver(post_save, sender=SocialAccount)
# def create_class(sender, instance, created, **kwargs):
# 	if created:
# 		user = User.objects.filter(email=instance.extra_data['email']).first()
# 		user.name = instance.extra_data['name']
# 		user.save()

@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):
    if sociallogin is not None:
	    if sociallogin.account.provider == 'facebook':
	        user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
	        #picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"            
	        #email = user_data['email']
	        name = user_data['name']
	    user.name = name
	    user.save()
from twilio.rest import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_sms_otp(to_phone: str, otp_code: str) -> str:
    """
    Sends a verification code via SMS using Twilio.
    Returns the message SID if sent successfully.
    """
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"🔐 Your Neetechs verification code is: {otp_code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        logger.info(f"Twilio SMS sent to {to_phone}: SID {message.sid}")
        return message.sid
    except Exception as e:
        logger.error(f"Failed to send OTP to {to_phone}: {e}")
        return ""
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from knox_allauth.views_otp import SendPhoneOTP, VerifyPhoneOTP
from knox_allauth.views_set_password import SetPasswordView

from .views import EmailConfirmation, KnoxLoginView, KnoxRegisterView, FacebookLogin, GoogleLogin
from .webauthn_view import (
    begin_registration,
    complete_registration,
    begin_authentication,
    complete_authentication,
)


urlpatterns = [ 
	path('auth/login/', KnoxLoginView.as_view()),
	path('auth/register/', KnoxRegisterView.as_view()),
	path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
	path('auth/google/', GoogleLogin.as_view(), name='google_login'),
	path('auth/', include('dj_rest_auth.urls')),
	path('accounts/', include('allauth.urls')),
	path('verify-email/again/', EmailConfirmation.as_view(), name='resend-email-confirmation'),
    
	
    path('auth/otp/send/', SendPhoneOTP.as_view()),
        path("auth/otp/verify/", VerifyPhoneOTP.as_view(), name="verify-phone-otp"),
        
    path("auth/webauthn/begin-registration/", begin_registration),
    path("auth/webauthn/finish-registration/", complete_registration),
    path("auth/webauthn/begin-login/", begin_authentication),
    path("auth/webauthn/finish-login/", complete_authentication),
    
    path('set-password/', SetPasswordView.as_view(), name='set-password'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from knox.models import AuthToken


def create_knox_token(token_model, user, serializer):
    token = AuthToken.objects.create(user=user)
    return token

# knox_allauth/views_otp.py

import random
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Neetechs import settings
from knox_allauth.models import CustomUser

from datetime import timedelta
from knox_allauth.twilio_utils import send_sms_otp
from knox.models import AuthToken
from datetime import timedelta
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from hashlib import sha256

import logging


class SendPhoneOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({"detail": "Phone number is required."}, status=400)

        hashed_email = sha256(phone.encode()).hexdigest()[:10]
        placeholder_email = f"{hashed_email}@neetechs.sms"

        user, created = CustomUser.objects.get_or_create(
            phone=phone,
            defaults={"email": placeholder_email, "name": "PhoneUser"}
        )


        otp = str(random.randint(100000, 999999))
        user.phone_otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        # 🔥 Replace this with real SMS send
        if settings.DEBUG:
            print(f"[MOCK OTP] to {phone}: {otp}")
            logger = logging.getLogger(__name__)
            logger.warning(f"[MOCK OTP] to {phone}: {otp}")
        else:
            try:
                send_sms_otp(phone, otp)
            except Exception as e:
                logger.error(f"Failed to send OTP to {phone}: {e}")


        return Response({"detail": "OTP sent successfully."}, status=200)


class VerifyPhoneOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        otp = request.data.get("otp")

        ip = request.META.get("REMOTE_ADDR")
        device_id = request.headers.get("X-Device-ID", "")
        attempt_key = f"otp_attempts_{ip}_{device_id}"
        attempts = cache.get(attempt_key, 0)

        if attempts >= 5:
            return Response({"detail": "Too many failed attempts. Try again in 1 hour."}, status=429)

        try:
            user = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        if not user.phone_otp or user.phone_otp != otp:
            cache.set(attempt_key, attempts + 1, timeout=3600)
            return Response({"detail": "Invalid OTP."}, status=400)

        if timezone.now() - user.otp_created_at > timedelta(minutes=5):
            return Response({"detail": "OTP expired."}, status=400)

        cache.delete(attempt_key)

        user.phone_otp = None
        user.otp_created_at = None
        user.save()

        token = AuthToken.objects.create(user)[1]

        return Response({
            "token": token,
            "user": {
                "id": user.id,
                "phone": user.phone,
                "email": user.email,
                "name": user.name,
            },
            "has_password": user.has_usable_password()
        }, status=200)


# knox_allauth/views_set_password.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class SetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data.get("password")
        if not password or len(password) < 6:
            return Response({"detail": "Password too short."}, status=400)

        user = request.user
        user.set_password(password)
        user.save()

        return Response({"detail": "Password set successfully."}, status=200)
import stripe
from allauth.account.models import EmailAddress
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from knox_allauth.models import CustomUser
from Neetechs import settings
from Profile.serializer import ProfileSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup, send_email_confirmation
from allauth.socialaccount.providers.facebook.views import \
    FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from dj_rest_auth.views import LoginView
from django.conf import settings

from .serializer import KnoxSerializer, UserSerializer
from .utils import create_knox_token

from .serializer_register import PhoneOrEmailRegisterSerializer

class KnoxLoginView(LoginView):
    permission_classes = [AllowAny]
    def get_response(self):
        serializer_class = self.get_response_serializer()

        data = {
            'user': self.user,
            'token': self.token[1]
        }
        serializer = serializer_class(instance=data, context={'request': self.request})

        return Response(serializer.data, status=200)


class KnoxRegisterView(RegisterView):
    permission_classes = [AllowAny]
    serializer_class = PhoneOrEmailRegisterSerializer


    def perform_create(self, serializer):
        # Create a Stripe customer for the new user.
        # Uses the provided email, or a placeholder if email is not available (e.g., phone registration).
        phone_number = self.request.data.get('phone')
        customer_email = self.request.data.get('email')
        if not customer_email:
            if phone_number:
                customer_email = f"no-email-{phone_number}@neetechs.com"
            else:
                # Fallback if neither email nor phone is provided, though this case might be handled by serializer validation.
                customer_email = f"no-email-anonymous@{settings.DEFAULT_DOMAIN or 'neetechs.com'}"


        customer = stripe.Customer.create(
            email=customer_email,
            payment_method='pm_card_visa',  # Sets 'pm_card_visa' as a default payment method.
            invoice_settings={
                'default_payment_method': 'pm_card_visa', # Ensures future invoices use this payment method.
            },
        )

        user = serializer.save(self.request)
        self.token = create_knox_token(None, user, None)
        identifier = self.request.data.get('email') or self.request.data.get('phone')
        instance = CustomUser.objects.filter(email=identifier).first() or CustomUser.objects.filter(phone=identifier).first()

        # Create a mutable copy of request.data to add stripeCustomerId
        profile_data = self.request.data.copy()
        profile_data['stripeCustomerId'] = customer.id
        # If 'name' is not provided, it can be defaulted from 'first_name' here or handled by model's pre_save.
        # profile_data['name'] = profile_data.get('first_name')

        # Update the user's profile with the stripeCustomerId and other potential data.
        serializer1 = ProfileSerializer(instance,data=profile_data, partial=True)
        if serializer1.is_valid():
            serializer1.save()
        complete_signup(self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None, signal_kwargs={'sociallogin': None})
        return user

    
class SocialLoginView_(SocialLoginView):
    """
    Customized SocialLoginView to include the Knox token directly in the login response.
    This is useful for client-side applications that need both user details and the
    authentication token immediately after a successful social login.
    It extends the standard SocialLoginView from dj_rest_auth.
    """
    permission_classes = [AllowAny]
    def get_response(self):
        serializer_class = self.get_response_serializer()
        
        data = {
            'user': self.user,
            'token': self.token[1]
        }
        serializer = serializer_class(instance=data, context={'request': self.request})

        return Response(serializer.data, status=200)

class FacebookLogin(SocialLoginView_):
    adapter_class = FacebookOAuth2Adapter

class GoogleLogin(SocialLoginView_):
    permission_classes = [AllowAny]
    adapter_class = GoogleOAuth2Adapter
    #callback_url = settings.GOOGLE_AUTH_CALLBACK_URL
    #client_class = OAuth2Client
    # The following commented-out 'login' method provides an example of how one might
    # override the default social login behavior. This could be used to explicitly
    # enable session-based authentication alongside token authentication,
    # especially if `REST_SESSION_LOGIN` is set to True in Django settings.
    # It's kept here for future reference or potential customization needs.
    # def login(self):
    #     self.user = self.serializer.validated_data['user']
    #     self.token, created = self.token_model.objects.get_or_create(
    #             user = self.user)
    #     if getattr(settings, 'REST_SESSION_LOGIN', True): # Check if session login is enabled
    #         if not hasattr(self.user, 'backend'): # Ensure user has a backend attribute
    #             self.user.backend = 'django.contrib.auth.backends.ModelBackend'
    #         login(self.request, self.user) # Perform session login

class EmailConfirmation(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        # Attempt to retrieve the user by the provided email.
        user = get_object_or_404(CustomUser, email=request.data['email'])
        # Check if the user's email address is already verified.
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            # If email is already verified, inform the user.
            return Response({'message': 'This email is already verified. Try to login and logout again to refresh the app.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If not verified, attempt to send a confirmation email.
            try:
                send_email_confirmation(request, user=user)
                return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)
            except APIException:
                # Handle cases where email sending might fail or user does not exist (though get_object_or_404 should catch this).
                return Response({'message': 'This email does not exist, please create a new account'}, status=status.HTTP_403_FORBIDDEN)
            
import json
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

from webauthn import (
    generate_registration_options,
    generate_authentication_options,
    verify_registration_response,
    verify_authentication_response,
)
from webauthn.helpers.structs import UserVerificationRequirement

RP_ID = "neetechs.com"
RP_NAME = "Neetechs"

@csrf_exempt
def begin_registration(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])
    username = data["username"]

    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=user_id.encode(),
        user_name=username,
        user_display_name=username,
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    cache.set(f"register_challenge:{user_id}", options.challenge, timeout=300)
    return JsonResponse(options.model_dump())


@csrf_exempt
def complete_registration(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])
    challenge_b64 = cache.get(f"register_challenge:{user_id}")

    result = verify_registration_response(
        expected_rp_id=RP_ID,
        expected_origin=f"https://{RP_ID}",
        credential=data,
        expected_challenge=challenge_b64,
        user_verification_required=True,
    )

    # Save result.credential_id, result.public_key, result.sign_count, etc. to DB here
    return JsonResponse({"status": "ok"})


@csrf_exempt
def begin_authentication(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])

    # TODO: Replace with real credential IDs from DB
    stored_credential_ids = [
        base64.b64decode("...")  # Replace with actual Base64URL-encoded credential ID bytes
    ]

    options = generate_authentication_options(
        rp_id=RP_ID,
        allow_credentials=stored_credential_ids,
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    cache.set(f"auth_challenge:{user_id}", options.challenge, timeout=300)
    return JsonResponse(options.model_dump())


@csrf_exempt
def complete_authentication(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])
    challenge = cache.get(f"auth_challenge:{user_id}")

    result = verify_authentication_response(
        expected_rp_id=RP_ID,
        expected_origin=f"https://{RP_ID}",
        credential=data,
        expected_challenge=challenge,
        credential_public_key=None,  # Replace with public key object from DB
        sign_count=0,                # Replace with stored sign count
        user_verification_required=True,
    )

    # Update stored sign_count with result.new_sign_count
    return JsonResponse({"status": "ok", "sign_count": result.new_sign_count})
