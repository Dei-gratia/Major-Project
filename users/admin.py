from django.contrib import admin
from .models import User, Profile, Review
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


# ====== REVIEW ADMIN =====
class ReviewAdmin(admin.ModelAdmin):
    model = Review
    extra = 0

    list_display = ['user', 'rate_value', 'comment', 'content_object', 'date']
    list_filter = ['date', 'user', 'content_object']
    search_fields = ['comment', 'rate_value']


admin.site.register(Review, ReviewAdmin)


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
