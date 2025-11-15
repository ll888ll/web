from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_published', 'sort_order')
    list_editable = ('price', 'is_published', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'teaser', 'description')
    list_filter = ('is_published',)

