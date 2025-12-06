# Visual Validation - Sacred Geometry Compliance

Valida un template/componente Django contra el sistema de diseño Sacred Geometry a través de análisis de código y verificación de tokens CSS.

## Context

Este comando verifica que los templates y CSS del proyecto Croody cumplan con el sistema de diseño basado en el Número Áureo (φ = 1.618). Invoca al `frontend-artist` agent para análisis detallado.

## Requirements

$ARGUMENTS

## Usage

```bash
/visual-validate proyecto_integrado/Croody/templates/shop/product_list.html
/visual-validate proyecto_integrado/Croody/static/css/components.css
/visual-validate all  # Auditoría completa
```

## Instructions

### Phase 1: Context Gathering

1. **Cargar Tokens de Referencia**
   - Leer `/static/css/tokens.css` (307 líneas)
   - Leer `.claude/skills/sacred-geometry-design/SKILL.md`

2. **Identificar Archivo Target**
   - Template HTML: verificar classes CSS usadas
   - Archivo CSS: verificar valores hardcodeados
   - Componente JS: verificar inline styles

### Phase 2: Token Compliance Checklist

```markdown
### Spacing (Golden Ratio φ = 1.618)
- [ ] Usa `var(--space-1)` a `var(--space-6)`
- [ ] No hardcodea valores de padding/margin
- [ ] Respeta secuencia Fibonacci: 8, 13, 21, 34, 55, 89px

### Colores
- [ ] Usa tokens de paleta Gator (--gator-*)
- [ ] Usa tokens de paleta Jungle (--jungle-*)
- [ ] Usa variables semánticas (--bg, --fg, --brand-base)
- [ ] NO hay colores hexadecimales hardcodeados

### Tipografía
- [ ] Usa `var(--font-sans)` o `var(--font-display)`
- [ ] Usa escala tipográfica (--text-xs a --text-4xl)
- [ ] NO hay font-size en px hardcodeados

### Border Radius
- [ ] Usa `var(--radius-1)` a `var(--radius-4)`
- [ ] NO hay border-radius hardcodeados

### Shadows
- [ ] Usa `var(--shadow-xs)` a `var(--shadow-lg)`
- [ ] NO hay box-shadow hardcodeados

### Transitions
- [ ] Usa `var(--duration-base)` (233ms) o `var(--duration-slow)` (377ms)
- [ ] Usa `var(--ease-base)` para easing
- [ ] NO hay transition-duration hardcodeados
```

### Phase 3: Anti-Pattern Detection

```bash
# Detectar colores hardcodeados
grep -E "#[0-9A-Fa-f]{3,6}|rgb\(|rgba\(" --include="*.css" --include="*.html"

# Detectar spacing hardcodeado
grep -E "padding:\s*\d+px|margin:\s*\d+px" --include="*.css"

# Detectar font-size hardcodeado
grep -E "font-size:\s*\d+px" --include="*.css"

# Detectar border-radius hardcodeado
grep -E "border-radius:\s*\d+px" --include="*.css"

# Detectar transition hardcodeado
grep -E "transition:\s*[\d.]+s|transition-duration:\s*[\d.]+ms" --include="*.css"
```

### Phase 4: Expressivity Zone Classification

| Zone | Uso | Características |
|------|-----|-----------------|
| **HIGH** | Hero sections, CTAs principales | Glows, animaciones complejas, gradientes |
| **MEDIUM** | Cards interactivos, productos | Hover effects, shimmer, transforms |
| **LOW** | Functional UI, forms, settings | Minimal transitions, sin efectos fancy |

#### Zone Detection Rules

```markdown
## HIGH Zone (Celebrations)
- Hero banners
- Success/celebration modals
- Featured products
- CTAs principales

Permitido:
- box-shadow con glow (color-mix con brand)
- Animaciones de entrada elaboradas
- Gradientes sutiles

## MEDIUM Zone (Interactive)
- Product cards (vector-card)
- Navigation items
- Botones secundarios

Permitido:
- translateY(-4px) en hover
- box-shadow escalado en hover
- Shimmer en botones

## LOW Zone (Functional)
- Forms de login/registro
- Settings
- Tablas de datos
- Admin panels

Permitido:
- Solo cambio de border-color en focus
- Transiciones de 100ms (--duration-fast)
- Sin transforms
```

### Phase 5: Template Analysis

Para archivos HTML/Django templates:

```python
# Verificar classes CSS usadas
import re

def analyze_template(content):
    # Extraer classes
    classes = re.findall(r'class="([^"]+)"', content)

    # Verificar contra tokens conocidos
    known_tokens = [
        'vector-card', 'btn-primary', 'btn-secondary',
        'fade-in-up', 'shimmer', 'surface-1', 'surface-2'
    ]

    violations = []
    for class_list in classes:
        for cls in class_list.split():
            if cls.startswith('p-') or cls.startswith('m-'):
                # Tailwind-style, verificar si usa sistema
                pass
            elif 'color' in cls.lower() and not cls.startswith('--'):
                violations.append(f"Possible hardcoded color class: {cls}")

    return violations

# Verificar inline styles (prohibidos)
inline_styles = re.findall(r'style="([^"]+)"', content)
if inline_styles:
    print("WARNING: Inline styles detected (should use CSS classes)")
```

### Phase 6: Generate Report

```markdown
# Visual Validation Report

**Archivo**: $ARGUMENTS
**Fecha**: [fecha]
**Zone**: [HIGH/MEDIUM/LOW]

## Compliance Summary

| Categoría | Status | Issues |
|-----------|--------|--------|
| Spacing | ✅/❌ | [count] |
| Colors | ✅/❌ | [count] |
| Typography | ✅/❌ | [count] |
| Border Radius | ✅/❌ | [count] |
| Shadows | ✅/❌ | [count] |
| Transitions | ✅/❌ | [count] |

## Violations Found

### Critical (Block merge)
1. **Line X**: `color: #3C9E5D` → Usar `var(--gator-500)`
2. **Line Y**: `padding: 16px` → Usar `var(--space-3)` (21px) o `var(--space-2)` (13px)

### Warnings (Should fix)
1. **Line Z**: Inline style detected

### Suggestions
1. Consider using `.vector-card` class for product cards

## Expressivity Zone Analysis

- **Expected Zone**: MEDIUM (product listing)
- **Actual Zone**: HIGH (has glow effects)
- **Recommendation**: Remove `box-shadow` glow, use standard elevation

## Recommended Fixes

```css
/* Before */
.product-card {
    padding: 16px;
    color: #3C9E5D;
    border-radius: 10px;
    transition: 0.3s ease;
}

/* After (Sacred Geometry compliant) */
.product-card {
    padding: var(--space-3);
    color: var(--brand-base);
    border-radius: var(--radius-2);
    transition: var(--transition);
}
```

## Token Reference (Quick Copy)

```css
/* Spacing */
var(--space-1)  /* 8px */
var(--space-2)  /* 13px */
var(--space-3)  /* 21px */
var(--space-4)  /* 34px */

/* Colors */
var(--brand-base)    /* #3C9E5D */
var(--brand-strong)  /* #277947 */
var(--bg)            /* Background */
var(--fg)            /* Foreground */

/* Radius */
var(--radius-2)  /* 10px - buttons */
var(--radius-3)  /* 16px - cards */
```
```

### Phase 7: Automated Fixes (Optional)

Si el usuario confirma, generar parche:

```diff
--- a/static/css/components.css
+++ b/static/css/components.css
@@ -45,7 +45,7 @@
 .product-card {
-    padding: 16px;
+    padding: var(--space-3);
-    color: #3C9E5D;
+    color: var(--brand-base);
 }
```

## Integration Points

- **Skill**: `sacred-geometry-design` (tokens reference)
- **Agent**: `frontend-artist` (CSS expertise)
- **Files**: `/static/css/tokens.css` (source of truth)

## Error Handling

- **File not found**: Suggest correct path
- **Not CSS/HTML**: Inform user this command is for frontend files
- **All compliant**: Celebrate! ✅

---

Argumento recibido: $ARGUMENTS

Si es "all", audita todos los archivos CSS en `/static/css/` y templates en `/templates/`.
Si es un archivo específico, analiza solo ese archivo.
