"""Modelos de la tienda Buddy."""
from __future__ import annotations

from django.db import models
from django.urls import reverse


class ProductQuerySet(models.QuerySet):
    def published(self) -> 'ProductQuerySet':
        return self.filter(is_published=True)

    def search(self, query: str) -> 'ProductQuerySet':
        if not query:
            return self
        return self.filter(models.Q(name__icontains=query) | models.Q(teaser__icontains=query))


class Product(models.Model):
    """Producto Buddy."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    teaser = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_estimate = models.CharField(max_length=100, default='Entrega 3 días')
    badge_label = models.CharField(max_length=32, blank=True)
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ('sort_order', 'name')

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('shop:detail', args=[self.slug])

