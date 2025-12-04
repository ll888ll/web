# Guía de Traducción - Croody

Este documento explica cómo funciona el sistema de traducción multiidioma implementado en Croody.

## Idiomas Soportados

El proyecto ahora soporta los siguientes 8 idiomas:

1. **Español (es)** - Idioma por defecto 🇪🇸
2. **Inglés (en)** - English 🇬🇧
3. **Francés (fr)** - Français 🇫🇷
4. **Portugués (pt)** - Português 🇵🇹
5. **Árabe (ar)** - العربية 🇸🇦
6. **Chino Simplificado (zh-hans)** - 简体中文 🇨🇳
7. **Japonés (ja)** - 日本語 🇯🇵
8. **Hindi (hi)** - हिन्दी 🇮🇳

## Selector de Idiomas

El selector de idiomas está ubicado en el header de todas las páginas y incluye:

- **Diseño estético**: Botón con icono 🌐 y código del idioma actual
- **Dropdown animado**: Lista desplegable con banderas y nombres de idiomas
- **Responsive**: Adaptado para móviles y tablets
- **Accesibilidad**: Navegación por teclado (flechas, Escape, Enter)
- **Estado activo**: El idioma seleccionado se muestra destacado

## Cómo Funciona

1. **Middleware**: Django LocaleMiddleware detecta el idioma del usuario
2. **URLs con prefijo**: Todas las URLs tienen prefijo de idioma (ej: `/es/`, `/en/`)
3. **Persistencia**: La selección se guarda en sesión/cookie
4. **Formulario POST**: El cambio de idioma se hace vía POST a `/i18n/set_language/`

## Contenido Actualizado

### Landing Page (Home)
- Hero section con mensaje "Volvamos a ser humanos"
- Tres vectores del ecosistema Croody:
  - **Buddy** (Fitness & Conexión) - "Conecta, Entrena y Destaca"
  - **My Luks** (Economía Digital) - "Seguridad, Abundancia y Proyección"
  - **Comida Real** (Alimentación) - "Alivio, Nostalgia y Satisfacción"

### Página Buddy
- Información completa del MVP de Buddy
- Tres pilares: IA personalizada, Biblioteca segura, Ecosistema de personajes
- Módulos, viajes de usuario y roadmap

## Próximos Pasos

Para completar la internacionalización:

1. **Crear archivos de traducción**:
   ```bash
   python manage.py makemessages -l en
   python manage.py makemessages -l fr
   python manage.py makemessages -l pt
   python manage.py makemessages -l ar
   python manage.py makemessages -l zh_Hans
   python manage.py makemessages -l ja
   python manage.py makemessages -l hi
   ```

2. **Traducir los archivos .po** en `locale/[idioma]/LC_MESSAGES/django.po`

3. **Compilar traducciones**:
   ```bash
   python manage.py compilemessages
   ```

4. **Envolver textos en templates** con `{% trans %}` y `{% blocktrans %}`

5. **Envolver textos en views.py** con `gettext()` o `gettext_lazy()`

## Archivos Modificados

- `croody/settings.py` - Configuración de idiomas y locale
- `croody/urls.py` - URLs con i18n_patterns
- `templates/base.html` - Selector de idiomas en header
- `static/css/components.css` - Estilos del selector
- `static/js/language-selector.js` - Funcionalidad del selector
- `landing/views.py` - Contenido actualizado según Landing.txt y Buddy.txt

## Diseño Visual

El selector de idiomas sigue el sistema de diseño de Croody:
- Variables CSS para colores y espaciado
- Animaciones suaves con cubic-bezier
- Coherente con el theme toggle y botones existentes
- Sombras y efectos de hover consistentes
