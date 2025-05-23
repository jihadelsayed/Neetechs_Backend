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
