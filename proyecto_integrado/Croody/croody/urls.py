"""Rutas principales del proyecto Croody.

P1 (i18n): mantener `/` y `/admin/` sin prefijo
-----------------------------------------------------------------
Implementamos la variante recomendada: se definen rutas sin prefijo
para el idioma por defecto y, además, un bloque con `i18n_patterns`
con `prefix_default_language=False` para servir también con prefijo
de idioma (p. ej. `/es/`). Esto evita `Resolver404` al resolver `'/'`
y mantiene la compatibilidad con las rutas prefijadas.
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path


# Rutas sin prefijo (idioma por defecto)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),  # sin prefijo
    path('dashboard/', include('telemetry.urls')),
    path('', include('landing.urls', namespace='landing')),  # home sin prefijo
    path('tienda/', include('shop.urls', namespace='shop')),
]

# Rutas con prefijo para idiomas distintos al por defecto
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('dashboard/', include('telemetry.urls')),
    path('', include('landing.urls', namespace='landing')),
    path('tienda/', include('shop.urls', namespace='shop')),
    prefix_default_language=False,  # clave para mantener / y /admin/ sin prefijo
)
