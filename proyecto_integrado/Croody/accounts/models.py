"""Modelos del ecosistema post-login de Croody.

Incluye:
- UserProfile: Perfil extendido con datos físicos y wallet
- UserInventory: Items adquiridos por el usuario
- Subscription: Gestión de suscripciones (3 tiers)
- WalletTransaction: Log de transacciones Solana
"""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.contrib.auth.models import User


# ========================================
# CHOICES
# ========================================

class Gender(models.TextChoices):
    """Opciones de género."""
    MALE = 'male', _('Masculino')
    FEMALE = 'female', _('Femenino')
    NON_BINARY = 'non_binary', _('No binario')
    PREFER_NOT_SAY = 'prefer_not_say', _('Prefiero no decir')


class SubscriptionTier(models.TextChoices):
    """Niveles de suscripción."""
    STARTER = 'starter', _('Starter - €19.99/mes')
    PRO = 'pro', _('Pro - €59.99/mes')
    ELITE = 'elite', _('Elite - €199.99/mes')


class SubscriptionStatus(models.TextChoices):
    """Estados de suscripción."""
    ACTIVE = 'active', _('Activa')
    PENDING = 'pending', _('Pendiente de pago')
    EXPIRED = 'expired', _('Expirada')
    CANCELLED = 'cancelled', _('Cancelada')


class TransactionStatus(models.TextChoices):
    """Estados de transacción blockchain."""
    PENDING = 'pending', _('Pendiente de verificación')
    VERIFIED = 'verified', _('Verificada')
    FAILED = 'failed', _('Fallida')
    EXPIRED = 'expired', _('Expirada')


class TransactionPurpose(models.TextChoices):
    """Propósito de la transacción."""
    SUBSCRIPTION = 'subscription', _('Suscripción')
    PURCHASE = 'purchase', _('Compra de producto')
    TIP = 'tip', _('Propina/Donación')


class UserRank(models.TextChoices):
    """Rangos de usuario basados en puntos."""
    NOVATO = 'novato', _('Novato')
    APRENDIZ = 'aprendiz', _('Aprendiz')
    GUERRERO = 'guerrero', _('Guerrero')
    MAESTRO = 'maestro', _('Maestro')
    LEYENDA = 'leyenda', _('Leyenda')


# ========================================
# MODELS
# ========================================

class UserProfile(models.Model):
    """Perfil extendido del usuario.

    Incluye datos físicos, configuración de avatar,
    wallet Solana y sistema de puntos/gamificación.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('Usuario')
    )

    # ---- Datos físicos ----
    weight = models.DecimalField(
        _('Peso (kg)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    height = models.DecimalField(
        _('Altura (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    birth_date = models.DateField(
        _('Fecha de nacimiento'),
        null=True,
        blank=True
    )
    gender = models.CharField(
        _('Género'),
        max_length=20,
        choices=Gender.choices,
        blank=True
    )
    fitness_goals = models.JSONField(
        _('Objetivos de fitness'),
        default=list,
        blank=True
    )
    bio = models.TextField(
        _('Biografía'),
        max_length=500,
        blank=True
    )

    # ---- Avatar y personalización ----
    profile_picture = models.ImageField(
        _('Foto de perfil'),
        upload_to='avatars/',
        null=True,
        blank=True
    )
    active_character = models.ForeignKey(
        'shop.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='active_for_users',
        verbose_name=_('Personaje activo'),
        help_text=_('Debe ser un item del inventario del usuario')
    )

    # ---- Wallet Solana ----
    solana_public_key = models.CharField(
        _('Llave pública Solana'),
        max_length=44,
        blank=True,
        help_text=_('Dirección de wallet Solana (base58)')
    )
    wallet_verified = models.BooleanField(
        _('Wallet verificada'),
        default=False
    )
    wallet_connected_at = models.DateTimeField(
        _('Fecha de conexión de wallet'),
        null=True,
        blank=True
    )

    # ---- Gamificación ----
    points = models.PositiveIntegerField(
        _('Puntos'),
        default=0
    )
    rank = models.CharField(
        _('Rango'),
        max_length=20,
        choices=UserRank.choices,
        default=UserRank.NOVATO
    )
    profile_completion = models.PositiveSmallIntegerField(
        _('Completitud del perfil (%)'),
        default=0
    )

    # ---- Metadata ----
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Perfil de usuario')
        verbose_name_plural = _('Perfiles de usuario')

    def __str__(self) -> str:
        return f'Perfil de {self.user.username}'

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

    def calculate_points(self) -> int:
        """Calcula los puntos totales del usuario."""
        points = 0

        # Puntos por perfil completo
        completion = self.calculate_profile_completion()
        if completion == 100:
            points += 500
        else:
            points += int(completion * 3)  # Hasta 300 puntos parciales

        # Puntos por wallet
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

        # Puntos por suscripción
        try:
            subscription = self.user.subscription
            if subscription.status == SubscriptionStatus.ACTIVE:
                tier_points = {
                    SubscriptionTier.STARTER: 300,
                    SubscriptionTier.PRO: 500,
                    SubscriptionTier.ELITE: 1000,
                }
                points += tier_points.get(subscription.tier, 0)
        except Subscription.DoesNotExist:
            pass

        return points

    def update_rank(self) -> str:
        """Actualiza el rango basado en los puntos."""
        points = self.calculate_points()

        if points >= 5000:
            new_rank = UserRank.LEYENDA
        elif points >= 3000:
            new_rank = UserRank.MAESTRO
        elif points >= 1500:
            new_rank = UserRank.GUERRERO
        elif points >= 500:
            new_rank = UserRank.APRENDIZ
        else:
            new_rank = UserRank.NOVATO

        return new_rank

    def refresh_stats(self) -> None:
        """Recalcula y guarda puntos, rango y completitud."""
        self.profile_completion = self.calculate_profile_completion()
        self.points = self.calculate_points()
        self.rank = self.update_rank()
        self.save(update_fields=['profile_completion', 'points', 'rank', 'updated_at'])


class UserInventory(models.Model):
    """Item del inventario del usuario.

    Representa un producto adquirido por el usuario,
    ya sea por compra directa o como beneficio de suscripción.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name=_('Usuario')
    )
    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='inventory_entries',
        verbose_name=_('Producto')
    )
    acquired_at = models.DateTimeField(
        _('Fecha de adquisición'),
        auto_now_add=True
    )
    transaction_signature = models.CharField(
        _('Firma de transacción'),
        max_length=88,
        blank=True,
        help_text=_('Signature de la transacción Solana')
    )
    download_count = models.PositiveIntegerField(
        _('Descargas'),
        default=0
    )
    is_gift = models.BooleanField(
        _('Es regalo'),
        default=False
    )
    notes = models.TextField(
        _('Notas'),
        blank=True
    )

    class Meta:
        verbose_name = _('Item de inventario')
        verbose_name_plural = _('Items de inventario')
        unique_together = ['user', 'product']
        ordering = ['-acquired_at']

    def __str__(self) -> str:
        return f'{self.product.name} - {self.user.username}'

    def increment_download(self) -> None:
        """Incrementa el contador de descargas."""
        self.download_count += 1
        self.save(update_fields=['download_count'])


class Subscription(models.Model):
    """Suscripción del usuario.

    Gestiona los 3 tiers de suscripción:
    - Starter: €19.99/mes
    - Pro: €59.99/mes
    - Elite: €199.99/mes
    """
    TIER_PRICES = {
        SubscriptionTier.STARTER: Decimal('19.99'),
        SubscriptionTier.PRO: Decimal('59.99'),
        SubscriptionTier.ELITE: Decimal('199.99'),
    }

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name=_('Usuario')
    )
    tier = models.CharField(
        _('Nivel'),
        max_length=20,
        choices=SubscriptionTier.choices,
        default=SubscriptionTier.STARTER
    )
    status = models.CharField(
        _('Estado'),
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.PENDING
    )
    started_at = models.DateTimeField(
        _('Fecha de inicio'),
        null=True,
        blank=True
    )
    expires_at = models.DateTimeField(
        _('Fecha de expiración'),
        null=True,
        blank=True
    )
    auto_renew = models.BooleanField(
        _('Renovación automática'),
        default=True
    )
    payment_tx_signature = models.CharField(
        _('Firma de transacción de pago'),
        max_length=88,
        blank=True
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Suscripción')
        verbose_name_plural = _('Suscripciones')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.get_tier_display()}'

    @property
    def price(self) -> Decimal:
        """Precio del tier actual."""
        return self.TIER_PRICES.get(self.tier, Decimal('0.00'))

    @property
    def is_active(self) -> bool:
        """Verifica si la suscripción está activa."""
        if self.status != SubscriptionStatus.ACTIVE:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True

    @property
    def days_remaining(self) -> int:
        """Días restantes de suscripción."""
        if not self.expires_at:
            return 0
        delta = self.expires_at - timezone.now()
        return max(0, delta.days)

    def activate(self, months: int = 1) -> None:
        """Activa la suscripción por N meses."""
        now = timezone.now()
        self.status = SubscriptionStatus.ACTIVE
        self.started_at = now

        # Calcular expiración
        from dateutil.relativedelta import relativedelta
        self.expires_at = now + relativedelta(months=months)

        self.save()

    def cancel(self) -> None:
        """Cancela la suscripción."""
        self.status = SubscriptionStatus.CANCELLED
        self.auto_renew = False
        self.save(update_fields=['status', 'auto_renew', 'updated_at'])

    def check_expiration(self) -> bool:
        """Verifica y actualiza estado si expiró."""
        if self.is_active:
            return True

        if self.status == SubscriptionStatus.ACTIVE:
            self.status = SubscriptionStatus.EXPIRED
            self.save(update_fields=['status', 'updated_at'])

        return False


class WalletTransaction(models.Model):
    """Registro de transacción de wallet Solana.

    Almacena las transacciones pendientes de verificación
    y el historial de pagos verificados.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet_transactions',
        verbose_name=_('Usuario')
    )
    tx_signature = models.CharField(
        _('Firma de transacción'),
        max_length=88,
        unique=True,
        help_text=_('Transaction signature de Solana')
    )
    amount_sol = models.DecimalField(
        _('Cantidad (SOL)'),
        max_digits=18,
        decimal_places=9
    )
    amount_usd = models.DecimalField(
        _('Cantidad (USD)'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    purpose = models.CharField(
        _('Propósito'),
        max_length=20,
        choices=TransactionPurpose.choices
    )
    status = models.CharField(
        _('Estado'),
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING
    )

    # Referencias opcionales
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name=_('Suscripción')
    )
    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wallet_transactions',
        verbose_name=_('Producto')
    )

    # Datos de verificación
    from_wallet = models.CharField(
        _('Wallet origen'),
        max_length=44,
        blank=True
    )
    to_wallet = models.CharField(
        _('Wallet destino'),
        max_length=44,
        blank=True,
        help_text=_('Wallet de Croody')
    )
    block_time = models.DateTimeField(
        _('Tiempo de bloque'),
        null=True,
        blank=True
    )
    verification_data = models.JSONField(
        _('Datos de verificación'),
        default=dict,
        blank=True
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(
        _('Fecha de verificación'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Transacción de wallet')
        verbose_name_plural = _('Transacciones de wallet')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['tx_signature']),
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self) -> str:
        return f'{self.tx_signature[:8]}... - {self.amount_sol} SOL'

    def mark_verified(self, verification_data: dict = None) -> None:
        """Marca la transacción como verificada."""
        self.status = TransactionStatus.VERIFIED
        self.verified_at = timezone.now()
        if verification_data:
            self.verification_data = verification_data
        self.save()

    def mark_failed(self, reason: str = '') -> None:
        """Marca la transacción como fallida."""
        self.status = TransactionStatus.FAILED
        self.verification_data['failure_reason'] = reason
        self.save()


# ========================================
# SIGNALS
# ========================================

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un perfil automáticamente cuando se crea un usuario."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Guarda el perfil cuando se guarda el usuario."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
