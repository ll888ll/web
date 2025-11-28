"""Rutas para la tienda Buddy."""
from django.urls import path

from .views import CheckoutPreviewView, ProductDetailView, ProductListView, cart_add_api


app_name = 'shop'


urlpatterns = [
    path('', ProductListView.as_view(), name='catalogue'),
    path('api/cart/add/', cart_add_api, name='cart-add-api'),
    path('checkout-preview/', CheckoutPreviewView.as_view(), name='checkout-preview'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
]


