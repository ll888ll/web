"""
Servicios externos de Croody.

Este paquete contiene servicios para integraciones con:
- Firebase Admin SDK (sincronizacion con Buddy app)
- Solana blockchain (verificacion de pagos)

Usage:
    from croody.services import firebase_service, solana_service

    # Sync subscription to Firebase
    firebase_service.sync_subscription(
        firebase_uid='user123',
        tier='pro',
        status='active',
        started_at='2025-01-01T00:00:00Z',
        expires_at='2025-02-01T00:00:00Z',
        payment_tx_signature='abc123...'
    )

    # Verify Solana payment
    result = solana_service.verify_subscription_payment(
        tx_signature='abc123...',
        expected_amount=Decimal('9.99'),
        user_wallet='So1ana...'
    )
"""
from .exceptions import (
    FirebaseServiceError,
    ServiceError,
    SolanaServiceError,
    TransactionVerificationError,
)
from .firebase_service import FirebaseService, firebase_service, get_firebase_service
from .solana_service import (
    SolanaService,
    TransactionVerification,
    get_solana_service,
    solana_service,
)

__all__ = [
    # Firebase
    'FirebaseService',
    'firebase_service',
    'get_firebase_service',
    # Solana
    'SolanaService',
    'solana_service',
    'get_solana_service',
    'TransactionVerification',
    # Exceptions
    'ServiceError',
    'FirebaseServiceError',
    'SolanaServiceError',
    'TransactionVerificationError',
]
