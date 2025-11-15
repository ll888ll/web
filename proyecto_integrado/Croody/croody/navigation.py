"""Utilidades de navegación global de Croody."""
from __future__ import annotations

from typing import List

from django.urls import reverse
from django.utils.translation import gettext as _


def primary_nav_links() -> List[dict[str, str]]:
    """Links principales usados en cabecera y drawer."""
    home_url = reverse('landing:home')
    return [
        {'label': _('Buddy'), 'url': reverse('landing:buddy')},
        {'label': _('Luks'), 'url': reverse('landing:luks')},
        {'label': _('Tienda'), 'url': reverse('shop:catalogue')},
        {'label': _('Integraciones'), 'url': reverse('landing:integrations')},
        {'label': _('Monitor en vivo'), 'url': reverse('landing:monitor')},
    ]


def global_search_entries() -> List[dict[str, str]]:
    """Resultados rápidos para el buscador del header."""
    home_url = reverse('landing:home')
    return [
        {'label': _('Croody · Inicio'), 'url': home_url, 'fragment': 'hero'},
        {'label': _('Croody · Ejes'), 'url': home_url, 'fragment': 'vectores'},
        {'label': _('Croody · Roadmap'), 'url': home_url, 'fragment': 'roadmap'},
        {'label': _('Buddy · Producto'), 'url': reverse('landing:buddy')},
        {'label': _('Buddy · Suscripciones'), 'url': reverse('landing:buddy-suscripciones')},
        {'label': _('Luks · Infraestructura'), 'url': reverse('landing:luks')},
        {'label': _('Tienda Buddy'), 'url': reverse('shop:catalogue'), 'fragment': 'tienda-home'},
        {'label': _('Buddy Checkout'), 'url': reverse('shop:checkout-preview')},
        {'label': _('Croody · Registro'), 'url': reverse('landing:signup')},
        {'label': _('Croody · Perfil'), 'url': reverse('landing:profile')},
        {'label': _('Monitor en vivo'), 'url': reverse('landing:monitor')},
    ]
