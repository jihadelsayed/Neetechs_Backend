
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser as User
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "site_id",
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
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "member_since")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "name", "phone"),
            },
        ),
    )

    list_display = ("email", "name", "is_staff", "is_active", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_active", "is_admin", "is_creator", "subscription_type", "country")
    search_fields = ("email", "name", "phone", "site_id")
    ordering = ("email",)
