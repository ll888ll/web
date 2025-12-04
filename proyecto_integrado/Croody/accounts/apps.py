"""Configuración de la app accounts."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    """Configuración del ecosistema post-login de Croody."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = _('Cuentas de Usuario')

    def ready(self):
        """Importa signals cuando la app está lista."""
        # Los signals están definidos en models.py
        pass
