# Componente Card - Documentación Completa

## Resumen
El sistema de cards de Croody implementa contenedores flexibles y accesibles para organizar contenido. Basado en **tokens CSS** y principios de **Geometría Sagrada**, ofrece múltiples variantes con estados interactivos, elevación dinámica y diseño responsivo.

## Ubicación
- **CSS Base**: `/proyecto_integrado/Croody/static/css/base.css`
- **Componentes**: `/proyecto_integrado/Croody/static/css/components.css` (líneas 42-207)
- **Tokens**: `/proyecto_integrado/Croody/static/css/tokens.css`

## Arquitectura del Sistema de Cards

### Estructura Base
```
┌────────────────────────────────────────┐
│ Card Container                          │
│ ┌────────────────────────────────────┐ │
│ │ Header (Opcional)                   │ │
│ │ ┌────────────────────────────────┐ │ │
│ │ │ Title / Icon                   │ │ │
│ │ └────────────────────────────────┘ │ │
│ ├────────────────────────────────────┤ │
│ │ Content                             │ │
│ │ ┌────────────────────────────────┐ │ │
│ │ │ Body Text / Media              │ │ │
│ │ │ ┌────────────────────────────┐ │ │ │
│ │ │ │ Image / Video / Chart      │ │ │ │
│ │ │ └────────────────────────────┘ │ │ │
│ │ └────────────────────────────────┘ │ │
│ ├────────────────────────────────────┤ │
│ │ Footer (Opcional)                   │ │
│ │ ┌────────────────────────────────┐ │ │
│ │ │ Actions / Meta / Tags          │ │ │
│ │ └────────────────────────────────┘ │ │
│ └────────────────────────────────────┘ │
└────────────────────────────────────────┘
```

### Card Base
```css
.card {
  background: var(--surface-1);
  padding: var(--space-3);
  border-radius: 20px;
  border: 1px solid color-mix(in oklab, var(--brand-base), transparent 85%);
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
```

**Características**:
- Padding: 21px (var(--space-3))
- Border radius: 20px
- Border: 1px con brand color al 15% opacidad
- Sombra sutil
- Layout flex column con gap de 13px

## Tipos de Cards

### 1. Product Card

**Uso**: Catálogo de productos, listados de items, showcases

```css
.product-card,
.product-card-ultra {
  transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1),
              border-color 200ms ease;
}

.product-card:hover,
.product-card-ultra:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: var(--shadow-lg);
  border-color: color-mix(in oklab, var(--brand-base), transparent 50%);
}

.product-card:active,
.product-card-ultra:active {
  transform: translateY(-2px) scale(1.005);
  transition-duration: 100ms;
}
```

#### Product Card Ultra (Versión Extendida)
```css
.product-card-ultra {
  background: var(--surface-1);
  border-radius: 24px;
  padding: var(--space-3);
  border: 2px solid color-mix(in oklab, var(--brand-base), transparent 85%);
  display: flex;
  flex-direction: column;
}

.product-card-ultra:hover {
  transform: translateY(-8px);
  border-color: var(--brand-base);
  box-shadow: 0 20px 40px color-mix(in oklab, var(--brand-base), transparent 85%);
}
```

**Estructura del Producto**:
```html
<article class="product-card-ultra">
  <!-- Imagen con gradiente -->
  <div class="product-image">
    <div class="product-badge">
      <span class="chip">Nuevo</span>
    </div>
    <div class="product-emoji">📦</div>
  </div>

  <!-- Contenido -->
  <h3 class="product-title">Cofre Premium</h3>
  <p class="product-teaser">
    Descripción del producto con sus características principales
  </p>

  <!-- Footer con precio y acciones -->
  <div class="product-footer">
    <div>
      <div class="product-price">€29.99</div>
      <div class="product-delivery">Entrega en 3-5 días</div>
    </div>
  </div>

  <!-- Botón de acción -->
  <button class="btn btn--primary add-to-cart-btn">
    Añadir al Carrito
  </button>
</article>
```

**Elementos Detallados**:

#### Product Image
```css
.product-image {
  background: linear-gradient(
    135deg,
    var(--brand-base) 0%,
    color-mix(in oklab, var(--brand-base), white 30%) 100%
  );
  border-radius: 18px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-3);
  position: relative;
  overflow: hidden;
}

.product-emoji {
  font-size: 6rem;
  filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.3));
  z-index: 1;
}
```

#### Product Badge
```css
.product-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 2;
}

.product-badge .chip {
  background: var(--brand-soft);
  color: var(--on-brand);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}
```

#### Product Footer
```css
.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}

.product-price {
  font-size: 2rem;
  font-weight: 800;
  color: var(--brand-base);
}

.product-delivery {
  font-size: 0.9rem;
  color: var(--fg-muted);
}
```

### 2. Vector Card

**Uso**: Representación de productos Buddy, Luks, Comida Real

```html
<article class="vector-card card">
  <header class="vector-card__header">
    <h3 class="vector-card__title">Buddy</h3>
    <span class="vector-card__icon">🤖</span>
  </header>

  <p class="vector-card__description">
    Tu entrenador personal AI que te ayuda a alcanzar tus metas de fitness
  </p>

  <div class="vector-card__keywords">
    #AI #Fitness #Personalizado
  </div>

  <footer class="vector-card__actions">
    <a href="/buddy" class="btn btn--ghost">Explorar</a>
  </footer>
</article>
```

**CSS específico**:
```css
.vector-card__keywords {
  font-size: 0.9rem;
  color: var(--brand-base);
  margin-top: 8px;
  font-style: italic;
  opacity: 0.9;
  font-weight: 500;
  letter-spacing: 0.01em;
}
```

### 3. Story Card (User Testimonials)

**Uso**: Testimonios de usuarios, casos de éxito, quotes

```html
<article class="story-card">
  <div class="story-card__avatar">👤</div>
  <blockquote>
    "Esta plataforma ha transformado completamente mi rutina de ejercicio.
    La IA de Buddy es increíblemente precisa."
  </blockquote>
  <div class="story-card__meta">
    <strong>María García</strong>
    <span>Usuaria desde 2024</span>
  </div>
</article>
```

**CSS**:
```css
.story-card {
  background: var(--surface-1);
  padding: var(--space-3);
  border-radius: 18px;
  border: 1px solid color-mix(in oklab, var(--brand-base), transparent 80%);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.story-card__avatar {
  font-size: 3rem;
  line-height: 1;
  text-align: center;
}

.story-card blockquote {
  margin: 0;
  font-size: 1.05rem;
  line-height: 1.6;
  color: var(--fg);
  font-style: italic;
}

.story-card__meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: auto;
}

.story-card__meta strong {
  color: var(--fg);
  font-size: 1rem;
}

.story-card__meta span {
  font-size: 0.9rem;
  color: var(--fg-tertiary);
}
```

### 4. Demo Step Card

**Uso**: Guías paso a paso, tutoriales, onboarding

```html
<div class="demo-step">
  <div class="demo-step__number">1</div>
  <h3>Configurar Perfil</h3>
  <p>Completa tu información personal y objetivos</p>
</div>
```

**CSS**:
```css
.demo-step {
  background: var(--surface-1);
  padding: var(--space-3);
  border-radius: 20px;
  border: 1px solid color-mix(in oklab, var(--brand-base), transparent 80%);
  text-align: center;
  position: relative;
}

.demo-step__number {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--brand-base);
  color: var(--on-brand);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 auto var(--space-3);
}

.demo-step h3 {
  margin: var(--space-2) 0;
}

.demo-step p {
  color: var(--fg-tertiary);
}
```

### 5. Account Shell Card

**Uso**: Dashboard de usuario, métricas, configuración

```html
<div class="account-shell">
  <div class="account-shell__intro">
    <h2>Bienvenido, Usuario</h2>
    <p>Gestiona tu cuenta y preferencias</p>
  </div>

  <div class="account-shell__grid">
    <div class="card">
      <h3>Métricas</h3>
      <dl class="account-metrics">
        <dt>Sesiones</dt>
        <dd>24</dd>
        <dt>Rutinas</dt>
        <dd>12</dd>
      </dl>
    </div>

    <div class="card">
      <h3>Token de API</h3>
      <div class="token-value">abc123...</div>
      <button class="btn btn--ghost btn--sm">Regenerar</button>
    </div>
  </div>
</div>
```

**CSS específico**:
```css
.account-shell__intro {
  padding: var(--space-4);
  border-radius: 24px;
  background: var(--surface-1);
  box-shadow: var(--shadow);
}

.account-metrics {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
  margin: var(--space-3) 0 0;
  padding: 0;
}

.account-metrics dt {
  font-size: 0.85rem;
  color: var(--fg-tertiary);
}

.account-metrics dd {
  font-size: 1.8rem;
  margin: 0;
  font-weight: 600;
}

.token-value {
  font-family: "Baloo 2", "Josefin Sans", sans-serif;
  font-size: 1.2rem;
  letter-spacing: 0.08em;
  background: color-mix(in oklab, var(--brand-base), transparent 90%);
  padding: var(--space-2);
  border-radius: 16px;
}
```

### 6. Telemetry Stream Card

**Uso**: Datos en tiempo real, monitoreo, dashboards

```html
<article class="telemetry-card">
  <header>
    <h4>Robot Position</h4>
    <span class="status online">🟢</span>
  </header>

  <div class="telemetry-data">
    <div class="data-point">
      <label>X:</label>
      <span>40.7128</span>
    </div>
    <div class="data-point">
      <label>Y:</label>
      <span>-74.0060</span>
    </div>
    <div class="data-point">
      <label>Temp:</label>
      <span>23.5°C</span>
    </div>
  </div>
</article>
```

**CSS**:
```css
.telemetry-stream article {
  border: 1px solid color-mix(in oklab, var(--brand-base), transparent 80%);
  border-radius: 16px;
  padding: var(--space-2);
  background: color-mix(in oklab, var(--surface-1), transparent 0%);
}

.telemetry-stream header {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: var(--fg-tertiary);
  margin-bottom: var(--space-2);
}

.data-point {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid color-mix(in oklab, var(--brand-base), transparent 90%);
}

.data-point:last-child {
  border-bottom: none;
}

.status.online {
  color: var(--gator-500);
}
```

## Estados Interactivos

### Hover State
```css
.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: color-mix(in oklab, var(--brand-base), transparent 50%);
}
```

### Active State
```css
.card:active {
  transform: translateY(-2px);
  transition-duration: 100ms;
}
```

### Focus State
```css
.card:focus-within,
.card:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 3px;
}
```

## Layouts de Card

### Grid de Cards
```css
.product-grid-ultra {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-4);
  margin-top: var(--space-4);
}
```

### Masonry Layout (CSS Grid)
```css
.card-masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  grid-auto-rows: max-content;
  gap: var(--space-3);
}

.card-masonry .card:nth-child(2n) {
  grid-row-end: span 2;
}
```

### Cards en Columnas
```css
.card-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.card-list .card {
  width: 100%;
}
```

## Responsive Design

### Mobile (≤ 767px)
```css
@media (max-width: 767.98px) {
  .product-grid-ultra {
    grid-template-columns: 1fr !important;
  }

  .product-card-ultra {
    max-width: 100%;
    overflow: hidden;
  }

  .story-card__avatar {
    font-size: 2.5rem;
  }

  .demo-step__number {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }
}
```

### Tablet (768px - 1023px)
```css
@media (min-width: 768px) and (max-width: 1023.98px) {
  .product-grid-ultra {
    grid-template-columns: repeat(2, 1fr);
  }

  .story-card {
    padding: var(--space-2);
  }
}
```

## Media y Contenido

### Card con Imagen
```html
<article class="card card--media">
  <div class="card__media">
    <img src="image.jpg" alt="Descripción">
  </div>
  <div class="card__content">
    <h3>Título</h3>
    <p>Contenido...</p>
  </div>
</article>
```

**CSS**:
```css
.card__media {
  margin: calc(-1 * var(--space-3));
  margin-bottom: var(--space-3);
  border-radius: 20px 20px 0 0;
  overflow: hidden;
}

.card__media img {
  width: 100%;
  height: auto;
  display: block;
}
```

### Card con Video
```html
<article class="card card--video">
  <div class="card__video">
    <video controls>
      <source src="video.mp4" type="video/mp4">
    </video>
  </div>
  <div class="card__content">
    <h3>Video Tutorial</h3>
  </div>
</article>
```

**CSS**:
```css
.card__video {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
  height: 0;
  overflow: hidden;
  border-radius: 16px;
  margin-bottom: var(--space-2);
}

.card__video video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
```

## Acciones y Footer

### Footer con Acciones
```html
<footer class="card__footer">
  <div class="card__actions">
    <button class="btn btn--ghost btn--sm">Cancelar</button>
    <button class="btn btn--primary btn--sm">Confirmar</button>
  </div>
</footer>
```

**CSS**:
```css
.card__footer {
  margin-top: var(--space-2);
  padding-top: var(--space-2);
  border-top: 1px solid color-mix(in oklab, var(--brand-base), transparent 85%);
}

.card__actions {
  display: flex;
  gap: var(--space-2);
  justify-content: flex-end;
}
```

### Meta Information
```html
<div class="card__meta">
  <span class="meta-item">
    <span class="icon">👁️</span>
    <span>1.2k vistas</span>
  </span>
  <span class="meta-item">
    <span class="icon">❤️</span>
    <span>156 likes</span>
  </span>
</div>
```

**CSS**:
```css
.card__meta {
  display: flex;
  gap: var(--space-2);
  font-size: 0.85rem;
  color: var(--fg-muted);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-item .icon {
  font-size: 1rem;
}
```

## Badges y Labels

### Badge Posicionado
```css
.card__badge {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 2;
}

.badge {
  background: var(--brand-base);
  color: var(--on-brand);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge--success {
  background: var(--gator-500);
}

.badge--warning {
  background: var(--warn-500);
  color: var(--jungle-900);
}

.badge--error {
  background: var(--error-500);
}
```

### Chip Labels
```css
.product-card__variants {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.product-card__variants .chip {
  height: 34px;
  padding: 0 13px;
}
```

## Efectos Visuales

### Glow Effect
```css
.card--glow {
  box-shadow: 0 0 0 6px color-mix(in oklab, var(--brand-base), transparent 92%);
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    box-shadow: 0 0 0 6px color-mix(in oklab, var(--brand-base), transparent 92%);
  }
  to {
    box-shadow: 0 0 20px 6px color-mix(in oklab, var(--brand-base), transparent 85%);
  }
}
```

### Gradient Border
```css
.card--gradient-border {
  position: relative;
  background: var(--surface-1);
  border-radius: 20px;
  padding: 2px;
}

.card--gradient-border::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 2px;
  background: linear-gradient(135deg, var(--brand-base), var(--brand-strong));
  border-radius: inherit;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  -webkit-mask-composite: xor;
}
```

### Glass Morphism
```css
.card--glass {
  background: color-mix(in oklab, var(--surface-1) 60%, transparent);
  backdrop-filter: blur(20px);
  border: 1px solid color-mix(in oklab, white 10%, transparent);
}
```

## Variantes Especiales

### Card Anidada (Nested)
```html
<div class="card card--outer">
  <h3>Card Padre</h3>
  <div class="card card--inner">
    <p>Card Hija</p>
  </div>
</div>
```

**CSS**:
```css
.card--outer {
  background: var(--surface-1);
}

.card--inner {
  background: var(--surface-2);
  border-color: color-mix(in oklab, var(--brand-base), transparent 90%);
}
```

### Card Expandible
```html
<article class="card card--expandable">
  <header class="card__header" tabindex="0" role="button">
    <h3>Ver más detalles</h3>
    <span class="expand-icon">▼</span>
  </header>
  <div class="card__content" hidden>
    <p>Contenido expandible...</p>
  </div>
</article>
```

**CSS**:
```css
.card--expandable .expand-icon {
  transition: transform 233ms ease;
}

.card--expandable.expanded .expand-icon {
  transform: rotate(180deg);
}

.card__content[hidden] {
  display: none;
}
```

**JavaScript**:
```javascript
document.querySelectorAll('.card--expandable').forEach(card => {
  const header = card.querySelector('.card__header');
  const content = card.querySelector('.card__content');

  header.addEventListener('click', () => {
    card.classList.toggle('expanded');
    if (content.hasAttribute('hidden')) {
      content.removeAttribute('hidden');
    } else {
      content.setAttribute('hidden', '');
    }
  });
});
```

## Loading States

### Skeleton Loader
```html
<article class="card card--loading">
  <div class="skeleton skeleton--image"></div>
  <div class="skeleton skeleton--title"></div>
  <div class="skeleton skeleton--text"></div>
  <div class="skeleton skeleton--text short"></div>
</article>
```

**CSS**:
```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--surface-2) 25%,
    color-mix(in oklab, var(--brand-base), transparent 90%) 37%,
    var(--surface-2) 63%
  );
  background-size: 400% 100%;
  animation: skeleton-loading 1.4s ease infinite;
  border-radius: 8px;
}

.skeleton--image {
  height: 200px;
  margin-bottom: var(--space-2);
  border-radius: 16px;
}

.skeleton--title {
  height: 24px;
  width: 60%;
  margin-bottom: var(--space-2);
}

.skeleton--text {
  height: 16px;
  width: 100%;
  margin-bottom: var(--space-1);
}

.skeleton--text.short {
  width: 80%;
}

@keyframes skeleton-loading {
  0% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0 50%;
  }
}
```

## Accesibilidad

### Estructura Semántica
```html
<article class="card" aria-labelledby="card-title-1">
  <header>
    <h3 id="card-title-1">Título de la Card</h3>
  </header>
  <section>
    <p>Contenido principal</p>
  </section>
  <footer>
    <button class="btn">Acción</button>
  </footer>
</article>
```

### ARIA Labels
```html
<!-- Card con descripción completa -->
<article class="card" aria-describedby="card-desc-1">
  <h3>Producto Premium</h3>
  <p id="card-desc-1">
    Descripción detallada del producto con características y beneficios
  </p>
</article>

<!-- Card interactiva -->
<article class="card" role="button" tabindex="0" aria-label="Abrir detalles del producto">
  <h3>Producto</h3>
</article>
```

### Focus Management
```css
.card[role="button"] {
  cursor: pointer;
}

.card[role="button"]:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 3px;
}
```

## Testing

### Unit Tests
```javascript
describe('Card Component', () => {
  test('renders with correct structure', () => {
    const card = render(
      <article className="card">
        <h3>Título</h3>
        <p>Contenido</p>
      </article>
    );

    expect(card.querySelector('h3')).toBeInTheDocument();
    expect(card.querySelector('p')).toBeInTheDocument();
  });

  test('applies hover effect', () => {
    const card = render(<article className="card">Content</article>);
    fireEvent.mouseEnter(card);
    // Verificar transform o box-shadow
    expect(card).toHaveClass('hovered');
  });

  test('supports custom padding', () => {
    const card = render(
      <article className="card card--compact">Content</article>
    );
    expect(card).toHaveClass('card--compact');
  });
});
```

### Visual Tests
```javascript
describe('Card Visual Tests', () => {
  it('renders all card variants', () => {
    cy.visit('/components/cards');

    // Product card
    cy.get('[data-testid="product-card"]').should('be.visible');

    // Story card
    cy.get('[data-testid="story-card"]').should('be.visible');

    // Demo step card
    cy.get('[data-testid="demo-step"]').should('be.visible');

    cy.percySnapshot('Card Variants');
  });

  it('shows hover state', () => {
    cy.get('[data-testid="product-card"]')
      .trigger('mouseover');
    cy.percySnapshot('Card Hover State');
  });
});
```

## JavaScript Integration

### Card Selection
```javascript
// Seleccionar cards
const cards = document.querySelectorAll('.card');

// Toggle selection
cards.forEach(card => {
  card.addEventListener('click', () => {
    card.classList.toggle('card--selected');
    const selected = card.classList.contains('card--selected');

    card.setAttribute('aria-pressed', selected);
    card.setAttribute('aria-selected', selected);
  });
});
```

### Lazy Loading Images
```javascript
// Intersection Observer para lazy loading
const imageCards = document.querySelectorAll('.card[data-lazy]');

const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target.querySelector('img');
      if (img.dataset.src) {
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
      }
      imageObserver.unobserve(entry.target);
    }
  });
});

imageCards.forEach(card => imageObserver.observe(card));
```

### Expand/Collapse
```javascript
function initExpandableCards() {
  document.querySelectorAll('.card--expandable').forEach(card => {
    const header = card.querySelector('.card__header');
    const content = card.querySelector('.card__content');

    function toggle() {
      const isExpanded = card.classList.contains('expanded');

      if (isExpanded) {
        card.classList.remove('expanded');
        content.hidden = true;
        header.setAttribute('aria-expanded', 'false');
      } else {
        card.classList.add('expanded');
        content.hidden = false;
        header.setAttribute('aria-expanded', 'true');
      }
    }

    header.addEventListener('click', toggle);
    header.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggle();
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', initExpandableCards);
```

## Buenas Prácticas

### ✅ Hacer
```html
<!-- Usar estructura semántica -->
<article class="card" aria-labelledby="title-1">
  <header>
    <h3 id="title-1">Título</h3>
  </header>
  <section>
    <p>Contenido</p>
  </section>
  <footer>
    <button class="btn">Acción</button>
  </footer>
</article>

<!-- Proporcionar alt text para imágenes -->
<div class="card__media">
  <img src="product.jpg" alt="Producto premium azul con acabados dorados">
</div>

<!-- Usar tokens CSS -->
<div class="card" style="padding: var(--space-3);">
  Contenido
</div>

<!-- Mantener proporción de imágenes -->
<div class="card__media">
  <img src="image.jpg" alt="Descripción" style="aspect-ratio: 16/9;">
</div>
```

### ❌ Evitar
```html
<!-- No usar div para contenido semántico -->
<div class="card">
  <h3>Título</h3>
  <div>Contenido</div>  <!-- Usar <p> o <section> -->
</div>

<!-- No omitir alt text -->
<img src="product.jpg">  <!-- Alt requerido -->

<!-- No usar px hardcoded -->
<div style="padding: 21px;">  <!-- Usar var(--space-3) -->

<!-- No imágenes sin contenedor -->
<img src="image.jpg" style="width: 100%;">
<!-- Usar: <div class="card__media"><img></div> -->
```

## Casos de Uso

### 1. Product Grid
```html
<section class="product-showcase">
  <div class="landing-blueprint__cards">
    <div class="product-grid-ultra">
      <!-- 12 productos en grid responsivo -->
      <article class="product-card-ultra">
        <!-- Product card content -->
      </article>
    </div>
  </div>
</section>
```

### 2. User Stories Carousel
```html
<section class="user-stories">
  <h2>Lo que dicen nuestros usuarios</h2>
  <div class="stories-grid">
    <!-- 3-6 story cards -->
    <article class="story-card">
      <!-- Story content -->
    </article>
  </div>
</section>
```

### 3. Dashboard Metrics
```html
<section class="account-dashboard">
  <div class="account-shell__grid">
    <!-- Métricas principales -->
    <div class="card">
      <h3>Actividad</h3>
      <div class="account-metrics">
        <div class="metric">
          <dt>Sesiones</dt>
          <dd>24</dd>
        </div>
      </div>
    </div>

    <!-- Token management -->
    <div class="card">
      <h3>API Token</h3>
      <div class="token-value">••••••••</div>
      <button class="btn btn--ghost btn--sm">Regenerar</button>
    </div>

    <!-- Activity list -->
    <div class="card card--wide">
      <h3>Actividad Reciente</h3>
      <ul class="activity-list">
        <li>Login desde Chrome</li>
        <li>Token regenerado</li>
      </ul>
    </div>
  </div>
</section>
```

## Referencias

### Archivos Relacionados
- `static/css/base.css` - Estilos base y tipografía
- `static/css/components.css` - Todas las variantes de cards
- `static/css/tokens.css` - Variables de espaciado y colores
- `static/js/theme.js` - Cambio de tema dinámico

### Documentación Externa
- [Card Pattern - WAI-ARIA](https://www.w3.org/WAI/ARIA/apg/patterns/card/)
- [Material Design - Cards](https://material.io/design/components/cards.html)
- [CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)

## Ver También
- [Botones](./botones.md)
- [Formularios](./formularios.md)
- [Modals](./modals.md)
- [Design System - Tokens](../design-system/tokens.md)
- [Design System - Colores](../design-system/colores.md)
