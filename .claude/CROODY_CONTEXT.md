# Croody Web Ecosystem - Contexto Técnico

> **Este archivo es leído por los subagentes para entender el proyecto.**
> No contiene instrucciones de comportamiento, solo información de referencia.

---

## Descripción del Proyecto

**Croody** es el ecosistema web multi-producto que incluye:
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
| Tailwind CSS | 3.x (custom) | Estilos via tokens |
| HTMX | 2.x | Interactividad sin JS pesado |

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
│   │   ├── static/css/           # Design Tokens CSS
│   │   │   ├── tokens.css        # Sistema de variables (307 líneas)
│   │   │   ├── base.css          # Estilos base
│   │   │   └── components.css    # Componentes
│   │   └── templates/            # Django templates (Jinja2-like)
│   │
│   ├── telemetry_api/            # FastAPI Microservicio
│   │   ├── api/                  # Endpoints
│   │   └── core/                 # Config y utils
│   │
│   ├── ids_api/                  # Sistema de Detección
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
└── .claude/                      # Claude Code Config
    ├── agents/                   # Agentes especializados
    ├── commands/                 # Slash commands
    ├── prompts/                  # Prompt templates
    ├── skills/                   # Skills invocables
    └── CROODY_CONTEXT.md         # Este archivo
```

---

## 3. Sistema de Diseño: Geometría Sagrada

### Filosofía
El sistema visual de Croody está basado en el **Número Áureo (φ = 1.618033988749)** aplicado matemáticamente a:
- Espaciado (Fibonacci: 8, 13, 21, 34, 55, 89px)
- Tipografía (escala modular)
- Proporciones de componentes
- Timing de animaciones

### Paletas de Color

#### Gator (Verde Corporativo - Croody)
```css
--gator-950: #041009;  /* Darkest */
--gator-900: #082015;
--gator-800: #103924;
--gator-700: #1C5C37;
--gator-600: #277947;
--gator-500: #3C9E5D;  /* Base */
--gator-400: #5BB97D;
--gator-300: #80D3A0;
--gator-200: #B4E5C6;
--gator-100: #DDF6E8;
--gator-50:  #F0FBF5;  /* Lightest */
```

#### Jungle (Neutros)
```css
--jungle-950: #050807;  /* bg dark */
--jungle-900: #0B1311;
--jungle-800: #141F1B;
--jungle-700: #1E2C26;
--jungle-600: #293833;
--jungle-500: #374640;
--jungle-400: #56655F;
--jungle-300: #7A8883;
--jungle-200: #A9B4B0;
--jungle-100: #D3DAD7;
--jungle-50:  #EEF1EF;  /* bg light */
```

#### Sand (Dorado - Luks Brand)
```css
--sand-600: #C18F4A;
--sand-500: #E0B771;
--sand-400: #F3D398;
--sand-300: #F8E1B7;
--sand-200: #FBECD1;
--sand-100: #FDF5E6;
```

#### Crimson (Rojo - Buddy Brand)
```css
--crimson-deep: #7A1E2A;
--crimson-primary: #E04F56;
--crimson-soft: #FFA7B5;
```

### Variables Dinámicas (Tema)

```css
/* Dark Theme (default) */
:root, html[data-theme="dark"] {
  --bg: var(--jungle-950);
  --surface-1: var(--jungle-900);
  --surface-2: var(--jungle-800);
  --fg: var(--jungle-50);
  --fg-muted: var(--jungle-200);
  --brand-base: var(--gator-500);
  --brand-strong: var(--gator-600);
}

/* Light Theme */
html[data-theme="light"] {
  --bg: var(--gator-50);
  --surface-1: var(--gator-100);
  --fg: var(--jungle-900);
}
```

### Espaciado (Golden Ratio)

```css
--space-1: 8px;
--space-2: 13px;   /* 8 × φ */
--space-3: 21px;   /* 13 × φ */
--space-4: 34px;   /* 21 × φ */
--space-5: 55px;   /* 34 × φ */
--space-6: 89px;   /* 55 × φ */
```

### Tipografía

```css
--font-sans: "Josefin Sans", -apple-system, BlinkMacSystemFont, sans-serif;
--font-display: "Baloo 2", var(--font-sans);
--font-mono: ui-monospace, SFMono-Regular, monospace;

/* Escala (basada en φ) */
--text-xs: 0.78rem;   /* 12.5px */
--text-sm: 0.9rem;    /* 14.4px */
--text-base: 1rem;    /* 16px - Root */
--text-lg: 1.15rem;   /* 18.4px */
--text-xl: 1.33rem;   /* 21.3px */
--text-2xl: 1.6rem;   /* 25.6px */
--text-3xl: 2.1rem;   /* 33.6px */
--text-4xl: clamp(2.3rem, 2vw + 2rem, 3.6rem);
```

### Border Radius

```css
--radius-1: 6px;   /* Small */
--radius-2: 10px;  /* Medium */
--radius-3: 16px;  /* Large */
--radius-4: 24px;  /* Extra large */
--radius-full: 9999px;
```

### Sombras (Elevation)

```css
--shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-sm: 0 4px 12px rgba(20, 30, 20, 0.08);
--shadow-md: 0 10px 30px rgba(20, 50, 30, 0.12);
--shadow-lg: 0 25px 55px rgba(32, 80, 50, 0.20);
```

### Transiciones

```css
--duration-fast: 100ms;
--duration-base: 233ms;  /* Golden ratio based */
--duration-slow: 377ms;
--ease-base: cubic-bezier(0.4, 0, 0.2, 1);
```

---

## 4. Patrones de Código

### Django Views (Class-Based)

```python
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category')
```

### Django Models (Fat Models)

```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    """Producto del catálogo."""

    name = models.CharField(_('Name'), max_length=200)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    def get_display_price(self):
        """Retorna precio formateado."""
        return f"${self.price:,.2f}"
```

### FastAPI Endpoints

```python
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

class EventCreate(BaseModel):
    event_type: str
    payload: dict
    timestamp: Optional[str] = None

@router.post("/events", status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate):
    """Registra un evento de telemetría."""
    # Process event
    return {"status": "created", "event_type": event.event_type}
```

### Templates (Django + HTMX)

```html
{% extends "base.html" %}

{% block content %}
<section class="product-grid">
  {% for product in products %}
  <article class="vector-card fade-in-up"
           hx-get="{% url 'shop:product-detail' product.slug %}"
           hx-trigger="click"
           hx-target="#modal-container"
           hx-swap="innerHTML">
    <header class="vector-card-header">
      <span class="badge">{{ product.category.name }}</span>
    </header>
    <div class="vector-card-content">
      <h3 class="title">{{ product.name }}</h3>
      <span class="price">{{ product.get_display_price }}</span>
    </div>
  </article>
  {% endfor %}
</section>
{% endblock %}
```

---

## 5. Convenciones de Código

### Nombres de Archivos

| Tipo | Patrón | Ejemplo |
|------|--------|---------|
| Views | `views.py` o `views/*.py` | `views/shop_views.py` |
| Models | `models.py` o `models/*.py` | `models/product.py` |
| Templates | `snake_case.html` | `product_list.html` |
| Static CSS | `snake_case.css` | `tokens.css` |
| URLs | `urls.py` | Siempre `urls.py` |
| Tests | `test_*.py` | `test_views.py` |
| Services | `services.py` | `services/cart_service.py` |

### CSS Classes (BEM-like)

```css
/* Block */
.vector-card { }

/* Element */
.vector-card-header { }
.vector-card-content { }
.vector-card-footer { }

/* Modifier */
.vector-card--featured { }
.btn-primary { }
.btn-secondary { }
```

### Imports (Python) - Orden Obligatorio

```python
# 1. Standard library
import os
from pathlib import Path
from typing import Optional, List

# 2. Third-party
from django.db import models
from django.views.generic import ListView
from rest_framework import viewsets

# 3. Local
from .models import Product
from core.utils import generate_slug
```

---

## 6. Seguridad (Critical)

### Security Headers (nginx)

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self' 'unsafe-inline' data: https:; object-src 'none'; frame-ancestors 'self'";
add_header X-Frame-Options SAMEORIGIN;
add_header X-Content-Type-Options nosniff;
add_header Referrer-Policy no-referrer-when-downgrade;
```

### Django Security Settings

```python
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Rate Limiting

```nginx
limit_req_zone $binary_remote_addr zone=api_zone:20m rate=150r/s;
limit_req zone=api_zone burst=150 nodelay;
```

### Zonas de Peligro (Requieren Doble Confirmación)

1. **`Makefile`:** Ejecuta comandos con `sudo`
2. **`ops/cicf/`:** Modifica interfaces de red y servicios del sistema
3. **`infra/terraform/`:** Genera costos reales en AWS
4. **`scripts/security/`:** Hardening scripts que modifican firewall

---

## 7. Testing

### pytest (Django)

```python
import pytest
from django.test import Client
from django.urls import reverse

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_product_list_view(client):
    url = reverse('shop:product-list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'products' in response.context
```

### pytest (FastAPI)

```python
from fastapi.testclient import TestClient
from telemetry_api.main import app

client = TestClient(app)

def test_create_event():
    response = client.post("/telemetry/events", json={
        "event_type": "page_view",
        "payload": {"page": "/home"}
    })
    assert response.status_code == 201
    assert response.json()["status"] == "created"
```

### Comandos de Testing

```bash
# Django tests
python manage.py test

# pytest con coverage
pytest -v --cov=. --cov-report=html

# Test específico
pytest test/test_views.py::test_product_list -v
```

---

## 8. DevOps

### Docker Compose Services

| Service | Puerto | Propósito |
|---------|--------|-----------|
| `web` | 8000 | Django principal |
| `telemetry` | 8001 | FastAPI telemetry |
| `ids` | 8002 | FastAPI IDS |
| `gateway` | 80/443 | Nginx proxy |
| `db` | 5432 | PostgreSQL |

### Comandos Útiles

```bash
# Desarrollo
docker compose up -d
docker compose logs -f web

# Producción
docker compose -f docker-compose.prod.yml up -d

# Django management
docker compose exec web python manage.py shell
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput

# Database
docker compose exec db psql -U croody -d croody_db
```

---

## 9. Documentación Viva

### Estructura

```
docs/
├── 01-ARQUITECTURA/      # Overview, decisiones técnicas (ADRs)
├── 02-BACKEND/           # Django, FastAPI, modelos, APIs
├── 03-FRONTEND/          # Design system, componentes, tokens
├── 04-DEVOPS/            # Docker, CI/CD, deploy, Makefile
├── 05-INFRAESTRUCTURA/   # AWS, Terraform, DNS
└── 06-SEGURIDAD/         # Hardening, headers, firewall, SSL
```

### Principio Fundamental

> **La documentación se actualiza junto con el código.**
> No existe código sin documentación. No existe merge sin docs actualizados.

### Framework Diátaxis

- **Tutoriales:** Paso a paso para operadores
- **How-To:** Guías de resolución de problemas (Runbooks)
- **Referencia:** Especificaciones técnicas de API y Modelos
- **Explicación:** Arquitectura y decisiones de diseño (ADRs)

---

## 10. Archivos Críticos

| Archivo | Propósito | Notas |
|---------|-----------|-------|
| `static/css/tokens.css` | Sistema de diseño | 307 líneas, geometría sagrada |
| `croody/settings.py` | Config Django | Security settings críticos |
| `gateway/nginx.conf` | Gateway config | Rate limiting, headers |
| `gateway/nginx.prod.conf` | Prod config | SSL, HSTS, CSP |
| `scripts/security/hardening_auto.sh` | Hardening | UFW, ModSecurity, SSL |
| `docker-compose.yml` | Orquestación | Multi-service setup |
| `PLAN_DOCUMENTACION_COMPLETO.md` | Roadmap docs | La biblia de documentación |

---

## 11. Quality Gates

### Checklist Pre-Commit

- [ ] `python manage.py check --deploy` pasa
- [ ] `pytest` pasa (target: >80% coverage)
- [ ] `flake8` sin errores
- [ ] `black` aplicado
- [ ] Documentación actualizada si hay cambio de API/modelo
- [ ] Tokens CSS usados (no colores hardcodeados)
- [ ] Sin secrets en código

### Checklist Pre-Deploy

- [ ] Migrations probadas en staging
- [ ] `collectstatic` ejecutado
- [ ] SSL certificate válido (>30 días)
- [ ] Rate limiting configurado
- [ ] Security headers verificados
- [ ] Logs configurados

---

## 12. Vocabulario Croody

| Término | Significado |
|---------|-------------|
| **Gator** | Color verde corporativo (#3C9E5D) |
| **Sacred Geometry** | Sistema basado en φ (1.618) |
| **Token** | Variable CSS del design system |
| **Vector Card** | Componente card con hover effects |
| **Shimmer** | Efecto de brillo en botones hover |
| **Surface** | Nivel de elevación (surface-1, surface-2) |
| **Jungle** | Paleta de neutros grises-verdes |

---

## 13. Comandos Claude Code

| Comando | Propósito |
|---------|-----------|
| `/clarify [idea]` | Clarificar requisitos con The Interrogation |
| `/test-generate [file]` | Generar tests automatizados para Django/FastAPI |
| `/security-audit` | Auditoría de seguridad OWASP Top 10 |
| `/deploy-check` | Verificar estado de deployment |
| `/visual-validate [template]` | Validar UI contra tokens Sacred Geometry |
| `/qa [scope]` | Quality Assurance y review de código |

---

## 14. Herramientas MCP Disponibles

### firecrawl (Web Scraping)

```
firecrawl_scrape     # Scrape single URL
firecrawl_map        # Discover URLs on site
firecrawl_search     # Search web with scraping
firecrawl_crawl      # Crawl multiple pages
firecrawl_extract    # Extract structured data
```

### playwright (Browser Automation)

```
browser_navigate      # Go to URL
browser_snapshot      # Accessibility snapshot
browser_click         # Click element
browser_type          # Type text
browser_screenshot    # Capture screenshot
browser_evaluate      # Run JavaScript
```

### 21st-magic (UI Components)

```
21st_magic_component_builder      # Build new UI component
21st_magic_component_inspiration  # Get component inspiration
21st_magic_component_refiner      # Refine existing component
logo_search                       # Search for logos
```

---

## 15. Seguridad

### SecureStorageService

No aplicable directamente en web, pero para APIs:

```python
# Usar django-environ para secrets
import environ
env = environ.Env()

# Datos protegidos en .env:
- DJANGO_SECRET_KEY
- DATABASE_URL
- AWS_ACCESS_KEY_ID
- STRIPE_SECRET_KEY
```

### Reglas de Seguridad

1. **NUNCA** hardcodear secrets en código
2. **SIEMPRE** usar variables de entorno para credenciales
3. **NUNCA** loggear información sensible
4. **SIEMPRE** parametrizar queries SQL (ORM)
5. Archivos `.env` están en `.gitignore`

---

## 16. Arquitectura de Servicios

### Flujo de Request

```
Usuario → Nginx Gateway → Django/FastAPI → PostgreSQL
                ↓
           Rate Limiting
           Security Headers
           SSL Termination
```

### Comunicación Entre Servicios

| Servicio | Comunicación | Protocolo |
|----------|--------------|-----------|
| Django → Telemetry | HTTP interno | REST |
| Django → IDS | HTTP interno | REST |
| Gateway → All | Reverse Proxy | HTTP |
| All → PostgreSQL | TCP | psycopg2 |

---

## 17. Expressivity Zones

El sistema de diseño define 3 zonas de expresividad visual:

### HIGH Zone (Celebrations)
- Hero banners
- Success modals
- Featured products
- CTAs principales

**Permitido:**
- `box-shadow` con glow (color-mix con brand)
- Animaciones de entrada elaboradas
- Gradientes sutiles

### MEDIUM Zone (Interactive)
- Product cards (vector-card)
- Navigation items
- Botones secundarios

**Permitido:**
- `translateY(-4px)` en hover
- `box-shadow` escalado en hover
- Shimmer en botones

### LOW Zone (Functional)
- Forms de login/registro
- Settings
- Tablas de datos
- Admin panels

**Permitido:**
- Solo cambio de `border-color` en focus
- Transiciones de 100ms (`--duration-fast`)
- Sin transforms

---

## 18. Convenciones de Código

### Commits

```
feat: nueva funcionalidad
fix: corrección de bug
docs: documentación
refactor: reestructuración sin cambio funcional
test: tests
chore: mantenimiento
style: cambios de formato (CSS, lint)
perf: mejoras de performance
security: parches de seguridad
```

### Comentarios

```python
# @deprecated      - No usar; incluir alternativa
# @security-critical - Requiere revisión manual
# @context(ADR-XX) - Link a Architecture Decision Record
# TODO(username)   - Tarea pendiente con owner
# FIXME            - Bug conocido que necesita fix
```

### Estilo

- **Intención sobre implementación** en comentarios
- `const` en JavaScript siempre que sea posible
- Type hints en Python 3.11+
- Docstrings en español para funciones públicas
- Nombres descriptivos > comentarios

---

## 19. Archivos Críticos

| Archivo | Descripción | Cuidado |
|---------|-------------|---------|
| `static/css/tokens.css` | Sistema de diseño Sacred Geometry | Source of truth para UI |
| `croody/settings.py` | Configuración Django | @security-critical |
| `gateway/nginx.conf` | Reverse proxy config | Rate limiting aquí |
| `gateway/nginx.prod.conf` | Producción | SSL, HSTS, CSP |
| `docker-compose.yml` | Orquestación servicios | Multi-service |
| `docker-compose.prod.yml` | Producción | Resource limits |
| `Makefile` | Comandos comunes | Usa sudo |
| `.env` | Secrets | NUNCA commitear |

---

## 20. Skills Disponibles

### sacred-geometry-design

```
skill: "sacred-geometry-design"
```

Contiene:
- Reglas de φ (Golden Ratio)
- Expressivity zones (HIGH/MEDIUM/LOW)
- Paletas Gator y Jungle
- Anti-patterns de diseño

**Invocar para**: Todo trabajo de UI, verificación de diseño, accesibilidad.

### django-patterns

```
skill: "django-patterns"
```

Contiene:
- Fat Models, Thin Views
- QuerySet y Managers personalizados
- CBV patterns
- FastAPI integration
- Query optimization

**Invocar para**: Todo trabajo de backend, modelos, vistas, APIs.

### security-hardening

```
skill: "security-hardening"
```

Contiene:
- OWASP Top 10 2021 compliance
- Django security settings
- Nginx headers configuration
- Input validation patterns
- SQL injection prevention

**Invocar para**: Auditorías de seguridad, configuración de headers, firewall.

---

## 21. Integración con Ecosistema UNIVERSIDAD

Croody Web es parte del monorepo UNIVERSIDAD junto con:

- **Buddy** (Mobile): App Flutter de fitness gamificado
- **Luks** (Blockchain): Smart contracts Solana/Anchor

### Relaciones

| Web (Croody) | Buddy | Luks |
|--------------|-------|------|
| Backend APIs | Consume APIs | Wallet integration |
| User auth | Firebase sync | Token ownership |
| Telemetry | Event tracking | Transaction history |
| E-commerce | In-app purchases | Crypto payments |

### Colores por Producto

```css
Croody (Web):   Gator Green   #3C9E5D
Buddy (Mobile): Crimson Red   #E04F56
Luks (Crypto):  Sand Gold     #E0B771
```

---

## 22. Diátaxis Documentation Framework

La documentación sigue el sistema de 4 cuadrantes:

| Cuadrante | Propósito | Directorio |
|-----------|-----------|------------|
| **Tutoriales** | Aprender haciendo | `docs/01-ARQUITECTURA/` |
| **How-To** | Resolver problemas | `docs/02-BACKEND/` etc. |
| **Referencia** | Descripción técnica | `docs/03-REFERENCIA/` |
| **Explicación** | El "por qué" | ADRs en cada sección |

### Regla de Documentación Viva

> Cambio de código = cambio de documentación en el mismo commit.
> Los subagentes están **obligados** a verificar y actualizar docs afectados.

---

**Última actualización**: Diciembre 2024
