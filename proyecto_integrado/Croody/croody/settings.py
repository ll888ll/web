"""Configuración principal del proyecto Croody.

IMPORTANTE: Este archivo mantiene compatibilidad hacia atrás.
Para configuraciones específicas de entorno, usa:
- DJANGO_SETTINGS_MODULE=croody.settings.development
- DJANGO_SETTINGS_MODULE=croody.settings.production

Por defecto usa la configuración de desarrollo.
"""
# Importar configuración desde la estructura modular
from .settings.base import *  # noqa
