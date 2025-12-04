"""Admin configuration para Landing app - Croody."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin para UserProfile."""
    list_display = ('user', 'display_name', 'preferred_language', 'preferred_theme', 'notification_level')
    list_filter = ('preferred_language', 'preferred_theme', 'notification_level', 'telemetry_alerts')
    search_fields = ('user__username', 'user__email', 'display_name', 'bio')
    readonly_fields = ('ingest_token', 'created_at', 'updated_at')

    fieldsets = (
        ('Usuario', {
            'fields': ('user', 'display_name')
        }),
        ('Preferencias', {
            'fields': ('preferred_language', 'preferred_theme', 'timezone', 'notification_level')
        }),
        ('Telemetry', {
            'fields': ('telemetry_alerts', 'ingest_token', 'favorite_robot')
        }),
        ('Perfil', {
            'fields': ('bio',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Extender User admin para mostrar UserProfile
class UserProfileInline(admin.StackedInline):
    """Inline para UserProfile en User admin."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fields = ('display_name', 'preferred_language', 'preferred_theme', 'notification_level', 'bio')


class CustomUserAdmin(BaseUserAdmin):
    """Custom User Admin con UserProfile inline."""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


# Re-registrar User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)