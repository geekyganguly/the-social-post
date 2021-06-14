from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User


class UserAdminConfig(UserAdmin):
    model = User
    list_display = ('username', 'phone', 'email', 'first_name')
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'username', 'password')}),
        ('Profile', {'fields': ('first_name',
         'last_name', 'bio', 'profile_pic')}),
        ('Connection', {'fields': ('connection',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {'fields': ('phone', 'email', 'username', 'password1', 'password2')}),
        ('Profile', {'fields': ('first_name',
         'last_name', 'bio', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),

    )


admin.site.register(User, UserAdminConfig)
admin.site.unregister(Group)
admin.site.site_header = 'The Social Post Admin'
