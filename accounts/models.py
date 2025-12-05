# accounts/models.py

import os
import random
import string
from binascii import hexlify
from datetime import date

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill


def generate_site_id(length: int = 10) -> str:
  chars = string.ascii_letters + string.digits
  return "".join(random.SystemRandom().choice(chars) for _ in range(length))


def upload_avatar(instance, filename: str) -> str:
  ext = filename.split(".")[-1].lower()
  return f"pictures/{instance.site_id}.{ext or 'png'}"


class UserManager(BaseUserManager):
  """
  Email as login, username required, no magic auto-usernames.
  """

  use_in_migrations = True

  def _create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError("The email address must be set")

    email = self.normalize_email(email)
    extra_fields.setdefault("is_staff", False)
    extra_fields.setdefault("is_superuser", False)

    # ensure site_id
    site_id = extra_fields.get("site_id") or generate_site_id()
    extra_fields["site_id"] = site_id

    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password=None, **extra_fields):
    extra_fields.setdefault("is_active", True)
    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    extra_fields.setdefault("is_active", True)

    if extra_fields.get("is_staff") is not True:
      raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
      raise ValueError("Superuser must have is_superuser=True.")

    return self._create_user(email, password, **extra_fields)
username_validator = UnicodeUsernameValidator()


class User(AbstractBaseUser, PermissionsMixin):
  # CORE IDENTITY
  email = models.EmailField(
    _("email address"),
    unique=True,
    db_index=True,
  )

  username = models.CharField(
    _("username"),
    max_length=50,
    unique=True,
    db_index=True,
    validators=[username_validator],
    help_text=_("Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."),
    error_messages={
      "unique": _("A user with that username already exists."),
    },
  )

  # What you show in the UI (“Full name” / display name)
  display_name = models.CharField(
    _("display name"),
    max_length=80,
    blank=True,
    null=True,
  )

  # Optional first/last if you ever need them (not required for login)
  first_name = models.CharField(_("first name"), max_length=50, blank=True)
  last_name = models.CharField(_("last name"), max_length=50, blank=True)

  phone = models.CharField(
    max_length=20,
    blank=True,
    null=True,
    help_text=_("E.164 phone number (+15551234567)."),
  )

  # Stable per-user ID for URLs / external references
  site_id = models.CharField(
    max_length=32,
    default=generate_site_id,
    unique=True,
    db_index=True,
  )

  # FLAGS / STATUS
  is_staff = models.BooleanField(_("staff status"), default=False)
  is_active = models.BooleanField(_("active"), default=True)
  date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

  is_admin = models.BooleanField(default=False)
  is_creator = models.BooleanField(default=False)
  profile_completed = models.BooleanField(default=False)

  # PROFILE / SOCIAL
  bio = models.CharField(max_length=500, blank=True, null=True)
  rating = models.DecimalField(
    default=0,
    decimal_places=1,
    max_digits=2,
    validators=[MaxValueValidator(5), MinValueValidator(0)],
  )
  members = models.PositiveIntegerField(default=0)
  followers = models.PositiveIntegerField(default=0)
  earning = models.PositiveIntegerField(default=0)

  profession = models.CharField(max_length=100, blank=True, null=True)
  location = models.CharField(max_length=100, blank=True, null=True)

  member_since = models.DateTimeField(default=timezone.now, null=True, blank=True)

  # AVATARS (imagekit)
  picture = ProcessedImageField(
    format="PNG",
    processors=[ResizeToFill(512, 512)],
    options={"quality": 70},
    upload_to=upload_avatar,
    blank=True,
    null=True,
    default="ProfileDefaultImage.png",
  )
  picture_medium = ProcessedImageField(
    format="PNG",
    processors=[ResizeToFill(256, 256)],
    options={"quality": 70},
    upload_to=upload_avatar,
    blank=True,
    null=True,
    default="ProfileDefaultImage.png",
  )
  picture_small = ProcessedImageField(
    format="PNG",
    processors=[ResizeToFill(128, 128)],
    options={"quality": 70},
    upload_to=upload_avatar,
    blank=True,
    null=True,
    default="ProfileDefaultImage.png",
  )
  picture_tag = ProcessedImageField(
    format="PNG",
    processors=[ResizeToFill(28, 28)],
    options={"quality": 70},
    upload_to=upload_avatar,
    blank=True,
    null=True,
    default="ProfileDefaultImage.png",
  )

  # ADDRESS
  address1 = models.CharField("Address line 1", max_length=255, blank=True, null=True)
  address2 = models.CharField("Address line 2", max_length=255, blank=True, null=True)
  zip_code = models.CharField("Postal Code", max_length=20, blank=True, null=True)
  city = models.CharField("City", max_length=100, blank=True, null=True)
  state = models.CharField("State / Region", max_length=100, blank=True, null=True)
  country = models.CharField("Country", max_length=100, blank=True, null=True)

  # SOCIAL
  facebook_link = models.URLField(max_length=255, blank=True, null=True)
  twitter = models.URLField(max_length=255, blank=True, null=True)
  linkedin_link = models.URLField(max_length=255, blank=True, null=True)
  other_social_media = models.URLField(max_length=255, blank=True, null=True)

  # STRIPE / BILLING
  stripe_customer_id = models.CharField(max_length=120, blank=True, null=True)
  subscription_type = models.CharField(
    max_length=20,
    default="groundplan",
    verbose_name="Subscription type",
  )

  # PERSONAL
  date_of_birth = models.DateField("Date of birth", blank=True, null=True)
  about = models.TextField(
    "About me",
    max_length=255,
    default="The user did not put anything yet",
  )

  # OTP (phone verification etc.)
  phone_otp = models.CharField(max_length=6, blank=True, null=True)
  otp_created_at = models.DateTimeField(blank=True, null=True)

  USERNAME_FIELD = "email"          # login by email
  REQUIRED_FIELDS = ["username"]    # when creating superuser via CLI

  objects = UserManager()

  class Meta:
    verbose_name = "user"
    verbose_name_plural = "users"
    ordering = ["-date_joined"]

  def __str__(self):
    return f"{self.email} ({self.username})"

  @property
  def age(self):
    if not self.date_of_birth:
      return None
    today = date.today()
    born = self.date_of_birth
    return today.year - born.year - (
      (today.month, today.day) < (born.month, born.day)
    )

  @property
  def name(self) -> str:
    """
    Backwards-compatible 'name' property for templates / serializers.
    """
    return self.display_name or f"{self.first_name} {self.last_name}".strip() or self.username
