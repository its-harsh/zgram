from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('User Profile', {'fields': ('full_name',
                                     'website', 'bio', 'image', 'gender')}),
        ('Account Settings', {
         'fields': ('is_active', 'is_private', 'creator_account')}),
        ('Account Credentials', {'fields': ('username', 'email', 'password')}),
        ('Permissions & Groups', {
         'fields': ('is_staff', 'is_superuser', 'user_permissions', 'groups')})
    )
    add_fieldsets = (
        (None, {'fields': ('username',
                           'email', 'password', 'confirm_password')}),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'full_name')
    list_filter = ('is_active', 'is_private', 'gender',
                   'is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'email', 'full_name')
    filter_horizontal = ('user_permissions', 'groups')
    ordering = ('username', )
