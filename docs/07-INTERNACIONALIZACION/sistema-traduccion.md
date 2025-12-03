# Sistema de Internacionalización - Documentación Completa

## Resumen
El sistema de internacionalización (i18n) de Croody implementa soporte completo para 8 idiomas usando Django's built-in i18n framework, GNU gettext, y Django templates. Incluye español (idioma fuente), inglés, francés, portugués, árabe (con soporte RTL), chino simplificado, japonés e hindi, con URL prefijadas y traducción automática de contenido.

## Ubicación
- **Configuración**: `/proyecto_integrado/Croody/croody/settings.py` (líneas 99-112)
- **URLs**: `/proyecto_integrado/Croody/croody/urls.py` (líneas 3-31)
- **Traducciones**: `/proyecto_integrado/Croody/locale/`
  - `es/` - Español (fuente)
  - `en/` - English
  - `fr/` - Français
  - `pt/` - Português
  - `ar/` - العربية (RTL)
  - `zh-hans/` - 简体中文
  - `ja/` - 日本語
  - `hi/` - हिन्दी
- **Templates**: Todas las plantillas cargan `{% load i18n %}`

## Idiomas Soportados

### Lista Completa
```python
LANGUAGES = [
    ('es', 'Español'),           # Idioma fuente
    ('en', 'English'),           # Inglés
    ('fr', 'Français'),          # Francés
    ('pt', 'Português'),         # Portugués
    ('ar', 'العربية'),           # Árabe (RTL)
    ('zh-hans', '简体中文'),     # Chino simplificado
    ('ja', '日本語'),             # Japonés
    ('hi', 'हिन्दी'),            # Hindi
]
```

### Detalles por Idioma

| Código | Nombre Nativo | Escritura | RTL | Familia Lingüística |
|--------|---------------|----------|-----|---------------------|
| **es** | Español | Latin | No | Romance |
| **en** | English | Latin | No | Germánica |
| **fr** | Français | Latin | No | Romance |
| **pt** | Português | Latin | No | Romance |
| **ar** | العربية | Arabic | **Sí** | Semítica |
| **zh-hans** | 简体中文 | Hanzi (Chinese characters) | No | Sino-Tibetana |
| **ja** | 日本語 | Kanji/Hiragana/Katakana | No | Japónica |
| **hi** | हिन्दी | Devanagari | No | Indo-Aria |

### Características Especiales

#### RTL (Right-to-Left) Languages
```html
<!-- Árabe requiere configuración especial -->
<html lang="ar" dir="rtl">

<!-- CSS considerations -->
.rtl {
    direction: rtl;
    text-align: right;
}

.rtl .nav {
    left: auto;
    right: 20px;
}
```

#### CJK Languages (Chinese, Japanese, Korean)
```html
<!-- Font considerations -->
body:lang(zh-hans) {
    font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

body:lang(ja) {
    font-family: 'Noto Sans JP', 'Hiragino Kaku Gothic Pro', 'Yu Gothic', sans-serif;
}

body:lang(hi) {
    font-family: 'Noto Sans Devanagari', 'Mangal', sans-serif;
}
```

## Configuración de Django

### Settings.py Configuration
```python
# === INTERNATIONALIZATION ===
LANGUAGE_CODE = 'es'  # Idioma por defecto (español)

# Idiomas disponibles
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

# Directorio donde están las traducciones
LOCALE_PATHS = [BASE_DIR / 'locale']

# Zona horaria
TIME_ZONE = 'UTC'

# Habilitar i18n
USE_I18N = True

# Habilitar timezone awareness
USE_TZ = True
```

### Configuración Explicada

#### LANGUAGE_CODE
```python
LANGUAGE_CODE = 'es'
```
- **Propósito**: Idioma por defecto del sitio
- **Uso**: Se usa cuando Django no puede determinar el idioma del usuario
- **Archivo**: `locale/es/django.po` es el archivo fuente (msgid = msgstr)

#### LANGUAGES
```python
LANGUAGES = [('es', 'Español'), ('en', 'English'), ...]
```
- **Propósito**: Lista de idiomas soportados
- **Formato**: Tupla `(código, nombre)`
- **Nombre**: Se muestra en admin y selector de idiomas
- **Código**: Usado en URLs y headers

#### LOCALE_PATHS
```python
LOCALE_PATHS = [BASE_DIR / 'locale']
```
- **Propósito**: Directorio donde Django busca archivos .po/.mo
- **Estructura**:
  ```
  locale/
    ├── es/
    │   └── LC_MESSAGES/
    │       ├── django.po (texto fuente)
    │       └── django.mo (compilado)
    ├── en/
    │   └── LC_MESSAGES/
    │       ├── django.po
    │       └── django.mo
    └── ...
  ```

#### USE_I18N
```python
USE_I18N = True
```
- **Propósito**: Habilita Django's internationalization framework
- **Alternativa**: `False` para sitios monolingües (mejor performance)

## URL Configuration

### Pattern Configuration
```python
# urls.py
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

# Rutas sin prefijo (idioma por defecto)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # JavaScript i18n
    path('admin/', admin.site.urls),                   # Sin prefijo
    path('dashboard/', include('telemetry.urls')),
    path('', include('landing.urls', namespace='landing')),
    path('tienda/', include('shop.urls', namespace='shop')),
]

# Rutas con prefijo para idiomas distintos al por defecto
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('dashboard/', include('telemetry.urls')),
    path('', include('landing.urls', namespace='landing')),
    path('tienda/', include('shop.urls', namespace='shop')),
    prefix_default_language=False,  # ¡Clave! Mantiene / sin prefijo
)
```

### URL Structure

| URL Sin Prefijo | URL Con Prefijo | Idioma |
|-----------------|-----------------|--------|
| `/` | `/es/` | Español (default) |
| `/admin/` | `/es/admin/` | Español |
| `/tienda/` | `/es/tienda/` | Español |
| `/` | `/en/` | English |
| `/admin/` | `/en/admin/` | English |
| `/tienda/` | `/en/tienda/` | English |
| `/` | `/fr/` | Français |
| `/` | `/ar/` | العربية |
| `/` | `/zh-hans/` | 简体中文 |
| `/` | `/ja/` | 日本語 |
| `/` | `/hi/` | हिन्दी |

### prefix_default_language=False

**Sin prefix_default_language**:
```python
# ❌ Comportamiento por defecto
urlpatterns += i18n_patterns(...)

# Resultado:
# /es/ → Español (default)
# /en/ → English
# /fr/ → Français
# Problema: `/` sin prefijo causa Resolver404
```

**Con prefix_default_language=False**:
```python
# ✅ Solución recomendada
urlpatterns += i18n_patterns(
    ...,
    prefix_default_language=False
)

# Resultado:
# / → Español (default, sin prefijo)
# /es/ → Español (con prefijo)
# /en/ → English
# /fr/ → Français
# Ventaja: Compatibilidad total con rutas existentes
```

### i18n JavaScript View
```python
path('i18n/', include('django.conf.urls.i18n'))
```

**Propósito**: Provee endpoint para JavaScript i18n
- **URL**: `/i18n/javascript/`
- **Uso**: Carga traducciones para JavaScript
- **Formato**: JSON con pares key-value

**Template Usage**:
```html
<script src="/i18n/javascript/"></script>
<script>
    console.log(gettext('Hello World'));  // Traducido
</script>
```

## Archivos de Traducción

### Estructura .po File
```po
# Spanish translations for Croody project.
# Copyright (C) 2024 Croody
#
msgid ""
msgstr ""
"Project-Id-Version: Croody 1.0\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2025-01-06 17:30+0000\n"
"PO-Revision-Date: 2025-01-06 17:30+0000\n"
"Last-Translator: Croody Team\n"
"Language-Team: Spanish <hola@croody.app>\n"
"Language: es\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"

msgid "Croody · Precisión cósmica con corazón"
msgstr ""

msgid "Saltar al contenido principal"
msgstr "Passer au contenu principal"
```

### Metadatos .po

| Campo | Ejemplo | Propósito |
|-------|---------|-----------|
| `Project-Id-Version` | `Croody 1.0` | Identificador del proyecto |
| `POT-Creation-Date` | `2025-01-06 17:30+0000` | Fecha de creación |
| `PO-Revision-Date` | `2025-01-06 17:30+0000` | Última revisión |
| `Last-Translator` | `Croody Team` | Último traductor |
| `Language-Team` | `Spanish <hola@croody.app>` | Equipo de traducción |
| `Language` | `es` | Código de idioma |
| `Content-Type` | `text/plain; charset=UTF-8` | Codificación |
| `Plural-Forms` | `nplurals=2; plural=(n != 1);` | Reglas pluralización |

### Plural Forms por Idioma

| Idioma | Regla Plural | Descripción |
|--------|--------------|-------------|
| **es** | `nplurals=2; plural=(n != 1);` | singular + plural |
| **en** | `nplurals=2; plural=(n != 1);` | singular + plural |
| **fr** | `nplurals=2; plural=(n != 1);` | singular + plural |
| **pt** | `nplurals=2; plural=(n != 1);` | singular + plural |
| **ar** | `nplurals=6; plural=(n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 && n%100<=99 ? 4 : 5);` | 6 formas |
| **zh-hans** | `nplurals=1; plural=0;` | Sin plurales |
| **ja** | `nplurals=1; plural=0;` | Sin plurales |
| **hi** | `nplurals=2; plural=(n!=1);` | singular + plural |

### .mo Files (Compiled)
```bash
# .po → .mo compilation
django-admin compilemessages

# Los archivos .mo son binary y no se editan manualmente
# Generados automáticamente desde .po
```

**Ubicación**:
```
locale/
  ├── es/
  │   └── LC_MESSAGES/
  │       ├── django.po  ← Editable
  │       └── django.mo  ← Compilado (no editar)
  ├── en/
  │   └── LC_MESSAGES/
  │       ├── django.po
  │       └── django.mo
  └── ...
```

## Uso en Templates

### Cargar i18n
```html
{% load i18n %}
```

**Importante**: Debe estar en la primera línea del template o antes de usar tags de traducción

### Trans Simple
```html
<!-- Básico -->
<h1>{% trans "Croody · Precisión cósmica con corazón" %}</h1>

<!-- Con variable -->
<p>{% trans "Hola" %}, {{ user.name }}!</p>

<!-- Sin traducción automática -->
{% trans "Text" noop %}

<!-- Con contexto -->
{% trans "Bar" context "noun" %}
```

### Trans con Block
```html
<!-- Para textos largos -->
{% blocktrans %}
    Esta es una descripción larga del producto
    que se extiende por múltiples líneas
    y será traducida completa.
{% endblocktrans %}

<!-- Con variables -->
{% blocktrans with product_name=product.name price=product.price %}
    El producto {{ product_name }} cuesta {{ price }} euros.
{% endblocktrans %}
```

### Trans con Formato
```html
<!-- Formateo de números -->
{% blocktrans count counter=num_items %}
    Tienes {{ counter }} producto.
{% plural %}
    Tienes {{ counter }} productos.
{% endblocktrans %}

<!-- Formateo de fechas -->
{% blocktrans with date=order.date %}
    Pedido del {{ date }}.
{% endblocktrans %}
```

### Ejemplos Reales en Croody

#### Base Template
```html
{% load i18n %}

<html lang="{{ LANGUAGE_CODE }}">
<a class="skip-link" href="#main">{% trans "Saltar al contenido principal" %}</a>

<button class="nav-toggle" type="button" aria-label="{% trans 'Abrir menú' %}">
  <span></span>
</button>

<input type="search" placeholder="{% trans 'Buscar (pulsa /)' %}">

<button aria-label="{% trans 'Seleccionar idioma' %}">
  <span>{{ LANGUAGE_CODE|upper }}</span>
</button>

<label aria-label="{% trans 'Cambiar tema' %}">
  <input type="checkbox" />
</label>

{% if request.user.is_authenticated %}
  <a>{% trans "Empezar" %}</a>
  <a>{% trans "Perfil" %}</a>
  <a>{% trans "Salir" %}</a>
{% else %}
  <a>{% trans "Acceder" %}</a>
{% endif %}
```

#### Landing Page
```html
{% extends "base.html" %}

{% block title %}{% trans "Croody · Diseño con propósito" %}{% endblock %}

{% block meta_description %}
    {% trans "Croody conecta personas con tecnología humanizada" %}
{% endblock %}

{% block body %}
<main id="main">
    <section class="hero">
        <h1>{% trans "Croody · Precisión cósmica con corazón" %}</h1>
        <p>{% trans "Inspirados en valores eternos" %}</p>
    </section>
</main>
{% endblock %}
```

### Variables en Trans
```html
<!-- ❌ Mal: Concatenación en template -->
{% trans "Hola " %}{{ user.name }}{% trans "!" %}

<!-- ✅ Bien: Con variable en blocktrans -->
{% blocktrans %}Hola {{ user.name }}!{% endblocktrans %}

<!-- ⚠️ Cuidado: gettext no concatena automáticamente -->
```

## Uso en Python

### Vistas
```python
from django.shortcuts import render
from django.utils.translation import gettext as _

def home_view(request):
    context = {
        'title': _('Croody · Diseño con propósito'),
        'description': _('Inspirados en valores eternos'),
        'user': request.user,
    }
    return render(request, 'landing/home.html', context)

# O usando ugettext_lazy para traducciones lazy
from django.utils.translation import ugettext_lazy as _

def product_view(request):
    product_name = _('Nombre del producto')
    return render(request, 'shop/product.html', {'product_name': product_name})
```

### Modelos
```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(_('Nombre'), max_length=200)
    description = models.TextField(_('Descripción'))
    price = models.DecimalField(_('Precio'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('Producto')
        verbose_name_plural = _('Productos')

    def __str__(self):
        return self.name
```

### Forms
```python
from django import forms
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(
        label=_('Nombre completo'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': _('Tu nombre')})
    )

    email = forms.EmailField(
        label=_('Correo electrónico'),
        widget=forms.EmailInput(attrs={'placeholder': _('tu@email.com')})
    )

    message = forms.CharField(
        label=_('Mensaje'),
        widget=forms.Textarea(attrs={'rows': 5})
    )
```

### Messages
```python
from django.contrib import messages
from django.utils.translation import gettext as _

def add_to_cart(request, product_id):
    if success:
        messages.success(request, _('Producto agregado al carrito'))
    else:
        messages.error(request, _('Error al agregar producto'))

# En template
{% if messages %}
    {% for message in messages %}
        <div class="flash flash--{{ message.tags }}">{{ message }}</div>
    {% endfor %}
{% endif %}
```

## JavaScript i18n

### Loading Translations
```html
<script src="/i18n/javascript/"></script>
<script>
    console.log(gettext('Hello World'));
    console.log(ngettext('%(count)s producto', '%(count)s productos', count));
</script>
```

### Custom JavaScript i18n
```javascript
// translations.js
const translations = {
    'es': {
        'Loading...': 'Cargando...',
        'Error': 'Error',
        'Success': 'Éxito'
    },
    'en': {
        'Loading...': 'Loading...',
        'Error': 'Error',
        'Success': 'Success'
    }
};

function getCurrentLanguage() {
    return document.documentElement.lang || 'es';
}

function gettext(message) {
    const lang = getCurrentLanguage();
    return translations[lang][message] || message;
}

function interpolate(template, context) {
    return template.replace(/%\(\w+\)s/g, match => context[match.slice(2, -1)]);
}

// Usage
console.log(gettext('Loading...'));
```

### AJAX with i18n
```javascript
// Incluir idioma en requests AJAX
function fetchWithI18n(url, data) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            'Accept-Language': document.documentElement.lang  // Enviar idioma
        },
        body: JSON.stringify(data)
    });
}

// Server puede detectar idioma del header
def api_view(request):
    language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'es')
    # Usar language para respuesta localizada
```

## Language Selector

### HTML Structure
```html
<div class="language-selector">
    <button class="language-selector__trigger" type="button"
            aria-haspopup="true" aria-expanded="false">
        <span class="language-selector__icon">🌐</span>
        <span class="language-selector__current">{{ LANGUAGE_CODE|upper }}</span>
    </button>
    <div class="language-selector__dropdown" hidden>
        <a href="/es/{{ request.get_full_path|slice:'3:' }}" class="language-selector__option active">
            <span class="language-selector__flag">🇪🇸</span>
            <span>Español</span>
        </a>
        <a href="/en/{{ request.get_full_path|slice:'3:' }}" class="language-selector__option">
            <span class="language-selector__flag">🇬🇧</span>
            <span>English</span>
        </a>
        <!-- Más idiomas... -->
    </div>
</div>
```

### URL Slicing Logic
```django
# Remover prefijo de idioma del path
# Ejemplo: /es/shop/products/ → /shop/products/

request.get_full_path|slice:'3:'

# Explicación:
# /es/shop/products/
# ^^^
# 0 1 2
# slice:'3:' = desde carácter 3 en adelante
# Resultado: /shop/products/
```

### Language Switch Views
```python
from django.views.generic import TemplateView
from django.utils.translation import activate

class LanguageSwitchView(TemplateView):
    def get(self, request, lang):
        activate(lang)  # Activa idioma
        # Preservar URL sin prefijo
        return redirect(request.META.get('HTTP_REFERER', '/'))

# urls.py
path('lang/<str:lang>/', LanguageSwitchView.as_view(), name='switch_language')
```

### JavaScript Implementation
```javascript
// language-selector.js
document.querySelectorAll('.language-selector__option').forEach(option => {
    option.addEventListener('click', function(e) {
        const lang = this.getAttribute('data-lang');
        const url = this.getAttribute('href');

        // Store in localStorage
        localStorage.setItem('preferred_language', lang);

        // Navigate
        window.location.href = url;
    });
});

// Detect preferred language on load
const storedLang = localStorage.getItem('preferred_language');
if (storedLang) {
    // Redirect if different from current
    const currentLang = document.documentElement.lang;
    if (storedLang !== currentLang) {
        const newUrl = '/' + storedLang + window.location.pathname;
        window.location.href = newUrl;
    }
}
```

## RTL Support (Árabe)

### HTML Setup
```html
<html lang="ar" dir="rtl">
```

### CSS Considerations
```css
/* RTL Base Styles */
[dir="rtl"] {
    direction: rtl;
    text-align: right;
}

/* Flipping margins/paddings */
[dir="rtl"] .nav {
    margin-left: 0;
    margin-right: 20px;
}

/* Flipping floats */
[dir="rtl"] .logo {
    float: right;
}

/* Flipping flex direction */
[dir="rtl"] .row {
    flex-direction: row-reverse;
}

/* Flipping absolute positioning */
[dir="rtl"] .dropdown {
    left: 20px;
    right: auto;
}
```

### Icons and Arrows
```css
/* Flipping icons */
[dir="rtl"] .icon-arrow-right::before {
    content: "←";  /* Flip arrow */
}

/* Text vs Icon alignment */
[dir="rtl"] .search-icon {
    left: 10px;
    right: auto;
}
```

### JavaScript RTL Handling
```javascript
function isRTL(lang) {
    return ['ar', 'fa', 'he', 'ur'].includes(lang);
}

function applyRTL(lang) {
    const html = document.documentElement;
    if (isRTL(lang)) {
        html.setAttribute('dir', 'rtl');
        html.classList.add('rtl');
    } else {
        html.setAttribute('dir', 'ltr');
        html.classList.remove('rtl');
    }
}

// Apply on language change
applyRTL(document.documentElement.lang);
```

## Date and Number Formatting

### DATE_FORMAT
```python
# settings.py
from django.conf import global_settings

# Formato de fecha por idioma
LANG_DATE_FORMATS = {
    'es': 'd/m/Y',
    'en': 'M j, Y',
    'fr': 'd/m/Y',
    'pt': 'd/m/Y',
    'ar': 'Y/m/d',
    'zh-hans': 'Y年m月d日',
    'ja': 'Y年m月d日',
    'hi': 'd/m/Y',
}

# Uso en templates
{% load i18n %}
{% load l10n %}

{% localize on %}
    {{ value|date:"d/m/Y" }}
{% endlocalize %}
```

### Number Formatting
```python
# Python
from django.utils import formats
from django.utils.translation import activate

activate('es')
formatted = formats.number_format(1000.50, decimal_pos=2)
# Resultado: '1.000,50'

activate('en')
formatted = formats.number_format(1000.50, decimal_pos=2)
# Resultado: '1,000.50'
```

### Currency Formatting
```python
# Python
from django.utils import formats

activate('es')
price = formats.format_lazy(
    '{0}',
    currency_amount,
    use_l10n=True
)
# Resultado: "1.000,50 €"

activate('en')
# Resultado: "$1,000.50"
```

## Compilation Workflow

### Extract Strings
```bash
# 1. Extraer strings desde código y templates
django-admin makemessages --all

# Genera/actualiza archivos .po
# locale/
#   ├── es/
#   │   └── LC_MESSAGES/
#   │       └── django.po (actualizado)
#   ├── en/
#   │   └── LC_MESSAGES/
#   │       └── django.po (actualizado)
#   └── ...
```

### Edit .po Files
```bash
# Editar manualmente o con herramienta
# Poedit (GUI) - https://poedit.net/
# Lokalize (KDE)
# Virtaal (GNOME)

# O editar directamente
nano locale/es/LC_MESSAGES/django.po
```

### Compile Messages
```bash
# 2. Compilar .po → .mo
django-admin compilemessages

# Resultado: archivos .mo compilados
# locale/
#   ├── es/
#   │   └── LC_MESSAGES/
#   │       ├── django.po
#   │       └── django.mo ← Binario compilado
```

### Make & Compile in Docker
```python
# En Dockerfile
RUN python manage.py makemessages --all \
    && python manage.py compilemessages

# O script
#!/bin/bash
python manage.py makemessages --all
python manage.py compilemessages
```

### CI/CD Integration
```yaml
# .github/workflows/ci.yml
- name: Extract messages
  run: python manage.py makemessages --all

- name: Compile messages
  run: python manage.py compilemessages

- name: Check compiled messages
  run: |
    if [ -n "$(git diff --name-only | grep locale)" ]; then
      echo "Translations changed, please compile messages"
      exit 1
    fi
```

## Translation Management

### Best Practices

#### 1. String Externalization
```python
# ✅ Bien: Todos los user-facing strings externalizados
def home_view(request):
    return render(request, 'home.html', {
        'title': _('Bienvenido a Croody'),
        'welcome': _('Hola'),
    })

# ❌ Mal: Strings hardcodeados
def home_view(request):
    return render(request, 'home.html', {
        'title': 'Bienvenido a Croody',  # ¡No traducir!
    })
```

#### 2. Use Lazy Translation
```python
# ✅ Bien: ugettext_lazy para modelos
from django.utils.translation import ugettext_lazy as _

class Product(models.Model):
    name = models.CharField(_('Nombre'), max_length=100)

# ❌ Mal: gettext directo (ejecuta inmediatamente)
from django.utils.translation import gettext as _

name = _('Nombre')  # Se ejecuta al importar
```

#### 3. Placeholders and Variables
```python
# ✅ Bien: Usar placeholders
{% blocktrans with name=user.name %}
    Hola {{ name }}, bienvenido.
{% endblocktrans %}

# ❌ Mal: Concatenación
{% trans "Hola " %}{{ user.name }}{% trans ", bienvenido" %}
```

#### 4. Context
```python
# ✅ Bien: Usar contexto para palabras ambiguas
{% trans "Bar" context "noun" %}  # Bebida
{% trans "Bar" context "verb" %}  # Presente de "barrer"

# Python
from django.utils.translation import pgettext
pgettext('noun', 'Bar')  # La bebida
pgettext('verb', 'Bar')  # Acción de barrer
```

#### 5. Plurals
```python
# ✅ Bien: Usar pluralización automática
{% blocktrans count counter=items|length %}
    Tienes {{ counter }} producto.
{% plural %}
    Tienes {{ counter }} productos.
{% endblocktrans %}

# Python
from django.utils.translation import ngettext
message = ngettext(
    '%(count)s producto',
    '%(count)s productos',
    count
) % {'count': count}
```

### String Review Checklist

#### Before Marking for Translation
```markdown
- [ ] ¿Es texto visible al usuario?
- [ ] ¿No es código técnico?
- [ ] ¿No es nombre de archivo o URL?
- [ ] ¿No es configuración?
- [ ] ¿Usa placeholders para variables?
- [ ] ¿Tiene contexto si es ambiguo?
- [ ] ¿Maneja plurales correctamente?
```

#### Translation Quality
```markdown
- [ ] Traducción completa (no incompleta)
- [ ] Tono consistente con la marca
- [ ] Terminología técnica correcta
- [ ] Cultura/localización apropiada
- [ ] Sin errores de ortografía/gramática
- [ ] Longitud apropiada (no overflow)
```

### Tools

#### Poedit (Recommended)
```bash
# GUI para edición de .po
# https://poedit.net/

# Instalar
sudo apt install poedit  # Linux
# O descargar de la web

# Abrir archivo
poedit locale/es/LC_MESSAGES/django.po
```

#### Lokalize
```bash
# KDE translation tool
sudo apt install lokalize
```

#### Virtaal
```bash
# GNOME translation tool
sudo apt install virtaal
```

#### Command Line (msgfmt)
```bash
# Compilar .po → .mo
msgfmt -o locale/es/LC_MESSAGES/django.mo locale/es/LC_MESSAGES/django.po

# Ver estadísticas
msgfmt --statistics locale/es/LC_MESSAGES/django.po
```

## Performance

### Compilation
```python
# .mo files are binary and fast
# Django caches compiled translations in memory
# No runtime .po parsing
```

### Lazy Loading
```python
# Django loads translations on-demand
from django.utils.translation import ugettext_lazy as _
# Translation happens only when the string is evaluated
```

### Caching
```python
# settings.py
# Django caches messages in memory by default
# For multiple languages, memory usage ~ number of translations

# Clear cache on updates
from django.utils.translation import gettext as _
_('String')  # Caches translation
```

### Optimization Tips
```python
# 1. Avoid translating in loops
for item in items:
    name = _('Name')  # ❌ Repeated
# Better:
name_label = _('Name')  # ✅ Once
for item in items:
    item.name_label = name_label

# 2. Use gettext_lazy in models
from django.utils.translation import ugettext_lazy as _
class Product(models.Model):
    name = models.CharField(_('Name'), max_length=100)

# 3. Minimize .po file size
# Remove obsolete translations regularly
django-admin makemessages --all
django-admin compilemessages
```

## Testing

### Unit Tests
```python
from django.test import TestCase
from django.utils.translation import activate
from django.utils.translation import gettext as _

class I18NTestCase(TestCase):
    def test_translation(self):
        # Test Spanish (default)
        activate('es')
        self.assertEqual(_('Hola'), 'Hola')

        # Test English
        activate('en')
        self.assertEqual(_('Hola'), 'Hello')

        # Test French
        activate('fr')
        self.assertEqual(_('Hola'), 'Bonjour')

    def test_plural(self):
        from django.utils.translation import ngettext
        activate('es')
        self.assertEqual(ngettext('%(count)s producto', '%(count)s productos', 1), '1 producto')
        self.assertEqual(ngettext('%(count)s producto', '%(count)s productos', 5), '5 productos')
```

### Template Tests
```python
from django.test import SimpleTestCase
from django.template import Context, Template

class I18NTemplateTest(SimpleTestCase):
    def test_trans_block(self):
        template = Template('{% load i18n %}{% blocktrans %}Hello{% endblocktrans %}')
        context = Context({'LANGUAGE_CODE': 'en'})
        result = template.render(context)
        self.assertEqual(result, 'Hello')

    def test_trans_with_var(self):
        template = Template('{% load i18n %}{% blocktrans with name="World" %}Hello {{ name }}{% endblocktrans %}')
        context = Context({'LANGUAGE_CODE': 'en'})
        result = template.render(context)
        self.assertEqual(result, 'Hello World')
```

### Translation Coverage
```bash
# Verificar cobertura de traducciones
# Herramienta: django-rosetta o custom script

python -c "
import os
import polib
total = 0
translated = 0
for lang in ['en', 'fr', 'pt', 'ar', 'zh-hans', 'ja', 'hi']:
    po = polib.po_file(f'locale/{lang}/LC_MESSAGES/django.po')
    total += len(po.translated_entries())
    translated += len(po.translated_entries())
print(f'Translated: {translated}/{total} ({translated/total*100:.1f}%)')
"
```

## Troubleshooting

### Strings Not Translated

#### 1. Forgot to Load i18n
```html
<!-- ❌ Error -->
{% trans "Hello" %}

<!-- ✅ Fixed -->
{% load i18n %}
{% trans "Hello" %}
```

#### 2. Missing compilemessages
```bash
# Translation not showing
django-admin compilemessages  # Compile .po → .mo
```

#### 3. Wrong File Location
```python
# ❌ Archivo en lugar incorrecto
locale/                    # Wrong path
  └── django.po            # Should be in locale/xx/LC_MESSAGES/

# ✅ Correct path
locale/
  └── es/
      └── LC_MESSAGES/
          └── django.po
```

#### 4. Language Not in LANGUAGES
```python
# settings.py
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
    # Missing 'fr' but trying to translate
]

# Add missing language
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
    ('fr', 'Français'),  # Added
]
```

### URL Issues

#### 404 on Language Prefixed URLs
```python
# ❌ Wrong: No prefix_default_language
urlpatterns += i18n_patterns(
    path('', include('landing.urls')),
)

# ✅ Fixed: Add prefix_default_language
urlpatterns += i18n_patterns(
    path('', include('landing.urls')),
    prefix_default_language=False,
)
```

#### Redirect Loops
```python
# Problem: language switch redirects to itself
# Solution: Check current language
def switch_language(request, lang):
    if lang == request.LANGUAGE_CODE:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    # ... switch
```

### Template Issues

#### Untranslated Variable
```html
<!-- ❌ Variable not translated -->
<h1>{{ product.name }}</h1>

<!-- ✅ Set translated name in view -->
context = {'product_name': _('Product Name')}
```

#### Plural Issues
```html
<!-- ❌ Incorrect plural -->
{% trans "1 producto" %}

<!-- ✅ Correct plural -->
{% blocktrans count counter=1 %}
    {{ counter }} producto
{% plural %}
    {{ counter }} productos
{% endblocktrans %}
```

### Performance Issues

#### Large .po Files
```bash
# Remove obsolete translations
django-admin makemessages --all --ignore=venv --ignore=node_modules

# Check file size
ls -lh locale/*/LC_MESSAGES/django.po
```

#### Memory Usage
```python
# Many languages = more memory
# Optimize by loading only needed languages
# Django loads all .mo files into memory

# Consider lazy loading for infrequently used languages
```

## Deployment

### Docker Integration
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

# Compile translations
RUN python manage.py compilemessages

# Collect static
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "croody.wsgi:application"]
```

### Git Workflow
```bash
# .gitignore
locale/*/LC_MESSAGES/*.mo  # Ignore compiled files (regenerate on deploy)
!locale/*/LC_MESSAGES/django.mo  # But keep source

# Or better: include all .mo
# They are small and speed up deployment
```

### CI/CD Integration
```yaml
# .github/workflows/deploy.yml
- name: Setup translations
  run: |
    python manage.py compilemessages

- name: Check message coverage
  run: |
    python manage.py makemessages --all --dry-run
    # Fail if new strings not translated
```

### Environment Variables
```bash
# Optional: Override languages
export DJANGO_LANGUAGES="es,en,fr"

# Or specific language
export DJANGO_LANGUAGE_CODE="en"
```

## Best Practices Summary

### ✅ Do
```python
# 1. Externalize all user-facing strings
_('User-friendly message')

# 2. Use lazy translation for models/forms
from django.utils.translation import ugettext_lazy as _
name = _('Name')

# 3. Use placeholder variables
{% blocktrans with name=user.name %}Hello {{ name }}{% endblocktrans %}

# 4. Handle plurals correctly
{% blocktrans count n=items %}{{ n }} item{% plural %}{{ n }} items{% endblocktrans %}

# 5. Test all languages
for lang in ['es', 'en', 'fr', ...]:
    activate(lang)
    assert translated_string

# 6. Keep source language (es) consistent
msgid "Exact source text"
msgstr ""  # Empty = same as msgid

# 7. Regular updates
django-admin makemessages --all
django-admin compilemessages

# 8. Version control .po files
git add locale/*/LC_MESSAGES/django.po

# 9. Document translation process
# README Translation section
```

### ❌ Don't
```python
# 1. Don't concatenate strings
_('Hello') + ' ' + user.name  # ❌ Wrong

# 2. Don't translate code/technical terms
_('for')  # Programming keyword
_('localhost')  # Technical

# 3. Don't use translation in constants
API_ENDPOINT = _('api.example.com')  # ❌ Wrong

# 4. Don't ignore RTL languages
# Ensure CSS supports dir="rtl"

# 5. Don't hardcode language codes
if lang == 'es':  # ❌ Use LANGUAGE_CODE
# Better: if lang == settings.LANGUAGE_CODE

# 6. Don't commit .mo files if regenerating
# Generate on deployment
# Or: commit all files (faster deployment)

# 7. Don't translate HTML tags
{% trans "<strong>Bold</strong>" %}  # ❌ Wrong
# Better: {% trans "Bold" %} with <strong>

# 8. Don't use translation in migration
# migrations are frozen snapshots
```

## Advanced Topics

### Custom Translation Backend
```python
# settings.py
# Use database-backed translations
LOCALE_PATHS = [BASE_DIR / 'locale']
USE_I18N = True

# Custom loader (optional)
# For dynamic translation loading
```

### Translation Extraction Script
```python
#!/usr/bin/env python3
"""Extract all translatable strings."""
import os
import re
from pathlib import Path

def extract_strings(directory):
    """Extract strings from Python and template files."""
    strings = set()

    # Python files
    for py_file in Path(directory).rglob('*.py'):
        with open(py_file) as f:
            content = f.read()
            # Find _('string') and _("string")
            matches = re.findall(r'_\([\'\"](.*?)[\'\"]\)', content)
            strings.update(matches)

    # Template files
    for html_file in Path(directory).rglob('*.html'):
        with open(html_file) as f:
            content = f.read()
            # Find {% trans "string" %}
            matches = re.findall(r'{% trans [\'\"](.*?)[\'\"]', content)
            strings.update(matches)

    return strings

# Usage
strings = extract_strings('proyecto_integrado')
for s in sorted(strings):
    print(s)
```

### Translation API
```python
# views.py
from django.http import JsonResponse
from django.utils.translation import gettext as _

def translate_text(request):
    """API endpoint for client-side translation."""
    text = request.GET.get('text', '')
    lang = request.GET.get('lang', 'es')

    # Activate language
    from django.utils.translation import activate
    activate(lang)

    # Translate
    translated = _(text)

    return JsonResponse({
        'original': text,
        'translated': translated,
        'language': lang
    })

# URL
path('api/translate/', translate_text, name='translate')
```

### Plural Rule Testing
```python
def test_plural_rules():
    """Test plural rules for all languages."""
    from django.utils.translation import ngettext

    test_cases = [
        ('es', 1, 'producto'),  # singular
        ('es', 5, 'productos'),  # plural
        ('en', 1, 'product'),  # singular
        ('en', 5, 'products'),  # plural
        ('ar', 0, 'منتج'),  # zero
        ('ar', 1, 'منتج'),  # one
        ('ar', 2, 'منتجان'),  # two
        ('ar', 3, 'منتجات'),  # few
        ('ar', 11, 'منتج'),  # many
    ]

    for lang, count, expected in test_cases:
        from django.utils.translation import activate
        activate(lang)
        # Test plural form
        result = ngettext('%(count)s منتج', '%(count)s منتجات', count) % {'count': count}
        print(f'{lang}: {count} → {result}')
```

## Referencias

### Archivos Relacionados
- `croody/settings.py` - Configuración i18n
- `croody/urls.py` - URL patterns con i18n
- `locale/` - Archivos de traducción .po/.mo
- `templates/base.html` - Template base con carga i18n

### Herramientas
- [Django i18n Documentation](https://docs.djangoproject.com/en/stable/topics/i18n/)
- [GNU gettext Manual](https://www.gnu.org/software/gettext/manual/)
- [Poedit](https://poedit.net/) - Editor GUI
- [Rosetta](https://github.com/mbi/django-rosetta) - Web UI para traducciones

### Estándares
- [BCP 47 - Language Tags](https://tools.ietf.org/html/bcp47)
- [ISO 639 - Language Codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
- [RFC 5646 - Accept-Language](https://tools.ietf.org/html/rfc5646)

## Ver También
- [Templates - Base](../03-FRONTEND/templates/base.md#i18n-in-templates)
- [JavaScript - Language Selector](../03-FRONTEND/javascript/language-selector.md)
- [CI/CD - Translation Workflows](../04-DEVOPS/ci-cd-workflows.md)
