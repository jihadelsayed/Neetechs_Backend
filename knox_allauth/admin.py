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
