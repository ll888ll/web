# Modelo UserProfile (accounts) - Documentación Completa

## Resumen
El modelo `UserProfile` en la app `accounts` es el perfil extendido principal del usuario en el ecosistema Croody. Incluye datos físicos, configuración de avatar, integración con wallet Solana y sistema de gamificación (puntos/rangos).

> **Nota:** Este modelo reemplaza al `LegacyUserProfile` de `landing/models.py`. El modelo legacy se mantiene solo por compatibilidad con migraciones existentes.

## Ubicación
`/proyecto_integrado/Croody/accounts/models.py`

## Estructura del Modelo

### Campos

#### Datos Físicos
| Campo | Tipo | Descripción | Por Defecto |
|-------|------|-------------|-------------|
| `user` | OneToOneField | Relación 1:1 con User | REQUIRED |
| `weight` | DecimalField(5,2) | Peso en kg | null |
| `height` | DecimalField(5,2) | Altura en cm | null |
| `birth_date` | DateField | Fecha de nacimiento | null |
| `gender` | CharField(20) | Género (choices) | "" |
| `fitness_goals` | JSONField | Objetivos de fitness | [] |
| `bio` | TextField(500) | Biografía | "" |

#### Avatar y Personalización
| Campo | Tipo | Descripción | Por Defecto |
|-------|------|-------------|-------------|
| `profile_picture` | ImageField | Foto de perfil | null |
| `active_character` | ForeignKey(Product) | Personaje activo del inventario | null |

#### Wallet Solana
| Campo | Tipo | Descripción | Por Defecto |
|-------|------|-------------|-------------|
| `solana_public_key` | CharField(44) | Dirección wallet Solana (base58) | "" |
| `wallet_verified` | BooleanField | Wallet verificada | False |
| `wallet_connected_at` | DateTimeField | Fecha de conexión | null |

#### Gamificación
| Campo | Tipo | Descripción | Por Defecto |
|-------|------|-------------|-------------|
| `points` | PositiveIntegerField | Puntos totales | 0 |
| `rank` | CharField(20) | Rango del usuario | "novato" |
| `profile_completion` | PositiveSmallIntegerField | Completitud (%) | 0 |

#### Metadata
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `created_at` | DateTimeField | Fecha de creación (auto) |
| `updated_at` | DateTimeField | Fecha de actualización (auto) |

### Choices

#### Gender
```python
class Gender(models.TextChoices):
    MALE = 'male', 'Masculino'
    FEMALE = 'female', 'Femenino'
    NON_BINARY = 'non_binary', 'No binario'
    PREFER_NOT_SAY = 'prefer_not_say', 'Prefiero no decir'
```

#### UserRank
```python
class UserRank(models.TextChoices):
    NOVATO = 'novato', 'Novato'        # 0-499 puntos
    APRENDIZ = 'aprendiz', 'Aprendiz'  # 500-1499 puntos
    GUERRERO = 'guerrero', 'Guerrero'  # 1500-2999 puntos
    MAESTRO = 'maestro', 'Maestro'     # 3000-4999 puntos
    LEYENDA = 'leyenda', 'Leyenda'     # 5000+ puntos
```

## Métodos Principales

### calculate_profile_completion()
Calcula el porcentaje de completitud del perfil basado en campos rellenados.

```python
def calculate_profile_completion(self) -> int:
    """Calcula el porcentaje de completitud del perfil."""
    fields_to_check = [
        self.weight is not None,
        self.height is not None,
        self.birth_date is not None,
        bool(self.gender),
        bool(self.bio),
        bool(self.profile_picture),
        bool(self.solana_public_key),
    ]
    completed = sum(fields_to_check)
    total = len(fields_to_check)
    return int((completed / total) * 100)
```

**Campos evaluados (7 total):**
- weight, height, birth_date, gender, bio, profile_picture, solana_public_key

### calculate_points()
Calcula los puntos totales del usuario basado en múltiples factores.

```python
def calculate_points(self) -> int:
    """Calcula los puntos totales del usuario."""
    points = 0

    # Puntos por perfil completo
    completion = self.calculate_profile_completion()
    if completion == 100:
        points += 500
    else:
        points += int(completion * 3)  # Hasta 300 puntos parciales

    # Puntos por wallet verificada
    if self.wallet_verified:
        points += 200

    # Puntos por foto de perfil
    if self.profile_picture:
        points += 100

    # Puntos por personaje activo
    if self.active_character:
        points += 50

    # Puntos por items en inventario
    inventory_count = self.user.inventory_items.count()
    points += inventory_count * 50

    # Puntos por suscripción activa
    # Starter: +300, Pro: +500, Elite: +1000

    return points
```

**Tabla de puntos:**
| Acción | Puntos |
|--------|--------|
| Perfil 100% completo | +500 |
| Perfil parcial | +3 por cada % |
| Wallet verificada | +200 |
| Foto de perfil | +100 |
| Personaje activo | +50 |
| Cada item en inventario | +50 |
| Suscripción Starter activa | +300 |
| Suscripción Pro activa | +500 |
| Suscripción Elite activa | +1000 |

### update_rank()
Actualiza el rango basado en los puntos acumulados.

```python
def update_rank(self) -> str:
    points = self.calculate_points()

    if points >= 5000:
        return UserRank.LEYENDA
    elif points >= 3000:
        return UserRank.MAESTRO
    elif points >= 1500:
        return UserRank.GUERRERO
    elif points >= 500:
        return UserRank.APRENDIZ
    else:
        return UserRank.NOVATO
```

### refresh_stats()
Recalcula y guarda todas las estadísticas del perfil.

```python
def refresh_stats(self) -> None:
    """Recalcula y guarda puntos, rango y completitud."""
    self.profile_completion = self.calculate_profile_completion()
    self.points = self.calculate_points()
    self.rank = self.update_rank()
    self.save(update_fields=['profile_completion', 'points', 'rank', 'updated_at'])
```

**Uso recomendado:**
```python
# Después de cualquier actualización del perfil
user.profile.refresh_stats()
```

## Señales Django

### Creación automática de perfil
```python
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un perfil automáticamente cuando se crea un usuario."""
    if created:
        UserProfile.objects.create(user=instance)
```

### Actualización automática
```python
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Guarda el perfil cuando se guarda el usuario."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

## Patrones de Uso

### Acceso al perfil
```python
# Acceso directo (recomendado)
profile = request.user.profile

# Con verificación
if hasattr(user, 'profile'):
    profile = user.profile
else:
    profile = UserProfile.objects.create(user=user)
```

### Actualizar datos físicos
```python
profile = user.profile
profile.weight = Decimal('75.5')
profile.height = Decimal('180.0')
profile.birth_date = date(1990, 5, 15)
profile.gender = Gender.MALE
profile.save()

# Recalcular estadísticas
profile.refresh_stats()
```

### Conectar wallet Solana
```python
from django.utils import timezone

profile = user.profile
profile.solana_public_key = "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU"
profile.wallet_connected_at = timezone.now()
profile.save()

# Marcar como verificada después de validación on-chain
profile.wallet_verified = True
profile.save()
profile.refresh_stats()  # +200 puntos
```

### Establecer personaje activo
```python
from shop.models import Product

# El personaje debe estar en el inventario del usuario
character = Product.objects.get(slug='buddy-warrior')

# Verificar que el usuario lo posee
if user.inventory_items.filter(product=character).exists():
    profile.active_character = character
    profile.save()
    profile.refresh_stats()  # +50 puntos
```

## Integración con Inventario

```python
# Obtener items del usuario
inventory = user.inventory_items.all()

# Verificar si posee un producto específico
has_product = user.inventory_items.filter(product__slug='cofre-premium').exists()

# Contar items para puntos
item_count = user.inventory_items.count()
inventory_points = item_count * 50
```

## Integración con Suscripción

```python
# Verificar suscripción activa
try:
    subscription = user.subscription
    if subscription.is_active:
        tier = subscription.tier  # 'starter', 'pro', 'elite'
        days_left = subscription.days_remaining
except Subscription.DoesNotExist:
    # Usuario sin suscripción
    pass
```

## Admin Django

```python
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rank', 'points', 'profile_completion', 'wallet_verified')
    list_filter = ('rank', 'wallet_verified', 'gender')
    search_fields = ('user__username', 'user__email', 'solana_public_key')
    readonly_fields = ('created_at', 'updated_at', 'points', 'rank', 'profile_completion')

    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Datos Físicos', {
            'fields': ('weight', 'height', 'birth_date', 'gender', 'bio')
        }),
        ('Avatar', {
            'fields': ('profile_picture', 'active_character')
        }),
        ('Wallet Solana', {
            'fields': ('solana_public_key', 'wallet_verified', 'wallet_connected_at')
        }),
        ('Gamificación', {
            'fields': ('points', 'rank', 'profile_completion'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

## Testing

```python
import pytest
from decimal import Decimal
from datetime import date
from django.contrib.auth.models import User
from accounts.models import UserProfile, Gender, UserRank

@pytest.mark.django_db
class TestUserProfile:
    def test_profile_auto_creation(self):
        """Test que el perfil se crea automáticamente."""
        user = User.objects.create_user(username='test')
        assert hasattr(user, 'profile')
        assert user.profile.rank == UserRank.NOVATO
        assert user.profile.points == 0

    def test_profile_completion(self):
        """Test cálculo de completitud."""
        user = User.objects.create_user(username='test')
        profile = user.profile

        # Perfil vacío = 0%
        assert profile.calculate_profile_completion() == 0

        # Agregar algunos campos
        profile.weight = Decimal('70.0')
        profile.height = Decimal('175.0')
        profile.save()

        # 2 de 7 campos = ~28%
        assert profile.calculate_profile_completion() == 28

    def test_points_calculation(self):
        """Test cálculo de puntos."""
        user = User.objects.create_user(username='test')
        profile = user.profile

        # Sin datos = 0 puntos
        assert profile.calculate_points() == 0

        # Con wallet verificada
        profile.wallet_verified = True
        profile.save()
        assert profile.calculate_points() == 200

    def test_rank_progression(self):
        """Test progresión de rangos."""
        user = User.objects.create_user(username='test')
        profile = user.profile

        # Simular puntos altos
        profile.points = 5000
        profile.save()

        assert profile.update_rank() == UserRank.LEYENDA
```

## Migración desde LegacyUserProfile

Si necesitas migrar datos del modelo legacy:

```python
from landing.models import LegacyUserProfile
from accounts.models import UserProfile

def migrate_legacy_profiles():
    """Migra perfiles legacy al nuevo modelo."""
    for legacy in LegacyUserProfile.objects.all():
        profile, created = UserProfile.objects.get_or_create(
            user=legacy.user,
            defaults={
                'bio': legacy.bio,
                # Mapear otros campos compatibles
            }
        )
        if created:
            print(f"Migrated: {legacy.user.username}")
```

## Referencias

### Archivos Relacionados
- `accounts/views.py` - Vistas de perfil
- `accounts/forms.py` - Formularios de perfil
- `accounts/admin.py` - Admin personalizado
- `accounts/urls.py` - URLs de la app

### Modelos Relacionados
- [UserInventory](./userinventory.md) - Inventario del usuario
- [Subscription](./subscription.md) - Suscripciones
- [WalletTransaction](./wallettransaction.md) - Transacciones Solana
- [Product](../modelos/product.md) - Productos (personajes)

### Documentación Externa
- [Django OneToOneField](https://docs.djangoproject.com/en/stable/ref/models/fields/#onetoonefield)
- [Solana Web3.js](https://solana-labs.github.io/solana-web3.js/)

## Ver También
- [Sistema de Gamificación](../../features/gamificacion.md)
- [Integración Solana](../../features/solana-wallet.md)
- [Vistas de Perfil](../vistas/accounts-views.md)
