# Modelo UserInventory - Documentación Completa

## Resumen
El modelo `UserInventory` representa los items adquiridos por un usuario en el ecosistema Croody. Cada entrada vincula un usuario con un producto (personaje, cofre, accesorio) que ha comprado o recibido como regalo.

## Ubicación
`/proyecto_integrado/Croody/accounts/models.py`

## Estructura del Modelo

### Campos

| Campo | Tipo | Descripción | Por Defecto |
|-------|------|-------------|-------------|
| `user` | ForeignKey(User) | Usuario propietario | REQUIRED |
| `product` | ForeignKey(Product) | Producto adquirido | REQUIRED |
| `acquired_at` | DateTimeField | Fecha de adquisición | auto_now_add |
| `transaction_signature` | CharField(88) | Firma tx Solana | "" |
| `download_count` | PositiveIntegerField | Contador de descargas | 0 |
| `is_gift` | BooleanField | Si fue un regalo | False |
| `notes` | TextField | Notas adicionales | "" |

### Meta

```python
class Meta:
    verbose_name = 'Item de inventario'
    verbose_name_plural = 'Items de inventario'
    unique_together = ['user', 'product']  # Un usuario no puede tener duplicados
    ordering = ['-acquired_at']  # Más recientes primero
```

## Relaciones

### Con User
```python
# Acceso desde User
user.inventory_items.all()  # Todos los items del usuario
user.inventory_items.count()  # Cantidad de items

# Filtrar por producto
user.inventory_items.filter(product__slug='cofre-premium')
```

### Con Product
```python
# Acceso desde Product
product.inventory_entries.all()  # Todos los usuarios que tienen este producto
product.inventory_entries.count()  # Cantidad de ventas/posesiones
```

## Métodos

### increment_download()
Incrementa el contador de descargas del item.

```python
def increment_download(self) -> None:
    """Incrementa el contador de descargas."""
    self.download_count += 1
    self.save(update_fields=['download_count'])

# Uso
inventory_item.increment_download()
```

## Patrones de Uso

### Agregar item al inventario
```python
from accounts.models import UserInventory
from shop.models import Product

def add_to_inventory(user, product_slug, tx_signature=None, is_gift=False):
    """Agrega un producto al inventario del usuario."""
    product = Product.objects.get(slug=product_slug)

    inventory_item, created = UserInventory.objects.get_or_create(
        user=user,
        product=product,
        defaults={
            'transaction_signature': tx_signature or '',
            'is_gift': is_gift,
        }
    )

    if created:
        # Recalcular puntos del usuario (+50 por item)
        user.profile.refresh_stats()

    return inventory_item, created
```

### Verificar si usuario posee producto
```python
def user_owns_product(user, product):
    """Verifica si el usuario posee un producto."""
    return user.inventory_items.filter(product=product).exists()

# Uso
if user_owns_product(request.user, character):
    # Permitir usar el personaje
    pass
```

### Listar inventario del usuario
```python
def get_user_inventory(user):
    """Obtiene el inventario completo del usuario."""
    return user.inventory_items.select_related('product').all()

# Con categorización
def get_inventory_by_type(user):
    """Agrupa inventario por tipo de producto."""
    inventory = user.inventory_items.select_related('product').all()

    return {
        'characters': [i for i in inventory if 'buddy' in i.product.slug.lower()],
        'chests': [i for i in inventory if 'cofre' in i.product.slug.lower()],
        'accessories': [i for i in inventory if 'accesorio' in i.product.slug.lower()],
    }
```

### Transferir item (regalo)
```python
def gift_item(from_user, to_user, product):
    """Transfiere un item de un usuario a otro."""
    # Verificar que el usuario origen posee el item
    try:
        original_item = from_user.inventory_items.get(product=product)
    except UserInventory.DoesNotExist:
        raise ValueError("El usuario no posee este producto")

    # Verificar que el destinatario no lo tenga
    if to_user.inventory_items.filter(product=product).exists():
        raise ValueError("El destinatario ya posee este producto")

    # Crear nuevo item para destinatario
    new_item = UserInventory.objects.create(
        user=to_user,
        product=product,
        is_gift=True,
        notes=f"Regalo de {from_user.username}"
    )

    # Eliminar del inventario original
    original_item.delete()

    # Actualizar puntos de ambos usuarios
    from_user.profile.refresh_stats()
    to_user.profile.refresh_stats()

    return new_item
```

### Descargar asset del item
```python
from django.http import FileResponse, Http404

def download_item_asset(request, item_id):
    """Descarga el asset asociado a un item del inventario."""
    try:
        item = request.user.inventory_items.get(id=item_id)
    except UserInventory.DoesNotExist:
        raise Http404("Item no encontrado en tu inventario")

    # Incrementar contador
    item.increment_download()

    # Retornar archivo (asumiendo que el producto tiene un campo asset_file)
    if hasattr(item.product, 'asset_file') and item.product.asset_file:
        return FileResponse(
            item.product.asset_file.open(),
            as_attachment=True,
            filename=f"{item.product.slug}.zip"
        )

    raise Http404("Asset no disponible")
```

## Integración con Compras

### Después de compra exitosa
```python
from shop.models import Order, OrderItem
from accounts.models import UserInventory

def process_successful_order(order):
    """Procesa orden exitosa y agrega items al inventario."""
    for order_item in order.items.all():
        UserInventory.objects.get_or_create(
            user=order.user,
            product=order_item.product,
            defaults={
                'notes': f"Compra #{order.id}"
            }
        )

    # Actualizar puntos
    order.user.profile.refresh_stats()
```

### Después de pago Solana
```python
from accounts.models import UserInventory, WalletTransaction

def process_solana_purchase(user, product, tx_signature):
    """Procesa compra con Solana."""
    # Verificar transacción
    transaction = WalletTransaction.objects.get(tx_signature=tx_signature)

    if transaction.status != 'verified':
        raise ValueError("Transacción no verificada")

    # Agregar al inventario
    inventory_item = UserInventory.objects.create(
        user=user,
        product=product,
        transaction_signature=tx_signature
    )

    # Actualizar puntos
    user.profile.refresh_stats()

    return inventory_item
```

## Admin Django

```python
@admin.register(UserInventory)
class UserInventoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'acquired_at', 'download_count', 'is_gift')
    list_filter = ('is_gift', 'acquired_at')
    search_fields = ('user__username', 'product__name', 'transaction_signature')
    date_hierarchy = 'acquired_at'
    raw_id_fields = ('user', 'product')

    readonly_fields = ('acquired_at',)

    fieldsets = (
        ('Propietario', {
            'fields': ('user', 'product')
        }),
        ('Adquisición', {
            'fields': ('acquired_at', 'transaction_signature', 'is_gift')
        }),
        ('Uso', {
            'fields': ('download_count', 'notes')
        }),
    )
```

## Vistas

### Vista de inventario
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def inventory_view(request):
    """Vista del inventario del usuario."""
    inventory = request.user.inventory_items.select_related('product').all()

    # Estadísticas
    total_items = inventory.count()
    total_downloads = sum(item.download_count for item in inventory)
    gifts_received = inventory.filter(is_gift=True).count()

    context = {
        'inventory': inventory,
        'stats': {
            'total_items': total_items,
            'total_downloads': total_downloads,
            'gifts_received': gifts_received,
        }
    }

    return render(request, 'accounts/inventory.html', context)
```

## API Endpoints

### Serializer
```python
from rest_framework import serializers
from accounts.models import UserInventory

class UserInventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)

    class Meta:
        model = UserInventory
        fields = [
            'id', 'product', 'product_name', 'product_slug',
            'acquired_at', 'download_count', 'is_gift'
        ]
        read_only_fields = ['acquired_at', 'download_count']
```

### ViewSet
```python
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class UserInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserInventorySerializer

    def get_queryset(self):
        return self.request.user.inventory_items.select_related('product')

    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Registra descarga del item."""
        item = self.get_object()
        item.increment_download()
        return Response({'download_count': item.download_count})
```

## Testing

```python
import pytest
from django.contrib.auth.models import User
from accounts.models import UserInventory
from shop.models import Product

@pytest.mark.django_db
class TestUserInventory:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='test')

    @pytest.fixture
    def product(self):
        return Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=29.99
        )

    def test_create_inventory_item(self, user, product):
        """Test creación de item en inventario."""
        item = UserInventory.objects.create(user=user, product=product)

        assert item.user == user
        assert item.product == product
        assert item.download_count == 0
        assert not item.is_gift

    def test_unique_together(self, user, product):
        """Test que no se pueden duplicar items."""
        UserInventory.objects.create(user=user, product=product)

        with pytest.raises(Exception):  # IntegrityError
            UserInventory.objects.create(user=user, product=product)

    def test_increment_download(self, user, product):
        """Test incremento de descargas."""
        item = UserInventory.objects.create(user=user, product=product)

        assert item.download_count == 0

        item.increment_download()
        item.refresh_from_db()

        assert item.download_count == 1

    def test_ordering(self, user, product):
        """Test ordenamiento por fecha."""
        item1 = UserInventory.objects.create(user=user, product=product)

        product2 = Product.objects.create(name='P2', slug='p2', price=10)
        item2 = UserInventory.objects.create(user=user, product=product2)

        items = list(user.inventory_items.all())
        assert items[0] == item2  # Más reciente primero

    def test_points_contribution(self, user, product):
        """Test que items contribuyen a puntos."""
        initial_points = user.profile.calculate_points()

        UserInventory.objects.create(user=user, product=product)
        user.profile.refresh_stats()

        new_points = user.profile.points
        assert new_points == initial_points + 50  # +50 por item
```

## Queries Optimizadas

### Evitar N+1
```python
# Malo - N+1 queries
for item in user.inventory_items.all():
    print(item.product.name)  # Query por cada item

# Bueno - 1 query con join
for item in user.inventory_items.select_related('product').all():
    print(item.product.name)  # Sin queries adicionales
```

### Prefetch para múltiples usuarios
```python
from django.db.models import Prefetch

# Obtener usuarios con sus inventarios optimizados
users = User.objects.prefetch_related(
    Prefetch(
        'inventory_items',
        queryset=UserInventory.objects.select_related('product')
    )
).all()
```

## Referencias

### Archivos Relacionados
- `accounts/views.py` - Vistas de inventario
- `shop/models.py` - Modelo Product
- `templates/accounts/inventory.html` - Template

### Modelos Relacionados
- [UserProfile](./userprofile.md) - Puntos por items
- [Product](../modelos/product.md) - Productos
- [WalletTransaction](./wallettransaction.md) - Compras Solana

## Ver También
- [Sistema de Compras](../shop/checkout-flow.md)
- [Flujo de Pagos Solana](../../features/solana-payments.md)
