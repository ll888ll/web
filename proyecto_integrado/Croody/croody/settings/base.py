"""Configuración base del proyecto Croody.

Esta configuración se comparte entre desarrollo y producción.
Configuraciones específicas van en development.py y production.py.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


import os

try:
    import dj_database_url
except ImportError:
    dj_database_url = None


# ========================================
# CORE SETTINGS
# ========================================

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-change-me-para-produccion'
)

DEBUG = os.getenv('DEBUG', 'true').lower() in {'1', 'true', 'yes', 'on'}

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if h.strip()
] or ['localhost', '127.0.0.1']


# ========================================
# INSTALLED APPS
# ========================================

INSTALLED_APPS = [
    # Admin moderno - DEBE ir ANTES de django.contrib.admin
    'unfold',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',

    # Local apps
    'landing.apps.LandingConfig',
    'shop.apps.ShopConfig',
    'telemetry.apps.TelemetryConfig',
]

if DEBUG and importlib.util.find_spec('sslserver'):
    INSTALLED_APPS.append('sslserver')


# ========================================
# MIDDLEWARE
# ========================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ========================================
# TEMPLATES
# ========================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ========================================
# WSGI
# ========================================

ROOT_URLCONF = 'croody.urls'
WSGI_APPLICATION = 'croody.wsgi.application'


# ========================================
# DATABASE
# ========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.getenv('DATABASE_URL') and dj_database_url:
    DATABASES['default'] = dj_database_url.parse(
        os.environ['DATABASE_URL'],
        conn_max_age=600,
        ssl_require=False
    )


# ========================================
# AUTH & PASSWORDS
# ========================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator'
    },
]


# ========================================
# INTERNATIONALIZATION
# ========================================

LANGUAGE_CODE = 'es'

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

LOCALE_PATHS = [BASE_DIR / 'locale']

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ========================================
# STATIC FILES
# ========================================

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ========================================
# MEDIA FILES
# ========================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ========================================
# DEFAULT FIELDS
# ========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ========================================
# AUTH SETTINGS
# ========================================

from django.urls import reverse_lazy

LOGIN_URL = reverse_lazy('landing:login')
LOGIN_REDIRECT_URL = reverse_lazy('shop:catalogue')
LOGOUT_REDIRECT_URL = reverse_lazy('landing:home')


# ========================================
# REST FRAMEWORK
# ========================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}


# ========================================
# UNFOLD (ADMIN MODERNO)
# ========================================

UNFOLD = {
    "SIDEBAR": {
        "show_search": True,
        "show_applications": True,
        "show_language_chooser": True,
    },
    "THEME": {
        "primary": "#3C9E5D",
        "secondary": "#E0B771",
        "accent": "#975C9B",
        "success": "#3C9E5D",
        "warning": "#F5B454",
        "danger": "#F06565",
        "info": "#31BFEA",
        "background": "#F0FBF5",
        "surface": "#DDF6E8",
        "border": "#B4E5C6",
    },
    "TABLES": {
        "row_hover": True,
        "header_background": "#DDF6E8",
    },
    "MODELS": {
        "hide_in_app_list": [],
    },
}


# ========================================
# SECURITY (Production overrides)
# ========================================

# Configuración de seguridad básica
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# HSTS
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Cookies
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# SSL
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# ========================================
# LOGGING
# ========================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
