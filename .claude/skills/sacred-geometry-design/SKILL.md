---
name: sacred-geometry-design
description: Sistema de diseño basado en Geometría Sagrada (φ = 1.618) para Croody. Use cuando trabaje en UI, CSS, templates o cualquier elemento visual del proyecto.
---

# Sacred Geometry Design System

> Sistema de diseño matemáticamente armónico basado en el Número Áureo.

---

## Filosofía

El sistema visual de Croody está basado en el **Número Áureo (φ = 1.618033988749...)** aplicado a:

- **Espaciado**: Secuencia de Fibonacci (8, 13, 21, 34, 55, 89px)
- **Tipografía**: Escala modular basada en φ
- **Proporciones**: Golden rectangles en layouts
- **Timing**: Duraciones basadas en φ (233ms, 377ms)

---

## Tokens de Espaciado

```css
/* Fibonacci sequence */
--space-1: 8px;    /* Base */
--space-2: 13px;   /* 8 × 1.618 ≈ 13 */
--space-3: 21px;   /* 13 × 1.618 ≈ 21 */
--space-4: 34px;   /* 21 × 1.618 ≈ 34 */
--space-5: 55px;   /* 34 × 1.618 ≈ 55 */
--space-6: 89px;   /* 55 × 1.618 ≈ 89 */

/* Half steps */
--space-half-1: 4px;
--space-half-2: 6.5px;
--space-half-3: 10.5px;
```

### Uso

```css
/* Padding de card */
.card {
    padding: var(--space-3);  /* 21px */
}

/* Margin entre secciones */
.section + .section {
    margin-top: var(--space-5);  /* 55px */
}

/* Gap en grid */
.grid {
    gap: var(--space-2);  /* 13px */
}
```

---

## Paletas de Color

### Gator (Verde Corporativo)

```css
--gator-950: #041009;  /* Darkest */
--gator-900: #082015;
--gator-800: #103924;
--gator-700: #1C5C37;
--gator-600: #277947;
--gator-500: #3C9E5D;  /* Base - Brand color */
--gator-400: #5BB97D;
--gator-300: #80D3A0;
--gator-200: #B4E5C6;
--gator-100: #DDF6E8;
--gator-50:  #F0FBF5;  /* Lightest */
```

### Jungle (Neutros)

```css
--jungle-950: #050807;  /* Background dark */
--jungle-900: #0B1311;
--jungle-800: #141F1B;
--jungle-700: #1E2C26;
--jungle-600: #293833;
--jungle-500: #374640;
--jungle-400: #56655F;
--jungle-300: #7A8883;
--jungle-200: #A9B4B0;
--jungle-100: #D3DAD7;
--jungle-50:  #EEF1EF;  /* Background light */
```

### Variables Semánticas

```css
/* Dark Theme (default) */
:root {
    --bg: var(--jungle-950);
    --surface-1: var(--jungle-900);
    --surface-2: var(--jungle-800);
    --fg: var(--jungle-50);
    --fg-muted: var(--jungle-200);
    --brand-base: var(--gator-500);
    --brand-strong: var(--gator-600);
    --on-brand: #FFFFFF;
}

/* Light Theme */
html[data-theme="light"] {
    --bg: var(--gator-50);
    --surface-1: var(--gator-100);
    --fg: var(--jungle-900);
    --brand-strong: var(--gator-300);
}
```

---

## Tipografía

### Font Stack

```css
--font-sans: "Josefin Sans", -apple-system, BlinkMacSystemFont, sans-serif;
--font-display: "Baloo 2", var(--font-sans);
--font-mono: ui-monospace, SFMono-Regular, monospace;
```

### Escala Tipográfica (basada en φ)

```css
--text-xs: 0.78rem;   /* 12.5px */
--text-sm: 0.9rem;    /* 14.4px */
--text-base: 1rem;    /* 16px - Root */
--text-lg: 1.15rem;   /* 18.4px */
--text-xl: 1.33rem;   /* 21.3px */
--text-2xl: 1.6rem;   /* 25.6px */
--text-3xl: 2.1rem;   /* 33.6px */
--text-4xl: clamp(2.3rem, 2vw + 2rem, 3.6rem);
```

### Line Heights

```css
--leading-tight: 1.15;   /* Headings */
--leading-base: 1.55;    /* Body text */
--leading-relaxed: 1.75; /* Long text */
```

---

## Border Radius

```css
--radius-1: 6px;     /* Small elements */
--radius-2: 10px;    /* Buttons, inputs */
--radius-3: 16px;    /* Cards */
--radius-4: 24px;    /* Large cards */
--radius-full: 9999px;  /* Pills, circles */
```

---

## Sombras (Elevation)

```css
--shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-sm: 0 4px 12px rgba(20, 30, 20, 0.08);
--shadow-md: 0 10px 30px rgba(20, 50, 30, 0.12);
--shadow-lg: 0 25px 55px rgba(32, 80, 50, 0.20);
--shadow-xl: 0 50px 100px rgba(32, 80, 50, 0.25);

/* Brand shadow */
--shadow-brand: 0 8px 24px color-mix(in oklab, var(--brand-base) 30%, transparent);
```

---

## Transiciones

```css
/* Duraciones basadas en φ */
--duration-fast: 100ms;
--duration-base: 233ms;   /* Golden ratio: 144 × 1.618 ≈ 233 */
--duration-slow: 377ms;   /* 233 × 1.618 ≈ 377 */
--duration-slower: 610ms; /* 377 × 1.618 ≈ 610 */

/* Easing */
--ease-base: cubic-bezier(0.4, 0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);

/* Shorthand */
--transition: all var(--duration-base) var(--ease-base);
```

---

## Componentes Patterns

### Button Primary

```css
.btn-primary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-2);

    min-height: 48px;
    padding: var(--space-2) var(--space-4);

    font-family: var(--font-sans);
    font-size: var(--text-base);
    font-weight: 600;

    background: var(--brand-strong);
    color: var(--on-brand);

    border: none;
    border-radius: var(--radius-2);

    box-shadow: var(--shadow-sm);
    transition: var(--transition);
}

.btn-primary:hover {
    background: var(--brand-base);
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}

.btn-primary:active {
    transform: translateY(0) scale(0.98);
}
```

### Vector Card

```css
.vector-card {
    display: flex;
    flex-direction: column;
    padding: var(--space-3);
    gap: var(--space-2);

    background: var(--surface-1);
    border: 1px solid var(--border-1);
    border-radius: var(--radius-3);

    box-shadow: var(--shadow-md);
    transition: var(--transition);
}

.vector-card:hover {
    transform: translateY(-4px) scale(1.01);
    box-shadow: var(--shadow-lg);
    border-color: color-mix(in oklab, var(--brand-base) 40%, transparent);
}
```

### Fade In Animation

```css
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp var(--duration-slow) var(--ease-base) forwards;
}

/* Staggered delays */
.fade-in-up:nth-child(1) { animation-delay: 0ms; }
.fade-in-up:nth-child(2) { animation-delay: 100ms; }
.fade-in-up:nth-child(3) { animation-delay: 200ms; }
.fade-in-up:nth-child(4) { animation-delay: 300ms; }
```

---

## Zones de Expresividad

| Zone | Uso | Elementos |
|------|-----|-----------|
| **HIGH** | Celebrations, hero sections | Glows, animaciones complejas |
| **MEDIUM** | Cards, interactivos | Hover effects, shimmer |
| **LOW** | Functional UI | Minimal transitions |

### HIGH Zone Example
```css
.celebration-card {
    box-shadow: var(--shadow-xl), 0 0 60px color-mix(in oklab, var(--brand-base) 40%, transparent);
}
```

### MEDIUM Zone Example
```css
.product-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}
```

### LOW Zone Example
```css
.settings-input {
    transition: border-color var(--duration-fast);
}
```

---

## Prohibiciones

| Prohibido | Usar En Su Lugar |
|-----------|------------------|
| `#3C9E5D` | `var(--gator-500)` |
| `16px` | `var(--space-3)` |
| `border-radius: 10px` | `var(--radius-2)` |
| `transition: 0.3s` | `var(--transition)` |
| `font-size: 14px` | `var(--text-sm)` |

---

## Verificación

### Checklist Pre-Commit

- [ ] Sin colores hardcodeados
- [ ] Sin spacing hardcodeado
- [ ] Sin font-size hardcodeado
- [ ] Usa tokens de `--radius-*`
- [ ] Usa `--duration-*` para transiciones
- [ ] Respeta zones de expresividad
- [ ] Accesibilidad verificada (contrast, focus)

---

## Recursos

- **Archivo principal**: `/static/css/tokens.css`
- **Documentación**: `/docs/03-FRONTEND/design-system/`
- **Referencias**: Golden Ratio, Fibonacci sequence
