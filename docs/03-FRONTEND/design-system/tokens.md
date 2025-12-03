# Design System - Tokens CSS

## Resumen
El sistema de tokens CSS de Croody está basado en principios de **Geometría Sagrada** y el **número áureo** (φ = 1.618). Define variables CSS reutilizables para colores, tipografía, espaciado, radios, sombras y más.

## Ubicación
`/proyecto_integrado/Croody/static/css/tokens.css` (307 líneas)

## Principios Fundamentales

### Número Áureo (φ)
```css
/* Base: 8px
 * Progresión: 8 × φⁿ
 */
--space-1: 8px;
--space-2: calc(var(--space-1) * 1.618); /* 13px */
--space-3: calc(var(--space-2) * 1.618); /* 21px */
--space-4: calc(var(--space-3) * 1.618); /* 34px */
--space-5: calc(var(--space-4) * 1.618); /* 55px */
--space-6: calc(var(--space-5) * 1.618); /* 89px */
```

**Ventajas:**
- Proporciones armónicas
- Consistencia visual
- Escalabilidad natural
- Psicología perceptual optimizada

## Paletas de Color

### 1. Gator (Verde Primario)

**Uso:** Marca principal, CTAs, elementos interactivos

```css
:root, html[data-theme="dark"] {
  /* Gator (Verde Corporativo) */
  --gator-950: #041009;
  --gator-900: #082015;
  --gator-800: #103924;
  --gator-700: #1C5C37;
  --gator-600: #277947;
  --gator-500: #3C9E5D;  /* Base - Color principal */
  --gator-400: #5BB97D;
  --gator-300: #80D3A0;
  --gator-200: #B4E5C6;
  --gator-100: #DDF6E8;
  --gator-50:  #F0FBF5;
}
```

**Aplicación típica:**
- `--gator-500`: Botones primarios, enlaces, iconos
- `--gator-600`: Hover de botones
- `--gator-700`: Active/pressed states
- `--gator-300`: Elementos sutiles, borders

### 2. Jungle (Neutros)

**Uso:** Fondos, superficies, texto

```css
:root, html[data-theme="dark"] {
  /* Jungle (Gris-Verde Neutros) */
  --jungle-950: #050807;  /* Fondo más oscuro */
  --jungle-900: #0B1311;
  --jungle-800: #141F1B;
  --jungle-700: #1E2C26;
  --jungle-600: #293833;
  --jungle-500: #374640;
  --jungle-400: #56655F;
  --jungle-300: #7A8883;
  --jungle-200: #A9B4B0;
  --jungle-100: #D3DAD7;
  --jungle-50:  #EEF1EF;  /* Fondo claro */
}
```

**Aplicación:**
- Fondo principal: `--jungle-950` (dark), `--jungle-50` (light)
- Superficies: `--jungle-900` (dark), `--jungle-100` (light)
- Texto: `--jungle-50` (dark), `--jungle-900` (light)
- Borders: `--jungle-700`, `--jungle-600`

### 3. Sand (Dorado Cálido)

**Uso:** Marca Luks, elementos premium

```css
:root {
  /* Sand (Dorado) */
  --sand-600: #C18F4A;  /* Luks primary */
  --sand-500: #E0B771;
  --sand-400: #F3D398;
  --sand-300: #F8E1B7;
  --sand-200: #FBECD1;
  --sand-100: #FDF5E6;
}
```

### 4. Crimson (Rojo)

**Uso:** Marca Buddy, alertas, urgencia

```css
:root {
  /* Crimson (Rojo) */
  --crimson-deep: #7A1E2A;
  --crimson-primary: #E04F56;  /* Buddy primary */
  --crimson-soft: #FFA7B5;
}
```

### 5. Semantic Colors

```css
:root {
  /* Feedback States */
  --info-500:  #31BFEA;  /* Información */
  --warn-500:  #F5B454;  /* Advertencia */
  --error-500: #F06565;  /* Error */
  --success-500: #4CAF50; /* Éxito */

  /* Brand Overrides */
  --brand-base: var(--gator-500);
  --brand-strong: var(--gator-600);
  --brand-soft: var(--gator-300);

  --on-brand: #FFFFFF;  /* Texto sobre brand */
}
```

## Variables Dinámicas de Tema

### Dark Theme (Default)
```css
:root, html[data-theme="dark"] {
  /* Backgrounds */
  --bg: var(--jungle-950);
  --surface-1: var(--jungle-900);
  --surface-2: var(--jungle-800);
  --surface-3: var(--jungle-700);

  /* Text */
  --fg: var(--jungle-50);
  --fg-muted: var(--jungle-200);
  --fg-subtle: var(--jungle-300);

  /* Borders */
  --border-1: color-mix(in oklab, var(--fg) 10%, transparent);
  --border-2: color-mix(in oklab, var(--fg) 20%, transparent);

  /* Interactive */
  --focus-ring: var(--orchid-500);
}
```

### Light Theme
```css
html[data-theme="light"] {
  /* Backgrounds */
  --bg: var(--gator-50);
  --surface-1: var(--gator-100);
  --surface-2: var(--gator-200);
  --surface-3: var(--gator-300);

  /* Text */
  --fg: var(--jungle-900);
  --fg-muted: var(--jungle-600);
  --fg-subtle: var(--jungle-500);

  /* Borders */
  --border-1: color-mix(in oklab, var(--fg) 10%, transparent);
  --border-2: color-mix(in oklab, var(--fg) 15%, transparent);

  /* Interactive */
  --focus-ring: var(--orchid-500);
}
```

## Tipografía

### Font Stack
```css
:root {
  /* Sans-serif (Body) */
  --font-sans: "Josefin Sans", -apple-system, BlinkMacSystemFont,
               "Segoe UI", Roboto, "Helvetica Neue", Arial,
               "Noto Sans", sans-serif;

  /* Display (Headings) */
  --font-display: "Baloo 2", var(--font-sans);

  /* Fallbacks */
  --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo,
               Consolas, "Liberation Mono", monospace;
}
```

### Escala Tipográfica (Basada en φ)
```css
:root {
  /* Text Sizes */
  --text-xs: 0.78rem;   /* 12.5px */
  --text-sm: 0.9rem;    /* 14.4px */
  --text-base: 1rem;    /* 16px - Root */
  --text-lg: 1.15rem;   /* 18.4px */
  --text-xl: 1.33rem;   /* 21.3px */
  --text-2xl: 1.6rem;   /* 25.6px */
  --text-3xl: 2.1rem;   /* 33.6px */
  --text-4xl: clamp(2.3rem, 2vw + 2rem, 3.6rem); /* Responsive */
}
```

### Line Heights
```css
:root {
  /* Line Heights */
  --leading-tight: 1.15;   /* Headings */
  --leading-snug: 1.35;
  --leading-base: 1.55;    /* Body text */
  --leading-relaxed: 1.75; /* Long text */
  --leading-loose: 2;      /* Pull quotes */
}
```

### Font Weights
```css
:root {
  --weight-light: 300;
  --weight-normal: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;
  --weight-extrabold: 800;
}
```

## Espaciado (Golden Ratio Scale)

```css
:root {
  /* Base: 8px */
  --space-1: 8px;
  --space-2: 13px;   /* 8 × 1.618 */
  --space-3: 21px;   /* 13 × 1.618 */
  --space-4: 34px;   /* 21 × 1.618 */
  --space-5: 55px;   /* 34 × 1.618 */
  --space-6: 89px;   /* 55 × 1.618 */

  /* Half steps */
  --space-half-1: 4px;
  --space-half-2: 6.5px;
  --space-half-3: 10.5px;

  /* Quarter steps */
  --space-quarter-1: 2px;
  --space-quarter-2: 3.25px;
  --space-quarter-3: 5.25px;
}
```

### Uso en CSS
```css
.component {
  /* Using space tokens */
  padding: var(--space-3) var(--space-4);
  margin-bottom: var(--space-5);

  /* Responsive spacing */
  gap: clamp(var(--space-2), 2vw, var(--space-4));
}
```

## Radios (Border Radius)

```css
:root {
  /* Scales */
  --radius-1: 6px;   /* Small elements */
  --radius-2: 10px;  /* Medium elements */
  --radius-3: 16px;  /* Large elements */
  --radius-4: 24px;  /* Extra large */

  /* Special */
  --radius-full: 9999px; /* Circle */
  --radius-pill: 1000px; /* Pills */
}
```

## Sombras (Elevation)

```css
:root {
  /* Shadow Steps */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 4px 12px rgba(20, 30, 20, 0.08);
  --shadow-md: 0 10px 30px rgba(20, 50, 30, 0.12);
  --shadow-lg: 0 25px 55px rgba(32, 80, 50, 0.20);
  --shadow-xl: 0 50px 100px rgba(32, 80, 50, 0.25);

  /* Colored shadows (brand) */
  --shadow-brand: 0 8px 24px color-mix(in oklab, var(--brand-base) 30%, transparent);
}
```

### Uso
```css
.card {
  box-shadow: var(--shadow-md);
  transition: box-shadow 233ms ease;
}

.card:hover {
  box-shadow: var(--shadow-lg);
}
```

## Z-Index Scale

```css
:root {
  /* Z-Index Scale */
  --z-base: 0;
  --z-dropdown: 10;
  --z-sticky: 100;
  --z-drawer: 1000;
  --z-modal: 10000;
  --z-tooltip: 11000;
  --z-toast: 12000;
}
```

## Breakpoints

```css
:root {
  /* Breakpoints */
  --bp-sm: 480px;
  --bp-md: 768px;
  --bp-lg: 1024px;
  --bp-xl: 1280px;
  --bp-2xl: 1536px;

  /* Container widths */
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  --container-2xl: 1536px;
}
```

## Grid System

```css
:root {
  /* Columns */
  --grid-cols-mobile: 5;
  --grid-cols-tablet: 8;
  --grid-cols-desktop: 12;
  --grid-cols-wide: 13;

  /* Gutters */
  --gutter: 24px;

  /* Container padding */
  --container-pad-mobile: 21px;
  --container-pad-tablet: 34px;
  --container-pad-desktop: 55px;
}
```

## Transiciones

```css
:root {
  /* Durations */
  --duration-fast: 100ms;
  --duration-base: 233ms;  /* Golden ratio based */
  --duration-slow: 377ms;
  --duration-slower: 610ms;

  /* Easing */
  --ease-linear: linear;
  --ease-base: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  /* Default transition */
  --transition: all var(--duration-base) var(--ease-base);
}
```

## Brand Switching

### Gator (Default)
```css
:root, html[data-brand="gator"] {
  --brand-base: var(--gator-500);
  --brand-strong: var(--gator-600);
  --brand-soft: var(--gator-300);
}
```

### Crimson (Buddy)
```css
html[data-brand="crimson"] {
  --brand-base: var(--crimson-primary);
  --brand-strong: var(--crimson-deep);
  --brand-soft: var(--crimson-soft);
}
```

### Gold (Luks)
```css
html[data-brand="gold"] {
  --brand-base: var(--sand-600);
  --brand-strong: var(--sand-500);
  --brand-soft: var(--sand-400);
}
```

## Accesibilidad

### Focus Rings
```css
:root {
  /* Focus styles */
  --focus-ring-width: 2px;
  --focus-ring-offset: 3px;
  --focus-ring-color: var(--orchid-500);
  --focus-ring: var(--focus-ring-width) solid var(--focus-ring-color);
}

*:focus-visible {
  outline: var(--focus-ring);
  outline-offset: var(--focus-ring-offset);
}
```

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Color Scheme
```css
:root {
  color-scheme: light dark;
}

html[data-theme="light"] {
  color-scheme: light;
}

html[data-theme="dark"] {
  color-scheme: dark;
}
```

## Uso en Componentes

### Botón Primario
```css
.btn-primary {
  /* Using tokens */
  background: var(--brand-strong);
  color: var(--on-brand);

  /* Spacing */
  padding: var(--space-2) var(--space-4);
  margin: var(--space-2) 0;

  /* Border radius */
  border-radius: var(--radius-2);

  /* Shadow */
  box-shadow: var(--shadow-sm);

  /* Transition */
  transition: var(--transition);

  /* States */
  &:hover {
    background: var(--brand-base);
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
  }

  &:active {
    transform: translateY(0);
    box-shadow: var(--shadow-xs);
  }
}
```

### Card Component
```css
.card {
  /* Using surface tokens */
  background: var(--surface-1);

  /* Spacing */
  padding: var(--space-3);

  /* Border radius */
  border-radius: var(--radius-3);

  /* Shadow */
  box-shadow: var(--shadow-md);

  /* Border */
  border: 1px solid var(--border-1);

  /* Responsive spacing */
  gap: clamp(var(--space-2), 2vw, var(--space-4));
}
```

### Form Input
```css
.input {
  /* Background */
  background: var(--surface-2);
  color: var(--fg);

  /* Spacing */
  height: 48px;
  padding: 0 var(--space-3);

  /* Border */
  border: 1px solid var(--border-1);
  border-radius: var(--radius-2);

  /* Transition */
  transition: var(--transition);

  &:focus {
    outline: none;
    border-color: var(--brand-base);
    box-shadow: 0 0 0 var(--focus-ring-offset) color-mix(in oklab, var(--brand-base) 20%, transparent);
  }
}
```

## Utils

### Espaciado
```css
/* Margin utilities */
.m-1 { margin: var(--space-1); }
.m-2 { margin: var(--space-2); }
.m-3 { margin: var(--space-3); }
.m-4 { margin: var(--space-4); }
.m-5 { margin: var(--space-5); }
.m-6 { margin: var(--space-6); }

.mt-1 { margin-top: var(--space-1); }
.mt-2 { margin-top: var(--space-2); }
.mt-3 { margin-top: var(--space-3); }
.mt-4 { margin-top: var(--space-4); }
.mt-5 { margin-top: var(--space-5); }
.mt-6 { margin-top: var(--space-6); }

/* Similar for mb-, ml-, mr-, p-, pt-, pb-, pl-, pr- */
```

### Colores
```css
/* Text colors */
.text-primary { color: var(--brand-base); }
.text-muted { color: var(--fg-muted); }
.text-subtle { color: var(--fg-subtle); }

/* Background colors */
.bg-primary { background: var(--brand-base); }
.bg-surface { background: var(--surface-1); }
.bg-brand { background: var(--brand-soft); }
```

## Buenas Prácticas

### 1. Usar tokens, no valores hard-coded
```css
/* Bad */
.component {
  padding: 16px;
  color: #3C9E5D;
}

/* Good */
.component {
  padding: var(--space-3);
  color: var(--brand-base);
}
```

### 2. Componer con tokens
```css
/* Good */
.card {
  background: var(--surface-1);
  padding: var(--space-3);
  border-radius: var(--radius-3);
  border: 1px solid var(--border-1);
}
```

### 3. Usar color-mix para variaciones
```css
/* Good */
.button-variant {
  background: color-mix(in oklab, var(--brand-base) 80%, black);
}

/* Bad */
.button-variant {
  background: #277947;  /* Hard-coded */
}
```

### 4. Respetar accesibilidad
```css
/* Good */
.link {
  color: var(--brand-base);
  transition: var(--transition);

  &:hover {
    color: var(--brand-strong);
  }
}
```

## Testing de Tokens

### Verificar Contraste
```javascript
// Herramienta para verificar contraste
function checkContrast(foreground, background) {
  // Usar librerías como 'color-contrast-checker'
}
```

### Visual Regression
```bash
# Con Percy, Chromatic, etc.
percy exec -- playwright test
```

## Referencias

### Archivos Relacionados
- `static/css/base.css` - Estilos base usando tokens
- `static/css/components.css` - Componentes con tokens
- `static/css/animations.css` - Animaciones con tokens

### Recursos Externos
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [Color-mix()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix())
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Golden Ratio in Design](https://www.smashingmagazine.com/2014/05/design-principles-visual-weight-golden-ratio/)

## Ver También
- [Tipografía](./tipografia.md)
- [Colores](./colores.md)
- [Espaciado](./espaciado.md)
- [Geometría Sagrada](./geometria-sagrada.md)
