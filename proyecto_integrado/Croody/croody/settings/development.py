"""Configuración de desarrollo para Croody.

Esta configuración está optimizada para desarrollo local.
Incluye tools de debugging y desarrollo rápido.
"""
from .base import *

import os


# ========================================
# CORE SETTINGS (Development)
# ========================================

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '0.0.0.0']


# ========================================
# INSTALLED APPS (Development)
# ========================================

INSTALLED_APPS += [
    # 'debug_toolbar',  # Deshabilitado temporalmente
    'django_extensions',
    # 'rosetta',  # Translation interface - deshabilitado temporalmente
    # 'silk',  # Deshabilitado temporalmente
]

# ========================================
# MIDDLEWARE (Development)
# ========================================

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',  # Deshabilitado temporalmente
    # 'silk.middleware.SilkyMiddleware',  # Deshabilitado temporalmente
] + MIDDLEWARE


# ========================================
# INTERNAL IPS
# ========================================

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]


# ========================================
# DEBUG TOOLBAR
# ========================================

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG and request.META.get('REMOTE_ADDR') in INTERNAL_IPS,
}


# ========================================
# LOGGING (Development)
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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'croody': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# ========================================
# SECURITY (Development - Relaxed)
# ========================================

# Deshabilitar SSL en desarrollo
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# ========================================
# CACHING (Development)
# ========================================

# Use LocMemCache for replay attack prevention to work
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'croody-dev-cache',
    }
}


# ========================================
# SILK (Profiling)
# ========================================

SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_PYTHON_PROFILER_RESULT_PATH = BASE_DIR / 'profiles'
SILKY_PYTHON_PROFILER_RESULT_BINARY_FILENAME = 'profile.prof'


# ========================================
# EMAIL (Development)
# ========================================

# Usar console backend para emails en desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ========================================
# STATIC FILES (Development)
# ========================================

# En desarrollo, servir archivos estáticos directamente
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


# ========================================
# DEVELOPMENT TOOLS
# ========================================

# Permitir all hosts en desarrollo para testing
ALLOWED_HOSTS = ['*'] if DEBUG else ALLOWED_HOSTS


# ========================================
# AUTO RELOAD
# ========================================

# Auto-reload en cambios de código
FILE_CHANGED_HANDLER = 'django.utils.autoreload.reload_code'


# ========================================
# DATABASE (Development)
# ========================================

# Usar SQLite por defecto en desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ========================================
# REST FRAMEWORK (Development)
# ========================================

# Configurar DRF para desarrollo
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]

REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = 'rest_framework.pagination.PageNumberPagination'
REST_FRAMEWORK['PAGE_SIZE'] = 20


# ========================================
# FIREBASE (Development - Emulator)
# ========================================

FIREBASE_USE_EMULATOR = True
FIREBASE_EMULATOR_HOST = 'localhost:8080'
FIREBASE_AUTH_EMULATOR_HOST = 'localhost:9099'


# ========================================
# SOLANA (Development - Localnet)
# ========================================

SOLANA_RPC_URL = 'http://127.0.0.1:8899'


# ========================================
# RATE LIMITING (Development - Disabled)
# ========================================

RATELIMIT_ENABLE = False
