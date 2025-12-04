"""Vistas para la tienda Buddy."""
from __future__ import annotations

from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, FormView, ListView, TemplateView, View

from croody.navigation import global_search_entries, primary_nav_links

from .forms import Cart, CheckoutForm, PaymentForm
from .models import Order, OrderItem, OrderStatus, PaymentStatus, Product, Transaction


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

    def get_queryset(self):
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
            'primary_cta': {'label': 'Ir al checkout', 'url': reverse('shop:cart')},
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

    def get_queryset(self):
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


# ===== VISTAS DE CARRITO =====

class CartView(NavContextMixin, TemplateView):
    """Vista del carrito de compras."""
    template_name = 'shop/cart.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        
        context['cart'] = cart
        context['cart_items'] = list(cart)
        context['cart_total'] = cart.get_total_price()
        context['item_count'] = cart.get_item_count()
        
        return context


@require_http_methods(['POST'])
def add_to_cart_view(request):
    """Vista para agregar productos al carrito (HTMX)."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if not product_id:
        return HttpResponseBadRequest('Product ID is required')
    
    product = get_object_or_404(Product, id=product_id, is_published=True)
    
    cart = Cart(request)
    cart.add(product_id, quantity)
    
    if request.headers.get('HX-Request'):
        # Respuesta para HTMX
        cart_count = cart.get_item_count()
        cart_total = cart.get_total_price()
        
        return render(request, 'shop/partials/cart-indicator.html', {
            'cart_count': cart_count,
            'cart_total': cart_total,
        })
    else:
        # Respuesta normal
        messages.success(
            request,
            f'{product.name} agregado al carrito'
        )
        return redirect('shop:cart')


@require_http_methods(['POST'])
def update_cart_item_view(request):
    """Vista para actualizar cantidad de un item en el carrito."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if not product_id:
        return HttpResponseBadRequest('Product ID is required')
    
    cart = Cart(request)
    cart.update_quantity(product_id, quantity)
    
    if request.headers.get('HX-Request'):
        # Respuesta HTMX - recargar carrito
        context = {
            'cart': cart,
            'cart_items': list(cart),
            'cart_total': cart.get_total_price(),
            'item_count': cart.get_item_count(),
        }
        return render(request, 'shop/partials/cart-items.html', context)
    else:
        return redirect('shop:cart')


@require_http_methods(['POST'])
def remove_from_cart_view(request):
    """Vista para remover un item del carrito."""
    product_id = request.POST.get('product_id')
    
    if not product_id:
        return HttpResponseBadRequest('Product ID is required')
    
    cart = Cart(request)
    cart.remove(product_id)
    
    if request.headers.get('HX-Request'):
        # Respuesta HTMX - recargar carrito
        context = {
            'cart': cart,
            'cart_items': list(cart),
            'cart_total': cart.get_total_price(),
            'item_count': cart.get_item_count(),
        }
        return render(request, 'shop/partials/cart-items.html', context)
    else:
        return redirect('shop:cart')


# ===== VISTAS DE CHECKOUT =====

@method_decorator(login_required, name='dispatch')
class CheckoutView(NavContextMixin, FormView):
    """Vista del formulario de checkout."""
    template_name = 'shop/checkout.html'
    form_class = CheckoutForm
    
    def dispatch(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart:
            messages.warning(request, 'Tu carrito está vacío.')
            return redirect('shop:catalogue')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        
        context['cart_items'] = list(cart)
        context['cart_total'] = cart.get_total_price()
        context['item_count'] = cart.get_item_count()
        
        return context
    
    def form_valid(self, form: CheckoutForm) -> HttpResponseRedirect:
        """Procesar datos de checkout."""
        cart = Cart(self.request)
        
        if not cart:
            messages.error(self.request, 'Tu carrito está vacío.')
            return redirect('shop:catalogue')
        
        # Crear orden
        order_data = form.cleaned_data.copy()
        order_data['user'] = self.request.user
        
        order = Order.objects.create(**order_data)
        
        # Agregar items a la orden
        for item_data in cart:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=price,
                subtotal=price * quantity
            )
        
        # Calcular total final
        order.calculate_total()
        order.save()
        
        # Limpiar carrito
        cart.clear()
        
        # Redirigir a pago
        messages.success(
            self.request,
            f'Orden #{order.id} creada exitosamente. Continúa con el pago.'
        )
        return redirect('shop:payment', order_id=order.id)


@method_decorator(login_required, name='dispatch')
class PaymentView(NavContextMixin, FormView):
    """Vista para procesar el pago."""
    template_name = 'shop/payment.html'
    form_class = PaymentForm
    
    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(
            Order,
            id=kwargs['order_id'],
            user=request.user
        )
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        context['order_items'] = self.order.items.all()
        
        return context
    
    def form_valid(self, form: PaymentForm) -> HttpResponseRedirect:
        """Procesar pago (simulado)."""
        # Crear transacción
        transaction = Transaction.objects.create(
            order=self.order,
            amount=self.order.total,
            status=PaymentStatus.COMPLETED,
            provider='stripe',
            provider_id=f'sim_{self.order.id}',
            provider_response={
                'card_last4': form.cleaned_data['card_number'][-4:],
                'status': 'succeeded'
            }
        )
        
        # Actualizar estado de la orden
        self.order.payment_status = PaymentStatus.COMPLETED
        self.order.status = OrderStatus.CONFIRMED
        self.order.save()
        
        messages.success(
            self.request,
            f'Pago exitoso para la orden #{self.order.id}'
        )
        
        return redirect('shop:order-confirmation', order_id=self.order.id)


@method_decorator(login_required, name='dispatch')
class OrderConfirmationView(NavContextMixin, TemplateView):
    """Vista de confirmación de orden."""
    template_name = 'shop/order_confirmation.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(
            Order,
            id=kwargs['order_id'],
            user=request.user
        )
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        context['order_items'] = self.order.items.all()
        
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


@csrf_exempt
@require_http_methods(['POST'])
def cart_add_api(request):
    """API endpoint para agregar productos al carrito."""
    import json

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')

        if not product_id:
            return JsonResponse(
                {'success': False, 'error': 'product_id es requerido'},
                status=400
            )

        product = Product.objects.filter(id=product_id, is_published=True).first()

        if not product:
            return JsonResponse(
                {'success': False, 'error': 'Producto no encontrado'},
                status=404
            )

        cart = Cart(request)
        cart.add(product_id, 1)

        return JsonResponse({
            'success': True,
            'message': f'{product.name} agregado al carrito',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'slug': product.slug
            }
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {'success': False, 'error': 'JSON inválido'},
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {'success': False, 'error': f'Error del servidor: {str(e)}'},
            status=500
        )
