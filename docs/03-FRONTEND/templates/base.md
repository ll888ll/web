# Template Base - Documentación Completa

## Resumen
El template base de Croody implementa una estructura HTML5 semántica, accesible y optimizada que sirve como foundation para todas las páginas. Incluye meta tags SEO, Open Graph, soporte multi-idioma, navegación responsive y componentes interactivos.

## Ubicación
`/proyecto_integrado/Croody/templates/base.html` (308 líneas)

## Estructura General

### DOCTYPE y HTML Tag
```html
{% load static %}
{% load i18n %}
<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE }}" data-theme="auto" data-brand="{{ brand|default:'gator' }}">
```

**Atributos HTML**:
- `lang="{{ LANGUAGE_CODE }}"`: Idioma actual (es, en, fr, pt, ar, zh-hans, ja, hi)
- `data-theme="auto"`: Tema inicial (auto/dark/light, sobrescrito por JS)
- `data-brand="{{ brand }}"`: Marca activa (gator, crimson, gold)

## Head Section

### Meta Tags Básicos
```html
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{% block meta_description %}...{% endblock %}" />
  <meta name="keywords" content="buddy, croody, fitness ai, entrenador artificial, luks, entrenamiento personalizado, fitness app" />
  <meta name="author" content="Croody" />
  <meta name="robots" content="index, follow" />
```

**Propsósito**:
- Charset UTF-8: Soporte internacional
- Viewport: Responsive design
- Description: SEO y social sharing
- Keywords: SEO (menos relevante pero mantenido)
- Robots: Indexación permitido

### Open Graph (Facebook, LinkedIn)
```html
<meta property="og:title" content="{% block og_title %}{% trans "Croody · Diseño con propósito" %}{% endblock %}" />
<meta property="og:description" content="{% block og_description %}...{% endblock %}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{{ request.build_absolute_uri }}" />
<meta property="og:image" content="{% static 'img/completo.png' %}" />
```

**Uso**:
- Cuando se comparte en Facebook/LinkedIn
- Preview con título, descripción e imagen
- URL canónica asegurada con `request.build_absolute_uri`

### Twitter Cards
```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{% block twitter_title %}Croody - Buddy AI Trainer{% endblock %}" />
<meta name="twitter:description" content="{% block twitter_description %}Entrena, progresa y destaca con Buddy AI.{% endblock %}" />
```

**Tipos de Twitter Card**:
- `summary_large_image`: Imagen grande + título + descripción
- `summary`: Imagen pequeña
- `app`: Apps móviles
- `player`: Videos/audio

### Theme Color (PWA)
```html
<meta
  name="theme-color"
  media="(prefers-color-scheme: dark)"
  content="#050807"
/>
<meta
  name="theme-color"
  media="(prefers-color-scheme: light)"
  content="#F0FBF5"
/>
```

**Uso**:
- Color de la barra de direcciones del navegador
- Color del tema PWA
- Diferente para modo claro y oscuro
- Actualizado dinámicamente por JavaScript

### Canonical URL
```html
<link rel="canonical" href="{{ request.build_absolute_uri }}" />
```

**Propsósito**:
- Evita contenido duplicado en SEO
- Especifica URL preferida para crawlers
- Consistencia en sharing social

### Favicon
```html
<link
  rel="icon"
  type="image/png"
  href="{% static 'img/favicon.png' %}?v=3"
/>
```

**Variantes adicionales recomendadas**:
```html
<!-- Apple Touch Icon -->
<link rel="apple-touch-icon" href="{% static 'img/apple-touch-icon.png' %}">

<!-- Favicon variants -->
<link rel="icon" type="image/png" sizes="16x16" href="{% static 'img/favicon-16x16.png' %}">
<link rel="icon" type="image/png" sizes="32x32" href="{% static 'img/favicon-32x32.png' %}">
<link rel="manifest" href="{% static 'img/site.webmanifest' %}">
```

### Fonts Preload
```html
{% block head_fonts %}
<link
  rel="preload"
  href="{% static 'fonts/Baloo2-Latin.woff2' %}"
  as="font"
  type="font/woff2"
  crossorigin
/>
<link
  rel="preload"
  href="{% static 'fonts/JosefinSans-Variable.woff2' %}"
  as="font"
  type="font/woff2"
  crossorigin
/>
<link rel="stylesheet" href="{% static 'css/fonts.css' }}" />
{% endblock %}
```

**Optimización**:
- `preload`: Carga fonts antes de necesitar
- `crossorigin`: Para fonts de CDN
- `as="font"`: Hint al browser sobre tipo de recurso
- `fonts.css`: Fallback sin preload

### CSS Loading Order
```html
<link rel="stylesheet" href="{% static 'css/tokens.css' %}" />
<link rel="stylesheet" href="{% static 'css/base.css' %}" />
<link rel="stylesheet" href="{% static 'css/components.css' %}" />
<link rel="stylesheet" href="{% static 'css/animations.css' %}" />
{% block head_extra %}{% endblock %}
```

**Orden importante**:
1. **tokens.css**: Variables CSS (debe cargar primero)
2. **base.css**: Estilos base y resets
3. **components.css**: Componentes UI
4. **animations.css**: Animaciones (puede cargar async)
5. **head_extra**: Bloque para CSS adicional

## Body Structure

### Skip Link (Accesibilidad)
```html
<a class="skip-link" href="#main">{% trans "Saltar al contenido principal" %}</a>
```

**CSS**:
```css
.skip-link {
  position: fixed;
  top: -100px;
  left: 21px;
  padding: 13px 21px;
  border-radius: 18px;
  background: var(--surface-2);
  color: var(--fg);
  box-shadow: var(--shadow);
  z-index: var(--z-10000);
  transition: top 144ms cubic-bezier(.2,.8,.2,1);
}

.skip-link:focus {
  top: 21px;
}
```

**Uso**:
- Permite skip navegación para usuarios de screen reader
- `focus-visible` cuando recibe focus
- `z-index` muy alto (10000)

### Header Structure

#### Header Element
```html
<header class="site-header" role="banner">
```

**ARIA Role**:
- `role="banner"`: Región de encabezado
- Solo uno por página
- Global, no dentro de `<main>`

#### Container
```html
<div class="container inner">
```

**CSS**:
```css
.container {
  width: min(100%, 1340px);
  margin-inline: auto;
  padding-inline: clamp(16px, 4vw, var(--container-pad));
}

.site-header .inner {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding-inline: clamp(16px, 4vw, var(--container-pad));
}
```

#### Brand Section
```html
<div class="brand">
  <a
    class="brand__home"
    href="{% url 'landing:home' %}#hero"
    aria-label="Volver al inicio de Croody"
  >
    <img
      src="{% static 'img/logo-main.png' %}?v=3"
      alt="Croody"
    />
  </a>
</div>
```

**Características**:
- Logo clickeable lleva a home
- `aria-label` describe acción
- `v=3`: Cache busting para updates

**CSS**:
```css
.brand__home {
  display: inline-flex;
  align-items: center;
  padding: 0;
  border: none;
  background: none;
  height: auto;
  transition: transform 200ms ease;
}

.brand__home:hover {
  transform: translateY(-2px);
}

.brand__home:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 3px;
}

.brand__home img {
  height: 40px;
  width: auto;
  filter: drop-shadow(0 12px 18px color-mix(in oklab, var(--brand-base), transparent 78%));
}
```

#### Mobile Nav Toggle
```html
<button
  class="nav-toggle"
  type="button"
  aria-label="{% trans 'Abrir menú' %}"
  aria-expanded="false"
>
  <span></span>
</button>
```

**ARIA**:
- `aria-label`: Descripción de acción
- `aria-expanded`: Estado (false/true)
- `aria-controls`: ID del drawer (opcional)

**CSS**:
```css
.nav-toggle {
  display: none; /* Visible only on mobile */
  width: 46px;
  height: 46px;
  border-radius: 50%;
  border: 1px solid color-mix(in oklab, var(--brand-base), transparent 65%);
  background: color-mix(in oklab, var(--brand-base) 10%, transparent 90%);
  position: relative;
  box-shadow: var(--shadow-sm);
}

.nav-toggle span,
.nav-toggle::before,
.nav-toggle::after {
  content: "";
  position: absolute;
  width: 20px;
  height: 2px;
  background: var(--fg);
  left: 50%;
  translate: -50% 0;
  transition: transform 233ms cubic-bezier(.2,.8,.2,1);
}

.nav-toggle span {
  top: 50%;
  translate: -50% -50%;
}

.nav-toggle::before {
  top: 15px;
}

.nav-toggle::after {
  bottom: 15px;
}

/* Animation states */
.nav-toggle[aria-expanded="true"] span {
  opacity: 0;
}

.nav-toggle[aria-expanded="true"]::before {
  transform: translate(-50%, 6px) rotate(45deg);
}

.nav-toggle[aria-expanded="true"]::after {
  transform: translate(-50%, -6px) rotate(-45deg);
}
```

#### Primary Navigation
```html
<ul class="nav__primary" role="menubar">
  {% for link in nav_links %}
  <li role="none">
    <a
      role="menuitem"
      class="nav-link{% if request.path == link.url %} is-active{% endif %}"
      {% if request.path == link.url %}aria-current="page"{% endif %}
      href="{{ link.url }}{% if link.fragment %}#{{ link.fragment }}{% endif %}"
      >{{ link.label }}</a
    >
  </li>
  {% endfor %}
</ul>
```

**ARIA**:
- `role="menubar"`: Contenedor principal de navegación
- `role="menuitem"`: Cada enlace
- `role="none"`: Li no es menú item (enlace lo es)
- `aria-current="page"`: Página actual

**CSS**:
```css
.nav__primary {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.nav__primary a {
  position: relative;
  padding-block: 8px;
  font-weight: 600;
  color: var(--fg-muted);
  text-transform: uppercase;
  letter-spacing: .08em;
  font-size: var(--text-sm);
}

.nav__primary a::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: -8px;
  height: 3px;
  border-radius: 999px;
  background: linear-gradient(120deg, var(--brand-base), var(--brand-strong));
  transform-origin: left;
  transform: scaleX(0);
  transition: transform 233ms cubic-bezier(.2,.8,.2,1);
}

.nav__primary a:focus-visible::after,
.nav__primary a:hover::after {
  transform: scaleX(1);
}

.nav__primary .is-active {
  color: var(--fg);
}

.nav__primary .is-active::after {
  transform: scaleX(1);
}
```

#### Header Actions
```html
<div class="header__actions">
  <!-- Search -->
  <div class="search" role="search">
    <label class="visually-hidden" for="site-search">{% trans "Buscar en Croody" %}</label>
    <input
      data-search-input
      id="site-search"
      class="search__input anim-focus-glow"
      type="search"
      placeholder="{% trans 'Buscar (pulsa /)' %}"
      aria-controls="search-list"
      aria-expanded="false"
    />
    <span aria-hidden="true" class="search__icon">⌕</span>
  </div>

  <!-- Language Selector -->
  <div class="language-selector">
    <button
      class="language-selector__trigger"
      type="button"
      aria-label="{% trans 'Seleccionar idioma' %}"
      aria-haspopup="true"
      aria-expanded="false"
    >
      <span class="language-selector__icon">🌐</span>
      <span class="language-selector__current">{{ LANGUAGE_CODE|upper }}</span>
    </button>
    <div class="language-selector__dropdown" hidden>
      <!-- Language options (8 languages) -->
    </div>
  </div>

  <!-- Theme Toggle -->
  <label class="theme-toggle" aria-label="{% trans 'Cambiar tema' %}">
    <input type="checkbox" class="theme-toggle__checkbox" />
  </label>

  <!-- Auth Buttons -->
  {% if request.user.is_authenticated %}
  <a class="btn btn--primary" href="{% url 'shop:catalogue' %}">{% trans "Empezar" %}</a>
  <a class="btn btn--ghost" href="{% url 'landing:profile' %}">{% trans "Perfil" %}</a>
  <a class="btn btn--ghost" href="{% url 'landing:logout' %}">{% trans "Salir" %}</a>
  {% else %}
  <a class="btn btn--ghost" href="{% url 'landing:login' %}?next={% url 'shop:catalogue' %}">{% trans "Acceder" %}</a>
  {% endif %}
</div>
```

#### Language Selector Options
```html
<div class="language-selector__dropdown" hidden>
  <div class="language-selector__list">
    <a href="/es/{{ request.get_full_path|slice:'3:' }}" class="language-selector__option {% if LANGUAGE_CODE == 'es' %}active{% endif %}">
      <span class="language-selector__flag">🇪🇸</span>
      <span>Español</span>
    </a>
    <a href="/en/{{ request.get_full_path|slice:'3:' }}" class="language-selector__option {% if LANGUAGE_CODE == 'en' %}active{% endif %}">
      <span class="language-selector__flag">🇬🇧</span>
      <span>English</span>
    </a>
    <!-- Más idiomas... -->
  </div>
</div>
```

**Path Slicing**:
```django
request.get_full_path|slice:'3:'
```
- `/es/shop/products/` → `/shop/products/`
- Quita prefijo de idioma del path
- Mantiene query string y fragment

**Idiomas Soportados** (8 total):
1. **es** - Español (🇪🇸)
2. **en** - English (🇬🇧)
3. **fr** - Français (🇫🇷)
4. **pt** - Português (🇵🇹)
5. **ar** - العربية (🇸🇦) - RTL
6. **zh-hans** - 简体中文 (🇨🇳)
7. **ja** - 日本語 (🇯🇵)
8. **hi** - हिन्दी (🇮🇳)

### Mobile Navigation Drawer

```html
<div class="nav-drawer" id="mobile-drawer" aria-hidden="true">
  <div class="search" role="search">
    <label class="visually-hidden" for="site-search-mobile">{% trans "Buscar en Croody" %}</label>
    <input
      data-search-input
      id="site-search-mobile"
      class="search__input"
      type="search"
      placeholder="{% trans 'Buscar (pulsa /)' %}"
      aria-controls="search-list"
      aria-expanded="false"
    />
    <span aria-hidden="true" class="search__icon">⌕</span>
  </div>

  <ul class="nav-drawer__nav">
    {% for link in nav_links %}
    <li>
      <a
        class="nav-link{% if request.path == link.url %} is-active{% endif %}"
        {% if request.path == link.url %}aria-current="page"{% endif %}
        href="{{ link.url }}{% if link.fragment %}#{{ link.fragment }}{% endif %}"
        >{{ link.label }}</a
      >
    </li>
    {% endfor %}

    {% if request.user.is_authenticated %}
    <li><a href="{% url 'shop:catalogue' %}">{% trans "Empezar" %}</a></li>
    <li><a href="{% url 'landing:profile' %}">{% trans "Perfil" %}</a></li>
    <li><a href="{% url 'landing:logout' %}">{% trans "Cerrar sesión" %}</a></li>
    {% else %}
    <li><a href="{% url 'landing:login' %}?next={% url 'shop:catalogue' %}">{% trans "Acceder" %}</a></li>
    {% endif %}

    <li><a href="{% url 'landing:home' %}#search">{% trans "Búsqueda" %}</a></li>
    <li><a href="{% url 'landing:home' %}#cta-final">{% trans "Contactar" %}</a></li>
  </ul>
</div>
```

**CSS**:
```css
.nav-drawer {
  position: fixed;
  inset: 0;
  background: color-mix(in oklab, var(--bg) 96%, transparent 4%);
  backdrop-filter: blur(14px);
  transform: translateY(-100%);
  transition: transform 333ms cubic-bezier(.2,.8,.2,1);
  padding: 88px clamp(18px, 5vw, var(--container-pad)) var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  z-index: var(--z-1000);
}

.nav-drawer.is-open {
  transform: translateY(0);
}

@media (max-width: 767.98px) {
  .nav-drawer__nav {
    grid-template-columns: repeat(1, minmax(0, 1fr));
    gap: var(--space-2);
  }
}
```

### Flash Messages

```html
{% if messages %}
<div class="flash-stack" role="status">
  {% for message in messages %}
  <div class="flash flash--{{ message.tags|default:'info' }}">{{ message }}</div>
  {% endfor %}
</div>
{% endif %}
```

**Tipos de message**:
- `success`: Éxito (verde)
- `error`: Error (rojo)
- `warning`: Advertencia (amarillo)
- `info`: Información (azul)

**CSS**:
```css
.flash-stack {
  position: sticky;
  top: var(--space-2);
  z-index: var(--z-1000);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin: var(--space-2);
}

.flash {
  padding: var(--space-2);
  border-radius: 16px;
  border: 1px solid color-mix(in oklab, var(--brand-base), transparent 80%);
  background: color-mix(in oklab, var(--brand-base), transparent 90%);
  color: var(--fg);
}

.flash--success {
  background: color-mix(in oklab, var(--brand-base), transparent 80%);
}

.flash--error {
  background: color-mix(in oklab, var(--error-500, #FF5A78), transparent 70%);
}
```

### Global Search Results (Optional)

```html
{% if show_global_shortcuts %}
<section id="search" class="search-results" aria-label="{% trans 'Accesos rápidos' %}">
  <div class="container">
    <ul
      id="search-list"
      class="search-results__grid"
      role="listbox"
      aria-label="{% trans 'Resultados sugeridos' %}"
    >
      {% for item in search_results %}
      <li role="option">
        <a href="{{ item.url }}{% if item.fragment %}#{{ item.fragment }}{% endif %}">
          {{ item.label }}
        </a>
      </li>
      {% endfor %}
    </ul>
  </div>
</section>
{% endif %}
```

**Características**:
- Solo se muestra si `show_global_shortcuts` es True
- `role="listbox"`: Container de opciones
- `role="option"`: Cada resultado
- Ctrl por JavaScript para filtrado

### Main Content

```html
{% block body %}{% endblock %}
```

**Uso**:
- Bloque para que páginas fillan el contenido
- Cada página extiende base.html y define `body`
- Puede contener `<main>` dentro del bloque

### Beta Signup Modal

```html
<div id="beta-modal" class="modal" role="dialog" aria-labelledby="beta-modal-title" aria-hidden="true">
  <div class="modal__content">
    <div class="modal__header">
      <h2 class="modal__title" id="beta-modal-title">Únete a la Beta de Buddy</h2>
      <button class="modal__close" id="beta-modal-close" aria-label="Cerrar">×</button>
    </div>

    <form class="modal__form" id="beta-signup-form">
      <div class="modal__field">
        <label for="beta-name">Nombre</label>
        <input type="text" id="beta-name" name="name" required placeholder="Tu nombre">
      </div>
      <div class="modal__field">
        <label for="beta-email">Email</label>
        <input type="email" id="beta-email" name="email" required placeholder="tu@email.com">
      </div>
      <div class="modal__field">
        <label for="beta-platform">Plataforma preferida</label>
        <select id="beta-platform" name="platform" required>
          <option value="">Selecciona una opción</option>
          <option value="ios">iOS (iPhone/iPad)</option>
          <option value="android">Android</option>
          <option value="web">Aplicación Web</option>
        </select>
      </div>
      <button type="submit" class="btn btn--primary modal__submit">¡Unirme a la Beta!</button>
    </form>

    <div id="beta-success" style="display:none; text-align:center; padding: var(--space-3);">
      <h3 style="color: var(--brand-base);">¡Gracias por unirte!</h3>
      <p>Te notificaremos cuando Buddy esté listo para descargar.</p>
    </div>
  </div>
</div>
```

**ARIA**:
- `role="dialog"`: Modal dialog
- `aria-labelledby`: Título del modal
- `aria-hidden="true"`: Oculto a screen readers
- `aria-modal="true"`: Modal activo (CSS)

**Estados**:
- **Closed**: `display: none` o `opacity: 0`
- **Open**: `display: flex`, `opacity: 1`, `aria-hidden="false"`
- **Success**: Form hidden, success message shown

### Footer

```html
<footer class="site-footer" role="contentinfo">
  <div class="container">
    <div>© Croody 2025 · {% trans "Inspirados en valores eternos" %}</div>
    <nav aria-label="{% trans 'Legal' %}">
      <a href="#">{% trans "Privacidad" %}</a>
      <a href="#">{% trans "Términos" %}</a>
      <a href="#">{% trans "Cookies" %}</a>
    </nav>
  </div>
</footer>
```

**ARIA**:
- `role="contentinfo"`: Región de pie de página
- Solo uno por página
- `<nav aria-label="Legal">`: Navegación de footer

**CSS**:
```css
.site-footer {
  background: var(--surface-1);
  padding: var(--space-4) 0;
  margin-top: var(--space-6);
  border-top: 1px solid color-mix(in oklab, var(--brand-base), transparent 85%);
}

.site-footer .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.site-footer nav {
  display: flex;
  gap: var(--space-3);
}

.site-footer nav a {
  color: var(--fg-muted);
  transition: color 233ms ease;
}

.site-footer nav a:hover {
  color: var(--fg);
}
```

### Scripts

```html
<script src="{% static 'js/theme.js' %}" defer></script>
<script src="{% static 'js/language-selector.js' %}" defer></script>
{% block body_scripts %}{% endblock %}
```

**Loading Strategy**:
- `defer`: Ejecuta después de parsear HTML
- Orden: theme.js → language-selector.js
- `body_scripts`: Block para scripts adicionales

## Context Variables

### Variables Disponibles

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `LANGUAGE_CODE` | Código de idioma actual | `"es"`, `"en"` |
| `brand` | Marca activa | `"gator"`, `"crimson"`, `"gold"` |
| `nav_links` | Links de navegación | `[{label: 'Tienda', url: '/tienda/'}]` |
| `search_results` | Resultados de búsqueda | `[{label: 'Producto 1', url: '/producto-1'}]` |
| `show_global_shortcuts` | Mostrar shortcuts | `True/False` |
| `messages` | Flash messages | `[(tags: 'success', message: 'OK')]` |
| `request` | Django request object | `request.path`, `request.user` |

### Injectar Variables desde Views

```python
# views.py
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
        'brand': 'gator',
        'nav_links': get_nav_links(),
        'search_results': get_search_results(),
        'show_global_shortcuts': True,
    })
    return context
```

## Block Tags

### Block Definitions

| Block | Propósito | Override en |
|-------|-----------|-------------|
| `title` | Título de la página | Todas las páginas |
| `meta_description` | Meta descripción SEO | Página específica |
| `og_title` | Open Graph título | Página específica |
| `og_description` | Open Graph descripción | Página específica |
| `twitter_title` | Twitter Card título | Página específica |
| `twitter_description` | Twitter Card descripción | Página específica |
| `head_fonts` | Preload fonts | Opcional |
| `head_extra` | Extra CSS/JS en `<head>` | Opcional |
| `body` | Contenido principal | **Todas las páginas** |
| `body_scripts` | Scripts antes de `</body>` | Opcional |

### Ejemplo de Extensión

```html
{% extends 'base.html' %}

{% block title %}Título de la Página{% endblock %}

{% block meta_description %}
  Descripción específica para SEO
{% endblock %}

{% block body %}
<main id="main">
  <h1>Mi Página</h1>
  <p>Contenido...</p>
</main>
{% endblock %}

{% block body_scripts %}
<script>
  // Código específico de la página
</script>
{% endblock %}
```

## SEO Optimization

### Structured Data (JSON-LD)
```html
{% block structured_data %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Croody",
  "url": "{{ request.build_absolute_uri }}",
  "description": "Croody conecta personas con tecnología humanizada",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "{{ request.build_absolute_uri }}search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
</script>
{% endblock %}
```

### Hreflang para i18n
```html
{% if LANGUAGE_CODE %}
<link rel="alternate" hreflang="{{ LANGUAGE_CODE }}" href="{{ request.build_absolute_uri }}">
<link rel="alternate" hreflang="x-default" href="{{ request.build_absolute_uri }}">
{% endif %}

{% for lang_code, lang_url in available_languages %}
<link rel="alternate" hreflang="{{ lang_code }}" href="{{ lang_url }}">
{% endfor %}
```

## Accessibility Features

### ARIA Landmarks
```html
<header role="banner">        <!-- Header principal -->
<nav role="navigation">       <!-- Navegación (implícita) -->
<main role="main">            <!-- Contenido principal -->
<aside role="complementary"> <!-- Contenido complementario -->
<section role="region">       <!-- Secciones genéricas -->
<footer role="contentinfo">  <!-- Footer -->
```

### Screen Reader Only Text
```css
.visually-hidden {
  position: absolute !important;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### Focus Management
```css
:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 3px;
}

/* Skip link visible on focus */
.skip-link:focus {
  top: 21px;
}
```

## Performance Optimization

### Critical CSS
```html
<!-- Above-the-fold CSS -->
<link rel="stylesheet" href="{% static 'css/tokens.css' %}">
<link rel="stylesheet" href="{% static 'css/base.css' %}">

<!-- Below-the-fold CSS -->
<link rel="stylesheet" href="{% static 'css/components.css' %}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{% static 'css/components.css' %}"></noscript>
```

### Resource Hints
```html
<!-- DNS Prefetch para dominios externos -->
<link rel="dns-prefetch" href="//fonts.googleapis.com">
<link rel="dns-prefetch" href="//www.google-analytics.com">

<!-- Preconnect para recursos críticos -->
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Prefetch para próxima página probable -->
<link rel="prefetch" href="{% url 'shop:catalogue' %}">
```

### Lazy Loading
```html
<!-- Imágenes no críticas -->
<img src="image.jpg" loading="lazy" alt="Description">

<!-- iframes -->
<iframe src="video.html" loading="lazy"></iframe>
```

## Responsive Breakpoints

### Breakpoint Variables
```css
:root {
  --bp-sm: 480px;
  --bp-md: 768px;
  --bp-lg: 1024px;
  --bp-xl: 1280px;
  --bp-2xl: 1536px;
}
```

### Media Queries en CSS
```css
/* Mobile First - Base styles */

/* Tablet */
@media (min-width: 768px) {
  .nav__primary {
    display: flex; /* Mostrar nav en tablet */
  }
  .nav-toggle {
    display: none;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .header__actions {
    gap: var(--space-2);
  }
}

/* Wide */
@media (min-width: 1280px) {
  .container {
    max-width: 1340px;
  }
}
```

## Testing

### HTML Validation
```bash
# Usar validator.w3.org o nu.html5.org
curl -H "Content-Type: text/html" \
     --data-binary @base.html \
     https://validator.w3.org/nu/
```

### Accessibility Testing
```javascript
// axe-core
import { configureAxe } from '@axe-core/playwright';

test('base template is accessible', async ({ page }) => {
  await page.goto('/');
  const results = await new AxePuppeteer(page).analyze();
  expect(results.violations).toEqual([]);
});
```

### Performance Testing
```javascript
// Lighthouse CI
import { playAudit } from 'lighthouse-ci-action';

test('page performance', async () => {
  await playAudit({
    url: 'http://localhost:8000',
    thresholds: {
      performance: 90,
      accessibility: 95,
      seo: 90,
    },
  });
});
```

## Best Practices

### ✅ Hacer
```html
<!-- Usar semantic HTML -->
<header role="banner">
<nav role="navigation">
<main role="main">
<footer role="contentinfo">

<!-- Proporcionar ARIA labels -->
<button aria-label="Abrir menú" aria-expanded="false">

<!-- Usar alt text descriptivo -->
<img src="logo.png" alt="Croody - Tecnología humanizada">

<!-- Bloques para customization -->
{% block body %}{% endblock %}
```

### ❌ Evitar
```html
<!-- No divs sin propósito -->
<div class="wrapper">
  <div class="container">
    <div class="content">

<!-- No inline styles -->
<div style="color: red;">

<!-- No JavaScript inline -->
<script>alert('test');</script>

<!-- No omitir lang attribute -->
<html>  <!-- Debe tener lang -->

<!-- No skip links -->
<!-- Los usuarios de teclado los necesitan -->
```

## Common Patterns

### 1. Page Template
```html
{% extends 'base.html' %}

{% block title %}Página - Croody{% endblock %}
{% block meta_description %}Descripción SEO{% endblock %}

{% block body %}
<main id="main">
  <section class="container">
    <h1>Título de Página</h1>
    <p>Contenido...</p>
  </section>
</main>
{% endblock %}
```

### 2. Landing Page with Hero
```html
{% extends 'base.html' %}

{% block body %}
<main id="main">
  <section id="hero" class="hero">
    <div class="container">
      <div class="hero__wrap">
        <div class="hero__content">
          <h1>Título Hero</h1>
          <p>Subtítulo</p>
          <div class="hero__cta">
            <a href="/cta" class="btn btn--primary">CTA Principal</a>
            <a href="#more" class="btn btn--ghost">CTA Secundario</a>
          </div>
        </div>
        <div class="hero__visual">
          <img src="{% static 'img/hero.svg' %}" alt="Ilustración hero">
        </div>
      </div>
    </div>
  </section>
</main>
{% endblock %}
```

### 3. Product Detail
```html
{% extends 'base.html' %}

{% block body %}
<main id="main">
  <article class="product-detail">
    <div class="container">
      <nav class="breadcrumb">
        <a href="/">Inicio</a> /
        <a href="/tienda/">Tienda</a> /
        <span>{{ product.name }}</span>
      </nav>

      <div class="product-layout">
        <div class="product-gallery">
          <img src="{{ product.image.url }}" alt="{{ product.name }}">
        </div>
        <div class="product-info">
          <h1>{{ product.name }}</h1>
          <p class="product-teaser">{{ product.teaser }}</p>
          <div class="product-price">{{ product.price }}</div>
          <button class="btn btn--primary">Añadir al carrito</button>
        </div>
      </div>
    </div>
  </article>
</main>
{% endblock %}
```

## Referencias

### Archivos Relacionados
- `templates/landing/home.html` - Página de inicio
- `templates/shop/catalogue.html` - Catálogo de productos
- `templates/account/profile.html` - Perfil de usuario
- `static/css/base.css` - Estilos base
- `static/js/theme.js` - Theme toggle
- `static/js/language-selector.js` - Selector de idiomas

### Documentación Externa
- [HTML Living Standard](https://html.spec.whatwg.org/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Schema.org](https://schema.org/)
- [Open Graph Protocol](https://ogp.me/)

## Ver También
- [Design System - Tokens](../design-system/tokens.md)
- [Design System - Colores](../design-system/colores.md)
- [JavaScript - Theme Toggle](../javascript/theme-toggle.md)
- [JavaScript - Language Selector](../javascript/language-selector.md)
