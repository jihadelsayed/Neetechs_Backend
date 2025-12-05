from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User as User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    # Which fields are shown on the user edit page
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "username",
                    "display_name",
                    "first_name",
                    "last_name",
                    "site_id",
                    "phone",
                    "profession",
                    "profile_completed",
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
                    "picture",
                    "picture_medium",
                    "picture_small",
                    "picture_tag",
                    "facebook_link",
                    "twitter",
                    "linkedin_link",
                    "other_social_media",
                    "stripe_customer_id",
                    "subscription_type",
                    "members",
                    "followers",
                    "earning",
                    "rating",
                    "member_since",
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
                    "is_admin",
                    "is_creator",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined")},
        ),
    )

    # Fields shown on the "Add user" page in admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "display_name",
                    "phone",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    list_display = (
        "email",
        "username",
        "display_name",
        "is_staff",
        "is_active",
        "is_superuser",
        "is_creator",
        "subscription_type",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "is_admin",
        "is_creator",
        "subscription_type",
        "country",
    )
    search_fields = ("email", "username", "display_name", "phone", "site_id")
    ordering = ("email",)

    readonly_fields = ("site_id", "date_joined", "last_login", "member_since")
