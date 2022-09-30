from django.db.models.signals import pre_save
import random
import string


from binascii import hexlify
import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.utils.translation import gettext_lazy  as _
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill#, ResizeToFill


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
        a_string = self.normalize_email(email)
        split_string = a_string.split("@", 1)

        site_id = split_string + ''.join(random.SystemRandom()
                            .choice(string.ascii_letters + string.digits) 
                            for _ in range(6))
        if_exist_already = CustomUser.objects.filter(site_id=site_id).count() > 0
        print(if_exist_already)
        while if_exist_already:
            print(if_exist_already)
            site_id = split_string + ''.join(random.SystemRandom()
                                .choice(string.ascii_letters + string.digits) 
                                for _ in range(6))
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

    def create_superuser(self, email, password, name, phone, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, name, phone,**extra_fields)

def upload_path(instance, filname):
    return '/'.join(['pictures/', str(instance.site_id)+'.'+filname.split('.')[-1]])



class CustomUser(AbstractUser):
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
    name = models.CharField(_('first_name'),max_length=50)
    first_name = models.CharField(_('first_name'),max_length=50)
    #name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    sms = models.CharField(max_length=15, blank=True, null=True)
    site_id = models.CharField(default=_createHash,max_length=50)
    is_admin = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    profile_completed = models.BooleanField(default=False)
    bio = models.CharField(max_length=500)
    rating = models.DecimalField(default=0, decimal_places=1, max_digits=2,
                                    validators=[MaxValueValidator(5),MinValueValidator(1)])
    members = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    earning = models.IntegerField(default=0)
    profession = models.CharField(max_length=100)
    location = models.CharField(max_length=50) #Name of city, change it to location maybe?
    member_since = models.DateTimeField(default=timezone.now, null=True) #Do something about it
    picture = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70},upload_to=upload_path, null=False, blank=False, default='ProfileDefaultImage.jpg')
  #  picture_medium = models.ImageField(upload_to=upload_path, null=False, blank=False, default='ProfileDefaultImage.jpg')
   # picture_small = models.ImageField(upload_to=upload_path, null=False, blank=False, default='ProfileDefaultImage.jpg')
    #picture_tag = models.ImageField(upload_to=upload_path, null=False, blank=False, default='ProfileDefaultImage.jpg')
    #picture_large = ProcessedImageField(format='PNG',source='picture', processors=[ResizeToFill(512, 512)], options={'quality': 70},upload_to=upload_path, null=False, blank=False, default='ProfileDefaultImage.jpg')
    picture_medium = ProcessedImageField(format='PNG', processors=[ResizeToFill(256, 256)], options={'quality': 70},upload_to=upload_path, blank=False, default='ProfileDefaultImage.jpg')
    picture_small = ProcessedImageField(format='PNG', processors=[ResizeToFill(128, 128)], options={'quality': 70},upload_to=upload_path, blank=False, default='ProfileDefaultImage.jpg')
    picture_tag = ProcessedImageField(format='PNG', processors=[ResizeToFill(28, 28)], options={'quality': 70},upload_to=upload_path, blank=False, default='ProfileDefaultImage.jpg')
 
    address1 = models.CharField(verbose_name="Address line 1", max_length=1024, blank=True, null=True)
    address2 = models.CharField(verbose_name="Address line 2", max_length=1024, blank=True, null=True)
    zip_code = models.CharField(verbose_name="Postal Code", max_length=12, blank=True, null=True)
    city = models.CharField(verbose_name="Kommun", max_length=1024, blank=True, null=True)
    state = models.CharField(verbose_name="Lansting", max_length=1024, blank=True, null=True)
    country = models.CharField(verbose_name="contry", max_length=1024, blank=True, null=True)
    Facebook_link = models.CharField(blank=True, null=True,help_text='Facebook_link',max_length=120)
    twitter = models.CharField(blank=True, null=True,help_text='twitter',max_length=120)
    Linkdin_link = models.CharField(blank=True, null=True,help_text='Linkdin_link',max_length=120)
    othersSocialMedia = models.CharField(blank=True, null=True,help_text='Linkdin_link',max_length=120)
    stripeCustomerId = models.CharField(blank=True, null=True,help_text='Linkdin_link',max_length=120)
    subscriptionType = models.CharField(max_length=10,
        default="groundplan", verbose_name="subscriptionType of the user:")


    date_of_birth = models.DateField(verbose_name="Date of birth", blank=True, null=True)
    about = models.TextField(verbose_name='Om mig', max_length=120, default='The user did not put any thing yet')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    def __str__(self):
        return f"email={self.email} site_id={self.site_id}"
    

    objects = UserManager()





def pre_save_service_post_receiever(sender, instance, *args, **kwargs):
    if not instance.name:
        instance.name = instance.first_name
pre_save.connect(pre_save_service_post_receiever, sender=CustomUser)
