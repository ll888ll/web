# 📚 PLAN DE DOCUMENTACIÓN COMPLETO - PROYECTO CROODY

## 🎯 RESUMEN EJECUTIVO

Este plan de documentación establece una estructura completa y detallada para documentar TODOS los aspectos del proyecto Croody, un ecosistema híbrido de e-commerce y telemetría construido sobre Django, con arquitectura de microservicios, infraestructura AWS y CI/CD automatizado.

### Estado Actual
- ✅ Documentación existente: 8 documentos (enfocados en traducciones y fixes)
- 📋 Plan propuesto: 35+ documentos nuevos
- 🎯 Cobertura objetivo: 100% del ecosistema

---

## 📋 ESTRUCTURA GENERAL DE DOCUMENTACIÓN

### 🏗️ ORGANIZACIÓN PROPUESTA

```
docs/
├── 01-ARQUITECTURA/
│   ├── README.md
│   ├── overview.md
│   ├── microservicios.md
│   ├── patrones-diseño.md
│   └── diagrams/
│       ├── arquitectura-general.mdj
│       ├── flujo-datos.mdj
│       └── secuencia-interacciones.mdj
│
├── 02-BACKEND/
│   ├── README.md
│   ├── modelos/
│   │   ├── userprofile.md
│   │   ├── product.md
│   │   └── robotposition.md
│   ├── vistas/
│   │   ├── landing-views.md
│   │   ├── shop-views.md
│   │   └── telemetry-views.md
│   ├── api/
│   │   ├── rest-endpoints.md
│   │   ├── serializers.md
│   │   └── authentication.md
│   ├── señales.md
│   └── formularios.md
│
├── 03-FRONTEND/
│   ├── README.md
│   ├── design-system/
│   │   ├── tokens.md
│   │   ├── tipografia.md
│   │   ├── colores.md
│   │   ├── espaciado.md
│   │   └── geometria-sagrada.md
│   ├── componentes/
│   │   ├── botones.md
│   │   ├── cards.md
│   │   ├── formularios.md
│   │   ├── navegacion.md
│   │   └── selector-idiomas.md
│   ├── patrones-css.md
│   ├── javascript/
│   │   ├── theme-toggle.md
│   │   └── language-selector.md
│   └── accesibilidad.md
│
├── 04-INFRAESTRUCTURA/
│   ├── README.md
│   ├── terraform/
│   │   ├── vpc-setup.md
│   │   ├── security-groups.md
│   │   ├── networking.md
│   │   └── deployment.md
│   ├── dns/
│   │   ├── bind9-config.md
│   │   ├── zone-files.md
│   │   └── dns-management.md
│   └── aws/
│       ├── servicios-utilizados.md
│       ├── costes.md
│       └── mejores-practicas.md
│
├── 05-DEVOPS/
│   ├── README.md
│   ├── docker/
│   │   ├── imagenes.md
│   │   ├── compose.md
│   │   └── optimizacion.md
│   ├── ci-cd/
│   │   ├── workflows.md
│   │   ├── pipelines.md
│   │   └── testing-e2e.md
│   └── deployment/
│       ├── production.md
│       ├── staging.md
│       └── rollback.md
│
├── 06-SEGURIDAD/
│   ├── README.md
│   ├── configuraciones.md
│   ├── hardening.md
│   ├── hsts-csp.md
│   ├── csrf-rate-limiting.md
│   ├── auditoria.md
│   └── vulnerabilidades.md
│
├── 07-INTERNACIONALIZACION/
│   ├── README.md
│   ├── sistema-traduccion.md
│   ├── idiomas-soportados.md
│   ├── flujo-traduccion.md
│   ├── mantenimiento-i18n.md
│   └── guia-contribuidores.md
│
├── 08-DESARROLLO/
│   ├── README.md
│   ├── patrones-utilizados.md
│   ├── guia-estilo.md
│   ├── testing/
│   │   ├── unitarios.md
│   │   ├── integracion.md
│   │   └── e2e.md
│   └── contribucion/
│       ├── workflow.md
│       └── branching-model.md
│
├── 09-USUARIO/
│   ├── README.md
│   ├── funcionalidades/
│   │   ├── landing.md
│   │   ├── tienda.md
│   │   └── perfil-usuario.md
│   ├── flujos-trabajo.md
│   └── casos-uso.md
│
├── 10-OPERATIVO/
│   ├── README.md
│   ├── monitoreo.md
│   ├── logs.md
│   ├── alertas.md
│   ├── troubleshooting/
│   │   ├── problemas-comunes.md
│   │   ├── debug-mode.md
│   │   └── performance.md
│   ├── mantenimiento/
│   │   ├── backups.md
│   │   ├── actualizaciones.md
│   │   └── optimizacion.md
│   └── runbooks/
│       ├── incident-response.md
│       └── disaster-recovery.md
│
└── 11-APENDICES/
    ├── glosario.md
    ├── comandos-utiles.md
    ├── recursos.md
    └── changelog.md
```

---

## 📖 DETALLE DE CADA SECCIÓN

### 1. 📐 ARQUITECTURA

#### 1.1 overview.md
**Contenido:**
- Visión general del ecosistema Croody
- Diagrama de arquitectura de alto nivel
- Principios de diseño aplicados
- Decisiones arquitectónicas clave (ADR)
- Tecnologías utilizadas y justificación
- Mapeo de componentes vs responsabilidades

**Archivos críticos a referenciar:**
- `/docker-compose.yml` - Orquestación de servicios
- `/infra/terraform/main.tf` - Infraestructura como código
- `/proyecto_integrado/Croody/croody/settings.py` - Configuración Django

**Nivel de detalle:** Avanzado

**Estructura:**
- Markdown + diagramas Mermaid
- ADR en formato Markdown (tabla decisiones)
- Diagramas de componentes y flujo de datos

---

#### 1.2 microservicios.md
**Contenido:**
- Descripción de cada microservicio
  - **Croody Django**: E-commerce + autenticación
  - **Telemetry Gateway**: API FastAPI para telemetría
  - **IDS ML**: Sistema de detección de intrusiones
  - **Robot Sim**: Simulador de telemetría
  - **Gateway Nginx**: Reverse proxy y balanceador
- Comunicación entre servicios (REST API)
- Patrones de despliegue
- Gestión de estado distribuido
- Service mesh y observabilidad

**Archivos críticos:**
- `/services/telemetry-gateway/` - Código FastAPI
- `/services/ids-ml/` - Sistema ML
- `/robots/telemetry-robot/` - Simulador

**Nivel:** Avanzado
**Formato:** Markdown + diagramas secuencia

---

#### 1.3 patrones-diseño.md
**Contenido:**
- Patrones arquitectónicos implementados:
  - **Mixin Pattern**: LandingNavigationMixin, NavContextMixin
  - **QuerySet Manager Pattern**: ProductQuerySet
  - **ViewSet Pattern**: Para APIs REST
  - **Signal Pattern**: Signals.py en landing
  - **Factory Pattern**: En modelos con métodos de clase
  - **Observer Pattern**: En signals de Django
- Diagramas UML de cada patrón
- Beneficios y trade-offs
- Cuándo usar cada patrón

**Archivos:**
- `/landing/views.py` - Mixins y CBVs
- `/shop/models.py` - QuerySet manager
- `/landing/signals.py` - Sistema de señales

**Nivel:** Intermedio-Avanzado
**Formato:** Markdown + UML

---

### 2. 💾 BACKEND

#### 2.1 Modelos

##### userprofile.md
**Contenido:**
- Modelo completo UserProfile
- Relación OneToOne con User
- Campos y validaciones:
  - `user`, `display_name`, `preferred_language`
  - `preferred_theme` (system/dark/light)
  - `timezone`, `notification_level`
  - `telemetry_alerts`, `ingest_token`
  - `favorite_robot`, `bio`
- Generación de tokens de ingestión
- Señales de creación/actualización
- Métodos personalizados (`regenerate_token()`)
- Índices de base de datos
- Migraciones

**Archivos:**
- `/landing/models.py`
- `/landing/signals.py`
- `/landing/admin.py` (registro admin)

**Nivel:** Completo (básico → avanzado)

---

##### product.md
**Contenido:**
- Modelo Product de la tienda
- QuerySet manager personalizado:
  - `.published()` - Filtra productos publicados
  - `.search(query)` - Búsqueda full-text
- Campos: name, slug, teaser, description, price
- Campos de negocio: delivery_estimate, badge_label
- Estados: is_published, sort_order
- URL reversa con `get_absolute_url()`
- Optimización de consultas (select_related, prefetch_related)
- Índices en slug y price para performance

**Archivos:**
- `/shop/models.py`
- `/shop/admin.py`
- `/shop/migrations/0002_seed_products.py`

**Nivel:** Completo

---

##### robotposition.md
**Contenido:**
- Modelo RobotPosition para telemetría
- Campos: x, y (float), atmosphere (JSONField)
- Almacenamiento de datos de sensores (temp, humidity)
- Timestamp automático
- Ordenamiento por timestamp descendente
- Optimización para consultas de series temporales
- Consideraciones de performance para Big Data

**Archivos:**
- `/telemetry/models.py`
- `/telemetry/views.py` (endpoints API)

**Nivel:** Intermedio

---

#### 2.2 Vistas

##### landing-views.md
**Contenido:**

**Vistas implementadas:**
- **HomeView**: Landing principal
  - Mixins: LandingNavigationMixin
  - Contexto: hero, metrics, vectors
  - i18n completo con `gettext_lazy`
  - Funcionalidad de búsqueda global

- **AboutView**: Página "Nosotros"
  - Inyección de navegación
  - Contexto de marca

- **BuddyView**: Página producto Buddy
- **LuksView**: Página Luks
- **CroodyLoginView**: Autenticación personalizada
  - Form class: CroodyLoginForm
  - Widgets personalizados
- **ProfileView**: Gestión de perfil
- **ProfilePreferencesView**: Preferencias
- **TokenResetView**: Regeneración de tokens

**Patrones aplicados:**
- CBVs (Class-Based Views)
- Mixins para reutilización
- Context injection
- Form handling con validación
- Signals post-save

**Archivos:**
- `/landing/views.py`
- `/landing/forms.py`
- `/landing/urls.py`

**Nivel:** Completo
**Formato:** Markdown + ejemplos de código

---

##### shop-views.md
**Contenido:**

**Vistas implementadas:**
- **ProductListView**: Catálogo con paginación (12 items)
  - Filtros: búsqueda, tipo, rango de precio
  - Ordenamiento: precio asc/desc, recientes
  - Facetas heurísticas (cofre, set, accesorio)
  - Performance: QuerySet optimizado

- **ProductDetailView**: Detalle de producto
- **StoreView**: Vista general de tienda
- **NavContextMixin**: Inyección de navegación

**API Endpoints (sin DRF):**
- Búsqueda de productos (JSON)
- Filtros de catálogo (JSON)
- Autocomplete (JSON)

**Patrones:**
- CBVs con mixins
- QuerySet managers
- Optimización de BD (indexes)
- Faceted search

**Archivos:**
- `/shop/views.py`
- `/shop/urls.py`

**Nivel:** Completo

---

##### telemetry-views.md
**Contenido:**
- **TelemetryIngestView**: Endpoint para ingestión de datos
- **RobotPositionView**: CRUD posiciones
- **API REST personalizada** (sin DRF)
- Autenticación por tokens
- Validación de datos de sensores
- Almacenamiento en JSONField
- Rate limiting
- Documentación OpenAPI/Swagger

**Archivos:**
- `/telemetry/views.py`
- `/telemetry/urls.py`
- `/telemetry/utils.py`

**Nivel:** Intermedio-Avanzado

---

#### 2.3 API / REST Endpoints

##### rest-endpoints.md
**Contenido:**

**Endpoint Catalog:**

**Landing API:**
- `POST /auth/login/` - Autenticación
- `POST /auth/signup/` - Registro
- `GET /profile/` - Obtener perfil
- `PUT /profile/` - Actualizar perfil
- `POST /profile/token/reset/` - Regenerar token

**Shop API:**
- `GET /shop/products/` - Listar productos
- `GET /shop/products/{slug}/` - Detalle producto
- `GET /shop/search/` - Búsqueda con filtros
- `POST /shop/cart/` - Añadir al carrito

**Telemetry API:**
- `POST /api/telemetry/ingest/` - Ingestión datos
- `GET /api/telemetry/positions/` - Listar posiciones
- `GET /api/telemetry/positions/{id}/` - Detalle posición
- `GET /api/healthz/` - Health check

**Autenticación:**
- JWT tokens
- Session-based auth
- Token-based (telemetry)

**Códigos de estado HTTP**
**Manejo de errores**
**Rate limiting**

**Formato:** Markdown + OpenAPI specs

---

#### 2.4 Señales y Formularios

##### señales.md
**Contenido:**
- **UserProfile Creation Signal**
  - Creación automática al registrar User
  - Hooks de post_save
  - Generación de ingest_token

- **Profile Update Signal**
  - Actualización de timestamps
  - Invalidación de caché
  - Eventos de auditoría

**Patrón Observer implementado**

**Archivos:**
- `/landing/signals.py`
- `/landing/apps.py` (registro signals)

**Nivel:** Intermedio

---

##### formularios.md
**Contenido:**

**Formularios implementados:**

**CroodyLoginForm:**
- Campos: username, password
- Widgets personalizados con clases CSS
- Validación custom
- Error handling

**CroodySignupForm:**
- Campos: email, password, confirm_password
- Validación de email único
- Validación de contraseña segura
- Integración con UserProfile

**ProfileForm:**
- Campos: display_name, bio, favorite_robot
- Validación de longitud
- Sanitización de entrada

**ProfilePreferencesForm:**
- preferred_language (ChoiceField)
- preferred_theme (ChoiceField)
- timezone (CharField)
- notification_level (ChoiceField)
- telemetry_alerts (BooleanField)

**TokenResetForm:**
- Confirmación de regeneración
- Logging de auditoría

**Multi-step forms**
**Validación asíncrona**
**CSRF protection**

**Archivos:**
- `/landing/forms.py`

**Nivel:** Completo

---

### 3. 🎨 FRONTEND

#### 3.1 Design System

##### tokens.md
**Contenido:**

**Sistema de Tokens CSS (Geometría Sagrada):**

**Paletas de Color:**
- **Gator** (Verde Corporativo): 10 tonos (950→50)
- **Jungle** (Neutros): 10 tonos para temas
- **Sand** (Dorado cálido): Para Luks
- **Crimson** (Rojo): Para Buddy
- **Info/Warn/Error**: Sistema de feedback

**Tipografía:**
- **Font Sans**: Josefin Sans + fallbacks
- **Font Display**: Baloo 2
- **Escala**: 7 niveles (xs→4xl) con golden ratio
- **Line-height**: tight (1.15), base (1.55), loose (1.75)

**Espaciado (Golden Ratio):**
- Base: 8px
- Secuencia: 8, 13, 21, 34, 55, 89px
- Rational: φ (1.618) aplicado

**Radios:**
- 6, 10, 16, 24px (escala armónica)

**Bordes:**
- 1, 1.5, 2px

**Sombras (Staircase):**
- xs: 0 1px 2px rgba(0,0,0,.08)
- sm: 0 4px 12px rgba(20,30,20,.12)
- md: 0 10px 30px rgba(20,50,30,.16)
- lg: 0 25px 55px rgba(32,80,50,.25)

**Z-Index Scale:**
- 0, 1, 10, 100, 1000, 10000

**Contenedores:**
- Container-pad: 34px (desktop), 21px (mobile)
- Gutter: 24px
- Grid: 12 cols (desktop), 8 (tablet), 5 (mobile)

**Color Schemes:**
- Dark theme (default)
- Light theme
- Auto (detecta preferencia sistema)

**Brand Overrides:**
- Gator (default)
- Crimson (Buddy)
- Gold (Luks)

**Breakpoints:**
- Mobile: ≤ 767.98px
- Tablet: 768px → 1023.98px
- Desktop: ≥ 1024px

**Dark Theme:**
- bg: jungle-950
- surface-1: jungle-900
- fg: jungle-50
- brand-strong: gator-700

**Light Theme:**
- bg: gator-50
- surface-1: gator-100
- fg: jungle-900
- brand-strong: gator-300

**Accesibilidad:**
- color-scheme: light dark
- prefers-reduced-motion
- High contrast ratios (WCAG 2.1 AA)

**Archivos:**
- `/static/css/tokens.css` (307 líneas)

**Nivel:** Avanzado
**Formato:** Markdown + CSS examples

---

##### geometria-sagrada.md
**Contenido:**

**Principios Matemáticos:**
- **Número Áureo (φ = 1.618033988749...)**
- Aplicación en espaciado, proporciones, tipografía
- Secuencia de Fibonacci en spacing scale
- Golden rectangles en layouts

**Implementación:**
- Espaciado: φ^n progression
- Typography: Modular scale basada en φ
- Componentes: Proporciones áureas
- Iconografía: Círculos y rectángulos áureos

**Beneficios:**
- Armonía visual
- Consistencia estética
- Psicología perceptual
- Reconocimiento de marca

**Ejemplos prácticos:**
- Logo proportions
- Card aspect ratios
- Button sizes
- Grid systems

**Código CSS:**
```css
:root {
  --space-1: 8px;
  --space-2: calc(var(--space-1) * 1.618); /* 13px */
  --space-3: calc(var(--space-2) * 1.618); /* 21px */
  --space-4: calc(var(--space-3) * 1.618); /* 34px */
  /* ... */
}
```

**Research:**
- Referencia: "Divine Proportion" by Mario Livio
- Aplicación en arquitectura (Parthenon, Pyramids)
- Aplicación en diseño (Apple, Google Material)

**Nivel:** Avanzado
**Formato:** Markdown + Mathematical proofs

---

##### tipografia.md
**Contenido:**

**Sistema Tipográfico:**

**Fuentes Principales:**
- **Josefin Sans**: Sans-serif humanista
- **Baloo 2**: Display/heading font

**Fallback Stack:**
```css
"Josefin Sans", -apple-system, BlinkMacSystemFont, 
"Segoe UI", Roboto, "Helvetica Neue", Arial, 
"Noto Sans", sans-serif
```

**Jerarquía:**
- **Text XS**: 0.78rem (12.5px)
- **Text SM**: 0.9rem (14.4px)
- **Text BASE**: 1rem (16px) - root
- **Text LG**: 1.15rem (18.4px)
- **Text XL**: 1.33rem (21.3px)
- **Text 2XL**: 1.6rem (25.6px)
- **Text 3XL**: 2.1rem (33.6px)
- **Text 4XL**: clamp(2.3rem, 2vw + 2rem, 3.6rem)

**Line Heights:**
- Tight: 1.15 (headings)
- Base: 1.55 (body text)
- Loose: 1.75 (pull quotes)

**Pesos Disponibles:**
- 300 (Light)
- 400 (Regular)
- 500 (Medium)
- 600 (Semi-bold)
- 700 (Bold)

**Optimización:**
- Font-display: swap
- Preload critical fonts
- Font subsetting para performance
- Variable fonts consideration

**Responsive Typography:**
- clamp() para fluid scaling
- Viewport units para headings
- RFS (Responsive Font Size) consideration

**Accesibilidad:**
- Minimum 16px para body text
- Line height ≥ 1.5
- High contrast ratios
- Readable at 200% zoom

** Internacionalización:**
- Font support para 8 idiomas
- CJK fonts en fallbacks
- Arabic font stack
- Hindi font support

**Nivel:** Completo
**Formato:** Markdown + CSS samples

---

##### colores.md
**Contenido:**

**Paleta Corporativa:**

**Gator (Verde Primario):**
- 950: #041009 (Darkest)
- 900: #082015
- 800: #103924
- 700: #1C5C37
- 600: #277947
- 500: #3C9E5D (Base)
- 400: #5BB97D
- 300: #80D3A0
- 200: #B4E5C6
- 100: #DDF6E8
- 50: #F0FBF5 (Lightest)

**Jungle (Neutros):**
- 950: #050807 (bg dark)
- 900: #0B1311
- 800: #141F1B
- 700: #1E2C26
- 600: #293833
- 500: #374640
- 400: #56655F
- 300: #7A8883
- 200: #A9B4B0
- 100: #D3DAD7
- 50: #EEF1EF

**Sand (Dorado para Luks):**
- 600: #C18F4A
- 500: #E0B771
- 400: #F3D398
- 300: #F8E1B7
- 200: #FBECD1
- 100: #FDF5E6

**Crimson (Rojo para Buddy):**
- 7A1E2A (Deep)
- E04F56 (Primary)
- FFA7B5 (Soft)

**Sistema de Temas:**

**Dark Theme Variables:**
```css
:root, html[data-theme="dark"] {
  --bg: var(--jungle-950);
  --surface-1: var(--jungle-900);
  --surface-2: var(--jungle-800);
  --surface-3: var(--jungle-700);
  --fg: var(--jungle-50);
  --fg-muted: var(--jungle-200);
  --brand-strong: var(--gator-700);
  --brand-base: var(--gator-500);
  --brand-soft: var(--gator-300);
}
```

**Light Theme Variables:**
```css
html[data-theme="light"] {
  --bg: var(--gator-50);
  --surface-1: var(--gator-100);
  --surface-2: var(--gator-200);
  --fg: var(--jungle-900);
  --brand-strong: var(--gator-300);
  --brand-base: var(--gator-500);
}
```

**Brand Switching:**
- Gator (default)
- Crimson (Buddy section)
- Gold (Luks section)

**Semantic Colors:**
- Info: #31BFEA
- Warn: #F5B454
- Error: #F06565

**Color Accessibility:**
- WCAG 2.1 AA compliant
- Contrast ratios ≥ 4.5:1 (normal text)
- Contrast ratios ≥ 3:1 (large text)
- Dark mode optimized

**Color Psychology:**
- Green: Growth, trust, nature
- Red: Energy, passion, urgency
- Gold: Luxury, quality, value
- Neutral grays: Balance, sophistication

**Nivel:** Completo
**Formato:** Markdown + Color swatches

---

#### 3.2 Componentes

##### botones.md
**Contenido:**

**Tipos de Botones:**

**Primary Button:**
```html
<button class="btn btn-primary">
  <span class="btn-text">Label</span>
  <span class="btn-shimmer"></span>
</button>
```

**Estados:**
- Default
- Hover (shimmer effect)
- Active (pressed)
- Disabled
- Loading (spinner)

**Variantes:**
- Primary: brand-strong background
- Secondary: outline style
- Tertiary: ghost style
- Danger: error color

**Sizes:**
- XS: 32px height
- SM: 40px height
- MD: 48px height (default)
- LG: 56px height
- XL: 64px height

**Animaciones:**
- Shimmer effect (light sweep)
- Loading spinner
- Scale on active (0.98)
- Hover elevation (translateY)

**CSS Properties:**
```css
.btn-primary {
  background: var(--brand-strong);
  color: var(--on-brand);
  border-radius: var(--radius-2);
  padding: var(--space-2) var(--space-4);
  font-weight: 600;
  transition: all 300ms ease;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow);
}

.btn-primary:active {
  transform: scale(0.98);
}
```

**Accesibilidad:**
- ARIA labels
- Keyboard navigation
- Focus ring (orchid-500)
- Touch target ≥ 44px

**Icon Support:**
- Leading icons
- Trailing icons
- Icon-only (24px minimum)

**Nivel:** Intermedio
**Formato:** Markdown + HTML/CSS samples

---

##### cards.md
**Contenido:**

**Vector Cards (Hero Section):**

**Estructura:**
```html
<article class="vector-card fade-in-up">
  <header class="vector-card-header">
    <span class="badge">Fitness & Conexión</span>
  </header>
  <div class="vector-card-content">
    <h3 class="title">Buddy</h3>
    <p class="copy">Descripción...</p>
    <div class="keywords">tag1, tag2, tag3</div>
  </div>
  <footer class="vector-card-footer">
    <a href="#" class="cta">Call to Action</a>
  </footer>
</article>
```

**Estados:**
- Default
- Hover: translateY(-4px) + scale(1.01)
- Focus: outline ring
- Active: pressed state

**Hover Effects:**
```css
.vector-card:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: var(--shadow-lg);
  border-color: color-mix(in oklab, 
    var(--brand-base) 40%, transparent);
}
```

**Product Cards (Shop):**
- Image gallery
- Price display
- Badge (new, sale, etc.)
- Quick actions
- Rating system

**Animations:**
- fadeInUp
- Stagger delays (0.1s, 0.2s, 0.3s)
- GPU-accelerated (transform, opacity)

**Responsive:**
- Mobile: full width
- Tablet: 2 cols
- Desktop: 3-4 cols

**Accessibility:**
- Semantic HTML (article, header, footer)
- ARIA labels
- Keyboard navigation
- Screen reader support

**Nivel:** Intermedio
**Formato:** Markdown + HTML samples

---

##### selector-idiomas.md
**Contenido:**

**Language Selector Component:**

**Características:**
- 8 idiomas soportados:
  - Español (es) - default
  - English (en)
  - Français (fr)
  - Português (pt)
  - العربية (ar)
  - 简体中文 (zh-hans)
  - 日本語 (ja)
  - हिन्दी (hi)

**UI Elements:**
- Bandera de idioma actual
- Dropdown animado
- Lista de idiomas
- Indicador de idioma activo

**HTML Structure:**
```html
<div class="language-selector">
  <button class="lang-current" aria-expanded="false">
    <img src="flag-es.svg" alt="Español" class="flag">
    <span class="lang-code">ES</span>
    <svg class="chevron">...</svg>
  </button>
  <ul class="lang-dropdown" role="menu">
    <li><a href="/en/" data-lang="en">English</a></li>
    <li><a href="/fr/" data-lang="fr">Français</a></li>
    <!-- ... -->
  </ul>
</div>
```

**JavaScript Behavior:**
```javascript
// Toggle dropdown
document.querySelector('.lang-current').addEventListener('click', () => {
  const dropdown = document.querySelector('.lang-dropdown');
  dropdown.classList.toggle('open');
});

// Change language
document.querySelectorAll('.lang-dropdown a').forEach(link => {
  link.addEventListener('click', (e) => {
    window.location.href = e.target.href;
  });
});
```

**CSS Styling:**
```css
.language-selector {
  position: relative;
  display: inline-block;
}

.lang-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--surface-1);
  border-radius: var(--radius-2);
  box-shadow: var(--shadow-md);
  opacity: 0;
  transform: translateY(-10px);
  transition: all 200ms ease;
}

.lang-dropdown.open {
  opacity: 1;
  transform: translateY(0);
}
```

**Animations:**
- Dropdown slide-down (200ms)
- Flag icon spin (CSS)
- Staggered list items

**Accessibility:**
- ARIA expanded state
- Keyboard navigation (arrow keys, enter, escape)
- Focus management
- Screen reader labels

**Django i18n Integration:**
- URL prefixes: /en/, /fr/, etc.
- Middleware: LocaleMiddleware
- Persistence: Cookie + session
- Translations: {% trans %} tags

**Responsive:**
- Mobile: full width dropdown
- Desktop: right-aligned
- Touch-friendly (44px min height)

**Performance:**
- Flags as SVG (lightweight)
- Lazy load translations
- Minimal JavaScript

**Testing:**
- Unit tests for toggle
- E2E tests for language switching
- Visual regression tests

**Nivel:** Completo
**Formato:** Markdown + Code samples

---

#### 3.3 JavaScript

##### theme-toggle.md
**Contenido:**

**Theme Toggle System:**

**FOUC Prevention (Fix aplicado):**
```javascript
// Inicialización INMEDIATA (línea 11-16 theme.js)
(function initTheme() {
  const saved = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = saved || (prefersDark ? 'dark' : 'light');
  
  document.documentElement.setAttribute('data-theme', theme);
})();
```

**Theme Detection:**
- localStorage (user preference)
- System preference (prefers-color-scheme)
- Default: dark theme

**Toggle Button:**
```html
<button class="theme-toggle" aria-label="Toggle theme">
  <svg class="icon-sun" ...>...</svg>
  <svg class="icon-moon" ...>...</svg>
</button>
```

**JavaScript Logic:**
```javascript
const toggle = document.querySelector('.theme-toggle');
toggle.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  
  // Update icons
  toggle.querySelector('.icon-sun').style.display = next === 'dark' ? 'none' : 'block';
  toggle.querySelector('.icon-moon').style.display = next === 'dark' ? 'block' : 'none';
});
```

**CSS Variables:**
```css
:root, html[data-theme="dark"] {
  --bg: var(--jungle-950);
  --fg: var(--jungle-50);
  /* ... */
}

html[data-theme="light"] {
  --bg: var(--gator-50);
  --fg: var(--jungle-900);
  /* ... */
}
```

**Transition:**
- No flash on load (FOUC fixed)
- Smooth theme switching (300ms)
- No layout shift

**Performance:**
- Pure CSS variables (no reflow)
- GPU acceleration
- Minimal JavaScript

**Accessibility:**
- ARIA labels
- Keyboard navigation
- High contrast modes
- Respects reduced motion

**Browser Support:**
- Modern browsers (ES6+)
- Fallback for older browsers
- CSS custom properties support check

**Nivel:** Completo
**Formato:** Markdown + JavaScript code

---

#### 3.4 Accesibilidad

##### accesibilidad.md
**Contenido:**

**WCAG 2.1 AA Compliance:**

**Nivel A:**
- ✅ Imágenes con alt text
- ✅ Estructura semántica (header, nav, main, footer)
- ✅ Form labels asociados
- ✅ Orden de tabulación lógico
- ✅ Enlaces descriptivos

**Nivel AA:**
- ✅ Contraste de color ≥ 4.5:1
- ✅ Texto redimensionable hasta 200%
- ✅ Focus visible en todos los elementos interactivos
- ✅ Hover y focus states diferenciados
- ✅ Estados de error claros

**Técnicas implementadas:**

**Semántica HTML:**
```html
<header role="banner">
  <nav role="navigation" aria-label="Main navigation">
    <ul role="menubar">
      <li role="none">
        <a href="/" role="menuitem">Home</a>
      </li>
    </ul>
  </nav>
</header>
<main role="main">
  <article aria-labelledby="page-title">
    <h1 id="page-title">Page Title</h1>
  </article>
</main>
<footer role="contentinfo">
  <!-- Footer content -->
</footer>
```

**ARIA Labels:**
- Language selector: `aria-label="Select language"`
- Theme toggle: `aria-label="Toggle dark/light theme"`
- Search: `aria-label="Search products"`
- Navigation: `aria-label="Main navigation"`

**Focus Management:**
```css
:focus {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none;
}
```

**Reduced Motion:**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Keyboard Navigation:**
- Tab: navegación secuencial
- Enter/Space: activar botones
- Arrow keys: dropdowns
- Escape: cerrar modals/dropdowns

**Screen Reader Support:**
- Announcements para cambios de estado
- Live regions para notificaciones
- Skip links

**Color Accessibility:**
- Dark theme: High contrast ratios
- Light theme: Warm neutrals
- Brand colors: Tested contrast

**Touch Targets:**
- Minimum 44x44px
- Adequate spacing between targets

**Nivel:** Avanzado
**Formato:** Markdown + HTML samples

---

### 4. 🏗️ INFRAESTRUCTURA

#### 4.1 Terraform

##### vpc-setup.md
**Contenido:**

**VPC Configuration:**

**Main VPC:**
```hcl
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name        = "croody-vpc"
    Environment = "production"
    Project     = "croody-ecosystem"
  }
}
```

**Subnets:**
- Public Subnets (2 AZs)
- Private Subnets (2 AZs)
- Database Subnets (2 AZs)

**Internet Gateway:**
```hcl
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "croody-igw"
  }
}
```

**Route Tables:**
- Public route table (0.0.0.0/0 → IGW)
- Private route table (NAT Gateway)
- Database route table (private)

**NAT Gateway:**
```hcl
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id
  
  depends_on = [aws_internet_gateway.gw]
  
  tags = {
    Name = "croody-nat"
  }
}
```

**VPC Flow Logs:**
- Enabled para monitoring
- CloudWatch integration
- Retention: 30 días

**Network ACLs:**
- Stateful filtering
- Rules por subnet type
- Security best practices

**VPC Peering (si aplica):**
- Cross-account setup
- Route propagation
- Security groups rules

**Nivel:** Avanzado
**Formato:** HCL + Diagrams

---

##### security-groups.md
**Contenido:**

**Security Groups (Stateful Firewalls):**

**Web Tier (Croody Django):**
```hcl
resource "aws_security_group" "web" {
  name_prefix = "croody-web-"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP from anywhere"
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS from anywhere"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }
}
```

**Database Tier:**
```hcl
resource "aws_security_group" "db" {
  name_prefix = "croody-db-"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
    description     = "PostgreSQL from web tier"
  }
}
```

**Load Balancer:**
```hcl
resource "aws_security_group" "alb" {
  name_prefix = "croody-alb-"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP from internet"
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS from internet"
  }
}
```

**Rules:**
- Least privilege principle
- No 0.0.0.0/0 outbound rules (except web)
- Stateful (return traffic automatic)
- Documentation en tags

**Best Practices:**
- No SG con 0.0.0.0/0 en inbound (except LB)
- Use named SGs en lugar de CIDRs
- Regular audit con AWS Config
- VPC Flow Logs enabled

**Nivel:** Avanzado
**Formato:** HCL + Network diagrams

---

#### 4.2 DNS

##### bind9-config.md
**Contenido:**

**BIND9 DNS Server:**

**Docker Compose Setup:**
```yaml
services:
  bind:
    image: ubuntu/bind9:latest
    container_name: croody-bind
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "127.0.0.1:8888:8888"
    volumes:
      - ./zones:/etc/bind/zones
      - ./config/named.conf.local:/etc/bind/named.conf.local
      - ./config/named.conf.options:/etc/bind/named.conf.options
    command: ["named", "-c", "/etc/bind/named.conf", "-g"]
    restart: unless-stopped
```

**named.conf.options:**
```bind
options {
    directory "/var/cache/bind";
    
    forwarders {
        8.8.8.8;
        8.8.4.4;
    };
    
    dnssec-validation auto;
    
    auth-nxdomain no;
    
    listen-on { any; };
    listen-on-v6 { any; };
};
```

**Zone File (croody.app):**
```bind
$TTL 86400
@       IN      SOA     ns1.croody.app. admin.croody.app. (
                        2024010101      ; Serial
                        3600            ; Refresh
                        1800            ; Retry
                        604800          ; Expire
                        86400 )         ; Minimum TTL

; NS Records
@       IN      NS      ns1.croody.app.

; A Records
ns1     IN      A       192.0.2.1
www     IN      A       192.0.2.10
api     IN      A       192.0.2.10
```

**DNSSEC:**
- Automatic validation
- Key signing
- Zone signing

**DNS Management:**
- zone command tool
- dynamic updates
- incremental transfers (IXFR)

**Security:**
- Rate limiting
- Recursion control
- Access control lists (ACL)
- No open recursion

**Monitoring:**
- Query logging
- Statistics channel (port 8888)
- Integration con Prometheus

**Nivel:** Avanzado
**Formato:** BIND config + DNS diagrams

---

##### zone-files.md
**Contenido:**

**Zone File Management:**

**Zone Structure:**
```
$ORIGIN croody.app.
$TTL 86400

; SOA Record
@       IN      SOA     ns1.croody.app. (
                        2024010101      ; Serial (YYYYMMDDNN)
                        3600            ; Refresh (1h)
                        1800            ; Retry (30m)
                        604800          ; Expire (7d)
                        86400 )         ; Minimum TTL (1d)
```

**Resource Records:**

**A Records (IPv4):**
```
; Load Balancer
lb      IN      A       192.0.2.10

; Application Servers
app1    IN      A       192.0.2.11
app2    IN      A       192.0.2.12

; Database
db      IN      A       192.0.2.20

; Monitoring
prom    IN      A       192.0.2.30
graf    IN      A       192.0.2.31
```

**CNAME Records:**
```
; Aliases
www     IN      CNAME   lb.croody.app.
api     IN      CNAME   lb.croody.app.
docs    IN      CNAME   lb.croody.app.
```

**MX Records (Email):**
```
; Mail Exchange
@       IN      MX 10   mail.croody.app.
mail    IN      A       192.0.2.40
```

**TXT Records (SPF, DKIM, etc.):**
```
; SPF Record
@       IN      TXT     "v=spf1 include:_spf.google.com ~all"

; DKIM
default._domainkey IN TXT "v=DKIM1; k=rsa; p=MIIBIjANBgkqh..."

; DMARC
_dmarc  IN      TXT     "v=DMARC1; p=quarantine; rua=mailto:dmarc@croody.app"
```

**AAAA Records (IPv6):**
```
; IPv6 support
lb      IN      AAAA    2001:db8::10
app1    IN      AAAA    2001:db8::11
```

**SRV Records:**
```
; Service records
_sip._tcp     IN      SRV     10      50      5060    sip.croody.app.
_imaps._tcp   IN      SRV     0       1       993     mail.croody.app.
```

**Zone File Best Practices:**
- Use $ORIGIN for relative names
- Increment Serial on every change
- Reasonable TTL values (3600 = 1h)
- Document all changes
- Test before deployment

**Dynamic DNS:**
- nsupdate command
- DHCP integration
- API automation

**Nivel:** Intermedio-Avanzado
**Formato:** BIND zone files + Examples

---

### 5. 🔧 DEVOPS

#### 5.1 Docker

##### imagenes.md
**Contenido:**

**Docker Image Strategy:**

**Croody Django Image:**
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --spider -q http://localhost:8000/ || exit 1

# Expose port
EXPOSE 8000

# Entrypoint
COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
```

**Image Optimization:**
- Multi-stage builds (production)
- Python slim base image
- No cache for pip
- Health checks
- Non-root user (security)

**Image Layers:**
1. Base Python
2. System deps
3. Python deps
4. App code
5. Entrypoint

**Security:**
- Minimal attack surface
- No unnecessary tools
- Regular base image updates
- Scan for vulnerabilities (Trivy)

**Build Context:**
- .dockerignore file
- Exclude venv, .git, __pycache__
- Optimize build cache

**Multi-Architecture:**
- arm64 and amd64 support
- Buildx for cross-platform

**Registry:**
- Docker Hub / AWS ECR
- Tagging strategy (semver)
- Image promotions (dev → staging → prod)

**Nivel:** Avanzado
**Formato:** Dockerfile + Build strategies

---

##### compose.md
**Contenido:**

**Docker Compose Multi-Service:**

**Service Architecture:**
```yaml
version: '3.8'

services:
  gateway:  # Nginx reverse proxy
    image: nginx:alpine
    container_name: gateway_new
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./gateway/nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./gateway/ssl:/etc/nginx/ssl:ro
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1"]
      interval: 10s
      timeout: 3s
      retries: 5
    read_only: true
    tmpfs:
      - /var/cache/nginx
      - /var/run
    mem_limit: 256m
    cpus: "0.50"
    depends_on:
      - croody
      - telemetry-gateway
      - ids-ml

  croody:  # Django application
    build:
      context: ./Croody
      dockerfile: Dockerfile
    container_name: croody_new
    restart: unless-stopped
    environment:
      - DJANGO_SETTINGS_MODULE=croody.settings
      - DATABASE_URL=sqlite:////data/croody.db
    volumes:
      - ./Croody:/app
      - croody_data:/data
    expose:
      - "8000"
    mem_limit: 512m
    cpus: "0.50"
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8000/"]
      interval: 10s
      timeout: 5s
      retries: 10

  telemetry-gateway:  # FastAPI service
    build:
      context: ./services/telemetry-gateway
      dockerfile: Dockerfile
    container_name: telemetry-gateway_new
    restart: unless-stopped
    environment:
      - TG_DB_PATH=/data/telemetry.db
    volumes:
      - telemetry_data:/data
    expose:
      - "9000"
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:9000/healthz"]
      interval: 10s
      timeout: 3s
      retries: 5

  ids-ml:  # Machine Learning service
    build:
      context: ./services/ids-ml
      dockerfile: Dockerfile
    container_name: ids-ml_new
    restart: unless-stopped
    volumes:
      - ./services/ids-ml/models:/models
    expose:
      - "9100"

  robot-sim:  # Telemetry simulator
    build:
      context: ./robots/telemetry-robot
    container_name: robot_sim
    restart: unless-stopped
    ports:
      - "9090:9090"
    environment:
      - TELEMETRY_INGEST_URL=http://telemetry-gateway:9000/api/telemetry/ingest
      - ROBOT_ID=robot-clases

volumes:
  croody_data:
  telemetry_data:
```

**Networking:**
- Custom bridge network
- Service discovery via DNS
- Internal communication (expose vs ports)
- External access only through gateway

**Data Persistence:**
- Named volumes for data
- Volume backups
- Volume permissions

**Resource Limits:**
- mem_limit for each service
- cpus limit
- Health checks for all services

**Restart Policies:**
- unless-stopped for production
- always for critical services

**Environment Variables:**
- .env file support
- Different configs per env
- Secrets management

**Nivel:** Completo
**Formato:** YAML + Service diagrams

---

#### 5.2 CI/CD

##### workflows.md
**Contenido:**

**GitHub Actions Workflows:**

**1. ci.yml - Continuous Integration:**
```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Cache pip
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
        run: |
          pytest --cov=./ --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

**2. deploy.yml - Deployment:**
```yaml
name: Deploy

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build image
        run: |
          docker build -t croody:${{ github.ref_name }} ./proyecto_integrado/Croody
      
      - name: Login to registry
        uses: docker/login-action@v2
        with:
          registry: ${{ secrets.REGISTRY }}
          username: ${{ secrets.USERNAME }}
          password: ${{ secrets.PASSWORD }}
      
      - name: Push image
        run: |
          docker push ${{ secrets.REGISTRY }}/croody:${{ github.ref_name }}
      
      - name: Deploy to production
        run: |
          ssh deploy@server "docker-compose pull && docker-compose up -d"
```

**3. full-stack-validate.yml - E2E Tests:**
```yaml
name: Full Stack Validation

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  e2e:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Start services
        run: docker-compose up -d
        
      - name: Wait for services
        run: |
          timeout 120 bash -c 'until curl -f http://localhost:8000/; do sleep 5; done'
      
      - name: Run Playwright tests
        uses: microsoft/playwright@v1.30
        with:
          install-browser: true
          tests: tests/e2e/
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

**Workflow Triggers:**
- push to main/develop
- pull_request to main
- tags (v*)
- schedule (cron)

**Job Dependencies:**
- test → build → deploy
- Parallel execution where possible

**Secrets Management:**
- Docker registry credentials
- SSH keys for deployment
- Database URLs
- API keys

**Artifacts:**
- Test reports
- Coverage reports
- Build images
- Deployment logs

**Nivel:** Avanzado
**Formato:** YAML + Pipeline diagrams

---

##### testing-e2e.md
**Contenido:**

**End-to-End Testing Strategy:**

**Testing Stack:**
- **Playwright**: E2E testing framework
- **pytest**: Test runner
- **Allure**: Test reporting
- **GitHub Actions**: CI integration

**Test Scenarios:**

**Landing Page:**
```python
import pytest
from playwright.sync_api import Page, expect

def test_homepage_loads(page: Page):
    page.goto("/")
    
    # Check hero section
    expect(page.locator('h1')).to_contain_text('Volvamos a ser humanos')
    
    # Check navigation
    expect(page.locator('nav')).to_be_visible()
    
    # Check vector cards
    cards = page.locator('.vector-card')
    expect(cards).to_have_count(3)

def test_language_switcher(page: Page):
    page.goto("/")
    
    # Click language selector
    page.click('.language-selector .lang-current')
    
    # Select English
    page.click('[data-lang="en"]')
    
    # Verify URL changed
    expect(page).to_have_url("*/en/")
    
    # Check content translated
    expect(page.locator('h1')).to_contain_text('Let\'s be human again')
```

**Theme Toggle:**
```python
def test_theme_toggle(page: Page):
    page.goto("/")
    
    # Get initial theme
    initial_theme = page.evaluate('document.documentElement.getAttribute("data-theme")')
    
    # Toggle theme
    page.click('.theme-toggle')
    
    # Check theme changed
    new_theme = page.evaluate('document.documentElement.getAttribute("data-theme")')
    assert initial_theme != new_theme
    
    # Check persistence
    page.reload()
    expect(page.locator('html')).to_have_attribute('data-theme', new_theme)

def test_no_fouc(page: Page):
    """Test no Flash of Unstyled Content"""
    page.goto("/", wait_until='domcontentloaded')
    
    # Check theme is set immediately
    theme = page.evaluate('document.documentElement.getAttribute("data-theme")')
    assert theme in ['light', 'dark']
    
    # Check no flash (no default theme)
    styles = page.evaluate('''
        [...document.styleSheets].flatMap(ss => [...ss.cssRules]).map(r => r.style && r.style.all)
    ''')
    # Verify no flash occurred
```

**Shop Tests:**
```python
def test_product_listing(page: Page):
    page.goto("/tienda/")
    
    # Check products loaded
    products = page.locator('.product-card')
    expect(products).to_have_count(10)
    
    # Check filters
    page.fill('input[name="q"]', 'cofre')
    page.click('button[type="submit"]')
    
    # Verify filtered results
    expect(page.locator('.product-card')).to_contain_text('cofre')

def test_product_detail(page: Page):
    page.goto("/tienda/")
    
    # Click first product
    page.click('.product-card:first-child a')
    
    # Check detail page
    expect(page.locator('.product-title')).to_be_visible()
    expect(page.locator('.product-price')).to_be_visible()
```

**Authentication:**
```python
def test_login(page: Page):
    page.goto("/auth/login/")
    
    # Fill form
    page.fill('input[name="username"]', 'testuser')
    page.fill('input[name="password"]', 'testpass')
    
    # Submit
    page.click('button[type="submit"]')
    
    # Check redirect to home
    expect(page).to_have_url("*/")
    
    # Check user logged in
    expect(page.locator('.user-menu')).to_be_visible()
```

**Responsive Testing:**
```python
@pytest.mark.parametrize("viewport", [
    {"width": 375, "height": 667},  # Mobile
    {"width": 768, "height": 1024}, # Tablet
    {"width": 1920, "height": 1080} # Desktop
])
def test_responsive_layout(page: Page, viewport):
    page.set_viewport_size(viewport)
    page.goto("/")
    
    # Check mobile menu
    if viewport["width"] < 768:
        expect(page.locator('.mobile-menu-button')).to_be_visible()
        page.click('.mobile-menu-button')
        expect(page.locator('.mobile-menu')).to_be_visible()
    else:
        expect(page.locator('.desktop-nav')).to_be_visible()
```

**Performance Tests:**
```python
def test_page_load_speed(page: Page):
    start_time = time.time()
    page.goto("/", wait_until='networkidle')
    load_time = time.time() - start_time
    
    # Check load time < 2 seconds
    assert load_time < 2.0

def test_cumulative_layout_shift(page: Page):
    page.goto("/")
    
    # Check CLS < 0.1
    cls = page.evaluate('window.performance.getEntriesByType("layout-shift").reduce((sum, entry) => sum + entry.value, 0)')
    assert cls < 0.1
```

**CI Integration:**
```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Start Docker Compose
        run: docker-compose up -d
        
      - name: Wait for services
        run: |
          ./scripts/wait-for-services.sh
          
      - name: Run Playwright tests
        uses: microsoft/playwright@v1.30
        with:
          install-browser: true
          tests: tests/e2e/
          
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

**Best Practices:**
- Test data isolation
- Parallel execution
- Flaky test detection
- Visual regression testing
- Accessibility testing (axe-core)

**Nivel:** Avanzado
**Formato:** Python + YAML

---

### 6. 🔒 SEGURIDAD

#### 6.1 Configuraciones

##### configuraciones.md
**Contenido:**

**Django Security Settings:**

**settings.py Security:**
```python
# SECURITY SETTINGS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS Redirect
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie Settings
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Password Hashers
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

# CSRF Protection
CSRF_TRUSTED_ORIGINS = [
    "https://croody.app",
    "https://www.croody.app",
]
```

**CSP (Content Security Policy):**
```python
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
```

**Rate Limiting:**
```python
# middleware.py
from django.core.cache import cache
from django.http import JsonResponse

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        key = f'rate_limit:{ip}'
        
        # Check rate limit (100 requests per minute)
        if cache.get(key, 0) >= 100:
            return JsonResponse(
                {'error': 'Rate limit exceeded'},
                status=429
            )
        
        # Increment counter
        cache.incr(key)
        cache.expire(key, 60)  # 1 minute window
        
        return self.get_response(request)
```

**Security Headers:**
- HSTS: Enforce HTTPS
- CSP: XSS protection
- X-Frame-Options: Clickjacking protection
- Referrer-Policy: Privacy protection

**Nivel:** Avanzado
**Formato:** Python + Headers

---

##### hardening.md
**Contenido:**

**System Hardening:**

**OS Level:**
- Regular security updates
- Firewall configuration (ufw)
- SSH key-based authentication
- Disable root login
- Fail2ban for brute force protection

**Docker Security:**
```dockerfile
# Non-root user
RUN addgroup --system --gid 1001 appuser
RUN adduser --system --uid 1001 appuser
USER appuser

# Read-only root filesystem
RUN chmod -R 755 /app
# Use read-only FS in production

# No unnecessary tools
RUN apt-get remove --purge -y wget curl netcat
```

**Docker Compose Security:**
```yaml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - SETGID
      - SETUID
```

**Application Security:**
- Input validation
- Output encoding
- SQL injection prevention (ORM)
- XSS protection (auto-escape)
- CSRF tokens
- Secure session management

**Database Security:**
- Encrypted connections (SSL)
- Least privilege (dedicated user)
- Regular backups
- Connection pooling

**Secrets Management:**
- Environment variables
- Docker secrets
- AWS Secrets Manager
- No secrets in code

**Monitoring:**
- Failed login attempts
- Suspicious activity
- Intrusion detection
- Log monitoring (ELK stack)

**Nivel:** Avanzado
**Formato:** Checklist + Config

---

#### 6.2 Auditoría

##### auditoria.md
**Contenido:**

**Security Audit Tools:**

**Bandit (Python Security Linter):**
```yaml
# .bandit
[bandit]
exclude_dirs = tests,venv,.venv
skips = B101,B601

# Run bandit
bandit -r . -f json -o bandit-report.json
```

**Safety (Dependency Vulnerability Scanning):**
```bash
# Check dependencies
safety check --json --output safety-report.json

# Fix vulnerabilities
safety update
```

**OWASP ZAP (Web App Scanner):**
```yaml
# Docker zap-baseline
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://croody.app \
  -J zap-report.json
```

**Audit Logging:**
```python
# models.py
import logging

audit_logger = logging.getLogger('audit')

class UserProfile(models.Model):
    # ... fields ...
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Log changes
        audit_logger.info(
            f"UserProfile {'created' if is_new else 'updated'}: {self.user.username}"
        )

# middleware.py
class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Log sensitive operations
        if request.method in ['POST', 'PUT', 'DELETE']:
            audit_logger.info(
                f"{request.user} {request.method} {request.path} "
                f"from {request.META['REMOTE_ADDR']}"
            )
        
        return response
```

**Vulnerability Assessment:**
- Automated scans (daily)
- Manual penetration testing (quarterly)
- Dependency updates (weekly)
- Security training (monthly)

**Incident Response:**
- Detection playbook
- Escalation procedures
- Forensics process
- Recovery plan

**Compliance:**
- GDPR requirements
- Data protection
- Privacy policies
- Data retention

**Nivel:** Avanzado
**Formato:** Tools + Procedures

---

### 7. 🌍 INTERNACIONALIZACIÓN

#### 7.1 Sistema de Traducción

##### sistema-traduccion.md
**Contenido:**

**Django i18n Architecture:**

**Configuration:**
```python
# settings.py
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
    ('fr', 'Français'),
    ('pt', 'Português'),
    ('ar', 'العربية'),
    ('zh-hans', '简体中文'),
    ('ja', '日本語'),
    ('hi', 'हिन्दी'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

USE_I18N = True
USE_L10N = True
USE_TZ = True

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Must be after SessionMiddleware
    'django.middleware.common.CommonMiddleware',
    # ...
]
```

**URL Configuration:**
```python
# urls.py
from django.conf.urls.i18n import i18n_patterns
from django.urls import path

urlpatterns = i18n_patterns(
    path('', include('landing.urls')),
    path('tienda/', include('shop.urls')),
    path('telemetry/', include('telemetry.urls')),
    prefix_default_language=False,  # Remove /es/ prefix for default
)
```

**Translation Methods:**

**In Templates:**
```django
{% load i18n %}
{% trans "Hello World" %}

{% blocktrans %}
  This is a multi-line
  translation with {{ variable }}.
{% endblocktrans %}

{% get_current_language as LANGUAGE_CODE %}
{% get_language_info for LANGUAGE_CODE as lang %}
```

**In Python Code:**
```python
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _

# Lazy translation (recommended)
name = _('Username')

# Translation with context
from django.utils.translation import pgettext
name = pgettext('user name', 'Name')

# Pluralization
from django.utils.translation import ngettext
message = ngettext(
    '%d result',
    '%d results',
    count
) % count
```

**Custom Translation Script (Sin gettext):**
```python
# compile_translations.py
import os
from pathlib import Path
from babel.messages.pofile import read_po, write_po
from babel.messages.mofile import write_mo

def compile_translations():
    locale_dir = Path(__file__).parent / 'locale'
    
    for lang_dir in locale_dir.iterdir():
        if lang_dir.is_dir() and (lang_dir / 'LC_MESSAGES' / 'django.po').exists():
            po_file = lang_dir / 'LC_MESSAGES' / 'django.po'
            mo_file = lang_dir / 'LC_MESSAGES' / 'django.mo'
            
            with po_file.open('rb') as f:
                catalog = read_po(f)
            
            with mo_file.open('wb') as f:
                write_mo(f, catalog)
            
            print(f"Compiled {po_file} → {mo_file}")
```

**Database Translation (Optional):**
```python
# models.py
from django.db.models import CharField, TextField
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = CharField(max_length=120)
    # ...
    
    # Method for translation
    def get_translated_name(self, lang='es'):
        # Get from translation table
        return Translation.objects.get(
            content_type=self.get_content_type(),
            object_id=self.id,
            field='name',
            language=lang
        ).text
```

**Language Detection:**
- URL prefix (/en/, /es/)
- User profile preference
- Session storage
- Cookie (django_language)
- Browser preference (fallback)

**Static Translation:**
```python
# utils.py
def get_available_languages():
    return [
        {'code': 'es', 'name': 'Español', 'flag': '🇪🇸'},
        {'code': 'en', 'name': 'English', 'flag': '🇺🇸'},
        {'code': 'fr', 'name': 'Français', 'flag': '🇫🇷'},
        # ...
    ]
```

**Nivel:** Completo
**Formato:** Django i18n patterns

---

##### idiomas-soportados.md
**Contenido:**

**Supported Languages:**

**1. Español (es) - Default:**
- Locale: es
- Direction: LTR
- Character set: UTF-8
- Status: ✅ Complete
- Coverage: 100%
- Translator: Native team

**2. English (en):**
- Locale: en
- Direction: LTR
- Status: ✅ Complete
- Coverage: 100% (65+ strings)
- File: locale/en/LC_MESSAGES/django.po
- Notes: Professional translation

**3. Français (fr):**
- Locale: fr
- Direction: LTR
- Status: 🔄 Partial
- Coverage: 80%
- File: locale/fr/LC_MESSAGES/django.po
- Issues: Duplicate messages cleaned

**4. Português (pt):**
- Locale: pt
- Direction: LTR
- Status: 🔄 Ready (template created)
- Coverage: 0% (needs translation)
- File: locale/pt/LC_MESSAGES/django.po

**5. العربية (ar) - Arabic:**
- Locale: ar
- Direction: RTL (Right-to-Left)
- Status: 🔄 Ready
- Coverage: 0%
- Notes: RTL support in CSS:
  ```css
  [dir="rtl"] .navigation {
    direction: rtl;
  }
  ```

**6. 简体中文 (zh-hans) - Simplified Chinese:**
- Locale: zh-hans
- Direction: LTR
- Status: 🔄 Ready
- Coverage: 0%
- File: locale/zh_Hans/LC_MESSAGES/django.po

**7. 日本語 (ja) - Japanese:**
- Locale: ja
- Direction: LTR
- Status: 🔄 Ready
- Coverage: 0%

**8. हिन्दी (hi) - Hindi:**
- Locale: hi
- Direction: LTR
- Status: 🔄 Ready
- Coverage: 0%

**RTL Support:**
```css
html[lang="ar"] {
  direction: rtl;
}

html[lang="ar"] .navigation {
  text-align: right;
}

html[lang="ar"] .brand-logo {
  order: 2;
}
```

**Font Support:**
- Arabic: Noto Sans Arabic
- Chinese: Noto Sans SC
- Japanese: Noto Sans JP
- Hindi: Noto Sans Devanagari

**Translation Coverage Metrics:**
```python
# Script to calculate coverage
def calculate_coverage(locale_dir):
    po_file = locale_dir / 'django.po'
    if not po_file.exists():
        return 0
    
    with open(po_file) as f:
        catalog = read_po(f)
    
    total = len(catalog)
    translated = len([m for m in catalog if m.string])
    
    return (translated / total) * 100 if total > 0 else 0
```

**Translation Workflow:**
1. Extract strings with `makemessages`
2. Send .po files to translators
3. Receive translated .po files
4. Compile with `compilemessages` or custom script
5. Deploy and test

**Nivel:** Completo
**Formato:** Language matrix + RTL guide

---

### 8. 🛠️ DESARROLLO

#### 8.1 Patrones Utilizados

##### patrones-utilizados.md
**Contenido:**

**Design Patterns Implementation:**

**1. Mixin Pattern:**
```python
# landing/views.py
class LandingNavigationMixin:
    """Injects navigation and search results."""
    
    def get_nav_links(self) -> list[dict[str, str]]:
        return primary_nav_links()
    
    def get_search_results(self) -> list[dict[str, str]]:
        return global_search_entries()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.setdefault('nav_links', self.get_nav_links())
        context.setdefault('search_results', self.get_search_results())
        return context

# Usage
class HomeView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/home.html'
    # Automatically gets nav and search in context
```

**Benefits:**
- Code reuse across views
- Multiple inheritance
- Composable behavior
- Separation of concerns

**2. QuerySet Manager Pattern:**
```python
# shop/models.py
class ProductQuerySet(models.QuerySet):
    """Custom QuerySet for Product model."""
    
    def published(self) -> 'ProductQuerySet':
        """Filter only published products."""
        return self.filter(is_published=True)
    
    def search(self, query: str) -> 'ProductQuerySet':
        """Search products by name or teaser."""
        if not query:
            return self
        return self.filter(
            models.Q(name__icontains=query) |
            models.Q(teaser__icontains=query)
        )

# Usage
Product.objects.published().search('cofre')
```

**Benefits:**
- Reusable query logic
- Chaining methods
- Type hints support
- IDE autocomplete

**3. Signal Pattern (Observer):**
```python
# landing/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when User is created."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()

# landing/apps.py
default_app_config = 'landing.apps.LandingConfig'
```

**Benefits:**
- Decoupled logic
- Event-driven architecture
- Multiple receivers possible
- Reduced model code

**4. ViewSet Pattern (API):**
```python
# Alternative to DRF ViewSets
class ProductViewSet:
    """REST API for products without DRF."""
    
    def list(self, request):
        queryset = Product.objects.published()
        serializer = ProductSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def detail(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return JsonResponse(
                {'error': 'Product not found'},
                status=404
            )
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)
```

**5. Factory Pattern (Model Methods):**
```python
# Alternative implementation
class UserProfile(models.Model):
    # ... fields ...
    
    @classmethod
    def create_for_user(cls, user, **kwargs):
        """Factory method to create profile."""
        return cls.objects.create(
            user=user,
            preferred_language='es',
            preferred_theme='system',
            **kwargs
        )
```

**6. Context Injection Pattern:**
```python
class NavContextMixin:
    """Context data injection via mixins."""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Inject navigation
        context['nav_links'] = primary_nav_links()
        # Inject brand
        context['brand'] = getattr(self, 'brand', 'gator')
        return context
```

**Pattern Selection Guidelines:**
- Use Mixins for cross-cutting concerns
- Use Managers for query logic
- Use Signals for events
- Use Factories for object creation
- Use Context Injection for view data

**Anti-Patterns to Avoid:**
- Fat models (use signals)
- Duplicate queries (use managers)
- Hardcoded strings (use i18n)
- Magic numbers (use constants)

**Nivel:** Intermedio-Avanzado
**Formato:** Pattern catalog + UML

---

#### 8.2 Testing

##### unitarios.md
**Contenido:**

**Unit Testing Strategy:**

**Tools:**
- **pytest**: Test framework
- **pytest-django**: Django integration
- **factory_boy**: Test data factories
- **freezegun**: Time mocking
- **pytest-mock**: Mocking

**Test Structure:**
```
tests/
├── conftest.py              # pytest configuration
├── fixtures/                # Shared fixtures
│   └── users.py
├── unit/                    # Unit tests
│   ├── models/
│   │   ├── test_userprofile.py
│   │   └── test_product.py
│   ├── views/
│   │   ├── test_landing.py
│   │   └── test_shop.py
│   └── forms/
│       └── test_forms.py
└── integration/             # Integration tests
    └── test_auth.py
```

**Model Tests:**
```python
# tests/unit/models/test_userprofile.py
import pytest
from django.contrib.auth.models import User
from landing.models import UserProfile

@pytest.mark.django_db
class TestUserProfile:
    """Test UserProfile model."""
    
    def test_profile_creation(self):
        """Test profile is created when user is created."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        assert hasattr(user, 'profile')
        assert user.profile.user == user
        assert user.profile.preferred_language == 'es'
        assert user.profile.preferred_theme == 'system'
        assert len(user.profile.ingest_token) == 32  # 16 hex chars * 2
    
    def test_token_regeneration(self):
        """Test token can be regenerated."""
        user = User.objects.create_user(username='testuser')
        old_token = user.profile.ingest_token
        
        user.profile.regenerate_token()
        user.profile.refresh_from_db()
        
        assert user.profile.ingest_token != old_token
        assert len(user.profile.ingest_token) == 32
    
    def test_profile_str_representation(self):
        """Test string representation."""
        user = User.objects.create_user(username='testuser')
        assert 'testuser' in str(user.profile)
```

**View Tests:**
```python
# tests/unit/views/test_landing.py
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestHomeView:
    """Test HomeView."""
    
    def test_get_context_data(self):
        """Test context data injection."""
        from landing.views import HomeView
        
        view = HomeView()
        view.request = Mock()
        context = view.get_context_data()
        
        assert 'nav_links' in context
        assert 'hero' in context
        assert context['brand'] == 'gator'
    
    def test_homepage_loads(self, client):
        """Test homepage loads successfully."""
        response = client.get(reverse('landing:home'))
        
        assert response.status_code == 200
        assert b'Volvamos a ser humanos' in response.content
    
    def test_i18n_english(self, client):
        """Test English translation."""
        response = client.get('/en/')
        
        assert response.status_code == 200
        assert b'Let\'s be human again' in response.content
```

**Form Tests:**
```python
# tests/unit/forms/test_forms.py
from django.test import TestCase
from landing.forms import CroodySignupForm

class TestCroodySignupForm:
    """Test custom signup form."""
    
    def test_valid_data(self):
        """Test form with valid data."""
        form_data = {
            'email': 'test@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
        }
        form = CroodySignupForm(data=form_data)
        
        assert form.is_valid()
    
    def test_password_mismatch(self):
        """Test password mismatch error."""
        form_data = {
            'email': 'test@example.com',
            'password': 'password1',
            'confirm_password': 'password2',
        }
        form = CroodySignupForm(data=form_data)
        
        assert not form.is_valid()
        assert 'password' in form.errors
    
    def test_email_unique(self):
        """Test email uniqueness validation."""
        User.objects.create_user(
            username='existinguser',
            email='test@example.com'
        )
        
        form_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        form = CroodySignupForm(data=form_data)
        
        assert not form.is_valid()
        assert 'email' in form.errors
```

**QuerySet Manager Tests:**
```python
# tests/unit/models/test_product.py
import pytest

@pytest.mark.django_db
class TestProductQuerySet:
    """Test ProductQuerySet custom methods."""
    
    def test_published(self, product_factory):
        """Test published() method."""
        published = product_factory(is_published=True)
        unpublished = product_factory(is_published=False)
        
        assert published in Product.objects.published()
        assert unpublished not in Product.objects.published()
    
    def test_search(self, product_factory):
        """Test search() method."""
        product = product_factory(name='Cofre Premium')
        
        # Search by name
        results = Product.objects.search('Cofre')
        assert product in results
        
        # Search by teaser
        product2 = product_factory(teaser='Set de temporada')
        results = Product.objects.search('temporada')
        assert product2 in results
    
    def test_search_empty_query(self, product_factory):
        """Test search with empty query returns all."""
        product_factory(name='Product 1')
        product_factory(name='Product 2')
        
        results = Product.objects.search('')
        assert results.count() == 2
```

**Fixtures:**
```python
# tests/conftest.py
import pytest
from django.contrib.auth.models import User
from shop.models import Product
import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = 'testpassword123'

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    name = factory.Sequence(lambda n: f'Product {n}')
    slug = factory.Sequence(lambda n: f'product-{n}')
    teaser = 'A great product'
    description = 'Product description'
    price = 29.99
    is_published = True

@pytest.fixture
def user(db):
    return UserFactory()

@pytest.fixture
def product(db):
    return ProductFactory()
```

**Test Configuration:**
```python
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --cov=landing shop telemetry
    --cov-report=html:htmlcov
    --cov-report=term-missing
    -ra
markers =
    django_db: database access
    slow: marks tests as slow
```

**Coverage Goals:**
- Models: 95%
- Views: 90%
- Forms: 95%
- Utils: 100%
- Overall: 90%+

**Nivel:** Completo
**Formato:** pytest patterns + Fixtures

---

##### integracion.md
**Contenido:**

**Integration Testing:**

**Django Test Case Classes:**
- TestCase: Transactional tests
- SimpleTestCase: No database
- LiveServerTestCase: Real server (Selenium/Playwright)

**Authentication Flow:**
```python
# tests/integration/test_auth_flow.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationFlowTest(TestCase):
    """Test complete authentication flow."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='securepass123'
        )
    
    def test_login_success(self):
        """Test successful login."""
        response = self.client.post(
            reverse('landing:login'),
            {
                'username': 'testuser',
                'password': 'securepass123'
            },
            follow=True
        )
        
        self.assertRedirects(response, reverse('landing:home'))
        self.assertIn('_auth_user_id', self.client.session)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(
            reverse('landing:login'),
            {
                'username': 'testuser',
                'password': 'wrongpassword'
            }
        )
        
        self.assertContains(response, 'Invalid credentials')
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_logout(self):
        """Test logout functionality."""
        # Login first
        self.client.login(
            username='testuser',
            password='securepass123'
        )
        
        # Logout
        response = self.client.post(reverse('landing:logout'))
        
        self.assertRedirects(response, reverse('landing:home'))
        self.assertNotIn('_auth_user_id', self.client.session)
```

**Profile Management:**
```python
# tests/integration/test_profile.py
class ProfileManagementTest(TestCase):
    """Test profile creation and updates."""
    
    def test_profile_auto_creation(self):
        """Test profile is auto-created on user signup."""
        response = self.client.post(
            reverse('landing:signup'),
            {
                'email': 'newuser@example.com',
                'password': 'password123',
                'confirm_password': 'password123'
            },
            follow=True
        )
        
        # Check user was created
        user = User.objects.get(email='newuser@example.com')
        
        # Check profile was auto-created
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.preferred_language, 'es')
    
    def test_profile_update(self):
        """Test profile update."""
        user = User.objects.create_user(username='user1')
        self.client.force_login(user)
        
        response = self.client.post(
            reverse('landing:profile'),
            {
                'display_name': 'Test User',
                'bio': 'Test bio',
                'preferred_language': 'en',
                'preferred_theme': 'dark'
            },
            follow=True
        )
        
        self.assertContains(response, 'Profile updated')
        
        # Check database
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.display_name, 'Test User')
        self.assertEqual(user.profile.preferred_language, 'en')
        self.assertEqual(user.profile.preferred_theme, 'dark')
    
    def test_token_regeneration(self):
        """Test token regeneration."""
        user = User.objects.create_user(username='user1')
        old_token = user.profile.ingest_token
        
        self.client.force_login(user)
        response = self.client.post(
            reverse('landing:token_reset'),
            follow=True
        )
        
        user.profile.refresh_from_db()
        self.assertNotEqual(user.profile.ingest_token, old_token)
        self.assertContains(response, 'Token regenerated')
```

**Shop Integration:**
```python
# tests/integration/test_shop.py
class ShopIntegrationTest(TestCase):
    """Test shop functionality."""
    
    def setUp(self):
        self.products = ProductFactory.create_batch(10)
    
    def test_product_listing(self):
        """Test product listing page."""
        response = self.client.get(reverse('shop:catalogue'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Productos')
        
        # Check pagination
        self.assertEqual(len(response.context['products']), 10)
    
    def test_product_search(self):
        """Test product search functionality."""
        product = ProductFactory(name='Special Product')
        
        response = self.client.get(
            reverse('shop:catalogue'),
            {'q': 'Special'}
        )
        
        self.assertContains(response, 'Special Product')
        self.assertIn(product, response.context['products'])
    
    def test_product_detail(self):
        """Test product detail page."""
        product = ProductFactory()
        
        response = self.client.get(
            reverse('shop:detail', args=[product.slug])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.name)
        self.assertContains(response, product.teaser)
        self.assertContains(response, f'${product.price}')
    
    def test_filter_by_type(self):
        """Test filtering products by type."""
        cofre = ProductFactory(name='Cofre Premium')
        set_product = ProductFactory(name='Set de Temporada')
        
        response = self.client.get(
            reverse('shop:catalogue'),
            {'type': 'cofre'}
        )
        
        self.assertIn(cofre, response.context['products'])
        self.assertNotIn(set_product, response.context['products'])
    
    def test_price_range_filter(self):
        """Test filtering by price range."""
        cheap = ProductFactory(price=10.00)
        expensive = ProductFactory(price=100.00)
        
        # Filter between 5 and 50
        response = self.client.get(
            reverse('shop:catalogue'),
            {'min_price': '5', 'max_price': '50'}
        )
        
        self.assertIn(cheap, response.context['products'])
        self.assertNotIn(expensive, response.context['products'])
```

**Telemetry Integration:**
```python
# tests/integration/test_telemetry.py
from telemetry.models import RobotPosition
import json

class TelemetryIntegrationTest(TestCase):
    """Test telemetry endpoints."""
    
    def test_position_ingestion(self):
        """Test ingesting robot position."""
        data = {
            'x': 10.5,
            'y': 20.3,
            'atmosphere': {
                'temperature': 23.5,
                'humidity': 65.0
            },
            'token': 'valid_token'
        }
        
        response = self.client.post(
            reverse('telemetry:ingest'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        
        # Check database
        position = RobotPosition.objects.latest('timestamp')
        self.assertEqual(position.x, 10.5)
        self.assertEqual(position.y, 20.3)
        self.assertEqual(position.atmosphere['temperature'], 23.5)
    
    def test_position_listing(self):
        """Test listing robot positions."""
        # Create some positions
        RobotPosition.objects.create(x=1, y=2, atmosphere={})
        RobotPosition.objects.create(x=3, y=4, atmosphere={})
        
        response = self.client.get(reverse('telemetry:positions'))
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
```

**i18n Integration:**
```python
# tests/integration/test_i18n.py
class I18nIntegrationTest(TestCase):
    """Test internationalization."""
    
    def test_language_switch(self):
        """Test switching languages via URL."""
        # Spanish (default)
        response = self.client.get('/')
        self.assertContains(response, 'Volvamos a ser humanos')
        
        # English
        response = self.client.get('/en/')
        self.assertContains(response, 'Let\'s be human again')
    
    def test_language_cookie(self):
        """Test language preference persistence."""
        self.client.cookies['django_language'] = 'en'
        
        response = self.client.get('/')
        self.assertContains(response, 'Let\'s be human again')
```

**Database Transactions:**
```python
from django.test import TransactionTestCase

class DatabaseTransactionTest(TransactionTestCase):
    """Test that requires transaction rollback."""
    
    def test_something_with_rollback(self):
        """Test with automatic rollback."""
        # This test will be rolled back after completion
        pass
```

**Best Practices:**
- Use TransactionTestCase for performance
- Mock external services
- Factory patterns for test data
- Clear test isolation
- Descriptive test names (test_should_do_something_when)

**Nivel:** Completo
**Formato:** Django TestCase + Examples

---

### 9. 👤 USUARIO

#### 9.1 Funcionalidades

##### landing.md
**Contenido:**

**Landing Page Features:**

**1. Hero Section:**
- Main headline: "Volvamos a ser humanos"
- Subheadline with value proposition
- Primary CTA: "Ir a la Tienda"
- Secondary CTA: "Ver Buddy"
- Tertiary CTA: "💎 Luks"
- Hero image with alt text
- Responsive typography (clamp for scaling)

**2. Metrics Section:**
- "1.2k+ rutinas ajustadas automáticamente cada semana"
- "92% personas mantienen su plan mensual con Buddy activo"
- "7 regiones operación sincronizada con soporte localizado"
- Animated counters
- Mobile-optimized layout

**3. Vector Cards (Ecosystem):**
- **Buddy** (Fitness & Conexión)
  - Description of AI trainer app
  - Keywords: Conecta, Entrena y Destaca
  - CTA to Buddy section
- **My Luks** (Economía Digital)
  - Description of digital economy
  - Keywords section
  - CTA to Luks section
- **Comida Real** (Lifestyle)
  - Description of real food
  - Lifestyle focus
  - Coming soon badge

**4. Buddy Pillars:**
- Connection features
- Training programs
- Social elements
- Highlight features with icons

**5. Global Search:**
- Keyboard shortcut integration
- Global search entries
- Quick access to sections
- Accessible via "?" key

**Navigation:**
- **Primary Navigation:**
  - Home
  - Buddy
  - Luks
  - Comida Real
  - Tienda
  - About

**Theme System:**
- Dark mode (default)
- Light mode
- Auto (system preference)
- Persistent via localStorage
- No FOUC (fixed)

**Language Selector:**
- 8 languages supported
- Flag icons
- Dropdown menu
- Smooth animations
- Keyboard navigation

**Responsive Design:**
- Mobile: Stacked layout
- Tablet: 2-column grid
- Desktop: 3-column grid
- Fluid typography

**Accessibility (WCAG 2.1 AA):**
- Semantic HTML5
- ARIA labels
- Keyboard navigation
- Focus management
- Reduced motion support
- High contrast

**Performance:**
- Lazy loading images
- CSS Grid/Flexbox
- GPU-accelerated animations
- Minimal JavaScript

**Nivel:** Básico-Intermedio
**Formato:** User guide

---

##### tienda.md
**Contenido:**

**Tienda Features:**

**1. Product Catalogue:**
- Grid layout (12 products per page)
- Product cards with:
  - Product image
  - Name
  - Teaser/short description
  - Price
  - Badge (new, sale, etc.)
  - Delivery estimate

**2. Search & Filters:**
- **Search Bar:**
  - Real-time search
  - Search by name and teaser
  - Clear search button
  - Results count

- **Filters:**
  - Type (cofre, set, accesorio)
  - Price range (min/max)
  - Sort order:
    - Default (sort_order)
    - Price: Low to High
    - Price: High to Low
    - Most Recent

- **Filter State:**
  - Active filters displayed
  - Clear all filters
  - Persist filters on pagination

**3. Product Detail Page:**
- Image gallery
- Full product name
- Detailed description
- Price and currency
- Delivery estimate
- Badge display
- Social sharing buttons

**4. Product Types:**

**Cofres (Loot Boxes):**
- Randomized items
- Mystery elements
- Collectible nature
- Premium feel

**Sets (Collections):**
- Themed collections
- Multiple items
- Seasonal content
- Bundle pricing

**Accesorios (Accessories):**
- Single items
- Specific use cases
- Quick purchase
- Available immediately

**5. User Flow:**
1. Browse catalogue
2. Use filters to narrow down
3. Click product card
4. View product detail
5. Add to cart (future)
6. Checkout (future)

**6. UI Components:**

**Product Card:**
```html
<article class="product-card">
  <div class="product-image">
    <img src="product.jpg" alt="Product name">
    <span class="badge">New</span>
  </div>
  <div class="product-info">
    <h3 class="product-name">Product Name</h3>
    <p class="product-teaser">Short description</p>
    <div class="product-meta">
      <span class="price">$29.99</span>
      <span class="delivery">Entrega 3 días</span>
    </div>
  </div>
</article>
```

**Filter Panel:**
```html
<aside class="filters">
  <div class="filter-group">
    <label>Search</label>
    <input type="search" name="q">
  </div>
  
  <div class="filter-group">
    <label>Type</label>
    <select name="type">
      <option value="">All</option>
      <option value="cofre">Cofre</option>
      <option value="set">Set</option>
      <option value="accesorio">Accesorio</option>
    </select>
  </div>
  
  <div class="filter-group">
    <label>Price Range</label>
    <input type="number" name="min_price" placeholder="Min">
    <input type="number" name="max_price" placeholder="Max">
  </div>
  
  <div class="filter-group">
    <label>Sort By</label>
    <select name="order">
      <option value="">Default</option>
      <option value="price_asc">Price: Low to High</option>
      <option value="price_desc">Price: High to Low</option>
      <option value="recent">Most Recent</option>
    </select>
  </div>
</aside>
```

**7. Mobile Experience:**
- Filter drawer
- Sticky search bar
- Infinite scroll option
- Touch-friendly cards

**8. SEO:**
- Product slugs
- Meta descriptions
- Structured data (schema.org)
- Sitemap integration

**Nivel:** Intermedio
**Formato:** User guide + HTML samples

---

### 10. 🔧 OPERATIVO

#### 10.1 Monitoreo

##### monitoreo.md
**Contenido:**

**Observability Stack:**

**1. Metrics Collection:**
- **Prometheus**: Metrics scraping
- **Grafana**: Visualization
- **Custom metrics**: Business logic

**Application Metrics:**
```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
REQUEST_COUNT = Counter(
    'croody_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'croody_request_duration_seconds',
    'Request latency',
    ['method', 'endpoint']
)

# Business metrics
ACTIVE_USERS = Gauge(
    'croody_active_users',
    'Number of active users'
)

PRODUCTS_SOLD = Counter(
    'croody_products_sold_total',
    'Total products sold',
    ['product_type']
)
```

**Dashboard (Grafana):**
- **System Dashboard:**
  - CPU usage
  - Memory usage
  - Disk I/O
  - Network traffic

- **Application Dashboard:**
  - Request rate
  - Error rate
  - Response time (P50, P95, P99)
  - Active sessions

- **Business Dashboard:**
  - User registrations
  - Product sales
  - Revenue tracking
  - Conversion funnels

**2. Logging:**
```python
# logging.py
import logging

logger = logging.getLogger('croody')

# Request logging
logger.info(
    'Request processed',
    extra={
        'request_id': request.id,
        'user_id': request.user.id if request.user.is_authenticated else None,
        'endpoint': request.path,
        'method': request.method,
        'status_code': response.status_code,
        'response_time': response_time
    }
)

# Error logging
logger.error(
    'Exception occurred',
    exc_info=True,
    extra={
        'request_id': request.id,
        'user_id': request.user.id,
        'path': request.path
    }
)
```

**Log Aggregation:**
- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Fluentd**: Log collection
- **Centralized logging**: All services

**3. Alerting:**
```yaml
# alerting_rules.yml
groups:
  - name: croody_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(croody_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
          
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(croody_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High response time
```

**Alert Channels:**
- Email
- Slack
- PagerDuty (critical)
- Microsoft Teams

**4. Tracing:**
- **Jaeger**: Distributed tracing
- **OpenTelemetry**: Instrumentation
- Trace correlation across services

**5. Health Checks:**
```python
# health.py
def health_check(request):
    """Health check endpoint."""
    checks = {
        'database': check_database(),
        'cache': check_cache(),
        'external_api': check_external_api(),
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return JsonResponse(
        {'status': 'healthy' if all_healthy else 'unhealthy', 'checks': checks},
        status=status_code
    )
```

**6. Uptime Monitoring:**
- **Pingdom**: External monitoring
- **StatusCake**: Uptime checks
- **Custom monitors**: Business logic

**7. Performance Monitoring:**
- **New Relic**: APM
- **Datadog**: Application performance
- **Custom metrics**: Business KPIs

**Nivel:** Avanzado
**Formato:** Config files + Dashboards

---

#### 10.2 Troubleshooting

##### problemas-comunes.md
**Contenido:**

**Common Issues & Solutions:**

**1. Login Issues:**

**Problem:** `TemplateSyntaxError` in login form
```
'as_widget' received an unexpected keyword argument 'attrs'
```

**Solution:**
- Use custom form with widgets defined in `__init__`
- Do NOT pass `attrs` to `as_widget()` in template
- Create `CroodyLoginForm` with custom widgets

**Code Fix:**
```python
# forms.py
class CroodyLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Password'
        })
```

---

**2. FOUC (Flash of Unstyled Content):**

**Problem:** Page flashes in dark mode before switching to light

**Solution:** Initialize theme immediately in JavaScript
```javascript
// theme.js - FIXED (lines 11-16)
(function initTheme() {
  const saved = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = saved || (prefersDark ? 'dark' : 'light');
  
  document.documentElement.setAttribute('data-theme', theme);
})();
```

**3. Translation Not Working:**

**Problem:** Language selector doesn't change content

**Diagnosis:**
1. Check locale files exist: `/locale/{lang}/LC_MESSAGES/django.po`
2. Verify `.po` files are compiled: `.mo` files exist
3. Check URL prefixes: `/en/`, `/fr/`, etc.
4. Verify `LocaleMiddleware` is in settings
5. Check `i18n_patterns` in URLs

**Solution:**
```python
# urls.py
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('', include('landing.urls')),
    path('tienda/', include('shop.urls')),
    prefix_default_language=False,
)
```

**Recompile translations:**
```bash
python3 compile_translations.py
```

---

**4. Docker Build Fails:**

**Problem:** `python:3.11-slim` not found

**Solution:**
```dockerfile
# Use specific tag
FROM python:3.11-slim@sha256:...

# Or use minor version
FROM python:3.11.9-slim
```

---

**5. Database Connection Issues:**

**Problem:** `OperationalError: could not connect to server`

**Diagnosis:**
```bash
# Check PostgreSQL is running
docker-compose ps

# Check logs
docker-compose logs croody

# Test database connection
python manage.py dbshell
```

**Solution:**
```yaml
# docker-compose.yml - Add healthcheck
croody:
  depends_on:
    db:
      condition: service_healthy
  
  db:
    image: postgres:13
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

---

**6. Static Files Not Loading:**

**Problem:** 404 on CSS/JS files

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_URL in settings
STATIC_URL = '/static/'

# For development, ensure DEBUG=True
# For production, use WhiteNoise or CDN
```

---

**7. High Memory Usage:**

**Problem:** Application runs out of memory

**Diagnosis:**
```bash
# Check memory usage
docker stats

# Check for memory leaks
docker-compose exec croody ps aux

# Django memory usage
python manage.py shell
from django.db import connection
from django.db.utils import OperationalError
print(connection.queries)
```

**Solution:**
- Add memory limits to Docker Compose
- Use connection pooling
- Optimize queries (select_related, prefetch_related)
- Enable Django debug toolbar in development

---

**8. Slow Performance:**

**Problem:** Page loads > 3 seconds

**Diagnosis:**
```python
# Add to settings.py (development only)
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG and request.META.get('REMOTE_ADDR') in ['127.0.0.1'],
}

# Install django-debug-toolbar
pip install django-debug-toolbar
```

**Solution:**
1. Add database indexes:
```python
class Product(models.Model):
    # ...
    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['price']),
            models.Index(fields=['-created_at']),
        ]
```

2. Optimize queries:
```python
# Bad (N+1 problem)
products = Product.objects.all()
for product in products:
    print(product.user.username)  # N+1 queries

# Good
products = Product.objects.select_related('user').all()
for product in products:
    print(product.user.username)  # Single query
```

3. Add caching:
```python
# views.py
from django.core.cache import cache

def home_view(request):
    cache_key = f'home_view_{request.LANGUAGE_CODE}'
    data = cache.get(cache_key)
    
    if not data:
        # Fetch data
        data = get_home_data()
        cache.set(cache_key, data, 300)  # 5 minutes
    
    return render(request, 'home.html', data)
```

---

**9. CORS Errors:**

**Problem:** `Access to fetch at 'http://api.com' from origin 'http://localhost:8000' has been blocked by CORS policy`

**Solution:**
```python
# settings.py - Install django-cors-headers
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://croody.app",
]

# Allow credentials
CORS_ALLOW_CREDENTIALS = True
```

---

**10. CSRF Token Errors:**

**Problem:** `Forbidden (CSRF token missing or incorrect)`

**Solution:**
```html
<!-- Template - Ensure CSRF token -->
<form method="post">
  {% csrf_token %}
  ...
</form>

<!-- AJAX requests -->
fetch('/api/endpoint/', {
  method: 'POST',
  headers: {
    'X-CSRFToken': getCookie('csrftoken')
  },
  body: JSON.stringify(data)
})
```

**Nivel:** Completo
**Formato:** Problem/Solution matrix

---

### 11. 📚 APÉNDICES

#### 11.1 Glosario

##### glosario.md
**Contenido:**

**Términos Técnicos:**

**ADR (Architecture Decision Record):**
Documento que registra una decisión arquitectónica importante y su contexto.

**CBV (Class-Based View):**
Vista basada en clases en Django, alternativa a las vistas basadas en funciones (FBV).

**CI/CD (Continuous Integration/Continuous Deployment):**
Práctica de desarrollo donde los cambios se integran y despliegan automáticamente.

**CSP (Content Security Policy):**
Política de seguridad que especifica qué fuentes de contenido está permitido cargar.

**CSRF (Cross-Site Request Forgery):**
Vulnerabilidad que permite a un atacante ejecutar acciones no autorizadas en una aplicación.

**DRF (Django REST Framework):**
Extensión de Django para crear APIs RESTful.

**FOUC (Flash of Unstyled Content):**
Parpadeo visual que ocurre cuando una página se carga con estilos por defecto antes de aplicar los estilos reales.

**HSTS (HTTP Strict Transport Security):**
Política de seguridad que fuerza a los navegadores a usar HTTPS.

**i18n (Internationalization):**
Proceso de hacer que una aplicación sea compatible con múltiples idiomas.

**l10n (Localization):**
Proceso de traducir y adaptar una aplicación a un idioma o región específica.

**JWT (JSON Web Token):**
Estándar para transmitir información segura entre partes como un objeto JSON.

**ORM (Object-Relational Mapping):**
Técnica que permite interactuar con bases de datos usando objetos Python.

**RBAC (Role-Based Access Control):**
Control de acceso basado en roles de usuario.

**RPO (Recovery Point Objective):**
Máximo período de tiempo en el que se pueden perder datos.

**RTO (Recovery Time Objective):**
Tiempo máximo para restaurar un servicio después de una interrupción.

**SLA (Service Level Agreement):**
Compromiso entre un proveedor de servicio y un cliente.

**SSRF (Server-Side Request Forgery):**
Vulnerabilidad que permite a un atacante hacer que el servidor realice solicitudes a ubicaciones no autorizadas.

**WCAG (Web Content Accessibility Guidelines):**
Pautas para hacer el contenido web más accesible para personas con discapacidades.

**Términos de Negocio:**

**Buddy:**
Aplicación de fitness y conexión social con IA.

**Luks:**
Ecosistema de economía digital de Croody.

**Comida Real:**
Marca de lifestyle enfocada en alimentación real.

**Croody:**
Ecosistema tecnológico que conecta personas a través de tecnología avanzada.

**Vector Card:**
Componente de UI que muestra información del ecosistema (Buddy, Luks, Comida Real).

**Golden Ratio (Número Áureo):**
Constante matemática φ ≈ 1.618, base del design system.

---

#### 11.2 Comandos Útiles

##### comandos-utiles.md
**Contenido:**

**Django Management Commands:**

**Development:**
```bash
# Start development server
python manage.py runserver

# Start HTTPS server (development)
python manage.py runhttps

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Access database shell
python manage.py dbshell

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Test coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Check for issues
python manage.py check

# View SQL for migration
python manage.py sqlmigrate shop 0001

# Clear cache
python manage.py clear_cache
```

**i18n Commands:**
```bash
# Extract messages
python manage.py makemessages -l en

# Compile messages
python manage.py compilemessages

# Custom compilation (no gettext)
python3 compile_translations.py

# Update translation files
python manage.py makemessages --all
```

**Docker Commands:**
```bash
# Build image
docker build -t croody:latest ./proyecto_integrado/Croody

# Run container
docker run -p 8000:8000 croody:latest

# Docker Compose
docker-compose up -d              # Start all services
docker-compose down               # Stop all services
docker-compose ps                 # List running containers
docker-compose logs -f croody     # Follow logs
docker-compose exec croody bash   # Shell into container
docker-compose restart croody     # Restart service
docker-compose up -d --build      # Rebuild and start

# View logs
docker-compose logs --tail=100 -f

# Scale service
docker-compose up -d --scale croody=3
```

**Git Commands:**
```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Stage and commit
git add .
git commit -m "feat: add new feature"

# Push branch
git push origin feature/new-feature

# Update main
git checkout main
git pull origin main
git checkout feature/new-feature
git rebase main

# Merge branch
git checkout main
git merge feature/new-feature
git push origin main

# Delete branch
git branch -d feature/new-feature
git push origin --delete feature/new-feature

# View commit history
git log --oneline --graph --all

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Stash changes
git stash
git stash pop
```

**PostgreSQL Commands:**
```bash
# Connect to database
psql -U postgres -d croody

# List databases
\l

# List tables
\dt

# Describe table
\d+ table_name

# Quit
\q
```

**Testing Commands:**
```bash
# Run specific test
pytest tests/unit/models/test_product.py::TestProductQuerySet::test_search

# Run tests with coverage
pytest --cov=./ --cov-report=html

# Run tests in parallel
pytest -n auto

# Run specific marker
pytest -m django_db

# Run tests without db
pytest -m "not django_db"

# Generate JUnit report
pytest --junitxml=report.xml
```

**Playwright (E2E) Commands:**
```bash
# Install browsers
playwright install

# Run tests
playwright test

# Run with UI
playwright test --ui

# Debug tests
playwright test --debug

# Generate test
playwright codegen http://localhost:8000
```

**System Commands:**
```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check CPU usage
top

# Check running services
systemctl status

# View system logs
journalctl -u croody

# Check port usage
netstat -tulpn | grep 8000

# Kill process on port
fuser -k 8000/tcp

# Check environment variables
env | grep DJANGO
```

**Monitoring:**
```bash
# View application logs
tail -f /var/log/croody/app.log

# View Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Check Prometheus metrics
curl http://localhost:9090/metrics

# Check Grafana
open http://localhost:3000

# Health check
curl http://localhost:8000/healthz/
```

**Security:**
```bash
# Scan dependencies
safety check

# Run security linter (Python)
bandit -r ./proyecto_integrado/Croody

# Update dependencies
pip list --outdated
pip install --upgrade package_name

# Generate requirements.txt
pip freeze > requirements.txt
```

**Utilities:**
```bash
# Format code (Black)
black . --line-length=88

# Sort imports (isort)
isort .

# Lint code (flake8)
flake8 .

# Type checking (mypy)
mypy .
```

**Nivel:** Intermedio
**Formato:** Command reference

---

## 🎯 CRONOGRAMA DE IMPLEMENTACIÓN

### Fase 1: Documentación Fundamental (2 semanas)
- **Semana 1:**
  - Documentación técnica de modelos y vistas
  - Documentación de APIs
  - Documentación del design system (tokens)

- **Semana 2:**
  - Documentación de arquitectura
  - Documentación de infraestructura Terraform
  - Documentación de Docker

### Fase 2: Documentación de Procesos (2 semanas)
- **Semana 3:**
  - Documentación de CI/CD
  - Documentación de seguridad
  - Documentación de i18n

- **Semana 4:**
  - Documentación de desarrollo (patrones, testing)
  - Documentación operativa (monitoreo, troubleshooting)
  - Documentación de usuario

### Fase 3: Mejoras y Completitud (1 semana)
- **Semana 5:**
  - Revisión y validación
  - Completar gaps identificados
  - Generar diagramas adicionales
  - Crear índice maestro

---

## 📊 MÉTRICAS DE ÉXITO

### Cobertura de Documentación
- **Modelos**: 100% documentados
- **Vistas**: 100% documentadas
- **APIs**: 100% documentadas
- **Componentes UI**: 100% documentados
- **Workflows**: 100% documentados
- **Infraestructura**: 100% documentada

### Calidad
- Ejemplos de código en 100% de documentos
- Diagramas en documentos arquitectónicos
- Referencias cruzadas entre documentos
- Validación de sintaxis en código ejemplo

### Usabilidad
- README en cada directorio
- Índice navegable
- Búsqueda integrada (si se usa Sphinx)
- Versionado con el código

---

## 🛠️ HERRAMIENTAS RECOMENDADAS

### Generación de Documentación
- **Sphinx**: Para documentación técnica
- **MkDocs**: Para documentación de usuario
- **Docusaurus**: Para documentación moderna

### Diagramas
- **Mermaid**: Diagramas en código
- **Draw.io**: Diagramas complejos
- **Lucidchart**: Diagramas colaborativos

### Validación
- **Vale**: Linting de documentación
- **Markdownlint**: Validación de Markdown
- **Broken Link Checker**: Verificar enlaces

---

## 💡 RECOMENDACIONES FINALES

### Principios
1. **Documentation as Code**: Versionar con el código
2. **Keep It Simple**: Mantener simple, actualizar frecuentemente
3. **Examples First**: Siempre con ejemplos de código
4. **Visuals Matter**: Diagramas valen más que 1000 palabras
5. **User-Centric**: Orientada a diferentes audiencias

### Mantenimiento
- Revisar documentación en cada release
- Asignar dueños a cada documento
- Automatizar validación donde sea posible
- Celebrar contribuciones a la documentación

### Próximos Pasos
1. Crear estructura de directorios
2. Implementar herramientas de generación
3. Asignar responsables por sección
4. Establecer cronograma de implementación
5. Configurar pipeline de validación

---

**FIN DEL PLAN DE DOCUMENTACIÓN COMPLETO**

Este plan establece una hoja de ruta completa para documentar TODOS los aspectos del proyecto Croody con el máximo nivel de detalle, evitando duplicación con la documentación existente y complementándola significativamente.
