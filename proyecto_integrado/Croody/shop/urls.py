"""Rutas para la tienda Buddy."""
from django.urls import path

from .views import (
    CheckoutPreviewView,
    CheckoutView,
    OrderConfirmationView,
    PaymentView,
    ProductDetailView,
    ProductListView,
    add_to_cart_view,
    cart_add_api,
    CartView,
    update_cart_item_view,
    remove_from_cart_view,
)

app_name = 'shop'


urlpatterns = [
    # Catálogo
    path('', ProductListView.as_view(), name='catalogue'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
    
    # Carrito
    path('carrito/', CartView.as_view(), name='cart'),
    path('carrito/agregar/', add_to_cart_view, name='cart-add'),
    path('carrito/actualizar/', update_cart_item_view, name='cart-update'),
    path('carrito/remover/', remove_from_cart_view, name='cart-remove'),
    path('api/cart/add/', cart_add_api, name='cart-add-api'),
    
    # Checkout y pago
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('pago/<str:order_id>/', PaymentView.as_view(), name='payment'),
    path('confirmacion/<str:order_id>/', OrderConfirmationView.as_view(), name='order-confirmation'),
    path('checkout-preview/', CheckoutPreviewView.as_view(), name='checkout-preview'),
]
