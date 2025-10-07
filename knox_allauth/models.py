
import os
import random
import string
from binascii import hexlify
from datetime import date

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill


def _create_hash() -> str:
    return hexlify(os.urandom(5)).decode()


def upload_path(instance, filename: str) -> str:
    return "/".join(["pictures", f"{instance.site_id}.{filename.split('.')[-1]}"])


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, name=None, phone=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        # unique 10-char site_id
        while True:
            site_id = "".join(
                random.SystemRandom().choice(string.ascii_letters + string.digits)
                for _ in range(10)
            )
            if not CustomUser.objects.filter(site_id=site_id).exists():
                break

        user = self.model(email=email, name=name, phone=phone, site_id=site_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, name=None, phone=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, name, phone, **extra_fields)

    def create_superuser(self, email, password=None, phone=None, name=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, name, phone, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(
        _("username"),
        default=_create_hash,
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages={"unique": _("A user with that username already exists.")},
    )
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("name"), max_length=50, blank=True, null=True)
    first_name = models.CharField(_("first name"), max_length=50, blank=True, null=True)

    phone = models.CharField(max_length=15, blank=True, null=True)
    sms = models.CharField(max_length=15, blank=True, null=True)
    site_id = models.CharField(default=_create_hash, max_length=50, db_index=True)

    is_admin = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    profile_completed = models.BooleanField(default=False)

    bio = models.CharField(max_length=500, blank=True, null=True)
    rating = models.DecimalField(
        default=0, decimal_places=1, max_digits=2, validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    members = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    earning = models.IntegerField(default=0)
    profession = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)

    member_since = models.DateTimeField(default=timezone.now, null=True, blank=True)

    picture = ProcessedImageField(
        format="PNG",
        processors=[ResizeToFill(512, 512)],
        options={"quality": 70},
        upload_to=upload_path,
        blank=True,
        null=True,
        default="ProfileDefaultImage.png",
    )
    picture_medium = ProcessedImageField(
        format="PNG",
        processors=[ResizeToFill(256, 256)],
        options={"quality": 70},
        upload_to=upload_path,
        blank=True,
        null=True,
        default="ProfileDefaultImage.png",
    )
    picture_small = ProcessedImageField(
        format="PNG",
        processors=[ResizeToFill(128, 128)],
        options={"quality": 70},
        upload_to=upload_path,
        blank=True,
        null=True,
        default="ProfileDefaultImage.png",
    )
    picture_tag = ProcessedImageField(
        format="PNG",
        processors=[ResizeToFill(28, 28)],
        options={"quality": 70},
        upload_to=upload_path,
        blank=True,
        null=True,
        default="ProfileDefaultImage.png",
    )

    address1 = models.CharField("Address line 1", max_length=1024, blank=True, null=True)
    address2 = models.CharField("Address line 2", max_length=1024, blank=True, null=True)
    zip_code = models.CharField("Postal Code", max_length=12, blank=True, null=True)
    city = models.CharField("Municipality", max_length=1024, blank=True, null=True)
    state = models.CharField("County/State", max_length=1024, blank=True, null=True)
    country = models.CharField("Country", max_length=1024, blank=True, null=True)

    facebook_link = models.CharField(max_length=120, blank=True, null=True)
    twitter = models.CharField(max_length=120, blank=True, null=True)
    linkedin_link = models.CharField(max_length=120, blank=True, null=True)
    other_social_media = models.CharField(max_length=120, blank=True, null=True)

    stripe_customer_id = models.CharField(max_length=120, blank=True, null=True)
    subscription_type = models.CharField(
        max_length=20, default="groundplan", verbose_name="Subscription type"
    )

    date_of_birth = models.DateField("Date of birth", blank=True, null=True)
    about = models.TextField("About me", max_length=120, default="The user did not put any thing yet")

    phone_otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = UserManager()

    def __str__(self):
        return f"email={self.email} site_id={self.site_id}"

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        born = self.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def _pre_save_fill_name(sender, instance: CustomUser, **kwargs):
    if not instance.name:
        instance.name = instance.first_name or instance.name


pre_save.connect(_pre_save_fill_name, sender=CustomUser)
