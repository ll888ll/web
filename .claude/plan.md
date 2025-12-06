# Plan: Sistema de Reviews y Ratings para Productos (E-commerce Enhancement)

## Resumen Ejecutivo

Implementar un sistema completo de opiniones de usuarios para productos de la tienda, incluyendo:
- Reviews con texto y rating (1-5 estrellas)
- Sistema de moderación con estado de aprobación
- Estadísticas agregadas por producto
- Integración con panel de administración

## Scope MVP

- **Incluido:** Reviews básicos + rating + moderación + display en producto
- **Excluido:** Respuestas a reviews, votos de utilidad, fotos en reviews (fase 2)

---

## Arquitectura: Fat Model Pattern

### Decision Arquitectónica (ADR)

**Contexto:** El sistema requiere:
1. Almacenamiento de reviews con relaciones a User y Product
2. Cálculo eficiente de ratings promedio
3. Moderación antes de publicación

**Decisión:** Implementar con **Fat Models** siguiendo los patrones de Croody:
- Lógica de negocio en el modelo Review
- Signals para actualizar estadísticas agregadas
- Manager personalizado para queries comunes

**Razones:**
| Aspecto | Decisión | Alternativa Descartada |
|---------|----------|------------------------|
| Rating promedio | Campo denormalizado en Product | Calcular en cada request (N+1) |
| Moderación | Campo `is_approved` con default False | Sistema separado de moderación |
| Estadísticas | Actualizar via signals | Task celery (overhead) |

**Consecuencias:**
- (+) Performance óptima en listados de productos
- (+) Moderación integrada en admin existente
- (+) Código cohesivo en un solo lugar
- (-) Requiere signals bien documentados

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    Django Models                             │
│                                                              │
│  ┌─────────────┐     ┌─────────────┐     ┌──────────────┐  │
│  │   Product   │     │   Review    │     │ ReviewStats  │  │
│  │             │◄────│             │────▶│  (agregado)  │  │
│  │ avg_rating  │     │ rating 1-5  │     │ por producto │  │
│  │ review_count│     │ text        │     │              │  │
│  └─────────────┘     │ is_approved │     └──────────────┘  │
│         ▲            │ user FK     │                        │
│         │            └─────────────┘                        │
│         │                   │                               │
│         └───────────────────┘                               │
│            post_save signal                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
           │                           │
           ▼                           ▼
┌─────────────────────┐     ┌─────────────────────┐
│   PRODUCT DETAIL    │     │    ADMIN PANEL      │
│  (shop/templates/)  │     │  (shop/admin.py)    │
│  ┌───────────────┐  │     │  ┌───────────────┐  │
│  │ ProductDetail │  │     │  │ ReviewAdmin   │  │
│  └───────────────┘  │     │  └───────────────┘  │
│  + ReviewList       │     │  + Approve action   │
│  + ReviewForm       │     │  + Bulk moderation  │
│  + RatingDisplay    │     │  + Filters          │
└─────────────────────┘     └─────────────────────┘
```

### Estructura de Archivos

```
proyecto_integrado/Croody/shop/
├── models/
│   ├── __init__.py              # Importar Review
│   ├── product.py               # MODIFICAR: agregar campos rating
│   └── review.py                # NUEVO: modelo Review
├── views/
│   └── shop_views.py            # MODIFICAR: agregar ReviewCreateView
├── forms/
│   └── review_forms.py          # NUEVO: ReviewForm
├── admin.py                     # MODIFICAR: registrar ReviewAdmin
├── signals/
│   └── review_signals.py        # NUEVO: actualizar stats en save
└── templates/shop/
    ├── product_detail.html      # MODIFICAR: agregar sección reviews
    └── partials/
        ├── review_list.html     # NUEVO: lista de reviews HTMX
        └── review_form.html     # NUEVO: formulario HTMX
```

---

## Fase 1: Domain Layer (Modelos)

### 1.1 Modelo `Review`

```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class ReviewManager(models.Manager):
    """Manager personalizado para queries comunes."""

    def approved(self):
        """Retorna solo reviews aprobados."""
        return self.filter(is_approved=True)

    def pending(self):
        """Retorna reviews pendientes de moderación."""
        return self.filter(is_approved=False)

    def for_product(self, product):
        """Reviews aprobados de un producto."""
        return self.approved().filter(product=product)


class Review(models.Model):
    """
    Opinión de usuario sobre un producto.

    @context(ADR-REVIEWS): Fat model con lógica de validación integrada.
    """

    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Product')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='product_reviews',
        verbose_name=_('User')
    )
    rating = models.PositiveSmallIntegerField(
        _('Rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rating from 1 to 5 stars')
    )
    title = models.CharField(
        _('Title'),
        max_length=100,
        blank=True
    )
    text = models.TextField(
        _('Review text'),
        max_length=2000,
        help_text=_('Maximum 2000 characters')
    )
    is_approved = models.BooleanField(
        _('Approved'),
        default=False,
        help_text=_('Review visible after admin approval')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        unique_together = ['product', 'user']  # Un review por usuario por producto
        indexes = [
            models.Index(fields=['product', 'is_approved', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"

    def get_stars_display(self):
        """Retorna representación visual de estrellas."""
        return '★' * self.rating + '☆' * (5 - self.rating)
```

### 1.2 Modificación de `Product`

Agregar campos denormalizados para performance:

```python
# En shop/models/product.py

class Product(models.Model):
    # ... campos existentes ...

    # Campos denormalizados para reviews (actualizados via signal)
    average_rating = models.DecimalField(
        _('Average rating'),
        max_digits=2,
        decimal_places=1,
        default=0,
        editable=False
    )
    review_count = models.PositiveIntegerField(
        _('Review count'),
        default=0,
        editable=False
    )

    def update_review_stats(self):
        """Recalcula estadísticas de reviews."""
        from django.db.models import Avg, Count
        stats = self.reviews.filter(is_approved=True).aggregate(
            avg=Avg('rating'),
            count=Count('id')
        )
        self.average_rating = stats['avg'] or 0
        self.review_count = stats['count']
        self.save(update_fields=['average_rating', 'review_count'])
```

### 1.3 Signal para Actualizar Stats

```python
# shop/signals/review_signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from shop.models import Review

@receiver(post_save, sender=Review)
def update_product_stats_on_save(sender, instance, **kwargs):
    """Actualiza stats del producto cuando se guarda/aprueba un review."""
    instance.product.update_review_stats()

@receiver(post_delete, sender=Review)
def update_product_stats_on_delete(sender, instance, **kwargs):
    """Actualiza stats del producto cuando se elimina un review."""
    instance.product.update_review_stats()
```

---

## Fase 2: Data Layer (Forms y Admin)

### 2.1 ReviewForm

```python
# shop/forms/review_forms.py

from django import forms
from django.utils.translation import gettext_lazy as _
from shop.models import Review

class ReviewForm(forms.ModelForm):
    """Formulario para crear reviews."""

    RATING_CHOICES = [(i, f'{i} {"★" * i}') for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label=_('Rating')
    )

    class Meta:
        model = Review
        fields = ['rating', 'title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('Brief summary (optional)')
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': _('Share your experience with this product...')
            }),
        }

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if len(text) < 20:
            raise forms.ValidationError(
                _('Review must be at least 20 characters long.')
            )
        return text
```

### 2.2 ReviewAdmin

```python
# En shop/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from shop.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'text']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    actions = ['approve_reviews', 'reject_reviews']

    @admin.action(description=_('Approve selected reviews'))
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} reviews approved.')

    @admin.action(description=_('Reject selected reviews'))
    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} reviews rejected.')
```

---

## Fase 3: Presentation Layer

### 3.1 ReviewCreateView (HTMX)

```python
# shop/views/review_views.py

from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from shop.models import Review, Product
from shop.forms import ReviewForm

class ReviewCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear reviews via HTMX."""
    model = Review
    form_class = ReviewForm
    template_name = 'shop/partials/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = Product.objects.get(
            slug=self.kwargs['product_slug']
        )
        form.save()
        # Retornar mensaje de éxito para HTMX
        return HttpResponse(
            '<div class="alert alert-success">'
            'Thank you! Your review is pending approval.</div>'
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
```

### 3.2 Templates

#### review_list.html (Partial HTMX)

```html
{# shop/templates/shop/partials/review_list.html #}
{% load i18n %}

<div class="reviews-section" id="reviews">
    <h3 class="text-2xl font-display">{% trans "Customer Reviews" %}</h3>

    {% if product.review_count > 0 %}
    <div class="rating-summary">
        <span class="rating-stars">
            {% for i in "12345" %}
                {% if forloop.counter <= product.average_rating %}
                    <span class="star filled">★</span>
                {% else %}
                    <span class="star">☆</span>
                {% endif %}
            {% endfor %}
        </span>
        <span class="rating-text">
            {{ product.average_rating }} {% trans "out of 5" %}
            ({{ product.review_count }} {% trans "reviews" %})
        </span>
    </div>

    <div class="reviews-list">
        {% for review in reviews %}
        <article class="review-card vector-card">
            <header class="review-header">
                <span class="reviewer-name">{{ review.user.username }}</span>
                <span class="review-rating">{{ review.get_stars_display }}</span>
                <time class="review-date">{{ review.created_at|date:"M d, Y" }}</time>
            </header>
            {% if review.title %}
            <h4 class="review-title">{{ review.title }}</h4>
            {% endif %}
            <p class="review-text">{{ review.text }}</p>
        </article>
        {% empty %}
        <p class="no-reviews">{% trans "No reviews yet. Be the first!" %}</p>
        {% endfor %}
    </div>
    {% endif %}
</div>
```

#### review_form.html (Partial HTMX)

```html
{# shop/templates/shop/partials/review_form.html #}
{% load i18n %}

<form hx-post="{% url 'shop:review-create' product.slug %}"
      hx-target="#review-form-container"
      hx-swap="innerHTML"
      class="review-form vector-card">
    {% csrf_token %}

    <h4>{% trans "Write a Review" %}</h4>

    <div class="form-group">
        <label>{% trans "Rating" %}</label>
        <div class="star-rating">
            {% for value, label in form.rating.field.choices %}
            <label class="star-label">
                <input type="radio" name="rating" value="{{ value }}"
                       {% if form.rating.value == value %}checked{% endif %}>
                <span class="star">{{ label }}</span>
            </label>
            {% endfor %}
        </div>
        {% if form.rating.errors %}
        <span class="error">{{ form.rating.errors.0 }}</span>
        {% endif %}
    </div>

    <div class="form-group">
        {{ form.title.label_tag }}
        {{ form.title }}
    </div>

    <div class="form-group">
        {{ form.text.label_tag }}
        {{ form.text }}
        {% if form.text.errors %}
        <span class="error">{{ form.text.errors.0 }}</span>
        {% endif %}
    </div>

    <button type="submit" class="btn-primary">
        {% trans "Submit Review" %}
    </button>
</form>
```

---

## Fase 4: URLs y Integración

### 4.1 URLs

```python
# shop/urls.py

from django.urls import path
from shop.views import ReviewCreateView

app_name = 'shop'

urlpatterns = [
    # ... existing patterns ...
    path(
        'product/<slug:product_slug>/review/',
        ReviewCreateView.as_view(),
        name='review-create'
    ),
]
```

### 4.2 Integración en ProductDetailView

```python
# Modificar shop/views/shop_views.py

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.for_product(self.object)[:10]
        context['review_form'] = ReviewForm()
        context['user_has_reviewed'] = (
            self.request.user.is_authenticated and
            Review.objects.filter(
                product=self.object,
                user=self.request.user
            ).exists()
        )
        return context
```

---

## Tareas de Implementación

### Sprint 1: Core Models (1-2 días)

| # | Tarea | Archivos |
|---|-------|----------|
| 1.1 | Crear modelo Review | `shop/models/review.py` |
| 1.2 | Modificar modelo Product | `shop/models/product.py` |
| 1.3 | Crear signals | `shop/signals/review_signals.py` |
| 1.4 | Crear migration | `shop/migrations/` |
| 1.5 | Tests unitarios | `tests/shop/test_review_model.py` |

### Sprint 2: Admin y Forms (1 día)

| # | Tarea | Archivos |
|---|-------|----------|
| 2.1 | Registrar ReviewAdmin | `shop/admin.py` |
| 2.2 | Crear ReviewForm | `shop/forms/review_forms.py` |
| 2.3 | Tests de admin | `tests/shop/test_review_admin.py` |

### Sprint 3: Views y Templates (2 días)

| # | Tarea | Archivos |
|---|-------|----------|
| 3.1 | Crear ReviewCreateView | `shop/views/review_views.py` |
| 3.2 | Crear templates HTMX | `templates/shop/partials/` |
| 3.3 | Integrar en product_detail | `templates/shop/product_detail.html` |
| 3.4 | Agregar URLs | `shop/urls.py` |
| 3.5 | Tests de integración | `tests/shop/test_review_views.py` |

### Sprint 4: Polish y QA (1 día)

| # | Tarea | Archivos |
|---|-------|----------|
| 4.1 | Estilos CSS | `static/css/components/reviews.css` |
| 4.2 | Traducciones | `locale/*/LC_MESSAGES/django.po` |
| 4.3 | Documentación | `docs/02-BACKEND/modelos/review.md` |

---

## Dependencias

```python
# No se requieren dependencias nuevas
# Usa solo Django core features
```

---

## Riesgos y Mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Spam de reviews | Sistema de moderación + rate limiting |
| Reviews falsos | unique_together(product, user) + verificación de compra (fase 2) |
| Performance con muchos reviews | Paginación + campos denormalizados |
| Contenido inapropiado | Moderación manual + filtros de palabras (fase 2) |

---

## Métricas de Éxito

- [ ] Usuario puede crear review desde página de producto
- [ ] Admin puede aprobar/rechazar reviews en bulk
- [ ] Rating promedio se actualiza correctamente
- [ ] Reviews se muestran solo después de aprobación
- [ ] HTMX funciona sin reload de página
- [ ] Tests con >80% coverage en módulo review

---

## Fase 2 (Futuro)

- Respuestas del vendedor a reviews
- Votos de utilidad ("¿Te fue útil?")
- Fotos en reviews
- Verificación de compra ("Compra verificada")
- Filtros por rating en listado
- Notificaciones de nuevos reviews
