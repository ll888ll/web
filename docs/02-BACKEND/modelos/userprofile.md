# Modelo UserProfile - Documentación Completa

## Resumen
El modelo `UserProfile` extiende el modelo `User` de Django para agregar funcionalidades específicas del ecosistema Croody, incluyendo preferencias de usuario, tokens de ingestión para telemetría, y configuraciones personalizadas.

## Ubicación
`/proyecto_integrado/Croody/landing/models.py`

## Estructura del Modelo

### Campos

| Campo | Tipo | Descripción | Por Defecto |
|-------|------|-------------|-------------|
| `user` | OneToOneField | Relación 1:1 con User | REQUIRED |
| `display_name` | CharField(120) | Nombre para mostrar | "" (vacío) |
| `preferred_language` | CharField(10) | Idioma preferido (ISO 639-1) | "es" |
| `preferred_theme` | CharField(12) | Tema (system/dark/light) | "system" |
| `timezone` | CharField(64) | Zona horaria | "UTC" |
| `notification_level` | CharField(24) | Nivel de notificaciones | "smart" |
| `telemetry_alerts` | BooleanField | Recibir alertas de telemetría | True |
| `ingest_token` | CharField(64) | Token único para ingestión | Auto-generado |
| `favorite_robot` | CharField(64) | Robot favorito | "" (vacío) |
| `bio` | TextField | Biografía del usuario | "" (vacío) |
| `created_at` | DateTimeField | Fecha de creación | auto_now_add |
| `updated_at` | DateTimeField | Fecha de actualización | auto_now |

### Choices

**TEMA_CHOICES:**
```python
THEME_CHOICES = [
    ('system', 'System'),
    ('dark', 'Dark'),
    ('light', 'Light'),
]
```

**NOTIFICATION_LEVEL_CHOICES:**
```python
NOTIFICATION_LEVEL_CHOICES = [
    ('smart', 'Smart'),
    ('minimal', 'Minimal'),
    ('all', 'All'),
]
```

## Funcionalidades Principales

### 1. Generación Automática de Token

**Función:** `_generate_ingest_token()`
```python
def _generate_ingest_token() -> str:
    """Genera token único para ingestión de telemetría."""
    return secrets.token_hex(16)  # 32 caracteres hex
```

**Propósito:** Cada usuario recibe un token único de 32 caracteres hexadecimales (16 bytes) para autenticación en el sistema de telemetría de robots.

**Seguridad:**
- Usa `secrets.token_hex()` (cryptographically secure)
- No es predecible
- Único globalmente

### 2. Regeneración de Token

**Método:** `regenerate_token()`
```python
def regenerate_token(self) -> None:
    """Regenera el token de ingestión de manera segura."""
    self.ingest_token = _generate_ingest_token()
    self.save(update_fields=['ingest_token'])
```

**Uso típico:**
```python
# Regenerar token
user.profile.regenerate_token()

# El nuevo token está disponible inmediatamente
print(user.profile.ingest_token)
```

**Casos de uso:**
- Compromiso de token anterior
- Rotación periódica de seguridad
- Reset manual del usuario

### 3. Señales Django

**Creación automática:**
```python
# signals.py
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea UserProfile automáticamente cuando se crea un User."""
    if created:
        UserProfile.objects.create(user=instance)
```

**Actualización automática:**
```python
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guarda UserProfile cuando se guarda el User."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

**Ventajas:**
- Garantiza que cada User tenga Profile
- Elimina código duplicado
- Previene inconsistencias

## Patrones de Uso

### 1. Acceso al Profile

**Método recomendado:**
```python
def get_user_profile(user):
    """Obtiene el profile del usuario de manera segura."""
    if hasattr(user, 'profile'):
        return user.profile
    return UserProfile.objects.get_or_create(user=user)[0]
```

**Acceso directo (usar con cuidado):**
```python
# Si el usuario está autenticado y tiene profile
profile = request.user.profile  # type: ignore[attr-defined]
```

**Nota:** El `type: ignore` es necesario porque Django no detecta automáticamente la relación OneToOne.

### 2. Actualización de Preferencias

```python
def update_user_preferences(user, language='es', theme='system'):
    """Actualiza preferencias de usuario."""
    profile = user.profile
    profile.preferred_language = language
    profile.preferred_theme = theme
    profile.save()
```

### 3. Verificación de Token

```python
def verify_ingest_token(token: str) -> bool:
    """Verifica si un token de ingestión es válido."""
    return UserProfile.objects.filter(ingest_token=token).exists()
```

## Índices de Base de Datos

### Índices Recomendados
```python
class UserProfile(models.Model):
    # ... campos ...

    class Meta:
        indexes = [
            models.Index(fields=['ingest_token']),  # Búsqueda rápida de token
            models.Index(fields=['user']),          # Join con User
            models.Index(fields=['preferred_language']),  # Filtrado por idioma
        ]
```

## Migraciones

### Migración Inicial
```python
# 0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(blank=True, max_length=120)),
                ('preferred_language', models.CharField(default='es', max_length=10)),
                ('preferred_theme', models.CharField(default='system', max_length=12)),
                ('timezone', models.CharField(default='UTC', max_length=64)),
                ('notification_level', models.CharField(default='smart', max_length=24)),
                ('telemetry_alerts', models.BooleanField(default=True)),
                ('ingest_token', models.CharField(default=landing.models._generate_ingest_token, editable=False, max_length=64, unique=True)),
                ('favorite_robot', models.CharField(blank=True, max_length=64)),
                ('bio', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
```

## Validaciones

### Validación de Email Único
**Ubicación:** `landing/forms.py` (CroodySignupForm)

```python
def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email__iexact=email).exists():
        raise forms.ValidationError(_('Ya existe una cuenta con este correo.'))
    return email
```

### Validación de Token
```python
def clean_ingest_token(self):
    token = self.cleaned_data.get('ingest_token')
    if token and len(token) != 32:
        raise ValidationError('Token debe tener 32 caracteres.')
    return token
```

## Admin Django

### Registro
```python
# landing/admin.py
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'preferred_language', 'preferred_theme', 'created_at')
    list_filter = ('preferred_language', 'preferred_theme', 'notification_level', 'telemetry_alerts')
    search_fields = ('user__username', 'user__email', 'display_name', 'ingest_token')
    readonly_fields = ('ingest_token', 'created_at', 'updated_at')

    fieldsets = (
        ('Usuario', {
            'fields': ('user', 'display_name', 'bio')
        }),
        ('Preferencias', {
            'fields': ('preferred_language', 'preferred_theme', 'timezone', 'notification_level')
        }),
        ('Telemetría', {
            'fields': ('telemetry_alerts', 'favorite_robot', 'ingest_token')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

## API Serializers (Django REST Framework)

```python
from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user', 'ingest_token', 'created_at', 'updated_at')
```

## Métodos Personalizados

### String Representation
```python
def __str__(self) -> str:
    return f"Profile({self.user.username})"
```

### Método Save Personalizado
```python
def save(self, *args, **kwargs):
    # Log antes de guardar
    logger.info(f"Guardando profile para usuario: {self.user.username}")

    # Validación adicional
    if self.preferred_language not in ['es', 'en', 'fr', 'pt', 'ar', 'zh-hans', 'ja', 'hi']:
        raise ValueError(f"Idioma no soportado: {self.preferred_language}")

    super().save(*args, **kwargs)
```

## Consideraciones de Performance

### 1. select_related
```python
# Good: Incluir user en la query
profiles = UserProfile.objects.select_related('user').all()

# Avoid: N+1 queries
for profile in UserProfile.objects.all():
    print(profile.user.username)  # Query adicional por cada iteration
```

### 2. prefetch_related (si hay relaciones M2M)
```python
profiles = UserProfile.objects.prefetch_related('favorite_robots').all()
```

### 3. Bulk Operations
```python
# Bulk update
UserProfile.objects.filter(preferred_theme='light').update(preferred_theme='dark')
```

## Seguridad

### Protección de Datos Sensibles
```python
def to_representation(self, instance):
    """Oculta el token en serialización pública."""
    data = super().to_representation(instance)
    # Solo mostrar token si el usuario es el propietario
    if self.context['request'].user != instance.user:
        data.pop('ingest_token', None)
    return data
```

### Auditoría
```python
def save(self, *args, **kwargs):
    is_new = self.pk is None
    super().save(*args, **kwargs)

    # Log de auditoría
    action = "created" if is_new else "updated"
    logger.info(f"Profile {action}: {self.user.username}")
```

## Testing

### Unit Tests
```python
# tests/unit/models/test_userprofile.py
import pytest
from django.contrib.auth.models import User
from landing.models import UserProfile

@pytest.mark.django_db
class TestUserProfile:
    def test_profile_creation(self):
        user = User.objects.create_user(username='test')
        assert hasattr(user, 'profile')
        assert user.profile.preferred_language == 'es'
        assert len(user.profile.ingest_token) == 32

    def test_token_regeneration(self):
        user = User.objects.create_user(username='test')
        old_token = user.profile.ingest_token

        user.profile.regenerate_token()
        user.profile.refresh_from_db()

        assert user.profile.ingest_token != old_token
        assert len(user.profile.ingest_token) == 32
```

## Ejemplos de Uso

### 1. Crear Usuario con Profile
```python
# Signals crean automáticamente el profile
user = User.objects.create_user(
    username='john_doe',
    email='john@example.com'
)

# El profile ya está creado
print(user.profile.display_name)  # ""
```

### 2. Actualizar Preferencias
```python
profile = user.profile
profile.preferred_language = 'en'
profile.preferred_theme = 'dark'
profile.save()
```

### 3. Usar Token para Telemetría
```python
# El usuario proporciona su token
token = user.profile.ingest_token

# Verificar en API de telemetría
if verify_ingest_token(token):
    # Permitir ingestión
    process_telemetry_data(data, token)
```

## Referencias

### Archivos Relacionados
- `landing/signals.py` - Señales de creación/actualización
- `landing/forms.py` - Formularios (ProfileForm, PreferencesForm)
- `landing/views.py` - ProfileView
- `landing/admin.py` - Admin personalizado

### Documentación Externa
- [Django OneToOneField](https://docs.djangoproject.com/en/stable/ref/models/fields/#onetoonefield)
- [Django Signals](https://docs.djangoproject.com/en/stable/topics/signals/)
- [secrets - Secure random numbers](https://docs.python.org/3/library/secrets.html)

## Ver También
- [Formularios UserProfile](../formularios.md)
- [Vistas de Profile](../vistas/profile-view.md)
- [Admin UserProfile](../../06-SEGURIDAD/admin.md)
