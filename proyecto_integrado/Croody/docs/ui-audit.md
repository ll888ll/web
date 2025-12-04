# UI Audit · Croody Frontend (Noviembre 2024)

## 1. Estructura y componentes actuales
- **Layout**: header pegajoso + secciones apiladas. Buena base responsive pero las columnas y componentes no comparten un grid único.
- **Componentes clave**: hero, metric-cards, vector-cards, product-cards y CTA slim. Cada uno usa espaciados distintos (mezcla de 16/20/24 px) y radios variables.
- **Sistema de tokens**: existe `tokens.css` con paleta "gator" pero convive con estilos inline en cada plantilla.

## 2. Usabilidad y experiencia
- Navegación principal no marca la página activa ni reduce su tamaño en scroll.
- Los formularios (búsqueda, filtros) usan placeholder genérico y no ofrecen estados de error/éxito consistentes.
- Jerarquía tipográfica depende del componente; los `h2` llegan a verse iguales a `h3`.
- En móvil, la búsqueda ocupa demasiado alto y compite con CTAs.

## 3. Inconsistencias visuales
- Radios distintos (12px, 18px, 20px) y sombras con opacidades variadas.
- Paleta secundaria no está documentada; aparecen tonos cálidos en CTA slim que no pertenecen a la marca.
- Grillas usan distintos `gap` (16px, 21px, 24px) sin relación con la escala definida.

## 4. Prioridades de mejora
1. Consolidar tokens (colores, tipografías, espacios, sombras) y documentarlos.
2. Redefinir header + navegación para mejorar contraste y estados activos.
3. Normalizar cards, métricas y formularios para mantener la misma densidad visual.
4. Revisar accesibilidad: contraste AA, tamaños mínimos de toque, etiquetas ARIA para toggles/idiomas.
