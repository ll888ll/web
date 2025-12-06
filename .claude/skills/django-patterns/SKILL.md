---
name: django-patterns
description: Patrones de Django/FastAPI para Croody. Use cuando trabaje en backend, modelos, vistas, APIs o cualquier código Python del proyecto.
---

# Django Patterns - Croody Backend Guide

> Guía de patrones y convenciones para desarrollo backend en el ecosistema Croody.

---

## Filosofía

El backend de Croody sigue el principio **Fat Models, Thin Views**:
- **Modelos**: Contienen lógica de negocio, validaciones, métodos de utilidad
- **Vistas**: Solo coordinan flujo, delegan a modelos y services
- **Services**: Lógica compleja que involucra múltiples modelos

---

## Patrones de Modelos

### Estructura Base

```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Product(models.Model):
    """
    Producto del catálogo de la tienda.

    Atributos:
        name: Nombre del producto (max 200 chars)
        slug: URL-friendly identifier (único)
        price: Precio en USD (2 decimales)
        is_active: Si está disponible para venta
    """

    # Campos principales
    name = models.CharField(
        _('Nombre'),
        max_length=200,
        help_text=_('Nombre visible en catálogo')
    )
    slug = models.SlugField(
        _('Slug'),
        unique=True,
        db_index=True
    )
    description = models.TextField(
        _('Descripción'),
        blank=True
    )
    price = models.DecimalField(
        _('Precio'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    # Estado
    is_active = models.BooleanField(
        _('Activo'),
        default=True,
        db_index=True
    )

    # Timestamps
    created_at = models.DateTimeField(_('Creado'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Actualizado'), auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Producto')
        verbose_name_plural = _('Productos')
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self):
        return self.name

    # Fat Model Methods
    def get_display_price(self) -> str:
        """Retorna precio formateado para display."""
        return f"${self.price:,.2f}"

    def is_available(self) -> bool:
        """Verifica disponibilidad del producto."""
        return self.is_active and self.stock > 0

    def apply_discount(self, percentage: Decimal) -> Decimal:
        """Calcula precio con descuento."""
        discount = self.price * (percentage / 100)
        return self.price - discount

    @classmethod
    def get_featured(cls, limit: int = 6):
        """Obtiene productos destacados."""
        return cls.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category')[:limit]
```

### Managers Personalizados

```python
class ProductQuerySet(models.QuerySet):
    """QuerySet personalizado para Product."""

    def active(self):
        """Solo productos activos."""
        return self.filter(is_active=True)

    def in_category(self, category_slug: str):
        """Filtrar por categoría."""
        return self.filter(category__slug=category_slug)

    def in_price_range(self, min_price: Decimal, max_price: Decimal):
        """Filtrar por rango de precio."""
        return self.filter(price__gte=min_price, price__lte=max_price)

    def with_stock(self):
        """Solo productos con stock."""
        return self.filter(stock__gt=0)


class ProductManager(models.Manager):
    """Manager personalizado para Product."""

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def available(self):
        """Productos activos con stock."""
        return self.get_queryset().active().with_stock()


class Product(models.Model):
    # ... campos ...

    objects = ProductManager()
```

### Signals (Cuando sea necesario)

```python
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

@receiver(pre_save, sender=Product)
def generate_slug(sender, instance, **kwargs):
    """Genera slug automáticamente si está vacío."""
    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(post_save, sender=Order)
def notify_order_created(sender, instance, created, **kwargs):
    """Notifica cuando se crea una orden."""
    if created:
        # Enviar email, crear notificación, etc.
        from shop.tasks import send_order_confirmation
        send_order_confirmation.delay(instance.id)
```

---

## Patrones de Vistas

### Class-Based Views (Preferido)

```python
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

class ProductListView(ListView):
    """
    Lista de productos del catálogo.

    GET /shop/products/
    """
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """Solo productos activos con categoría precargada."""
        return Product.objects.active().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured'] = Product.get_featured(limit=3)
        return context


class ProductDetailView(DetailView):
    """
    Detalle de producto.

    GET /shop/products/<slug>/
    """
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.active().select_related('category')


class OrderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Crear nueva orden.

    POST /shop/orders/create/
    """
    model = Order
    form_class = OrderForm
    template_name = 'shop/order_create.html'
    success_url = reverse_lazy('shop:order-success')
    success_message = "Orden creada exitosamente"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
```

### Function-Based Views (Casos específicos)

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

@login_required
@require_POST
def add_to_cart(request, product_id):
    """
    Agrega producto al carrito.

    POST /shop/cart/add/<product_id>/
    """
    product = get_object_or_404(Product.objects.active(), id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    request.session['cart'] = cart

    if request.headers.get('HX-Request'):
        # HTMX request - retornar fragmento
        return render(request, 'shop/partials/cart_count.html', {
            'cart_count': sum(cart.values())
        })

    return redirect('shop:cart')
```

---

## Patrones de FastAPI

### Estructura de Endpoint

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

# Schemas (Pydantic)
class EventCreate(BaseModel):
    """Schema para crear evento de telemetría."""
    event_type: str = Field(..., min_length=1, max_length=50)
    payload: dict = Field(default_factory=dict)
    timestamp: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "page_view",
                "payload": {"page": "/home", "duration": 1500}
            }
        }


class EventResponse(BaseModel):
    """Schema de respuesta de evento."""
    id: int
    event_type: str
    created_at: datetime


# Endpoints
@router.post(
    "/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear evento de telemetría",
    description="Registra un nuevo evento de telemetría en el sistema."
)
async def create_event(event: EventCreate):
    """
    Crea un evento de telemetría.

    - **event_type**: Tipo de evento (page_view, click, etc.)
    - **payload**: Datos adicionales del evento
    - **timestamp**: Timestamp opcional (default: now)
    """
    # Lógica de creación
    new_event = await EventService.create(event)
    return new_event


@router.get(
    "/events",
    response_model=List[EventResponse],
    summary="Listar eventos"
)
async def list_events(
    event_type: Optional[str] = Query(None, description="Filtrar por tipo"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Lista eventos con paginación."""
    events = await EventService.list(
        event_type=event_type,
        limit=limit,
        offset=offset
    )
    return events
```

### Dependencias

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Dependencia para autenticación."""
    token = credentials.credentials
    user = await verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    return user


async def get_db():
    """Dependencia para conexión de DB."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Uso
@router.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"message": f"Hola {user.name}"}
```

---

## Optimización de Queries

### Select Related / Prefetch Related

```python
# ❌ MAL: N+1 queries
products = Product.objects.all()
for product in products:
    print(product.category.name)  # Query por cada producto

# ✅ BIEN: 1 query con JOIN
products = Product.objects.select_related('category').all()

# ❌ MAL: N+1 en relación many-to-many
orders = Order.objects.all()
for order in orders:
    for item in order.items.all():  # Query por cada orden
        print(item.product.name)

# ✅ BIEN: Prefetch para many-to-many
orders = Order.objects.prefetch_related(
    'items',
    'items__product'
).all()
```

### Only / Defer

```python
# Solo campos necesarios
products = Product.objects.only('name', 'price', 'slug')

# Excluir campos pesados
products = Product.objects.defer('description', 'full_specifications')
```

### Aggregations

```python
from django.db.models import Count, Sum, Avg, F, Q

# Contar productos por categoría
Category.objects.annotate(product_count=Count('products'))

# Total de ventas
Order.objects.filter(status='completed').aggregate(
    total=Sum('total'),
    average=Avg('total'),
    count=Count('id')
)

# Filtros complejos
Product.objects.filter(
    Q(is_active=True) & (Q(stock__gt=0) | Q(preorder=True))
)
```

---

## Forms

### ModelForm

```python
from django import forms
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    """Form para crear/editar productos."""

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean_price(self):
        """Validación de precio."""
        price = self.cleaned_data.get('price')
        if price and price < Decimal('0.01'):
            raise ValidationError('El precio debe ser mayor a $0.01')
        return price

    def clean(self):
        """Validación cross-field."""
        cleaned_data = super().clean()
        is_active = cleaned_data.get('is_active')
        stock = cleaned_data.get('stock', 0)

        if is_active and stock == 0:
            raise ValidationError(
                'No se puede activar un producto sin stock'
            )
        return cleaned_data
```

---

## Services (Lógica Compleja)

```python
# shop/services.py

from decimal import Decimal
from typing import Optional
from django.db import transaction
from django.core.mail import send_mail

class OrderService:
    """Servicio para operaciones de órdenes."""

    @staticmethod
    @transaction.atomic
    def create_order(user, cart_items: list) -> Order:
        """
        Crea una orden a partir del carrito.

        Args:
            user: Usuario que realiza la compra
            cart_items: Lista de items del carrito

        Returns:
            Order: Orden creada

        Raises:
            ValidationError: Si no hay stock suficiente
        """
        # Validar stock
        for item in cart_items:
            if item['product'].stock < item['quantity']:
                raise ValidationError(
                    f"Stock insuficiente para {item['product'].name}"
                )

        # Crear orden
        order = Order.objects.create(
            user=user,
            status='pending'
        )

        # Crear items y actualizar stock
        total = Decimal('0')
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
            item['product'].stock -= item['quantity']
            item['product'].save()
            total += item['product'].price * item['quantity']

        order.total = total
        order.save()

        # Enviar email (async)
        send_order_confirmation_email.delay(order.id)

        return order

    @staticmethod
    def cancel_order(order: Order, reason: str) -> None:
        """Cancela una orden y restaura stock."""
        with transaction.atomic():
            for item in order.items.all():
                item.product.stock += item.quantity
                item.product.save()

            order.status = 'cancelled'
            order.cancellation_reason = reason
            order.save()
```

---

## Testing Patterns

### Fixtures con Factory Boy

```python
import factory
from factory.django import DjangoModelFactory
from shop.models import Product, Category

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category {n}')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('product_name')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    category = factory.SubFactory(CategoryFactory)
    is_active = True
```

---

## Prohibiciones

| Prohibido | Usar En Su Lugar |
|-----------|------------------|
| Raw SQL sin parametrizar | ORM de Django |
| Lógica en vistas | Fat Models o Services |
| `objects.all()` sin limitar | Paginación + filtros |
| Hardcodear configuración | `settings.py` o env vars |
| Print para debug | `logging` module |

---

## Recursos

- **Settings**: `/proyecto_integrado/Croody/croody/settings/`
- **Modelos Shop**: `/proyecto_integrado/Croody/shop/models.py`
- **Views Shop**: `/proyecto_integrado/Croody/shop/views.py`
- **Documentación**: `/docs/02-BACKEND/`
