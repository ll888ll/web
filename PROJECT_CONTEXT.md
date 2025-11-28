# CROODY / BUDDY / LUKS - PROJECT CONTEXT

## Fuente de la Verdad Visual (Visual Source of Truth)
NO EXISTEN MOCKUPS. La verdad absoluta es el código en `/app` y `/components`.
1. **Diseño "Nocturne":** Fondo oscuro con ruido, neones sutiles, tipografía 'Baloo 2' (headers) e 'Inter' (cuerpo).
2. **Colores:** Definidos estrictamente en `tailwind.config.ts`. NO usar valores HEX arbitrarios (ej: #333), usar clases utilitarias (ej: `bg-croody-dark`).
3. **Componentes:** Antes de crear UI, revisa `/components/ui`. Si existe `Button.tsx`, ÚSALO.

## Reglas de Negocio (Ecosistema)
- **Croody:** La puerta de entrada / Landing.
- **Buddy:** El entrenador IA. Se adapta, no juzga.
- **Luks:** Utility Token. Sirve para *usar*, no para *especular*. Prohibido lenguaje financiero ("ROI", "Inversión").

## Tu Flujo de Trabajo OBLIGATORIO
1. **Audita:** Usa `puppeteer` (Chrome DevTools) para ver `http://localhost:3000` o scrappear referencias y entender el estilo actual.
2. **Lee:** Lee `tailwind.config.ts` y `app/globals.css`.
3. **Implementa:** Escribe código consistente.
4. **Verifica:** Vuelve a usar `puppeteer` para confirmar que no rompiste el diseño.
