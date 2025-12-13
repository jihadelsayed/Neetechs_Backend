import hashlib

from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.core.exceptions import ValidationError

from .models import User


def _placeholder_email_for_phone(phone: str) -> str:
    return f"{hashlib.sha256(phone.encode('utf-8')).hexdigest()[:10]}@phone.neetechs.invalid"


class UserCreationForm(DjangoUserCreationForm):
    """
    Admin "Add user" form.
    Allows email OR phone (to match your actual signup rules).
    Username is optional (auto-generated if missing).
    """

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ("email", "phone", "username", "handle", "display_name")

    def clean(self):
        cleaned = super().clean()
        email = (cleaned.get("email") or "").strip()
        phone = (cleaned.get("phone") or "").strip()

        if not email and not phone:
            raise ValidationError("Provide either email or phone.")

        # normalize blanks -> None
        cleaned["email"] = email or None
        cleaned["phone"] = phone or None

        # If phone-only, set a safe placeholder email so model constraint (unique email) is satisfied.
        if not cleaned["email"] and cleaned["phone"]:
            cleaned["email"] = _placeholder_email_for_phone(cleaned["phone"])

        return cleaned

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip()
        if phone and User.objects.filter(phone=phone).exists():
            raise ValidationError("A user with this phone already exists.")
        return phone

    def clean_handle(self):
        handle = (self.cleaned_data.get("handle") or "").strip().lower()
        if not handle:
            return None
        if User.objects.filter(handle=handle).exists():
            raise ValidationError("Handle already taken.")
        return handle


class UserChangeForm(DjangoUserChangeForm):
    """
    Admin "Change user" form.
    """

    password = None  # hide hashed password field on main edit form

    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "username",
            "handle",
            "display_name",
            "first_name",
            "last_name",
            "site_id",
            "is_admin",
            "is_creator",
            "profession",
            "profile_completed",
            "picture",
            "picture_medium",
            "picture_small",
            "picture_tag",
            "facebook_link",
            "twitter",
            "linkedin_link",
            "other_social_media",
            "bio",
            "about",
            "date_of_birth",
            "location",
            "address1",
            "address2",
            "city",
            "state",
            "zip_code",
            "country",
            "stripe_customer_id",
            "subscription_type",
            "members",
            "followers",
            "earning",
            "rating",
            "member_since",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class UserLoginForm(forms.Form):
    identifier = forms.CharField(label="Email or Phone")
    password = forms.CharField(widget=forms.PasswordInput)
