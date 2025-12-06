"""
Excepciones personalizadas para servicios externos.

Estas excepciones proporcionan informacion contextual sobre errores
en integraciones con Firebase y Solana.
"""
from __future__ import annotations

from typing import Optional


class ServiceError(Exception):
    """Error base para todos los servicios externos."""

    def __init__(self, message: str, service_name: str = 'unknown'):
        super().__init__(message)
        self.service_name = service_name


class FirebaseServiceError(ServiceError):
    """Error en operaciones de Firebase Admin SDK."""

    def __init__(self, message: str, operation: Optional[str] = None):
        super().__init__(message, service_name='firebase')
        self.operation = operation

    def __str__(self) -> str:
        if self.operation:
            return f"Firebase [{self.operation}]: {super().__str__()}"
        return f"Firebase: {super().__str__()}"


class SolanaServiceError(ServiceError):
    """Error en operaciones de Solana blockchain."""

    def __init__(self, message: str, operation: Optional[str] = None):
        super().__init__(message, service_name='solana')
        self.operation = operation

    def __str__(self) -> str:
        if self.operation:
            return f"Solana [{self.operation}]: {super().__str__()}"
        return f"Solana: {super().__str__()}"


class TransactionVerificationError(SolanaServiceError):
    """
    Error al verificar una transaccion de Solana.

    Incluye informacion sobre cual verificacion fallo de las 8 posibles:
    1. signature_format - Formato de firma invalido
    2. tx_exists - Transaccion no existe en blockchain
    3. tx_confirmed - Transaccion no confirmada
    4. destination - Destino incorrecto (no es treasury)
    5. amount - Monto insuficiente
    6. token - Token incorrecto (no es USDT-SPL)
    7. timestamp - Transaccion muy antigua
    8. replay - Transaccion ya procesada (replay attack)
    """

    VALID_CHECKS = [
        'signature_format',
        'tx_exists',
        'tx_confirmed',
        'destination',
        'amount',
        'token',
        'timestamp',
        'replay',
    ]

    def __init__(
        self,
        message: str,
        check_failed: Optional[str] = None,
        tx_signature: Optional[str] = None,
    ):
        super().__init__(message, operation='verify_transaction')
        self.check_failed = check_failed
        self.tx_signature = tx_signature

    def __str__(self) -> str:
        parts = [f"Transaction verification failed: {self.args[0]}"]
        if self.check_failed:
            parts.append(f"Check failed: {self.check_failed}")
        if self.tx_signature:
            # Solo mostrar primeros 8 caracteres por seguridad
            parts.append(f"Signature: {self.tx_signature[:8]}...")
        return " | ".join(parts)
