# Croody Web - Guía Completa del Proyecto

Guía técnica exhaustiva para implementación en el ecosistema Croody Web.

---

## 1. Descripción del Proyecto

**Croody Web** es el ecosistema multi-producto que incluye:
- **croody.app** - Landing page principal con showcase de productos
- **Tienda Online** - E-commerce con carrito y checkout
- **Telemetría API** - Microservicio FastAPI para analytics
- **IDS API** - Sistema de detección de intrusos
- **Panel de Control** - Django admin personalizado

### Stack Principal

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Django | 5.1+ | Framework principal |
| FastAPI | 0.115+ | Microservicios API |
| PostgreSQL | 15+ | Base de datos |
| Nginx | alpine | Gateway/Proxy |
| Docker | compose v2 | Contenedores |
| HTMX | 2.x | Interactividad sin JS pesado |
| CSS Tokens | custom | Sistema de diseño Sacred Geometry |

---

## 2. Estructura del Proyecto

```
Web/
├── proyecto_integrado/
│   ├── Croody/                    # Django App Principal
│   │   ├── croody/               # Settings & Config
│   │   │   ├── settings.py       # Config principal
│   │   │   ├── settings/         # Settings modulares
│   │   │   └── urls.py           # URL router
│   │   ├── landing/              # Landing page views
│   │   ├── shop/                 # E-commerce (Modelos, Views)
│   │   │   ├── models/           # Product, Cart, Order
│   │   │   ├── views/            # CBV para shop
│   │   │   ├── services/         # Lógica de negocio
│   │   │   └── admin.py          # Admin customizado
│   │   ├── static/css/           # Design Tokens CSS
│   │   │   ├── tokens.css        # Variables Sacred Geometry
│   │   │   ├── base.css          # Estilos base
│   │   │   └── components.css    # Componentes
│   │   └── templates/            # Django templates
│   │       ├── base.html         # Layout principal
│   │       ├── shop/             # Templates de tienda
│   │       └── partials/         # Componentes HTMX
│   │
│   ├── telemetry_api/            # FastAPI Microservicio
│   │   ├── api/                  # Endpoints
│   │   │   ├── events.py         # Event tracking
│   │   │   └── health.py         # Health checks
│   │   ├── core/                 # Config y utils
│   │   └── main.py               # Entry point
│   │
│   ├── ids_api/                  # Sistema de Detección
│   │   └── api/                  # Endpoints IDS
│   │
│   └── gateway/                  # Nginx Configuration
│       ├── nginx.conf            # Dev config
│       └── nginx.prod.conf       # Production config
│
├── docs/                         # Documentación Viva
│   ├── 01-ARQUITECTURA/
│   ├── 02-BACKEND/
│   ├── 03-FRONTEND/
│   ├── 04-DEVOPS/
│   ├── 05-INFRAESTRUCTURA/
│   └── 06-SEGURIDAD/
│
├── scripts/
│   ├── security/                 # Hardening scripts
│   └── deployment/               # Deploy scripts
│
├── .claude/                      # Claude Code Config
│   ├── agents/                   # 8 agentes especializados
│   ├── commands/                 # 10 slash commands
│   ├── skills/                   # 7 skills
│   ├── hooks/                    # Hooks de automatización
│   └── prompts/                  # Prompt templates
│
├── docker-compose.yml            # Orquestación dev
├── docker-compose.prod.yml       # Orquestación prod
├── Makefile                      # Comandos comunes
└── CLAUDE.md                     # Orchestrator config
```

---

## 3. Sistema de Diseño: Sacred Geometry

### Filosofía

El sistema visual de Croody está basado en el **Número Áureo (φ = 1.618033988749)** aplicado a:
- Espaciado (Fibonacci: 8, 13, 21, 34, 55, 89px)
- Tipografía (escala modular)
- Proporciones de componentes
- Timing de animaciones (233ms)

### Paleta Gator (Verde Corporativo)

```css
--gator-950: #041009;   /* Darkest */
--gator-500: #3C9E5D;   /* Brand base */
--gator-50:  #F0FBF5;   /* Lightest */
```

### Paleta Jungle (Neutros)

```css
--jungle-950: #050807;  /* bg dark */
--jungle-500: #374640;  /* mid */
--jungle-50:  #EEF1EF;  /* bg light */
```

### Variables Dinámicas (Tema Dark)

```css
:root {
  --bg: var(--jungle-950);
  --surface-1: var(--jungle-900);
  --surface-2: var(--jungle-800);
  --fg: var(--jungle-50);
  --fg-muted: var(--jungle-200);
  --brand-base: var(--gator-500);
  --brand-strong: var(--gator-600);
}
```

### Spacing (Golden Ratio)

```css
--space-1: 8px;    /* Base */
--space-2: 13px;   /* 8 × φ */
--space-3: 21px;   /* 13 × φ */
--space-4: 34px;   /* 21 × φ */
--space-5: 55px;   /* 34 × φ */
--space-6: 89px;   /* 55 × φ */
```

### Expressivity Zones

| Zone | Uso | Permitido |
|------|-----|-----------|
| **HIGH** | Hero, featured, celebrations | Glows, animaciones complejas |
| **MEDIUM** | Cards, navigation | Hover effects, transforms |
| **LOW** | Forms, tables, admin | Solo border/color changes |

---

## 4. Patrones de Código Django

### Models (Fat Model Pattern)

```python
# shop/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    """Producto del catálogo."""

    name = models.CharField(_('Nombre'), max_length=200)
    slug = models.SlugField(unique=True, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(_('Descripción'), blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Producto')
        verbose_name_plural = _('Productos')
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
        ]

    def __str__(self):
        return self.name

    # Fat model: lógica de negocio aquí
    def get_display_price(self) -> str:
        """Retorna precio formateado."""
        return f"${self.price:,.2f}"

    def is_available(self) -> bool:
        """Verifica disponibilidad."""
        return self.is_active and self.stock > 0

    @classmethod
    def get_featured(cls, limit: int = 6):
        """Obtiene productos destacados."""
        return cls.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category')[:limit]
```

### Views (Class-Based)

```python
# shop/views.py
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product

class ProductListView(ListView):
    """Lista de productos con paginación."""

    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """Optimiza query con select_related."""
        return Product.objects.filter(
            is_active=True
        ).select_related('category').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured'] = Product.get_featured()
        return context


class ProductDetailView(DetailView):
    """Detalle de producto."""

    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)
```

### Services (Lógica Compleja)

```python
# shop/services/cart_service.py
"""
Servicio de carrito de compras.
Lógica compleja que no pertenece al modelo.
"""
from decimal import Decimal
from typing import Optional
from django.db import transaction
from ..models import Cart, CartItem, Product

class CartService:
    """Servicio de carrito."""

    def __init__(self, cart: Cart):
        self.cart = cart

    @transaction.atomic
    def add_item(self, product: Product, quantity: int = 1) -> CartItem:
        """Añade producto al carrito."""
        item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return item

    def get_total(self) -> Decimal:
        """Calcula total del carrito."""
        return sum(
            item.product.price * item.quantity
            for item in self.cart.items.select_related('product')
        )

    def apply_discount(self, code: str) -> Optional[Decimal]:
        """Aplica código de descuento."""
        # Implementar lógica de descuentos
        pass
```

---

## 5. Patrones FastAPI

### Endpoints

```python
# telemetry_api/api/events.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/events", tags=["events"])

class EventCreate(BaseModel):
    """Schema de creación de evento."""
    event_type: str = Field(..., min_length=1, max_length=100)
    payload: dict = Field(default_factory=dict)
    timestamp: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "page_view",
                "payload": {"page": "/shop", "user_agent": "Mozilla/5.0"}
            }
        }

class EventResponse(BaseModel):
    """Schema de respuesta."""
    id: str
    event_type: str
    created_at: datetime

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EventResponse)
async def create_event(event: EventCreate):
    """
    Registra un evento de telemetría.

    - **event_type**: Tipo de evento (page_view, click, etc.)
    - **payload**: Datos adicionales del evento
    """
    # Procesar evento
    result = await event_service.create(event)
    return result

@router.get("/stats")
async def get_stats(
    event_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """Obtiene estadísticas de eventos."""
    return await event_service.get_stats(event_type, start_date, end_date)
```

### Dependency Injection

```python
# telemetry_api/core/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer(auto_error=False)

async def get_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """Valida API key."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )
    return credentials.credentials

async def get_current_service(api_key: str = Depends(get_api_key)) -> str:
    """Identifica servicio por API key."""
    # Validar key contra base de datos
    service = await validate_api_key(api_key)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    return service
```

---

## 6. Templates y HTMX

### Layout Base

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Croody{% endblock %}</title>

    <link rel="stylesheet" href="{% static 'css/tokens.css' %}">
    <link rel="stylesheet" href="{% static 'css/base.css' %}">
    <link rel="stylesheet" href="{% static 'css/components.css' %}">

    <script src="https://unpkg.com/htmx.org@2.0.0"></script>
</head>
<body>
    <div id="app">
        {% include "partials/navbar.html" %}

        <main class="main-content">
            {% block content %}{% endblock %}
        </main>

        {% include "partials/footer.html" %}
    </div>

    <!-- Modal container para HTMX -->
    <div id="modal-container" class="modal-container"></div>

    {% block scripts %}{% endblock %}
</body>
</html>
```

### Componente HTMX

```html
<!-- templates/shop/partials/product_card.html -->
<article class="vector-card fade-in-up"
         hx-get="{% url 'shop:product-quick-view' product.slug %}"
         hx-trigger="click"
         hx-target="#modal-container"
         hx-swap="innerHTML">

    <div class="vector-card-media">
        {% if product.image %}
        <img src="{{ product.image.url }}"
             alt="{{ product.name }}"
             loading="lazy">
        {% endif %}

        {% if product.is_featured %}
        <span class="badge badge-featured">Destacado</span>
        {% endif %}
    </div>

    <div class="vector-card-content">
        <h3 class="vector-card-title">{{ product.name }}</h3>
        <p class="vector-card-description">
            {{ product.description|truncatewords:20 }}
        </p>
    </div>

    <footer class="vector-card-footer">
        <span class="price">{{ product.get_display_price }}</span>
        <button class="btn btn-primary btn-sm"
                hx-post="{% url 'shop:add-to-cart' product.id %}"
                hx-swap="none"
                hx-trigger="click consume"
                hx-indicator=".cart-indicator">
            Añadir
        </button>
    </footer>
</article>
```

### CSS del Componente

```css
/* static/css/components.css */

.vector-card {
    background: var(--surface-1);
    border-radius: var(--radius-3);
    padding: var(--space-3);
    transition: transform var(--duration-base) var(--ease-base),
                box-shadow var(--duration-base) var(--ease-base);
}

.vector-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
}

.vector-card-media {
    position: relative;
    border-radius: var(--radius-2);
    overflow: hidden;
    margin-bottom: var(--space-2);
}

.vector-card-media img {
    width: 100%;
    aspect-ratio: 4/3;
    object-fit: cover;
}

.vector-card-title {
    font-size: var(--text-lg);
    font-weight: 600;
    color: var(--fg);
    margin-bottom: var(--space-1);
}

.vector-card-description {
    font-size: var(--text-sm);
    color: var(--fg-muted);
    line-height: 1.5;
}

.vector-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: var(--space-3);
    padding-top: var(--space-2);
    border-top: 1px solid var(--surface-2);
}

.price {
    font-size: var(--text-xl);
    font-weight: 700;
    color: var(--brand-base);
}
```

---

## 7. Docker y DevOps

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build:
      context: ./proyecto_integrado/Croody
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./proyecto_integrado/Croody:/app
    environment:
      - DEBUG=True
      - DATABASE_URL=postgres://croody:croody@db:5432/croody_db
    depends_on:
      - db

  telemetry:
    build:
      context: ./proyecto_integrado/telemetry_api
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgres://croody:croody@db:5432/croody_db

  gateway:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./proyecto_integrado/gateway/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
      - telemetry

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=croody_db
      - POSTGRES_USER=croody
      - POSTGRES_PASSWORD=croody

volumes:
  postgres_data:
```

### Comandos Útiles

```bash
# Desarrollo
docker compose up -d
docker compose logs -f web
docker compose exec web python manage.py shell

# Migrations
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Tests
docker compose exec web pytest -v --cov=.

# Producción
docker compose -f docker-compose.prod.yml up -d
```

---

## 8. Testing

### pytest Django

```python
# tests/test_shop_views.py
import pytest
from django.test import Client
from django.urls import reverse
from shop.models import Product

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def product(db):
    return Product.objects.create(
        name="Test Product",
        slug="test-product",
        price=99.99,
        is_active=True
    )

@pytest.mark.django_db
class TestProductViews:
    """Tests de vistas de productos."""

    def test_product_list_returns_200(self, client):
        """Lista de productos debe retornar 200."""
        url = reverse('shop:product-list')
        response = client.get(url)
        assert response.status_code == 200

    def test_product_list_shows_active_products(self, client, product):
        """Debe mostrar productos activos."""
        url = reverse('shop:product-list')
        response = client.get(url)
        assert product.name in response.content.decode()

    def test_product_detail_returns_200(self, client, product):
        """Detalle de producto debe retornar 200."""
        url = reverse('shop:product-detail', kwargs={'slug': product.slug})
        response = client.get(url)
        assert response.status_code == 200
```

### pytest FastAPI

```python
# telemetry_api/tests/test_events.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_event():
    """Test creación de evento."""
    response = client.post(
        "/events/",
        json={
            "event_type": "page_view",
            "payload": {"page": "/home"}
        }
    )
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_stats():
    """Test obtención de estadísticas."""
    response = client.get("/events/stats")
    assert response.status_code == 200
```

---

## 9. Seguridad

### Django Settings

```python
# croody/settings/production.py
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### Nginx Headers

```nginx
# gateway/nginx.prod.conf
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options SAMEORIGIN;
add_header X-Content-Type-Options nosniff;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline';";
add_header Referrer-Policy no-referrer-when-downgrade;
```

---

## 10. Archivos Críticos

| Archivo | Propósito | Notas |
|---------|-----------|-------|
| `static/css/tokens.css` | Sistema de diseño | Source of truth para UI |
| `croody/settings.py` | Config Django | @security-critical |
| `gateway/nginx.conf` | Reverse proxy | Rate limiting |
| `docker-compose.yml` | Orquestación | Multi-service |
| `Makefile` | Comandos | Usa sudo |
| `.env` | Secrets | NUNCA commitear |

---

## 11. Comandos Claude Code

| Comando | Propósito |
|---------|-----------|
| `/clarify [idea]` | Clarificar requisitos |
| `/test-generate [file]` | Generar tests |
| `/security-audit` | Auditoría OWASP |
| `/deploy-check` | Estado de deploy |
| `/visual-validate` | Validar UI tokens |
| `/qa [scope]` | Quality review |
| `/accessibility-audit` | Auditoría WCAG |
| `/compliance-check` | GDPR/PCI-DSS |
| `/optimize-prompt` | Optimizar prompts |

---

## 12. Skills Disponibles

| Skill | Trigger | Propósito |
|-------|---------|-----------|
| `sacred-geometry-design` | UI work | Tokens y diseño |
| `django-patterns` | Backend | Fat models, CBV |
| `security-hardening` | Security | OWASP, headers |
| `prompt-engineering-patterns` | AI | Prompts LLM |
| `project-guide` | General | Esta guía |
| `api-design` | FastAPI | REST patterns |
| `devops-automation` | Deploy | Docker, nginx |

---

**Última actualización:** Diciembre 2024
