# Sistema Tipográfico - Documentación Completa

## Resumen
El sistema tipográfico de Croody implementa una jerarquía clara basada en principios de **Geometría Sagrada** y **modular scale**. Utiliza dos fuentes principales: **Josefin Sans** para texto corrido y **Baloo 2** para títulos.

## Fuentes Principales

### 1. Josefin Sans (Sans-serif Principal)

**Uso:** Body text, UI elements, navegación, formularios

**Características:**
- Fuente variable (weights 100-700)
- Excelente legibilidad en pantallas
- Geométrica con toques humanistas
- Optimizada para idiomas latinos
- Tamaño total: ~28.5 KB (WOFF2)

**Font Stack:**
```css
--font-sans: "Josefin Sans",
             -apple-system,
             BlinkMacSystemFont,
             "Segoe UI",
             Roboto,
             "Helvetica Neue",
             Arial,
             "Noto Sans",
             sans-serif;
```

**Fallback Strategy:**
1. **Josefin Sans** - Fuente personalizada
2. **-apple-system** - San Francisco (iOS)
3. **BlinkMacSystemFont** - San Francisco (macOS Chrome)
4. **Segoe UI** - Windows
5. **Roboto** - Android
6. **Helvetica Neue** - macOS anterior
7. **Arial** - Windows anterior
8. **Noto Sans** - Cobertura internacional
9. **sans-serif** - Genérico final

### 2. Baloo 2 (Display Font)

**Uso:** Headings, títulos, display text, hero sections

**Características:**
- Fuente variable (weights 400-800)
- Redondeada y friendly
- Alta legibilidad en títulos
- Personalidad cálida y accesible
- Tamaño total: ~33.2 KB (WOFF2)

**Font Stack:**
```css
--font-display: "Baloo 2",
                var(--font-sans);
```

**Fallback:** Usa Josefin Sans si Baloo 2 no está disponible

### 3. Monospace (Coding)

**Uso:** Code blocks, datos técnicos

```css
--font-mono: ui-monospace,
             SFMono-Regular,
             "SF Mono",
             Menlo,
             Consolas,
             "Liberation Mono",
             monospace;
```

## Jerarquía Tipográfica

### Escala Modular (Basada en φ)

**Ratios aplicados:**
- Major Third (1.25)
- Perfect Fourth (1.333)
- Perfect Fifth (1.5)
- Golden Ratio (1.618)

**Tamaños:**
```css
:root {
  /* Base: 16px = 1rem */
  --text-xs: 0.78rem;   /* 12.5px - Captions */
  --text-sm: 0.9rem;    /* 14.4px - Small text */
  --text-base: 1rem;    /* 16px - Body default */
  --text-lg: 1.15rem;   /* 18.4px - Large body */
  --text-xl: 1.33rem;   /* 21.3px - Small headings */
  --text-2xl: 1.6rem;   /* 25.6px - H6 */
  --text-3xl: 2.1rem;   /* 33.6px - H5 */
  --text-4xl: clamp(2.3rem, 2vw + 2rem, 3.6rem); /* H4 responsive */
  --text-5xl: clamp(2.8rem, 3vw + 2rem, 4.5rem); /* H3 responsive */
  --text-6xl: clamp(3.4rem, 4vw + 2rem, 5.6rem); /* H2 responsive */
  --text-7xl: clamp(4.2rem, 5vw + 2rem, 7rem);   /* H1 responsive */
}
```

### Aplicación por Elemento

#### Headings
```css
h1, .h1 {
  font-family: var(--font-display);
  font-size: var(--text-7xl);
  font-weight: var(--weight-bold);
  line-height: var(--leading-tight);
  letter-spacing: -0.02em;
}

h2, .h2 {
  font-family: var(--font-display);
  font-size: var(--text-6xl);
  font-weight: var(--weight-bold);
  line-height: var(--leading-tight);
  letter-spacing: -0.015em;
}

h3, .h3 {
  font-family: var(--font-display);
  font-size: var(--text-5xl);
  font-weight: var(--weight-semibold);
  line-height: var(--leading-snug);
  letter-spacing: -0.01em;
}

h4, .h4 {
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: var(--weight-semibold);
  line-height: var(--leading-snug);
}

h5, .h5 {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--weight-semibold);
  line-height: var(--leading-base);
}

h6, .h6 {
  font-family: var(--font-sans);
  font-size: var(--text-2xl);
  font-weight: var(--weight-medium);
  line-height: var(--leading-base);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

#### Body Text
```css
body, p, .text-body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  font-weight: var(--weight-normal);
  line-height: var(--leading-base);
  color: var(--fg);
}

.text-large {
  font-size: var(--text-lg);
  line-height: var(--leading-snug);
}

.text-small {
  font-size: var(--text-sm);
  line-height: var(--leading-base);
}

.text-xs {
  font-size: var(--text-xs);
  line-height: var(--leading-base);
}
```

#### UI Elements
```css
.button-text {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  letter-spacing: 0.025em;
}

.nav-link {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  font-weight: var(--weight-medium);
}

.input-text {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  font-weight: var(--weight-normal);
}
```

## Line Heights

### Escala de Line Heights
```css
:root {
  --leading-tight: 1.15;    /* Títulos, elementos compactos */
  --leading-snug: 1.35;     /* Títulos pequeños */
  --leading-base: 1.55;     /* Texto corrido */
  --leading-relaxed: 1.75;  /* Texto largo, legibilidad */
  --leading-loose: 2;       /* Pull quotes, énfasis */
}
```

### Aplicación
```css
/* Headings */
h1, h2, h3 {
  line-height: var(--leading-tight);
}

h4, h5, h6 {
  line-height: var(--leading-snug);
}

/* Body */
p, li {
  line-height: var(--leading-base);
}

/* Long text */
.article p,
.text-relaxed {
  line-height: var(--leading-relaxed);
}

/* Quotes */
blockquote {
  line-height: var(--leading-loose);
}
```

## Font Weights

### Disponibles
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

### Uso Recomendado

#### Body Text
```css
.text-light {
  font-weight: var(--weight-light);
}

.text-regular {
  font-weight: var(--weight-normal);
}

.text-medium {
  font-weight: var(--weight-medium);
}
```

#### Headings
```css
h1, h2 {
  font-weight: var(--weight-bold); /* 700 */
}

h3, h4 {
  font-weight: var(--weight-semibold); /* 600 */
}

h5, h6 {
  font-weight: var(--weight-medium); /* 500 */
}
```

#### Emphasis
```css
strong, .text-bold {
  font-weight: var(--weight-bold);
}

.text-semibold {
  font-weight: var(--weight-semibold);
}

.text-medium {
  font-weight: var(--weight-medium);
}
```

## Letter Spacing

### Tracking
```css
:root {
  /* Tracking */
  --tracking-tight: -0.02em;   /* Large headings */
  --tracking-snug: -0.01em;    /* Medium headings */
  --tracking-base: 0;          /* Body */
  --tracking-wide: 0.01em;     /* Small text */
  --tracking-wider: 0.05em;    /* Uppercase */
  --tracking-widest: 0.1em;    /* Extra wide */
}
```

### Aplicación
```css
h1, h2 {
  letter-spacing: var(--tracking-tight);
}

h3, h4 {
  letter-spacing: var(--tracking-snug);
}

.text-uppercase {
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
}
```

## Responsive Typography

### Clamp Function
```css
/* Scalable text with clamp */
.text-fluid {
  font-size: clamp(1rem, 2vw, 1.5rem);
}

/* Breakdown */
.text-responsive {
  /* Mobile: 1rem, Desktop: 1.5rem */
  font-size: clamp(1rem, 0.5rem + 2vw, 1.5rem);
}
```

### Responsive Headings
```css
/* H1 responsive */
h1 {
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  /* Alternative with min, fluid, max */
  font-size: clamp(
    2.5rem,  /* minimum */
    1rem + 5vw,  /* fluid */
    4.5rem  /* maximum */
  );
}

/* H2 responsive */
h2 {
  font-size: clamp(2rem, 4vw, 3.5rem);
}

/* H3 responsive */
h3 {
  font-size: clamp(1.75rem, 3vw, 2.75rem);
}
```

### Fluid Type Scale
```css
/* Container-based sizing */
@media (min-width: 768px) {
  h1 {
    font-size: calc(1.5rem + 3vw);
  }
}

@media (min-width: 1024px) {
  h1 {
    font-size: calc(2rem + 2vw);
  }
}
```

## Optimización de Performance

### Font Loading Strategy

#### 1. Preload Critical Fonts
```html
<link
  rel="preload"
  href="fonts/JosefinSans-Variable.woff2"
  as="font"
  type="font/woff2"
  crossorigin
>

<link
  rel="preload"
  href="fonts/Baloo2-Latin.woff2"
  as="font"
  type="font/woff2"
  crossorigin
>
```

#### 2. Font Display Swap
```css
@font-face {
  font-family: 'Josefin Sans';
  src: url('fonts/JosefinSans-Variable.woff2') format('woff2');
  font-weight: 100 700;
  font-style: normal;
  font-display: swap;  /* Evita FOIT */
}
```

#### 3. CSS Font Loading API
```javascript
// JavaScript para optimizar carga
if ('fonts' in document) {
  // Cargar fonts de manera inteligente
  document.fonts.load('400 1em Josefin Sans');
  document.fonts.load('700 1em Baloo 2');
}
```

### Subsetting
```bash
# Herramientas como glyphhanger o subset-font
# Para reducir tamaño de fuentes

# Ejemplo con glyphhanger
glyphhanger --formats=woff2 --whitelist=U+0020-007E
```

## Internacionalización

### Soporte Multi-idioma

#### Fuentes por Idioma
```css
/* Árabe */
html[lang="ar"] {
  font-family: "Noto Sans Arabic", "Amiri", var(--font-sans);
}

/* Chino */
html[lang="zh-hans"] {
  font-family: "Noto Sans SC", "Source Han Sans", var(--font-sans);
}

/* Japonés */
html[lang="ja"] {
  font-family: "Noto Sans JP", "Hiragino Sans", var(--font-sans);
}

/* Hindi */
html[lang="hi"] {
  font-family: "Noto Sans Devanagari", "Mangal", var(--font-sans);
}
```

#### Fallback Strategy
```css
.font-international {
  /* Primary: Josefin Sans (Latin) */
  font-family: var(--font-sans);

  /* Fallbacks with coverage */
  font-family:
    var(--font-sans),
    "Noto Sans",     /* Wide coverage */
    "Segoe UI",      /* Windows */
    "Apple Color Emoji", /* Emojis */
    sans-serif;      /* Final fallback */
}
```

## Accesibilidad

### Tamaño Mínimo
```css
/* WCAG AA: 16px mínimo para body text */
body {
  font-size: 1rem; /* 16px */
}

/* Permitir zoom hasta 200% */
.text-responsive {
  font-size: clamp(1rem, 2vw, 1.125rem);
}
```

### Line Length
```css
.text-readable {
  /* 45-75 caracteres por línea */
  max-width: 65ch;  /* ch unit = width of '0' */
}

/* En contenedores */
.container-text {
  max-width: 60ch;
  margin: 0 auto;
}
```

### Contraste
```css
/* Asegurar contraste adecuado */
.text-primary {
  color: var(--brand-base); /* Alto contraste con fondo */
}

.text-muted {
  color: var(--fg-muted); /* Cumple WCAG AA */
}
```

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  /* Evitar animaciones de text */
  * {
    text-shadow: none !important;
    transition: none !important;
  }
}
```

## Uso en Componentes

### Hero Section
```css
.hero-title {
  font-family: var(--font-display);
  font-size: var(--text-7xl);
  font-weight: var(--weight-bold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
}

.hero-subtitle {
  font-family: var(--font-sans);
  font-size: var(--text-xl);
  font-weight: var(--weight-light);
  line-height: var(--leading-relaxed);
}
```

### Cards
```css
.card-title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--weight-semibold);
  line-height: var(--leading-snug);
}

.card-text {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  font-weight: var(--weight-normal);
  line-height: var(--leading-base);
}
```

### Navigation
```css
.nav-link {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  font-weight: var(--weight-medium);
  text-decoration: none;
}

.nav-link:hover {
  font-weight: var(--weight-semibold);
}
```

### Buttons
```css
.btn {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  letter-spacing: var(--tracking-wide);
}

.btn-lg {
  font-size: var(--text-base);
}
```

## Utils Classes

### Text Size
```css
.text-xs { font-size: var(--text-xs); }
.text-sm { font-size: var(--text-sm); }
.text-base { font-size: var(--text-base); }
.text-lg { font-size: var(--text-lg); }
.text-xl { font-size: var(--text-xl); }
.text-2xl { font-size: var(--text-2xl); }
.text-3xl { font-size: var(--text-3xl); }
.text-4xl { font-size: var(--text-4xl); }
```

### Text Weight
```css
.font-light { font-weight: var(--weight-light); }
.font-normal { font-weight: var(--weight-normal); }
.font-medium { font-weight: var(--weight-medium); }
.font-semibold { font-weight: var(--weight-semibold); }
.font-bold { font-weight: var(--weight-bold); }
.font-extrabold { font-weight: var(--weight-extrabold); }
```

### Text Style
```css
.italic { font-style: italic; }
.not-italic { font-style: normal; }

.uppercase { text-transform: uppercase; }
.lowercase { text-transform: lowercase; }
.capitalize { text-transform: capitalize; }

.underline { text-decoration: underline; }
.line-through { text-decoration: line-through; }
.no-underline { text-decoration: none; }
```

### Text Alignment
```css
.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-justify { text-align: justify; }
```

### Line Height
```css.leading-tight { line-height: var(--leading-tight); }
.leading-snug { line-height: var(--leading-snug); }
.leading-base { line-height: var(--leading-base); }
.leading-relaxed { line-height: var(--leading-relaxed); }
.leading-loose { line-height: var(--leading-loose); }
```

## Testing

### Legibilidad
```javascript
// Test de legibilidad
function checkReadability(text, fontSize, lineHeight) {
  const charsPerLine = calculateCharsPerLine(text, fontSize);
  return charsPerLine >= 45 && charsPerLine <= 75;
}
```

### Performance
```javascript
// Medir FOUT (Flash of Unstyled Text)
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    if (entry.name === 'first-contentful-paint') {
      console.log('Font loaded before FCP');
    }
  });
});
observer.observe({entryTypes: ['paint']});
```

### Accesibilidad
```javascript
// Verificar tamaño mínimo
function checkMinFontSize(element) {
  const computedSize = window.getComputedStyle(element).fontSize;
  return parseFloat(computedSize) >= 16;
}
```

## Herramientas

### Generación de Scales
```javascript
// Generar escala tipográfica
function generateTypeScale(base, ratio) {
  const scale = [base];
  for (let i = 1; i <= 6; i++) {
    scale.push(base * Math.pow(ratio, i));
  }
  return scale;
}

// Ejemplo: base 16px, ratio 1.618
const scale = generateTypeScale(16, 1.618);
console.log(scale); // [16, 25.9, 41.9, 67.8, 109.7, 177.5, 287.3]
```

### Visualización
```bash
# Herramientas como Type Scale
# https://type-scale.com/

# Instalación local
npm install -g type-scale-cli
type-scale
```

## Buenas Prácticas

### 1. Usar rem para escalabilidad
```css
/* Good */
h1 {
  font-size: 2.5rem; /* Scalable */
}

/* Bad */
h1 {
  font-size: 40px; /* Fixed */
}
```

### 2. Line height relativo
```css
/* Good */
p {
  line-height: 1.6; /* Unitless, relative */
}

/* Bad */
p {
  line-height: 25.6px; /* Fixed */
}
```

### 3. Preferir font-display: swap
```css
@font-face {
  font-family: 'Custom';
  src: url('font.woff2');
  font-display: swap; /* Evita FOIT */
}
```

### 4. Testing en múltiples dispositivos
```javascript
// Test responsive typography
const viewports = [
  { width: 375, name: 'Mobile' },
  { width: 768, name: 'Tablet' },
  { width: 1024, name: 'Desktop' },
  { width: 1440, name: 'Wide' }
];
```

## Referencias

### Archivos Relacionados
- `static/css/tokens.css` - Definición de tokens tipográficos
- `static/css/base.css` - Estilos base con tipografía
- `templates/base.html` - Preload de fuentes

### Recursos Externos
- [Josefin Sans - Google Fonts](https://fonts.google.com/specimen/Josefin+Sans)
- [Baloo 2 - Google Fonts](https://fonts.google.com/specimen/Baloo+2)
- [Modular Scale](https://www.modularscale.com/)
- [Type Scale Calculator](https://type-scale.com/)
- [Web Typography](https://webtypography.net/)

## Ver También
- [Tokens CSS](./tokens.md)
- [Colores](./colores.md)
- [Geometría Sagrada](./geometria-sagrada.md)
- [Accesibilidad](../accesibilidad.md)
