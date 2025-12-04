"""URLs del ecosistema post-login de Croody."""
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),

    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),

    # Inventory
    path('inventory/', views.InventoryView.as_view(), name='inventory'),
    path('inventory/<int:pk>/', views.InventoryItemDetailView.as_view(), name='inventory_detail'),
    path('inventory/<int:pk>/download/', views.download_item, name='download'),
    path('inventory/<int:pk>/set-active/', views.set_active_character, name='set_active'),

    # Shop (Internal)
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('shop/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Subscriptions
    path('subscriptions/', views.SubscriptionView.as_view(), name='subscriptions'),
    path('subscriptions/subscribe/<str:tier>/', views.subscribe, name='subscribe'),
    path('subscriptions/cancel/', views.cancel_subscription, name='cancel_subscription'),

    # Wallet
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    path('wallet/connect/', views.WalletConnectView.as_view(), name='wallet_connect'),
    path('wallet/disconnect/', views.disconnect_wallet, name='wallet_disconnect'),

    # Points & Gamification
    path('points/', views.PointsView.as_view(), name='points'),

    # API Endpoints
    path('api/stats/', views.api_profile_stats, name='api_stats'),
    path('api/inventory/count/', views.api_inventory_count, name='api_inventory_count'),
]
