import os
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Image, Tier, ThumbnailSize


@admin.register(ThumbnailSize)
class ThumbnailSizeAdmin(admin.ModelAdmin):
    pass


class ThumbnailInline(admin.TabularInline):
    model = ThumbnailSize
    extra = 1


class CustomUserInline(admin.TabularInline):
    model = CustomUser
    extra = 0

    fields = ['username']

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    inlines = [ThumbnailInline, CustomUserInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['fileName', 'owner']
    exclude = ['id', 'expiring_link_created_at',
               'token', 'link_expiration_time']

    # Function for geting file name

    def fileName(self, obj):
        return os.path.basename(obj.file.name)


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'tier']

    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'tier')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'tier')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        })
    )


admin.site.register(CustomUser, CustomUserAdmin)
