"""Vistas del ecosistema post-login de Croody."""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from shop.models import Product

from .forms import ProfileEditForm, WalletConnectForm
from .models import (
    Subscription,
    SubscriptionStatus,
    SubscriptionTier,
    UserInventory,
    UserProfile,
    WalletTransaction,
)


# ========================================
# DASHBOARD
# ========================================

class DashboardView(LoginRequiredMixin, TemplateView):
    """Vista principal del dashboard post-login."""

    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = user.profile

        # Actualizar stats
        profile.refresh_stats()

        context.update({
            'profile': profile,
            'inventory_count': user.inventory_items.count(),
            'recent_items': user.inventory_items.select_related('product')[:5],
            'subscription': getattr(user, 'subscription', None),
        })
        return context


# ========================================
# PROFILE
# ========================================

class ProfileView(LoginRequiredMixin, DetailView):
    """Vista del perfil del usuario."""

    model = UserProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Vista para editar el perfil."""

    model = UserProfile
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.refresh_stats()
        messages.success(self.request, _('Perfil actualizado correctamente.'))
        return response


# ========================================
# INVENTORY
# ========================================

class InventoryView(LoginRequiredMixin, ListView):
    """Vista del inventario del usuario."""

    model = UserInventory
    template_name = 'accounts/inventory.html'
    context_object_name = 'items'
    paginate_by = 12

    def get_queryset(self):
        return self.request.user.inventory_items.select_related('product')


class InventoryItemDetailView(LoginRequiredMixin, DetailView):
    """Vista de detalle de un item del inventario."""

    model = UserInventory
    template_name = 'accounts/inventory_detail.html'
    context_object_name = 'item'

    def get_queryset(self):
        return self.request.user.inventory_items.select_related('product')


@login_required
def download_item(request, pk):
    """Descarga un item del inventario."""
    item = get_object_or_404(
        UserInventory.objects.select_related('product'),
        pk=pk,
        user=request.user
    )

    # Incrementar contador de descargas
    item.increment_download()

    # TODO: Implementar lógica real de descarga
    # Por ahora, redirigir con mensaje
    messages.success(
        request,
        _('Descarga iniciada para "%(name)s"') % {'name': item.product.name}
    )
    return redirect('accounts:inventory')


@login_required
def set_active_character(request, pk):
    """Establece un item como personaje activo."""
    item = get_object_or_404(
        UserInventory.objects.select_related('product'),
        pk=pk,
        user=request.user
    )

    profile = request.user.profile
    profile.active_character = item.product
    profile.save(update_fields=['active_character', 'updated_at'])
    profile.refresh_stats()

    messages.success(
        request,
        _('Personaje activo cambiado a "%(name)s"') % {'name': item.product.name}
    )
    return redirect('accounts:inventory')


# ========================================
# SHOP (Internal)
# ========================================

class ShopView(LoginRequiredMixin, ListView):
    """Tienda interna para usuarios logueados."""

    model = Product
    template_name = 'accounts/shop.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.published().exclude(
            # Excluir productos que ya tiene el usuario
            pk__in=self.request.user.inventory_items.values_list('product_id', flat=True)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owned_count'] = self.request.user.inventory_items.count()
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Detalle de producto en la tienda."""

    model = Product
    template_name = 'accounts/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owned'] = UserInventory.objects.filter(
            user=self.request.user,
            product=self.object
        ).exists()
        return context


# ========================================
# SUBSCRIPTIONS
# ========================================

class SubscriptionView(LoginRequiredMixin, TemplateView):
    """Vista de gestión de suscripciones."""

    template_name = 'accounts/subscriptions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Suscripción actual del usuario
        try:
            subscription = self.request.user.subscription
        except Subscription.DoesNotExist:
            subscription = None

        context.update({
            'subscription': subscription,
            'tiers': [
                {
                    'id': SubscriptionTier.STARTER,
                    'name': 'Starter',
                    'price': '19.99',
                    'features': [
                        _('Acceso básico'),
                        _('5 descargas/mes'),
                        _('Soporte por email'),
                    ],
                },
                {
                    'id': SubscriptionTier.PRO,
                    'name': 'Pro',
                    'price': '59.99',
                    'features': [
                        _('Acceso completo'),
                        _('Descargas ilimitadas'),
                        _('Soporte prioritario'),
                        _('Personajes exclusivos'),
                    ],
                    'popular': True,
                },
                {
                    'id': SubscriptionTier.ELITE,
                    'name': 'Elite',
                    'price': '199.99',
                    'features': [
                        _('Todo lo de Pro'),
                        _('Acceso anticipado'),
                        _('NFTs exclusivos'),
                        _('Sesiones 1-on-1'),
                        _('Badge Elite'),
                    ],
                },
            ],
        })
        return context


@login_required
def subscribe(request, tier):
    """Iniciar proceso de suscripción."""
    if tier not in [t[0] for t in SubscriptionTier.choices]:
        messages.error(request, _('Plan de suscripción no válido.'))
        return redirect('accounts:subscriptions')

    # Crear o actualizar suscripción pendiente
    subscription, created = Subscription.objects.update_or_create(
        user=request.user,
        defaults={
            'tier': tier,
            'status': SubscriptionStatus.PENDING,
        }
    )

    messages.info(
        request,
        _('Por favor, completa el pago para activar tu suscripción.')
    )
    return redirect('accounts:wallet')


@login_required
def cancel_subscription(request):
    """Cancelar suscripción actual."""
    try:
        subscription = request.user.subscription
        subscription.cancel()
        messages.success(request, _('Suscripción cancelada.'))
    except Subscription.DoesNotExist:
        messages.error(request, _('No tienes una suscripción activa.'))

    return redirect('accounts:subscriptions')


# ========================================
# WALLET
# ========================================

class WalletView(LoginRequiredMixin, TemplateView):
    """Vista de gestión de wallet."""

    template_name = 'accounts/wallet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile

        context.update({
            'profile': profile,
            'transactions': self.request.user.wallet_transactions.all()[:10],
            'form': WalletConnectForm(instance=profile),
            # Wallet de Croody para recibir pagos (placeholder)
            'croody_wallet': 'CroodyWa11etPub1icKeyHereXXXXXXXXXXXX',
        })
        return context


class WalletConnectView(LoginRequiredMixin, View):
    """Conectar/desconectar wallet."""

    def post(self, request):
        profile = request.user.profile
        form = WalletConnectForm(request.POST, instance=profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.wallet_connected_at = timezone.now()
            profile.wallet_verified = False  # Requiere verificación
            profile.save()
            profile.refresh_stats()

            messages.success(request, _('Wallet conectada. Pendiente de verificación.'))
        else:
            messages.error(request, _('Error al conectar wallet.'))

        return redirect('accounts:wallet')


@login_required
def disconnect_wallet(request):
    """Desconectar wallet."""
    profile = request.user.profile
    profile.solana_public_key = ''
    profile.wallet_verified = False
    profile.wallet_connected_at = None
    profile.save()
    profile.refresh_stats()

    messages.success(request, _('Wallet desconectada.'))
    return redirect('accounts:wallet')


# ========================================
# POINTS & GAMIFICATION
# ========================================

class PointsView(LoginRequiredMixin, TemplateView):
    """Vista del sistema de puntos."""

    template_name = 'accounts/points.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        profile.refresh_stats()

        context.update({
            'profile': profile,
            'ranks': [
                {'name': 'Novato', 'min_points': 0, 'icon': 'seedling'},
                {'name': 'Aprendiz', 'min_points': 500, 'icon': 'leaf'},
                {'name': 'Guerrero', 'min_points': 1500, 'icon': 'tree'},
                {'name': 'Maestro', 'min_points': 3000, 'icon': 'crown'},
                {'name': 'Leyenda', 'min_points': 5000, 'icon': 'star'},
            ],
            'point_sources': [
                {'action': _('Perfil completo'), 'points': 500},
                {'action': _('Wallet verificada'), 'points': 200},
                {'action': _('Foto de perfil'), 'points': 100},
                {'action': _('Personaje activo'), 'points': 50},
                {'action': _('Cada item en inventario'), 'points': 50},
                {'action': _('Suscripción Starter'), 'points': 300},
                {'action': _('Suscripción Pro'), 'points': 500},
                {'action': _('Suscripción Elite'), 'points': 1000},
            ],
        })
        return context


# ========================================
# API ENDPOINTS (For AJAX)
# ========================================

@login_required
def api_profile_stats(request):
    """API: Obtener stats del perfil."""
    profile = request.user.profile
    profile.refresh_stats()

    return JsonResponse({
        'points': profile.points,
        'rank': profile.rank,
        'rank_display': profile.get_rank_display(),
        'profile_completion': profile.profile_completion,
        'wallet_verified': profile.wallet_verified,
    })


@login_required
def api_inventory_count(request):
    """API: Obtener contador de inventario."""
    return JsonResponse({
        'count': request.user.inventory_items.count(),
    })
