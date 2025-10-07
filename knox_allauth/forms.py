
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "name", "phone")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and CustomUser.objects.filter(phone=phone).exists():
            raise ValidationError("A user with this phone already exists.")
        return phone


class CustomUserChangeForm(UserChangeForm):
    password = None  # hide unusable raw password field in admin edit

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "name",
            "first_name",
            "phone",
            "sms",
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
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class UserLoginForm(forms.Form):
    identifier = forms.CharField(label="Email or Phone")
    password = forms.CharField(widget=forms.PasswordInput)
