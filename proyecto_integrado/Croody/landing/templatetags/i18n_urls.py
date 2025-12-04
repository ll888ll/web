"""Template tags for internationalized URLs."""
from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.translation import get_language

register = template.Library()

# Cache of language codes
LANG_CODES = {lang[0] for lang in settings.LANGUAGES}


def _add_lang_prefix(url: str) -> str:
    """Internal helper to add language prefix to URL."""
    lang = get_language()

    # Don't prefix for default language
    if lang == settings.LANGUAGE_CODE:
        return url

    # Don't prefix if URL already has a language prefix
    if url.startswith('/'):
        parts = url.split('/')
        if len(parts) > 1 and parts[1] in LANG_CODES:
            return url

    # Add language prefix
    if url.startswith('/'):
        return f'/{lang}{url}'
    return f'/{lang}/{url}'


@register.simple_tag(takes_context=True)
def localized_url(context, url):
    """Add language prefix to URL if not default language.

    Usage: {% localized_url url %}
    """
    return _add_lang_prefix(url)


@register.filter
def add_lang_prefix(url):
    """Filter version of localized_url.

    Usage: {{ url|add_lang_prefix }}
    """
    return _add_lang_prefix(url)


@register.simple_tag
def lang_url(url_name, *args, **kwargs):
    """Generate a URL with language prefix.

    Usage: {% lang_url 'landing:home' %}
           {% lang_url 'shop:product' slug='my-product' %}
    """
    url = reverse(url_name, args=args, kwargs=kwargs)
    return _add_lang_prefix(url)
