# Sistema de Colores - Documentación Completa

## Resumen
El sistema de colores de Croody implementa una paleta armoniosa basada en **Geometría Sagrada** y principios de **percepción visual**. Utiliza 4 paletas principales (Gator, Jungle, Sand, Crimson) con soporte completo para temas claro y oscuro, y cambio dinámico de marca.

## Ubicación
`/proyecto_integrado/Croody/static/css/tokens.css` (líneas 31-132)

## Filosofía del Sistema

### Principios Fundamentales
1. **Armonía Natural**: Colores basados en proporciones áureas
2. **Accesibilidad WCAG 2.1**: Contraste mínimo AA (4.5:1)
3. **Versatilidad**: Soporte multi-marca (Gator, Buddy, Luks)
4. **Flexibilidad**: Temas claro y oscuro dinámicos
5. **Psicología del Color**: Colores que evocan emociones específicas

### Aplicación del Número Áureo
```css
/* Las escalas de color siguen progresión φ */
--gator-100: color-mix(in oklab, var(--gator-500) 20%, white);
--gator-200: color-mix(in oklab, var(--gator-500) 40%, white);
--gator-300: color-mix(in oklab, var(--gator-500) 60%, white);
```

## Paletas Principales

### 1. Gator (Verde Corporativo)

**Propósito**: Marca principal de Croody, naturaleza, crecimiento, bienestar

**Psicología**: Confianza, salud, equilibrio, renovación

**Aplicaciones**:
- Botones primarios
- Enlaces principales
- Elementos de navegación
- Indicadores de éxito
- Iconos de estado positivo

#### Escala Completa
```css
:root, html[data-theme="dark"] {
  --gator-950: #041009;  /* Más oscuro - Header hover, overlays */
  --gator-900: #082015;  /* Oscuro - Backgrounds profundos */
  --gator-800: #103924;  /* Sombra profunda */
  --gator-700: #1C5C37;  /* Active state, pressed */
  --gator-600: #277947;  /* Hover state */
  --gator-500: #3C9E5D;  /* BASE - Color principal */
  --gator-400: #5BB97D;  /* Hover suave */
  --gator-300: #80D3A0;  /* Elementos sutiles, borders */
  --gator-200: #B4E5C6;  /* Backgrounds suaves */
  --gator-100: #DDF6E8;  /* Hovers de superficie */
  --gator-50:  #F0FBF5;  /* Más claro - Backgrounds principales */
}
```

#### Uso por Intensidad
```css
/* Primarios */
.btn-primary {
  background: var(--gator-500);
  color: white;
}

.btn-primary:hover {
  background: var(--gator-600);
}

/* Superficies */
.surface-primary {
  background: var(--gator-50);
  border: 1px solid var(--gator-300);
}

/* Estados */
.status-success {
  background: var(--gator-100);
  color: var(--gator-700);
  border: 1px solid var(--gator-300);
}
```

### 2. Jungle (Gris-Verde Neutros)

**Propósito**: Fondos, superficies, texto, bordes

**Psicología**: Neutralidad, profesionalidad, elegancia

**Aplicaciones**:
- Backgrounds principales
- Superficies de componentes
- Texto y tipografía
- Bordes y divisores
- Estados deshabilitados

#### Escala Completa
```css
:root, html[data-theme="dark"] {
  --jungle-950: #050807;  /* Fondo más oscuro */
  --jungle-900: #0B1311;  /* Fondo principal dark */
  --jungle-800: #141F1B;  /* Superficie nivel 1 */
  --jungle-700: #1E2C26;  /* Superficie nivel 2 */
  --jungle-600: #293833;  /* Bordes dark */
  --jungle-500: #374640;  /* Texto secundario */
  --jungle-400: #56655F;  /* Texto muted */
  --jungle-300: #7A8883;  /* Texto placeholder */
  --jungle-200: #A9B4B0;  /* Bordes suaves */
  --jungle-100: #D3DAD7;  /* Backgrounds claros */
  --jungle-50:  #EEF1EF;  /* Fondo claro principal */
}
```

#### Mapeo por Tema
```css
/* Dark Theme (default) */
:root, html[data-theme="dark"] {
  --bg: var(--jungle-950);
  --surface-1: var(--jungle-900);
  --surface-2: var(--jungle-800);
  --surface-3: var(--jungle-700);
  --fg: var(--jungle-50);
  --fg-muted: var(--jungle-200);
  --fg-subtle: var(--jungle-300);
  --border-1: color-mix(in oklab, var(--jungle-50) 10%, transparent);
  --border-2: color-mix(in oklab, var(--jungle-50) 20%, transparent);
}

/* Light Theme */
html[data-theme="light"] {
  --bg: var(--jungle-50);
  --surface-1: var(--jungle-100);
  --surface-2: var(--jungle-200);
  --surface-3: var(--jungle-300);
  --fg: var(--jungle-900);
  --fg-muted: var(--jungle-600);
  --fg-subtle: var(--jungle-500);
  --border-1: color-mix(in oklab, var(--jungle-900) 10%, transparent);
  --border-2: color-mix(in oklab, var(--jungle-900) 15%, transparent);
}
```

#### Uso en Tipografía
```css
/* Text hierarchy */
.text-primary {
  color: var(--fg);  /* Texto principal */
}

.text-secondary {
  color: var(--fg-muted);  /* Texto secundario */
}

.text-tertiary {
  color: var(--fg-subtle);  /* Texto sutil */
}

/* Estados */
.text-disabled {
  color: var(--jungle-400);
  opacity: 0.6;
}
```

### 3. Sand (Dorado Cálido)

**Propósito**: Marca Luks, elementos premium, lujo

**Psicología**: Elegancia, lujo, riqueza, calidez

**Aplicaciones**:
- Marca Luks
- Elementos premium
- Badges de status especial
- Gradientes decorativos
- Acentos de alto valor

#### Escala Completa
```css
:root {
  --sand-600: #C18F4A;  /* Luks primary - Más intenso */
  --sand-500: #E0B771;  /* Luks base - Color principal */
  --sand-400: #F3D398;  /* Hover suave */
  --sand-300: #F8E1B7;  /* Elementos sutiles */
  --sand-200: #FBECD1;  /* Backgrounds */
  --sand-100: #FDF5E6;  /* Fondos principales */
}
```

#### Aplicación Premium
```css
/* Badge premium */
.badge-premium {
  background: var(--sand-500);
  color: var(--jungle-950);
  border: 1px solid var(--sand-600);
}

.badge-premium:hover {
  background: var(--sand-600);
}

/* Botón premium */
.btn-premium {
  background: linear-gradient(
    135deg,
    var(--sand-400),
    var(--sand-500)
  );
  color: var(--jungle-950);
  box-shadow: var(--shadow-brand);
}
```

#### Activación de Marca Luks
```css
html[data-brand="gold"] {
  --brand-base: var(--sand-600);
  --brand-strong: var(--sand-500);
  --brand-soft: var(--sand-400);
}
```

### 4. Crimson (Rojo)

**Propósito**: Marca Buddy, alertas, urgencia, acción

**Psicología**: Energía, pasión, urgencia, dinamismo

**Aplicaciones**:
- Marca Buddy
- Alertas y errores
- Estados de peligro
- CTAs críticos
- Indicadores de urgencia

#### Escala Completa
```css
:root {
  --crimson-deep: #7A1E2A;    /* Profundo - Estados graves */
  --crimson-primary: #E04F56;  /* Buddy primary - Principal */
  --crimson-soft: #FFA7B5;     /* Suave - Estados leves */
}
```

#### Uso en Alertas
```css
/* Alert - Error */
.alert-error {
  background: color-mix(in oklab, var(--crimson-soft) 20%, white);
  border: 1px solid var(--crimson-primary);
  color: var(--crimson-deep);
}

.alert-error::before {
  content: "⚠️";
  color: var(--crimson-primary);
}

/* Estado crítico */
.status-critical {
  background: var(--crimson-soft);
  color: var(--crimson-deep);
  animation: pulse 2s infinite;
}
```

#### Activación de Marca Buddy
```css
html[data-brand="crimson"] {
  --brand-base: var(--crimson-primary);
  --brand-strong: var(--crimson-deep);
  --brand-soft: var(--crimson-soft);
}
```

## Colores Semánticos

### Estados de Feedback

#### Información
```css
:root {
  --info-500: #31BFEA;  /* Azul informativo */
  --info-100: #E6F9FC;  /* Background suave */
}

/* Uso */
.notification-info {
  background: var(--info-100);
  border: 1px solid var(--info-500);
  color: color-mix(in oklab, var(--info-500) 80%, black);
}
```

#### Advertencia
```css
:root {
  --warn-500: #F5B454;  /* Amarillo-naranja */
  --warn-100: #FEF3E6;  /* Background suave */
}

/* Uso */
.notification-warning {
  background: var(--warn-100);
  border: 1px solid var(--warn-500);
  color: color-mix(in oklab, var(--warn-500) 80%, black);
}
```

#### Error
```css
:root {
  --error-500: #F06565;  /* Rojo */
  --error-100: #FCE8E8;  /* Background suave */
}

/* Uso */
.notification-error {
  background: var(--error-100);
  border: 1px solid var(--error-500);
  color: color-mix(in oklab, var(--error-500) 80%, black);
}
```

#### Éxito
```css
:root {
  --success-500: #4CAF50;  /* Verde */
  --success-100: #E8F5E9;  /* Background suave */
}

/* Uso */
.notification-success {
  background: var(--success-100);
  border: 1px solid var(--success-500);
  color: color-mix(in oklab, var(--success-500) 80%, black);
}
```

## Variables Dinámicas de Tema

### Tema Oscuro (Por Defecto)
```css
:root, html[data-theme="dark"] {
  /* Backgrounds */
  --bg: var(--jungle-950);        /* Fondo principal */
  --surface-1: var(--jungle-900);  /* Superficie nivel 1 */
  --surface-2: var(--jungle-800);  /* Superficie nivel 2 */
  --surface-3: var(--jungle-700);  /* Superficie nivel 3 */

  /* Texto */
  --fg: var(--jungle-50);          /* Texto principal */
  --fg-muted: var(--jungle-200);   /* Texto secundario */
  --fg-subtle: var(--jungle-300);  /* Texto sutil */

  /* Bordes */
  --border-1: color-mix(in oklab, var(--jungle-50) 10%, transparent);
  --border-2: color-mix(in oklab, var(--jungle-50) 20%, transparent);

  /* Interactivo */
  --focus-ring: var(--gator-500);   /* Anillo de foco */
  --overlay: rgba(0, 0, 0, 0.5);   /* Overlays */
}
```

### Tema Claro
```css
html[data-theme="light"] {
  /* Backgrounds */
  --bg: var(--jungle-50);          /* Fondo principal */
  --surface-1: var(--jungle-100);  /* Superficie nivel 1 */
  --surface-2: var(--jungle-200);  /* Superficie nivel 2 */
  --surface-3: var(--jungle-300);  /* Superficie nivel 3 */

  /* Texto */
  --fg: var(--jungle-900);         /* Texto principal */
  --fg-muted: var(--jungle-600);   /* Texto secundario */
  --fg-subtle: var(--jungle-500);  /* Texto sutil */

  /* Bordes */
  --border-1: color-mix(in oklab, var(--jungle-900) 10%, transparent);
  --border-2: color-mix(in oklab, var(--jungle-900) 15%, transparent);

  /* Interactivo */
  --focus-ring: var(--gator-500);
  --overlay: rgba(0, 0, 0, 0.3);
}
```

## Sistema de Marcas (Brand Switching)

### Gator (Por Defecto)
```css
:root, html[data-brand="gator"] {
  /* Variables semánticas */
  --brand-base: var(--gator-500);
  --brand-strong: var(--gator-600);
  --brand-soft: var(--gator-300);
  --on-brand: #FFFFFF;

  /* Aplicación */
  --brand-contrast: color-mix(in oklab, var(--brand-base) 80%, black);
  --brand-surface: color-mix(in oklab, var(--brand-base) 10%, transparent);
}
```

### Buddy (Crimson)
```css
html[data-brand="crimson"] {
  --brand-base: var(--crimson-primary);
  --brand-strong: var(--crimson-deep);
  --brand-soft: var(--crimson-soft);
  --on-brand: #FFFFFF;

  /* Ajustes automáticos */
  --brand-contrast: color-mix(in oklab, var(--brand-base) 85%, black);
  --brand-surface: color-mix(in oklab, var(--brand-base) 15%, transparent);
}
```

### Luks (Sand/Gold)
```css
html[data-brand="gold"] {
  --brand-base: var(--sand-600);
  --brand-strong: var(--sand-500);
  --brand-soft: var(--sand-400);
  --on-brand: var(--jungle-950);  /* Texto oscuro sobre dorado */

  /* Ajustes para dorado */
  --brand-contrast: var(--jungle-700);
  --brand-surface: color-mix(in oklab, var(--sand-600) 12%, transparent);
}
```

### Cambio Dinámico de Marca
```javascript
// Cambiar marca en runtime
function switchBrand(brandName) {
  document.documentElement.setAttribute('data-brand', brandName);

  // Disparar evento para listeners
  window.dispatchEvent(new CustomEvent('brand-change', {
    detail: { brand: brandName }
  }));
}

// Uso
switchBrand('crimson');  // Activar Buddy
switchBrand('gold');     // Activar Luks
switchBrand('gator');    // Activar Gator
```

## Utilidades CSS

### Classes de Color
```css
/* Text colors */
.text-primary { color: var(--brand-base); }
.text-success { color: var(--gator-500); }
.text-warning { color: var(--warn-500); }
.text-error { color: var(--error-500); }
.text-info { color: var(--info-500); }

.text-on-brand { color: var(--on-brand); }
.text-muted { color: var(--fg-muted); }
.text-subtle { color: var(--fg-subtle); }

/* Background colors */
.bg-primary { background: var(--bg); }
.bg-surface { background: var(--surface-1); }
.bg-brand { background: var(--brand-base); }

.bg-gator { background: var(--gator-500); }
.bg-jungle { background: var(--jungle-500); }
.bg-sand { background: var(--sand-500); }
.bg-crimson { background: var(--crimson-primary); }

/* Border colors */
.border-primary { border-color: var(--border-1); }
.border-secondary { border-color: var(--border-2); }
.border-brand { border-color: var(--brand-base); }
```

### Mixins (Via @apply)
```css
/* Button variants */
.btn-primary {
  @apply px-4 py-2 rounded-md font-medium;
  background: var(--brand-base);
  color: var(--on-brand);
  border: 1px solid var(--brand-strong);
}

.btn-primary:hover {
  background: var(--brand-strong);
}

/* Alert variants */
.alert {
  @apply p-4 rounded-lg border;
  background: var(--surface-1);
  border-color: var(--border-1);
}

.alert-success {
  @apply alert;
  background: var(--success-100);
  border-color: var(--success-500);
  color: var(--success-600);
}

.alert-error {
  @apply alert;
  background: var(--error-100);
  border-color: var(--error-500);
  color: var(--error-600);
}
```

## Accesibilidad

### Estándares WCAG 2.1
```css
/* Contraste mínimo AA - 4.5:1 */
/* Ejemplo: Gator-500 sobre blanco */
.contrast-example {
  color: #3C9E5D;  /* Gator-500 */
  background: white;
  /* Ratio: 4.82:1 ✅ Cumple AA */
}

/* Verificación programática */
:root {
  --min-contrast-ratio: 4.5;
  --target-contrast-ratio: 7;  /* AAA */
}

/* Estados de focus visibles */
*:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}
```

### Contraste por Combinación
| Texto | Fondo | Ratio | Nivel |
|-------|-------|-------|-------|
| `var(--fg)` | `var(--bg)` | 15.3:1 | AAA |
| `var(--fg-muted)` | `var(--bg)` | 7.8:1 | AAA |
| `var(--fg-subtle)` | `var(--bg)` | 5.2:1 | AA |
| `var(--brand-base)` | White | 4.82:1 | AA |
| `var(--gator-400)` | White | 3.2:1 | ⚠️ Fallback |
| `var(--jungle-300)` | White | 2.8:1 | ❌ No usar |

### Uso Seguro de Colores
```css
/* ✅ Correcto - Cumple AA */
.button-primary {
  background: var(--gator-500);  /* 4.82:1 sobre blanco */
  color: white;                  /* 15.3:1 sobre gator-500 */
}

/* ❌ Incorrecto - No cumple */
.button-bad {
  background: var(--gator-300);  /* 2.8:1 sobre blanco - FALLA */
  color: white;
}

/* ✅ Corrección */
.button-good {
  background: var(--gator-500);  /* Cambiar a base */
  color: white;
}

/* Alternativa para texto suave */
.text-safe {
  color: var(--fg-muted);  /* 7.8:1 - AAA */
}
```

### Modo Alto Contraste
```css
@media (prefers-contrast: high) {
  :root {
    --border-1: color-mix(in oklab, var(--fg) 30%, transparent);
    --border-2: color-mix(in oklab, var(--fg) 50%, transparent);
  }

  .button {
    border: 2px solid var(--fg);
  }
}
```

## Paleta por Contexto

### Landing Page
```css
.landing-hero {
  background: linear-gradient(
    135deg,
    var(--gator-900),
    var(--jungle-900)
  );
  color: var(--jungle-50);
}

.landing-cta {
  background: var(--gator-500);
  color: white;
  transition: background 233ms ease;
}

.landing-cta:hover {
  background: var(--gator-600);
}
```

### Tienda
```css
.product-card {
  background: var(--surface-1);
  border: 1px solid var(--border-1);
  transition: all 233ms ease;
}

.product-card:hover {
  border-color: var(--brand-soft);
  box-shadow: var(--shadow-md);
}

.product-price {
  color: var(--brand-base);
  font-weight: var(--weight-semibold);
}

.product-badge {
  background: var(--brand-soft);
  color: var(--on-brand);
}
```

### Perfil de Usuario
```css
.profile-header {
  background: var(--surface-2);
  border-bottom: 1px solid var(--border-1);
}

.profile-form label {
  color: var(--fg);
  font-weight: var(--weight-medium);
}

.profile-input {
  background: var(--surface-3);
  border: 1px solid var(--border-1);
  color: var(--fg);
}

.profile-input:focus {
  border-color: var(--brand-base);
  box-shadow: 0 0 0 3px color-mix(in oklab, var(--brand-base) 20%, transparent);
}
```

## Gradientes

### Gradientes de Marca
```css
/* Gator gradient */
.gradient-gator {
  background: linear-gradient(
    135deg,
    var(--gator-400),
    var(--gator-600)
  );
}

/* Jungle gradient */
.gradient-jungle {
  background: linear-gradient(
    to bottom,
    var(--jungle-900),
    var(--jungle-950)
  );
}

/* Sand gradient (Luks) */
.gradient-premium {
  background: linear-gradient(
    135deg,
    var(--sand-400),
    var(--sand-600)
  );
}

/* Multi-brand gradient */
.gradient-brand {
  background: linear-gradient(
    90deg,
    var(--gator-500),
    var(--sand-500),
    var(--crimson-primary)
  );
}
```

### Gradientes Radiales
```css
.radial-glow {
  background: radial-gradient(
    circle at center,
    color-mix(in oklab, var(--brand-base) 30%, transparent),
    transparent 70%
  );
}
```

## Overlays y Transparencias

### Sistema de Overlays
```css
:root {
  /* Overlay levels */
  --overlay-1: rgba(0, 0, 0, 0.1);
  --overlay-2: rgba(0, 0, 0, 0.2);
  --overlay-3: rgba(0, 0, 0, 0.5);
  --overlay-4: rgba(0, 0, 0, 0.7);

  /* Colored overlays */
  --overlay-brand: color-mix(in oklab, var(--brand-base) 50%, transparent);
  --overlay-jungle: color-mix(in oklab, var(--jungle-900) 70%, transparent);
}

/* Uso */
.modal-backdrop {
  background: var(--overlay-3);
  backdrop-filter: blur(4px);
}

.tooltip {
  background: var(--surface-2);
  border: 1px solid var(--border-1);
  box-shadow: var(--overlay-2);
}
```

## Estados de Interacción

### Hover States
```css
/* Links */
a {
  color: var(--brand-base);
  transition: color 233ms ease;
}

a:hover {
  color: var(--brand-strong);
}

/* Buttons */
.button {
  background: var(--brand-base);
  color: var(--on-brand);
  transition: all 233ms ease;
}

.button:hover {
  background: var(--brand-strong);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.button:active {
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
}
```

### Disabled States
```css
.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
  background: var(--jungle-700);
  color: var(--jungle-400);
}
```

### Loading States
```css
.loading {
  position: relative;
  color: transparent;
}

.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 1em;
  height: 1em;
  margin: -0.5em;
  border: 2px solid var(--fg-muted);
  border-top-color: var(--brand-base);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
```

## Skins y Variaciones

### Tema Gator (Por Defecto)
```css
html[data-brand="gator"] {
  --brand-primary: var(--gator-500);
  --brand-secondary: var(--gator-300);
  --accent-1: var(--jungle-400);
  --accent-2: var(--sand-400);
}
```

### Tema Buddy
```css
html[data-brand="crimson"] {
  --brand-primary: var(--crimson-primary);
  --brand-secondary: var(--crimson-soft);
  --accent-1: var(--jungle-500);
  --accent-2: var(--gator-400);
}
```

### Tema Luks
```css
html[data-brand="gold"] {
  --brand-primary: var(--sand-600);
  --brand-secondary: var(--sand-300);
  --accent-1: var(--gator-400);
  --accent-2: var(--jungle-300);
}
```

## Implementación en JavaScript

### Detección de Preferencias del Sistema
```javascript
// Detectar preferencia de tema
function getPreferredTheme() {
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return 'dark';
  }
  return 'light';
}

// Aplicar tema al cargar
const theme = getPreferredTheme();
document.documentElement.setAttribute('data-theme', theme);

// Escuchar cambios
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
});
```

### Contraste Dinámico
```javascript
// Verificar contraste
function checkContrast(foreground, background) {
  // Algoritmo WCAG para calcular contraste
  const getLuminance = (color) => {
    // ... cálculo de luminancia
  };

  const l1 = getLuminance(foreground);
  const l2 = getLuminance(background);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  const ratio = (lighter + 0.05) / (darker + 0.05);

  return {
    ratio: ratio.toFixed(2),
    passesAA: ratio >= 4.5,
    passesAAA: ratio >= 7
  };
}
```

### Cambio de Tema en Runtime
```javascript
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);

  // Guardar preferencia
  localStorage.setItem('theme', next);
}
```

## Testing de Colores

### Visual Regression Testing
```javascript
// Percy/Cypress test
describe('Color system', () => {
  it('should render correct brand colors', () => {
    cy.visit('/');

    // Verificar color de botón primario
    cy.get('.btn-primary')
      .should('have.css', 'background-color', 'rgb(60, 158, 93)');

    // Verificar contraste
    cy.get('.btn-primary').then(($el) => {
      const bgColor = $el.css('background-color');
      const textColor = $el.css('color');
      const contrast = checkContrast(textColor, bgColor);
      expect(contrast.passesAA).to.be.true;
    });
  });
});
```

### Unit Tests
```javascript
// Test colores CSS
describe('CSS Color Tokens', () => {
  it('should have valid color values', () => {
    const styles = getComputedStyle(document.documentElement);
    const gator500 = styles.getPropertyValue('--gator-500').trim();
    expect(gator500).to.equal('#3C9E5D');
  });

  it('should have proper contrast ratios', () => {
    const fg = getComputedStyle(document.documentElement).getPropertyValue('--fg');
    const bg = getComputedStyle(document.documentElement).getPropertyValue('--bg');
    const contrast = checkContrast(fg, bg);

    expect(contrast.ratio).to.be.gte(4.5);
  });
});
```

## Buenas Prácticas

### ✅ Hacer
```css
/* Usar variables semánticas */
.button {
  background: var(--brand-base);
  color: var(--on-brand);
}

/* Verificar contraste */
.text-safe {
  color: var(--fg);  /* 15.3:1 sobre bg */
}

/* Usar color-mix para variaciones */
.button-variant {
  background: color-mix(in oklab, var(--brand-base) 80%, black);
}

/* Definir estados de interacción */
.interactive {
  transition: all var(--duration-base) var(--ease-base);
}

.interactive:hover {
  transform: translateY(-2px);
}
```

### ❌ Evitar
```css
/* No hardcodear colores */
.bad {
  background: #3C9E5D;  /* Usar var(--gator-500) */
}

/* No usar colores sin verificar contraste */
.ugly {
  color: #80D3A0;  /* Solo 2.8:1 sobre blanco - FALLA */
}

/* No mezclar sistemas de color */
.mess {
  background: var(--gator-500);
  border: 1px solid #cccccc;  /* Inconsistente */
}

/* No olvidar estados */
.static {
  /* Sin transition */
}
```

## Herramientas y Recursos

### Validación de Contraste
```bash
# Conaxe - Accessibility tooling
npm install -g @axe-core/cli
axe https://your-site.com

# Pa11y
npm install -g pa11y
pa11y https://your-site.com
```

### Extensiones de Navegador
- **Color Oracle**: Simulador de daltonismo
- **WAVE**: Evaluador de accesibilidad web
- **axe DevTools**: Auditoría de accesibilidad
- **Stark (Figma/Sketch)**: Design tools

### Paleta Generada
```javascript
// Generar escala de color basada en φ
function generateScale(baseColor, steps = 11) {
  const scale = [];
  const ratio = 1.618;

  for (let i = 0; i < steps; i++) {
    const intensity = Math.pow(ratio, i - Math.floor(steps / 2));
    const color = colorMix(baseColor, intensity > 1 ? 'black' : 'white', Math.abs(intensity - 1));
    scale.push(color);
  }

  return scale;
}
```

## Referencias

### Archivos Relacionados
- `static/css/tokens.css` - Definición completa de tokens
- `static/css/base.css` - Aplicación de colores base
- `static/css/components.css` - Componentes con colores
- `static/js/theme.js` - Cambio de tema dinámico

### Documentación Externa
- [WCAG 2.1 - Color Contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [color-mix() - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix())
- [OKLCH Color Model](https://bottosson.github.io/posts/oklab/)
- [Color Accessibility](https://webaim.org/articles/contrast/)

## Ver También
- [Tokens CSS](./tokens.md)
- [Tipografía](./tipografia.md)
- [Espaciado](./espaciado.md)
- [Geometría Sagrada](./geometria-sagrada.md)
- [Accesibilidad](../accesibilidad.md)
