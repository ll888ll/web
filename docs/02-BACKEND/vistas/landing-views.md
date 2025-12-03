# Vistas Landing - Documentación Completa

## Resumen
Las vistas de la aplicación Landing manejan la página principal, información corporativa, productos Buddy/Luks, autenticación y gestión de perfil de usuario. Implementan Class-Based Views (CBV) con mixins reutilizables.

## Ubicación
`/proyecto_integrado/Croody/landing/views.py`

## Vistas Principales

### 1. HomeView - Página Principal

**Herencia:**
```python
class HomeView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/home.html'
```

**Responsabilidades:**
- Página de inicio del ecosistema Croody
- Hero section con llamadas a la acción
- Métricas del producto
- Vector cards (Buddy, Luks, Comida Real)
- Principios de diseño
- Roadmap por fases

**Context Data:**
```python
def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
        hero=hero,              # Datos del hero
        metrics=metrics,        # Métricas de negocio
        vectors=vectors,        # Buddy, Luks, Comida Real
        principles=principles,  # Principios de diseño
        phases=phases,          # Roadmap fases
        products=get_sample_products(),  # Productos destacados
        brand='gator',          # Marca: gator, crimson, gold
    )
    return context
```

**URL:** `/` (raíz)

**Template:** `landing/home.html`

**Mixins aplicados:**
- `LandingNavigationMixin`: Inyecta navegación y búsqueda global

### 2. AboutView - Página Nosotros

**Herencia:**
```python
class AboutView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/about.html'
```

**URL:** `/nosotros/`

**Características:**
- Información corporativa
- Equipo
- Misión y visión
- Historia del proyecto

### 3. BuddyView - Producto Buddy

**Herencia:**
```python
class BuddyView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/buddy.html'
```

**URL:** `/buddy/`

**Características:**
- Información del producto AI de fitness
- Beneficios y características
- Roadmap del producto
- Marca: `crimson` (tema rojo)

### 4. LuksView - Producto Luks

**Herencia:**
```python
class LuksView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/luks.html'
```

**URL:** `/luks/`

**Características:**
- Información de la economía digital
- Token y blockchain
- Casos de uso
- Marca: `gold` (tema dorado)

### 5. IntegrationsView - Integraciones

**Herencia:**
```python
class IntegrationsView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/integrations.html'
```

**URL:** `/integraciones/`

**Características:**
- APIs disponibles
- Webhooks
- SDKs
- Documentación técnica

### 6. CroodyLoginView - Autenticación

**Herencia:**
```python
class CroodyLoginView(LandingNavigationMixin, LoginView):
    template_name = 'account/login.html'
```

**URL:** `/cuenta/acceder/`

**Formulario:** `CroodyLoginForm`

**Características:**
- Login con email o username
- Widgets personalizados
- Validación de credenciales
- Redirección post-login

**Validaciones:**
```python
def clean(self):
    cleaned_data = super().clean()
    username = cleaned_data.get('username')

    # Permite login con email
    if username and '@' in username:
        try:
            user = User.objects.get(email__iexact=username)
            cleaned_data['username'] = user.get_username()
        except User.DoesNotExist:
            pass

    return cleaned_data
```

### 7. CroodySignupView - Registro

**Herencia:**
```python
class CroodySignupView(LandingNavigationMixin, SignupView):
    template_name = 'account/register.html'
    form_class = CroodySignupForm
```

**URL:** `/cuenta/registro/`

**Características:**
- Registro con email
- Validación de contraseña
- Creación automática de UserProfile
- Redirección post-registro

**Flujo:**
1. Usuario completa formulario
2. Validación de email único
3. Generación de username único
4. Creación de User
5. Señal crea UserProfile automáticamente
6. Login automático y redirección

### 8. ProfileView - Gestión de Perfil

**Herencia:**
```python
class ProfileView(LoginRequiredMixin, LandingNavigationMixin, TemplateView):
    template_name = 'account/profile.html'
```

**URL:** `/cuenta/perfil/`

**Formularios soportados:**
- `ProfileForm` - Datos de usuario
- `ProfilePreferencesForm` - Preferencias
- `TokenResetForm` - Regenerar token

**Manejo Multi-Form:**
```python
def post(self, request, *args, **kwargs):
    user = request.user
    profile = user.profile  # type: ignore[attr-defined]
    form_name = request.POST.get('form')

    if form_name == 'profile':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Perfil actualizado.'))
            return redirect('landing:profile')

    elif form_name == 'preferences':
        form = ProfilePreferencesForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Preferencias actualizadas.'))
            return redirect('landing:profile')

    elif form_name == 'token_reset':
        form = TokenResetForm(request.POST)
        if form.is_valid():
            old_token = profile.ingest_token
            profile.regenerate_token()
            profile.save()

            # Log de auditoría
            logger.info(
                f"Token regenerated for user {user.username}. "
                f"Old: {old_token[:8]}..., New: {profile.ingest_token[:8]}..."
            )
            messages.success(request, _('Token regenerado correctamente.'))
            return redirect('landing:profile')

    # Re-render con errores
    return self.get(request, *args, **kwargs)
```

**Context Data:**
```python
def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    user = self.request.user
    profile = user.profile  # type: ignore[attr-defined]

    context = super().get_context_data(**kwargs)
    context.update(
        profile_form=ProfileForm(instance=user),
        preferences_form=ProfilePreferencesForm(instance=profile),
        token_form=TokenResetForm(),
        brand='gator',
    )
    return context
```

### 9. TokenResetView - Regenerar Token

**Herencia:**
```python
class TokenResetView(LoginRequiredMixin, FormView):
    template_name = 'account/token_reset.html'
    form_class = TokenResetForm
    success_url = reverse_lazy('landing:profile')
```

**URL:** `/cuenta/token/reset/`

**Propósito:** Vista dedicada para regeneración de token (puede ser accesada directamente o via ProfileView).

## Mixins Utilizados

### LandingNavigationMixin

```python
class LandingNavigationMixin:
    """Inyecta navegación y búsqueda en contexto."""

    def get_nav_links(self) -> list[dict[str, str]]:
        """Retorna links de navegación principal."""
        return primary_nav_links()

    def get_search_results(self) -> list[dict[str, str]]:
        """Retorna entradas para búsqueda global."""
        return global_search_entries()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Inyecta navegación en contexto."""
        context = super().get_context_data(**kwargs)
        context.setdefault('nav_links', self.get_nav_links())
        context.setdefault('search_results', self.get_search_results())
        return context
```

**Usado por:**
- HomeView
- AboutView
- BuddyView
- LuksView
- ProfileView

### Patrón de Uso

```python
# Definir una vista
class MiVista(LandingNavigationMixin, TemplateView):
    template_name = 'mi_template.html'
    brand = 'crimson'  # Opcional: cambiar marca

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mi_dato'] = 'valor'
        return context
```

## Context Data Injection

### Ejemplo Completo
```python
def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    # 1. Llamar a super() para obtener contexto base
    context = super().get_context_data(**kwargs)

    # 2. Agregar datos específicos de la vista
    context.update({
        'hero': {
            'title': 'Volvamos a ser humanos',
            'subtitle': 'Conecta con tecnología humanizada',
            'cta_primary': 'Ir a la Tienda',
            'cta_secondary': 'Ver Buddy'
        },
        'metrics': {
            'routines_adjusted': '1.2k+',
            'retention_rate': '92%',
            'regions': '7'
        },
        'brand': getattr(self, 'brand', 'gator'),
    })

    # 3. Retornar contexto completo
    return context
```

## Configuración de URLs

### landing/urls.py
```python
from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    # Páginas públicas
    path('', views.HomeView.as_view(), name='home'),
    path('nosotros/', views.AboutView.as_view(), name='about'),
    path('buddy/', views.BuddyView.as_view(), name='buddy'),
    path('luks/', views.LuksView.as_view(), name='luks'),
    path('integraciones/', views.IntegrationsView.as_view(), name='integrations'),

    # Autenticación
    path('cuenta/acceder/', views.CroodyLoginView.as_view(), name='login'),
    path('cuenta/registro/', views.CroodySignupView.as_view(), name='signup'),
    path('cuenta/salir/', LogoutView.as_view(), name='logout'),

    # Perfil
    path('cuenta/perfil/', views.ProfileView.as_view(), name='profile'),
    path('cuenta/token/reset/', views.TokenResetView.as_view(), name='token_reset'),
]
```

## Templates

### Estructura Base
```django
{# landing/home.html #}
{% extends 'base.html' %}

{% block title %}
  {% trans 'Croody · Diseño con propósito' %}
{% endblock %}

{% block meta_description %}
  {% trans 'Croody conecta personas con tecnología humanizada para un futuro mejor.' %}
{% endblock %}

{% block body %}
  {# Hero Section #}
  <section class="landing-hero">
    <div class="container">
      <h1>{{ hero.title }}</h1>
      <p>{{ hero.subtitle }}</p>
      <div class="cta-group">
        <a href="{% url 'shop:catalogue' %}" class="btn btn-primary">
          {{ hero.cta_primary }}
        </a>
        <a href="{% url 'landing:buddy' %}" class="btn btn-secondary">
          {{ hero.cta_secondary }}
        </a>
      </div>
    </div>
  </section>

  {# Metrics Section #}
  <section class="metrics">
    <div class="metric">
      <span class="number">{{ metrics.routines_adjusted }}</span>
      <span class="label">rutinas ajustadas automáticamente cada semana</span>
    </div>
    <div class="metric">
      <span class="number">{{ metrics.retention_rate }}</span>
      <span class="label">personas mantienen su plan mensual</span>
    </div>
    <div class="metric">
      <span class="number">{{ metrics.regions }}</span>
      <span class="label">regiones de operación sincronizada</span>
    </div>
  </section>
{% endblock %}
```

## Testing

### Unit Tests
```python
# tests/unit/views/test_landing.py
from django.test import Client, RequestFactory
from django.contrib.auth.models import User
from landing.views import HomeView

class TestHomeView:
    def test_get_context_data(self):
        """Test inyección de contexto."""
        factory = RequestFactory()
        request = factory.get('/')
        view = HomeView()
        view.setup(request)

        context = view.get_context_data()

        assert 'nav_links' in context
        assert 'hero' in context
        assert 'metrics' in context
        assert 'vectors' in context
        assert context['brand'] == 'gator'

    def test_homepage_loads(self, client):
        """Test carga de homepage."""
        response = client.get(reverse('landing:home'))
        assert response.status_code == 200
        assert b'Volvamos a ser humanos' in response.content

    def test_i18n_english(self, client):
        """Test traducción en inglés."""
        response = client.get('/en/')
        assert response.status_code == 200
        assert b'Let\'s be human again' in response.content
```

### Integration Tests
```python
# tests/integration/test_auth_flow.py
from django.urls import reverse

class TestAuthenticationFlow:
    def test_login_and_logout(self, client):
        # Crear usuario
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Login
        response = client.post(
            reverse('landing:login'),
            {
                'username': 'testuser',
                'password': 'testpass123'
            },
            follow=True
        )
        assert response.redirect_chain[0][0] == reverse('landing:home')

        # Logout
        response = client.post(reverse('landing:logout'), follow=True)
        assert response.redirect_chain[0][0] == reverse('landing:home')

    def test_signup_creates_profile(self, client):
        """Test que signup crea UserProfile automáticamente."""
        response = client.post(
            reverse('landing:signup'),
            {
                'email': 'newuser@example.com',
                'password': 'securepass123',
                'confirm_password': 'securepass123',
                'full_name': 'Test User',
                'preferred_language': 'es',
                'preferred_theme': 'dark',
                'accept_terms': True
            },
            follow=True
        )

        # Verificar que usuario fue creado
        user = User.objects.get(email='newuser@example.com')
        assert user.check_password('securepass123')

        # Verificar que profile fue creado
        assert hasattr(user, 'profile')
        assert user.profile.preferred_language == 'es'
        assert user.profile.preferred_theme == 'dark'
```

## Configuraciones

### Settings.py Relevantes

```python
# Configuración de login
LOGIN_URL = reverse_lazy('landing:login')
LOGIN_REDIRECT_URL = reverse_lazy('shop:catalogue')
LOGOUT_REDIRECT_URL = reverse_lazy('landing:home')
```

### Middleware Aplicado

```python
MIDDLEWARE = [
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # i18n
    'django.middleware.common.CommonMiddleware',
    # ...
]
```

## Performance

### 1. Cache de Contexto
```python
from django.core.cache import cache

def get_context_data(self, **kwargs):
    cache_key = f'landing_context_{self.request.LANGUAGE_CODE}'
    context = cache.get(cache_key)

    if not context:
        context = {
            'hero': get_hero_data(),
            'metrics': get_metrics(),
            'vectors': get_vectors(),
        }
        cache.set(cache_key, context, 300)  # 5 minutos

    context.update(super().get_context_data(**kwargs))
    return context
```

### 2. Prefetch de Datos
```python
def get_context_data(self, **kwargs):
    # Datos que no cambian frecuentemente
    hero = HeroData.objects.filter(is_active=True).first()
    metrics = get_cached_metrics()

    context = super().get_context_data(**kwargs)
    context.update({
        'hero': hero,
        'metrics': metrics,
    })
    return context
```

### 3. Lazy Loading
```python
def get_context_data(self, **kwargs):
    # Solo cargar productos si es necesario
    include_products = self.request.GET.get('include_products', False)

    context = super().get_context_data(**kwargs)

    if include_products:
        context['products'] = Product.objects.published()[:12]

    return context
```

## Seguridad

### 1. Validación de Entrada
```python
def post(self, request, *args, **kwargs):
    # Validar CSRF
    if not request.POST.get('csrfmiddlewaretoken'):
        return HttpResponseBadRequest("CSRF token missing")

    # Validar formularios
    form_name = request.POST.get('form')
    if form_name not in ['profile', 'preferences', 'token_reset']:
        return HttpResponseBadRequest("Invalid form")

    # ... resto del código
```

### 2. Rate Limiting
```python
from django.core.cache import cache

def post(self, request, *args, **kwargs):
    # Rate limiting: 5 attempts per minute
    ip = request.META.get('REMOTE_ADDR')
    key = f'profile_update_rate:{ip}'

    attempts = cache.get(key, 0)
    if attempts >= 5:
        return JsonResponse(
            {'error': 'Too many attempts. Please try again later.'},
            status=429
        )

    cache.set(key, attempts + 1, 60)

    # ... resto del código
```

### 3. Logging de Auditoría
```python
def post(self, request, *args, **kwargs):
    user = request.user

    # Log antes de modificar
    logger.info(
        f"Profile update initiated by {user.username}",
        extra={
            'user_id': user.id,
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT')
        }
    )

    # ... procesamiento ...

    # Log después de éxito
    logger.info(f"Profile updated successfully for {user.username}")
```

## Mejores Prácticas

### 1. Separación de Responsabilidades
```python
# Bad: Vista hace demasiado
class BadHomeView(View):
    def get(self, request):
        # Procesar lógica de negocio
        products = Product.objects.all()
        # Hacer cálculos
        metrics = calculate_metrics()
        # Renderizar
        return render(request, 'home.html')

# Good: Usar métodos separados
class GoodHomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_products()
        context['metrics'] = self.get_metrics()
        return context

    def get_products(self):
        return Product.objects.published()[:12]

    def get_metrics(self):
        return get_cached_metrics()
```

### 2. Reutilización con Mixins
```python
# Usar mixins para funcionalidad común
class DataMixin:
    """Mixin para datos comunes."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['common_data'] = get_common_data()
        return context

class MyView(DataMixin, TemplateView):
    template_name = 'my_template.html'
```

### 3. Type Hints
```python
from typing import Any, Dict

class MyView(TemplateView):
    template_name = 'my_template.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Retorna contexto tipado."""
        return {
            'data': 'value'
        }
```

## Referencias

### Archivos Relacionados
- `landing/models.py` - UserProfile
- `landing/forms.py` - Formularios
- `landing/urls.py` - Configuración de rutas
- `landing/navigation.py` - Helpers de navegación

### Documentación Externa
- [Django Class-Based Views](https://docs.djangoproject.com/en/stable/topics/class-based-views/)
- [Django LoginView](https://docs.djangoproject.com/en/stable/topics/auth/default/#django.contrib.auth.views.LoginView)
- [Django SignupView](https://django-allauth.readthedocs.io/en/latest/views.html#signup)

## Ver También
- [UserProfile](../modelos/userprofile.md)
- [Formularios Landing](../formularios.md)
- [Navegación Global](./navigation.md)
- [Internationalization](../../07-INTERNACIONALIZACION/sistema-traduccion.md)
