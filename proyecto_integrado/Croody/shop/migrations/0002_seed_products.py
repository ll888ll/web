from decimal import Decimal

from django.db import migrations


def seed_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    data = [
        {
            'name': 'Buddy One',
            'slug': 'buddy-one',
            'teaser': 'El compañero esencial. Materiales reciclables, IA Croody Core.',
            'description': 'Diseñado con proporción áurea en cada componente. Integración total con Croody Cloud y soporte 24/7.',
            'price': Decimal('99.00'),
            'delivery_estimate': 'Entrega 6 días',
            'badge_label': '3·6·9',
            'sort_order': 1,
        },
        {
            'name': 'Buddy Plus',
            'slug': 'buddy-plus',
            'teaser': 'Productividad aumentada. Sensores hápticos y sincronización en tiempo real.',
            'description': 'Ideal para equipos creativos. Incluye acceso a Croody OS y dashboards métricos en vivo.',
            'price': Decimal('149.00'),
            'delivery_estimate': 'Entrega 3 días',
            'badge_label': 'Φ Power',
            'sort_order': 2,
        },
        {
            'name': 'Buddy Pro',
            'slug': 'buddy-pro',
            'teaser': 'Para líderes visionarios. Seguridad multinube, control por gestos y asistencia predictiva.',
            'description': 'Construido con materiales premium. Incluye garantías extendidas y soporte dedicado nivel 33°.',
            'price': Decimal('199.00'),
            'delivery_estimate': 'Entrega 2 días',
            'badge_label': '33°',
            'sort_order': 3,
        },
    ]
    for item in data:
        Product.objects.update_or_create(slug=item['slug'], defaults=item)


def remove_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Product.objects.filter(slug__in=['buddy-one', 'buddy-plus', 'buddy-pro']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_products, remove_products),
    ]

