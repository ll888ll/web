# Vistas Shop - Documentación Completa

## Resumen
Las vistas de la aplicación Shop manejan el catálogo de productos, detalle de producto, búsqueda, filtros y API del carrito. Implementan paginación, filtros avanzados y optimización de consultas.

## Ubicación
`/proyecto_integrado/Croody/shop/views.py`

## Vistas Principales

### 1. ProductListView - Catálogo de Productos

**Herencia:**
```python
class ProductListView(NavContextMixin, ListView):
    model = Product
    template_name = 'shop/catalogue.html'
    context_object_name = 'products'
    paginate_by = 12  # 12 productos por página
```

**URL:** `/tienda/`

**Funcionalidades:**
- Listado de productos con paginación
- Búsqueda por texto (q)
- Filtros por tipo (cofre, set, accesorio)
- Filtros por rango de precio (min_price, max_price)
- Ordenamiento (price_asc, price_desc, recent)
- Facetas heurísticas

### Configuración de Filtros

```python
def get_queryset(self):
    """Filtra productos según parámetros GET."""
    # QuerySet base
    queryset = Product.objects.published()

    # Parámetros de búsqueda
    query = self.request.GET.get('q', '')
    product_type = self.request.GET.get('type', '')
    min_price = self.request.GET.get('min_price')
    max_price = self.request.GET.get('max_price')
    order = self.request.GET.get('order', '')

    # Aplicar búsqueda
    if query:
        queryset = queryset.search(query)

    # Filtrar por tipo
    if product_type:
        queryset = queryset.filter(badge_label=product_type)

    # Filtrar por precio
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    # Ordenamiento
    if order == 'price_asc':
        queryset = queryset.order_by('price')
    elif order == 'price_desc':
        queryset = queryset.order_by('-price')
    elif order == 'recent':
        queryset = queryset.order_by('-created_at')

    return queryset
```

### Context Data

```python
def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    """Inyecta datos adicionales en contexto."""
    context = super().get_context_data(**kwargs)

    # Datos de la página
    context.update(
        hero=self.get_hero_data(),
        metrics=self.get_metrics(),
        filters=self.get_filter_options(),
        current_filters=self.get_current_filters(),
        search_query=self.request.GET.get('q', ''),
        brand='gator',
    )

    return context

def get_hero_data(self) -> dict[str, str]:
    """Retorna datos del hero section."""
    return {
        'title': 'Tienda Croody',
        'subtitle': 'Productos del ecosistema de bienestar y tecnología',
        'description': 'Descubre cofres, sets y accesorios premium.'
    }

def get_metrics(self) -> dict[str, str]:
    """Retorna métricas de la tienda."""
    return {
        'total_products': Product.objects.published().count(),
        'types': ['cofre', 'set', 'accesorio'],
        'avg_price': self.get_average_price()
    }

def get_filter_options(self) -> dict[str, Any]:
    """Retorna opciones disponibles para filtros."""
    return {
        'types': [
            {'value': 'cofre', 'label': 'Cofres'},
            {'value': 'set', 'label': 'Sets'},
            {'value': 'accesorio', 'label': 'Accesorios'},
        ],
        'price_range': {
            'min': 0,
            'max': 999,
            'step': 10
        },
        'sort_options': [
            {'value': '', 'label': 'Orden por defecto'},
            {'value': 'price_asc', 'label': 'Precio: menor a mayor'},
            {'value': 'price_desc', 'label': 'Precio: mayor a menor'},
            {'value': 'recent', 'label': 'Más recientes'},
        ]
    }
```

### Paginación Personalizada

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    # Agregar información de paginación
    paginator = context['paginator']
    page_obj = context['page_obj']

    context.update({
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'page_range': paginator.get_elided_page_range(page_obj.number),
    })

    return context
```

### 2. ProductDetailView - Detalle de Producto

**Herencia:**
```python
class ProductDetailView(NavContextMixin, DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
```

**URL:** `/tienda/<slug:slug>/`

**Características:**
- Solo muestra productos publicados
- Productos relacionados
- Información completa del producto
- Purchase highlights
- Post-purchase steps

```python
def get_queryset(self):
    """Retorna solo productos publicados."""
    return Product.objects.published()

def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    """Agrega productos relacionados al contexto."""
    context = super().get_context_data(**kwargs)

    # Obtener productos relacionados (top 3)
    related_products = Product.objects.published().exclude(
        id=self.object.id
    ).order_by('sort_order', 'name')[:3]

    context.update(
        related_products=related_products,
        purchase_highlights=self.get_purchase_highlights(),
        post_purchase_steps=self.get_post_purchase_steps(),
    )

    return context

def get_purchase_highlights(self) -> list[dict[str, str]]:
    """Retorna puntos destacados de compra."""
    return [
        {
            'icon': '🚚',
            'title': 'Entrega rápida',
            'description': 'Recibe tu producto en 3 días'
        },
        {
            'icon': '🔒',
            'title': 'Pago seguro',
            'description': 'Transacciones protegidas'
        },
        {
            'icon': '↩️',
            'title': 'Garantía',
            'description': '30 días de garantía'
        }
    ]

def get_post_purchase_steps(self) -> list[str]:
    """Retorna pasos post-compra."""
    return [
        'Recibirás un email de confirmación',
        'Tu pedido será procesado en 24h',
        'Recibirás tracking por email',
        'Entrega en 3-5 días laborables'
    ]
```

### 3. StoreView - Vista General de Tienda

**Herencia:**
```python
class StoreView(NavContextMixin, TemplateView):
    template_name = 'shop/store.html'
```

**URL:** `/tienda/` (alternativa a ProductListView)

**Características:**
- Vista de bienvenida a la tienda
- Categorías de productos
- Productos destacados
- Promociones

## NavContextMixin

```python
class NavContextMixin:
    """Mixin para inyectar navegación específica de la tienda."""

    def get_nav_links(self) -> list[dict[str, str]]:
        """Retorna links de navegación de la tienda."""
        return [
            {
                'label': _('Tienda'),
                'url': reverse('shop:catalogue'),
                'fragment': None
            },
            {
                'label': _('Cofres'),
                'url': reverse('shop:catalogue') + '?type=cofre',
                'fragment': None
            },
            {
                'label': _('Sets'),
                'url': reverse('shop:catalogue') + '?type=set',
                'fragment': None
            },
            {
                'label': _('Accesorios'),
                'url': reverse('shop:catalogue') + '?type=accesorio',
                'fragment': None
            }
        ]

    def get_search_results(self) -> list[dict[str, str]]:
        """Retorna entradas para búsqueda global desde la tienda."""
        return [
            {
                'title': _('Buscar productos'),
                'url': reverse('shop:catalogue'),
                'description': _('Explora nuestro catálogo')
            }
        ]
```

## API Endpoints

### cart_add_api - Añadir al Carrito

**Ubicación:** `shop/views.py` (función, no clase)

**URL:** `/tienda/api/cart/add/`

**Método:** POST

**Características:**
- Endpoint para AJAX
- Recibe product_id
- Retorna JSON con resultado
- CSRF exempt (⚠️ **Pendiente de seguridad**)

```python
@csrf_exempt
@require_http_methods(['POST'])
def cart_add_api(request):
    """
    API para añadir producto al carrito.

    Request Body (JSON):
    {
        "product_id": 1,
        "quantity": 1
    }

    Response (JSON):
    {
        "success": true,
        "message": "Producto añadido al carrito",
        "cart_total": 2
    }
    """
    try:
        # Parsear JSON
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        # Validar product_id
        if not product_id:
            return JsonResponse({
                'success': False,
                'error': 'product_id es requerido'
            }, status=400)

        # Obtener producto
        try:
            product = Product.objects.get(id=product_id, is_published=True)
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Producto no encontrado'
            }, status=404)

        # ⚠️ TODO: Implementar lógica de carrito
        # Por ahora, solo retornamos éxito
        return JsonResponse({
            'success': True,
            'message': f'Producto "{product.name}" añadido al carrito',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
            },
            'cart_total': quantity  # Placeholder
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)

    except Exception as e:
        logger.exception(f"Error in cart_add_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor'
        }, status=500)
```

**⚠️ Consideraciones de Seguridad:**
- `@csrf_exempt` debería usar CSRF token en producción
- Falta validación de quantity
- Falta rate limiting
- Falta autenticación de usuario

### Mejora Propuesta

```python
@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def cart_add_api_improved(request):
    """Versión mejorada con seguridad."""
    # Validar CSRF
    if not csrf.csrf_token_valid(request):
        return JsonResponse({
            'success': False,
            'error': 'CSRF token inválido'
        }, status=403)

    # Rate limiting
    ip = request.META.get('REMOTE_ADDR')
    if is_rate_limited(ip, limit=100, window=60):
        return JsonResponse({
            'success': False,
            'error': 'Rate limit exceeded'
        }, status=429)

    # Parsear y validar
    serializer = CartAddSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse({
            'success': False,
            'errors': serializer.errors
        }, status=400)

    # Procesar
    product = serializer.validated_data['product']
    quantity = serializer.validated_data['quantity']

    # Lógica de carrito
    cart = get_or_create_cart(request.user)
    cart_item = cart.add_product(product, quantity)

    return JsonResponse({
        'success': True,
        'message': 'Producto añadido al carrito',
        'cart': {
            'total_items': cart.total_items,
            'total_price': str(cart.total_price),
        }
    })
```

## CheckoutPreviewView - Vista Previa de Compra

**Herencia:**
```python
class CheckoutPreviewView(TemplateView):
    template_name = 'shop/checkout_preview.html'
```

**URL:** `/tienda/checkout-preview/`

**Características:**
- Vista previa de 4 pasos
- Datos → Revisión → Pago → Confirmación
- Trust signals

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    # Obtener carrito (placeholder)
    cart_items = []  # TODO: implementar carrito real
    total = sum(item['price'] * item['quantity'] for item in cart_items)

    context.update({
        'steps': self.get_checkout_steps(),
        'trust_signals': self.get_trust_signals(),
        'cart_items': cart_items,
        'total': total,
    })

    return context

def get_checkout_steps(self):
    return [
        {'id': 1, 'name': 'Datos', 'status': 'current'},
        {'id': 2, 'name': 'Revisión', 'status': 'pending'},
        {'id': 3, 'name': 'Pago', 'status': 'pending'},
        {'id': 4, 'name': 'Confirmación', 'status': 'pending'},
    ]

def get_trust_signals(self):
    return [
        {
            'icon': '🔒',
            'text': 'Pago 100% seguro con encriptación SSL'
        },
        {
            'icon': '🚚',
            'text': 'Entrega gratuita en pedidos +50€'
        },
        {
            'icon': '↩️',
            'text': '30 días para devoluciones'
        }
    ]
```

## Configuración de URLs

### shop/urls.py
```python
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Catálogo
    path('', views.ProductListView.as_view(), name='catalogue'),

    # Detalle
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),

    # API
    path('api/cart/add/', views.cart_add_api, name='cart-add-api'),

    # Checkout
    path('checkout-preview/', views.CheckoutPreviewView.as_view(), name='checkout-preview'),
]
```

## Templates

### ProductListView Template

```django
{# shop/catalogue.html #}
{% extends 'base.html' %}

{% block title %}
  {% trans 'Tienda Croody' %} - {{ search_query|default:"" }}
{% endblock %}

{% block body %}
<div class="shop-page">
  {# Hero #}
  <section class="shop-hero">
    <h1>{{ hero.title }}</h1>
    <p>{{ hero.subtitle }}</p>
  </section>

  <div class="shop-content">
    {# Filtros #}
    <aside class="filters">
      <form method="get" class="filter-form">
        {# Búsqueda #}
        <div class="filter-group">
          <label for="search">{% trans 'Buscar' %}</label>
          <input
            type="search"
            name="q"
            id="search"
            value="{{ search_query }}"
            placeholder="{% trans 'Buscar productos...' %}"
          >
        </div>

        {# Tipo #}
        <div class="filter-group">
          <label for="type">{% trans 'Tipo' %}</label>
          <select name="type" id="type">
            <option value="">{% trans 'Todos' %}</option>
            {% for type in filters.types %}
              <option value="{{ type.value }}" {% if current_filters.type == type.value %}selected{% endif %}>
                {{ type.label }}
              </option>
            {% endfor %}
          </select>
        </div>

        {# Precio #}
        <div class="filter-group">
          <label>{% trans 'Rango de precio' %}</label>
          <div class="price-range">
            <input
              type="number"
              name="min_price"
              placeholder="Min"
              value="{{ current_filters.min_price|default:'' }}"
            >
            <span>-</span>
            <input
              type="number"
              name="max_price"
              placeholder="Max"
              value="{{ current_filters.max_price|default:'' }}"
            >
          </div>
        </div>

        {# Orden #}
        <div class="filter-group">
          <label for="order">{% trans 'Ordenar por' %}</label>
          <select name="order" id="order">
            {% for option in filters.sort_options %}
              <option value="{{ option.value }}" {% if current_filters.order == option.value %}selected{% endif %}>
                {{ option.label }}
              </option>
            {% endfor %}
          </select>
        </div>

        <button type="submit" class="btn btn-primary">
          {% trans 'Aplicar filtros' %}
        </button>
      </form>
    </aside>

    {# Resultados #}
    <main class="product-grid">
      {# Contador de resultados #}
      <div class="results-info">
        {% blocktrans with count=products.paginator.count %}
          {{ count }} productos encontrados
        {% endblocktrans %}
      </div>

      {# Grid de productos #}
      <div class="product-grid-ultra">
        {% for product in products %}
          {% include 'shop/components/product-card.html' with product=product %}
        {% empty %}
          <p class="no-results">
            {% trans 'No se encontraron productos.' %}
          </p>
        {% endfor %}
      </div>

      {# Paginación #}
      {% if products.has_other_pages %}
        <nav class="pagination">
          {% if products.has_previous %}
            <a href="?page={{ products.previous_page_number }}" class="pagination-link">
              {% trans 'Anterior' %}
            </a>
          {% endif %}

          <span class="pagination-current">
            {% blocktrans with number=products.number total=products.paginator.num_pages %}
              Página {{ number }} de {{ total }}
            {% endblocktrans %}
          </span>

          {% if products.has_next %}
            <a href="?page={{ products.next_page_number }}" class="pagination-link">
              {% trans 'Siguiente' %}
            </a>
          {% endif %}
        </nav>
      {% endif %}
    </main>
  </div>
</div>
{% endblock %}
```

### ProductCard Component

```django
{# shop/components/product-card.html #}
<article class="product-card">
  <a href="{{ product.get_absolute_url }}" class="product-link">
    {# Imagen #}
    <div class="product-image">
      <img
        src="{{ product.image.url }}"
        alt="{{ product.name }}"
        loading="lazy"
      >
      {% if product.badge_label %}
        <span class="badge">{{ product.badge_label }}</span>
      {% endif %}
    </div>

    {# Info #}
    <div class="product-info">
      <h3 class="product-name">{{ product.name }}</h3>
      <p class="product-teaser">{{ product.teaser }}</p>

      <div class="product-meta">
        <span class="price">{{ product.get_formatted_price }}</span>
        <span class="delivery">{{ product.delivery_estimate }}</span>
      </div>
    </div>
  </a>

  {# Acciones #}
  <div class="product-actions">
    <button
      class="btn btn-primary add-to-cart"
      data-product-id="{{ product.id }}"
    >
      {% trans 'Añadir al carrito' %}
    </button>
  </div>
</article>

<script>
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', async (e) => {
      e.preventDefault();

      const productId = button.dataset.productId;

      try {
        const response = await fetch('/tienda/api/cart/add/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({
            product_id: productId,
            quantity: 1
          })
        });

        const data = await response.json();

        if (data.success) {
          // Mostrar notificación de éxito
          showNotification(data.message, 'success');
        } else {
          showNotification(data.error, 'error');
        }
      } catch (error) {
        console.error('Error:', error);
        showNotification('Error al añadir al carrito', 'error');
      }
    });
  });
});
</script>
```

## Testing

### Unit Tests
```python
# tests/unit/views/test_shop.py
from django.test import Client, RequestFactory
from django.contrib.auth.models import User
from shop.models import Product
from shop.views import ProductListView, ProductDetailView

class TestProductListView:
    def test_get_queryset_with_search(self):
        """Test búsqueda en ProductListView."""
        factory = RequestFactory()
        request = factory.get('/tienda/', {'q': 'cofre'})
        view = ProductListView()
        view.setup(request)

        # Crear productos de prueba
        product1 = Product.objects.create(
            name='Cofre Premium',
            slug='cofre-premium',
            price=29.99
        )
        product2 = Product.objects.create(
            name='Set Básico',
            slug='set-basico',
            price=19.99
        )

        queryset = view.get_queryset()

        # Aplicar búsqueda
        view.request = request
        filtered_queryset = view.get_queryset()

        assert product1 in filtered_queryset
        assert product2 not in filtered_queryset

    def test_get_queryset_with_filters(self):
        """Test filtros en ProductListView."""
        factory = RequestFactory()
        request = factory.get('/tienda/', {
            'min_price': '10',
            'max_price': '30',
            'type': 'cofre'
        })
        view = ProductListView()
        view.setup(request)

        # Crear productos
        cheap = Product.objects.create(
            name='Producto Barato',
            slug='producto-barato',
            price=5.99
        )
        expensive = Product.objects.create(
            name='Producto Caro',
            slug='producto-caro',
            price=50.00
        )

        filtered_queryset = view.get_queryset()

        # Solo productos en rango de precio
        assert cheap in filtered_queryset
        assert expensive not in filtered_queryset

    def test_pagination(self, client):
        """Test paginación de productos."""
        # Crear 15 productos
        for i in range(15):
            Product.objects.create(
                name=f'Producto {i}',
                slug=f'producto-{i}',
                price=i * 10
            )

        response = client.get('/tienda/')

        assert response.status_code == 200
        assert len(response.context['products']) == 12  # paginate_by

        # Verificar segunda página
        response = client.get('/tienda/?page=2')
        assert response.status_code == 200
        assert len(response.context['products']) == 3
```

### API Tests
```python
# tests/api/test_cart_api.py
import json
from django.test import Client
from django.contrib.auth.models import User
from shop.models import Product

class TestCartAddAPI:
    def test_add_product_success(self):
        """Test añadir producto exitosamente."""
        client = Client()

        # Crear producto
        product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=29.99,
            is_published=True
        )

        # Hacer request
        response = client.post(
            '/tienda/api/cart/add/',
            json.dumps({'product_id': product.id}),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'Producto' in data['message']

    def test_add_product_not_found(self):
        """Test error cuando producto no existe."""
        client = Client()

        response = client.post(
            '/tienda/api/cart/add/',
            json.dumps({'product_id': 999}),
            content_type='application/json'
        )

        assert response.status_code == 404
        assert response.json()['success'] is False

    def test_add_product_missing_id(self):
        """Test error cuando falta product_id."""
        client = Client()

        response = client.post(
            '/tienda/api/cart/add/',
            json.dumps({}),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'product_id es requerido' in response.json()['error']
```

## Performance

### 1. Optimización de Consultas
```python
def get_queryset(self):
    # Solo campos necesarios
    return Product.objects.published().only(
        'name', 'slug', 'teaser', 'price', 'delivery_estimate', 'badge_label'
    ).select_related(None)  # No hay ForeignKeys por defecto
```

### 2. Cache de Filtros
```python
from django.core.cache import cache

def get_filter_options(self):
    cache_key = 'shop_filter_options'
    options = cache.get(cache_key)

    if not options:
        options = {
            'types': [...],
            'price_range': {...}
        }
        cache.set(cache_key, options, 300)  # 5 minutos

    return options
```

### 3. Paginación Eficiente
```python
# Usar Django paginator
from django.core.paginator import Paginator

# Query optimizado con only()
queryset = Product.objects.published().only(
    'id', 'name', 'slug', 'price'
)

paginator = Paginator(queryset, 12)
page_number = self.request.GET.get('page')
page_obj = paginator.get_page(page_number)

context['products'] = page_obj
```

## Seguridad

### 1. Validación de Parámetros
```python
def get_queryset(self):
    queryset = Product.objects.published()

    # Validar y sanear parámetros
    query = self.request.GET.get('q', '')
    if query and len(query) > 100:
        query = query[:100]  # Limitar longitud

    # Validar tipo
    product_type = self.request.GET.get('type', '')
    valid_types = ['cofre', 'set', 'accesorio']
    if product_type not in valid_types:
        product_type = ''

    # Aplicar filtros validados
    if query:
        queryset = queryset.search(query)

    if product_type:
        queryset = queryset.filter(badge_label=product_type)

    return queryset
```

### 2. Rate Limiting para API
```python
@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
def cart_add_api(request):
    # Implementar rate limiting
    pass

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour'
    }
}
```

## Referencias

### Archivos Relacionados
- `shop/models.py` - Product y ProductQuerySet
- `shop/admin.py` - ProductAdmin
- `shop/forms.py` - ProductForm (si existe)
- `shop/urls.py` - Configuración de rutas

### Documentación Externa
- [Django ListView](https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-display/#listview)
- [Django DetailView](https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-display/#detailview)
- [Django Paginator](https://docs.djangoproject.com/en/stable/topics/pagination/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## Ver También
- [Product Model](../modelos/product.md)
- [ProductAdmin](../../06-SEGURIDAD/admin.md#productadmin)
- [Cart API](./cart-api.md)
- [Search Implementation](./search-implementation.md)
