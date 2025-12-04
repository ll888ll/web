"""Admin configuration para Telemetry app - Croody."""

from django.contrib import admin
from .models import RobotPosition


@admin.register(RobotPosition)
class RobotPositionAdmin(admin.ModelAdmin):
    """Admin para RobotPosition."""
    list_display = ('timestamp', 'x', 'y', 'atmosphere')
    list_filter = ('timestamp',)
    search_fields = ('x', 'y')
    readonly_fields = ('timestamp',)

    fieldsets = (
        ('Posición', {
            'fields': ('x', 'y')
        }),
        ('Atmósfera', {
            'fields': ('atmosphere',)
        }),
        ('Metadatos', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )
