"""Rutas para la tienda Buddy."""
from django.urls import path

from .views import CheckoutPreviewView, ProductDetailView, ProductListView


app_name = 'shop'


urlpatterns = [
    path('', ProductListView.as_view(), name='catalogue'),
    path('checkout-preview/', CheckoutPreviewView.as_view(), name='checkout-preview'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
]

