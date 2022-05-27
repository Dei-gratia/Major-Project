from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

# ======PROFILE ADMIN======


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1

# ======USER ADMIN======


class UserAdmin(BaseUserAdmin, admin.ModelAdmin):

    model = User
    inlines = [ProfileInline]
    fieldsets = (
        (None, {'fields': ('email', 'password',
                           'first_name', 'last_name', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
