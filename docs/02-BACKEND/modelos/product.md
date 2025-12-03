# Modelo Product - Documentación Completa

## Resumen
El modelo `Product` representa los productos en la tienda Croody, incluyendo cofres, sets y accesorios del ecosistema Buddy/Luks. Implementa un QuerySet manager personalizado para encapsular lógica de negocio y optimización de consultas.

## Ubicación
`/proyecto_integrado/Croody/shop/models.py`

## ProductQuerySet - Manager Personalizado

### Funcionalidades Principales

#### 1. Método `published()`
Filtra únicamente productos publicados (is_published=True)

```python
class ProductQuerySet(models.QuerySet):
    def published(self) -> 'ProductQuerySet':
        """Retorna solo productos publicados."""
        return self.filter(is_published=True)
```

**Uso:**
```python
# Obtener solo productos activos
active_products = Product.objects.published()

# Encadenar con otros filtros
expensive_products = Product.objects.published().filter(price__gt=100)
```

#### 2. Método `search(query)`
Búsqueda full-text en name y teaser (case-insensitive)

```python
def search(self, query: str) -> 'ProductQuerySet':
    """Busca productos por nombre o teaser."""
    if not query:
        return self
    return self.filter(
        models.Q(name__icontains=query) |
        models.Q(teaser__icontains=query)
    )
```

**Uso:**
```python
# Búsqueda por nombre
results = Product.objects.search('cofre')

# Búsqueda por teaser
results = Product.objects.search('entrenamiento')

# Búsqueda combinada (name OR teaser)
results = Product.objects.search('premium luxury')
```

**Características:**
- Búsqueda parcial (icontains)
- Búsqueda en múltiples campos
- Retorna todos si query está vacío
- Case-insensitive

#### 3. Encadenamiento de Métodos
```python
# Componer múltiples filtros
products = Product.objects.published().search('cofre').order_by('-price')

# Crear QuerySet reusable
published_products = Product.objects.published()
filtered = published_products.search('set')
```

## Estructura del Modelo Product

### Campos

| Campo | Tipo | Descripción | Por Defecto |
|-------|------|-------------|-------------|
| `name` | CharField(120) | Nombre del producto | REQUIRED |
| `slug` | SlugField | URL amigable (único) | REQUIRED |
| `teaser` | CharField(240) | Descripción corta | "" |
| `description` | TextField | Descripción completa | "" |
| `price` | DecimalField(8,2) | Precio en euros | REQUIRED |
| `delivery_estimate` | CharField(100) | Estimación de entrega | "Entrega 3 días" |
| `badge_label` | CharField(32) | Etiqueta (new, sale, etc.) | "" |
| `is_published` | BooleanField | Producto visible en tienda | True |
| `sort_order` | PositiveIntegerField | Orden de exhibición | 0 |
| `created_at` | DateTimeField | Fecha de creación | auto_now_add |
| `updated_at` | DateTimeField | Fecha de actualización | auto_now |

### Tipo de Productos

**Tipos implícitos (detectables por badge_label o name):**
- **Cofres:** Productos tipo loot box (ej: "Cofre Premium")
- **Sets:** Colecciones temáticas (ej: "Set de Temporada")
- **Accesorios:** Productos individuales (ej: "Accesorio X")

## Patrones de Uso

### 1. Obtener Productos Publicados
```python
# Método recomendado
products = Product.objects.published()

# Filtrado adicional
active = Product.objects.published().filter(is_published=True)
```

### 2. Búsqueda con Filtros
```python
# Búsqueda simple
results = Product.objects.search('cofre')

# Búsqueda con filtros adicionales
results = Product.objects.search('premium').filter(price__gte=50)

# Búsqueda con ordenamiento
results = Product.objects.search('set').order_by('-created_at')
```

### 3. Búsqueda Avanzada con Q Objects
```python
from django.db.models import Q

# Búsqueda por múltiples criterios
products = Product.objects.filter(
    Q(name__icontains=query) |
    Q(teaser__icontains=query) |
    Q(description__icontains=query)
)
```

## get_absolute_url()

```python
def get_absolute_url(self) -> str:
    """Retorna URL canonical del producto."""
    return reverse('shop:detail', kwargs={'slug': self.slug})
```

**Uso en templates:**
```django
<a href="{{ product.get_absolute_url }}">
    {{ product.name }}
</a>
```

## Meta Configuration

```python
class Product(models.Model):
    # ... campos ...

    class Meta:
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['price']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_published']),
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
```

**Ordenamiento por defecto:**
1. `sort_order` (ascendente)
2. `name` (ascendente)

**Índices para optimización:**
- `slug`: Búsqueda por URL amigable
- `price`: Filtrado y ordenamiento por precio
- `-created_at`: Productos recientes
- `is_published`: Filtrado de productos activos

## Admin Django

### ProductAdmin Personalizado

```python
# shop/admin.py
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
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
```

**Características destacadas:**
- `list_display`: Columnas en listado
- `list_editable`: Edición inline
- `prepopulated_fields`: Auto-slug
- `search_fields`: Búsqueda full-text
- `list_filter`: Filtros laterales
- `readonly_fields`: Campos solo lectura

### Vista Previa de Imagen

```python
def image_preview(self, obj):
    """Muestra preview visual del producto en admin."""
    return format_html(
        '<div style="width:50px;height:50px;background:linear-gradient(135deg,#3C9E5D,#277947);'
        'border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;'
        'font-weight:bold;">{}</div>',
        obj.name[:2].upper()
    )

image_preview.short_description = 'Vista Previa'
```

## Serializers (Django REST Framework)

```python
# serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        """Personaliza serialización."""
        data = super().to_representation(instance)
        # Agregar URL absoluta
        data['url'] = instance.get_absolute_url()
        return data
```

## Optimización de Consultas

### 1. select_related
```python
# No necesario (Product no tiene ForeignKey a User por defecto)
# Solo usar si agregamos relaciones FK
```

### 2. prefetch_related (para M2M)
```python
# Si Product tiene relación M2M con Category
products = Product.objects.prefetch_related('categories').all()
```

### 3. Values y ValuesList
```python
# Solo obtener campos específicos
product_names = Product.objects.published().values_list('name', flat=True)

# Query más eficiente
product_data = Product.objects.published().values('id', 'name', 'price')
```

## Casos de Uso Comunes

### 1. Catálogo de Productos (Paginación)
```python
def get_product_catalog(request):
    """Obtiene productos paginados."""
    page = request.GET.get('page', 1)
    paginator = Paginator(Product.objects.published(), 12)

    return paginator.get_page(page)
```

### 2. Filtros de Búsqueda
```python
def filter_products(request):
    """Filtra productos por criterios."""
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.published()

    if query:
        products = products.search(query)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    return products
```

### 3. Ordenamiento por Precio
```python
# Precio ascendente
cheap = Product.objects.published().order_by('price')

# Precio descendente
expensive = Product.objects.published().order_by('-price')
```

### 4. Productos Recientes
```python
# Últimos productos creados
recent = Product.objects.published().order_by('-created_at')[:10]
```

## Migraciones

### Migración Inicial
```python
# 0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('teaser', models.CharField(blank=True, max_length=240)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('delivery_estimate', models.CharField(default='Entrega 3 días', max_length=100)),
                ('badge_label', models.CharField(blank=True, max_length=32)),
                ('is_published', models.BooleanField(default=True)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['sort_order', 'name'],
            },
        ),
    ]
```

### Migración de Datos (Seed)
```python
# 0002_seed_products.py
from django.db import migrations

def seed_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Product.objects.create(
        name="Cofre Premium",
        slug="cofre-premium",
        teaser="Cofre misterioso con productos exclusivos",
        description="Un cofre lleno de sorpresas...",
        price=29.99,
        badge_label="new",
        sort_order=1
    )

def reverse_seed(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Product.objects.filter(slug='cofre-premium').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_products, reverse_seed),
    ]
```

## Métodos Personalizados

### String Representation
```python
def __str__(self) -> str:
    return self.name
```

### Precio Formateado
```python
def get_formatted_price(self) -> str:
    """Retorna precio formateado para display."""
    return f"{self.price:.2f}€"

# En template:
{{ product.get_formatted_price }}
```

### Verificar Disponibilidad
```python
def is_available(self) -> bool:
    """Verifica si el producto está disponible."""
    return self.is_published

# Uso:
if product.is_available():
    # Mostrar botón de compra
    pass
```

## Validaciones

### Validación de Slug
```python
def clean_slug(self):
    slug = self.cleaned_data.get('slug')
    if slug:
        # Slug debe ser único
        if Product.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este slug ya existe.')
    return slug
```

### Validación de Precio
```python
def clean_price(self):
    price = self.cleaned_data.get('price')
    if price and price < 0:
        raise forms.ValidationError('El precio debe ser positivo.')
    return price
```

## Testing

### Unit Tests
```python
# tests/unit/models/test_product.py
import pytest

@pytest.mark.django_db
class TestProductQuerySet:
    def test_published(self, product_factory):
        published = product_factory(is_published=True)
        unpublished = product_factory(is_published=False)

        assert published in Product.objects.published()
        assert unpublished not in Product.objects.published()

    def test_search(self, product_factory):
        product = product_factory(name='Cofre Premium')

        results = Product.objects.search('Cofre')
        assert product in results

        results = Product.objects.search('Premium')
        assert product in results

    def test_search_empty_query(self, product_factory):
        product_factory(name='Product 1')
        product_factory(name='Product 2')

        results = Product.objects.search('')
        assert results.count() == 2
```

### Factory para Tests
```python
# factories.py
import factory
from shop.models import Product

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product {n}')
    slug = factory.Sequence(lambda n: f'product-{n}')
    teaser = 'A great product'
    description = 'Product description'
    price = 29.99
    is_published = True

@pytest.fixture
def product(db):
    return ProductFactory()
```

## Consideraciones de Performance

### 1. Indexación Correcta
```python
class Meta:
    indexes = [
        # Los índices ya están definidos arriba
        models.Index(fields=['slug', 'is_published']),
    ]
```

### 2. Evitar N+1 Queries
```python
# Bad
for product in products:
    print(product.name)

# Good (no necesario para Product, pero sí para relaciones)
for product in Product.objects.published().select_related(None):
    print(product.name)
```

### 3. Paginación
```python
from django.core.paginator import Paginator

def paginate_products(request):
    product_list = Product.objects.published()
    paginator = Paginator(product_list, 12)  # 12 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
```

### 4. Caching
```python
from django.core.cache import cache

def get_cached_products():
    cache_key = 'published_products'
    products = cache.get(cache_key)

    if not products:
        products = list(Product.objects.published())
        cache.set(cache_key, products, 300)  # 5 minutos

    return products
```

## Seguridad

### Validación de Entrada
```python
# En forms
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0 or price > 9999.99:
            raise forms.ValidationError('Precio inválido.')
        return price
```

### Sanitización
```python
# Los campos TextField y CharField de Django ya escapan HTML automáticamente
# No usar mark_safe a menos que sea absolutamente necesario
```

## Integración con Vistas

### En ProductListView
```python
# shop/views.py
class ProductListView(ListView):
    model = Product
    template_name = 'shop/catalogue.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.published()
```

### En ProductDetailView
```python
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.published()
```

## Referencias

### Archivos Relacionados
- `shop/views.py` - Vistas (ProductListView, ProductDetailView)
- `shop/admin.py` - Admin personalizado
- `shop/urls.py` - Rutas
- `shop/forms.py` - Formularios (ProductForm)

### Documentación Externa
- [Django QuerySet API](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- [Django Custom Managers](https://docs.djangoproject.com/en/stable/topics/db/managers/)
- [Django DecimalField](https://docs.djangoproject.com/en/stable/ref/models/fields/#decimalfield)

## Ver También
- [ProductListView](../vistas/shop-views.md#productlistview)
- [ProductDetailView](../vistas/shop-views.md#productdetailview)
- [ProductAdmin](../../06-SEGURIDAD/admin.md#productadmin)
- [ProductForm](../formularios.md#productform)
