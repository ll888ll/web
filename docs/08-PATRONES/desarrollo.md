# Patrones de Desarrollo - Documentación Completa

## Resumen
La arquitectura de desarrollo de Croody implementa patrones Django consolidados y mejores prácticas modernas: Class-Based Views (CBV) con mixins reutilizables, QuerySets personalizados con managers, signals para automatización, formularios tipados, type hints completos, y separación clara de responsabilidades por módulos. Utiliza patrones funcionales para inyección de contexto, composición de formularios, y generación automática de tokens.

## Ubicación
- **Models**: `/proyecto_integrado/Croody/landing/models.py`, `/proyecto_integrado/Croody/shop/models.py`
- **Views**: `/proyecto_integrado/Croody/landing/views.py`, `/proyecto_integrado/Croody/shop/views.py`
- **Forms**: `/proyecto_integrado/Croody/landing/forms.py`
- **Signals**: `/proyecto_integrado/Croody/landing/signals.py`
- **Apps**: `/proyecto_integrado/Croody/landing/apps.py`

## Arquitectura General

### Patrones Principales Implementados
```python
# 1. Model-View-Template (MVT) Pattern
Model (Datos) → View (Lógica) → Template (Presentación)

# 2. Class-Based Views con Mixins
class LandingNavigationMixin: ...
class HomeView(LandingNavigationMixin, TemplateView): ...

# 3. Custom QuerySet Managers
class ProductQuerySet(models.QuerySet):
    def published(self): ...
    def search(self, query: str): ...

# 4. Django Signals Pattern
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs): ...

# 5. Form Composition Pattern
class CroodySignupForm(UserCreationForm):
    custom_field = forms.CharField(...)
    def save(self, commit=True): ...

# 6. Type Hints Pattern
def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...
```

## Model Patterns

### 1. Custom QuerySet Managers

#### Pattern: QuerySet como Manager Personalizado
```python
# shop/models.py
class ProductQuerySet(models.QuerySet):
    """QuerySet personalizado para Product con métodos reutilizables."""

    def published(self) -> 'ProductQuerySet':
        """Filtra solo productos publicados."""
        return self.filter(is_published=True)

    def search(self, query: str) -> 'ProductQuerySet':
        """Búsqueda por nombre o descripción."""
        if not query:
            return self
        return self.filter(
            models.Q(name__icontains=query) |
            models.Q(teaser__icontains=query)
        )

class Product(models.Model):
    # ... campos ...
    objects = ProductQuerySet.as_manager()
```

#### Uso en Vistas
```python
# En vistas/shop/views.py o templates
products = Product.objects.published().search(query)
products = Product.objects.published().order_by('sort_order')
```

#### Beneficios
- **Reutilización**: Lógica de consulta centralizada
- **Chainability**: Métodos encadenables
- **Type Safety**: PyCharm/IDE autocomplete
- **Testabilidad**: Tests aislados por método

### 2. OneToOne Relationship Pattern

#### Pattern: Perfil Extendido de Usuario
```python
# landing/models.py
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Borra perfil si se borra usuario
        related_name="profile",    # user.profile → accede al perfil
    )
    display_name = models.CharField(max_length=120, blank=True)
    preferred_language = models.CharField(max_length=10, default="es")
    # ... más campos ...

    def __str__(self) -> str:
        return f"Perfil {self.user.get_username()}"
```

#### Acceso Bidireccional
```python
# Desde User → Profile
user = User.objects.first()
profile = user.profile  # Reverse relation

# Desde Profile → User
profile = UserProfile.objects.first()
user = profile.user  # Forward relation
```

#### Beneficios
- **Extensibilidad**: Agregar campos sin modificar User
- **Separación**: Datos de auth vs. datos de perfil
- **Flexibilidad**: Relación 1:1 explícita

### 3. Automatic Field Generation

#### Pattern: Campo Auto-generado con Función
```python
# landing/models.py
def _generate_ingest_token() -> str:
    """Genera token hexadecimal de 32 caracteres."""
    return secrets.token_hex(16)

class UserProfile(models.Model):
    ingest_token = models.CharField(
        max_length=64,
        unique=True,
        editable=False,  # No editable en admin
        default=_generate_ingest_token
    )

    def regenerate_token(self) -> None:
        """Regenera token y guarda solo ese campo."""
        self.ingest_token = _generate_ingest_token()
        self.save(update_fields=["ingest_token"])
```

#### Uso
```python
# Regenerar token (actualización parcial)
profile.regenerate_token()

# Nuevo perfil → token automático
profile = UserProfile.objects.create(user=user)
# ingest_token ya tiene valor generado automáticamente
```

#### Beneficios
- **Seguridad**: Tokens únicos y aleatorios
- **Eficiencia**: update_fields evita UPDATE completo
- **Automatización**: Token al crear perfil

### 4. Choice Fields Pattern

#### Pattern: Choices Definidos en Tupla
```python
class UserProfile(models.Model):
    THEME_CHOICES = (
        ("system", _("Sistema")),
        ("dark", _("Oscuro")),
        ("light", _("Claro")),
    )

    preferred_theme = models.CharField(
        max_length=12,
        choices=THEME_CHOICES,
        default="system"
    )
```

#### Uso en Formularios
```python
# forms.py
preferred_theme = forms.ChoiceField(
    label=_('Tema visual'),
    choices=UserProfile.THEME_CHOICES,  # Reutiliza tupla
    widget=forms.Select(attrs={'class': 'auth-input'}),
)
```

#### Beneficios
- **Consistencia**: Mismas choices en modelo y formulario
- **DRY**: No duplicar enumeraciones
- **i18n**: Choices traducidas con gettext_lazy

### 5. Meta Class Pattern

#### Pattern: Meta Opciones de Modelo
```python
class Product(models.Model):
    # ... campos ...

    class Meta:
        ordering = ('sort_order', 'name')  # Ordenación por defecto
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self) -> str:
        return self.name
```

#### Ordenación Personalizada
```python
# Usar ordenación del modelo
products = Product.objects.all()  # Ya ordenado por sort_order, name

# Sobrescribir ordenación específica
Product.objects.order_by('-created_at')  # Más reciente primero
```

#### Beneficios
- **Consistencia**: Ordenación automática
- **Legibilidad**: __str__ para debug
- **Admin**: verbose_name en interfaz

## View Patterns

### 1. Class-Based Views (CBV) Pattern

#### Pattern: TemplateView con Contexto Personalizado
```python
# landing/views.py
class HomeView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Datos estáticos estructurados
        hero = {
            'eyebrow': _('Buddy AI · Entrena, Progresa, Destaca'),
            'title': _('Tu entrenador AI personal'),
            'lead': _('Rutinas que se adaptan a ti...'),
            'primary_cta': {'label': _('🛒 Ir a la Tienda'), 'url': reverse('shop:catalogue')},
            # ... más datos
        }

        # Query optimizada con values()
        buddy_products = list(
            Product.objects.filter(is_published=True)
            .order_by('sort_order', 'name')
            .values('name', 'slug', 'teaser', 'price', 'delivery_estimate', 'badge_label')[:3]
        )

        context.update(
            hero=hero,
            metrics=metrics,
            vectors=vectors,
            buddy_products=buddy_products,
        )
        return context
```

#### Composición de Vistas
```python
class AboutView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/about.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            page_title=_('Nosotros'),
        )
        return context
```

#### Beneficios
- **Reutilización**: Lógica en métodos separados
- **Herencia**: cbv → mixin → view
- **Type Hints**: dict[str, Any] para tipado

### 2. Mixin Pattern

#### Pattern: Mixin de Navegación Reutilizable
```python
class LandingNavigationMixin:
    """Inyecta navegación primaria y resultados de búsqueda global."""

    def get_nav_links(self) -> list[dict[str, str]]:
        """Obtiene links de navegación primaria."""
        return primary_nav_links()

    def get_search_results(self) -> list[dict[str, str]]:
        """Obtiene entradas de búsqueda global."""
        return global_search_entries()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Inyecta navegación en contexto de cualquier vista."""
        context = super().get_context_data(**kwargs)

        # setdefault evita sobrescribir si ya existe
        context.setdefault('nav_links', self.get_nav_links())

        show_shortcuts = context.get('show_global_shortcuts', False)
        context['show_global_shortcuts'] = show_shortcuts
        context['search_results'] = self.get_search_results() if show_shortcuts else []

        # Marca por defecto
        context.setdefault('brand', 'gator')
        return context
```

#### Uso en Múltiples Vistas
```python
class HomeView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/home.html'

class AboutView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/about.html'

class BuddyView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/buddy.html'
```

#### Beneficios
- **DRY**: No repetir lógica de navegación
- **Flexibilidad**: Fácil de extender
- **Composicional**: Múltiples mixins posibles

### 3. LoginRequiredMixin Pattern

#### Pattern: Vista Protegida para Autenticados
```python
class ProfileView(LoginRequiredMixin, LandingNavigationMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = user.profile  # type: ignore[attr-defined]

        context.update(
            profile_form=ProfileForm(instance=user),
            preferences_form=ProfilePreferencesForm(instance=profile),
            token_form=TokenResetForm(),
            ingest_token=profile.ingest_token,
            # ... más contexto
        )
        return context
```

#### Multi-Form POST Pattern
```python
def post(self, request, *args, **kwargs):  # type: ignore[override]
    """Maneja múltiples formularios en una vista."""
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
    elif form_name == 'token':
        profile.regenerate_token()
        messages.success(request, _('Generamos un nuevo token para tus robots.'))

    return self.get(request, *args, **kwargs)
```

#### Beneficios
- **Seguridad**: Solo usuarios autenticados
- **Eficiencia**: Un endpoint para múltiples acciones
- **UX**: Messages framework para feedback

### 4. FormView Pattern

#### Pattern: Formulario de Registro Customizado
```python
class CroodySignupView(LandingNavigationMixin, FormView):
    template_name = 'account/register.html'
    form_class = CroodySignupForm

    def get_success_url(self) -> str:
        return reverse('landing:profile')

    def form_valid(self, form: CroodySignupForm):  # type: ignore[override]
        """Procesa formulario válido con lógica custom."""
        user = form.save()
        login(self.request, user)  # Auto-login después de registro
        messages.success(self.request, _('Bienvenido a Croody...'))
        return super().form_valid(form)
```

#### Beneficios
- **Separación**: Lógica de formulario en Form class
- **Reutilización**: Mismo form_class en múltiples vistas
- **Callbacks**: form_valid() para lógica post-save

## Form Patterns

### 1. Custom Form Fields Pattern

#### Pattern: Widgets Personalizados con Clases CSS
```python
# forms.py
class CroodyLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Usuario o correo'),
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'auth-input',           # Clase CSS custom
                'placeholder': 'ej. mateo@croody.app',
                'autocomplete': 'username',      # Autocompletado del browser
            }
        ),
    )

    password = forms.CharField(
        label=_('Contraseña'),
        strip=False,  # No quitar espacios en blanco
        widget=forms.PasswordInput(
            attrs={
                'class': 'auth-input',
                'placeholder': '••••••••',
                'autocomplete': 'current-password',
            }
        ),
    )
```

#### Beneficios
- **Consistencia**: Misma clase CSS en todos los inputs
- **UX**: Placeholders y autocomplete
- **Seguridad**: strip=False para passwords

### 2. Form Validation Pattern

#### Pattern: Validación Email Existente
```python
def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email__iexact=email).exists():
        raise forms.ValidationError(_('Ya existe una cuenta con este correo.'))
    return email
```

#### Pattern: Email-to-Username Conversion
```python
class CroodyLoginForm(AuthenticationForm):
    def clean(self):  # type: ignore[override]
        """Convierte email a username automáticamente."""
        username = self.cleaned_data.get('username')
        if username and '@' in username:
            try:
                user = User.objects.get(email__iexact=username)
                self.cleaned_data['username'] = user.get_username()
            except User.DoesNotExist:
                pass
        return super().clean()
```

#### Beneficios
- **UX**: Login con email O username
- **UX**: Validación en tiempo real
- **Robustez**: Caso edge (email no existe)

### 3. Form Composition Pattern

#### Pattern: Herencia de UserCreationForm
```python
class CroodySignupForm(UserCreationForm):
    """Extiende UserCreationForm con campos adicionales."""

    full_name = forms.CharField(...)
    email = forms.EmailField(...)
    preferred_language = forms.ChoiceField(...)
    preferred_theme = forms.ChoiceField(...)
    accept_terms = forms.BooleanField(...)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name', 'email', 'preferred_language', 'preferred_theme', 'password1', 'password2')
```

#### Widget Attributes Injection
```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Inyecta clase CSS a todos los password inputs
    for name in ('password1', 'password2'):
        self.fields[name].widget.attrs.update({'class': 'auth-input'})

    self.fields['accept_terms'].widget.attrs.update({'class': 'auth-checkbox'})
```

#### Custom save() Method
```python
def save(self, commit: bool = True):  # type: ignore[override]
    """Guarda user y crea perfil con datos adicionales."""
    user = super().save(commit=False)

    # Procesar email y username
    email = self.cleaned_data['email']
    user.email = email
    user.username = self._build_username(email)

    # Separar nombre completo
    full_name = self.cleaned_data['full_name'].strip()
    if full_name:
        parts = full_name.split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ''

    if commit:
        user.save()
        # Crear perfil con preferencias
        profile = user.profile  # type: ignore[attr-defined]
        profile.preferred_language = self.cleaned_data['preferred_language']
        profile.preferred_theme = self.cleaned_data['preferred_theme']
        profile.display_name = full_name or user.username
        profile.save()

    return user
```

#### Username Generation Pattern
```python
def _build_username(self, email: str) -> str:
    """Genera username único desde email."""
    base = email.split('@')[0][:30] or 'croody'
    candidate = base
    idx = 1
    while User.objects.filter(username=candidate).exists():
        candidate = f"{base}-{idx}"
        idx += 1
    return candidate
```

#### Beneficios
- **Extensibilidad**: Hereda funcionalidad base
- **Customización**: Campos adicionales
- **Username único**: Auto-generación idempotente
- **Relaciones**: Crea perfil automáticamente

### 4. ModelForm Pattern

#### Pattern: Formularios desde Modelo
```python
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'auth-input',
                'placeholder': _('Nombre')
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'auth-input',
                'placeholder': _('Apellidos')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'auth-input',
                'placeholder': 'tucorreo@croody.app'
            }),
        }
```

#### Field Iteration Pattern
```python
class ProfilePreferencesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'display_name',
            'preferred_language',
            'preferred_theme',
            # ... más campos
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inyecta clases CSS a todos los campos
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'auth-checkbox'})
            else:
                field.widget.attrs.setdefault('class', 'auth-input')
```

#### Beneficios
- **DRY**: No reescribir campos del modelo
- **Sincronización**: Form refleja modelo automáticamente
- **Consistencia**: Inyección de attrs programática

## Signal Patterns

### 1. post_save Signal Pattern

#### Pattern: Creación Automática de Perfil
```python
# signals.py
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created: bool, **kwargs):
    """Crea UserProfile automáticamente cuando se crea User."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance: User, **kwargs):
    """Guarda UserProfile cuando se actualiza User."""
    if hasattr(instance, "profile"):
        instance.profile.save()
```

#### Beneficios
- **Automatización**: No olvidar crear perfil
- **Consistencia**: Un perfil por usuario
- **Transparencia**: Invisible para el dev

### 2. Signal Registration Pattern

#### Pattern: Registro en AppConfig
```python
# apps.py
class LandingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landing'
    verbose_name = 'Landing Croody'

    def ready(self) -> None:
        """Se ejecuta cuando Django inicia la app."""
        from . import signals  # noqa: F401
        return super().ready()
```

#### Cómo Funciona
1. Django importa `apps.py` al arrancar
2. `ready()` se ejecuta
3. `signals` se importa por efectos secundarios
4. Decoradores `@receiver` se registran
5. Signals quedan activos para toda la app

#### Beneficios
- **Explícito**: Señales se registran en un lugar claro
- **Lazy**: No se importan hasta que Django inicie
- **Testeable**: Fácil de mock en tests

## Type Hints Pattern

### 1. Return Type Annotations

#### Pattern: Type Hints en Métodos
```python
def __str__(self) -> str:
    return f"Perfil {self.user.get_username()}"

def regenerate_token(self) -> None:
    self.ingest_token = _generate_ingest_token()
    self.save(update_fields=["ingest_token"])

def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(...)
    return context
```

#### Pattern: Generic Types
```python
from typing import Any, TypedDict

class ProductDict(TypedDict):
    name: str
    slug: str
    teaser: str
    price: Decimal
    delivery_estimate: str
    badge_label: str

def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    buddy_products: list[ProductDict] = list(
        Product.objects.published()
        .order_by('sort_order', 'name')
        .values('name', 'slug', 'teaser', 'price', 'delivery_estimate', 'badge_label')[:3]
    )
```

#### Pattern: Optional Types
```python
from typing import Optional

def _load_ids_model_meta(self) -> Optional[dict[str, Any]]:
    """Retorna metadata del modelo IDS o None si no existe."""
    meta_path = Path(settings.BASE_DIR) / 'services/ids-ml/models/model_metadata.json'
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding='utf-8'))
        return data
    except Exception:
        return None
```

### 2. Type Ignore Comments

#### Pattern: Type Ignore para Dynamic Attributes
```python
# profile es OneToOneField pero el tipo está en settings.AUTH_USER_MODEL
user = self.request.user
profile = user.profile  # type: ignore[attr-defined]

# profile.save() es método del modelo
profile.save()  # type: ignore[attr-defined]
```

#### Beneficios
- **IDE Support**: PyCharm autocompletado
- **Detección errores**: Mypy catching bugs
- **Documentación**: Tipos como documentación
- **Refactoring**: IDE knows types when renaming

## Utility Patterns

### 1. Helper Function Pattern

#### Pattern: Funciones Utilitarias
```python
# Modelo con función helper
def _generate_ingest_token() -> str:
    return secrets.token_hex(16)

# Uso en modelo
class UserProfile(models.Model):
    ingest_token = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
        default=_generate_ingest_token
    )
```

#### Pattern: Build Username
```python
def _build_username(self, email: str) -> str:
    """Genera username único desde email."""
    base = email.split('@')[0][:30] or 'croody'
    candidate = base
    idx = 1
    while User.objects.filter(username=candidate).exists():
        candidate = f"{base}-{idx}"
        idx += 1
    return candidate
```

#### Beneficios
- **Reutilización**: Función se puede reutilizar
- **Testeable**: Tests unitarios aislados
- **Legible**: Nombre descriptivo con _ prefix
- **Modular**: Separada del modelo

### 2. Activity Log Pattern

#### Pattern: Listas de Diccionario para UI
```python
def _activity_log(self, profile: UserProfile) -> list[dict[str, str]]:
    """Genera log de actividad para mostrar en UI."""
    return [
        {
            'title': _('Token de ingestión listo'),
            'subtitle': profile.ingest_token,
            'status': _('activo'),
        },
        {
            'title': _('Alertas de telemetría'),
            'subtitle': (
                _('Recibir notificaciones críticas')
                if profile.telemetry_alerts
                else _('Alertas desactivadas')
            ),
            'status': 'ok' if profile.telemetry_alerts else 'muted',
        },
    ]
```

#### Uso en Template
```python
# En template
{% for entry in activity_log %}
    <div class="entry">
        <h4>{{ entry.title }}</h4>
        <p>{{ entry.subtitle }}</p>
        <span class="status {{ entry.status }}"></span>
    </div>
{% endfor %}
```

#### Beneficios
- **Flexibility**: Estructura flexible para UI
- **Simplicity**: No necesita modelo ActivityLog
- **Direct**: Computation on-the-fly

## Query Patterns

### 1. values() Optimization Pattern

#### Pattern: Seleccionar Solo Campos Necesarios
```python
buddy_products = list(
    Product.objects.filter(is_published=True)
    .order_by('sort_order', 'name')
    .values('name', 'slug', 'teaser', 'price', 'delivery_estimate', 'badge_label')[:3]
)
```

#### Equivalente SQL
```sql
SELECT name, slug, teaser, price, delivery_estimate, badge_label
FROM shop_product
WHERE is_published = true
ORDER BY sort_order ASC, name ASC
LIMIT 3;
```

#### Beneficios
- **Performance**: Solo campos necesarios
- **Memory**: Menos datos en memoria
- **Network**: Respuesta más liviana

### 2. Fallback Data Pattern

#### Pattern: Datos por Defecto si No Hay DB
```python
if not buddy_products:
    buddy_products = [
        {
            'name': 'Pack Buddy Starter',
            'slug': 'buddy-starter',
            'teaser': 'Incluye rutina Wimpy...',
            'price': Decimal('79.00'),
            'delivery_estimate': 'Activación inmediata',
            'badge_label': 'Starter',
        },
        # ... más productos por defecto
    ]
```

#### Beneficios
- **Resilience**: Funciona sin datos en BD
- **Demo**: Muestra ejemplo de producto
- **UX**: No página vacía

### 3. Q Objects Pattern

#### Pattern: Búsqueda con OR Logic
```python
def search(self, query: str) -> 'ProductQuerySet':
    if not query:
        return self
    return self.filter(
        models.Q(name__icontains=query) |
        models.Q(teaser__icontains=query)
    )
```

#### Equivalente SQL
```sql
WHERE name ILIKE '%query%' OR teaser ILIKE '%query%'
```

#### Beneficios
- **Búsqueda**: Querycase-insensitive
- **Flexibility**: Fácil agregar más campos
- **Reutilización**: Método en QuerySet

## Import Patterns

### 1. Future Imports Pattern

#### Pattern: from __future__ import annotations
```python
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _
```

#### Beneficios
- **Forward Reference**: `ProductQuerySet` como string
- **Python 3.10+**: Required para PEP 563
- **No quotes**: 'ProductQuerySet' en lugar de 'ProductQuerySet'

### 2. get_user_model() Pattern

#### Pattern: Lazy User Model Reference
```python
from django.contrib.auth import get_user_model

User = get_user_model()
```

#### En lugar de
```python
from django.contrib.auth.models import User  # ❌ Hard-coded
```

#### Beneficios
- **Customizable**: Funciona con AUTH_USER_MODEL
- **Testing**: Fácil de mock
- **Future-proof**: Compatible con Custom User

### 3. Settings Reference Pattern

#### Pattern: Dynamic Settings Access
```python
from django.conf import settings

class RobotMonitorView(TemplateView):
    def _load_ids_model_meta(self) -> dict[str, Any] | None:
        meta_path = Path(settings.BASE_DIR) / 'services/ids-ml/models/model_metadata.json'
        # ... resto del código
```

#### Beneficios
- **Configurable**: No hard-coded paths
- **Environment**: Diferente en dev/prod
- **Testable**: Mock settings en tests

## URL Patterns

### 1. reverse() Pattern

#### Pattern: URLs Dinámicas en Vistas
```python
primary_cta = {'label': _('🛒 Ir a la Tienda'), 'url': reverse('shop:catalogue')}
secondary_cta = {'label': _('Ver Buddy'), 'url': reverse('landing:buddy')}
```

#### En lugar de
```python
primary_cta = {'label': 'Ir a la Tienda', 'url': '/tienda/'}  # ❌ Hard-coded
```

#### Beneficios
- **Maintainable**: Cambio en URL → actualiza automáticamente
- **Namespacing**: Soporta namespaces (shop:catalogue)
- **i18n**: Compatible con URL patterns

### 2. reverse_lazy() Pattern

#### Pattern: URLs en Class Attributes
```python
class CroodyLogoutView(LogoutView):
    next_page = reverse_lazy('landing:home')
```

#### Beneficios
- **Lazy**: No ejecuta reverse en import time
- **Required**: Para class attributes (no pueden ser functions)
- **Safe**: Funciona en module import

## Message Framework Pattern

### Pattern: Feedback al Usuario
```python
from django.contrib import messages

def form_valid(self, form):
    user = form.save()
    login(self.request, user)
    messages.success(self.request, _('Bienvenido a Croody. Ajusta tu perfil cuando quieras.'))
    return super().form_valid(form)

def post(self, request, *args, **kwargs):
    if form_name == 'token':
        profile.regenerate_token()
        messages.success(request, _('Generamos un nuevo token para tus robots.'))
    else:
        messages.error(request, _('Acción no reconocida.'))
    return self.get(request, *args, **kwargs)
```

#### Tipos de Messages
- `messages.success()`: Éxito (verde)
- `messages.error()`: Error (rojo)
- `messages.warning()`: Advertencia (amarillo)
- `messages.info()`: Info (azul)

#### En Template
```django
{% if messages %}
    {% for message in messages %}
        <div class="flash flash--{{ message.tags }}">{{ message }}</div>
    {% endfor %}
{% endif %}
```

#### Beneficios
- **UX**: Feedback inmediato
- **Persistence**: Sobre redirect/next request
- **Customizable**: Estilos por tipo

## Best Practices

### ✅ Hacer

#### 1. Usar Type Hints Completos
```python
def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    return context
```

#### 2. Separar Lógica con Mixins
```python
class LandingNavigationMixin:
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['nav_links'] = self.get_nav_links()
        return context
```

#### 3. Custom Managers para Query Logic
```python
class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)
```

#### 4. Signals para Automatización
```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

#### 5. form_valid() para Lógica Post-Save
```python
def form_valid(self, form):
    user = form.save()
    login(self.request, user)
    return super().form_valid(form)
```

#### 6. Widgets Personalizados con attrs
```python
username = forms.CharField(
    widget=forms.TextInput(attrs={'class': 'auth-input', 'autocomplete': 'username'})
)
```

#### 7. Messages para Feedback
```python
messages.success(request, _('Operación exitosa.'))
```

#### 8. values() para Optimización
```python
products = Product.objects.published().values('name', 'slug')[:10]
```

#### 9. reverse() para URLs Dinámicas
```python
url = reverse('shop:detail', args=[product.slug])
```

#### 10. get_user_model() en lugar de User hard-coded
```python
from django.contrib.auth import get_user_model
User = get_user_model()
```

### ❌ Evitar

#### 1. No Hard-coded URLs
```python
# ❌ Mal
'url': '/tienda/'

# ✅ Bien
'url': reverse('shop:catalogue')
```

#### 2. No N+1 Queries
```python
# ❌ Mal
for product in products:
    print(product.category.name)  # N queries adicionales

# ✅ Bien
products = Product.objects.select_related('category')
```

#### 3. No Lógica en Templates
```python
# ❌ Mal
{% if user.profile.preferred_theme == 'dark' %}

# ✅ Bien
{% if theme == 'dark' %}
```

#### 4. No Queries en get_context_data sin Optimizar
```python
# ❌ Mal
def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    # Query sin select_related
    context['user_profile'] = self.request.user.profile
    return context

# ✅ Bien
def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    # Query optimizada o mejor aún, está en request si usaste middleware
    context['user_profile'] = getattr(self.request.user, 'profile', None)
    return context
```

#### 5. No Duplicate Query Logic
```python
# ❌ Mal
products = Product.objects.filter(is_published=True)
products2 = Product.objects.filter(is_published=True).order_by('name')

# ✅ Bien
# Usar custom manager
class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

products = Product.objects.published()
products2 = Product.objects.published().order_by('name')
```

#### 6. No Magic Numbers
```python
# ❌ Mal
TOKEN_LENGTH = 32

# ✅ Bien
TOKEN_LENGTH = secrets.token_hex(16).__len__()
# O mejor: docstring
```

## Testing Patterns

### 1. Testing Custom Managers
```python
from django.test import TestCase
from shop.models import Product

class ProductQuerySetTest(TestCase):
    def test_published(self):
        Product.objects.create(name="P1", is_published=True)
        Product.objects.create(name="P2", is_published=False)

        published = Product.objects.published()
        self.assertEqual(published.count(), 1)
        self.assertEqual(published.first().name, "P1")
```

### 2. Testing Signals
```python
from django.contrib.auth import get_user_model
from landing.models import UserProfile

User = get_user_model()

class UserProfileSignalTest(TestCase):
    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='test', email='test@example.com')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, UserProfile)
```

### 3. Testing Forms
```python
from landing.forms import CroodySignupForm

class CroodySignupFormTest(TestCase):
    def test_clean_email_duplicate(self):
        User.objects.create_user(username='existing', email='test@example.com')
        form = CroodySignupForm({
            'full_name': 'Test User',
            'email': 'test@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'preferred_language': 'es',
            'preferred_theme': 'system',
            'accept_terms': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Ya existe una cuenta', form.errors['email'][0])
```

### 4. Testing Views
```python
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileViewTest(TestCase):
    def test_profile_requires_login(self):
        client = Client()
        response = client.get('/perfil/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_shows_user_data(self):
        user = User.objects.create_user(username='test', email='test@example.com')
        client = Client()
        client.force_login(user)
        response = client.get('/perfil/')
        self.assertContains(response, user.email)
```

## Performance Patterns

### 1. select_related() para ForeignKeys
```python
# En lugar de
products = Product.objects.all()

# Usar
products = Product.objects.select_related('category')
```

### 2. prefetch_related() para ManyToMany
```python
products = Product.objects.prefetch_related('tags', 'images')
```

### 3. values() para Queries de Solo Lectura
```python
product_list = list(
    Product.objects.published()
    .order_by('sort_order')
    .values('id', 'name', 'slug', 'price')
)
```

### 4. only() para Reducir Campos
```python
# Solo cargar campos necesarios
products = Product.objects.only('name', 'price')
```

### 5. defer() para Posponer Campos Grandes
```python
# Cargar todos excepto description (campo grande)
products = Product.objects.defer('description')
```

### 6. Pagination Pattern
```python
from django.core.paginator import Paginator

def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    all_products = Product.objects.published()
    paginator = Paginator(all_products, 12)  # 12 por página
    page_obj = paginator.get_page(self.request.GET.get('page'))
    context['products'] = page_obj
    return context
```

## Security Patterns

### 1. CSRF Protection
```python
# En formularios Django (automático)
<form method="post">
    {% csrf_token %}
    ...
</form>
```

### 2. LoginRequiredMixin
```python
class ProfileView(LoginRequiredMixin, TemplateView):
    # Solo usuarios autenticados pueden acceder
    pass
```

### 3. Password Validation
```python
# Django内置 validación de passwords
# UserCreationForm incluye password1 y password2
# Django verifica que no sea muy común, muy corto, etc.
```

### 4. Mass Assignment Protection
```python
# ModelForm solo permite campos en Meta.fields
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')  # Solo estos campos
        # NO incluye password, is_staff, is_superuser, etc.
```

### 5. SQL Injection Prevention
```python
# ✅ Bien: ORM queries
Product.objects.filter(name__icontains=query)

# ❌ Mal: Raw SQL con concatenación
Product.objects.raw(f"SELECT * FROM shop_product WHERE name LIKE '%{query}%'")
```

## Architectural Patterns

### 1. Separation of Concerns
```
landing/
├── models.py          # Solo datos
├── views.py           # Solo lógica HTTP
├── forms.py           # Solo validación/entrada
├── signals.py         # Solo automatización
└── apps.py            # Solo configuración
```

### 2. Module Organization
```
shop/
├── models.py          # Product y ProductQuerySet
├── views.py           # ProductListView, ProductDetailView
├── urls.py            # URLs del módulo shop
└── admin.py           # Customización admin
```

### 3. App Structure
```
landing/
├── __init__.py
├── apps.py            # AppConfig
├── models.py          # Modelos
├── views.py           # Vistas
├── forms.py           # Formularios
├── urls.py            # URLs
├── admin.py           # Admin
├── signals.py         # Signals
├── migrations/        # Migraciones DB
└── management/        # Comandos personalizados
```

### 4. Namespace Pattern
```python
# URLs con namespace
app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='catalogue'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
]

# Referenciar con namespace
reverse('shop:catalogue')
reverse('shop:detail', args=[product.slug])
```

### 5. Settings Pattern
```python
# Usar settings configurables
from django.conf import settings

class RobotMonitorView(TemplateView):
    def _load_ids_model_meta(self) -> Optional[dict[str, Any]]:
        meta_path = Path(settings.BASE_DIR) / 'services/ids-ml/models/model_metadata.json'
```

## i18n Patterns

### 1. gettext_lazy() para Strings Traducibles
```python
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    THEME_CHOICES = (
        ("system", _("Sistema")),
        ("dark", _("Oscuro")),
        ("light", _("Claro")),
    )
```

### 2. Translatable Default Values
```python
from django.utils.translation import gettext_lazy as _

preferred_language = models.CharField(max_length=10, default=_("es"))
```

### 3. Translatable Error Messages
```python
def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email__iexact=email).exists():
        raise forms.ValidationError(_('Ya existe una cuenta con este correo.'))
    return email
```

### 4. Translatable Content in Views
```python
def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
        page_title=_('Nosotros'),
    )
    return context
```

## Common Pitfalls

### 1. Not Using select_related
```python
# ❌ Mal: N+1 queries
for product in products:
    print(product.category.name)

# ✅ Bien
products = Product.objects.select_related('category')
for product in products:
    print(product.category.name)
```

### 2. Overriding save() for Simple Logic
```python
# ❌ Mal: Overriding save()
class Product(models.Model):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# ✅ Bien: Pre-save signal o override save method con lógica compleja
# O usar auto_slug field
```

### 3. Multiple Queries in Template
```python
# ❌ Mal: Query en template
{% for product in products %}
    {{ product.category.name }}  # Query para cada producto
{% endfor %}

# ✅ Bien: select_related en vista
products = Product.objects.select_related('category')
```

### 4. Not Using get_user_model()
```python
# ❌ Mal
from django.contrib.auth.models import User

# ✅ Bien
from django.contrib.auth import get_user_model
User = get_user_model()
```

### 5. Hard-coded Paths
```python
# ❌ Mal
meta_path = '/app/services/ids-ml/models/model_metadata.json'

# ✅ Bien
from django.conf import settings
meta_path = Path(settings.BASE_DIR) / 'services/ids-ml/models/model_metadata.json'
```

### 6. Not Using reverse()
```python
# ❌ Mal
'url': '/tienda/producto/abc-123/'

# ✅ Bien
'url': reverse('shop:detail', args=[product.slug])
```

### 7. Mixing Query Logic
```python
# ❌ Mal: Query logic en vista
products = Product.objects.filter(is_published=True).order_by('name')

# ✅ Bien: Custom QuerySet
products = Product.objects.published().order_by('name')
```

### 8. Not Using Type Hints
```python
# ❌ Mal
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context

# ✅ Bien
def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    return context
```

## Performance Monitoring

### 1. django-debug-toolbar
```python
# settings.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

### 2. Query Counts in Tests
```python
from django.test import TestCase

class ProductListTest(TestCase):
    def test_product_list_queries(self):
        with self.assertNumQueries(1):  # Solo 1 query
            response = self.client.get('/tienda/')
            self.assertContains(response, 'Products')
```

### 3. Logging Slow Queries
```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Migration Patterns

### 1. Data Migrations
```python
# migrations/0002_seed_products.py
from django.db import migrations

def seed_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Product.objects.create(
        name='Pack Buddy Starter',
        slug='buddy-starter',
        price=Decimal('79.00'),
        is_published=True,
    )

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_products),
    ]
```

### 2. Custom Management Commands
```python
# landing/management/commands/runhttps.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Lógica del comando
        pass
```

## Referencias

### Archivos Relacionados
- `landing/models.py` - Modelos con patrones de manager y signals
- `landing/views.py` - CBVs con mixins y type hints
- `landing/forms.py` - Formularios customizados con validación
- `landing/signals.py` - Signal handlers para automatización
- `shop/models.py` - QuerySet personalizado

### Documentación Externa
- [Django Class-Based Views](https://docs.djangoproject.com/en/stable/topics/class-based-views/)
- [Django Forms](https://docs.djangoproject.com/en/stable/topics/forms/)
- [Django Signals](https://docs.djangoproject.com/en/stable/topics/signals/)
- [Django QuerySets](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## Ver También
- [Modelos](../02-BACKEND/modelos.md)
- [Vistas](../02-BACKEND/vistas.md)
- [APIs REST](../02-BACKEND/apis-rest.md)
- [Formularios](../03-FRONTEND/componentes/formularios.md)
- [Testing - Unitario, Integración, E2E](../testing/testing-general.md)
