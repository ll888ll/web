# Language Selector - Documentación Completa

## Resumen
El selector de idiomas de Croody implementa un dropdown accesible con navegación por teclado, gestión de focus, estados ARIA apropiados y soporte para 8 idiomas (ES, EN, FR, PT, AR, ZH, JA, HI).

## Ubicación
`/proyecto_integrado/Croody/static/js/language-selector.js` (102 líneas)

## Arquitectura

### IIFE Pattern with Strict Mode
```javascript
(function() {
  'use strict';
  // Todo el código
})();
```

**Ventajas**:
- Previene variables globales accidentales
- Mejora performance (modo strict)
- Facilita minificación

### Initialization Strategy
```javascript
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
```

**Casos**:
- `loading`: DOM aún se está cargando → esperar `DOMContentLoaded`
- `interactive` o `complete`: DOM ya está listo → ejecutar inmediatamente

## Componentes Principales

### 1. Elements Query
```javascript
function init() {
  const selector = document.querySelector('.language-selector');
  if (!selector) return;

  const trigger = selector.querySelector('.language-selector__trigger');
  const dropdown = selector.querySelector('.language-selector__dropdown');

  if (!trigger || !dropdown) return;
  // ... inicialización
}
```

**Validaciones**:
1. Verifica existencia del selector principal
2. Verifica trigger y dropdown
3. Early return si no existen elementos

### 2. Dropdown Toggle

#### Open Function
```javascript
function openDropdown() {
  trigger.setAttribute('aria-expanded', 'true');
  dropdown.removeAttribute('hidden');

  // Focus en opción activa o primera disponible
  const activeOption = dropdown.querySelector('.language-selector__option.active');
  const firstOption = dropdown.querySelector('.language-selector__option');
  if (activeOption) {
    activeOption.focus();
  } else if (firstOption) {
    firstOption.focus();
  }
}
```

**Operaciones**:
1. Actualiza `aria-expanded="true"`
2. Quita atributo `hidden` (dropdown visible)
3. Focus en opción activa si existe
4. Fallback: focus en primera opción

#### Close Function
```javascript
function closeDropdown() {
  trigger.setAttribute('aria-expanded', 'false');
  dropdown.setAttribute('hidden', '');
}
```

**Operaciones**:
1. Actualiza `aria-expanded="false"`
2. Añade atributo `hidden` (dropdown oculto)
3. Return focus al trigger (automático del browser)

#### Click Event
```javascript
trigger.addEventListener('click', function(e) {
  e.stopPropagation();
  const isExpanded = trigger.getAttribute('aria-expanded') === 'true';

  if (isExpanded) {
    closeDropdown();
  } else {
    openDropdown();
  }
});
```

**Características**:
- `stopPropagation()`: Evita cerrar inmediatamente
- Toggle: abre si cerrado, cierra si abierto

### 3. Click Outside Handler

```javascript
document.addEventListener('click', function(e) {
  if (!selector.contains(e.target)) {
    closeDropdown();
  }
});
```

**Propósito**: Cierra dropdown cuando usuario hace click fuera del selector

**Lógica**:
1. Escucha clicks en todo el documento
2. Verifica si click está dentro del selector
3. Si está fuera → cerrar dropdown

### 4. Escape Key Handler

```javascript
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeDropdown();
    trigger.focus();
  }
});
```

**Comportamiento**:
1. Detecta tecla Escape
2. Cierra dropdown
3. Return focus al trigger

### 5. Keyboard Navigation

```javascript
dropdown.addEventListener('keydown', function(e) {
  const options = Array.from(dropdown.querySelectorAll('.language-selector__option'));
  const currentIndex = options.indexOf(document.activeElement);

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    const nextIndex = currentIndex < options.length - 1 ? currentIndex + 1 : 0;
    options[nextIndex].focus();
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    const prevIndex = currentIndex > 0 ? currentIndex - 1 : options.length - 1;
    options[prevIndex].focus();
  } else if (e.key === 'Home') {
    e.preventDefault();
    options[0].focus();
  } else if (e.key === 'End') {
    e.preventDefault();
    options[options.length - 1].focus();
  }
});
```

**Teclas Soportadas**:

| Tecla | Acción | Comportamiento |
|-------|--------|----------------|
| `ArrowDown` | Navegación | Va a siguiente opción (wrap around) |
| `ArrowUp` | Navegación | Va a opción anterior (wrap around) |
| `Home` | Navegación | Salta a primera opción |
| `End` | Navegación | Salta a última opción |
| `Escape` | Cerrar | Cierra dropdown y return focus |
| `Enter`/`Space` | Activación | Activa enlace (comportamiento por defecto) |

**Implementación**:
- `preventDefault()`: Previene scroll o focus default
- Wrap around: `ArrowDown` en última opción → primera
- Wrap around: `ArrowUp` en primera opción → última
- Dynamic index: Calcula índice actual del elemento activo

## HTML Structure

### Selector Base
```html
<div class="language-selector">
  <!-- Trigger Button -->
  <button
    class="language-selector__trigger"
    aria-expanded="false"
    aria-haspopup="listbox"
    aria-label="Seleccionar idioma"
  >
    <span class="language-selector__icon">🌐</span>
    <span class="language-selector__current">ES</span>
  </button>

  <!-- Dropdown -->
  <div class="language-selector__dropdown" hidden>
    <ul class="language-selector__list" role="listbox">
      <li role="none">
        <a
          href="/es/"
          class="language-selector__option active"
          role="option"
          aria-selected="true"
          lang="es"
        >
          <span class="language-selector__flag">🇪🇸</span>
          <span class="language-selector__name">Español</span>
        </a>
      </li>

      <li role="none">
        <a
          href="/en/"
          class="language-selector__option"
          role="option"
          aria-selected="false"
          lang="en"
        >
          <span class="language-selector__flag">🇺🇸</span>
          <span class="language-selector__name">English</span>
        </a>
      </li>

      <!-- Más idiomas... -->
    </ul>
  </div>
</div>
```

### ARIA Attributes

| Elemento | Atributo | Valor | Propósito |
|----------|----------|-------|-----------|
| Trigger | `aria-expanded` | `"false"/"true"` | Estado expandido |
| Trigger | `aria-haspopup` | `"listbox"` | Indica que tiene popup |
| Trigger | `aria-label` | `"Seleccionar idioma"` | Descripción |
| Dropdown | `hidden` | `""` | Oculto visualmente |
| Option | `role` | `"option"` | Semántica ARIA |
| Option | `aria-selected` | `"true"/"false"` | Opción activa |
| Option | `lang` | `"es"` | Idioma del enlace |

## CSS Integration

### Language Selector Container
```css
.language-selector {
  position: relative;
  display: inline-flex;
}
```

### Trigger Button
```css
.language-selector__trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 13px;
  background: var(--surface-2);
  border: 1px solid color-mix(in oklab, var(--brand-base), transparent 70%);
  border-radius: 8px;
  color: var(--fg);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 233ms cubic-bezier(.2,.8,.2,1);
}

.language-selector__trigger:hover {
  background: var(--surface-3);
  border-color: var(--brand-base);
}

.language-selector__trigger[aria-expanded="true"] {
  background: var(--surface-3);
  border-color: var(--brand-base);
}
```

**Estados**:
- **Default**: Fondo surface-2, border 70% transparent
- **Hover**: Fondo surface-3, border-color brand
- **Expanded**: Mismo que hover

### Dropdown
```css
.language-selector__dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: var(--surface-2);
  border: 1px solid color-mix(in oklab, var(--brand-base), transparent 70%);
  border-radius: 12px;
  box-shadow: var(--shadow);
  min-width: 200px;
  z-index: 100;
  animation: languageDropdownFadeIn 233ms cubic-bezier(.2,.8,.2,1);
}

.language-selector__dropdown[hidden] {
  display: none;
}

@keyframes languageDropdownFadeIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Posicionamiento**:
- `position: absolute`: Posicionado relativo al trigger
- `top: calc(100% + 8px)`: Aparece debajo del trigger con 8px gap
- `right: 0`: Alineado a la derecha del trigger
- `z-index: 100`: Por encima de otros elementos

### Options List
```css
.language-selector__list {
  padding: 8px;
  margin: 0;
  list-style: none;
}

.language-selector__option {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 13px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: var(--fg);
  font-size: 14px;
  font-weight: 500;
  text-align: left;
  cursor: pointer;
  transition: background 144ms ease;
  text-decoration: none;
}

.language-selector__option:hover {
  background: var(--surface-3);
  color: var(--fg);
}

.language-selector__option.active {
  background: color-mix(in oklab, var(--brand-base), transparent 90%);
  color: var(--brand-base);
}
```

### Flag and Name
```css
.language-selector__flag {
  font-size: 20px;
  line-height: 1;
}

.language-selector__current {
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
```

### Responsive Design
```css
@media (max-width: 767.98px) {
  .language-selector__trigger {
    padding: 6px 10px;
    font-size: 13px;
  }

  .language-selector__icon {
    font-size: 16px;
  }

  .language-selector__dropdown {
    min-width: 180px;
    right: -8px; /* Ajuste para móvil */
  }

  .language-selector__option {
    padding: 8px 10px;
    font-size: 13px;
  }

  .language-selector__flag {
    font-size: 18px;
  }
}
```

## Languages Supported

### Configuration
```javascript
const languages = [
  { code: 'es', name: 'Español', flag: '🇪🇸', url: '/es/' },
  { code: 'en', name: 'English', flag: '🇺🇸', url: '/en/' },
  { code: 'fr', name: 'Français', flag: '🇫🇷', url: '/fr/' },
  { code: 'pt', name: 'Português', flag: '🇵🇹', url: '/pt/' },
  { code: 'ar', name: 'العربية', flag: '🇸🇦', url: '/ar/', dir: 'rtl' },
  { code: 'zh-hans', name: '简体中文', flag: '🇨🇳', url: '/zh-hans/' },
  { code: 'ja', name: '日本語', flag: '🇯🇵', url: '/ja/' },
  { code: 'hi', name: 'हिन्दी', flag: '🇮🇳', url: '/hi/' }
];
```

### Dynamic Generation
```javascript
function generateLanguageOptions(currentLang) {
  return languages.map(lang => {
    const isActive = lang.code === currentLang;
    return `
      <li role="none">
        <a
          href="${lang.url}"
          class="language-selector__option ${isActive ? 'active' : ''}"
          role="option"
          aria-selected="${isActive ? 'true' : 'false'}"
          lang="${lang.code}"
          ${lang.dir ? `dir="${lang.dir}"` : ''}
        >
          <span class="language-selector__flag">${lang.flag}</span>
          <span class="language-selector__name">${lang.name}</span>
        </a>
      </li>
    `;
  }).join('');
}
```

## Accessibility Features

### 1. ARIA Pattern Compliance
**Pattern**: Combobox o Listbox pattern de ARIA

**Implementación**:
- Trigger con `aria-haspopup="listbox"`
- Opciones con `role="option"`
- Estado activo con `aria-selected="true"`

### 2. Keyboard Navigation
```javascript
// Ver tabla anterior en sección Keyboard Navigation
```

### 3. Focus Management
```javascript
// Al abrir
const activeOption = dropdown.querySelector('.language-selector__option.active');
if (activeOption) {
  activeOption.focus();
} else {
  firstOption.focus();
}

// Al cerrar (automático)
// Browser returna focus al trigger automáticamente
```

### 4. Screen Reader Support
```html
<!-- Descripción clara -->
<button aria-label="Seleccionar idioma">
  🌐 <span aria-hidden="true">ES</span>
</button>

<!-- Estado activo claro -->
<a aria-selected="true" aria-current="true">
  🇪🇸 Español (actual)
</a>

<!-- Idioma con dir RTL -->
<a lang="ar" dir="rtl">
  العربية
</a>
```

### 5. Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  .language-selector__dropdown {
    animation: none;
  }

  .language-selector__trigger,
  .language-selector__option {
    transition: none;
  }
}
```

## Testing

### Unit Tests (Jest)
```javascript
describe('Language Selector', () => {
  let selector, trigger, dropdown;

  beforeEach(() => {
    document.body.innerHTML = `
      <div class="language-selector">
        <button class="language-selector__trigger" aria-expanded="false">
          ES
        </button>
        <div class="language-selector__dropdown" hidden>
          <ul class="language-selector__list">
            <li><a href="/es/" class="language-selector__option active">ES</a></li>
            <li><a href="/en/" class="language-selector__option">EN</a></li>
          </ul>
        </div>
      </div>
    `;
    selector = document.querySelector('.language-selector');
    trigger = selector.querySelector('.language-selector__trigger');
    dropdown = selector.querySelector('.language-selector__dropdown');
  });

  test('initializes correctly', () => {
    init();
    expect(trigger.getAttribute('aria-expanded')).toBe('false');
    expect(dropdown.hasAttribute('hidden')).toBe(true);
  });

  test('opens dropdown on trigger click', () => {
    init();
    trigger.click();
    expect(trigger.getAttribute('aria-expanded')).toBe('true');
    expect(dropdown.hasAttribute('hidden')).toBe(true); // still hidden because should removeAttribute
  });

  test('toggles dropdown state', () => {
    init();
    trigger.click();
    expect(trigger.getAttribute('aria-expanded')).toBe('true');

    trigger.click();
    expect(trigger.getAttribute('aria-expanded')).toBe('false');
  });

  test('closes dropdown when clicking outside', () => {
    init();
    trigger.click();
    expect(trigger.getAttribute('aria-expanded')).toBe('true');

    document.body.click();
    expect(trigger.getAttribute('aria-expanded')).toBe('false');
  });

  test('focuses active option on open', () => {
    init();
    trigger.click();

    const activeOption = dropdown.querySelector('.active');
    expect(document.activeElement).toBe(activeOption);
  });

  test('navigates with arrow keys', () => {
    init();
    trigger.click();

    // Start with first option focused
    let currentOption = dropdown.querySelector('.language-selector__option');
    currentOption.focus();

    // Press ArrowDown
    currentOption.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown' }));
    let nextOption = dropdown.querySelectorAll('.language-selector__option')[1];
    expect(document.activeElement).toBe(nextOption);
  });

  test('closes on Escape key', () => {
    init();
    trigger.click();
    expect(trigger.getAttribute('aria-expanded')).toBe('true');

    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
    expect(trigger.getAttribute('aria-expanded')).toBe('false');
    expect(document.activeElement).toBe(trigger);
  });
});
```

### Integration Tests (Cypress)
```javascript
describe('Language Selector Integration', () => {
  it('opens and closes dropdown', () => {
    cy.visit('/');
    cy.get('.language-selector__trigger').click();

    // Dropdown should be visible
    cy.get('.language-selector__dropdown')
      .should('be.visible')
      .and('have.attr', 'aria-hidden', 'false');

    cy.get('.language-selector__trigger')
      .should('have.attr', 'aria-expanded', 'true');

    // Click again to close
    cy.get('.language-selector__trigger').click();

    cy.get('.language-selector__dropdown').should('be.hidden');
    cy.get('.language-selector__trigger')
      .should('have.attr', 'aria-expanded', 'false');
  });

  it('closes when clicking outside', () => {
    cy.visit('/');
    cy.get('.language-selector__trigger').click();

    cy.get('.language-selector__dropdown').should('be.visible');

    cy.get('body').click();
    cy.get('.language-selector__dropdown').should('be.hidden');
  });

  it('shows active language', () => {
    cy.visit('/es/');
    cy.get('.language-selector__trigger').click();

    cy.get('.language-selector__option.active')
      .should('have.class', 'active')
      .and('have.attr', 'aria-selected', 'true')
      .and('contain', 'Español');
  });

  it('navigates with keyboard', () => {
    cy.visit('/');

    // Open dropdown
    cy.get('.language-selector__trigger').type('{enter}');
    cy.get('.language-selector__dropdown').should('be.visible');

    // Navigate with arrow keys
    cy.get('.language-selector__option').first().should('be.focused');

    cy.get('body').type('{arrowdown}');
    cy.get('.language-selector__option').eq(1).should('be.focused');

    cy.get('body').type('{arrowup}');
    cy.get('.language-selector__option').first().should('be.focused');

    // Close with Escape
    cy.get('body').type('{escape}');
    cy.get('.language-selector__dropdown').should('be.hidden');
  });

  it('redirects to selected language', () => {
    cy.visit('/');
    cy.get('.language-selector__trigger').click();

    cy.get('.language-selector__option')
      .contains('English')
      .click();

    cy.url().should('include', '/en/');
  });

  it('supports RTL languages', () => {
    cy.visit('/ar/');
    cy.get('.language-selector__option[lang="ar"]')
      .should('have.attr', 'dir', 'rtl');
  });
});
```

### Accessibility Tests
```javascript
describe('Language Selector Accessibility', () => {
  it('has proper ARIA attributes', () => {
    cy.visit('/');
    cy.get('.language-selector__trigger')
      .should('have.attr', 'aria-haspopup', 'listbox')
      .and('have.attr', 'aria-expanded', 'false');

    cy.get('.language-selector__trigger').click();

    cy.get('.language-selector__trigger')
      .should('have.attr', 'aria-expanded', 'true');

    cy.get('.language-selector__option')
      .each(($option) => {
        cy.wrap($option).should('have.attr', 'role', 'option');
      });
  });

  it('is keyboard navigable', () => {
    cy.visit('/');
    cy.injectAxe();

    // Open with keyboard
    cy.get('.language-selector__trigger').focus().type('{enter}');
    cy.checkA11y();

    // Navigate
    cy.get('.language-selector__option').first().focus();
    cy.get('body').type('{arrowdown}');
    cy.get('.language-selector__option').eq(1).should('be.focused');

    // Close with Escape
    cy.get('body').type('{escape}');
    cy.get('.language-selector__trigger').should('be.focused');
  });

  it('announces changes to screen readers', () => {
    cy.visit('/');
    cy.get('.language-selector__trigger').click();

    // SR should announce current selection
    cy.get('.language-selector__option.active')
      .should('have.attr', 'aria-selected', 'true')
      .and('have.attr', 'aria-current', 'true');
  });
});
```

## Events and Custom Events

### Language Change Event
```javascript
// Disparar evento al cambiar idioma
links.forEach(link => {
  link.addEventListener('click', function(e) {
    const newLang = this.getAttribute('lang');

    // Cerrar dropdown primero
    closeDropdown();

    // Disparar evento personalizado
    window.dispatchEvent(new CustomEvent('language-change', {
      detail: {
        from: currentLang,
        to: newLang,
        url: this.href
      }
    }));

    // Log para debugging
    console.log(`Language changed: ${currentLang} -> ${newLang}`);
  });
});

// Escuchar cambios
window.addEventListener('language-change', (e) => {
  console.log('Language changed:', e.detail);
  // Actualizar UI, analytics, etc.
});
```

### Dropdown State Events
```javascript
// Evento cuando dropdown se abre
trigger.addEventListener('click', () => {
  const isExpanded = trigger.getAttribute('aria-expanded') === 'true';

  if (!isExpanded) {
    window.dispatchEvent(new CustomEvent('language-dropdown-open'));
  }
});

// Evento cuando dropdown se cierra
document.addEventListener('click', (e) => {
  if (!selector.contains(e.target)) {
    window.dispatchEvent(new CustomEvent('language-dropdown-close'));
  }
});
```

## Integration Examples

### 1. Google Analytics
```javascript
window.addEventListener('language-change', (e) => {
  if (typeof gtag !== 'undefined') {
    gtag('event', 'language_change', {
      event_category: 'engagement',
      event_label: e.detail.to,
      value: 1
    });
  }
});
```

### 2. i18n Framework (react-i18next)
```javascript
window.addEventListener('language-change', (e) => {
  if (window.i18next) {
    window.i18next.changeLanguage(e.detail.to);
  }
});
```

### 3. Django Locale Middleware
```javascript
// views.py
def set_language(request):
  language = request.POST.get('language')
  if language:
    request.session['language'] = language
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('django_language', language)
    return response
```

## Performance Optimization

### 1. Event Delegation
```javascript
// En lugar de múltiples listeners
links.forEach(link => {
  link.addEventListener('click', handler);
});

// Usar delegación
dropdown.addEventListener('click', (e) => {
  const link = e.target.closest('.language-selector__option');
  if (link) {
    handleLinkClick(link);
  }
});
```

### 2. Debounce Click Outside
```javascript
const debouncedOutsideClick = debounce((e) => {
  if (!selector.contains(e.target)) {
    closeDropdown();
  }
}, 100);

document.addEventListener('click', debouncedOutsideClick);
```

### 3. Document Ready State Check
```javascript
// Evita añadir listeners múltiples veces
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
```

## Buenas Prácticas

### ✅ Hacer
```javascript
// Usar IIFE con strict mode
(function() {
  'use strict';
  // código
})();

// Validar existencia de elementos
if (!trigger || !dropdown) return;

// Usar ARIA apropiado
trigger.setAttribute('aria-expanded', 'true');

// Gestionar focus correctamente
if (activeOption) {
  activeOption.focus();
}

// Prevenir propagación cuando necesario
trigger.addEventListener('click', (e) => {
  e.stopPropagation();
  // toggle logic
});

// Cerrar al hacer click fuera
document.addEventListener('click', (e) => {
  if (!selector.contains(e.target)) {
    closeDropdown();
  }
});
```

### ❌ Evitar
```javascript
// No global scope pollution
var languageSelector = {};  // Usar IIFE

// No listeners sin validación
trigger.addEventListener('click', callback);  // Verificar existencia

// No olvidar preventDefault para navegación custom
// (A menos que quieras comportamiento por defecto)

// No gestionar estado global aquí
// (Usar eventos personalizados o store)

// No múltiples listeners idénticos
// Considerar cleanup en unmount (si aplicable)
```

## Casos de Uso

### 1. E-commerce Localization
```javascript
window.addEventListener('language-change', (e) => {
  // Actualizar prices, currency, etc.
  updatePrices(e.detail.to);
  // Cambiar moneda según país
  updateCurrency(e.detail.to);
  // Recargar productos localizados
  fetchLocalizedProducts(e.detail.to);
});
```

### 2. Analytics Tracking
```javascript
window.addEventListener('language-change', (e) => {
  analytics.track('language_changed', {
    from: e.detail.from,
    to: e.detail.to,
    page: window.location.pathname
  });
});
```

### 3. SEO Hreflang
```html
<!-- En template base.html -->
<link rel="alternate" hreflang="es" href="https://croody.com/es/">
<link rel="alternate" hreflang="en" href="https://croody.com/en/">
<link rel="alternate" hreflang="fr" href="https://croody.com/fr/">
<link rel="alternate" hreflang="x-default" href="https://croody.com/">
```

## Referencias

### Archivos Relacionados
- `static/css/components.css` - Estilos del selector
- `templates/base.html` - Template con selector
- `static/js/theme.js` - Theme toggle relacionado
- `locale/` - Archivos de traducción

### Documentación Externa
- [ARIA Listbox Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/)
- [ARIA Combobox Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/)
- [MDN - keyboard navigation](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/listbox_role)
- [WCAG 2.1 - Keyboard](https://www.w3.org/WAI/WCAG21/Understanding/keyboard.html)

### RFCs y Estándares
- [BCP 47 - Language Tags](https://tools.ietf.org/html/bcp47)
- [W3C Internationalization](https://www.w3.org/International/)

## Ver También
- [Theme Toggle](./theme-toggle.md)
- [Design System - Colores](../design-system/colores.md)
- [Design System - Tokens](../design-system/tokens.md)
- [Internationalization](../../07-INTERNACIONALIZACION/sistema-traduccion.md)
