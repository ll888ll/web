"""
Firebase Admin SDK Service.

Permite a Django escribir directamente en Firestore con privilegios de admin.
Las credenciales se cargan desde variable de entorno o archivo.

Soporta:
- Firebase Emulator Suite para desarrollo local
- Inicialización lazy con graceful degradation
"""
from __future__ import annotations

import json
import logging
import os
from typing import TYPE_CHECKING, Optional

from django.conf import settings

from .exceptions import FirebaseServiceError

if TYPE_CHECKING:
    from google.cloud.firestore import Client as FirestoreClient

logger = logging.getLogger(__name__)


class FirebaseService:
    """
    Servicio singleton para interactuar con Firebase Admin SDK.

    Patrón: Singleton con inicialización lazy.
    Si las credenciales no están configuradas, opera en modo degradado
    (las operaciones retornan False en lugar de lanzar excepciones).
    """

    _instance: Optional[FirebaseService] = None
    _initialized: bool = False
    _db: Optional[FirestoreClient] = None
    _available: bool = False

    def __new__(cls) -> FirebaseService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not FirebaseService._initialized:
            self._initialize()
            FirebaseService._initialized = True

    def _initialize(self) -> None:
        """Inicializa Firebase Admin SDK con credenciales."""
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore
        except ImportError:
            logger.warning(
                'firebase-admin package not installed. '
                'Firebase integration will be unavailable.'
            )
            return

        # Check for emulator mode
        if getattr(settings, 'FIREBASE_USE_EMULATOR', False):
            emulator_host = getattr(
                settings, 'FIREBASE_EMULATOR_HOST', 'localhost:8080'
            )
            os.environ['FIRESTORE_EMULATOR_HOST'] = emulator_host

            auth_emulator_host = getattr(
                settings, 'FIREBASE_AUTH_EMULATOR_HOST', 'localhost:9099'
            )
            os.environ['FIREBASE_AUTH_EMULATOR_HOST'] = auth_emulator_host

            logger.info(
                f'Firebase Emulator mode enabled: '
                f'Firestore={emulator_host}, Auth={auth_emulator_host}'
            )

        try:
            # Already initialized?
            if firebase_admin._apps:
                self._db = firestore.client()
                self._available = True
                logger.info('Firebase Admin SDK already initialized')
                return

            cred = None

            # Option 1: JSON credentials from env var (production/Docker)
            cred_json = getattr(settings, 'FIREBASE_ADMIN_CREDENTIALS', '')
            if cred_json:
                cred_dict = json.loads(cred_json)
                cred = credentials.Certificate(cred_dict)
                logger.debug('Firebase credentials loaded from environment variable')

            # Option 2: Path to credentials file (local development)
            if cred is None:
                cred_path = getattr(settings, 'FIREBASE_ADMIN_CREDENTIALS_PATH', '')
                if cred_path:
                    # Handle relative paths (relative to BASE_DIR)
                    from pathlib import Path
                    path = Path(cred_path)
                    if not path.is_absolute():
                        path = settings.BASE_DIR / cred_path
                    cred = credentials.Certificate(str(path))
                    logger.debug(f'Firebase credentials loaded from file: {path}')

            # Option 3: Emulator mode without credentials
            if cred is None and getattr(settings, 'FIREBASE_USE_EMULATOR', False):
                project_id = getattr(settings, 'FIREBASE_PROJECT_ID', 'demo-project')
                firebase_admin.initialize_app(options={'projectId': project_id})
                self._db = firestore.client()
                self._available = True
                logger.info(
                    f'Firebase initialized in emulator mode with project: {project_id}'
                )
                return

            if cred is None:
                logger.warning(
                    'No Firebase credentials configured. '
                    'Firebase integration will be unavailable. '
                    'Set FIREBASE_ADMIN_CREDENTIALS or FIREBASE_ADMIN_CREDENTIALS_PATH.'
                )
                return

            firebase_admin.initialize_app(cred)
            self._db = firestore.client()
            self._available = True
            logger.info('Firebase Admin SDK initialized successfully')

        except json.JSONDecodeError as e:
            logger.error(f'Invalid JSON in FIREBASE_ADMIN_CREDENTIALS: {e}')
        except Exception as e:
            logger.error(f'Failed to initialize Firebase Admin SDK: {e}')

    @property
    def is_available(self) -> bool:
        """Indica si el servicio de Firebase está disponible."""
        return self._available

    @property
    def db(self) -> FirestoreClient:
        """Retorna el cliente de Firestore."""
        if self._db is None:
            raise FirebaseServiceError(
                'Firebase not initialized. Check credentials configuration.',
                operation='get_db'
            )
        return self._db

    # ========================================
    # SUBSCRIPTION OPERATIONS
    # ========================================

    def sync_subscription(
        self,
        firebase_uid: str,
        tier: str,
        status: str,
        started_at: str,
        expires_at: str,
        payment_tx_signature: str,
        payment_method: str = 'usdt-spl',
    ) -> bool:
        """
        Sincroniza el estado de suscripción a Firestore.

        Escribe en: users/{firebase_uid}/subscription/current

        Args:
            firebase_uid: UID del usuario en Firebase Auth
            tier: 'starter', 'pro', 'elite'
            status: 'active', 'pending', 'expired', 'cancelled'
            started_at: ISO 8601 timestamp
            expires_at: ISO 8601 timestamp
            payment_tx_signature: Firma de transacción Solana
            payment_method: Método de pago ('usdt-spl', 'sol')

        Returns:
            True si la operación fue exitosa, False si no disponible
        """
        if not self._available:
            logger.warning(
                f'Firebase unavailable. Skipping subscription sync for {firebase_uid}'
            )
            return False

        try:
            from firebase_admin import firestore as fs

            doc_ref = (
                self.db.collection('users')
                .document(firebase_uid)
                .collection('subscription')
                .document('current')
            )

            doc_ref.set({
                'tier': tier,
                'status': status,
                'startedAt': started_at,
                'expiresAt': expires_at,
                'paymentTxSignature': payment_tx_signature,
                'paymentMethod': payment_method,
                'syncedAt': fs.SERVER_TIMESTAMP,
            })

            logger.info(
                f'Subscription synced for user {firebase_uid}: {tier}/{status}'
            )
            return True

        except Exception as e:
            logger.error(f'Failed to sync subscription for {firebase_uid}: {e}')
            raise FirebaseServiceError(
                f'Failed to sync subscription: {e}',
                operation='sync_subscription'
            )

    # ========================================
    # INVENTORY OPERATIONS
    # ========================================

    def add_inventory_item(
        self,
        firebase_uid: str,
        item_id: str,
        item_type: str,
        product_id: str,
        mint_address: Optional[str] = None,
        tx_signature: Optional[str] = None,
    ) -> bool:
        """
        Agrega un item al inventario del usuario en Firestore.

        Escribe en: users/{firebase_uid}/inventory/{item_id}

        Args:
            firebase_uid: UID del usuario
            item_id: ID único del item
            item_type: 'companion', 'cosmetic', 'powerup'
            product_id: ID del producto en Django
            mint_address: Dirección del NFT (si aplica)
            tx_signature: Firma de transacción

        Returns:
            True si la operación fue exitosa, False si no disponible
        """
        if not self._available:
            logger.warning(
                f'Firebase unavailable. Skipping inventory add for {firebase_uid}'
            )
            return False

        try:
            from firebase_admin import firestore as fs

            doc_ref = (
                self.db.collection('users')
                .document(firebase_uid)
                .collection('inventory')
                .document(item_id)
            )

            data = {
                'type': item_type,
                'productId': product_id,
                'acquiredAt': fs.SERVER_TIMESTAMP,
            }

            if mint_address:
                data['mintAddress'] = mint_address
            if tx_signature:
                data['txSignature'] = tx_signature

            doc_ref.set(data)

            logger.info(f'Inventory item {item_id} added for user {firebase_uid}')
            return True

        except Exception as e:
            logger.error(f'Failed to add inventory item for {firebase_uid}: {e}')
            raise FirebaseServiceError(
                f'Failed to add inventory item: {e}',
                operation='add_inventory_item'
            )

    # ========================================
    # WALLET OPERATIONS
    # ========================================

    def sync_wallet(
        self,
        firebase_uid: str,
        solana_public_key: str,
        verified: bool = True,
    ) -> bool:
        """
        Sincroniza la wallet vinculada al perfil del usuario.

        Actualiza: users/{firebase_uid} con campo wallet

        Args:
            firebase_uid: UID del usuario
            solana_public_key: Dirección de wallet Solana (base58)
            verified: Si la wallet ha sido verificada

        Returns:
            True si la operación fue exitosa, False si no disponible
        """
        if not self._available:
            logger.warning(
                f'Firebase unavailable. Skipping wallet sync for {firebase_uid}'
            )
            return False

        try:
            from firebase_admin import firestore as fs

            doc_ref = self.db.collection('users').document(firebase_uid)

            doc_ref.set(
                {
                    'wallet': {
                        'solanaPublicKey': solana_public_key,
                        'verified': verified,
                        'linkedAt': fs.SERVER_TIMESTAMP,
                    }
                },
                merge=True,
            )

            logger.info(f'Wallet synced for user {firebase_uid}')
            return True

        except Exception as e:
            logger.error(f'Failed to sync wallet for {firebase_uid}: {e}')
            raise FirebaseServiceError(
                f'Failed to sync wallet: {e}',
                operation='sync_wallet'
            )


# Singleton instance - lazy initialization
_firebase_service: Optional[FirebaseService] = None


def get_firebase_service() -> FirebaseService:
    """
    Obtiene la instancia singleton de FirebaseService.

    Returns:
        FirebaseService singleton
    """
    global _firebase_service
    if _firebase_service is None:
        _firebase_service = FirebaseService()
    return _firebase_service


# Alias para acceso directo
firebase_service = get_firebase_service()
