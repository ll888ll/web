# Modelo WalletTransaction - Documentación Completa

## Resumen
El modelo `WalletTransaction` registra las transacciones de wallet Solana en el ecosistema Croody. Almacena transacciones pendientes de verificación y el historial de pagos verificados para suscripciones, compras de productos y donaciones.

## Ubicación
`/proyecto_integrado/Croody/accounts/models.py`

## Estructura del Modelo

### Campos Principales

| Campo | Tipo | Descripción | Por Defecto |
|-------|------|-------------|-------------|
| `user` | ForeignKey(User) | Usuario que realizó la transacción | REQUIRED |
| `tx_signature` | CharField(88) | Firma de transacción Solana (única) | REQUIRED |
| `amount_sol` | DecimalField(18,9) | Cantidad en SOL | REQUIRED |
| `amount_usd` | DecimalField(10,2) | Cantidad equivalente en USD | null |
| `purpose` | CharField(20) | Propósito de la transacción | REQUIRED |
| `status` | CharField(20) | Estado de verificación | "pending" |

### Campos de Referencias

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `subscription` | ForeignKey(Subscription) | Suscripción asociada (opcional) |
| `product` | ForeignKey(Product) | Producto comprado (opcional) |

### Campos de Verificación

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `from_wallet` | CharField(44) | Dirección wallet origen |
| `to_wallet` | CharField(44) | Dirección wallet destino (Croody) |
| `block_time` | DateTimeField | Timestamp del bloque |
| `verification_data` | JSONField | Datos adicionales de verificación |

### Campos de Metadata

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `created_at` | DateTimeField | Fecha de creación (auto) |
| `verified_at` | DateTimeField | Fecha de verificación |

### Choices

#### TransactionStatus
```python
class TransactionStatus(models.TextChoices):
    PENDING = 'pending', 'Pendiente de verificación'
    VERIFIED = 'verified', 'Verificada'
    FAILED = 'failed', 'Fallida'
    EXPIRED = 'expired', 'Expirada'
```

#### TransactionPurpose
```python
class TransactionPurpose(models.TextChoices):
    SUBSCRIPTION = 'subscription', 'Suscripción'
    PURCHASE = 'purchase', 'Compra de producto'
    TIP = 'tip', 'Propina/Donación'
```

### Meta

```python
class Meta:
    verbose_name = 'Transacción de wallet'
    verbose_name_plural = 'Transacciones de wallet'
    ordering = ['-created_at']
    indexes = [
        models.Index(fields=['user', 'status']),
        models.Index(fields=['tx_signature']),
        models.Index(fields=['status', 'created_at']),
    ]
```

## Métodos

### mark_verified()
Marca la transacción como verificada exitosamente.

```python
def mark_verified(self, verification_data: dict = None) -> None:
    """Marca la transacción como verificada."""
    self.status = TransactionStatus.VERIFIED
    self.verified_at = timezone.now()
    if verification_data:
        self.verification_data = verification_data
    self.save()

# Uso
transaction.mark_verified({
    'block_slot': 123456789,
    'confirmations': 32,
    'fee': 0.000005
})
```

### mark_failed()
Marca la transacción como fallida con razón.

```python
def mark_failed(self, reason: str = '') -> None:
    """Marca la transacción como fallida."""
    self.status = TransactionStatus.FAILED
    self.verification_data['failure_reason'] = reason
    self.save()

# Uso
transaction.mark_failed("Insufficient funds")
```

## Flujo de Verificación

```
┌─────────────────┐
│ Frontend envía  │
│ tx_signature    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Crear registro  │
│ status=PENDING  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Verificar       │
│ on-chain        │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│VERIFIED│ │FAILED │
└───┬───┘ └───────┘
    │
    ▼
┌─────────────────┐
│ Procesar acción │
│ (suscripción,   │
│  inventario)    │
└─────────────────┘
```

## Patrones de Uso

### Crear transacción pendiente
```python
from accounts.models import WalletTransaction, TransactionPurpose
from decimal import Decimal

def create_pending_transaction(user, tx_signature, amount_sol, purpose, **kwargs):
    """Crea una transacción pendiente de verificación."""
    transaction = WalletTransaction.objects.create(
        user=user,
        tx_signature=tx_signature,
        amount_sol=Decimal(str(amount_sol)),
        purpose=purpose,
        from_wallet=kwargs.get('from_wallet', user.profile.solana_public_key),
        to_wallet=kwargs.get('to_wallet', CROODY_WALLET),
        subscription=kwargs.get('subscription'),
        product=kwargs.get('product'),
    )

    return transaction
```

### Verificar transacción on-chain
```python
import httpx
from django.conf import settings

async def verify_transaction_onchain(tx_signature):
    """Verifica una transacción en la blockchain de Solana."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.SOLANA_RPC_URL,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTransaction",
                "params": [
                    tx_signature,
                    {"encoding": "json", "commitment": "confirmed"}
                ]
            }
        )

    data = response.json()

    if data.get('result') is None:
        return None  # Transacción no encontrada

    result = data['result']

    return {
        'slot': result['slot'],
        'block_time': result['blockTime'],
        'fee': result['meta']['fee'],
        'status': 'success' if result['meta']['err'] is None else 'failed',
        'pre_balances': result['meta']['preBalances'],
        'post_balances': result['meta']['postBalances'],
    }
```

### Procesar pago de suscripción
```python
from accounts.models import (
    WalletTransaction, Subscription,
    TransactionPurpose, TransactionStatus
)

async def process_subscription_payment(user, tx_signature, tier):
    """Procesa pago de suscripción con Solana."""
    # 1. Obtener o crear suscripción
    subscription, _ = Subscription.objects.get_or_create(
        user=user,
        defaults={'tier': tier}
    )

    # 2. Calcular precio en SOL
    sol_price = await get_sol_price_for_tier(tier)

    # 3. Crear registro de transacción
    transaction = WalletTransaction.objects.create(
        user=user,
        tx_signature=tx_signature,
        amount_sol=sol_price,
        purpose=TransactionPurpose.SUBSCRIPTION,
        subscription=subscription,
        from_wallet=user.profile.solana_public_key,
        to_wallet=settings.CROODY_WALLET_ADDRESS,
    )

    # 4. Verificar on-chain
    verification = await verify_transaction_onchain(tx_signature)

    if verification is None:
        transaction.mark_failed("Transaction not found on chain")
        return False, "Transacción no encontrada"

    if verification['status'] != 'success':
        transaction.mark_failed("Transaction failed on chain")
        return False, "Transacción fallida"

    # 5. Verificar monto
    # (simplificado - en producción verificar transfers exactos)

    # 6. Marcar como verificada
    transaction.mark_verified(verification)
    transaction.block_time = timezone.datetime.fromtimestamp(
        verification['block_time'],
        tz=timezone.utc
    )
    transaction.save()

    # 7. Activar suscripción
    subscription.tier = tier
    subscription.payment_tx_signature = tx_signature
    subscription.activate(months=1)

    # 8. Actualizar puntos
    user.profile.refresh_stats()

    return True, "Suscripción activada exitosamente"
```

### Procesar compra de producto
```python
async def process_product_purchase(user, tx_signature, product):
    """Procesa compra de producto con Solana."""
    from accounts.models import UserInventory

    # Calcular precio en SOL
    sol_price = await convert_eur_to_sol(product.price)

    # Crear transacción
    transaction = WalletTransaction.objects.create(
        user=user,
        tx_signature=tx_signature,
        amount_sol=sol_price,
        purpose=TransactionPurpose.PURCHASE,
        product=product,
        from_wallet=user.profile.solana_public_key,
        to_wallet=settings.CROODY_WALLET_ADDRESS,
    )

    # Verificar
    verification = await verify_transaction_onchain(tx_signature)

    if verification and verification['status'] == 'success':
        transaction.mark_verified(verification)

        # Agregar al inventario
        UserInventory.objects.create(
            user=user,
            product=product,
            transaction_signature=tx_signature
        )

        user.profile.refresh_stats()
        return True, "Producto agregado al inventario"

    transaction.mark_failed("Verification failed")
    return False, "Error al verificar transacción"
```

### Historial de transacciones
```python
def get_user_transactions(user, status=None, purpose=None):
    """Obtiene historial de transacciones del usuario."""
    queryset = user.wallet_transactions.all()

    if status:
        queryset = queryset.filter(status=status)

    if purpose:
        queryset = queryset.filter(purpose=purpose)

    return queryset.select_related('subscription', 'product')
```

### Limpiar transacciones expiradas
```python
from datetime import timedelta
from django.utils import timezone

def expire_old_pending_transactions():
    """Marca como expiradas transacciones pendientes antiguas."""
    cutoff = timezone.now() - timedelta(hours=1)

    expired_count = WalletTransaction.objects.filter(
        status=TransactionStatus.PENDING,
        created_at__lt=cutoff
    ).update(status=TransactionStatus.EXPIRED)

    return expired_count
```

## Admin Django

```python
from django.contrib import admin
from accounts.models import WalletTransaction

@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'tx_short', 'user', 'amount_sol', 'purpose',
        'status', 'created_at', 'verified_at'
    )
    list_filter = ('status', 'purpose', 'created_at')
    search_fields = ('tx_signature', 'user__username', 'from_wallet', 'to_wallet')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user', 'subscription', 'product')

    readonly_fields = ('created_at', 'verified_at', 'verification_data')

    fieldsets = (
        ('Transacción', {
            'fields': ('user', 'tx_signature', 'amount_sol', 'amount_usd')
        }),
        ('Propósito', {
            'fields': ('purpose', 'subscription', 'product')
        }),
        ('Wallets', {
            'fields': ('from_wallet', 'to_wallet')
        }),
        ('Verificación', {
            'fields': ('status', 'block_time', 'verification_data', 'verified_at')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def tx_short(self, obj):
        """Muestra firma truncada."""
        return f"{obj.tx_signature[:8]}...{obj.tx_signature[-4:]}"
    tx_short.short_description = 'Transacción'

    actions = ['verify_transactions', 'mark_as_expired']

    def verify_transactions(self, request, queryset):
        """Acción para verificar transacciones pendientes."""
        # En producción: llamar a verificación async
        for tx in queryset.filter(status='pending'):
            # Verificar on-chain...
            pass
    verify_transactions.short_description = 'Verificar transacciones seleccionadas'

    def mark_as_expired(self, request, queryset):
        """Marca transacciones como expiradas."""
        count = queryset.filter(status='pending').update(status='expired')
        self.message_user(request, f'{count} transacciones marcadas como expiradas')
    mark_as_expired.short_description = 'Marcar como expiradas'
```

## API Endpoints

### Serializer
```python
from rest_framework import serializers
from accounts.models import WalletTransaction

class WalletTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subscription_tier = serializers.CharField(source='subscription.tier', read_only=True)

    class Meta:
        model = WalletTransaction
        fields = [
            'id', 'tx_signature', 'amount_sol', 'amount_usd',
            'purpose', 'status', 'product_name', 'subscription_tier',
            'created_at', 'verified_at'
        ]
        read_only_fields = ['status', 'verified_at']

class CreateTransactionSerializer(serializers.Serializer):
    tx_signature = serializers.CharField(max_length=88)
    purpose = serializers.ChoiceField(choices=TransactionPurpose.choices)
    product_slug = serializers.CharField(required=False)
    subscription_tier = serializers.CharField(required=False)
```

### ViewSet
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

class WalletTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WalletTransactionSerializer

    def get_queryset(self):
        return self.request.user.wallet_transactions.select_related(
            'product', 'subscription'
        )

    @action(detail=False, methods=['post'])
    def submit(self, request):
        """Envía nueva transacción para verificación."""
        serializer = CreateTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Crear y procesar transacción
        # ...

        return Response({'status': 'pending'}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get'])
    def check_status(self, request, pk=None):
        """Verifica estado de una transacción."""
        transaction = self.get_object()
        return Response({
            'status': transaction.status,
            'verified_at': transaction.verified_at
        })
```

## Testing

```python
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from accounts.models import (
    WalletTransaction, TransactionStatus,
    TransactionPurpose, Subscription
)

@pytest.mark.django_db
class TestWalletTransaction:
    @pytest.fixture
    def user(self):
        user = User.objects.create_user(username='test')
        user.profile.solana_public_key = "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU"
        user.profile.save()
        return user

    def test_create_transaction(self, user):
        """Test creación de transacción."""
        tx = WalletTransaction.objects.create(
            user=user,
            tx_signature="5UfgJ3vN8X" + "a" * 78,
            amount_sol=Decimal('0.5'),
            purpose=TransactionPurpose.SUBSCRIPTION
        )

        assert tx.status == TransactionStatus.PENDING
        assert tx.verified_at is None

    def test_unique_signature(self, user):
        """Test que signature es única."""
        signature = "5UfgJ3vN8X" + "b" * 78

        WalletTransaction.objects.create(
            user=user,
            tx_signature=signature,
            amount_sol=Decimal('0.5'),
            purpose=TransactionPurpose.TIP
        )

        with pytest.raises(Exception):  # IntegrityError
            WalletTransaction.objects.create(
                user=user,
                tx_signature=signature,  # Duplicada
                amount_sol=Decimal('0.3'),
                purpose=TransactionPurpose.TIP
            )

    def test_mark_verified(self, user):
        """Test marcar como verificada."""
        tx = WalletTransaction.objects.create(
            user=user,
            tx_signature="5UfgJ3vN8X" + "c" * 78,
            amount_sol=Decimal('1.0'),
            purpose=TransactionPurpose.PURCHASE
        )

        tx.mark_verified({'block_slot': 123456})

        tx.refresh_from_db()
        assert tx.status == TransactionStatus.VERIFIED
        assert tx.verified_at is not None
        assert tx.verification_data['block_slot'] == 123456

    def test_mark_failed(self, user):
        """Test marcar como fallida."""
        tx = WalletTransaction.objects.create(
            user=user,
            tx_signature="5UfgJ3vN8X" + "d" * 78,
            amount_sol=Decimal('0.1'),
            purpose=TransactionPurpose.TIP
        )

        tx.mark_failed("Insufficient balance")

        tx.refresh_from_db()
        assert tx.status == TransactionStatus.FAILED
        assert tx.verification_data['failure_reason'] == "Insufficient balance"

    def test_ordering(self, user):
        """Test ordenamiento por fecha."""
        tx1 = WalletTransaction.objects.create(
            user=user,
            tx_signature="tx1" + "a" * 85,
            amount_sol=Decimal('0.1'),
            purpose=TransactionPurpose.TIP
        )
        tx2 = WalletTransaction.objects.create(
            user=user,
            tx_signature="tx2" + "b" * 85,
            amount_sol=Decimal('0.2'),
            purpose=TransactionPurpose.TIP
        )

        transactions = list(user.wallet_transactions.all())
        assert transactions[0] == tx2  # Más reciente primero
```

## Tareas Celery

```python
from celery import shared_task
from accounts.models import WalletTransaction, TransactionStatus

@shared_task
def verify_pending_transactions():
    """Verifica transacciones pendientes."""
    pending = WalletTransaction.objects.filter(
        status=TransactionStatus.PENDING
    ).order_by('created_at')[:100]

    verified = 0
    failed = 0

    for tx in pending:
        result = verify_transaction_sync(tx.tx_signature)

        if result and result['status'] == 'success':
            tx.mark_verified(result)
            verified += 1
        elif result:
            tx.mark_failed(result.get('error', 'Unknown error'))
            failed += 1

    return f"Verified: {verified}, Failed: {failed}"

@shared_task
def cleanup_expired_transactions():
    """Limpia transacciones pendientes expiradas."""
    from datetime import timedelta
    from django.utils import timezone

    cutoff = timezone.now() - timedelta(hours=24)

    count = WalletTransaction.objects.filter(
        status=TransactionStatus.PENDING,
        created_at__lt=cutoff
    ).update(status=TransactionStatus.EXPIRED)

    return f"Expired {count} transactions"
```

## Configuración Solana

```python
# settings.py
SOLANA_NETWORK = env('SOLANA_NETWORK', default='devnet')  # 'devnet' o 'mainnet-beta'

SOLANA_RPC_URLS = {
    'devnet': 'https://api.devnet.solana.com',
    'mainnet-beta': 'https://api.mainnet-beta.solana.com',
}

SOLANA_RPC_URL = SOLANA_RPC_URLS[SOLANA_NETWORK]

# Wallet de Croody para recibir pagos
CROODY_WALLET_ADDRESS = env('CROODY_WALLET_ADDRESS')
```

## Referencias

### Archivos Relacionados
- `accounts/views.py` - Endpoints de transacciones
- `accounts/tasks.py` - Tareas Celery
- `services/solana-verifier/` - Servicio de verificación

### Modelos Relacionados
- [UserProfile](./userprofile.md) - Wallet del usuario
- [Subscription](./subscription.md) - Suscripciones
- [UserInventory](./userinventory.md) - Compras

### Documentación Externa
- [Solana JSON RPC API](https://docs.solana.com/developing/clients/jsonrpc-api)
- [Solana Web3.js](https://solana-labs.github.io/solana-web3.js/)
- [Solana Pay](https://docs.solanapay.com/)

## Ver También
- [Integración Solana](../../features/solana-integration.md)
- [Flujo de Pagos](../../features/payment-flows.md)
