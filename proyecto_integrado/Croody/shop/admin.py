"""Admin configuration para Shop app - Croody."""

from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin para Product."""
    list_display = ('name', 'price', 'is_published', 'badge_label')
    list_filter = ('is_published', 'badge_label')
    search_fields = ('name', 'description', 'teaser')
    list_editable = ('price', 'is_published')
    readonly_fields = ('slug',)
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'teaser', 'description')
        }),
        ('Precio', {
            'fields': ('price',)
        }),
        ('Estado', {
            'fields': ('is_published', 'badge_label', 'delivery_estimate')
        }),
    )
