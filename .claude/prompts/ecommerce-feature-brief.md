# E-Commerce Feature: Brief para /feature-dev

> Copia este contenido como argumento de una feature o pégalo directamente.
> Template para features de la tienda online Croody.

---

<default_to_action>true</default_to_action>

## Feature: [NOMBRE DE LA FEATURE]

Necesito implementar **[descripción corta]** en la tienda online de Croody. La UI debe seguir el sistema **Sacred Geometry** con tokens CSS del proyecto, respetando la paleta Gator (verde) y Jungle (neutros).

### Contexto del Proyecto

Este es un proyecto Django + HTMX con tema dark por defecto. El sistema de diseño está basado en el Número Áureo (φ = 1.618). Los tokens CSS están en `static/css/tokens.css`.

La documentación relevante está en:
- `docs/03-FRONTEND/` — Sistema de diseño y componentes
- `docs/02-BACKEND/` — Modelos y APIs
- `.claude/skills/sacred-geometry-design/SKILL.md` — Guía completa de diseño
- `.claude/skills/django-patterns/SKILL.md` — Patrones de backend

### Lo que necesito implementar

**1. Backend (django-architect)**

[Describe los modelos, vistas, y lógica de negocio necesarios]

Ejemplo:
```python
# shop/models.py
class Review(models.Model):
    """Review de producto por usuario."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[...])
    comment = models.TextField(max_length=1000)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def get_stars_display(self) -> str:
        """Retorna rating como estrellas Unicode."""
        full = int(self.rating)
        half = 1 if self.rating - full >= 0.5 else 0
        return '★' * full + '½' * half + '☆' * (5 - full - half)
```

**2. Frontend (frontend-artist)**

[Describe los templates y CSS necesarios]

Ejemplo:
```html
<!-- templates/shop/partials/review_card.html -->
<article class="review-card fade-in-up"
         hx-get="{% url 'shop:review-detail' review.id %}"
         hx-trigger="click"
         hx-target="#modal-container">
    <header class="review-card-header">
        <span class="rating">{{ review.get_stars_display }}</span>
        <time datetime="{{ review.created_at|date:'c' }}">
            {{ review.created_at|timesince }} ago
        </time>
    </header>
    <div class="review-card-content">
        <p>{{ review.comment|truncatewords:50 }}</p>
    </div>
    <footer class="review-card-footer">
        <span class="author">{{ review.user.username }}</span>
    </footer>
</article>
```

```css
/* static/css/components.css */
.review-card {
    padding: var(--space-3);
    background: var(--surface-1);
    border-radius: var(--radius-2);
    transition: var(--transition);
}

.review-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}

.review-card-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--space-2);
}

.rating {
    color: var(--sand-500); /* Gold for stars */
}
```

**3. API (si es FastAPI)**

[Si la feature requiere endpoints API]

```python
# telemetry_api/api/reviews.py
@router.post("/products/{product_id}/reviews", status_code=201)
async def create_review(product_id: int, review: ReviewCreate):
    """Crea un review para un producto."""
    pass
```

### Expressivity Zone

Esta feature es **[HIGH/MEDIUM/LOW]** expressivity:
- HIGH: Hero sections, featured products, CTAs → Permitir glows, animaciones complejas
- MEDIUM: Cards, navigation → Hover effects sutiles, transforms
- LOW: Forms, tables, admin → Minimal, solo cambios de border/color

### Restricciones importantes

- **Modifica archivos in-situ**. Evita crear nuevos archivos helper o abstracciones. Trabaja con el código existente porque reduce la complejidad del codebase.

- **Fat model pattern**. La lógica de negocio va en el modelo, no en las vistas. Las vistas solo coordinan.

- **Tokens CSS obligatorios**. Nunca hardcodear colores, spacing, o border-radius. Siempre usar `var(--token-name)`.

- **HTMX para interactividad**. Evitar JavaScript pesado. Usar `hx-*` attributes para dinamismo.

- **Implementa completamente**. Cuando llegues a la fase de implementación, escribe el código completo que puedo copiar y ejecutar.

### Paleta de colores (referencia rápida)

```css
/* Brand */
var(--brand-base)     /* Gator green #3C9E5D */
var(--brand-strong)   /* Gator dark #277947 */

/* Surfaces */
var(--bg)             /* Jungle darkest */
var(--surface-1)      /* Elevation 1 */
var(--surface-2)      /* Elevation 2 */

/* Text */
var(--fg)             /* Primary text */
var(--fg-muted)       /* Secondary text */

/* Accents */
var(--sand-500)       /* Gold (Luks brand, ratings) */
var(--crimson-primary)/* Red (Buddy brand, errors) */
```

### Criterio de éxito

[Define qué significa "terminado" para esta feature]

- [ ] Modelo creado con migrations
- [ ] Vistas/endpoints funcionando
- [ ] Templates renderizando correctamente
- [ ] CSS usando tokens del sistema
- [ ] HTMX para interactividad
- [ ] Responsive (mobile-first)
- [ ] Accesibilidad básica (aria-labels, contraste)

---

## Checklist para el desarrollador

- [ ] Leer `CROODY_CONTEXT.md` para contexto técnico
- [ ] Verificar `tokens.css` para colores/spacing disponibles
- [ ] Usar `python manage.py check --deploy` después de cambios
- [ ] Ejecutar `pytest` para verificar que no rompe nada
- [ ] Si tocas CSS, verificar compliance con Sacred Geometry

---

## Notas para el desarrollo

- Usa ORM de Django siempre, nunca SQL raw porque previene injection.
- Verifica visualmente el resultado porque el design system requiere validación visual.
- Si encuentras código relacionado que podría "mejorarse", resiste la tentación. Solo toca lo necesario para esta feature.
- Documenta decisiones técnicas en el PR description.
