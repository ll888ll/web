# Principios de Prompting para Opus 4.5

> Referencia rápida para optimizar prompts manualmente.
> **Proyecto-aware**: Respeta el sistema de diseño Sacred Geometry de Croody Web.

---

## TL;DR: Los 5 Principios

```
1. TONO       → Trata a Opus como colega senior brillante pero sensible
2. ACCIÓN     → <default_to_action>true</default_to_action> + "implementa, no sugieras"
3. MINIMAL    → "Modifica in-situ, footprint mínimo, sin abstracciones nuevas"
4. JUSTIFICA  → Toda regla necesita "porque [razón técnica]"
5. CREATIVIDAD→ **CONTEXTO-AWARE** (ver sección Frontend vs Backend)
```

---

## 1. Calibra el Tono

| Evita | Usa |
|-------|-----|
| `NEVER`, `ALWAYS`, `MUST` | "Por favor evita...", "Preferimos..." |
| `CRITICAL:`, `IMPORTANT:` | Prosa natural |
| `DO NOT` | "Evita X porque Y" |
| MAYÚSCULAS | **Negritas** |
| Imperativos secos | Contexto conversacional |

---

## 2. Fuerza la Acción

```xml
<default_to_action>true</default_to_action>
```

Frases clave:
- "Implementa la solución completa."
- "Escribe código funcional, no fragmentos."
- "Realiza los cambios directamente."

---

## 3. Contén la Sobre-Ingeniería

```
"Modifica archivos in-situ."
"Mantén el nivel de abstracción actual."
"Footprint mínimo de archivos."
"Resiste la tentación de mejorar código no relacionado."
"Fat model pattern - lógica en modelos, no en vistas."
```

---

## 4. Justifica tus Reglas

**Estructura:** `Haz X porque [razón].`

| Sin Justificar | Justificado |
|----------------|-------------|
| "Use CSS tokens" | "Use CSS tokens porque mantiene consistencia con Sacred Geometry" |
| "No crear helpers" | "Evita helpers porque queremos footprint mínimo" |
| "Use ORM" | "Use ORM porque previene SQL injection" |

---

## 5. Creatividad Contextual (IMPORTANTE)

### Si es Frontend/Diseño → Usa el Sistema Sacred Geometry

**No uses adjetivos genéricos.** Invoca el skill:

```
skill: "sacred-geometry-design"
```

| Genérico (evitar) | Croody-Specific (usar) |
|-------------------|----------------------|
| "moderno" | "Dark theme con surface layers" |
| "minimalista" | "Functional UI zone (LOW expressivity)" |
| "colorido" | "Gator palette tokens" |
| "animado" | "233ms transition, spring ease" |
| "premium" | "Vector card con shimmer hover" |
| "ecológico" | "Gator green brand-base" |

**Restricciones Croody:**
- Tokens de `tokens.css`, nunca colores hardcodeados
- Border radius: var(--radius-2) para botones, var(--radius-3) para cards
- Glows solo en featured products y celebrations (HIGH zone)
- Spacing: Fibonacci sequence (8, 13, 21, 34, 55, 89px)
- Timing: 233ms base (φ-derived)

### Si es Backend → Patrones Django/FastAPI

Para lógica/backend, usa el skill:

```
skill: "django-patterns"
```

Adjetivos técnicos permitidos:
- `Fat model` - lógica en modelo
- `Thin view` - vistas solo coordinan
- `Parametrized` - queries seguras
- `Surgical` - cambios precisos

---

## Quick Reference: Croody Design System

**Expressivity Zones:**
```
HIGH   → Hero sections, featured products, celebrations, CTAs principales
MEDIUM → Product cards (vector-card), navigation items, interactive elements
LOW    → Forms, settings, tables, admin panels
```

**Colores (tokens):**
```
Brand:    var(--brand-base)     /* Gator #3C9E5D */
Background: var(--bg)           /* Jungle dark */
Surface:  var(--surface-1/2)    /* Elevation layers */
Text:     var(--fg), var(--fg-muted)
```

**Spacing (Fibonacci φ):**
```
var(--space-1)   /* 8px */
var(--space-2)   /* 13px */
var(--space-3)   /* 21px */
var(--space-4)   /* 34px */
var(--space-5)   /* 55px */
var(--space-6)   /* 89px */
```

**Prohibido:**
```
✗ Colores hexadecimales hardcodeados
✗ Inline styles
✗ Font-size en px (usar escala)
✗ Border-radius hardcodeado
✗ Transition timing hardcodeado
✗ SQL sin parametrizar
✗ Secrets en código
```
