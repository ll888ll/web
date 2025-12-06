# Modelos de E-Commerce (Order, OrderItem, Transaction)

## Resumen
Los modelos de e-commerce en la app `shop` gestionan el flujo completo de compras: ordenes, items de orden y transacciones de pago.

## Ubicacion
`/proyecto_integrado/Croody/shop/models.py`

---

## Modelo Order

### Descripcion
Representa una orden de compra completa con datos de usuario, direccion de envio y estado de pago.

### Campos

| Campo | Tipo | Descripcion | Por Defecto |
|-------|------|-------------|-------------|
| `id` | CharField(20) | ID unico (ej: ORD-241205-A1B2C3) | Auto-generado |
| `user` | ForeignKey(User) | Usuario que realiza la compra | REQUIRED |
| `status` | CharField(20) | Estado de la orden | "pending" |
| `total` | DecimalField(10,2) | Total de la orden | 0.00 |
| `payment_method` | CharField(30) | Metodo de pago | "stripe" |
| `payment_status` | CharField(20) | Estado del pago | "pending" |

#### Datos de Facturacion
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `first_name` | CharField(50) | Nombre |
| `last_name` | CharField(50) | Apellido |
| `email` | EmailField | Email de contacto |
| `phone` | CharField(20) | Telefono (opcional) |

#### Direccion de Envio
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `address_line_1` | CharField(100) | Direccion principal |
| `address_line_2` | CharField(100) | Direccion secundaria (opcional) |
| `city` | CharField(50) | Ciudad |
| `state` | CharField(50) | Estado/Provincia (opcional) |
| `postal_code` | CharField(10) | Codigo postal |
| `country` | CharField(50) | Pais (default: "Espana") |

#### Metadata
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `notes` | TextField | Notas del cliente |
| `created_at` | DateTimeField | Fecha de creacion |
| `updated_at` | DateTimeField | Fecha de actualizacion |

### Choices

#### OrderStatus
```python
class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pendiente'
    CONFIRMED = 'confirmed', 'Confirmada'
    PROCESSING = 'processing', 'Procesando'
    SHIPPED = 'shipped', 'Enviada'
    DELIVERED = 'delivered', 'Entregada'
    CANCELLED = 'cancelled', 'Cancelada'
    REFUNDED = 'refunded', 'Reembolsada'
```

#### PaymentStatus
```python
class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pendiente'
    PROCESSING = 'processing', 'Procesando'
    COMPLETED = 'completed', 'Completado'
    FAILED = 'failed', 'Fallido'
    REFUNDED = 'refunded', 'Reembolsado'
    CANCELLED = 'cancelled', 'Cancelado'
```

#### PaymentMethod
```python
class PaymentMethod(models.TextChoices):
    STRIPE = 'stripe', 'Tarjeta (Stripe)'
    PAYPAL = 'paypal', 'PayPal'
    BANK_TRANSFER = 'bank_transfer', 'Transferencia Bancaria'
    CASH_ON_DELIVERY = 'cash_on_delivery', 'Pago Contra Entrega'
```

### Metodos

#### generate_order_id()
```python
def generate_order_id(self) -> str:
    """Generar ID unico para la orden."""
    from django.utils import timezone
    import secrets

    timestamp = timezone.now().strftime('%y%m%d')
    random_part = secrets.token_hex(3).upper()
    return f'ORD-{timestamp}-{random_part}'

# Ejemplo: ORD-241205-A1B2C3
```

#### calculate_total()
```python
def calculate_total(self) -> Decimal:
    """Calcular total de la orden basado en items."""
    total = Decimal('0.00')
    for item in self.items.all():
        total += item.subtotal
    self.total = total
    return total
```

#### item_count (property)
```python
@property
def item_count(self) -> int:
    """Cantidad total de items en la orden."""
    return sum(item.quantity for item in self.items.all())
```

### Indices
```python
class Meta:
    ordering = ('-created_at',)
    indexes = [
        models.Index(fields=['user', 'status']),
        models.Index(fields=['payment_status']),
    ]
```

---

## Modelo OrderItem

### Descripcion
Representa un item individual dentro de una orden.

### Campos

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `order` | ForeignKey(Order) | Orden padre |
| `product` | ForeignKey(Product) | Producto |
| `quantity` | PositiveIntegerField | Cantidad |
| `price_at_purchase` | DecimalField(8,2) | Precio al momento de compra |
| `subtotal` | DecimalField(10,2) | Subtotal (precio * cantidad) |

### Meta
```python
class Meta:
    unique_together = ('order', 'product')  # No duplicar productos
    indexes = [
        models.Index(fields=['order']),
        models.Index(fields=['product']),
    ]
```

### Comportamiento de save()
```python
def save(self, *args, **kwargs) -> None:
    """Calcular subtotal automaticamente."""
    self.subtotal = self.price_at_purchase * self.quantity
    super().save(*args, **kwargs)

    # Actualizar total de la orden
    if self.order:
        self.order.calculate_total()
        self.order.save(update_fields=['total'])
```

---

## Modelo Transaction

### Descripcion
Registro de transaccion de pago asociada a una orden.

### Campos

| Campo | Tipo | Descripcion | Por Defecto |
|-------|------|-------------|-------------|
| `order` | ForeignKey(Order) | Orden asociada | REQUIRED |
| `amount` | DecimalField(10,2) | Monto | REQUIRED |
| `status` | CharField(20) | Estado | "pending" |
| `provider` | CharField(20) | Proveedor | "stripe" |
| `provider_id` | CharField(100) | ID del proveedor | "" |
| `provider_response` | JSONField | Respuesta del proveedor | {} |
| `created_at` | DateTimeField | Fecha de creacion | auto |
| `updated_at` | DateTimeField | Fecha de actualizacion | auto |

### Choices

#### PaymentProvider
```python
class PaymentProvider(models.TextChoices):
    STRIPE = 'stripe', 'Stripe'
    PAYPAL = 'paypal', 'PayPal'
    MANUAL = 'manual', 'Manual'
```

### Indices
```python
class Meta:
    ordering = ('-created_at',)
    indexes = [
        models.Index(fields=['order', 'status']),
        models.Index(fields=['provider', 'provider_id']),
    ]
```

---

## Flujo de Checkout

### 1. Crear Orden
```python
from shop.models import Order, OrderItem, OrderStatus, PaymentMethod

def create_order(user, cart_items, shipping_data, payment_method):
    """Crea una orden desde el carrito."""
    order = Order.objects.create(
        user=user,
        status=OrderStatus.PENDING,
        payment_method=payment_method,
        first_name=shipping_data['first_name'],
        last_name=shipping_data['last_name'],
        email=shipping_data['email'],
        phone=shipping_data.get('phone', ''),
        address_line_1=shipping_data['address_line_1'],
        address_line_2=shipping_data.get('address_line_2', ''),
        city=shipping_data['city'],
        state=shipping_data.get('state', ''),
        postal_code=shipping_data['postal_code'],
        country=shipping_data.get('country', 'Espana'),
    )

    # Agregar items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price_at_purchase=item['product'].price,
        )

    return order
```

### 2. Procesar Pago
```python
from shop.models import Transaction, PaymentStatus, PaymentProvider

def process_payment(order, payment_data):
    """Procesa el pago de una orden."""
    # Crear transaccion
    transaction = Transaction.objects.create(
        order=order,
        amount=order.total,
        provider=PaymentProvider.STRIPE,
    )

    try:
        # Llamar al proveedor (Stripe)
        result = stripe_charge(
            amount=int(order.total * 100),  # Centavos
            currency='eur',
            source=payment_data['token'],
        )

        transaction.provider_id = result['id']
        transaction.provider_response = result
        transaction.status = PaymentStatus.COMPLETED
        transaction.save()

        # Actualizar orden
        order.payment_status = PaymentStatus.COMPLETED
        order.status = OrderStatus.CONFIRMED
        order.save()

        return True, transaction

    except Exception as e:
        transaction.status = PaymentStatus.FAILED
        transaction.provider_response = {'error': str(e)}
        transaction.save()

        return False, transaction
```

### 3. Confirmar Orden
```python
def confirm_order(order):
    """Confirma una orden despues de pago exitoso."""
    order.status = OrderStatus.CONFIRMED
    order.save()

    # Enviar email de confirmacion
    send_order_confirmation_email(order)

    # Agregar productos al inventario del usuario (si aplica)
    for item in order.items.all():
        add_to_user_inventory(order.user, item.product)
```

---

## Patrones de Uso

### Obtener ordenes de usuario
```python
# Todas las ordenes
orders = user.orders.all()

# Ordenes completadas
completed = user.orders.filter(status=OrderStatus.DELIVERED)

# Con items precargados
orders = user.orders.prefetch_related('items__product').all()
```

### Calcular estadisticas
```python
from django.db.models import Sum, Count

def get_user_stats(user):
    """Estadisticas de compras del usuario."""
    return user.orders.filter(
        status=OrderStatus.DELIVERED
    ).aggregate(
        total_spent=Sum('total'),
        order_count=Count('id'),
    )
```

### Actualizar estado de orden
```python
def update_order_status(order, new_status):
    """Actualiza estado de orden con validacion."""
    valid_transitions = {
        OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
        OrderStatus.CONFIRMED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
        OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
        OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [OrderStatus.REFUNDED],
    }

    if new_status not in valid_transitions.get(order.status, []):
        raise ValueError(f"Transicion invalida: {order.status} -> {new_status}")

    order.status = new_status
    order.save()
```

---

## Admin Django

```python
from django.contrib import admin
from shop.models import Order, OrderItem, Transaction

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    readonly_fields = ('provider_response',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_status', 'total', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method')
    search_fields = ('id', 'user__username', 'email')
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline, TransactionInline]

    fieldsets = (
        ('Orden', {
            'fields': ('id', 'user', 'status', 'total')
        }),
        ('Pago', {
            'fields': ('payment_method', 'payment_status')
        }),
        ('Cliente', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Envio', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
```

---

## Testing

```python
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from shop.models import Product, Order, OrderItem, OrderStatus

@pytest.mark.django_db
class TestOrder:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='test')

    @pytest.fixture
    def product(self):
        return Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=Decimal('29.99')
        )

    def test_order_id_generation(self, user):
        """Test generacion de ID unico."""
        order = Order.objects.create(
            user=user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address_line_1='123 Test St',
            city='Madrid',
            postal_code='28001',
        )
        assert order.id.startswith('ORD-')
        assert len(order.id) == 17  # ORD-YYMMDD-XXXXXX

    def test_total_calculation(self, user, product):
        """Test calculo de total."""
        order = Order.objects.create(
            user=user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address_line_1='123 Test St',
            city='Madrid',
            postal_code='28001',
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
            price_at_purchase=product.price,
        )

        order.refresh_from_db()
        assert order.total == Decimal('59.98')

    def test_item_count(self, user, product):
        """Test conteo de items."""
        order = Order.objects.create(
            user=user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address_line_1='123 Test St',
            city='Madrid',
            postal_code='28001',
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=3,
            price_at_purchase=product.price,
        )

        assert order.item_count == 3
```

---

## Ver Tambien

- [Product](./product.md) - Modelo de productos
- [accounts.UserInventory](../accounts/userinventory.md) - Inventario post-compra
- [accounts.WalletTransaction](../accounts/wallettransaction.md) - Pagos con Solana
