#!/usr/bin/env python3
"""
Script para crear productos de ejemplo en la tienda Buddy.
Ejecutar con: python3 create_products.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'croody.settings')
django.setup()

from shop.models import Product


def create_products():
    """Crear productos de ejemplo para la tienda."""

    products = [
        {
            'name': 'Buddy Pro - Plan Mensual',
            'slug': 'buddy-pro-mensual',
            'teaser': 'Acceso completo a Buddy AI con todas las funciones premium',
            'description': 'Obtén el máximo de tu entrenamiento con Buddy Pro. Incluye: rutinas personalizadas ilimitadas, análisis de progreso con IA, planes nutricionales personalizados, acceso prioritario a nuevas funciones, soporte 24/7.',
            'price': 29.99,
            'delivery_estimate': 'Acceso instantáneo',
            'badge_label': 'Popular',
            'is_published': True,
            'sort_order': 1
        },
        {
            'name': 'Buddy Basic - Plan Mensual',
            'slug': 'buddy-basic-mensual',
            'teaser': 'Perfecto para comenzar tu journey fitness con IA',
            'description': 'Inicia tu transformación con Buddy Basic. Incluye: rutinas personalizadas, seguimiento básico de progreso, biblioteca de ejercicios, recordatorios inteligentes.',
            'price': 9.99,
            'delivery_estimate': 'Acceso instantáneo',
            'badge_label': 'Ideal para empezar',
            'is_published': True,
            'sort_order': 2
        },
        {
            'name': 'Buddy Pro - Plan Anual',
            'slug': 'buddy-pro-anual',
            'teaser': 'Ahorra 2 meses con el plan anual de Buddy Pro',
            'description': 'Comprométete con tu transformación anual. Todas las funciones de Buddy Pro + 2 meses gratis +礼包 exclusivo anual con accesorios fitness.',
            'price': 299.99,
            'delivery_estimate': 'Acceso instantáneo',
            'badge_label': 'Mejor precio',
            'is_published': True,
            'sort_order': 3
        },
        {
            'name': 'Luks Pack - 1000 Luks',
            'slug': 'luks-pack-1000',
            'teaser': 'Moneda virtual para acceder a contenido premium',
            'description': 'Los Luks son la moneda oficial de Croody. Úsalos para desbloquear rutinas exclusivas, accesorios virtuales, temas premium y mucho más.',
            'price': 4.99,
            'delivery_estimate': 'Entrega inmediata',
            'badge_label': 'Nuevo',
            'is_published': True,
            'sort_order': 4
        },
        {
            'name': 'Luks Pack - 5000 Luks',
            'slug': 'luks-pack-5000',
            'teaser': 'Pack medio para usuarios regulares',
            'description': 'Perfecto para usuarios que quieren aprovechar al máximo el ecosistema Croody. Incluye bonus de 500 Luks adicionales.',
            'price': 19.99,
            'delivery_estimate': 'Entrega inmediata',
            'badge_label': 'Recomendado',
            'is_published': True,
            'sort_order': 5
        },
        {
            'name': 'Luks Pack - 10000 Luks',
            'slug': 'luks-pack-10000',
            'teaser': 'Máximo valor para usuarios dedicados',
            'description': 'El pack definitivo. Incluye 12,000 Luks (bonus de 20%) + acceso anticipado a nuevas funciones + badge exclusivo de usuario VIP.',
            'price': 34.99,
            'delivery_estimate': 'Entrega inmediata',
            'badge_label': 'VIP',
            'is_published': True,
            'sort_order': 6
        },
        {
            'name': 'Rutina Personalizada Premium',
            'slug': 'rutina-personalizada-premium',
            'teaser': 'Plan de entrenamiento 100% diseñado para ti por expertos',
            'description': 'Nuestros entrenadores certificados crearán una rutina única basada en tus objetivos, experiencia, limitaciones y preferencias. Incluye seguimiento semanal y ajustes constantes.',
            'price': 49.99,
            'delivery_estimate': 'Entrega en 48h',
            'badge_label': 'Personalizado',
            'is_published': True,
            'sort_order': 7
        },
        {
            'name': 'Plan Nutricional Completo',
            'slug': 'plan-nutricional-completo',
            'teaser': 'Nutrición personalizada que se adapta a tu cuerpo y objetivos',
            'description': 'Recibe un plan nutricional detallado con recetas, listas de compras, timing de nutrientes y sugerencias de suplementación. Ajustado a tus restricciones alimentarias.',
            'price': 39.99,
            'delivery_estimate': 'Entrega en 72h',
            'badge_label': 'Esencial',
            'is_published': True,
            'sort_order': 8
        },
        {
            'name': 'Buddy Premium Skin Pack',
            'slug': 'buddy-premium-skin-pack',
            'teaser': 'Personaliza tu experiencia visual con Buddy',
            'description': 'Expresarte es importante. Este pack incluye: 5 temas exclusivos de Buddy, 20 fondos de pantalla HD, animaciones premium, efectos de sonido únicos.',
            'price': 14.99,
            'delivery_estimate': 'Entrega inmediata',
            'badge_label': 'Cosmético',
            'is_published': True,
            'sort_order': 9
        },
        {
            'name': 'Mentoría 1:1 con Entrenador',
            'slug': 'mentoria-1a1',
            'teaser': 'Sesión privada con un entrenador certificado',
            'description': 'Una sesión de 60 minutos por videollamada con uno de nuestros entrenadores certificados. Revisión de técnica, ajustes de rutina, resolución de dudas específicas.',
            'price': 79.99,
            'delivery_estimate': 'Programar en 24h',
            'badge_label': 'Premium',
            'is_published': True,
            'sort_order': 10
        },
    ]

    created = 0
    for product_data in products:
        # Verificar si ya existe
        if Product.objects.filter(slug=product_data['slug']).exists():
            print(f'⏭️  Ya existe: {product_data["name"]}')
            continue

        # Crear producto
        product = Product.objects.create(**product_data)
        created += 1
        print(f'✅ Creado: {product.name} - ${product.price}')

    print(f'\n🎉 ¡Listo! {created} productos creados.')
    print(f'📊 Total de productos en la tienda: {Product.objects.count()}')


if __name__ == '__main__':
    print('🚀 Creando productos para la tienda Buddy...\n')
    create_products()
