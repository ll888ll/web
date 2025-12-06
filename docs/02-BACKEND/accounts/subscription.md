# Modelo Subscription - Documentación Completa

## Resumen
El modelo `Subscription` gestiona las suscripciones de usuarios en el ecosistema Croody. Implementa 3 tiers de suscripción (Starter, Pro, Elite) con precios en EUR y soporte para pagos con Solana.

## Ubicación
`/proyecto_integrado/Croody/accounts/models.py`

## Tiers de Suscripción

| Tier | Precio | Puntos | Beneficios |
|------|--------|--------|------------|
| **Starter** | €19.99/mes | +300 | Acceso básico, soporte email |
| **Pro** | €59.99/mes | +500 | Acceso completo, soporte prioritario |
| **Elite** | €199.99/mes | +1000 | Acceso VIP, soporte 24/7, exclusivos |

## Estructura del Modelo

### Campos

| Campo | Tipo | Descripción | Por Defecto |
|-------|------|-------------|-------------|
| `user` | OneToOneField | Usuario (1:1) | REQUIRED |
| `tier` | CharField(20) | Nivel de suscripción | "starter" |
| `status` | CharField(20) | Estado de la suscripción | "pending" |
| `started_at` | DateTimeField | Fecha de inicio | null |
| `expires_at` | DateTimeField | Fecha de expiración | null |
| `auto_renew` | BooleanField | Renovación automática | True |
| `payment_tx_signature` | CharField(88) | Firma tx Solana del pago | "" |
| `created_at` | DateTimeField | Fecha de creación | auto |
| `updated_at` | DateTimeField | Fecha de actualización | auto |

### Choices

#### SubscriptionTier
```python
class SubscriptionTier(models.TextChoices):
    STARTER = 'starter', 'Starter - €19.99/mes'
    PRO = 'pro', 'Pro - €59.99/mes'
    ELITE = 'elite', 'Elite - €199.99/mes'
```

#### SubscriptionStatus
```python
class SubscriptionStatus(models.TextChoices):
    ACTIVE = 'active', 'Activa'
    PENDING = 'pending', 'Pendiente de pago'
    EXPIRED = 'expired', 'Expirada'
    CANCELLED = 'cancelled', 'Cancelada'
```

### Constantes

```python
TIER_PRICES = {
    SubscriptionTier.STARTER: Decimal('19.99'),
    SubscriptionTier.PRO: Decimal('59.99'),
    SubscriptionTier.ELITE: Decimal('199.99'),
}
```

## Propiedades

### price
Retorna el precio del tier actual en EUR.

```python
@property
def price(self) -> Decimal:
    """Precio del tier actual."""
    return self.TIER_PRICES.get(self.tier, Decimal('0.00'))

# Uso
subscription.price  # Decimal('59.99') para Pro
```

### is_active
Verifica si la suscripción está activa y no expirada.

```python
@property
def is_active(self) -> bool:
    """Verifica si la suscripción está activa."""
    if self.status != SubscriptionStatus.ACTIVE:
        return False
    if self.expires_at and self.expires_at < timezone.now():
        return False
    return True

# Uso
if subscription.is_active:
    # Dar acceso a features premium
    pass
```

### days_remaining
Calcula los días restantes de suscripción.

```python
@property
def days_remaining(self) -> int:
    """Días restantes de suscripción."""
    if not self.expires_at:
        return 0
    delta = self.expires_at - timezone.now()
    return max(0, delta.days)

# Uso
print(f"Te quedan {subscription.days_remaining} días")
```

## Métodos

### activate(months=1)
Activa la suscripción por N meses.

```python
def activate(self, months: int = 1) -> None:
    """Activa la suscripción por N meses."""
    from dateutil.relativedelta import relativedelta

    now = timezone.now()
    self.status = SubscriptionStatus.ACTIVE
    self.started_at = now
    self.expires_at = now + relativedelta(months=months)
    self.save()

# Uso
subscription.tier = SubscriptionTier.PRO
subscription.activate(months=12)  # 1 año
```

### cancel()
Cancela la suscripción.

```python
def cancel(self) -> None:
    """Cancela la suscripción."""
    self.status = SubscriptionStatus.CANCELLED
    self.auto_renew = False
    self.save(update_fields=['status', 'auto_renew', 'updated_at'])

# Uso
subscription.cancel()
```

### check_expiration()
Verifica y actualiza el estado si la suscripción expiró.

```python
def check_expiration(self) -> bool:
    """Verifica y actualiza estado si expiró."""
    if self.is_active:
        return True

    if self.status == SubscriptionStatus.ACTIVE:
        self.status = SubscriptionStatus.EXPIRED
        self.save(update_fields=['status', 'updated_at'])

    return False

# Uso en middleware o cron
for subscription in Subscription.objects.filter(status='active'):
    subscription.check_expiration()
```

## Patrones de Uso

### Crear suscripción nueva
```python
from accounts.models import Subscription, SubscriptionTier

# Crear suscripción pendiente
subscription = Subscription.objects.create(
    user=user,
    tier=SubscriptionTier.PRO
)

# Después de verificar pago Solana
subscription.payment_tx_signature = "5UfgJ3vN8X..."
subscription.activate(months=1)

# Actualizar puntos del usuario
user.profile.refresh_stats()
```

### Upgrade de tier
```python
def upgrade_subscription(user, new_tier):
    """Actualiza el tier de suscripción."""
    subscription = user.subscription

    # Calcular diferencia de precio (prorrateado)
    old_price = subscription.price
    new_price = Subscription.TIER_PRICES[new_tier]

    subscription.tier = new_tier
    subscription.save()

    # Recalcular puntos
    user.profile.refresh_stats()

    return subscription
```

### Verificar acceso a features
```python
def has_feature_access(user, feature):
    """Verifica si el usuario tiene acceso a una feature."""
    try:
        subscription = user.subscription
        if not subscription.is_active:
            return False

        # Features por tier
        tier_features = {
            'starter': ['basic_training', 'community'],
            'pro': ['basic_training', 'community', 'advanced_analytics', 'priority_support'],
            'elite': ['basic_training', 'community', 'advanced_analytics', 'priority_support', 'vip_content', '1on1_coaching'],
        }

        return feature in tier_features.get(subscription.tier, [])

    except Subscription.DoesNotExist:
        return False
```

### Renovación automática
```python
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import Subscription, SubscriptionStatus

class Command(BaseCommand):
    help = 'Procesa renovaciones automáticas'

    def handle(self, *args, **options):
        # Suscripciones que expiran en 3 días con auto_renew
        expiring_soon = Subscription.objects.filter(
            status=SubscriptionStatus.ACTIVE,
            auto_renew=True,
            expires_at__lte=timezone.now() + timedelta(days=3),
            expires_at__gt=timezone.now()
        )

        for subscription in expiring_soon:
            # Intentar cobro automático
            self.process_renewal(subscription)

    def process_renewal(self, subscription):
        # Lógica de cobro Solana
        pass
```

## Integración con Solana

### Flujo de pago
```
1. Usuario selecciona tier
2. Frontend genera transacción Solana
3. Usuario firma con wallet
4. Backend recibe tx_signature
5. Backend verifica on-chain
6. Si válida → activar suscripción
```

### Verificación de transacción
```python
from accounts.models import WalletTransaction, TransactionPurpose

async def verify_subscription_payment(user, tx_signature, tier):
    """Verifica pago de suscripción en Solana."""

    # Crear registro de transacción
    transaction = WalletTransaction.objects.create(
        user=user,
        tx_signature=tx_signature,
        amount_sol=calculate_sol_price(tier),
        purpose=TransactionPurpose.SUBSCRIPTION
    )

    # Verificar on-chain (pseudo-código)
    is_valid = await solana_client.verify_transaction(
        signature=tx_signature,
        expected_amount=transaction.amount_sol,
        recipient=CROODY_WALLET_ADDRESS
    )

    if is_valid:
        transaction.mark_verified()

        # Activar suscripción
        subscription, _ = Subscription.objects.get_or_create(user=user)
        subscription.tier = tier
        subscription.payment_tx_signature = tx_signature
        subscription.activate()

        return True

    transaction.mark_failed("Verification failed")
    return False
```

## Admin Django

```python
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tier', 'status', 'days_remaining', 'auto_renew', 'expires_at')
    list_filter = ('tier', 'status', 'auto_renew')
    search_fields = ('user__username', 'user__email', 'payment_tx_signature')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    actions = ['activate_subscriptions', 'cancel_subscriptions']

    def days_remaining(self, obj):
        return obj.days_remaining
    days_remaining.short_description = 'Días restantes'

    def activate_subscriptions(self, request, queryset):
        for subscription in queryset:
            subscription.activate()
        self.message_user(request, f'{queryset.count()} suscripciones activadas')
    activate_subscriptions.short_description = 'Activar suscripciones seleccionadas'

    def cancel_subscriptions(self, request, queryset):
        queryset.update(status=SubscriptionStatus.CANCELLED, auto_renew=False)
        self.message_user(request, f'{queryset.count()} suscripciones canceladas')
    cancel_subscriptions.short_description = 'Cancelar suscripciones seleccionadas'
```

## Vistas y Endpoints

### Vista de suscripción
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.models import Subscription, SubscriptionTier

@login_required
def subscription_view(request):
    """Vista principal de suscripción."""
    subscription = getattr(request.user, 'subscription', None)

    context = {
        'subscription': subscription,
        'tiers': [
            {
                'id': SubscriptionTier.STARTER,
                'name': 'Starter',
                'price': Subscription.TIER_PRICES[SubscriptionTier.STARTER],
                'features': ['Acceso básico', 'Soporte email']
            },
            {
                'id': SubscriptionTier.PRO,
                'name': 'Pro',
                'price': Subscription.TIER_PRICES[SubscriptionTier.PRO],
                'features': ['Todo de Starter', 'Analytics avanzados', 'Soporte prioritario']
            },
            {
                'id': SubscriptionTier.ELITE,
                'name': 'Elite',
                'price': Subscription.TIER_PRICES[SubscriptionTier.ELITE],
                'features': ['Todo de Pro', 'Contenido VIP', 'Coaching 1:1', 'Soporte 24/7']
            },
        ]
    }

    return render(request, 'accounts/subscription.html', context)
```

## Testing

```python
import pytest
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Subscription, SubscriptionTier, SubscriptionStatus

@pytest.mark.django_db
class TestSubscription:
    def test_tier_prices(self):
        """Test precios de tiers."""
        assert Subscription.TIER_PRICES[SubscriptionTier.STARTER] == Decimal('19.99')
        assert Subscription.TIER_PRICES[SubscriptionTier.PRO] == Decimal('59.99')
        assert Subscription.TIER_PRICES[SubscriptionTier.ELITE] == Decimal('199.99')

    def test_activate(self):
        """Test activación de suscripción."""
        user = User.objects.create_user(username='test')
        subscription = Subscription.objects.create(user=user, tier=SubscriptionTier.PRO)

        assert subscription.status == SubscriptionStatus.PENDING
        assert subscription.expires_at is None

        subscription.activate(months=1)

        assert subscription.status == SubscriptionStatus.ACTIVE
        assert subscription.expires_at is not None
        assert subscription.is_active

    def test_is_active_expired(self):
        """Test que suscripción expirada no es activa."""
        user = User.objects.create_user(username='test')
        subscription = Subscription.objects.create(
            user=user,
            tier=SubscriptionTier.STARTER,
            status=SubscriptionStatus.ACTIVE,
            expires_at=timezone.now() - timedelta(days=1)  # Expiró ayer
        )

        assert not subscription.is_active

    def test_days_remaining(self):
        """Test cálculo de días restantes."""
        user = User.objects.create_user(username='test')
        subscription = Subscription.objects.create(user=user)
        subscription.activate(months=1)

        # Debería tener ~30 días
        assert 28 <= subscription.days_remaining <= 31

    def test_cancel(self):
        """Test cancelación."""
        user = User.objects.create_user(username='test')
        subscription = Subscription.objects.create(user=user)
        subscription.activate()

        subscription.cancel()

        assert subscription.status == SubscriptionStatus.CANCELLED
        assert not subscription.auto_renew

    def test_price_property(self):
        """Test propiedad price."""
        user = User.objects.create_user(username='test')

        subscription = Subscription.objects.create(user=user, tier=SubscriptionTier.ELITE)
        assert subscription.price == Decimal('199.99')
```

## Tareas Celery (Opcionales)

```python
from celery import shared_task
from django.utils import timezone
from accounts.models import Subscription, SubscriptionStatus

@shared_task
def check_expired_subscriptions():
    """Tarea periódica para marcar suscripciones expiradas."""
    expired = Subscription.objects.filter(
        status=SubscriptionStatus.ACTIVE,
        expires_at__lt=timezone.now()
    )

    count = expired.update(status=SubscriptionStatus.EXPIRED)
    return f"Marked {count} subscriptions as expired"

@shared_task
def send_expiration_warnings():
    """Envía avisos de expiración próxima."""
    from datetime import timedelta

    expiring_soon = Subscription.objects.filter(
        status=SubscriptionStatus.ACTIVE,
        expires_at__lte=timezone.now() + timedelta(days=7),
        expires_at__gt=timezone.now()
    )

    for subscription in expiring_soon:
        send_expiration_email(subscription.user)

    return f"Sent {expiring_soon.count()} expiration warnings"
```

## Referencias

### Archivos Relacionados
- `accounts/views.py` - Vistas de suscripción
- `accounts/forms.py` - Formularios
- `templates/accounts/subscription.html` - Template

### Modelos Relacionados
- [UserProfile](./userprofile.md) - Perfil (puntos por suscripción)
- [WalletTransaction](./wallettransaction.md) - Transacciones de pago

### Documentación Externa
- [dateutil relativedelta](https://dateutil.readthedocs.io/en/stable/relativedelta.html)
- [Solana Pay](https://docs.solanapay.com/)

## Ver También
- [Flujo de Pagos Solana](../../features/solana-payments.md)
- [Sistema de Gamificación](../../features/gamificacion.md)
