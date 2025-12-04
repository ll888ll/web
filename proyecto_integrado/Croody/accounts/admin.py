"""Admin del ecosistema post-login de Croody."""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    UserProfile,
    UserInventory,
    Subscription,
    WalletTransaction,
    SubscriptionStatus,
    TransactionStatus,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin para perfiles de usuario."""

    list_display = [
        'user',
        'rank_badge',
        'points',
        'profile_completion_bar',
        'wallet_status',
        'updated_at',
    ]
    list_filter = ['rank', 'wallet_verified', 'gender']
    search_fields = ['user__username', 'user__email', 'solana_public_key']
    readonly_fields = ['points', 'rank', 'profile_completion', 'created_at', 'updated_at']

    fieldsets = (
        (_('Usuario'), {
            'fields': ('user',)
        }),
        (_('Datos Físicos'), {
            'fields': ('weight', 'height', 'birth_date', 'gender', 'bio', 'fitness_goals'),
            'classes': ('collapse',),
        }),
        (_('Avatar'), {
            'fields': ('profile_picture', 'active_character'),
        }),
        (_('Wallet Solana'), {
            'fields': ('solana_public_key', 'wallet_verified', 'wallet_connected_at'),
        }),
        (_('Gamificación'), {
            'fields': ('points', 'rank', 'profile_completion'),
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def rank_badge(self, obj):
        """Muestra el rango con color."""
        colors = {
            'novato': '#808080',
            'aprendiz': '#4CAF50',
            'guerrero': '#2196F3',
            'maestro': '#9C27B0',
            'leyenda': '#FFD700',
        }
        color = colors.get(obj.rank, '#808080')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_rank_display()
        )
    rank_badge.short_description = _('Rango')

    def profile_completion_bar(self, obj):
        """Muestra barra de progreso de completitud."""
        percentage = obj.profile_completion
        color = '#4CAF50' if percentage >= 80 else '#FFC107' if percentage >= 50 else '#F44336'
        return format_html(
            '<div style="width:100px; background:#ddd; border-radius:4px;">'
            '<div style="width:{}%; background:{}; height:20px; border-radius:4px; '
            'text-align:center; color:white; font-size:12px; line-height:20px;">'
            '{}%</div></div>',
            percentage, color, percentage
        )
    profile_completion_bar.short_description = _('Completitud')

    def wallet_status(self, obj):
        """Muestra estado de wallet."""
        if obj.wallet_verified:
            return format_html(
                '<span style="color: #4CAF50;">✓ Verificada</span>'
            )
        elif obj.solana_public_key:
            return format_html(
                '<span style="color: #FFC107;">⏳ Pendiente</span>'
            )
        return format_html(
            '<span style="color: #808080;">— Sin conectar</span>'
        )
    wallet_status.short_description = _('Wallet')

    actions = ['refresh_user_stats']

    @admin.action(description=_('Recalcular estadísticas de usuarios'))
    def refresh_user_stats(self, request, queryset):
        for profile in queryset:
            profile.refresh_stats()
        self.message_user(request, _('Estadísticas recalculadas correctamente.'))


@admin.register(UserInventory)
class UserInventoryAdmin(admin.ModelAdmin):
    """Admin para inventario de usuarios."""

    list_display = ['product', 'user', 'acquired_at', 'download_count', 'is_gift']
    list_filter = ['is_gift', 'acquired_at']
    search_fields = ['user__username', 'product__name', 'transaction_signature']
    raw_id_fields = ['user', 'product']
    date_hierarchy = 'acquired_at'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin para suscripciones."""

    list_display = [
        'user',
        'tier_badge',
        'status_badge',
        'days_remaining_display',
        'auto_renew',
        'expires_at',
    ]
    list_filter = ['tier', 'status', 'auto_renew']
    search_fields = ['user__username', 'user__email', 'payment_tx_signature']
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Usuario'), {
            'fields': ('user',)
        }),
        (_('Suscripción'), {
            'fields': ('tier', 'status', 'auto_renew'),
        }),
        (_('Fechas'), {
            'fields': ('started_at', 'expires_at'),
        }),
        (_('Pago'), {
            'fields': ('payment_tx_signature',),
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def tier_badge(self, obj):
        """Muestra el tier con estilo."""
        colors = {
            'starter': '#4CAF50',
            'pro': '#2196F3',
            'elite': '#FFD700',
        }
        color = colors.get(obj.tier, '#808080')
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; '
            'border-radius:4px; font-weight:bold;">{}</span>',
            color,
            obj.get_tier_display().split(' - ')[0]
        )
    tier_badge.short_description = _('Nivel')

    def status_badge(self, obj):
        """Muestra el estado con color."""
        colors = {
            SubscriptionStatus.ACTIVE: '#4CAF50',
            SubscriptionStatus.PENDING: '#FFC107',
            SubscriptionStatus.EXPIRED: '#F44336',
            SubscriptionStatus.CANCELLED: '#808080',
        }
        color = colors.get(obj.status, '#808080')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = _('Estado')

    def days_remaining_display(self, obj):
        """Muestra días restantes."""
        days = obj.days_remaining
        if days > 30:
            color = '#4CAF50'
        elif days > 7:
            color = '#FFC107'
        else:
            color = '#F44336'
        return format_html(
            '<span style="color: {};">{} días</span>',
            color,
            days
        )
    days_remaining_display.short_description = _('Días restantes')

    actions = ['activate_subscriptions', 'cancel_subscriptions']

    @admin.action(description=_('Activar suscripciones seleccionadas'))
    def activate_subscriptions(self, request, queryset):
        for sub in queryset:
            sub.activate(months=1)
        self.message_user(request, _('Suscripciones activadas.'))

    @admin.action(description=_('Cancelar suscripciones seleccionadas'))
    def cancel_subscriptions(self, request, queryset):
        for sub in queryset:
            sub.cancel()
        self.message_user(request, _('Suscripciones canceladas.'))


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    """Admin para transacciones de wallet."""

    list_display = [
        'tx_short',
        'user',
        'amount_sol',
        'purpose',
        'status_badge',
        'created_at',
        'verified_at',
    ]
    list_filter = ['status', 'purpose', 'created_at']
    search_fields = ['user__username', 'tx_signature', 'from_wallet', 'to_wallet']
    raw_id_fields = ['user', 'subscription', 'product']
    readonly_fields = ['created_at', 'verified_at', 'verification_data']
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('Transacción'), {
            'fields': ('user', 'tx_signature', 'amount_sol', 'amount_usd', 'purpose', 'status'),
        }),
        (_('Referencias'), {
            'fields': ('subscription', 'product'),
            'classes': ('collapse',),
        }),
        (_('Wallets'), {
            'fields': ('from_wallet', 'to_wallet', 'block_time'),
        }),
        (_('Verificación'), {
            'fields': ('verification_data', 'verified_at'),
            'classes': ('collapse',),
        }),
        (_('Metadata'), {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def tx_short(self, obj):
        """Muestra firma truncada."""
        return f'{obj.tx_signature[:12]}...'
    tx_short.short_description = _('TX Signature')

    def status_badge(self, obj):
        """Muestra estado con color."""
        colors = {
            TransactionStatus.PENDING: '#FFC107',
            TransactionStatus.VERIFIED: '#4CAF50',
            TransactionStatus.FAILED: '#F44336',
            TransactionStatus.EXPIRED: '#808080',
        }
        color = colors.get(obj.status, '#808080')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = _('Estado')

    actions = ['mark_as_verified', 'mark_as_failed']

    @admin.action(description=_('Marcar como verificadas'))
    def mark_as_verified(self, request, queryset):
        for tx in queryset:
            tx.mark_verified({'manual_verification': True})
        self.message_user(request, _('Transacciones marcadas como verificadas.'))

    @admin.action(description=_('Marcar como fallidas'))
    def mark_as_failed(self, request, queryset):
        for tx in queryset:
            tx.mark_failed('Rechazada manualmente')
        self.message_user(request, _('Transacciones marcadas como fallidas.'))
