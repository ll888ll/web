"""Blueprint extraído de tienda.txt para la tienda Buddy.

Nota: Este módulo es de referencia interna para el equipo. No se
renderiza directamente en la UI. Se mantiene coherencia de
terminología ("Luks" en estilo título) y tipografías (Baloo 2 para
titulares, Josefin Sans para cuerpo) para evitar confusiones.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List


def _clone(data: Any) -> Any:
    """Devuelve una copia para evitar mutaciones accidentales."""
    return deepcopy(data)


UX_PRINCIPLES_DATA: List[Dict[str, str]] = [
    {'title': 'Núcleo transaccional', 'description': 'La web es el hub de compra/venta; CTAs conducen a checkout o listado.'},
    {'title': 'Inventario como hub', 'description': 'Visualiza, abre, equipa o lista ítems sin salir de la experiencia web.'},
    {'title': 'Facetas y búsqueda robustas', 'description': 'Filtros visibles, tokens en la barra y estados persistentes en la URL.'},
    {'title': 'Transparencia', 'description': 'Probabilidades, tarifas y confirmaciones firmadas siempre a la vista.'},
    {'title': 'Accesibilidad y confianza', 'description': 'AA/AAA, copy sobrio, recibos y certificados de integridad.'},
]

INFORMATION_ARCHITECTURE_DATA: List[Dict[str, str]] = [
    {'path': '/', 'label': 'Home Tienda', 'description': 'Destacados, ventas relámpago, cofres, sets, accesorios, música y animaciones.'},
    {'path': '/catalogo', 'label': 'Catálogo completo', 'description': 'Listado con facetas avanzadas, orden y filtros combinables.'},
    {'path': '/producto/:slug', 'label': 'Detalle de producto', 'description': 'Packs, sets, personajes y accesorios con odds y compatibilidad.'},
    {'path': '/inventario', 'label': 'Inventario web', 'description': 'Ítems propios con acciones de abrir, aplicar, equipar y vender/listar.'},
    {'path': '/mercado', 'label': 'Marketplace P2P', 'description': 'Listados, gráficos de precio y filtros por rareza, personaje y temporada.'},
    {'path': '/mercado/:id', 'label': 'Detalle de listado', 'description': 'Información del vendedor, royalties, historial y acciones de compra/oferta.'},
    {'path': '/vender', 'label': 'Creador de listados', 'description': 'Seleccionar ítem, fijar precio, duración y firmar publicación.'},
    {'path': '/wallet', 'label': 'Billetera Luks', 'description': 'Saldo, depósitos, retiros, historial y configuración custodial/non-custodial.'},
    {'path': '/eventos/:temporada', 'label': 'Landing de temporada', 'description': 'Bonos, pity, probabilidades y ofertas por evento.'},
    {'path': '/soporte', 'label': 'Centro de ayuda', 'description': 'FAQ, regulatorio, límites por región/edad y estado del sistema.'},
]

URL_POLICIES_DATA = [
    'Slugs legibles (ej. /producto/cofre-helado-s3-legendario).',
    'IDs opacos solo para listados críticos del mercado (/mercado/0xabc…).',
    'Filtros parametrizados por querystring (ej. /catalogo?tipo=set&rareza=legendario).',
]

HEADER_LAYOUT_DATA = {
    'header': [
        'Logo Buddy enlaza al home de la tienda.',
        'Buscador con type-ahead por categoría y personaje.',
        'Bóveda Luks con saldo abreviado y variación diaria.',
        'Tabs directos a Tienda, Inventario y Mercado.',
        'Conectar wallet / Perfil con estado de sesión.',
    ],
    'layout': [
        'Grid responsivo: 12 columnas en desktop, 4–6 en mobile.',
        'Container máximo de 1440px con gutters de 24px desktop / 16px mobile.',
    ],
    'footer': [
        'Enlaces legales, divulgación de probabilidades y estado del sistema.',
        'Accesos a soporte y redes oficiales.',
    ],
}

HOME_SECTIONS_DATA = [
    {'title': 'Hero con carrusel', 'description': 'Banners de ventas relámpago, sets de temporada y cofres destacados.'},
    {'title': 'Cofres & Cajas', 'description': 'Cards con probabilidades, pity counter y CTA Comprar ahora.'},
    {'title': 'Sets de temporada', 'description': 'Tarjetas XL con Ver detalles, Comprar y demo de aplicar.'},
    {'title': 'Personajes destacados', 'description': 'Compatibilidad con la rutina activa y contexto de progreso.'},
    {'title': 'Temas, Accesorios, Música y Animaciones', 'description': 'Grids específicos que respetan tokens visuales.'},
]

CATALOGUE_SPEC_DATA = {
    'facets': ['Tipo', 'Rareza', 'Personaje', 'Temporada', 'Estado (propio, vendible)', 'Precio Luks', 'Solo ofertas/relámpago'],
    'ordering': ['Relevancia (default)', 'Recientes', 'Precio asc/desc', 'Rareza', 'Fin de oferta'],
    'card': [
        'Imagen 1:1 o 3:4 con badge de rareza.',
        'Chips para personaje/temporada y etiqueta Nuevo/Limitado.',
        'Estado “En tu inventario” si ya lo posees.',
        'CTAs Comprar ahora o Ver en Mercado, además de Ver detalles.',
    ],
}

PRODUCT_DETAIL_SPEC_DATA = {
    'sections': [
        'Cabecera con nombre, rareza, personaje/temporada y estado de propiedad.',
        'Galería de imágenes o Rive con video corto opcional.',
        'Descripción y contenidos del pack/set con elementos incluidos.',
        'Probabilidades visibles con tooltips explicativos.',
        'Compatibilidad por personaje y requisitos previos.',
        'Precio en Luks y estimación fiat orientativa.',
        'Acciones: Comprar ahora, Añadir a deseos, Compartir.',
        'Sección técnica: colección, ID de serie, políticas de duplicados y royalties.',
        'Recomendados relacionados por personaje/temporada.',
    ],
}

CHECKOUT_SPEC_DATA = {
    'flow': [
        'Comprar ahora → conectar wallet (custodial por defecto, upgrade a non-custodial).',
        'Resumen con producto, precio, tarifas de red/royalties y total.',
        'Confirmar y firmar con feedback de estado de red.',
        'Recibo con hash/ID, fecha y asignación inmediata en inventario.',
    ],
    'protections': [
        'Reintentos con nonce distinto si falla la firma.',
        'Rate-limit en checkouts y captcha ante patrones anómalos.',
        'Quotes de red guardadas 60–120s para consistencia.',
    ],
}

WALLET_SPEC_DATA = [
    'Saldo LUKS (on-chain + espejo off-chain para UX).',
    'Depositar / Retirar con instrucciones, direcciones y QR.',
    'Historial de movimientos (compra, venta, premios, conversiones).',
    'Seguridad: 2FA, spending rápido, límites por transacción/día, avisos de riesgo.',
    'Conexiones: link con app móvil y exportación watch-only.',
]

MARKETPLACE_SPEC_DATA = {
    'modes': ['Precio fijo (Buy Now)', 'Subasta (MVP+1)', 'Ofertas (Make Offer)'],
    'facets': ['Tipo', 'Rareza', 'Personaje', 'Temporada', 'Precio LUKS', 'Estado', 'Serie/limitado', 'Vendedor verificado'],
    'ordering': ['Recientes', 'Precio asc/desc', 'Finaliza pronto', 'Más vistos', 'Rareza'],
    'listing_card': [
        'Thumbnail con rareza y personaje/temporada.',
        'Precio visible con badge de vendedor verificado.',
        'Pill con descuento porcentual si aplica.',
    ],
    'listing_detail': [
        'Galería, atributos, rareza/mapa de color y conversión estimada.',
        'Vendedor, royalties, fees y historial de propiedad/precios (mini-gráfico).',
        'Acciones: Comprar ahora, Hacer oferta, Ver en mi inventario, Compartir.',
    ],
    'create_listing': [
        'Seleccionar ítem desde inventario.',
        'Elegir tipo de venta y configurar precio/duración/cantidad.',
        'Revisión con tarifas (royalty, fee, gas) y preview.',
        'Firmar y publicar con opciones de gestión (pausar, editar, bajar).',
    ],
    'security': [
        'Marca de agua y auditoría de media.',
        'Verificación de origen del ítem y escrow inteligente.',
        'Cooldown post-compra antes de revender y flags automáticos.',
    ],
}

INVENTORY_SPEC_DATA = {
    'views': ['Todo', 'Abribles', 'Sets', 'Personajes', 'Carátulas', 'Colores', 'Accesorios', 'Música', 'Animaciones'],
    'facets': ['Rareza', 'Personaje', 'Temporada', 'Estado', 'Compatibilidad', 'Serie/limitado'],
    'actions': ['Abrir packs x1/x10', 'Aplicar set completo', 'Equipar accesorios por slot', 'Activar carátulas/colores/música/animaciones', 'Vender (precarga /vender)', 'Ver en Mercado'],
    'item_card': [
        'Estados: propio, equipado, nuevo, vendible, limitado, compatibilidad.',
        'Mini-acciones hover (desktop) o menú contextual (mobile).',
    ],
}

DESIGN_SPEC_DATA = {
    'color': 'Escala por rareza: común→mítico con tokens CSS (modo claro/oscuro).',
    'typography': 'Baloo 2 para titulares y Josefin Sans para cuerpo y labels.',
    'components': ['Píldoras Liquid Glass', 'Chips con contadores', 'Tarjetas con borde de rareza', 'Toasts de confirmación', 'Modales multi-paso'],
    'motion': ['Curvas MD3 emphasized', 'Animación count-up (350–600ms)', 'Animaciones de apertura tap-to-skip', 'Skeletons y lazy loading'],
    'accessibility': ['Contraste AA/AAA', 'Foco visible', 'Teclado completo', 'Roles ARIA y descripciones de medios'],
}

MICROCOPY_DATA = [
    'Comprar ahora', 'Firmar y obtener', 'Listar en Mercado', 'Confirmar listado',
    'Conecta tu wallet para continuar', 'Límites de gasto activos',
    'Probabilidades visibles. Sin sorpresas.', 'Tienes 3 accesorios equipables para Wimpy.',
]

TRANSPARENCY_SPEC_DATA = [
    'Divulgación de probabilidades en cada producto/pack.',
    'Royalties, fee de plataforma y gas claramente indicados.',
    'Limitaciones por región/edad con age gate si aplica.',
    'KYC/AML opcional para límites de retiro elevados.',
    'Compras con fiat → primero Luks (o no permitidas según jurisdicción).',
]

PERFORMANCE_SPEC_DATA = [
    'SSR/SSG para catálogos y producto con hydration de filtros.',
    'Imágenes/Rive vía CDN en formatos modernos (WebP/AVIF).',
    'Structured data schema.org/Product y Offer.',
    'Open Graph/Twitter Cards en PDP y listados.',
    'PWA instalable con offline shell para inventario de lectura.',
]

SECURITY_SPEC_DATA = [
    'Autenticación con 2FA y rotación de sesiones.',
    'CSRF y CSP estrictas con SRI en assets.',
    'Anti-bot: rate-limits, proof-of-work ligero y detección de automatización.',
    'Firmas visibles con hash/ID y tracking de reintentos.',
]

TELEMETRY_SPEC_DATA = {
    'events': ['view_product', 'add_to_wishlist', 'start_checkout', 'purchase_success', 'list_item', 'buy_listing', 'open_pack_web', 'apply_set_web', 'equip_accessory_web'],
    'kpis': ['Conversión a compra', 'Tasa de listado', 'Precio medio por rareza/personaje', 'Tiempo a primera compra', 'CTR de banner/hero'],
}

ADMIN_SPEC_DATA = [
    'Catálogo: CRUD de productos, temporadas, probabilidades, pity, bundles y precios.',
    'Promos: ventas relámpago con ventana y stock, banners/hero.',
    'Mercado: moderación, flags, disputas y escrow.',
    'Soporte: devoluciones/cancelaciones y auditoría de transacciones.',
]

INTERNATIONALIZATION_SPEC_DATA = [
    'Idiomas ES/EN con formatos de número/moneda (Luks + fiat).',
    'Zona horaria del usuario y copy culturalmente neutro.',
    'Glosario consistente (Set, Cofre, Sobre...).',
]

QA_SPEC_DATA = [
    'E2E de checkout y creación de listados.',
    'Pruebas de filtros pesados, back/forward y deep-links.',
    'Accesibilidad con teclado y lectores de pantalla.',
    'Resiliencia ante caídas de red, firmas fallidas y latencias altas.',
]

ROADMAP_SPEC_DATA = [
    {'label': 'MVP', 'items': ['Home Tienda', 'Catálogo', 'Detalle', 'Checkout LUKS', 'Inventario (lectura + vender)', 'Mercado precio fijo']},
    {'label': 'MVP+1', 'items': ['Abrir packs en web', 'Subastas/Ofertas', 'Gráficos históricos', 'PWA offline']},
    {'label': 'MVP+2', 'items': ['Forja con fragmentos', 'Gifting', 'Colecciones y logros web']},
]

CHECKLIST_DATA = [
    'IA y rutas listas.',
    'Header sticky con Bóveda/Wallet, Inventario, Tienda y Mercado.',
    'Catálogo con facetas completas (Tipo/Rareza/Personaje/Temporada/Precio/Propiedad).',
    'Detalle con probabilidades, royalties y compatibilidad.',
    'Checkout con wallet, resumen, firma y recibo.',
    'Marketplace con listado, detalle, creación y gestión.',
    'Inventario web con estados y acciones (abrir/aplicar/equipar/vender).',
    'Accesibilidad AA/AAA y rendimiento verde (SSR/CDN).',
    'Telemetría y dashboard de KPIs.',
    'Backoffice de catálogo, promos y mercado.',
]

GLOSSARY_DATA = [
    {'term': 'LUKS', 'definition': 'Token de valor de Buddy.'},
    {'term': 'Pack', 'definition': 'Cofre/caja/sobre abrible con probabilidades.'},
    {'term': 'Set', 'definition': 'Lote temático con rutina, tema, música y animaciones.'},
    {'term': 'Vendible', 'definition': 'Ítem transferible en el marketplace P2P.'},
    {'term': 'Pity Counter', 'definition': 'Garantía de rareza tras N aperturas.'},
]


def ux_principles() -> List[Dict[str, str]]:
    return _clone(UX_PRINCIPLES_DATA)


def information_architecture() -> List[Dict[str, str]]:
    return _clone(INFORMATION_ARCHITECTURE_DATA)


def url_policies() -> List[str]:
    return _clone(URL_POLICIES_DATA)


def header_layout() -> Dict[str, List[str]]:
    return _clone(HEADER_LAYOUT_DATA)


def home_sections() -> List[Dict[str, str]]:
    return _clone(HOME_SECTIONS_DATA)


def catalogue_spec() -> Dict[str, List[str]]:
    return _clone(CATALOGUE_SPEC_DATA)


def product_detail_spec() -> Dict[str, List[str]]:
    return _clone(PRODUCT_DETAIL_SPEC_DATA)


def checkout_spec() -> Dict[str, List[str]]:
    return _clone(CHECKOUT_SPEC_DATA)


def wallet_spec() -> List[str]:
    return _clone(WALLET_SPEC_DATA)


def marketplace_spec() -> Dict[str, List[str]]:
    return _clone(MARKETPLACE_SPEC_DATA)


def inventory_spec() -> Dict[str, List[str]]:
    return _clone(INVENTORY_SPEC_DATA)


def design_spec() -> Dict[str, Any]:
    return _clone(DESIGN_SPEC_DATA)


def microcopy() -> List[str]:
    return _clone(MICROCOPY_DATA)


def transparency_spec() -> List[str]:
    return _clone(TRANSPARENCY_SPEC_DATA)


def performance_spec() -> List[str]:
    return _clone(PERFORMANCE_SPEC_DATA)


def security_spec() -> List[str]:
    return _clone(SECURITY_SPEC_DATA)


def telemetry_spec() -> Dict[str, List[str]]:
    return _clone(TELEMETRY_SPEC_DATA)


def admin_spec() -> List[str]:
    return _clone(ADMIN_SPEC_DATA)


def internationalization_spec() -> List[str]:
    return _clone(INTERNATIONALIZATION_SPEC_DATA)


def qa_spec() -> List[str]:
    return _clone(QA_SPEC_DATA)


def roadmap_spec() -> List[Dict[str, Any]]:
    return _clone(ROADMAP_SPEC_DATA)


def checklist() -> List[str]:
    return _clone(CHECKLIST_DATA)


def glossary() -> List[Dict[str, str]]:
    return _clone(GLOSSARY_DATA)
