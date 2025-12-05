from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(UserCreationForm):
    """
    Used in admin when adding a new user.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        # What the admin “Add user” form will ask for
        fields = ("email", "username", "display_name", "phone")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username__iexact=username).exists():
            raise ValidationError("A user with this username already exists.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and User.objects.filter(phone=phone).exists():
            raise ValidationError("A user with this phone already exists.")
        return phone


class UserChangeForm(UserChangeForm):
    """
    Used in admin when editing an existing user.
    We don’t expose the raw password field; DjangoUserAdmin will still
    handle password change via the built-in “Change password” form.
    """

    password = None  # hide the hashed password field on the main edit form

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "display_name",
            "first_name",
            "last_name",
            "phone",
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
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class UserLoginForm(forms.Form):
    # This one can stay as-is; depends on how your login view works
    identifier = forms.CharField(label="Email or Phone")
    password = forms.CharField(widget=forms.PasswordInput)
