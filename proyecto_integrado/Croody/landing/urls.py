"""Rutas del módulo landing."""
from django.urls import path

from .views import (
    BuddyView,
    CroodyLoginView,
    CroodyLogoutView,
    CroodySignupView,
    HomeView,
    LuksView,
    RobotMonitorView,
    SuscripcionesView,
    IntegrationsView,
    ProfileView,
)


app_name = 'landing'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('buddy/', BuddyView.as_view(), name='buddy'),
    path('buddy/suscripciones/', SuscripcionesView.as_view(), name='buddy-suscripciones'),
    path('luks/', LuksView.as_view(), name='luks'),
    path('integraciones/', IntegrationsView.as_view(), name='integrations'),
    path('cuenta/acceder/', CroodyLoginView.as_view(), name='login'),
    path('cuenta/salir/', CroodyLogoutView.as_view(), name='logout'),
    path('cuenta/registro/', CroodySignupView.as_view(), name='signup'),
    path('cuenta/perfil/', ProfileView.as_view(), name='profile'),
    path('robots/monitor/', RobotMonitorView.as_view(), name='monitor'),
]
