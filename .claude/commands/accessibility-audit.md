# Accessibility Audit para Django/HTMX

Eres un experto en accesibilidad web especializado en WCAG 2.2 AA/AAA, diseño inclusivo y compatibilidad con tecnologías asistivas. Realiza auditorías completas de templates Django y componentes HTMX.

## Contexto

El usuario necesita auditar y mejorar la accesibilidad de las plantillas Django/HTMX del proyecto Croody Web para garantizar cumplimiento WCAG y experiencia inclusiva. El sistema usa Sacred Geometry design system con tokens CSS.

## Requisitos

$ARGUMENTS

## Instrucciones

### 1. Testing Automatizado con axe-core + Playwright

```python
# accessibility_audit.py
"""
Auditoría de accesibilidad para Django templates.
Usa Playwright con axe-core para testing automatizado.
"""
import asyncio
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright
from axe_playwright_python.async_playwright import Axe

class DjangoAccessibilityAuditor:
    """Auditor de accesibilidad para templates Django."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.wcag_level = "wcag2aa"
        self.results = []

    async def audit_page(self, path: str) -> dict:
        """
        Audita una página específica.

        Args:
            path: URL relativa (ej: "/shop/products/")

        Returns:
            Resultado de axe con violations y passes
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            url = f"{self.base_url}{path}"
            await page.goto(url, wait_until="networkidle")

            # Esperar a que HTMX complete cargas dinámicas
            await page.wait_for_timeout(1000)

            axe = Axe()
            results = await axe.run(page)

            await browser.close()

            return {
                "url": url,
                "timestamp": datetime.utcnow().isoformat(),
                "violations": results.violations,
                "passes": results.passes,
                "incomplete": results.incomplete,
                "score": self._calculate_score(results)
            }

    def _calculate_score(self, results) -> int:
        """Calcula score de accesibilidad (0-100)."""
        weights = {"critical": 10, "serious": 5, "moderate": 2, "minor": 1}
        penalty = sum(
            weights.get(v.get("impact", "minor"), 1) * len(v.get("nodes", []))
            for v in results.violations
        )
        return max(0, 100 - penalty)

    async def audit_critical_pages(self) -> list:
        """Audita páginas críticas de Croody."""
        critical_pages = [
            "/",                      # Landing
            "/shop/",                 # Tienda
            "/shop/cart/",            # Carrito
            "/shop/checkout/",        # Checkout
            "/accounts/login/",       # Login
            "/accounts/register/",    # Registro
        ]

        for path in critical_pages:
            result = await self.audit_page(path)
            self.results.append(result)

        return self.results


# Uso con pytest
import pytest

@pytest.mark.asyncio
async def test_landing_accessibility():
    """Test de accesibilidad para landing page."""
    auditor = DjangoAccessibilityAuditor()
    result = await auditor.audit_page("/")

    # Sin violaciones críticas o serias
    critical_violations = [
        v for v in result["violations"]
        if v.get("impact") in ("critical", "serious")
    ]
    assert len(critical_violations) == 0, f"Violaciones críticas: {critical_violations}"
    assert result["score"] >= 90, f"Score bajo: {result['score']}"
```

### 2. Validación de Contraste de Color

```python
# contrast_validator.py
"""
Valida contraste de colores contra tokens de Sacred Geometry.
"""
import re
from pathlib import Path

class ContrastValidator:
    """Validador de contraste para tokens CSS de Croody."""

    # Ratios WCAG 2.2
    WCAG_RATIOS = {
        "AA_normal": 4.5,
        "AA_large": 3.0,
        "AAA_normal": 7.0,
        "AAA_large": 4.5,
    }

    # Colores de Sacred Geometry (tokens.css)
    GATOR_PALETTE = {
        "--gator-950": "#041009",
        "--gator-900": "#082015",
        "--gator-500": "#3C9E5D",  # Brand base
        "--gator-100": "#DDF6E8",
        "--gator-50": "#F0FBF5",
    }

    JUNGLE_PALETTE = {
        "--jungle-950": "#050807",  # bg dark
        "--jungle-50": "#EEF1EF",   # bg light
    }

    def parse_rgb(self, hex_color: str) -> tuple:
        """Convierte hex a RGB."""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def relative_luminance(self, rgb: tuple) -> float:
        """Calcula luminancia relativa según WCAG."""
        def adjust(val):
            val = val / 255
            return val / 12.92 if val <= 0.03928 else ((val + 0.055) / 1.055) ** 2.4

        r, g, b = [adjust(c) for c in rgb]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def contrast_ratio(self, fg: str, bg: str) -> float:
        """Calcula ratio de contraste entre dos colores."""
        l1 = self.relative_luminance(self.parse_rgb(fg))
        l2 = self.relative_luminance(self.parse_rgb(bg))
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    def validate_token_combinations(self) -> list:
        """Valida combinaciones de tokens críticas."""
        issues = []

        # Texto sobre fondos comunes
        combinations = [
            ("--fg (jungle-50)", "#EEF1EF", "--bg (jungle-950)", "#050807"),
            ("--brand-base (gator-500)", "#3C9E5D", "--bg (jungle-950)", "#050807"),
            ("--fg-muted (jungle-200)", "#A9B4B0", "--surface-1 (jungle-900)", "#0B1311"),
        ]

        for fg_name, fg_hex, bg_name, bg_hex in combinations:
            ratio = self.contrast_ratio(fg_hex, bg_hex)
            if ratio < self.WCAG_RATIOS["AA_normal"]:
                issues.append({
                    "combination": f"{fg_name} on {bg_name}",
                    "ratio": round(ratio, 2),
                    "required": self.WCAG_RATIOS["AA_normal"],
                    "passed": False
                })

        return issues


# Test
def test_sacred_geometry_contrast():
    """Verifica que tokens Sacred Geometry cumplan WCAG AA."""
    validator = ContrastValidator()
    issues = validator.validate_token_combinations()

    assert len(issues) == 0, f"Problemas de contraste: {issues}"
```

### 3. Validación de Templates Django

```python
# template_validator.py
"""
Valida accesibilidad en templates Django.
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup

class DjangoTemplateAccessibilityValidator:
    """Validador de accesibilidad para templates Django."""

    def __init__(self, templates_dir: str = "proyecto_integrado/Croody/templates"):
        self.templates_dir = Path(templates_dir)
        self.issues = []

    def validate_template(self, template_path: Path) -> list:
        """Valida un template individual."""
        issues = []
        content = template_path.read_text()
        soup = BeautifulSoup(content, "html.parser")

        # 1. Imágenes sin alt
        for img in soup.find_all("img"):
            if not img.get("alt"):
                issues.append({
                    "file": str(template_path),
                    "type": "missing_alt",
                    "element": str(img)[:100],
                    "fix": 'Agregar alt="" (decorativa) o alt="descripción"'
                })

        # 2. Forms sin labels
        for input_el in soup.find_all(["input", "textarea", "select"]):
            input_id = input_el.get("id")
            input_type = input_el.get("type", "text")

            # Ignorar hidden, submit, button
            if input_type in ("hidden", "submit", "button"):
                continue

            # Buscar label asociado
            has_label = False
            if input_id:
                has_label = soup.find("label", {"for": input_id}) is not None

            # También acepta aria-label
            has_aria = input_el.get("aria-label") or input_el.get("aria-labelledby")

            if not has_label and not has_aria:
                issues.append({
                    "file": str(template_path),
                    "type": "missing_label",
                    "element": str(input_el)[:100],
                    "fix": f'Agregar <label for="{input_id}"> o aria-label'
                })

        # 3. Botones sin texto accesible
        for btn in soup.find_all("button"):
            text = btn.get_text(strip=True)
            aria_label = btn.get("aria-label")

            if not text and not aria_label:
                issues.append({
                    "file": str(template_path),
                    "type": "empty_button",
                    "element": str(btn)[:100],
                    "fix": "Agregar texto visible o aria-label"
                })

        # 4. Links sin texto
        for link in soup.find_all("a"):
            text = link.get_text(strip=True)
            aria_label = link.get("aria-label")

            if not text and not aria_label:
                # Podría tener imagen con alt
                img = link.find("img")
                if not img or not img.get("alt"):
                    issues.append({
                        "file": str(template_path),
                        "type": "empty_link",
                        "element": str(link)[:100],
                        "fix": "Agregar texto, aria-label o imagen con alt"
                    })

        # 5. HTMX sin indicadores de carga
        for htmx_el in soup.find_all(attrs={"hx-get": True}):
            if not htmx_el.get("hx-indicator"):
                issues.append({
                    "file": str(template_path),
                    "type": "htmx_no_indicator",
                    "element": str(htmx_el)[:100],
                    "fix": "Agregar hx-indicator para feedback de carga"
                })

        # 6. Estructura de headings
        headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        levels = [int(h.name[1]) for h in headings]

        for i in range(1, len(levels)):
            if levels[i] > levels[i-1] + 1:
                issues.append({
                    "file": str(template_path),
                    "type": "heading_skip",
                    "element": f"h{levels[i-1]} -> h{levels[i]}",
                    "fix": f"No saltar de h{levels[i-1]} a h{levels[i]}"
                })

        return issues

    def validate_all(self) -> list:
        """Valida todos los templates."""
        for template in self.templates_dir.rglob("*.html"):
            self.issues.extend(self.validate_template(template))
        return self.issues
```

### 4. Navegación por Teclado

```python
# keyboard_navigation.py
"""
Verifica navegación por teclado en componentes HTMX.
"""

class KeyboardNavigationChecker:
    """Verificador de navegación por teclado."""

    REQUIRED_PATTERNS = {
        "modal": {
            "focus_trap": True,
            "escape_close": True,
            "initial_focus": "first_focusable"
        },
        "dropdown": {
            "arrow_navigation": True,
            "escape_close": True,
            "enter_select": True
        },
        "tabs": {
            "arrow_navigation": True,
            "home_end": True
        }
    }

    def generate_htmx_keyboard_fixes(self) -> str:
        """Genera código JavaScript para mejorar accesibilidad HTMX."""
        return '''
// keyboard-a11y.js
// Mejoras de accesibilidad para componentes HTMX

document.addEventListener('DOMContentLoaded', () => {
    // Focus trap para modales
    document.addEventListener('htmx:afterSwap', (e) => {
        const modal = e.detail.target.querySelector('[role="dialog"]');
        if (modal) {
            setupFocusTrap(modal);
            announceToScreenReader('Modal abierto');
        }
    });

    // Cerrar modal con Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const modal = document.querySelector('[role="dialog"]');
            if (modal) {
                htmx.trigger(modal.querySelector('[data-dismiss]'), 'click');
            }
        }
    });

    // Hacer elementos clickeables accesibles
    document.querySelectorAll('[hx-get], [hx-post]').forEach(el => {
        if (!['A', 'BUTTON', 'INPUT'].includes(el.tagName)) {
            el.setAttribute('tabindex', '0');
            el.setAttribute('role', 'button');

            el.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    el.click();
                }
            });
        }
    });
});

function setupFocusTrap(modal) {
    const focusables = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const first = focusables[0];
    const last = focusables[focusables.length - 1];

    first?.focus();

    modal.addEventListener('keydown', (e) => {
        if (e.key !== 'Tab') return;

        if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last?.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first?.focus();
        }
    });
}

function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.classList.add('sr-only');
    announcement.textContent = message;
    document.body.appendChild(announcement);
    setTimeout(() => announcement.remove(), 1000);
}
'''
```

### 5. Checklist Manual de Accesibilidad

```markdown
## Checklist Manual - Croody Web

### Navegación por Teclado
- [ ] Todos los elementos interactivos accesibles con Tab
- [ ] Botones activan con Enter/Space
- [ ] Modales se cierran con Escape
- [ ] Focus visible siempre (var(--brand-base) outline)
- [ ] Sin keyboard traps
- [ ] Orden de tab lógico

### Screen Reader
- [ ] Título de página descriptivo (<title>)
- [ ] Headings crean outline lógico (h1 → h2 → h3)
- [ ] Imágenes tienen alt text
- [ ] Formularios tienen labels
- [ ] Errores anunciados con aria-live
- [ ] Actualizaciones HTMX anunciadas

### Visual
- [ ] Texto redimensionable a 200% sin pérdida
- [ ] Color no es único medio de información
- [ ] Focus indicators con contraste suficiente
- [ ] Contenido reflows a 320px
- [ ] Animaciones pausables (prefers-reduced-motion)

### Cognitive
- [ ] Instrucciones claras y simples
- [ ] Mensajes de error útiles
- [ ] Sin límites de tiempo en formularios
- [ ] Navegación consistente
- [ ] Acciones importantes reversibles
```

### 6. CSS de Accesibilidad para Sacred Geometry

```css
/* a11y-enhancements.css */
/* Mejoras de accesibilidad compatibles con Sacred Geometry */

/* Skip link */
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    padding: var(--space-2) var(--space-3);
    background: var(--brand-base);
    color: var(--bg);
    z-index: 9999;
    transition: top var(--duration-fast) var(--ease-base);
}

.skip-link:focus {
    top: 0;
}

/* Focus visible mejorado */
:focus-visible {
    outline: 3px solid var(--brand-base);
    outline-offset: 2px;
    border-radius: var(--radius-1);
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* High contrast mode */
@media (prefers-contrast: high) {
    :root {
        --fg: #ffffff;
        --bg: #000000;
        --brand-base: #00ff00;
    }

    a, button {
        text-decoration: underline !important;
    }

    input, textarea, select {
        border: 2px solid var(--fg) !important;
    }
}

/* Screen reader only (utilidad) */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* Touch targets mínimos */
button,
a,
input[type="checkbox"],
input[type="radio"] {
    min-height: 44px;
    min-width: 44px;
}

/* HTMX loading indicator accesible */
.htmx-request .htmx-indicator {
    display: inline-block;
}

.htmx-indicator {
    display: none;
}

.htmx-indicator::after {
    content: "Cargando...";
    /* Solo visible para screen readers si hay spinner visual */
}
```

### 7. Integración CI/CD

```yaml
# .github/workflows/accessibility.yml
name: Accessibility Tests

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  a11y-audit:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: croody_test
          POSTGRES_USER: croody
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install playwright axe-playwright-python beautifulsoup4
        playwright install chromium

    - name: Start Django server
      run: |
        cd proyecto_integrado/Croody
        python manage.py migrate --settings=croody.settings.test
        python manage.py runserver &
        sleep 5

    - name: Run accessibility audit
      run: |
        python scripts/accessibility_audit.py

    - name: Validate templates
      run: |
        python scripts/template_validator.py

    - name: Check color contrast
      run: |
        python scripts/contrast_validator.py

    - name: Upload report
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: a11y-report
        path: reports/accessibility-*.html
```

### 8. Reporte de Auditoría

```python
# report_generator.py
"""Generador de reporte HTML de accesibilidad."""

def generate_html_report(audit_results: dict) -> str:
    """Genera reporte HTML con resultados de auditoría."""
    return f'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Auditoría de Accesibilidad - Croody Web</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .summary {{ background: #f0f0f0; padding: 20px; border-radius: 8px; }}
        .score {{ font-size: 48px; font-weight: bold; color: {"#0a0" if audit_results["score"] >= 90 else "#f00"}; }}
        .violation {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }}
        .critical {{ border-color: #f00; background: #fee; }}
        .serious {{ border-color: #fa0; background: #ffe; }}
        .moderate {{ border-color: #ff0; background: #ffc; }}
    </style>
</head>
<body>
    <h1>🦎 Auditoría de Accesibilidad - Croody Web</h1>
    <p>Generado: {audit_results["timestamp"]}</p>

    <div class="summary">
        <h2>Resumen</h2>
        <div class="score">{audit_results["score"]}/100</div>
        <p>Total Violaciones: {len(audit_results["violations"])}</p>
        <p>WCAG Level: {audit_results["wcag_level"]}</p>
    </div>

    <h2>Violaciones</h2>
    {"".join(f'''
        <div class="violation {v["impact"]}">
            <h3>{v["help"]}</h3>
            <p><strong>Impacto:</strong> {v["impact"]}</p>
            <p>{v["description"]}</p>
            <p><strong>Elementos afectados:</strong> {len(v["nodes"])}</p>
            <a href="{v["helpUrl"]}">Más información</a>
        </div>
    ''' for v in audit_results["violations"])}

    <h2>Recomendaciones</h2>
    <ul>
        <li>Agregar skip links al inicio de cada página</li>
        <li>Verificar focus visible en todos los componentes interactivos</li>
        <li>Asegurar que todas las imágenes tengan alt text descriptivo</li>
        <li>Implementar aria-live regions para actualizaciones HTMX</li>
    </ul>
</body>
</html>
'''
```

## Output Esperado

1. **Score de Accesibilidad**: Puntuación de cumplimiento WCAG (0-100)
2. **Reporte de Violaciones**: Issues detallados con severidad y fixes
3. **Resultados de Tests**: Automatizados y manuales
4. **Guía de Remediación**: Fixes paso a paso para cada issue
5. **Código de Ejemplo**: Componentes Django/HTMX accesibles

## Restricciones

- Usa tokens CSS de Sacred Geometry, no valores hardcodeados
- Mantén compatibilidad con tema dark (Jungle/Gator)
- Prioriza fixes que no rompan el diseño visual
- Focus en WCAG 2.2 AA como mínimo

Enfócate en crear experiencias inclusivas que funcionen para todos los usuarios, independientemente de sus capacidades o tecnologías asistivas.
