from django.contrib import admin
from django.utils.html import format_html

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin personalizado para productos Buddy."""

    list_display = ('image_preview', 'name', 'price', 'badge_label', 'is_published', 'sort_order')
    list_editable = ('price', 'is_published', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'teaser', 'description')
    list_filter = ('is_published', 'badge_label')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'teaser', 'description')
        }),
        ('Precio y Estado', {
            'fields': ('price', 'delivery_estimate', 'badge_label', 'is_published', 'sort_order')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Muestra preview si hay imagen (placeholder por ahora)."""
        return format_html(
            '<div style="width:50px;height:50px;background:linear-gradient(135deg,#3C9E5D,#277947);'
            'border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;'
            'font-weight:bold;">{}</div>',
            obj.name[:2].upper()
        )

    image_preview.short_description = 'Vista Previa'

