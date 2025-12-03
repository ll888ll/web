# Theme Toggle - Documentación Completa

## Resumen
El sistema de cambio de tema de Croody implementa un toggle dinámico entre temas **claro** y **oscuro** con persistencia en localStorage, detección de preferencias del sistema y prevención de FOUC (Flash of Unstyled Content).

## Ubicación
`/proyecto_integrado/Croody/static/js/theme.js` (180 líneas)

## Arquitectura

### IIFE Pattern
```javascript
(function(){
  // Todo el código envuelto en IIFE
  // Evita contaminación del scope global
})();
```

### Variables Principales
```javascript
const root = document.documentElement;
const KEY = 'theme';  // Clave para localStorage
```

## Funcionalidades Principales

### 1. Theme Management

#### Set Theme
```javascript
const setTheme = t => {
  root.setAttribute('data-theme', t);
  localStorage.setItem(KEY, t);
};
```

**Operaciones**:
1. Actualiza atributo `data-theme` en `<html>`
2. Guarda en localStorage para persistencia
3. Dispara evento personalizado (opcional)

#### Get Theme
```javascript
const getTheme = () => localStorage.getItem(KEY) || 'dark';
```

**Fallbacks**:
1. Intenta localStorage (tema guardado)
2. Si no existe, usa 'dark' por defecto

### 2. Inicialización (FOUC Prevention)

```javascript
(function initTheme(){
  const savedTheme = localStorage.getItem(KEY);
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
  setTheme(initialTheme);
})();
```

**Proceso**:
1. **Antes de DOMContentLoaded** - Se ejecuta inmediatamente
2. Lee tema guardado en localStorage
3. Si no existe, consulta preferencia del sistema
4. Aplica tema inmediatamente (evita FOUC)
5. Renderiza sin parpadeo

### 3. Toggle Switch

```javascript
document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.querySelector('.theme-toggle__checkbox');
  if(themeToggle){
    themeToggle.checked = getTheme() === 'light';
    themeToggle.addEventListener('change', () => {
      setTheme(themeToggle.checked ? 'light' : 'dark');
    });
  }
});
```

**Características**:
- Sincroniza estado visual con localStorage
- Toggle checkbox controla el tema
- `checked` = light, `unchecked` = dark

### 4. Responsive Navigation

#### Nav Toggle
```javascript
const navToggle = document.querySelector('.nav-toggle');
const navDrawer = document.querySelector('.nav-drawer');
const body = document.body;

const toggleNav = force => {
  if(!navToggle || !navDrawer) return;
  const isOpen = force !== undefined ? !force : navToggle.getAttribute('aria-expanded') === 'true';
  const next = !isOpen;
  navToggle.setAttribute('aria-expanded', String(next));
  navDrawer.classList.toggle('is-open', next);
  navDrawer.setAttribute('aria-hidden', String(!next));
  body.classList.toggle('nav-open', next);
  if(next){
    const firstLink = navDrawer.querySelector('a');
    firstLink && firstLink.focus();
  } else {
    navToggle.focus();
  }
};
```

**Estados**:
- **Closed**: `aria-expanded="false"`, `is-open` class removed, body normal
- **Open**: `aria-expanded="true"`, `is-open` class added, body overflow hidden, focus on first link

#### Event Listeners
```javascript
// Click en toggle
navToggle.addEventListener('click', () => toggleNav());

// Click fuera del drawer para cerrar
navDrawer.addEventListener('click', e => {
  if(e.target === navDrawer) toggleNav(false);
  if(e.target instanceof HTMLElement && e.target.closest('a')) toggleNav(false);
});

// Escape para cerrar
document.addEventListener('keydown', e => {
  if(e.key === 'Escape' && navDrawer.classList.contains('is-open')) toggleNav(false);
});
```

### 5. Header Scroll Behavior

```javascript
const header = document.querySelector('.site-header');
if(header){
  let ticking = false;
  const handleScroll = () => {
    const condense = window.scrollY > 89;
    header.classList.toggle('is-condensed', condense);
    ticking = false;
  };
  handleScroll();
  window.addEventListener('scroll', () => {
    if(!ticking){
      window.requestAnimationFrame(handleScroll);
      ticking = true;
    }
  }, {passive: true});
}
```

**Optimizaciones**:
- **requestAnimationFrame**: Sincroniza con repaint del navegador
- **passive listener**: Optimiza scroll performance
- **ticking flag**: Previene múltiples ejecuciones por frame
- **Umbral**: 89px - Aplica clase `is-condensed`

### 6. Debounce Utility

```javascript
const debounce = (fn, ms) => {
  let t;
  return (...a) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...a), ms);
  };
};
```

**Uso**:
```javascript
const run = debounce(() => {
  applyFilter(field.value);
}, 233);  // 233ms = Golden Ratio basado
```

### 7. Search Functionality

#### Search Input
```html
<input
  type="search"
  data-search-input
  aria-expanded="false"
  aria-controls="search-list"
>
```

#### Search List
```html
<ul id="search-list" role="listbox">
  <li role="option">Resultado 1</li>
  <li role="option">Resultado 2</li>
</ul>
```

#### Filter Logic
```javascript
const list = document.querySelector('#search-list');
const searchFields = Array.from(document.querySelectorAll('[data-search-input]'));
if(list && searchFields.length){
  const items = Array.from(list.querySelectorAll('[role="option"]'));
  const applyFilter = value => {
    const q = value.trim().toLowerCase();
    let visible = 0;
    items.forEach(it => {
      const match = !q || it.textContent.toLowerCase().includes(q);
      it.style.display = match ? 'block' : 'none';
      if(match) visible++;
    });
    const expanded = String(visible > 0);
    searchFields.forEach(inp => inp.setAttribute('aria-expanded', expanded));
  };
  // ... más código
}
```

**Características**:
- Debounce de 233ms
- Sincroniza entre múltiples inputs
- Actualiza aria-expanded
- Acceso rápido con tecla `/`

#### Keyboard Shortcuts
```javascript
// Focus en search con /
document.addEventListener('keydown', e => {
  if(e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey &&
     e.target instanceof HTMLElement &&
     e.target.tagName !== 'INPUT' &&
     e.target.tagName !== 'TEXTAREA' &&
     !e.target.isContentEditable){
    e.preventDefault();
    const preferred = searchFields.find(inp => inp.offsetParent !== null) || searchFields[0];
    preferred && preferred.focus();
  }
});

// Escape para limpiar
field.addEventListener('keydown', e => {
  if(e.key === 'Escape'){
    field.value = '';
    syncValue(field, '');
    applyFilter('');
    field.setAttribute('aria-expanded', 'false');
  }
});
```

### 8. Tab System (Interactive Ecosystem)

```javascript
const tabButtons = document.querySelectorAll('.tab-button');
if(tabButtons.length){
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const tab = btn.dataset.tab;
      tabButtons.forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      const targetContent = document.getElementById(`${tab}-tab`);
      if(targetContent){
        targetContent.classList.add('active');
      }
    });
  });
}
```

**Estructura HTML**:
```html
<div class="ecosystem-tabs">
  <button class="tab-button active" data-tab="buddy">Buddy</button>
  <button class="tab-button" data-tab="luks">Luks</button>
</div>

<div id="buddy-tab" class="tab-content active">Buddy Content</div>
<div id="luks-tab" class="tab-content">Luks Content</div>
```

### 9. Beta Signup Modal

#### Open/Close Logic
```javascript
const betaBtn = document.getElementById('beta-signup-btn');
const betaModal = document.getElementById('beta-modal');
if(betaBtn && betaModal){
  betaBtn.addEventListener('click', () => {
    betaModal.classList.add('active');
    betaModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  });

  const closeModal = () => {
    betaModal.classList.remove('active');
    betaModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  };

  betaClose.addEventListener('click', closeModal);
  betaModal.addEventListener('click', e => {
    if(e.target === betaModal) closeModal();
  });

  document.addEventListener('keydown', e => {
    if(e.key === 'Escape' && betaModal.classList.contains('active')){
      closeModal();
    }
  });
}
```

#### Form Handling
```javascript
const betaForm = document.getElementById('beta-signup-form');
const betaSuccess = document.getElementById('beta-success');
if(betaForm){
  betaForm.addEventListener('submit', e => {
    e.preventDefault();
    const formData = new FormData(betaForm);
    const data = Object.fromEntries(formData);
    console.log('Beta signup:', data);
    betaForm.style.display = 'none';
    betaSuccess.style.display = 'block';
    setTimeout(closeModal, 3000);
  });
}
```

**Estados**:
1. **Closed**: `active` class removed, `aria-hidden="true"`
2. **Open**: `active` class added, `aria-hidden="false"`, body overflow hidden
3. **Success**: Form hidden, success message shown, auto-close after 3s

## Integración CSS

### Theme Toggle Checkbox
```css
.theme-toggle__checkbox {
  width: 33px;
  height: 21px;
  appearance: none;
  background: var(--surface-2);
  border-radius: 21px;
  position: relative;
  border: 1px solid color-mix(in oklab, var(--brand-base), transparent 70%);
}

.theme-toggle__checkbox::after {
  content: "";
  position: absolute;
  top: 2px;
  left: 2px;
  width: 17px;
  height: 17px;
  border-radius: 50%;
  background: var(--brand-base);
  transition: left 233ms cubic-bezier(.2,.8,.2,1);
}

.theme-toggle__checkbox:checked::after {
  left: 14px;
}
```

### Navigation Drawer
```css
.nav-drawer {
  position: fixed;
  inset: 0;
  background: color-mix(in oklab, var(--bg) 96%, transparent 4%);
  backdrop-filter: blur(14px);
  transform: translateY(-100%);
  transition: transform 333ms cubic-bezier(.2,.8,.2,1);
  z-index: var(--z-1000);
}

.nav-drawer.is-open {
  transform: translateY(0);
}
```

### Header Condensed
```css
.site-header {
  height: 82px;
  transition: height .24s cubic-bezier(.2,.8,.2,1),
              box-shadow .24s,
              background .24s;
}

.site-header.is-condensed {
  height: 64px;
  box-shadow: var(--shadow-sm);
  background: color-mix(in oklab, var(--bg) 80%, transparent 20%);
}
```

## Eventos Personalizados

### Theme Change Event
```javascript
const setTheme = t => {
  root.setAttribute('data-theme', t);
  localStorage.setItem(KEY, t);

  // Disparar evento personalizado
  window.dispatchEvent(new CustomEvent('theme-change', {
    detail: { theme: t }
  }));
};

// Escuchar cambios
window.addEventListener('theme-change', (e) => {
  console.log('Theme changed to:', e.detail.theme);
});
```

## Optimizaciones

### 1. FOUC Prevention
```javascript
// Se ejecuta INMEDIATAMENTE, antes de cualquier render
(function initTheme(){
  // ... código de inicialización
})();
```

### 2. RequestAnimationFrame para Scroll
```javascript
window.addEventListener('scroll', () => {
  if(!ticking){
    window.requestAnimationFrame(handleScroll);
    ticking = true;
  }
}, {passive: true});
```

### 3. Debounce para Search
```javascript
const run = debounce(() => {
  applyFilter(field.value);
}, 233);  // Golden ratio timing
```

### 4. Passive Listeners
```javascript
window.addEventListener('scroll', handler, {passive: true});
```

## Accessibility

### ARIA Attributes
```html
<!-- Theme Toggle -->
<input
  type="checkbox"
  class="theme-toggle__checkbox"
  role="switch"
  aria-label="Toggle dark mode"
  aria-checked="false"
>

<!-- Navigation -->
<button class="nav-toggle" aria-expanded="false" aria-controls="nav-drawer">
  Menu
</button>

<!-- Search -->
<input
  data-search-input
  type="search"
  aria-expanded="false"
  aria-controls="search-list"
  aria-label="Search"
>

<!-- Modal -->
<div id="beta-modal" aria-hidden="true" role="dialog" aria-modal="true">
  <div class="modal__content" role="document">
    <button id="beta-modal-close" aria-label="Close modal">×</button>
  </div>
</div>
```

### Focus Management
```javascript
// En nav open
if(next){
  const firstLink = navDrawer.querySelector('a');
  firstLink && firstLink.focus();
}

// En nav close
else {
  navToggle.focus();
}

// En modal open
betaModal.classList.add('active');
betaModal.setAttribute('aria-hidden', 'false');
// Focus en primer elemento focusable
```

### Keyboard Navigation
```javascript
// Escape para cerrar nav
document.addEventListener('keydown', e => {
  if(e.key === 'Escape' && navDrawer.classList.contains('is-open')) {
    toggleNav(false);
  }
});

// Global search shortcut
document.addEventListener('keydown', e => {
  if(e.key === '/' && /* condiciones */) {
    e.preventDefault();
    searchField.focus();
  }
});
```

## Testing

### Unit Tests (Jest)
```javascript
describe('Theme Toggle', () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.removeAttribute('data-theme');
  });

  test('sets dark theme by default', () => {
    setTheme('dark');
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    expect(localStorage.getItem('theme')).toBe('dark');
  });

  test('toggles between light and dark', () => {
    setTheme('dark');
    expect(getTheme()).toBe('dark');

    setTheme('light');
    expect(getTheme()).toBe('light');
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
  });

  test('initializes from localStorage', () => {
    localStorage.setItem('theme', 'light');
    const initialTheme = localStorage.getItem(KEY) || 'dark';
    expect(initialTheme).toBe('light');
  });

  test('initializes from system preference', () => {
    localStorage.clear();
    // Mock system preference
    Object.defineProperty(window, 'matchMedia', {
      value: jest.fn().mockImplementation(query => ({
        matches: query === '(prefers-color-scheme: dark)',
        addListener: jest.fn(),
        removeListener: jest.fn(),
      }))
    });

    const savedTheme = localStorage.getItem(KEY);
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
    expect(initialTheme).toBe('dark');
  });
});
```

### Integration Tests (Cypress)
```javascript
describe('Theme Toggle Integration', () => {
  it('toggles theme on click', () => {
    cy.visit('/');
    cy.get('.theme-toggle__checkbox').as('toggle');

    // Initially dark
    cy.get('@toggle').should('not.be.checked');
    cy.get('html').should('have.attr', 'data-theme', 'dark');

    // Toggle to light
    cy.get('@toggle').click();
    cy.get('@toggle').should('be.checked');
    cy.get('html').should('have.attr', 'data-theme', 'light');

    // Toggle back to dark
    cy.get('@toggle').click();
    cy.get('@toggle').should('not.be.checked');
    cy.get('html').should('have.attr', 'data-theme', 'dark');
  });

  it('persists theme in localStorage', () => {
    cy.visit('/');
    cy.get('.theme-toggle__checkbox').click();
    cy.window().then(win => {
      expect(win.localStorage.getItem('theme')).toBe('light');
    });
  });

  it('respects system preference on first visit', () => {
    cy.clearLocalStorage();
    cy.visit('/');
    cy.get('.theme-toggle__checkbox').should('not.be.checked');
  });
});

describe('Navigation Drawer', () => {
  it('opens on toggle click', () => {
    cy.visit('/');
    cy.get('.nav-toggle').click();
    cy.get('.nav-drawer').should('have.class', 'is-open');
    cy.get('.nav-toggle').should('have.attr', 'aria-expanded', 'true');
  });

  it('closes on Escape key', () => {
    cy.visit('/');
    cy.get('.nav-toggle').click();
    cy.get('.nav-drawer').should('have.class', 'is-open');
    cy.get('body').type('{esc}');
    cy.get('.nav-drawer').should('not.have.class', 'is-open');
  });

  it('closes when clicking outside', () => {
    cy.visit('/');
    cy.get('.nav-toggle').click();
    cy.get('.nav-drawer').should('have.class', 'is-open');
    cy.get('.nav-drawer').click(0, 0);
    cy.get('.nav-drawer').should('not.have.class', 'is-open');
  });
});

describe('Search Functionality', () => {
  it('filters results on input', () => {
    cy.visit('/');
    cy.get('[data-search-input]').type('test');
    cy.get('#search-list [role="option"]').should('contain', 'test');
  });

  it('opens search with / key', () => {
    cy.visit('/');
    cy.get('body').type('/');
    cy.get('[data-search-input]').should('be.focused');
  });

  it('clears search with Escape', () => {
    cy.visit('/');
    cy.get('[data-search-input]').type('test').type('{esc}');
    cy.get('[data-search-input]').should('have.value', '');
  });
});
```

## Buenas Prácticas

### ✅ Hacer
```javascript
// Usar IIFE para evitar scope global
(function(){
  'use strict';
  // código
})();

// Validar existencia de elementos
if(themeToggle){
  // usar elemento
}

// Usar passive listeners para scroll
window.addEventListener('scroll', handler, {passive: true});

// Debounce para eventos frecuentes
const run = debounce(() => {
  applyFilter(field.value);
}, 233);

// ARIA attributes apropiados
element.setAttribute('aria-expanded', 'true');
element.setAttribute('aria-hidden', 'false');

// FOUC prevention
(function initTheme(){
  // código
})();
```

### ❌ Evitar
```javascript
// No pollutor global
var theme = 'dark';  // Usar const/let

// No listeners sin validación
navToggle.addEventListener('click', () => {});  // puede fallar

// No usar setTimeout para scroll
window.addEventListener('scroll', () => {
  setTimeout(handleScroll, 100);  // Usar rAF
});

// No olvidar passive
window.addEventListener('scroll', handler);  // Añadir {passive: true}

// No mutar sin validación
document.documentElement.setAttribute('data-theme', theme);  // Verificar primero

// No listeners duplicados
element.addEventListener('click', handler1);
element.addEventListener('click', handler2);  // OK para múltiples, pero considerar
```

## Eventos y Custom Events

### Theme Change Event
```javascript
// Disparar
window.dispatchEvent(new CustomEvent('theme-change', {
  detail: { theme: 'light' }
}));

// Escuchar
window.addEventListener('theme-change', (e) => {
  console.log('Theme:', e.detail.theme);
});
```

### Tab Change Event
```javascript
tabButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab;
    // Actualizar UI
    window.dispatchEvent(new CustomEvent('tab-change', {
      detail: { tab }
    }));
  });
});
```

## Performance Monitoring

### Metrics Collection
```javascript
// Medir tiempo de inicialización
const initStart = performance.now();
initTheme();
const initTime = performance.now() - initStart;
console.log(`Theme init: ${initTime}ms`);

// Medir frecuencia de scroll
let scrollCount = 0;
window.addEventListener('scroll', () => {
  scrollCount++;
}, {passive: true});
```

## Casos de Uso

### 1. Theme Provider (React)
```javascript
// Para integración con frameworks
const ThemeContext = {
  getTheme: () => getTheme(),
  setTheme: (theme) => setTheme(theme),
  subscribe: (callback) => {
    window.addEventListener('theme-change', callback);
    return () => window.removeEventListener('theme-change', callback);
  }
};
```

### 2. Server-Side Theme Detection
```javascript
// middleware.py (Django)
def set_theme_cookie(request, response):
    theme = request.COOKIES.get('theme', 'dark')
    response.set_cookie('theme', theme, max_age=31536000)
    return response
```

### 3. Multi-Brand Theme Support
```javascript
// Extender para soporte multi-marca
const setBrand = (brand) => {
  root.setAttribute('data-brand', brand);
  localStorage.setItem('brand', brand);
};

const getBrand = () => localStorage.getItem('brand') || 'gator';
```

## Referencias

### Archivos Relacionados
- `static/css/base.css` - Estilos de componentes
- `static/css/components.css` - Estilos de theme toggle y nav
- `static/js/language-selector.js` - Selector de idiomas
- `templates/base.html` - Template base con scripts

### Documentación Externa
- [localStorage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
- [matchMedia API](https://developer.mozilla.org/en-US/docs/Web/API/Window/matchMedia)
- [CustomEvent](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent)
- [ARIA Switch Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/switch/)

## Ver También
- [Language Selector](./language-selector.md)
- [Design System - Colores](../design-system/colores.md)
- [Design System - Tokens](../design-system/tokens.md)
- [Accessibility](../accesibilidad.md)
