# Componente Botón - Documentación Completa

## Resumen
El sistema de botones de Croody implementa un diseño consistente basado en **principios de accesibilidad** y **tokens CSS**. Soporta múltiples variantes, tamaños y estados con transiciones suaves y feedback visual inmediato.

## Ubicación
- **CSS Base**: `/proyecto_integrado/Croody/static/css/base.css` (líneas 90-97)
- **Componentes**: `/proyecto_integrado/Croody/static/css/components.css`
- **Tokens**: `/proyecto_integrado/Croody/static/css/tokens.css`

## Anatomía del Botón

### Estructura Base
```css
.btn {
  /* Layout */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 13px;  /* var(--space-2) */

  /* Dimensiones */
  height: 55px;  /* Altura estándar */
  padding: 0 21px;  /* var(--space-4) */

  /* Visuales */
  border-radius: 18px;  /* var(--radius-3) */
  border: 1.5px solid color-mix(in oklab, var(--brand-base), transparent 65%);

  /* Transiciones */
  transition: box-shadow 200ms ease,
              transform 200ms ease,
              background 300ms ease;
}
```

### Anatomía Detallada
```
┌────────────────────────────────────────┐
│                                        │
│  [Icon]  Button Text          [Icon]   │  ← Padding: 21px
│                                        │
│              ↑                         │  ↑ Gap: 13px
│              55px                      │
│                                        │
└────────────────────────────────────────┘
                  ↑
            Border radius: 18px
```

## Variantes de Botón

### 1. Botón Primario

**Uso**: Acciones principales, CTAs críticos, formularios de envío

```css
.btn--primary {
  background-image: linear-gradient(33deg, var(--brand-strong), var(--brand-base));
  color: var(--on-brand);
  box-shadow: var(--shadow);
}

.btn--primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-strong);
}

.btn--primary:active {
  transform: translateY(0);
  box-shadow: var(--shadow-strong);
}
```

**Ejemplo de uso**:
```html
<button class="btn btn--primary">
  <span>Comprar Ahora</span>
</button>

<!-- Con iconos -->
<button class="btn btn--primary">
  <span class="icon">🛒</span>
  <span>Añadir al Carrito</span>
</button>
```

**Estados**:
- **Default**: Gradiente de marca, sombra sutil
- **Hover**: Translación -2px, sombra profunda
- **Active**: Translación 0, sombra profunda
- **Focus**: Outline de 2px con `--focus-ring`

### 2. Botón Ghost

**Uso**: Acciones secundarias, botones de navegación, CTAs sutiles

```css
.btn--ghost {
  background: transparent;
  color: var(--fg);
  border-color: color-mix(in oklab, var(--brand-base), transparent 50%);
}

.btn--ghost:hover {
  background: color-mix(in oklab, var(--brand-base), transparent 90%);
  border-color: var(--brand-base);
}
```

**Ejemplo de uso**:
```html
<button class="btn btn--ghost">
  <span>Cancelar</span>
</button>

<!-- Versión outline -->
<button class="btn btn--ghost">
  <span class="icon">↩️</span>
  <span>Volver</span>
</button>
```

### 3. Botón de Texto (Text Button)

**Uso**: Enlaces con apariencia de botón, acciones menos prominentes

```html
<a href="/action" class="btn btn--text">
  Más información
</a>
```

**CSS personalizado**:
```css
.btn--text {
  height: auto;
  padding: 0;
  border: none;
  background: transparent;
  color: var(--brand-base);
  font-weight: 500;
  text-decoration: underline;
}

.btn--text:hover {
  color: var(--brand-strong);
  transform: none;
  box-shadow: none;
}
```

### 4. Botón Icon Only

**Uso**: Acciones contextuales, toolbars, menús

```html
<button class="btn btn--icon-only" aria-label="Cerrar">
  <span class="icon">✕</span>
</button>
```

**CSS personalizado**:
```css
.btn--icon-only {
  width: 44px;
  height: 44px;
  padding: 0;
  border-radius: 50%;
}
```

## Tamaños de Botón

### Large (Default)
```css
.btn {
  height: 55px;
  padding: 0 21px;
  font-size: var(--text-base);
}
```

### Medium
```css
.btn--md {
  height: 44px;
  padding: 0 16px;
  font-size: var(--text-sm);
}
```

### Small
```css
.btn--sm {
  height: 34px;
  padding: 0 12px;
  font-size: var(--text-xs);
  border-radius: 12px;
}
```

**Ejemplo de uso**:
```html
<!-- Large -->
<button class="btn btn--primary btn--lg">Comprar</button>

<!-- Medium -->
<button class="btn btn--primary btn--md">Aplicar</button>

<!-- Small -->
<button class="btn btn--ghost btn--sm">Eliminar</button>
```

## Estados Interactivos

### 1. Disabled
```css
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
  background: var(--jungle-700);
  color: var(--jungle-400);
  box-shadow: none;
}
```

**Ejemplo de uso**:
```html
<button class="btn btn--primary" disabled>
  Procesando...
</button>
```

### 2. Loading
```html
<button class="btn btn--primary" disabled>
  <span class="spinner"></span>
  <span>Procesando...</span>
</button>
```

**CSS del spinner**:
```css
.spinner {
  width: 1em;
  height: 1em;
  border: 2px solid var(--on-brand);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### 3. Loading con Overlay
```html
<div class="btn-wrapper">
  <button class="btn btn--primary">Enviar</button>
  <div class="btn-overlay">
    <div class="spinner"></div>
  </div>
</div>
```

**CSS**:
```css
.btn-wrapper {
  position: relative;
  display: inline-block;
}

.btn-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
}
```

## Botones de Icono

### Icon Only
```html
<button class="btn btn--icon-only" aria-label="Eliminar">
  <span class="icon">🗑️</span>
</button>
```

### Icon + Texto
```html
<button class="btn btn--icon-text">
  <span class="icon">💾</span>
  <span>Guardar</span>
</button>
```

**CSS**:
```css
.btn--icon-text .icon {
  font-size: 1.2em;
  line-height: 1;
}
```

### Icono a la Derecha
```html
<button class="btn btn--primary">
  <span>Siguiente</span>
  <span class="icon">➡️</span>
</button>
```

## Variantes por Color

### Botón de Éxito
```css
.btn--success {
  background: linear-gradient(33deg, var(--gator-600), var(--gator-500));
  color: white;
  border-color: var(--gator-500);
}
```

### Botón de Advertencia
```css
.btn--warning {
  background: linear-gradient(33deg, var(--warn-600), var(--warn-500));
  color: var(--jungle-900);
  border-color: var(--warn-500);
}
```

### Botón de Error
```css
.btn--error {
  background: linear-gradient(33deg, var(--error-600), var(--error-500));
  color: white;
  border-color: var(--error-500);
}
```

**Ejemplo de uso**:
```html
<button class="btn btn--success">✓ Completado</button>
<button class="btn btn--warning">⚠️ Atención</button>
<button class="btn btn--error">✕ Error</button>
```

## Botones por Contexto

### Header Actions
```css
.header-actions .btn {
  height: 44px;
  padding: 0 16px;
  font-size: var(--text-sm);
}
```

**HTML**:
```html
<div class="header-actions">
  <button class="btn btn--primary btn--sm">Acceder</button>
</div>
```

### Hero Section
```css
.hero-cta .btn {
  min-width: 180px;
  height: 60px;
}
```

**HTML**:
```html
<div class="hero-cta">
  <button class="btn btn--primary btn--lg">
    Comenzar Gratis
  </button>
  <button class="btn btn--ghost btn--lg">
    Ver Demo
  </button>
</div>
```

### Formularios
```css
.form-actions {
  display: flex;
  gap: var(--space-2);
  margin-top: var(--space-3);
}

.form-actions .btn {
  flex: 1;
}
```

**HTML**:
```html
<form class="form">
  <!-- Campos del formulario -->
  <div class="form-actions">
    <button type="button" class="btn btn--ghost">Cancelar</button>
    <button type="submit" class="btn btn--primary">Enviar</button>
  </div>
</form>
```

### Modal/Dialog
```css
.modal__actions {
  display: flex;
  gap: var(--space-2);
  justify-content: flex-end;
  margin-top: var(--space-3);
}
```

**HTML**:
```html
<div class="modal__content">
  <div class="modal__body">
    <p>¿Estás seguro?</p>
  </div>
  <div class="modal__actions">
    <button class="btn btn--ghost">Cancelar</button>
    <button class="btn btn--error">Eliminar</button>
  </div>
</div>
```

## Responsive Design

### Mobile Optimizations
```css
@media (max-width: 767.98px) {
  /* Mejorar targets táctiles en móvil */
  .btn {
    min-height: 48px;
    padding: 0 24px;
  }

  /* Botones de icono más grandes */
  .btn--icon-only {
    width: 48px;
    height: 48px;
  }

  /* CTAs en hero más prominentes */
  .hero-cta .btn {
    width: 100%;
    min-height: 52px;
  }
}
```

### Touch Targets
**Tamaño mínimo recomendado**: 48px × 48px (WCAG 2.1 Level AAA)

```html
<!-- ✅ Correcto - Cumple WCAG -->
<button class="btn btn--primary" style="min-height: 48px; min-width: 48px;">
  ✓
</button>

<!-- ❌ Incorrecto - Muy pequeño -->
<button class="btn" style="width: 32px; height: 32px;">
  ✓
</button>
```

## Accesibilidad

### 1. Estados de Focus
```css
.btn:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 3px;
}
```

### 2. Atributos ARIA
```html
<!-- Botón con descripción -->
<button class="btn btn--primary" aria-describedby="help-text">
  Enviar
</button>
<div id="help-text" class="sr-only">
  Enviará el formulario y no se puede deshacer
</div>

<!-- Botón toggle -->
<button
  class="btn btn--ghost"
  aria-pressed="false"
  aria-label="Activar modo oscuro"
>
  🌙
</button>

<!-- Botón expandible -->
<button
  class="btn btn--ghost"
  aria-expanded="false"
  aria-controls="menu-content"
>
  Menú ▼
</button>
```

### 3. Contraste
**Cumplimiento WCAG 2.1**:
- **AA**: Ratio mínimo 4.5:1
- **AAA**: Ratio mínimo 7:1

```css
/* ✅ Botón primario - 15.3:1 sobre fondo */
.btn--primary {
  background: var(--brand-base);  /* #3C9E5D */
  color: white;                   /* 15.3:1 */
}

/* ❌ Evitar - Contraste insuficiente */
.btn--bad {
  background: #80D3A0;  /* Gator-300 */
  color: white;          /* Solo 2.8:1 - FALLA */
}
```

### 4. Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  .btn {
    transition: none;
  }

  .btn:hover {
    transform: none;
  }
}
```

## Animaciones

### Hover Effect
```css
.btn {
  transition: all var(--duration-base) var(--ease-base);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

### Active Effect
```css
.btn:active {
  transform: translateY(0);
  transition-duration: 100ms;
}
```

### Loading Effect
```css
.btn--loading {
  position: relative;
  color: transparent;
}

.btn--loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 1em;
  height: 1em;
  margin: -0.5em;
  border: 2px solid var(--on-brand);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
```

### Ripple Effect (Material Design)
```html
<button class="btn btn--primary">
  <span class="btn__text">Click Me</span>
  <span class="btn__ripple"></span>
</button>
```

```css
.btn {
  position: relative;
  overflow: hidden;
}

.btn__ripple {
  position: absolute;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: scale(0);
  animation: ripple 600ms ease-out;
}

@keyframes ripple {
  to {
    transform: scale(4);
    opacity: 0;
  }
}
```

## Grupo de Botones (Button Group)

### Horizontal
```html
<div class="btn-group" role="group">
  <button class="btn btn--ghost">Opción 1</button>
  <button class="btn btn--ghost">Opción 2</button>
  <button class="btn btn--ghost">Opción 3</button>
</div>
```

**CSS**:
```css
.btn-group {
  display: inline-flex;
  border-radius: 18px;
  overflow: hidden;
  border: 1.5px solid color-mix(in oklab, var(--brand-base), transparent 65%);
}

.btn-group .btn {
  border: none;
  border-right: 1px solid color-mix(in oklab, var(--brand-base), transparent 65%);
  border-radius: 0;
}

.btn-group .btn:last-child {
  border-right: none;
}
```

### Vertical
```html
<div class="btn-group-vertical" role="group">
  <button class="btn btn--ghost">Opción 1</button>
  <button class="btn btn--ghost">Opción 2</button>
  <button class="btn btn--ghost">Opción 3</button>
</div>
```

**CSS**:
```css
.btn-group-vertical {
  display: inline-flex;
  flex-direction: column;
  border-radius: 18px;
  overflow: hidden;
  border: 1.5px solid color-mix(in oklab, var(--brand-base), transparent 65%);
}

.btn-group-vertical .btn {
  border: none;
  border-bottom: 1px solid color-mix(in oklab, var(--brand-base), transparent 65%);
  border-radius: 0;
}

.btn-group-vertical .btn:last-child {
  border-bottom: none;
}
```

### Toggle Group
```html
<div class="btn-toggle" role="group" aria-label="Opciones">
  <button class="btn btn--ghost" aria-pressed="false">Opción 1</button>
  <button class="btn btn--ghost" aria-pressed="true">Opción 2</button>
  <button class="btn btn--ghost" aria-pressed="false">Opción 3</button>
</div>
```

**CSS**:
```css
.btn-toggle .btn[aria-pressed="true"] {
  background: var(--brand-base);
  color: var(--on-brand);
}
```

## Button Dropdown

### Implementación
```html
<div class="btn-dropdown">
  <button class="btn btn--primary" aria-expanded="false" aria-haspopup="true">
    Acciones <span class="icon">▼</span>
  </button>
  <div class="dropdown-menu" hidden>
    <a href="#" class="dropdown-item">Opción 1</a>
    <a href="#" class="dropdown-item">Opción 2</a>
    <div class="dropdown-divider"></div>
    <a href="#" class="dropdown-item">Opción 3</a>
  </div>
</div>
```

**CSS**:
```css
.btn-dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  background: var(--surface-1);
  border: 1px solid var(--border-1);
  border-radius: 12px;
  box-shadow: var(--shadow-lg);
  min-width: 200px;
  z-index: var(--z-dropdown);
}

.dropdown-item {
  display: block;
  padding: 12px 16px;
  color: var(--fg);
  transition: background 144ms ease;
}

.dropdown-item:hover {
  background: var(--surface-2);
}

.dropdown-divider {
  height: 1px;
  background: var(--border-1);
  margin: 8px 0;
}
```

## JavaScript Integration

### Toggle Button State
```javascript
// Toggle entre estados
function toggleButton(btn) {
  const pressed = btn.getAttribute('aria-pressed') === 'true';
  btn.setAttribute('aria-pressed', !pressed);
}

// Ejemplo de uso
document.querySelectorAll('[aria-pressed]').forEach(btn => {
  btn.addEventListener('click', () => toggleButton(btn));
});
```

### Loading State
```javascript
function setButtonLoading(btn, isLoading) {
  if (isLoading) {
    btn.classList.add('btn--loading');
    btn.disabled = true;
  } else {
    btn.classList.remove('btn--loading');
    btn.disabled = false;
  }
}

// Ejemplo de uso
document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', async (e) => {
    const submitBtn = form.querySelector('[type="submit"]');
    setButtonLoading(submitBtn, true);

    try {
      await fetch('/api/action', {
        method: 'POST',
        body: new FormData(form)
      });
    } finally {
      setButtonLoading(submitBtn, false);
    }
  });
});
```

### Confirm Dialog
```javascript
function confirmAction(button, message = '¿Estás seguro?') {
  if (confirm(message)) {
    // Acción confirmada
    const form = button.closest('form');
    if (form) form.submit();
    return true;
  }
  return false;
}

// Ejemplo de uso
<button
  class="btn btn--error"
  onclick="return confirmAction(this, '¿Eliminar permanentemente?')"
>
  Eliminar
</button>
```

### Ripple Effect
```javascript
function createRipple(event) {
  const button = event.currentTarget;
  const circle = document.createElement('span');
  const diameter = Math.max(button.clientWidth, button.clientHeight);
  const radius = diameter / 2;

  circle.style.width = circle.style.height = `${diameter}px`;
  circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
  circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
  circle.classList.add('btn__ripple');

  const ripple = button.querySelector('.btn__ripple');
  if (ripple) {
    ripple.remove();
  }

  button.appendChild(circle);
}

document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', createRipple);
});
```

## Testing

### Unit Tests (Jest/Vitest)
```javascript
describe('Button Component', () => {
  test('renders with correct classes', () => {
    const btn = render(
      <button className="btn btn--primary">Click Me</button>
    );
    expect(btn.classList.contains('btn')).toBe(true);
    expect(btn.classList.contains('btn--primary')).toBe(true);
  });

  test('applies disabled state', () => {
    const btn = render(
      <button className="btn" disabled>Click Me</button>
    );
    expect(btn.disabled).toBe(true);
  });

  test('handles click events', () => {
    const handleClick = vi.fn();
    const btn = render(
      <button className="btn" onClick={handleClick}>Click Me</button>
    );
    btn.click();
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('shows loading state', () => {
    const btn = render(
      <button className="btn btn--loading" disabled>Loading...</button>
    );
    expect(btn.classList.contains('btn--loading')).toBe(true);
    expect(btn.disabled).toBe(true);
  });
});
```

### Visual Regression Tests (Percy/Cypress)
```javascript
// Cypress test
describe('Button Visual Tests', () => {
  it('renders all button variants', () => {
    cy.visit('/components/buttons');

    // Primary button
    cy.get('[data-testid="btn-primary"]').should('be.visible');

    // Ghost button
    cy.get('[data-testid="btn-ghost"]').should('be.visible');

    // Hover state
    cy.get('[data-testid="btn-primary"]').trigger('mouseover');
    cy.percySnapshot('Button Primary Hover');

    // Disabled state
    cy.get('[data-testid="btn-disabled"]').should('be.disabled');
    cy.percySnapshot('Button Disabled');
  });
});
```

### Accessibility Tests
```javascript
// Axe test
describe('Button Accessibility', () => {
  test('meets WCAG color contrast requirements', () => {
    cy.visit('/components/buttons');
    cy.injectAxe();
    cy.checkA11y(null, {
      runOnly: {
        type: 'tag',
        values: ['wcag2aa']
      }
    });
  });

  test('has proper focus management', () => {
    cy.visit('/components/buttons');
    cy.get('[data-testid="btn-primary"]').focus();
    cy.focused().should('have.class', 'btn');

    // Verificar focus visible
    cy.focused().should('have.css', 'outline-width').and('not.equal', '0px');
  });
});
```

## Buenas Prácticas

### ✅ Hacer
```html
<!-- Usar button para acciones -->
<button class="btn btn--primary">Enviar</button>

<!-- Proporcionar aria-label para icon-only -->
<button class="btn btn--icon-only" aria-label="Cerrar">✕</button>

<!-- Usar disabled apropiadamente -->
<button class="btn btn--primary" disabled>Procesando...</button>

<!-- Mantener targets táctiles ≥ 48px -->
<button class="btn" style="min-height: 48px;">Click</button>

<!-- Usar type en formularios -->
<form>
  <button type="submit" class="btn btn--primary">Enviar</button>
  <button type="button" class="btn btn--ghost">Cancelar</button>
</form>
```

### ❌ Evitar
```html
<!-- No usar link como botón -->
<a href="/action" class="btn">Usar Botón</a>
<!-- ✅ Correcto: <button> para acciones -->

<!-- No omitir aria-label -->
<button class="btn btn--icon-only">?</button>
<!-- ✅ Correcto: aria-label="Ayuda" -->

<!-- No targets táctiles pequeños -->
<button class="btn" style="width: 32px; height: 32px;">+</button>
<!-- ✅ Correcto: min 48px -->

<!-- No forget type en formularios -->
<form>
  <button class="btn btn--primary">Enviar</button>
  <!-- ✅ Correcto: type="submit" -->
</form>

<!-- No estilos inline excesivos -->
<button class="btn" style="background: red; padding: 20px;">Bad</button>
<!-- ✅ Correcto: Usar clases CSS -->
```

## Casos de Uso

### 1. E-commerce - Add to Cart
```html
<div class="product-actions">
  <button class="btn btn--primary btn--lg add-to-cart" data-product-id="123">
    <span class="icon">🛒</span>
    <span>Añadir al Carrito</span>
  </button>
</div>

<script>
// Mostrar feedback
document.querySelector('.add-to-cart').addEventListener('click', async (e) => {
  const btn = e.currentTarget;
  const originalText = btn.innerHTML;

  // Estado de carga
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span><span>Añadiendo...</span>';

  try {
    await addToCart(btn.dataset.productId);
    btn.innerHTML = '<span>✓</span><span>Añadido</span>';

    // Mostrar toast
    showToast('Producto añadido al carrito');
  } catch (error) {
    btn.innerHTML = '<span>✕</span><span>Error</span>';
    showToast('Error al añadir al carrito', 'error');
  } finally {
    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = originalText;
    }, 2000);
  }
});
</script>
```

### 2. Form - Multi-step
```html
<form class="form-multi-step">
  <div class="step step-1 active">
    <h3>Paso 1: Información Personal</h3>
    <!-- Campos -->
    <div class="form-actions">
      <button type="button" class="btn btn--ghost" disabled>Anterior</button>
      <button type="button" class="btn btn--primary" data-next>Siguiente</button>
    </div>
  </div>

  <div class="step step-2">
    <h3>Paso 2: Información de Pago</h3>
    <!-- Campos -->
    <div class="form-actions">
      <button type="button" class="btn btn--ghost" data-prev>Anterior</button>
      <button type="submit" class="btn btn--primary">Finalizar</button>
    </div>
  </div>
</form>
```

### 3. Modal - Confirm Action
```html
<div class="modal" id="delete-modal">
  <div class="modal__content">
    <h3 class="modal__title">Confirmar Eliminación</h3>
    <p>Esta acción no se puede deshacer.</p>
    <div class="modal__actions">
      <button class="btn btn--ghost" data-dismiss>Cancelar</button>
      <button class="btn btn--error" id="confirm-delete">Eliminar</button>
    </div>
  </div>
</div>

<script>
// Abrir modal
function openDeleteModal(itemId) {
  const modal = document.getElementById('delete-modal');
  modal.classList.add('active');
  document.getElementById('confirm-delete').dataset.itemId = itemId;
}

// Cerrar modal
document.querySelectorAll('[data-dismiss]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.getElementById('delete-modal').classList.remove('active');
  });
});

// Confirmar eliminación
document.getElementById('confirm-delete').addEventListener('click', async (e) => {
  const btn = e.currentTarget;
  const itemId = btn.dataset.itemId;

  setButtonLoading(btn, true);

  try {
    await deleteItem(itemId);
    document.getElementById('delete-modal').classList.remove('active');
    showToast('Elemento eliminado', 'success');
  } catch (error) {
    showToast('Error al eliminar', 'error');
  } finally {
    setButtonLoading(btn, false);
  }
});
</script>
```

## Referencias

### Archivos Relacionados
- `static/css/base.css` - Estilos base de botones
- `static/css/components.css` - Componentes extendidos
- `static/css/tokens.css` - Tokens de color y espaciado
- `static/js/theme.js` - Cambio de tema dinámico

### Documentación Externa
- [WCAG 2.1 - Buttons](https://www.w3.org/WAI/WCAG21/Understanding/non-text-content.html)
- [Material Design - Buttons](https://material.io/design/components/buttons.html)
- [Button Pattern - A11y](https://www.w3.org/WAI/tutorials/forms/)

## Ver También
- [Cards](./cards.md)
- [Formularios](./formularios.md)
- [Modals & Dialogs](./modals.md)
- [Design System - Colores](../design-system/colores.md)
- [Design System - Tokens](../design-system/tokens.md)
