# Aplicación de Usuario - Documentación Completa

## Resumen
La aplicación de usuario de Croody implementa una experiencia completa de onboarding, entrenamiento personalizado y comercio electrónico con tres secciones principales: **Landing** (presentación del ecosistema), **Buddy** (entrenador AI personalizado), y **Shop** (catálogo de productos). Utiliza internacionalización multi-idioma (8 idiomas), tema dual (claro/oscuro), y navegación fluida entre secciones.

## Ubicación
- **Templates**: `/proyecto_integrado/Croody/templates/`
  - `landing/home.html` - Página principal
  - `landing/buddy.html` - Feature Buddy
  - `landing/about.html` - Sobre nosotros
  - `shop/catalogue.html` - Catálogo de productos
  - `shop/detail.html` - Detalle de producto
- **Static**: `/proyecto_integrado/Croody/static/`
  - `css/` - Estilos del Design System
  - `js/` - JavaScript (theme toggle, language selector)
- **Views**: `/proyecto_integrado/Croody/landing/views.py`, `/proyecto_integrado/Croody/shop/views.py`
- **Models**: `/proyecto_integrado/Croody/landing/models.py`, `/proyecto_integrado/Croody/shop/models.py`

## Estructura de la Aplicación

### Diagrama de Navegación
```
Landing Page (/)
├── Hero Section
│   ├── Primary CTA: Ir a la Tienda → /tienda/
│   ├── Secondary CTA: Ver Buddy → /buddy/
│   └── Tertiary CTA: Conoce Más → /nosotros/
├── Metrics Section (Estadísticas)
├── Ecosystem Tabs (Landing, Buddy, Shop)
└── Footer

Buddy Feature (/buddy/)
├── Hero Buddy
├── Explicación Paso a Paso (3 pasos)
├── Beneficios
└── CTA: Ir a la Tienda

Shop (/tienda/)
├── Lista de Productos
├── Filtros
│   ├── Por categoría
│   ├── Por precio
│   └── Por estado (publicado/borrador)
├── Búsqueda
│   ├── Por nombre
│   └── Por teaser
└── Detalle de Producto → /tienda/<slug>/

User Profile (/perfil/)
├── Información Personal
├── Preferencias
│   ├── Idioma
│   └── Tema
└── Token de Ingestión (para robots)
```

## 1. Landing Page

### 1.1 Hero Section

#### Estructura del Contexto
```python
# landing/views.py - HomeView.get_context_data()
hero = {
    'eyebrow': _('Buddy AI · Entrena, Progresa, Destaca'),
    'title': _('Tu entrenador AI personal'),
    'lead': _('Rutinas que se adaptan a ti en tiempo real'),
    'primary_cta': {
        'label': _('🛒 Ir a la Tienda'),
        'url': reverse('shop:catalogue')
    },
    'secondary_cta': {
        'label': _('Ver Buddy'),
        'url': reverse('landing:buddy')
    },
    'tertiary_cta': {
        'label': _('Conocer Más'),
        'url': reverse('landing:about')
    },
    'image': {
        'src': '/static/images/hero-buddy.svg',
        'alt': _('Buddy AI entrenando'),
        'width': 640,
        'height': 480
    }
}
```

#### Implementación en Template
```django
<!-- landing/templates/landing/home.html -->
<section class="hero" data-testid="hero-section">
  <div class="hero__content">
    <div class="hero__text">
      <span class="hero__eyebrow">{{ hero.eyebrow }}</span>
      <h1 class="hero__title">{{ hero.title }}</h1>
      <p class="hero__lead">{{ hero.lead }}</p>

      <div class="hero__cta">
        <a href="{{ hero.primary_cta.url }}"
           class="btn btn--primary"
           data-testid="primary-cta">
          {{ hero.primary_cta.label }}
        </a>
        <a href="{{ hero.secondary_cta.url }}"
           class="btn btn--secondary"
           data-testid="secondary-cta">
          {{ hero.secondary_cta.label }}
        </a>
      </div>
    </div>

    <div class="hero__image">
      <img src="{{ hero.image.src }}"
           alt="{{ hero.image.alt }}"
           width="{{ hero.image.width }}"
           height="{{ hero.image.height }}">
    </div>
  </div>
</section>
```

#### Beneficios UX
- **Eyebrow**: Llamada de atención inicial que menciona el producto principal
- **Title**: Valor proposicional claro en una línea
- **Lead**: Descripción del beneficio para el usuario
- **CTAs**: Múltiples puntos de entrada al ecosistema
  - Primary (Tienda): Conversión directa
  - Secondary (Buddy): Educación sobre el producto
  - Tertiary (Nosotros): Construcción de confianza

### 1.2 Metrics Section

#### Datos Estructurados
```python
metrics = {
    'headline': _('Números que Hablan por Sí Solos'),
    'items': [
        {
            'value': '10,000+',
            'label': _('Usuarios Activos'),
            'description': _('Entrenan con Buddy AI')
        },
        {
            'value': '98%',
            'label': _('Satisfacción'),
            'description': _('Recomiendan la plataforma')
        },
        {
            'value': '50M+',
            'label': _('Rutinas Ejecutadas'),
            'description': _('Entrenamientos completados')
        },
        {
            'value': '24/7',
            'label': _('Soporte'),
            'description': _('Disponible siempre')
        }
    ]
}
```

#### Renderizado
```django
<section class="metrics" data-testid="metrics-section">
  <h2>{{ metrics.headline }}</h2>
  <div class="metrics__grid">
    {% for item in metrics.items %}
      <div class="metric-card" data-testid="metric-item">
        <span class="metric-card__value">{{ item.value }}</span>
        <span class="metric-card__label">{{ item.label }}</span>
        <p class="metric-card__description">{{ item.description }}</p>
      </div>
    {% endfor %}
  </div>
</section>
```

#### Beneficios
- **Credibilidad**: Números concretos generan confianza
- **Social Proof**: Uso de "+" sugiere crecimiento
- **Diferenciación**: 24/7 destaca el soporte constante

### 1.3 Ecosystem Tabs

#### Navegación por Pestañas
```python
vectors = [
    {
        'id': 'landing',
        'label': _('Landing'),
        'title': _('Tu Punto de Partida'),
        'description': _('Conoce la plataforma'),
        'features': [
            _('Onboarding guiado'),
            _('Tutoriales interactivos'),
            _('Casos de uso')
        ]
    },
    {
        'id': 'buddy',
        'label': _('Buddy AI'),
        'title': _('Tu Entrenador Personal'),
        'description': _('IA que se adapta a ti'),
        'features': [
            _('Rutinas personalizadas'),
            _('Seguimiento en tiempo real'),
            _('Ajustes automáticos')
        ]
    },
    {
        'id': 'shop',
        'label': _('Tienda'),
        'title': _('Productos Buddy'),
        'description': _('Elige tu plan'),
        'features': [
            _('Planes flexibles'),
            _('Pago seguro'),
            _('Acceso inmediato')
        ]
    }
]
```

#### Sistema de Tabs
```django
<section class="ecosystem" data-testid="ecosystem-tabs">
  <div class="ecosystem__tabs" role="tablist">
    {% for tab in vectors %}
      <button class="tab"
              role="tab"
              data-tab="{{ tab.id }}"
              aria-selected="{% if forloop.first %}true{% else %}false{% endif %}">
        {{ tab.label }}
      </button>
    {% endfor %}
  </div>

  <div class="ecosystem__content">
    {% for tab in vectors %}
      <div class="tab-panel"
           role="tabpanel"
           data-panel="{{ tab.id }}"
           {% if not forloop.first %}hidden{% endif %}>
        <h3>{{ tab.title }}</h3>
        <p>{{ tab.description }}</p>
        <ul class="feature-list">
          {% for feature in tab.features %}
            <li>{{ feature }}</li>
          {% endfor %}
        </ul>
      </div>
    {% endfor %}
  </div>
</section>
```

#### JavaScript de Tabs
```javascript
// static/js/ecosystem-tabs.js
document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.tab');
  const panels = document.querySelectorAll('.tab-panel');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = tab.dataset.tab;

      // Actualizar tabs activos
      tabs.forEach(t => t.classList.remove('tab--active'));
      tab.classList.add('tab--active');

      // Mostrar panel correspondiente
      panels.forEach(panel => {
        panel.hidden = panel.dataset.panel !== targetId;
      });
    });
  });
});
```

### 1.4 Productos Buddy en Landing

#### Query Optimizada
```python
# En HomeView.get_context_data()
buddy_products = list(
    Product.objects.filter(is_published=True)
    .order_by('sort_order', 'name')
    .values('name', 'slug', 'teaser', 'price', 'delivery_estimate', 'badge_label')[:3]
)

# Fallback si no hay productos en DB
if not buddy_products:
    buddy_products = [
        {
            'name': 'Pack Buddy Starter',
            'slug': 'buddy-starter',
            'teaser': 'Incluye rutina Wimpy para principiantes',
            'price': Decimal('79.00'),
            'delivery_estimate': 'Activación inmediata',
            'badge_label': 'Starter',
        },
        {
            'name': 'Pack Buddy Pro',
            'slug': 'buddy-pro',
            'teaser': 'Rutinas avanzadas con IA personalizada',
            'price': Decimal('149.00'),
            'delivery_estimate': 'Activación inmediata',
            'badge_label': 'Pro',
        },
        {
            'name': 'Pack Buddy Elite',
            'slug': 'buddy-elite',
            'teaser': 'Entrenador AI completo con seguimiento',
            'price': Decimal('299.00'),
            'delivery_estimate': 'Activación inmediata',
            'badge_label': 'Elite',
        }
    ]
```

#### Renderizado
```django
<section class="buddy-products" data-testid="buddy-products">
  <h2>{% trans "Productos Buddy" %}</h2>
  <div class="product-grid">
    {% for product in buddy_products %}
      <article class="product-card">
        {% if product.badge_label %}
          <span class="badge">{{ product.badge_label }}</span>
        {% endif %}
        <h3>{{ product.name }}</h3>
        <p class="teaser">{{ product.teaser }}</p>
        <div class="price">
          <span class="currency">€</span>
          <span class="amount">{{ product.price }}</span>
        </div>
        <p class="delivery">{{ product.delivery_estimate }}</p>
        <a href="{% url 'shop:detail' slug=product.slug %}"
           class="btn btn--primary">
          {% trans "Ver Detalles" %}
        </a>
      </article>
    {% endfor %}
  </div>
</section>
```

## 2. Buddy Feature

### 2.1 Buddy Hero

#### Contexto
```python
# landing/views.py - BuddyView.get_context_data()
buddy_hero = {
    'eyebrow': _('Buddy AI'),
    'title': _('Tu Entrenador Personal'),
    'subtitle': _('IA que Nunca Descansa'),
    'description': _(
        'Buddy AI analiza tu progreso en tiempo real y ajusta '
        'tus rutinas para maximizar resultados. Como tener un '
        'entrenador personal 24/7.'
    ),
    'features': [
        {
            'icon': '🧠',
            'title': _('Aprendizaje Continuo'),
            'description': _('Se adapta a tu progreso')
        },
        {
            'icon': '📊',
            'title': _('Análisis Avanzado'),
            'description': _('Métricas detalladas')
        },
        {
            'icon': '⚡',
            'title': 'Rutinas Dinámicas',
            'description': _('Se ajustan automáticamente')
        }
    ]
}
```

#### Template
```django
<!-- landing/templates/landing/buddy.html -->
<section class="buddy-hero">
  <div class="buddy-hero__content">
    <div class="buddy-hero__text">
      <span class="eyebrow">{{ buddy_hero.eyebrow }}</span>
      <h1>{{ buddy_hero.title }}</h1>
      <h2>{{ buddy_hero.subtitle }}</h2>
      <p class="description">{{ buddy_hero.description }}</p>

      <div class="features">
        {% for feature in buddy_hero.features %}
          <div class="feature">
            <span class="icon">{{ feature.icon }}</span>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        {% endfor %}
      </div>

      <a href="{% url 'shop:catalogue' %}"
         class="btn btn--primary btn--large">
        {% trans "Empezar Ahora" %}
      </a>
    </div>

    <div class="buddy-hero__visual">
      <img src="/static/images/buddy-ai-demo.svg"
           alt="Buddy AI en acción"
           width="640"
           height="480">
    </div>
  </div>
</section>
```

### 2.2 Explicación Paso a Paso

#### Flujo de 3 Pasos
```python
buddy_steps = [
    {
        'number': '01',
        'title': _('Configura tu Perfil'),
        'description': _(
            'Completa tu perfil con tus objetivos, '
            'nivel de experiencia y preferencias.'
        ),
        'details': [
            _('Evaluación inicial'),
            _('Establecimiento de metas'),
            _('Configuración de parámetros')
        ],
        'image': '/static/images/step-1-config.svg'
    },
    {
        'number': '02',
        'title': _('Sigue las Rutinas'),
        'description': _(
            'Ejecuta las rutinas personalizadas que '
            'Buddy genera para ti.'
        ),
        'details': [
            _('Rutinas diarias'),
            _('Seguimiento automático'),
            _('Recordatorios inteligentes')
        ],
        'image': '/static/images/step-2-routine.svg'
    },
    {
        'number': '03',
        'title': _('Observa tu Progreso'),
        'description': _(
            'Ve cómo Buddy ajusta las rutinas basándose '
            'en tus resultados y mejora continua.'
        ),
        'details': [
            _('Métricas en tiempo real'),
            _('Ajustes automáticos'),
            _('Recomendaciones avanzadas')
        ],
        'image': '/static/images/step-3-progress.svg'
    }
]
```

#### Renderizado
```django
<section class="buddy-steps">
  <h2>{% trans "¿Cómo Funciona?" %}</h2>

  <div class="steps">
    {% for step in buddy_steps %}
      <article class="step">
        <div class="step__visual">
          <img src="{{ step.image }}"
               alt="{{ step.title }}"
               width="320"
               height="240">
        </div>

        <div class="step__content">
          <span class="step__number">{{ step.number }}</span>
          <h3>{{ step.title }}</h3>
          <p>{{ step.description }}</p>

          <ul class="step__details">
            {% for detail in step.details %}
              <li>{{ detail }}</li>
            {% endfor %}
          </ul>
        </div>
      </article>
    {% endfor %}
  </div>
</section>
```

### 2.3 Beneficios

#### Lista de Beneficios
```python
buddy_benefits = [
    {
        'icon': '🎯',
        'title': _('Personalización Total'),
        'description': _(
            'Cada rutina está diseñada específicamente '
            'para tus objetivos y capacidades.'
        )
    },
    {
        'icon': '📈',
        'title': _('Progreso Medible'),
        'description': _(
            'Métricas claras que muestran tu evolución '
            'día a día.'
        )
    },
    {
        'icon': '🔄',
        'title': _('Adaptación Continua'),
        'description': _(
            'La IA ajusta automáticamente según '
            'tu rendimiento.'
        )
    },
    {
        'icon': '💪',
        'title': _('Resultados Reales'),
        'description': _(
            'Miles de usuarios han logrado sus '
            'metas con Buddy AI.'
        )
    }
]
```

## 3. Shop (Catálogo)

### 3.1 ProductListView

#### Implementación
```python
# shop/views.py
from django.views.generic import ListView, DetailView
from django.db.models import Q

class ProductListView(LandingNavigationMixin, ListView):
    """Lista de productos con filtros y búsqueda."""
    model = Product
    template_name = 'shop/catalogue.html'
    context_object_name = 'products'
    paginate_by = 12
    ordering = ['sort_order', 'name']

    def get_queryset(self):
        """Queryset filtrado por publicados."""
        queryset = Product.objects.published()

        # Búsqueda
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.search(query)

        # Filtro por categoría (si existe)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)

        # Filtro por rango de precio
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        """Contexto con filtros y resultados."""
        context = super().get_context_data(**kwargs)

        # Búsqueda actual
        context['current_query'] = self.request.GET.get('q', '')

        # Resultados de búsqueda (si hay query)
        if context['current_query']:
            context['search_results'] = self.get_queryset().search(
                context['current_query']
            )
            context['results_count'] = context['search_results'].count()

        return context
```

### 3.2 Catálogo Template

#### Estructura HTML
```django
<!-- shop/templates/shop/catalogue.html -->
{% extends "base.html" %}
{% load i18n %}

{% block title %}{% trans "Tienda" %}{% endblock %}

{% block content %}
<div class="shop" data-testid="shop-catalogue">
  <header class="shop__header">
    <h1>{% trans "Productos Buddy" %}</h1>
    <p class="shop__description">
      {% trans "Elige el plan que mejor se adapte a tus necesidades" %}
    </p>
  </header>

  <div class="shop__content">
    <!-- Sidebar con filtros -->
    <aside class="shop__filters" data-testid="filters-sidebar">
      <form method="get" class="filters-form">
        <!-- Búsqueda -->
        <div class="filter-group">
          <label for="search-input">{% trans "Buscar" %}</label>
          <input type="search"
                 id="search-input"
                 name="q"
                 value="{{ current_query }}"
                 placeholder="{% trans 'Buscar productos...' %}"
                 class="search-input">
        </div>

        <!-- Rango de precio -->
        <div class="filter-group">
          <label>{% trans "Precio" %}</label>
          <div class="price-range">
            <input type="number"
                   name="min_price"
                   placeholder="{% trans 'Mín' %}"
                   min="0">
            <span>—</span>
            <input type="number"
                   name="max_price"
                   placeholder="{% trans 'Máx' %}"
                   min="0">
          </div>
        </div>

        <button type="submit" class="btn btn--primary">
          {% trans "Filtrar" %}
        </button>
      </form>
    </aside>

    <!-- Lista de productos -->
    <main class="shop__products">
      {% if search_results %}
        <div class="search-results" data-testid="search-results">
          <p>
            {% blocktrans with count=results_count %}
              Se encontraron {{ count }} resultado{{ count|pluralize }}
            {% endblocktrans %}
            para "<strong>{{ current_query }}</strong>"
          </p>
        </div>
      {% endif %}

      {% if products %}
        <div class="product-grid" data-testid="product-grid">
          {% for product in products %}
            <article class="product-card" data-testid="product-item">
              <!-- Badge si existe -->
              {% if product.badge_label %}
                <span class="badge badge--primary">{{ product.badge_label }}</span>
              {% endif %}

              <!-- Imagen del producto -->
              <div class="product-card__image">
                <a href="{% url 'shop:detail' slug=product.slug %}">
                  <img src="{{ product.image.url }}"
                       alt="{{ product.name }}"
                       width="320"
                       height="240">
                </a>
              </div>

              <!-- Información del producto -->
              <div class="product-card__content">
                <h3 class="product-card__title">
                  <a href="{% url 'shop:detail' slug=product.slug %}">
                    {{ product.name }}
                  </a>
                </h3>

                <p class="product-card__teaser">{{ product.teaser }}</p>

                <div class="product-card__footer">
                  <span class="price">
                    <span class="currency">€</span>
                    {{ product.price }}
                  </span>

                  <a href="{% url 'shop:detail' slug=product.slug %}"
                     class="btn btn--secondary">
                    {% trans "Ver Detalles" %}
                  </a>
                </div>
              </div>
            </article>
          {% endfor %}
        </div>

        <!-- Paginación -->
        {% if is_paginated %}
          <nav class="pagination" data-testid="pagination">
            {% if page_obj.has_previous %}
              <a href="?page={{ page_obj.previous_page_number }}"
                 class="pagination__link">
                {% trans "Anterior" %}
              </a>
            {% endif %}

            <span class="pagination__current">
              {% blocktrans with number=page_obj.number total=paginator.num_pages %}
                Página {{ number }} de {{ total }}
              {% endblocktrans %}
            </span>

            {% if page_obj.has_next %}
              <a href="?page={{ page_obj.next_page_number }}"
                 class="pagination__link">
                {% trans "Siguiente" %}
              </a>
            {% endif %}
          </nav>
        {% endif %}

      {% else %}
        <!-- Estado vacío -->
        <div class="empty-state" data-testid="empty-state">
          <p>{% trans "No se encontraron productos" %}</p>
          <a href="{% url 'shop:catalogue' %}" class="btn btn--primary">
            {% trans "Ver Todos los Productos" %}
          </a>
        </div>
      {% endif %}
    </main>
  </div>
</div>
{% endblock %}
```

### 3.3 ProductDetailView

#### Implementación
```python
# shop/views.py
class ProductDetailView(LandingNavigationMixin, DetailView):
    """Vista de detalle de producto."""
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """Solo productos publicados."""
        return Product.objects.published()

    def get_context_data(self, **kwargs):
        """Contexto con productos relacionados."""
        context = super().get_context_data(**kwargs)

        # Productos relacionados (misma categoría o publicados)
        product = self.object
        related_products = Product.objects.published().exclude(
            id=product.id
        )[:4]

        context['related_products'] = related_products

        return context
```

#### Template de Detalle
```django
<!-- shop/templates/shop/detail.html -->
{% extends "base.html" %}
{% load i18n %}

{% block title %}{{ product.name }}{% endblock %}

{% block content %}
<article class="product-detail" data-testid="product-detail">
  <div class="product-detail__gallery">
    <img src="{{ product.image.url }}"
         alt="{{ product.name }}"
         width="640"
         height="480">
  </div>

  <div class="product-detail__info">
    {% if product.badge_label %}
      <span class="badge">{{ product.badge_label }}</span>
    {% endif %}

    <h1>{{ product.name }}</h1>
    <p class="teaser">{{ product.teaser }}</p>

    <div class="price">
      <span class="currency">€</span>
      <span class="amount">{{ product.price }}</span>
    </div>

    <div class="delivery-estimate">
      <span class="icon">🚚</span>
      <span>{{ product.delivery_estimate }}</span>
    </div>

    <div class="product-detail__actions">
      <button class="btn btn--primary btn--large" data-testid="add-to-cart">
        {% trans "Añadir al Carrito" %}
      </button>
      <button class="btn btn--secondary">
        {% trans "Favoritos" %}
      </button>
    </div>

    <div class="product-detail__description">
      <h2>{% trans "Descripción" %}</h2>
      <p>{{ product.description|linebreaks }}</p>
    </div>

    <div class="product-detail__features">
      <h3>{% trans "Características" %}</h3>
      <ul>
        <li>✅ {% trans "Rutinas personalizadas" %}</li>
        <li>✅ {% trans "Seguimiento en tiempo real" %}</li>
        <li>✅ {% trans "Soporte 24/7" %}</li>
        <li>✅ {% trans "Acceso de por vida" %}</li>
      </ul>
    </div>
  </div>
</article>

<!-- Productos relacionados -->
{% if related_products %}
  <section class="related-products">
    <h2>{% trans "Productos Relacionados" %}</h2>
    <div class="product-grid">
      {% for related in related_products %}
        <article class="product-card">
          <h3>
            <a href="{% url 'shop:detail' slug=related.slug %}">
              {{ related.name }}
            </a>
          </h3>
          <p class="teaser">{{ related.teaser }}</p>
          <span class="price">€{{ related.price }}</span>
        </article>
      {% endfor %}
    </div>
  </section>
{% endif %}
{% endblock %}
```

## 4. User Profile

### 4.1 ProfileView

#### Implementación
```python
# landing/views.py
class ProfileView(LoginRequiredMixin, LandingNavigationMixin, TemplateView):
    """Vista de perfil de usuario."""
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        """Contexto con formularios y datos del usuario."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = user.profile  # type: ignore[attr-defined]

        # Formularios
        context['profile_form'] = ProfileForm(instance=user)
        context['preferences_form'] = ProfilePreferencesForm(instance=profile)
        context['token_form'] = TokenResetForm()
        context['ingest_token'] = profile.ingest_token

        # Datos para UI
        context['user_display_name'] = profile.display_name or user.get_username()
        context['activity_log'] = self._activity_log(profile)

        return context

    def post(self, request, *args, **kwargs):
        """Maneja múltiples formularios en una vista."""
        form_name = request.POST.get('form')
        user = request.user
        profile = user.profile  # type: ignore[attr-defined]

        if form_name == 'profile':
            form = ProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, _('Perfil actualizado.'))
            else:
                messages.error(request, _('Revisa los campos del perfil.'))

        elif form_name == 'preferences':
            form = ProfilePreferencesForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, _('Preferencias guardadas.'))
            else:
                messages.error(request, _('Revisa las preferencias.'))

        elif form_name == 'token':
            profile.regenerate_token()
            messages.success(
                request,
                _('Generamos un nuevo token para tus robots.')
            )

        return self.get(request, *args, **kwargs)

    def _activity_log(self, profile):
        """Genera log de actividad para UI."""
        return [
            {
                'title': _('Token de ingestión listo'),
                'subtitle': profile.ingest_token,
                'status': 'active' if profile.ingest_token else 'inactive',
            },
            {
                'title': _('Alertas de telemetría'),
                'subtitle': (
                    _('Recibir notificaciones críticas')
                    if profile.telemetry_alerts
                    else _('Alertas desactivadas')
                ),
                'status': 'ok' if profile.telemetry_alerts else 'muted',
            },
        ]
```

### 4.2 Profile Template

#### Estructura HTML
```django
<!-- templates/account/profile.html -->
{% extends "base.html" %}
{% load i18n %}
{% load static %}

{% block title %}{% trans "Mi Perfil" %}{% endblock %}

{% block content %}
<div class="profile" data-testid="user-profile">
  <header class="profile__header">
    <h1>{% trans "Mi Perfil" %}</h1>
    <p class="profile__welcome">
      {% blocktrans with name=user_display_name %}
        Bienvenido, {{ name }}
      {% endblocktrans %}
    </p>
  </header>

  <div class="profile__content">
    <!-- Formulario de Perfil -->
    <section class="profile-section" data-testid="profile-form-section">
      <h2>{% trans "Información Personal" %}</h2>
      <form method="post" class="form">
        {% csrf_token %}
        <input type="hidden" name="form" value="profile">
        {{ profile_form.as_p }}
        <button type="submit" class="btn btn--primary">
          {% trans "Guardar Perfil" %}
        </button>
      </form>
    </section>

    <!-- Formulario de Preferencias -->
    <section class="profile-section" data-testid="preferences-section">
      <h2>{% trans "Preferencias" %}</h2>
      <form method="post" class="form">
        {% csrf_token %}
        <input type="hidden" name="form" value="preferences">
        {{ preferences_form.as_p }}
        <button type="submit" class="btn btn--primary">
          {% trans "Guardar Preferencias" %}
        </button>
      </form>
    </section>

    <!-- Token de Ingestión -->
    <section class="profile-section" data-testid="token-section">
      <h2>{% trans "Token de Ingestión para Robots" %}</h2>
      <p class="description">
        {% trans "Utiliza este token para que tus robots envíen datos de telemetría." %}
      </p>

      <div class="token-display">
        <input type="text"
               value="{{ ingest_token }}"
               readonly
               class="token-input"
               data-testid="ingest-token">
        <button class="btn btn--secondary"
                onclick="copyToken()"
                data-testid="copy-token-btn">
          {% trans "Copiar" %}
        </button>
      </div>

      <form method="post" class="form">
        {% csrf_token %}
        <input type="hidden" name="form" value="token">
        <button type="submit" class="btn btn--danger">
          {% trans "Regenerar Token" %}
        </button>
      </form>
    </section>

    <!-- Activity Log -->
    <section class="profile-section" data-testid="activity-log">
      <h2>{% trans "Actividad Reciente" %}</h2>
      <div class="activity-list">
        {% for entry in activity_log %}
          <div class="activity-item">
            <div class="activity-item__content">
              <h3>{{ entry.title }}</h3>
              <p>{{ entry.subtitle }}</p>
            </div>
            <span class="status status--{{ entry.status }}"></span>
          </div>
        {% endfor %}
      </div>
    </section>
  </div>
</div>

<script>
function copyToken() {
  const tokenInput = document.querySelector('[data-testid="ingest-token"]');
  tokenInput.select();
  document.execCommand('copy');

  const btn = document.querySelector('[data-testid="copy-token-btn"]');
  const originalText = btn.textContent;
  btn.textContent = '{% trans "Copiado" %}';
  setTimeout(() => {
    btn.textContent = originalText;
  }, 2000);
}
</script>
{% endblock %}
```

## 5. Navegación y UX

### 5.1 Primary Navigation

#### Implementación
```python
# landing/views.py
def primary_nav_links() -> list[dict[str, str]]:
    """Links de navegación primaria."""
    return [
        {
            'label': _('Inicio'),
            'url': reverse('landing:home'),
            'icon': '🏠'
        },
        {
            'label': _('Buddy'),
            'url': reverse('landing:buddy'),
            'icon': '🤖'
        },
        {
            'label': _('Tienda'),
            'url': reverse('shop:catalogue'),
            'icon': '🛒'
        },
        {
            'label': _('Nosotros'),
            'url': reverse('landing:about'),
            'icon': 'ℹ️'
        },
    ]
```

#### Template
```django
<!-- templates/base.html -->
<nav class="primary-nav" data-testid="primary-navigation">
  <ul class="nav-list">
    {% for link in nav_links %}
      <li class="nav-item">
        <a href="{{ link.url }}"
           class="nav-link"
           {% if request.resolver_match.url_name == link.url|slice:":-1"|slice:"1:" %}aria-current="page"{% endif %}>
          <span class="nav-icon">{{ link.icon }}</span>
          <span class="nav-label">{{ link.label }}</span>
        </a>
      </li>
    {% endfor %}
  </ul>
</nav>
```

### 5.2 User Menu

#### Con Autenticación
```django
{% if request.user.is_authenticated %}
  <div class="user-menu" data-testid="user-menu">
    <button class="user-menu__trigger"
            aria-expanded="false"
            aria-haspopup="true">
      <span class="user-avatar">
        {{ request.user.get_username|first|upper }}
      </span>
      <span class="user-name">{{ request.user.get_username }}</span>
    </button>

    <ul class="user-menu__dropdown">
      <li>
        <a href="{% url 'landing:profile' %}">
          {% trans "Mi Perfil" %}
        </a>
      </li>
      <li>
        <a href="{% url 'landing:logout' %}">
          {% trans "Cerrar Sesión" %}
        </a>
      </li>
    </ul>
  </div>
{% else %}
  <div class="auth-links" data-testid="auth-links">
    <a href="{% url 'landing:login' %}" class="btn btn--secondary">
      {% trans "Iniciar Sesión" %}
    </a>
    <a href="{% url 'landing:signup' %}" class="btn btn--primary">
      {% trans "Registrarse" %}
    </a>
  </div>
{% endif %}
```

### 5.3 Footer

#### Enlaces del Footer
```django
<footer class="footer" data-testid="site-footer">
  <div class="footer__content">
    <div class="footer__brand">
      <h3>Croody</h3>
      <p>{% trans "Tu entrenador AI personal" %}</p>
    </div>

    <div class="footer__links">
      <h4>{% trans "Producto" %}</h4>
      <ul>
        <li><a href="{% url 'landing:buddy' %}">{% trans "Buddy AI" %}</a></li>
        <li><a href="{% url 'shop:catalogue' %}">{% trans "Planes" %}</a></li>
        <li><a href="#">{% trans "Precios" %}</a></li>
      </ul>
    </div>

    <div class="footer__links">
      <h4>{% trans "Empresa" %}</h4>
      <ul>
        <li><a href="{% url 'landing:about' %}">{% trans "Nosotros" %}</a></li>
        <li><a href="#">{% trans "Blog" %}</a></li>
        <li><a href="#">{% trans "Carreras" %}</a></li>
      </ul>
    </div>

    <div class="footer__links">
      <h4>{% trans "Soporte" %}</h4>
      <ul>
        <li><a href="#">{% trans "Ayuda" %}</a></li>
        <li><a href="#">{% trans "Contacto" %}</a></li>
        <li><a href="#">{% trans "Estado" %}</a></li>
      </ul>
    </div>
  </div>

  <div class="footer__bottom">
    <p>&copy; {% now "Y" %} Croody. {% trans "Todos los derechos reservados" %}</p>
    <div class="footer__legal">
      <a href="#">{% trans "Privacidad" %}</a>
      <a href="#">{% trans "Términos" %}</a>
    </div>
  </div>
</footer>
```

## 6. Estados de la Aplicación

### 6.1 Loading States

#### Skeleton Loader
```html
<div class="product-card skeleton" data-testid="loading">
  <div class="skeleton-image"></div>
  <div class="skeleton-title"></div>
  <div class="skeleton-text"></div>
  <div class="skeleton-button"></div>
</div>
```

#### CSS Skeleton
```css
.skeleton {
  background: #f0f0f0;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.skeleton-image,
.skeleton-title,
.skeleton-text,
.skeleton-button {
  background: #e0e0e0;
  border-radius: 4px;
  margin-bottom: 12px;
}

.skeleton-image {
  width: 100%;
  height: 240px;
}

.skeleton-title {
  width: 70%;
  height: 24px;
}

.skeleton-text {
  width: 100%;
  height: 16px;
}

.skeleton-button {
  width: 50%;
  height: 40px;
}
```

### 6.2 Empty States

#### Sin Productos
```django
<div class="empty-state" data-testid="empty-state">
  <div class="empty-state__icon">📦</div>
  <h3>{% trans "No hay productos" %}</h3>
  <p>{% trans "Aún no hemos añadido productos a esta categoría." %}</p>
  <a href="{% url 'shop:catalogue' %}" class="btn btn--primary">
    {% trans "Ver Todos los Productos" %}
  </a>
</div>
```

#### CSS Empty State
```css
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-state__icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.empty-state h3 {
  margin-bottom: 12px;
  color: var(--color-text-primary);
}

.empty-state p {
  color: var(--color-text-secondary);
  margin-bottom: 24px;
}
```

### 6.3 Error States

#### Error de Carga
```django
<div class="error-state" data-testid="error-state">
  <div class="error-state__icon">⚠️</div>
  <h3>{% trans "Error al cargar" %}</h3>
  <p>{% trans "No pudimos cargar el contenido. Inténtalo de nuevo." %}</p>
  <button onclick="window.location.reload()" class="btn btn--primary">
    {% trans "Reintentar" %}
  </button>
</div>
```

## 7. Accesibilidad (a11y)

### 7.1 Semántica HTML

#### Landmarks
```html
<main role="main" data-testid="main-content">
  <!-- Contenido principal -->
</main>

<aside role="complementary" data-testid="sidebar">
  <!-- Contenido complementario -->
</aside>

<nav role="navigation" aria-label="Primary" data-testid="primary-navigation">
  <!-- Navegación -->
</nav>

<footer role="contentinfo" data-testid="site-footer">
  <!-- Footer -->
</footer>
```

### 7.2 ARIA Labels

#### Tablist
```html
<div role="tablist" aria-label="Ecosystem sections">
  <button role="tab"
          aria-selected="true"
          aria-controls="panel-landing"
          id="tab-landing">
    Landing
  </button>
  <button role="tab"
          aria-selected="false"
          aria-controls="panel-buddy"
          id="tab-buddy"
          tabindex="-1">
    Buddy
  </button>
</div>

<div role="tabpanel"
     id="panel-landing"
     aria-labelledby="tab-landing">
  <!-- Panel content -->
</div>
```

### 7.3 Skip Links

```django
<a href="#main-content" class="skip-link">
  {% trans "Saltar al contenido principal" %}
</a>

<!-- Al inicio del body -->
```

#### CSS Skip Link
```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-primary);
  color: white;
  padding: 8px 16px;
  z-index: 100;
  text-decoration: none;
}

.skip-link:focus {
  top: 0;
}
```

### 7.4 Focus Management

#### Focus Visible
```css
/* Mejora la visibilidad del foco */
*:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Focus visible para elementos interactivos */
.btn:focus-visible,
a:focus-visible,
input:focus-visible {
  box-shadow: 0 0 0 3px var(--color-primary-alpha);
}
```

#### JavaScript Focus Trap (Modal)
```javascript
// Ejemplo para modal o dropdown
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
  );
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  element.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    }
  });
}
```

## 8. Responsive Design

### 8.1 Breakpoints

#### CSS Custom Properties
```css
:root {
  /* Breakpoints */
  --breakpoint-xs: 480px;
  --breakpoint-sm: 768px;
  --breakpoint-md: 1024px;
  --breakpoint-lg: 1280px;
  --breakpoint-xl: 1536px;
}
```

#### Media Queries
```css
/* Mobile First */
.shop__content {
  display: block;
}

/* Tablet */
@media (min-width: 768px) {
  .shop__content {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 32px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .shop__content {
    gap: 48px;
  }
}
```

### 8.2 Responsive Navigation

#### Mobile Menu
```django
<button class="mobile-menu__toggle"
        aria-expanded="false"
        aria-controls="mobile-menu"
        data-testid="mobile-menu-toggle">
  <span class="sr-only">{% trans "Abrir menú" %}</span>
  <svg class="icon-menu" width="24" height="24">
    <!-- Icono hamburguesa -->
  </svg>
</button>

<div id="mobile-menu" class="mobile-menu" hidden>
  <!-- Menú móvil -->
</div>
```

#### JavaScript Mobile Menu
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('[data-testid="mobile-menu-toggle"]');
  const menu = document.getElementById('mobile-menu');

  toggle.addEventListener('click', () => {
    const isOpen = menu.hasAttribute('hidden') ? false : true;

    if (isOpen) {
      menu.setAttribute('hidden', '');
      toggle.setAttribute('aria-expanded', 'false');
    } else {
      menu.removeAttribute('hidden');
      toggle.setAttribute('aria-expanded', 'true');
    }
  });
});
```

### 8.3 Responsive Grid

#### Product Grid
```css
.product-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: 1fr;
}

/* 2 columnas en tablet */
@media (min-width: 768px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

/* 3 columnas en desktop */
@media (min-width: 1024px) {
  .product-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
  }
}

/* 4 columnas en desktop grande */
@media (min-width: 1280px) {
  .product-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

## 9. Performance

### 9.1 Lazy Loading

#### Imágenes
```django
<!-- Lazy loading nativo -->
<img src="{{ product.image.url }}"
     alt="{{ product.name }}"
     width="320"
     height="240"
     loading="lazy">

<!-- Lazy loading con Intersection Observer -->
<img data-src="{{ product.image.url }}"
     alt="{{ product.name }}"
     class="lazy-image">
```

#### JavaScript Lazy Loading
```javascript
// Lazy loading de imágenes
const images = document.querySelectorAll('.lazy-image');

const imageObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.classList.remove('lazy-image');
      imageObserver.unobserve(img);
    }
  });
});

images.forEach(img => imageObserver.observe(img));
```

### 9.2 Code Splitting

#### JavaScript Módulos
```javascript
// theme.js
export function initThemeToggle() {
  // Lógica del toggle de tema
}

// language-selector.js
export function initLanguageSelector() {
  // Lógica del selector de idioma
}

// main.js
import { initThemeToggle } from './theme.js';
import { initLanguageSelector } from './language-selector.js';

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initLanguageSelector();
});
```

### 9.3 Image Optimization

#### Responsive Images
```django
<picture>
  <source media="(min-width: 1280px)"
          srcset="{{ product.image-xl.url }} 1280w,
                  {{ product.image-lg.url }} 1024w">
  <source media="(min-width: 768px)"
          srcset="{{ product.image-md.url }} 768w">
  <img src="{{ product.image-sm.url }}"
       alt="{{ product.name }}"
       width="320"
       height="240"
       loading="lazy">
</picture>
```

#### WebP Support
```django
<picture>
  <source srcset="{{ product.image.webp }}"
          type="image/webp">
  <img src="{{ product.image.jpg }}"
       alt="{{ product.name }}">
</picture>
```

## 10. SEO

### 10.1 Meta Tags

#### Base Template
```django
<!-- templates/base.html -->
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- SEO Básico -->
  <title>{% block title %}Croody - Tu Entrenador AI{% endblock %}</title>
  <meta name="description"
        content="{% block description %}Entrena con Buddy AI, tu entrenador personal que se adapta a ti en tiempo real.{% endblock %}">

  <!-- Open Graph -->
  <meta property="og:title" content="{% block og_title %}{{ block.super }}{% endblock %}">
  <meta property="og:description" content="{% block og_description %}{{ block.super }}{% endblock %}">
  <meta property="og:image" content="{% block og_image %}{% static 'images/og-image.jpg' %}{% endblock %}">
  <meta property="og:url" content="{{ request.build_absolute_uri }}">
  <meta property="og:type" content="website">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{% block twitter_title %}{{ block.super }}{% endblock %}">
  <meta name="twitter:description" content="{% block twitter_description %}{{ block.super }}{% endblock %}">
  <meta name="twitter:image" content="{% block twitter_image %}{% static 'images/twitter-image.jpg' %}{% endblock %}">
</head>
```

#### Product Detail SEO
```django
{% block title %}{{ product.name }} - {{ block.super }}{% endblock %}

{% block description %}{{ product.teaser }}{% endblock %}

{% block og_title %}{{ product.name }} - €{{ product.price }}{% endblock %}

{% block og_description %}{{ product.teaser }}{% endblock %}

{% block og_image %}{{ product.image.url }}{% endblock %}
```

### 10.2 Structured Data

#### Product Schema
```django
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "{{ product.name }}",
  "image": "{{ request.scheme }}://{{ request.get_host }}{{ product.image.url }}",
  "description": "{{ product.teaser }}",
  "brand": {
    "@type": "Brand",
    "name": "Croody"
  },
  "offers": {
    "@type": "Offer",
    "url": "{{ request.build_absolute_uri }}",
    "priceCurrency": "EUR",
    "price": "{{ product.price }}",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

#### Breadcrumb Schema
```django
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Inicio",
      "item": "{{ request.scheme }}://{{ request.get_host }}/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Tienda",
      "item": "{{ request.scheme }}://{{ request.get_host }}{% url 'shop:catalogue' %}"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "{{ product.name }}",
      "item": "{{ request.build_absolute_uri }}"
    }
  ]
}
</script>
```

### 10.3 Sitemap

#### Generación Automática
```python
# shop/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Product

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.published()

    def lastmod(self, obj):
        return obj.updated_at
```

#### Registro en Sitemaps
```python
# croody/urls.py
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from shop.sitemaps import ProductSitemap

sitemaps = {
    'products': ProductSitemap,
}

urlpatterns = [
    # ...
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
```

## Referencias

### Archivos Relacionados
- `templates/landing/home.html` - Landing page con hero, metrics, ecosystem
- `templates/landing/buddy.html` - Feature Buddy con explicación paso a paso
- `templates/shop/catalogue.html` - Catálogo de productos con filtros
- `templates/shop/detail.html` - Detalle de producto individual
- `templates/account/profile.html` - Perfil de usuario con formularios
- `landing/views.py` - Views de landing (HomeView, BuddyView, ProfileView)
- `shop/views.py` - Views de shop (ProductListView, ProductDetailView)
- `landing/models.py` - UserProfile con OneToOne y tokens
- `shop/models.py` - Product con QuerySet personalizado

### Herramientas
- [Django Templates](https://docs.djangoproject.com/en/stable/ref/templates/) - Sistema de templates
- [Django i18n](https://docs.djangoproject.com/en/stable/topics/i18n/) - Internacionalización
- [HTML Living Standard](https://html.spec.whatwg.org/) - Estándares HTML
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/) - Guías de accesibilidad
- [Schema.org](https://schema.org/) - Datos estructurados

### Documentación Externa
- [Django Class-Based Views](https://docs.djangoproject.com/en/stable/topics/class-based-views/)
- [Responsive Web Design](https://web.dev/responsive-web-design-basics/)
- [Image Optimization](https://web.dev/fast/)
- [Core Web Vitals](https://web.dev/vitals/)

## Ver También
- [Design System - Tokens y Componentes](../07-DESIGN-System/componentes.md)
- [JavaScript - Theme Toggle y Language Selector](../07-DESIGN-System/javascript.md)
- [Internacionalización - 8 Idiomas](../05-INTERNACIONALIZACION/i18n-completo.md)
- [Patrones de Desarrollo - CBV y Mixins](../08-PATRONES/desarrollo.md)
