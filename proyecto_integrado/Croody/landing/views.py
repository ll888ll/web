"""Vistas del módulo landing."""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, FormView

from croody.navigation import global_search_entries, primary_nav_links
from landing.forms import (
    CroodyLoginForm,
    CroodySignupForm,
    ProfileForm,
    ProfilePreferencesForm,
    TokenResetForm,
)
from shop.models import Product
from .models import UserProfile


class LandingNavigationMixin:
    """Inyecta navegación primaria y resultados de búsqueda global."""

    def get_nav_links(self) -> list[dict[str, str]]:
        return primary_nav_links()

    def get_search_results(self) -> list[dict[str, str]]:
        return global_search_entries()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        context.setdefault('nav_links', self.get_nav_links())
        show_shortcuts = context.get('show_global_shortcuts', False)
        context['show_global_shortcuts'] = show_shortcuts
        context['search_results'] = self.get_search_results() if show_shortcuts else []
        # Marca por defecto (Home) y otras páginas que no lo sobreescriban
        context.setdefault('brand', 'gator')
        return context


class AboutView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/about.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            page_title=_('Nosotros'),
        )
        return context


class HomeView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Demostrar funcionalidad de búsqueda global en landing
        context['show_global_shortcuts'] = True

        hero = {
            'eyebrow': _('Buddy AI · Entrena, Progresa, Destaca'),
            'title': _('Tu entrenador AI personal'),
            'lead': _(
                'Rutinas que se adaptan a ti. Recompensas que te motivan. La tecnología que conecta.'
            ),
            'primary_cta': {'label': _('🛒 Ir a la Tienda'), 'url': reverse('shop:catalogue')},
            'secondary_cta': {'label': _('Ver Buddy'), 'url': reverse('landing:buddy')},
            'tertiary_cta': {'label': _('💎 Luks'), 'url': reverse('landing:luks')},
            'image': {
                'src': 'img/logo-main.png',
                'alt': _('Croody - Tecnología que conecta'),
            },
        }

        metrics = [
            {'value': '1.2k+', 'caption': _('rutinas ajustadas automáticamente cada semana')},
            {'value': '92%', 'caption': _('personas mantienen su plan mensual con Buddy activo')},
            {'value': _('7 regiones'), 'caption': _('operación sincronizada con soporte localizado')},
        ]

        vectors = [
            {
                'badge': _('Fitness & Conexión'),
                'title': _('Buddy'),
                'copy': _('Una aplicación intuitiva, simétrica, de alta estética y gran fluidez, diseñada para que tanto quien ya entrena como quien apenas empieza encuentre cada día un porqué claro para construir el físico y los hábitos de salud de sus sueños. Conecta con tus amigos, entrena juntos y destaca.'),
                'cta_label': _('Conecta, Entrena y Destaca'),
                'url': reverse('landing:buddy'),
                'keywords': _('Conecta, Entrena y Destaca'),
            },
            {
                'badge': _('Economía Digital'),
                'title': _('My Luks'),
                'copy': _('Creamos un mercado con el cual puedes de forma segura incursionar en el mundo cripto, obtener ingresos extra y apoyarte en divisas que no dependen de una política interna de tu país y prosperar incluso en los entornos hostiles por decisiones de gobiernos.'),
                'cta_label': _('Seguridad, Abundancia y Proyección'),
                'url': reverse('landing:luks'),
                'keywords': _('Seguridad, Abundancia y Proyección'),
            },
            {
                'badge': _('Alimentación Real'),
                'title': _('Comida Real (Próximamente)'),
                'copy': _('A través de investigación y compromiso alimenticio ofrecemos comida real y soluciones eficaces para aquellos que se quieren alimentar bien y carecen de tiempo, para todas las edades. Promovemos alimentos de origen animal y vegetal, sin productos químicos dañinos.'),
                'cta_label': _('Alivio, Nostalgia y Satisfacción'),
                'url': '#',
                'keywords': _('Alivio, Nostalgia y Satisfacción'),
            },
        ]

        principles = [
            {
                'title': 'Claridad en cada decisión',
                'description': 'Interfaces limpias, métricas visibles y lenguaje directo para que cualquier equipo entienda qué sigue.',
            },
            {
                'title': 'Motivación sostenible',
                'description': 'Personajes, mensajes y animaciones que elevan la energía sin perder profesionalismo.',
            },
            {
                'title': 'Economía justa',
                'description': 'Probabilidades, tarifas y recompensas públicas. Sin sorpresas ni ventajas pay-to-win.',
            },
            {
                'title': 'Accesibilidad real',
                'description': 'Soporte total a teclado, contraste AA/AAA y narrativa pensada para distintas culturas y edades.',
            },
            {
                'title': 'Vocación de servicio',
                'description': 'Nos guía una ética de servicio discreta: cuidamos a las personas primero y dejamos que el diseño lo haga evidente.',
            },
        ]

        blueprint_highlights = [
            {
                'title': 'Compras sin fricción',
                'details': 'Checkout Luks en segundos con costos claros y asignación inmediata al inventario.',
            },
            {
                'title': 'Inventario conectado',
                'details': 'Abre packs, equipa rutinas o lista ítems desde web y móvil con el mismo estado.',
            },
            {
                'title': 'Eventos que mueven',
                'details': 'Temporadas y recompensas tokenizadas con métricas claras para sostener la constancia.',
            },
        ]

        roadmap = [
            {
                'badge': 'Semana 1',
                'title': 'Narrativa alineada',
                'points': [
                    'Landing Croody con la historia Buddy + Luks lista para stakeholders.',
                    'Formularios conectados y analítica básica para medir interés desde el día uno.',
                ],
            },
            {
                'badge': 'Semana 3',
                'title': 'Ventas activas',
                'points': [
                    'Catálogo, PDP y checkout Luks operando con seguimiento de conversiones.',
                    'Inventario y marketplace en beta controlada para refinar procesos.',
                ],
            },
            {
                'badge': 'Semana 6',
                'title': 'Expansión tokenizada',
                'points': [
                    'Eventos temáticos con recompensas en vivo y retos medidos en paneles de datos.',
                    'Dashboard de datos listo para alianzas y marcas aliadas.',
                ],
            },
        ]

        buddy_products = list(
            Product.objects.filter(is_published=True)
            .order_by('sort_order', 'name')
            .values('name', 'slug', 'teaser', 'price', 'delivery_estimate', 'badge_label')[:3]
        )
        if not buddy_products:
            buddy_products = [
                {
                    'name': 'Pack Buddy Starter',
                    'slug': 'buddy-starter',
                    'teaser': 'Incluye rutina Wimpy, guía de movilidad y acceso a la biblioteca de ejercicios.',
                    'price': Decimal('79.00'),
                    'delivery_estimate': 'Activación inmediata',
                    'badge_label': 'Starter',
                },
                {
                    'name': 'Set Atmos Green',
                    'slug': 'set-atmos-green',
                    'teaser': 'Tema completo con música, animaciones y retos comunitarios para mantener la motivación.',
                    'price': Decimal('129.00'),
                    'delivery_estimate': 'Entrega digital 24h',
                    'badge_label': 'Temporada',
                },
                {
                    'name': 'Accesorios Pulse Pack',
                    'slug': 'accesorios-pulse-pack',
                    'teaser': 'Accesorios equipables con telemetría en vivo y recompensas Luks por constancia.',
                    'price': Decimal('54.00'),
                    'delivery_estimate': 'Entrega 48h',
                    'badge_label': 'Recompensa',
                },
            ]

        context.update(
            hero=hero,
            metrics=metrics,
            vectors=vectors,
            principles=principles,
            blueprint_highlights=blueprint_highlights,
            roadmap=roadmap,
            buddy_products=buddy_products,
        )
        return context


class BuddyView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/buddy.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Demostrar funcionalidad de búsqueda global en Buddy
        context['show_global_shortcuts'] = True
        hero = {
            'eyebrow': _('Buddy · Conecta, Entrena y Destaca'),
            'title': _('Más que entrenar: una conexión contigo y con los tuyos'),
            'lead': _(
                'Buddy es una aplicación intuitiva, simétrica, de alta estética y gran fluidez, diseñada para que tanto quien ya entrena en un gimnasio como quien apenas empieza a considerar la idea encuentre, cada día, un porqué claro para enfocarse y construir el físico y los hábitos de salud de sus sueños. Además de verse y sentirse bien, Buddy cuida que la experiencia sea coherente, agradable y profundamente motivadora desde el primer contacto, con una ética inspirada en nuestras convicciones de servicio que priorizan el cuidado de las personas.'
            ),
            'primary_cta': {'label': _('Ir a la tienda Buddy'), 'url': reverse('shop:catalogue')},
            'secondary_cta': {'label': _('Ver roadmap'), 'fragment': 'buddy-roadmap'},
        }
        metrics = [
            {'value': _('365 días'), 'caption': _('de rutinas nuevas sin reciclar combinaciones')},
            {'value': _('±5% fatiga'), 'caption': _('ajuste automático según tu energía real')},
            {'value': _('5 estilos'), 'caption': _('personajes con tonos y objetivos definidos')},
        ]
        pillars = [
            {
                'title': _('Entrenador con IA y rutinas a tu medida'),
                'description': _('Buddy ofrece la oportunidad de diseñar rutinas mediante un entrenador personalizado con IA. Cada semana recibes un plan de entrenamiento pensado exclusivamente para ti, basado en tus entrenamientos previos, datos e historial. La IA automatiza este proceso a través de conversaciones naturales, manteniendo siempre el control total de tu entrenamiento.'),
            },
            {
                'title': _('Biblioteca de ejercicios segura y consistente'),
                'description': _('Cada movimiento incluye video-claves cortos con la técnica correcta, pautas de respiración, puntos de seguridad y errores comunes a evitar. Con progresiones sugeridas (fácil/intermedia/avanzada), siempre tendrás una alternativa acorde a tu nivel y equipo disponible.'),
            },
            {
                'title': _('Ecosistema de personajes con carisma'),
                'description': _('Buddy cuenta con un ecosistema de personajes, cada uno con su personalidad única. Puedes elegir rutinas predeterminadas según el estilo de cada personaje o configurar que uno solo te entregue todas las rutinas. Cada personaje ofrece gestos, animaciones y apoyo constante para una experiencia cercana y estimulante.'),
            },
        ]
        modules = [
            {
                'title': 'App móvil',
                'items': [
                    'Diálogo natural para crear rutinas y ajustar bloques en segundos.',
                    'Conteo automático de series, descansos inteligentes y feedback háptico.',
                    'Modo compañero para entrenar con tus contactos o personaje favorito.',
                ],
            },
            {
                'title': 'Buddy Web',
                'items': [
                    'Inventario vivo para abrir packs, equipar sets y listar ítems.',
                    'Reproductor de sesiones, biblioteca extendida y guardado de favoritos.',
                    'Telemetría lista para equipos, coaches o marcas aliadas.',
                ],
            },
            {
                'title': 'Economía Buddy',
                'items': [
                    'Sets temáticos, accesorios y cofres con probabilidades públicas.',
                    'Luks como moneda única con recompensas por constancia y eventos.',
                    'Marketplace integrado para vender o intercambiar sin salir de Buddy.',
                ],
            },
        ]
        journeys = [
            {
                'title': 'Antes de entrenar',
                'items': [
                    'Escaneo rápido de energía y movilidad.',
                    'Recomendaciones de personajes, sets y accesorios según tu meta.',
                    'Recordatorios contextuales desde la app y sincronía con tus calendarios habituales.',
                ],
            },
            {
                'title': 'Durante la sesión',
                'items': [
                    'Conteo automático de repeticiones y control de tempo.',
                    'Feedback visual y de voz sobre técnica, respiración y seguridad.',
                    'Notas rápidas, clips y variaciones disponibles en un toque.',
                ],
            },
            {
                'title': 'Después del entrenamiento',
                'items': [
                    'Resumen claro con métricas, descanso sugerido y próximos pasos.',
                    'Recompensas Luks y retos desbloqueados según tu constancia.',
                    'Historial listo para compartir con tu entrenador o comunidad.',
                ],
            },
        ]
        roadmap = [
            {
                'label': 'Semana 1',
                'items': [
                    'Piloto interno con rutinas adaptativas y biblioteca completa.',
                    'Configuración de personajes base y mensajes personalizados.',
                ],
            },
            {
                'label': 'Semana 3',
                'items': [
                    'Inventario web conectado para abrir packs y equipar sets.',
                    'Alertas inteligentes en móvil y correo para mantener la constancia.',
                ],
            },
            {
                'label': 'Semana 6',
                'items': [
                    'Marketplace activo con recompensas y eventos temáticos.',
                    'Dashboard de telemetría para coaches, squads y marcas.',
                ],
            },
        ]
        context.update(
            hero=hero,
            metrics=metrics,
            pillars=pillars,
            modules=modules,
            journeys=journeys,
            roadmap=roadmap,
        )
        context['brand'] = 'crimson'
        return context


class IntegrationsView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/integrations.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            telemetry_last_endpoint='/api/telemetry/last',
            telemetry_ingest_endpoint='/api/telemetry/ingest',
            ids_predict_endpoint='/api/ids/predict',
            ids_model_endpoint='/api/ids/model',
        )
        return context


class LuksView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/luks.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Demostrar funcionalidad de búsqueda global en Luks
        context['show_global_shortcuts'] = True
        hero = {
            'eyebrow': 'Luks · Economía Buddy',
            'title': 'Token que recompensa la constancia y da confianza a cada transacción.',
            'lead': 'Pagos, royalties y telemetría on-chain con una experiencia diseñada para usuarios reales y equipos regulados. La infraestructura nace de principios de transparencia y servicio comunicados con un tono ejecutivo.',
            'primary_cta': {'label': 'Ver tienda Buddy', 'url': reverse('shop:catalogue')},
            'secondary_cta': {'label': 'Contactar equipo Luks', 'url': 'mailto:hola@croody.app?subject=Luks'},
        }
        metrics = [
            {'value': '≤2s', 'caption': 'finalidad promedio de las transacciones'},
            {'value': '99.9%', 'caption': 'disponibilidad de la bóveda custodial'},
            {'value': '100%', 'caption': 'catálogo con probabilidades visibles'},
        ]
        pillars = [
            {
                'title': 'Transparencia total',
                'items': [
                    'Probabilidades, tarifas y royalties visibles antes de confirmar.',
                    'Recibos con hash verificable y seguimiento en tu panel.',
                    'Historial público de drops especiales y ajustes de rareza.',
                ],
            },
            {
                'title': 'Seguridad por defecto',
                'items': [
                    'Custodia con 2FA, límites dinámicos y alertas en tiempo real.',
                    'Escrow inteligente y cooldowns para frenar especulación.',
                    'Monitoreo anti-bot y protección ante picos de red.',
                ],
            },
            {
                'title': 'Medición constante',
                'items': [
                    'Dashboards con conversión, listados y salud de la red.',
                    'Eventos trazables para campañas y recompensas por consistencia.',
                    'Exportación de datos para socios, auditorías y reguladores.',
                ],
            },
        ]
        economy = [
            {'title': 'Tienda Buddy', 'points': ['Checkout en segundos', 'Packs con pity visible', 'Asignación inmediata al inventario.']},
            {'title': 'Inventario web', 'points': ['Estados sincronizados', 'Listado instantáneo', 'Eventos y bonos por temporada.']},
            {'title': 'Marketplace P2P', 'points': ['Royalties configurables', 'Escrow automático', 'Historial de precios y volumen.']},
        ]
        compliance = [
            'KYC/AML opcional para límites de retiro elevados.',
            'Políticas anti loot-box con fiat: todo pasa primero por Luks.',
            'Age gate configurable y reportes regionales listos para reguladores.',
        ]
        integrations = [
            'SDK ligero para apps y gimnasios que quieran ofrecer recompensas Buddy.',
            'Webhooks firmados para sincronizar inventario con partners externos.',
            'Panel operativo con métricas de conversión, uso y salud de red.',
        ]
        context.update(
            hero=hero,
            metrics=metrics,
            pillars=pillars,
            economy=economy,
            compliance=compliance,
            integrations=integrations,
        )
        context['brand'] = 'gold'
        return context


class SuscripcionesView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/suscripciones.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)

        hero = {
            'eyebrow': 'Buddy · Suscripciones',
            'title': 'Elige un plan para empezar hoy',
            'lead': (
                'Planes simples que activan rutinas con IA, biblioteca de ejercicios y progreso vivo. '
                'Cámbialos o cancélalos cuando quieras.'
            ),
        }

        plans = [
            {
                'name': 'Starter',
                'price': '9.99',
                'period': 'mes',
                'features': [
                    'Rutinas con IA (básico)',
                    'Biblioteca de ejercicios con video‑claves',
                    'Progreso semanal y temporizador de descansos',
                ],
                'cta_label': 'Comenzar',
            },
            {
                'name': 'Focus',
                'price': '14.99',
                'period': 'mes',
                'features': [
                    'Rutinas con IA (avanzado)',
                    'Ajustes por personaje y objetivos',
                    'Recordatorios inteligentes y tendencias mensuales',
                ],
                'cta_label': 'Activar Focus',
                'badge': 'Recomendado',
            },
            {
                'name': 'Crew',
                'price': '29.99',
                'period': 'mes',
                'features': [
                    'Todo Focus + 3 perfiles',
                    'Retos y tableros para equipo/familia',
                    'Soporte prioritario',
                ],
                'cta_label': 'Probar Crew',
            },
        ]

        faq = [
            {
                'q': '¿Puedo cancelar cuando quiera?',
                'a': 'Sí, gestionas tu plan desde tu cuenta. Sin permanencias.',
            },
            {
                'q': '¿Qué incluye la prueba?',
                'a': '7 días con funciones Focus para que sientas el flujo completo.',
            },
        ]

        context['brand'] = 'crimson'
        context.update(hero=hero, plans=plans, faq=faq)
        return context


class CroodyLoginView(LandingNavigationMixin, LoginView):
    template_name = 'account/login.html'
    form_class = CroodyLoginForm
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return self.get_redirect_url() or reverse('shop:catalogue')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        context.setdefault('show_global_shortcuts', False)
        context['page_title'] = 'Inicia sesión'
        context['next_url'] = self.get_redirect_url() or reverse('shop:catalogue')
        context['signup_url'] = reverse('landing:signup')
        return context


class CroodyLogoutView(LogoutView):
    next_page = reverse_lazy('landing:home')


class CroodySignupView(LandingNavigationMixin, FormView):
    template_name = 'account/register.html'
    form_class = CroodySignupForm

    def get_success_url(self) -> str:
        return reverse('landing:profile')

    def form_valid(self, form: CroodySignupForm):  # type: ignore[override]
        user = form.save()
        login(self.request, user)
        messages.success(self.request, _('Bienvenido a Croody. Ajusta tu perfil cuando quieras.'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('brand', 'gator')
        ctx['page_title'] = _('Crear cuenta Croody')
        return ctx


class ProfileView(LoginRequiredMixin, LandingNavigationMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = user.profile  # type: ignore[attr-defined]
        context.update(
            profile_form=ProfileForm(instance=user),
            preferences_form=ProfilePreferencesForm(instance=profile),
            token_form=TokenResetForm(),
            ingest_token=profile.ingest_token,
            telemetry_live_endpoint='/api/telemetry/live',
            telemetry_query_endpoint='/api/telemetry/query',
            ingest_endpoint='/api/telemetry/ingest',
            activity_log=self._activity_log(profile),
        )
        return context

    def post(self, request, *args, **kwargs):  # type: ignore[override]
        form_name = request.POST.get('form')
        user = request.user
        profile = user.profile  # type: ignore[attr-defined]

        if form_name == 'profile':
            form = ProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, _('Perfil actualizado.'))
            else:
                messages.error(request, _('Revisa los campos del perfil.'))
        elif form_name == 'preferences':
            form = ProfilePreferencesForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, _('Preferencias guardadas.'))
            else:
                messages.error(request, _('No pudimos guardar las preferencias.'))
        elif form_name == 'token':
            profile.regenerate_token()
            messages.success(request, _('Generamos un nuevo token para tus robots.'))
        else:
            messages.error(request, _('Acción no reconocida.'))
        return self.get(request, *args, **kwargs)

    def _activity_log(self, profile: UserProfile) -> list[dict[str, str]]:
        return [
            {
                'title': _('Token de ingestión listo'),
                'subtitle': profile.ingest_token,
                'status': _('activo'),
            },
            {
                'title': _('Alertas de telemetría'),
                'subtitle': _('Recibir notificaciones críticas') if profile.telemetry_alerts else _('Alertas desactivadas'),
                'status': 'ok' if profile.telemetry_alerts else 'muted',
            },
        ]


class RobotMonitorView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/monitor.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx['show_global_shortcuts'] = True
        ctx['brand'] = 'gold'
        ctx['live_endpoint'] = '/api/telemetry/live'
        ctx['history_endpoint'] = '/api/telemetry/query'
        ctx['ingest_endpoint'] = '/api/telemetry/ingest'
        ctx['monitor_meta'] = {
            'hero': {
                'title': _('Monitoreo en tiempo real'),
                'lead': _('Visualiza la posición del robot, variables atmosféricas y estados críticos en un tablero neofuturista listo para operación global.'),
            },
            'metrics': [
                {'label': _('Robots activos'), 'value': '––', 'id': 'robot-count'},
                {'label': _('Última actualización'), 'value': '––', 'id': 'last-update'},
                {'label': _('Alertas'), 'value': '0', 'id': 'alert-count'},
            ],
        }
        ctx['robot_demo'] = {
            'id': 'robot-clases',
            'source_path': 'proyecto_integrado/robots/telemetry-robot',
            'protocol': _('TCP ASCII · LOGIN/GET_DATA/MOVE'),
            'frequency': _('Emite cada 15 s y el bridge envía a Telemetry Gateway automáticamente.'),
        }
        ctx['ids_model_meta'] = self._load_ids_model_meta()
        return ctx

    def _load_ids_model_meta(self) -> dict[str, Any] | None:
        meta_path = Path(settings.BASE_DIR) / 'services/ids-ml/models/model_metadata.json'
        if not meta_path.exists():
            return None
        try:
            data = json.loads(meta_path.read_text(encoding='utf-8'))
            data['evaluation_path'] = str(meta_path.parent / 'evaluation.txt')
            return data
        except Exception:
            return None
