# Modelo LegacyUserProfile (DEPRECATED)

> **IMPORTANTE:** Este documento describe el modelo `LegacyUserProfile` en `landing/models.py` que esta **DEPRECATED**.
>
> **Para nueva funcionalidad, usar:** [`accounts.models.UserProfile`](../accounts/userprofile.md)

## Estado de Deprecacion

| Aspecto | Detalle |
|---------|---------|
| **Modelo** | `LegacyUserProfile` (alias: `UserProfile` en landing) |
| **Ubicacion** | `/proyecto_integrado/Croody/landing/models.py` |
| **Estado** | DEPRECATED - Solo para compatibilidad |
| **Reemplazo** | `accounts.models.UserProfile` |
| **Tabla DB** | `landing_userprofile` (mantenida por compatibilidad) |

## Por Que Esta Deprecated

1. **Funcionalidad limitada**: Solo preferencias basicas (idioma, tema)
2. **Sin gamificacion**: No tiene puntos, rangos, ni sistema de logros
3. **Sin wallet Solana**: No soporta pagos blockchain
4. **Sin datos fisicos**: No almacena peso, altura, objetivos fitness
5. **Sin inventario**: No se conecta con productos adquiridos

## Modelo Recomendado: accounts.UserProfile

El nuevo modelo `accounts.UserProfile` incluye:

### Datos Fisicos
- `weight` - Peso en kg
- `height` - Altura en cm
- `birth_date` - Fecha de nacimiento
- `gender` - Genero
- `fitness_goals` - Objetivos (JSON)

### Wallet Solana
- `solana_public_key` - Direccion wallet
- `wallet_verified` - Estado de verificacion
- `wallet_connected_at` - Fecha de conexion

### Gamificacion
- `points` - Puntos totales
- `rank` - Rango (Novato, Aprendiz, Guerrero, Maestro, Leyenda)
- `profile_completion` - Porcentaje de completitud

### Avatar y Personalizacion
- `profile_picture` - Foto de perfil
- `active_character` - Personaje activo del inventario

**Documentacion completa:** [accounts/userprofile.md](../accounts/userprofile.md)

---

## Referencia del Modelo Legacy

### Estructura (Solo Referencia)

```python
class LegacyUserProfile(models.Model):
    """DEPRECATED - usar accounts.UserProfile"""

    THEME_CHOICES = (
        ("system", "Sistema"),
        ("dark", "Oscuro"),
        ("light", "Claro"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="legacy_profile",
    )
    display_name = models.CharField(max_length=120, blank=True)
    preferred_language = models.CharField(max_length=10, default="es")
    preferred_theme = models.CharField(max_length=12, choices=THEME_CHOICES, default="system")
    timezone = models.CharField(max_length=64, default="UTC")
    notification_level = models.CharField(max_length=24, default="smart")
    telemetry_alerts = models.BooleanField(default=True)
    ingest_token = models.CharField(max_length=64, unique=True, editable=False)
    favorite_robot = models.CharField(max_length=64, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'landing_userprofile'  # Mantiene tabla existente
```

### Campos Legacy vs Nuevo

| Campo Legacy | Campo Nuevo (accounts) | Notas |
|--------------|------------------------|-------|
| `user` | `user` | Mismo |
| `display_name` | - | Eliminado (usar User.first_name) |
| `preferred_language` | - | Movido a settings de Django |
| `preferred_theme` | - | Movido a localStorage frontend |
| `timezone` | - | Eliminado |
| `notification_level` | - | Eliminado |
| `telemetry_alerts` | - | Eliminado |
| `ingest_token` | - | Eliminado (autenticacion diferente) |
| `favorite_robot` | - | Eliminado |
| `bio` | `bio` | Mismo |
| - | `weight` | NUEVO |
| - | `height` | NUEVO |
| - | `birth_date` | NUEVO |
| - | `gender` | NUEVO |
| - | `fitness_goals` | NUEVO |
| - | `profile_picture` | NUEVO |
| - | `active_character` | NUEVO |
| - | `solana_public_key` | NUEVO |
| - | `wallet_verified` | NUEVO |
| - | `points` | NUEVO |
| - | `rank` | NUEVO |

## Migracion de Datos

Si tienes datos en `LegacyUserProfile` que necesitas migrar:

```python
from landing.models import LegacyUserProfile
from accounts.models import UserProfile

def migrate_legacy_profiles():
    """Migra perfiles legacy al nuevo modelo."""
    migrated = 0

    for legacy in LegacyUserProfile.objects.all():
        profile, created = UserProfile.objects.get_or_create(
            user=legacy.user,
            defaults={
                'bio': legacy.bio,
            }
        )
        if created:
            migrated += 1

    return migrated
```

## Codigo que Usa el Modelo Legacy

Si encuentras codigo que usa `landing.models.UserProfile`:

```python
# ANTES (legacy)
from landing.models import UserProfile
profile = request.user.legacy_profile

# DESPUES (nuevo)
from accounts.models import UserProfile
profile = request.user.profile
```

## Ver Tambien

- **[accounts.UserProfile](../accounts/userprofile.md)** - Modelo actual (USAR ESTE)
- **[accounts.Subscription](../accounts/subscription.md)** - Suscripciones
- **[accounts.UserInventory](../accounts/userinventory.md)** - Inventario
- **[accounts.WalletTransaction](../accounts/wallettransaction.md)** - Transacciones Solana
