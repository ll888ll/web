# Croody · Design System 2025

## Identidad visual
- **Paleta principal**
  - Verde Croody `#3C9E5D` (base) con acentos `#1C5C37` y `#80D3A0`.
  - Neutros "Jungle" para fondos (`#0B1311` a `#EEF1EF`).
  - Dorados suaves (`#E0B771`) reservados para CTAs secundarios y datos financieros.
- **Tipografía**
  - Display: `Baloo 2` para títulos (`var(--text-4xl)` a `--text-lg`).
  - Texto: `Josefin Sans / Inter` (`var(--text-base)`), line-height `1.55`.
  - Uso consistente de mayúsculas con tracking en navegación y chips.

## Componentes
- **Header**: sticky con fondo blur, estado compacto y resaltado de enlace activo.
- **Cards**: radios de 20/24 px, sombras uniformes, estados hover con `box-shadow: var(--shadow-lg)`.
- **Buttons**: gradiente verde para primario, ghost con borde de contraste 4.5:1, estados focus visibles.
- **Metric cards**: tipografía display para números, etiquetas en `--text-sm`.

## Accesibilidad
- Contraste mínimo AA (verificado 4.5:1 para texto regular y 3:1 para títulos).
- Entradas con `outline` y `box-shadow` personalizados.
- Navegación móvil con enlaces de 48px de alto y `aria-current` en páginas activas.

## Reglas de uso
1. Paleta secundaria (dorados, acentos cálidos) solo para finanzas/Luks y no más del 20% del layout.
2. Animaciones <= 300ms y cubren hover/focus sin bloquear interacción.
3. Cada nueva sección debe reutilizar `.section`, `.container` y `var(--space-n)` para mantener ritmo.

Mantener este documento junto a `static/css/tokens.css` para futuras referencias.
