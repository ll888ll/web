# App Accounts - Documentación

## Resumen
La app `accounts` gestiona el ecosistema post-login de Croody, incluyendo perfiles de usuario extendidos, inventario de productos, suscripciones y transacciones de wallet Solana.

## Ubicación
`/proyecto_integrado/Croody/accounts/`

## Modelos

| Modelo | Descripción | Documentación |
|--------|-------------|---------------|
| **UserProfile** | Perfil extendido con datos físicos, avatar, wallet Solana y gamificación | [userprofile.md](./userprofile.md) |
| **UserInventory** | Items adquiridos por el usuario (productos, personajes) | [userinventory.md](./userinventory.md) |
| **Subscription** | Gestión de suscripciones (Starter, Pro, Elite) | [subscription.md](./subscription.md) |
| **WalletTransaction** | Registro de transacciones Solana | [wallettransaction.md](./wallettransaction.md) |

## Choices (Enumeraciones)

### Gender
```python
MALE = 'male'
FEMALE = 'female'
NON_BINARY = 'non_binary'
PREFER_NOT_SAY = 'prefer_not_say'
```

### UserRank
```python
NOVATO = 'novato'      # 0-499 puntos
APRENDIZ = 'aprendiz'  # 500-1499 puntos
GUERRERO = 'guerrero'  # 1500-2999 puntos
MAESTRO = 'maestro'    # 3000-4999 puntos
LEYENDA = 'leyenda'    # 5000+ puntos
```

### SubscriptionTier
```python
STARTER = 'starter'  # €19.99/mes
PRO = 'pro'          # €59.99/mes
ELITE = 'elite'      # €199.99/mes
```

### SubscriptionStatus
```python
ACTIVE = 'active'
PENDING = 'pending'
EXPIRED = 'expired'
CANCELLED = 'cancelled'
```

### TransactionStatus
```python
PENDING = 'pending'
VERIFIED = 'verified'
FAILED = 'failed'
EXPIRED = 'expired'
```

### TransactionPurpose
```python
SUBSCRIPTION = 'subscription'
PURCHASE = 'purchase'
TIP = 'tip'
```

## Estructura de Archivos

```
accounts/
├── __init__.py
├── admin.py        # Configuración del admin Django
├── apps.py         # Configuración de la app
├── forms.py        # Formularios de perfil y suscripción
├── models.py       # Modelos (UserProfile, Subscription, etc.)
├── tests.py        # Tests unitarios
├── urls.py         # URLs de la app
└── views.py        # Vistas de perfil, inventario, etc.
```

## Señales

### Creación automática de perfil
Cuando se crea un `User`, automáticamente se crea un `UserProfile` asociado:

```python
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

## Sistema de Gamificación

### Cálculo de Puntos

| Acción | Puntos |
|--------|--------|
| Perfil 100% completo | +500 |
| Perfil parcial | +3 por cada % |
| Wallet Solana verificada | +200 |
| Foto de perfil | +100 |
| Personaje activo | +50 |
| Cada item en inventario | +50 |
| Suscripción Starter | +300 |
| Suscripción Pro | +500 |
| Suscripción Elite | +1000 |

### Progresión de Rangos

| Rango | Puntos Requeridos |
|-------|-------------------|
| Novato | 0-499 |
| Aprendiz | 500-1499 |
| Guerrero | 1500-2999 |
| Maestro | 3000-4999 |
| Leyenda | 5000+ |

## Integración con Solana

### Wallet del Usuario
- Dirección pública almacenada en `UserProfile.solana_public_key`
- Estado de verificación en `UserProfile.wallet_verified`
- Fecha de conexión en `UserProfile.wallet_connected_at`

### Flujo de Pago
1. Usuario selecciona producto/suscripción
2. Frontend genera transacción Solana
3. Usuario firma con su wallet
4. Backend recibe `tx_signature`
5. Backend verifica on-chain
6. Si válida → procesar acción (activar suscripción, agregar a inventario)

### Wallet de Croody
Configurada en `settings.CROODY_WALLET_ADDRESS`

## Relaciones entre Modelos

```
User
 ├── profile (OneToOne) → UserProfile
 │    └── active_character (FK) → Product
 │
 ├── subscription (OneToOne) → Subscription
 │    └── transactions (FK) → WalletTransaction[]
 │
 ├── inventory_items (FK) → UserInventory[]
 │    └── product (FK) → Product
 │
 └── wallet_transactions (FK) → WalletTransaction[]
      ├── subscription (FK) → Subscription
      └── product (FK) → Product
```

## URLs

```python
# accounts/urls.py
urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile-edit'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('subscription/', views.subscription_view, name='subscription'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('wallet/connect/', views.wallet_connect, name='wallet-connect'),
    path('transactions/', views.transactions_view, name='transactions'),
]
```

## Migraciones

La app `accounts` requiere que exista la app `shop` (para `Product`).

```bash
python manage.py makemigrations accounts
python manage.py migrate accounts
```

## Testing

```bash
# Ejecutar tests de la app
python manage.py test accounts

# Con pytest
pytest proyecto_integrado/Croody/accounts/tests.py -v
```

## Ver También

- [Landing App (Legacy)](../modelos/userprofile-legacy.md) - Modelo legacy `LegacyUserProfile`
- [Shop App](../modelos/product.md) - Modelo `Product`
- [Integración Solana](../../features/solana-integration.md)
- [Sistema de Gamificación](../../features/gamificacion.md)
