"""
Solana Blockchain Verification Service.

Verifica transacciones en la blockchain de Solana antes de activar suscripciones.
Implementa las 8 capas de seguridad documentadas en la arquitectura.

Checklist de verificación:
1. signature_format - Formato de firma válido
2. tx_exists - Transacción existe en blockchain
3. tx_confirmed - Transacción confirmada
4. destination - Destino es treasury wallet
5. amount - Monto suficiente
6. token - Token correcto (USDT-SPL)
7. timestamp - Transacción reciente
8. replay - No procesada anteriormente
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, Optional, Tuple

from django.conf import settings
from django.core.cache import cache

from .exceptions import SolanaServiceError, TransactionVerificationError

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


@dataclass
class TransactionVerification:
    """Resultado de verificación de transacción."""

    is_valid: bool
    signature: str
    from_wallet: Optional[str] = None
    to_wallet: Optional[str] = None
    amount: Optional[Decimal] = None
    token_mint: Optional[str] = None
    block_time: Optional[datetime] = None
    error: Optional[str] = None
    check_failed: Optional[str] = None


class SolanaService:
    """
    Servicio para verificar transacciones en Solana.

    Patrón: Singleton con inicialización lazy.
    Soporta modo degradado si las dependencias no están instaladas.
    """

    _instance: Optional[SolanaService] = None
    _initialized: bool = False
    _available: bool = False
    _client = None

    # Tiempo máximo de antigüedad de transacción (1 hora)
    MAX_TX_AGE_SECONDS = 3600

    # Cache key prefix para replay attack prevention
    USED_TX_CACHE_PREFIX = 'solana_tx_used:'

    def __new__(cls) -> SolanaService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not SolanaService._initialized:
            self._initialize()
            SolanaService._initialized = True

    def _initialize(self) -> None:
        """Inicializa el cliente de Solana RPC."""
        try:
            from solana.rpc.api import Client
        except ImportError:
            logger.warning(
                'solana package not installed. '
                'Solana verification will be unavailable.'
            )
            return

        rpc_url = getattr(settings, 'SOLANA_RPC_URL', '')
        if not rpc_url:
            logger.warning(
                'SOLANA_RPC_URL not configured. '
                'Solana verification will be unavailable.'
            )
            return

        try:
            self._client = Client(rpc_url)
            self._available = True
            logger.info(f'Solana RPC client initialized: {rpc_url}')
        except Exception as e:
            logger.error(f'Failed to initialize Solana client: {e}')

    @property
    def is_available(self) -> bool:
        """Indica si el servicio de Solana está disponible."""
        return self._available

    @property
    def treasury_wallet(self) -> str:
        """Wallet treasury de Croody."""
        return getattr(settings, 'SOLANA_TREASURY_WALLET', '')

    @property
    def usdt_mint(self) -> str:
        """Dirección del token USDT-SPL."""
        return getattr(settings, 'SOLANA_USDT_MINT', '')

    @property
    def tx_cache_timeout(self) -> int:
        """TTL para el cache de transacciones usadas (replay prevention)."""
        return getattr(settings, 'SOLANA_TX_CACHE_TIMEOUT', 604800)  # 7 días

    def verify_subscription_payment(
        self,
        tx_signature: str,
        expected_amount: Decimal,
        user_wallet: str,
    ) -> TransactionVerification:
        """
        Verifica un pago de suscripción en Solana.

        Implementa el checklist de 8 verificaciones:
        1. signature_format - ¿Formato de firma válido?
        2. tx_exists - ¿La transacción existe en blockchain?
        3. tx_confirmed - ¿El status es "confirmed"?
        4. destination - ¿El destino es nuestra treasury wallet?
        5. amount - ¿El monto es >= al precio del producto?
        6. token - ¿El token es USDT-SPL?
        7. timestamp - ¿La transacción es reciente (< 1 hora)?
        8. replay - ¿No ha sido usada antes (replay attack)?

        Args:
            tx_signature: Firma de transacción Solana (base58)
            expected_amount: Monto esperado en USDT
            user_wallet: Wallet del usuario que debería ser el origen

        Returns:
            TransactionVerification con resultado de la verificación
        """
        if not self._available:
            logger.warning('Solana service unavailable. Skipping verification.')
            return TransactionVerification(
                is_valid=False,
                signature=tx_signature,
                error='Solana service unavailable',
                check_failed='service_unavailable',
            )

        try:
            from solana.rpc.commitment import Confirmed
            from solders.signature import Signature
        except ImportError:
            return TransactionVerification(
                is_valid=False,
                signature=tx_signature,
                error='Solana packages not installed',
                check_failed='service_unavailable',
            )

        # Check 1: Validar formato de signature
        try:
            sig = Signature.from_string(tx_signature)
        except Exception:
            return TransactionVerification(
                is_valid=False,
                signature=tx_signature,
                error='Invalid transaction signature format',
                check_failed='signature_format',
            )

        # Check 8: Replay attack prevention (check first, before network call)
        cache_key = f'{self.USED_TX_CACHE_PREFIX}{tx_signature}'
        if cache.get(cache_key):
            return TransactionVerification(
                is_valid=False,
                signature=tx_signature,
                error='Transaction already used (replay attack prevented)',
                check_failed='replay',
            )

        try:
            # Check 2 & 3: Fetch transaction with confirmed commitment
            response = self._client.get_transaction(
                sig,
                encoding='jsonParsed',
                commitment=Confirmed,
                max_supported_transaction_version=0,
            )

            if response.value is None:
                return TransactionVerification(
                    is_valid=False,
                    signature=tx_signature,
                    error='Transaction not found or not confirmed',
                    check_failed='tx_exists',
                )

            tx = response.value

            # Check 7: Transaction age
            block_time = tx.block_time
            tx_datetime = None
            if block_time:
                tx_datetime = datetime.fromtimestamp(block_time, tz=timezone.utc)
                age = datetime.now(timezone.utc) - tx_datetime
                if age > timedelta(seconds=self.MAX_TX_AGE_SECONDS):
                    return TransactionVerification(
                        is_valid=False,
                        signature=tx_signature,
                        block_time=tx_datetime,
                        error=f'Transaction too old ({age.total_seconds():.0f}s > {self.MAX_TX_AGE_SECONDS}s)',
                        check_failed='timestamp',
                    )

            # Parse transaction for token transfer
            transfer_info = self._extract_token_transfer(tx)

            if transfer_info is None:
                return TransactionVerification(
                    is_valid=False,
                    signature=tx_signature,
                    error='No valid token transfer found in transaction',
                    check_failed='token',
                )

            from_wallet, to_wallet, amount, token_mint = transfer_info

            # Check: Wallet ownership (sender is user)
            if from_wallet != user_wallet:
                return TransactionVerification(
                    is_valid=False,
                    signature=tx_signature,
                    from_wallet=from_wallet,
                    error=f'Transaction sender {from_wallet[:8]}... does not match user wallet',
                    check_failed='destination',
                )

            # Check 4: Destination is treasury
            if to_wallet != self.treasury_wallet:
                return TransactionVerification(
                    is_valid=False,
                    signature=tx_signature,
                    to_wallet=to_wallet,
                    error=f'Destination is not treasury wallet',
                    check_failed='destination',
                )

            # Check 6: Token is USDT-SPL
            if self.usdt_mint and token_mint != self.usdt_mint:
                return TransactionVerification(
                    is_valid=False,
                    signature=tx_signature,
                    token_mint=token_mint,
                    error=f'Token is not USDT-SPL',
                    check_failed='token',
                )

            # Check 5: Amount is sufficient
            if amount < expected_amount:
                return TransactionVerification(
                    is_valid=False,
                    signature=tx_signature,
                    amount=amount,
                    error=f'Amount {amount} is less than expected {expected_amount}',
                    check_failed='amount',
                )

            # All checks passed - mark as used to prevent replay
            cache.set(cache_key, True, self.tx_cache_timeout)

            logger.info(
                f'Transaction {tx_signature[:8]}... verified: '
                f'{amount} USDT from {from_wallet[:8]}... to treasury'
            )

            return TransactionVerification(
                is_valid=True,
                signature=tx_signature,
                from_wallet=from_wallet,
                to_wallet=to_wallet,
                amount=amount,
                token_mint=token_mint,
                block_time=tx_datetime,
            )

        except Exception as e:
            logger.exception(f'Error verifying transaction {tx_signature[:16]}...')
            raise SolanaServiceError(
                f'Transaction verification failed: {e}',
                operation='verify_subscription_payment',
            )

    def _extract_token_transfer(
        self, tx
    ) -> Optional[Tuple[str, str, Decimal, str]]:
        """
        Extrae información de transferencia de token de una transacción.

        Soporta tanto SPL Token como Token-2022.

        Returns:
            Tuple de (from_wallet, to_wallet, amount, token_mint) o None
        """
        try:
            meta = tx.transaction.meta
            if meta is None:
                return None

            # Buscar en post_token_balances para Token-2022
            pre_balances = {
                b.account_index: b for b in (meta.pre_token_balances or [])
            }
            post_balances = {
                b.account_index: b for b in (meta.post_token_balances or [])
            }

            for idx, post in post_balances.items():
                if idx in pre_balances:
                    pre = pre_balances[idx]

                    # Calcular diferencia
                    pre_amount = Decimal(
                        pre.ui_token_amount.ui_amount_string or '0'
                    )
                    post_amount = Decimal(
                        post.ui_token_amount.ui_amount_string or '0'
                    )

                    diff = post_amount - pre_amount

                    # Si es un incremento, es el receptor
                    if diff > 0:
                        # Encontrar el sender
                        for sender_idx, sender_pre in pre_balances.items():
                            if sender_idx != idx:
                                sender_post = post_balances.get(sender_idx)
                                if sender_post:
                                    sender_pre_amount = Decimal(
                                        sender_pre.ui_token_amount.ui_amount_string
                                        or '0'
                                    )
                                    sender_post_amount = Decimal(
                                        sender_post.ui_token_amount.ui_amount_string
                                        or '0'
                                    )
                                    sender_diff = sender_post_amount - sender_pre_amount

                                    if sender_diff < 0 and abs(sender_diff) >= diff:
                                        return (
                                            sender_pre.owner,  # from
                                            post.owner,  # to
                                            diff,  # amount
                                            post.mint,  # token mint
                                        )

            return None

        except Exception as e:
            logger.error(f'Error extracting token transfer: {e}')
            return None

    def check_wallet_balance(
        self, wallet_address: str, token_mint: Optional[str] = None
    ) -> Optional[Decimal]:
        """
        Verifica el balance de una wallet.

        Args:
            wallet_address: Dirección de la wallet (base58)
            token_mint: Dirección del token (None para SOL nativo)

        Returns:
            Balance en la unidad del token, o None si error
        """
        if not self._available:
            return None

        try:
            import base58
            from solders.pubkey import Pubkey

            pubkey = Pubkey.from_string(wallet_address)

            if token_mint is None:
                # Balance de SOL nativo
                response = self._client.get_balance(pubkey)
                if response.value is not None:
                    # Convertir lamports a SOL
                    return Decimal(response.value) / Decimal(10**9)
            else:
                # Balance de token SPL
                token_pubkey = Pubkey.from_string(token_mint)
                response = self._client.get_token_accounts_by_owner(
                    pubkey, {'mint': token_pubkey}
                )
                if response.value:
                    # Sum all token account balances
                    total = Decimal(0)
                    for account in response.value:
                        data = account.account.data
                        if hasattr(data, 'parsed'):
                            amount = data.parsed['info']['tokenAmount']['uiAmount']
                            if amount:
                                total += Decimal(str(amount))
                    return total

            return None

        except Exception as e:
            logger.error(f'Error checking wallet balance: {e}')
            return None


# Singleton instance - lazy initialization
_solana_service: Optional[SolanaService] = None


def get_solana_service() -> SolanaService:
    """
    Obtiene la instancia singleton de SolanaService.

    Returns:
        SolanaService singleton
    """
    global _solana_service
    if _solana_service is None:
        _solana_service = SolanaService()
    return _solana_service


# Alias para acceso directo
solana_service = get_solana_service()
