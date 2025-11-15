"""Vistas para la tienda Buddy."""
from __future__ import annotations

from typing import Any

from django.db.models import QuerySet
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView

from croody.navigation import global_search_entries, primary_nav_links

from .models import Product


class NavContextMixin:
    """Inyecta navegación y búsqueda global en el contexto."""

    def get_nav_links(self) -> list[dict[str, str]]:
        return primary_nav_links()

    def get_search_results(self) -> list[dict[str, str]]:
        return global_search_entries()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        context.setdefault('nav_links', self.get_nav_links())
        context.setdefault('search_results', self.get_search_results())
        # La tienda mantiene el verde por defecto
        context.setdefault('brand', 'gator')
        return context


class ProductListView(NavContextMixin, ListView):
    template_name = 'shop/catalogue.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self) -> QuerySet[Product]:
        queryset = Product.objects.published()
        q = self.request.GET.get('q', '').strip()
        item_type = self.request.GET.get('type', '').strip().lower()
        min_price = self.request.GET.get('min_price', '').strip()
        max_price = self.request.GET.get('max_price', '').strip()
        order = self.request.GET.get('order', '').strip()

        # Búsqueda libre
        if q:
            queryset = queryset.search(q)

        # Faceta tipo (heurística por nombre/teaser mientras no hay taxonomía)
        type_map = {
            'cofre': ['cofre', 'sobre', 'pack'],
            'set': ['set', 'tema', 'season', 'temporada'],
            'accesorio': ['accesorio', 'accesorios'],
        }
        if item_type in type_map:
            tokens = type_map[item_type]
            from django.db.models import Q
            cond = Q()
            for t in tokens:
                cond |= Q(name__icontains=t) | Q(teaser__icontains=t)
            queryset = queryset.filter(cond)

        # Rango de precio
        try:
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
        except Exception:
            pass

        # Orden
        if order == 'price_asc':
            queryset = queryset.order_by('price', 'sort_order', 'name')
        elif order == 'price_desc':
            queryset = queryset.order_by('-price', 'sort_order', 'name')
        elif order == 'recent':
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '').strip()
        context['query'] = q
        context['selected_type'] = self.request.GET.get('type', '').strip().lower()
        context['min_price'] = self.request.GET.get('min_price', '').strip()
        context['max_price'] = self.request.GET.get('max_price', '').strip()
        context['order'] = self.request.GET.get('order', '').strip()

        store_hero = {
            'eyebrow': 'Buddy Store',
            'title': 'Compra ítems oficiales Buddy y recíbelos en segundos.',
            'subtitle': (
                'Explora cofres, sets y accesorios listos para usar. Compra en dos pasos: elige y confirma.'
            ),
            'primary_cta': {'label': 'Ir al checkout', 'url': reverse('shop:checkout-preview')},
            'secondary_cta': {'label': 'Ver categorías', 'url': '#catalogo'},
            'search_placeholder': 'Busca cofres, sets, personajes o temporadas',
        }

        store_metrics = [
            {'value': '≤2 pasos', 'caption': 'elige, confirma y listo'},
            {'value': 'Pagos seguros', 'caption': 'sin fricción'},
            {'value': '24/7', 'caption': 'asistencia en compras'},
        ]

        quick_filters = [
            {'label': 'Cofres y sobres', 'hint': 'Probabilidades visibles y pity garantizado.', 'url': f"{reverse('shop:catalogue')}?type=cofre"},
            {'label': 'Sets temáticos', 'hint': 'Personajes, música y animaciones combinadas.', 'url': f"{reverse('shop:catalogue')}?type=set"},
            {'label': 'Accesorios', 'hint': 'Personaliza tus sesiones al instante.', 'url': f"{reverse('shop:catalogue')}?type=accesorio"},
        ]

        purchase_steps = [
            {
                'title': 'Selecciona tu ítem',
                'description': 'Filtra por cofres, sets o accesorios y revisa probabilidades y precio.',
            },
            {
                'title': 'Confirma la compra',
                'description': 'Revisa el resumen y valida el pago de forma segura.',
            },
            {
                'title': 'Recibe en segundos',
                'description': 'Confirmación inmediata y listo para activar en Buddy.',
            },
        ]

        payment_methods = [
            'Tarjeta de débito/crédito',
            'Apple Pay / Google Pay',
            'Otros métodos regionales',
        ]

        support_promises = [
            'Confirmación al instante en tu cuenta.',
            'Soporte 24/7 para compras.',
            'Recibos disponibles desde tu perfil.',
        ]

        context.update(
            store_hero=store_hero,
            store_metrics=store_metrics,
            quick_filters=quick_filters,
            purchase_steps=purchase_steps,
            payment_methods=payment_methods,
            support_promises=support_promises,
        )

        return context


class ProductDetailView(NavContextMixin, DetailView):
    template_name = 'shop/detail.html'
    model = Product
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self) -> QuerySet[Product]:
        return Product.objects.published()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        context['related_products'] = (
            Product.objects.published()
            .exclude(pk=context['product'].pk)
            .order_by('sort_order', 'name')[:3]
        )
        context['purchase_highlights'] = [
            'Precio final claro antes de firmar, incluyendo tarifas y royalties.',
            'Confirmación inmediata con hash verificable y recibo descargable.',
            'Soporte humano disponible en el mismo flujo si algo falla.',
        ]
        context['post_purchase_steps'] = [
            'Recibe un correo y notificación en Buddy con tu compra confirmada.',
            'Consulta el hash de la transacción y tu factura cuando lo necesites.',
            'Activa el ítem en la app Buddy o prográmalo para tu próxima rutina.',
        ]
        return context


class CheckoutPreviewView(NavContextMixin, TemplateView):
    template_name = 'shop/checkout_preview.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        steps = [
            {'step': 1, 'title': 'Añade tus datos', 'description': 'Datos de contacto y entrega.'},
            {'step': 2, 'title': 'Revisa tu pedido', 'description': 'Resumen claro antes de pagar.'},
            {'step': 3, 'title': 'Paga de forma segura', 'description': 'Tarjeta o métodos compatibles.'},
            {'step': 4, 'title': 'Confirmación inmediata', 'description': 'Recibo y activación en segundos.'},
        ]
        context['steps'] = steps
        context['checkout_notes'] = [
            'Sin sorpresas: total claro antes de pagar.',
            'Reintentos automáticos si algo falla.',
            'Ayuda disponible durante todo el proceso.',
        ]
        context['wallet_points'] = []
        context['trust_notes'] = [
            'Probabilidades visibles en cada producto.',
            'Comisiones incluidas antes del pago.',
            'Consulta recibos cuando lo necesites.',
        ]
        context['products'] = Product.objects.published()[:3]
        return context
