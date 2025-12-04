"""Modelos de la tienda Buddy."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse

if TYPE_CHECKING:
    from django.contrib.auth.models import User


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


class OrderStatus(models.TextChoices):
    """Estados posibles de una orden."""
    PENDING = 'pending', 'Pendiente'
    CONFIRMED = 'confirmed', 'Confirmada'
    PROCESSING = 'processing', 'Procesando'
    SHIPPED = 'shipped', 'Enviada'
    DELIVERED = 'delivered', 'Entregada'
    CANCELLED = 'cancelled', 'Cancelada'
    REFUNDED = 'refunded', 'Reembolsada'


class PaymentStatus(models.TextChoices):
    """Estados de pago."""
    PENDING = 'pending', 'Pendiente'
    PROCESSING = 'processing', 'Procesando'
    COMPLETED = 'completed', 'Completado'
    FAILED = 'failed', 'Fallido'
    REFUNDED = 'refunded', 'Reembolsado'
    CANCELLED = 'cancelled', 'Cancelado'


class PaymentMethod(models.TextChoices):
    """Métodos de pago disponibles."""
    STRIPE = 'stripe', 'Tarjeta (Stripe)'
    PAYPAL = 'paypal', 'PayPal'
    BANK_TRANSFER = 'bank_transfer', 'Transferencia Bancaria'
    CASH_ON_DELIVERY = 'cash_on_delivery', 'Pago Contra Entrega'


class PaymentProvider(models.TextChoices):
    """Proveedores de pago."""
    STRIPE = 'stripe', 'Stripe'
    PAYPAL = 'paypal', 'PayPal'
    MANUAL = 'manual', 'Manual'


class Order(models.Model):
    """Orden de compra."""
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        default=PaymentMethod.STRIPE
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    
    # Datos de facturación y envío
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Dirección de envío
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='España')
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self) -> str:
        return f'Orden #{self.id}'

    def save(self, *args, **kwargs) -> None:
        """Generar ID único si no existe."""
        if not self.id:
            self.id = self.generate_order_id()
        super().save(*args, **kwargs)

    def generate_order_id(self) -> str:
        """Generar ID único para la orden."""
        from django.utils import timezone
        import secrets
        
        timestamp = timezone.now().strftime('%y%m%d')
        random_part = secrets.token_hex(3).upper()
        return f'ORD-{timestamp}-{random_part}'

    def calculate_total(self) -> Decimal:
        """Calcular total de la orden basado en items."""
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.subtotal
        self.total = total
        return total

    @property
    def item_count(self) -> int:
        """Cantidad total de items en la orden."""
        return sum(item.quantity for item in self.items.all())

    def get_absolute_url(self) -> str:
        return reverse('shop:order-confirmation', args=[self.id])


class OrderItem(models.Model):
    """Item individual en una orden."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'product')
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]

    def __str__(self) -> str:
        return f'{self.product.name} x{self.quantity}'

    def save(self, *args, **kwargs) -> None:
        """Calcular subtotal automáticamente."""
        self.subtotal = self.price_at_purchase * self.quantity
        super().save(*args, **kwargs)
        
        # Actualizar total de la orden
        if self.order:
            self.order.calculate_total()
            self.order.save(update_fields=['total'])


class Transaction(models.Model):
    """Registro de transacción de pago."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    provider = models.CharField(
        max_length=20,
        choices=PaymentProvider.choices,
        default=PaymentProvider.STRIPE
    )
    provider_id = models.CharField(max_length=100, blank=True)
    provider_response = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['order', 'status']),
            models.Index(fields=['provider', 'provider_id']),
        ]

    def __str__(self) -> str:
        return f'Transacción {self.id} - {self.order.id}'
