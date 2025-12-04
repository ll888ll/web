"""Configuración de producción para Croody.

Esta configuración está optimizada para deployment en AWS ECS.
Requiere variables de entorno configuradas en AWS Systems Manager o Secrets Manager.
"""
from .base import *

import os


# ========================================
# CORE SETTINGS (Production)
# ========================================

DEBUG = False

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv('ALLOWED_HOSTS', 'croody.app,*.croody.app').split(',')
    if h.strip()
]

# ========================================
# SECURITY (Hardened)
# ========================================

# HSTS
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# SSL
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'false').lower() == 'true'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Additional security headers
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# ========================================
# DATABASE (Production)
# ========================================

# RDS PostgreSQL Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'croody'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
        'OPTIONS': {
            'sslmode': os.getenv('DB_SSL_MODE', 'require'),
            'connect_timeout': 10,
        },
    }
}

# Override with DATABASE_URL if provided (Heroku-style)
import dj_database_url
if os.getenv('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=os.getenv('DB_SSL_REQUIRE', 'false').lower() == 'true',
    )

# ========================================
# STATIC FILES (Production)
# ========================================

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Allow CDN
WHITENOISE_KEEP_ONLY_HASHED_FILES = True

# ========================================
# LOGGING (Production)
# ========================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{asctime} [{levelname}] {name} {module}.{funcName}:{lineno} - {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'croody': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# ========================================
# CACHING (Production)
# ========================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://localhost:6379/1'),
        'KEY_PREFIX': 'croody_',
        'TIMEOUT': 300,
    }
}

# ========================================
# SESSION (Production)
# ========================================

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 86400  # 1 día
SESSION_COOKIE_SAMESITE = 'Lax'

# ========================================
# EMAIL (Production)
# ========================================

# Configurar SES o servicio de email
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = os.getenv('AWS_SES_REGION_NAME', 'us-east-1')
AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@croody.app')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ========================================
# MONITORING (Production)
# ========================================

# Integración con CloudWatch
if os.getenv('ENABLE_CLOUDWATCH', 'false').lower() == 'true':
    INSTALLED_APPS.append('watchtower')

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'watchtower.CloudWatchLogHandler',
                'level': 'INFO',
            },
        },
        'root': {
            'handlers': ['console'],
        },
    }

# ========================================
# CELERY (Si se usa)
# ========================================

if os.getenv('USE_CELERY', 'false').lower() == 'true':
    INSTALLED_APPS.append('celery')

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE

# ========================================
# PERFORMANCE (Production)
# ========================================

# Comprimir responses
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# ========================================
# HEALTH CHECKS
# ========================================

HEALTH_CHECK = {
    'DISK_USAGE_MAX': 90,  # porcentaje
    'MEMORY_MIN': 100,  # MB
    'DISK_MIN': 1000,  # MB
}
