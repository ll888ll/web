#!/usr/bin/env python3
"""
Script de administración completo para Croody - ULTRATHINK
==========================================================

Funciones disponibles:
- Verificar estado del admin
- Listar usuarios y modelos
- Gestión de traducciones
- Estadísticas del sistema
- Comandos de mantenimiento

Uso:
    python3 admin_utilities.py --check-admin
    python3 admin_utilities.py --list-users
    python3 admin_utilities.py --stats
    python3 admin_utilities.py --all
"""

import os
import sys
import django
import argparse
from datetime import datetime
from collections import Counter

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'croody.settings.development')
django.setup()

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.core.management import call_command
from landing.models import UserProfile
from shop.models import Product
# from telemetry.models import RobotPosition  # Disabled - no migrations


def print_header(title, char='='):
    """Imprimir header formateado."""
    print(f"\n{char * 70}")
    print(f"  {title}")
    print(f"{char * 70}\n")


def print_section(title):
    """Imprimir sección formateada."""
    print(f"\n{'-' * 70}")
    print(f"  {title}")
    print(f"{'-' * 70}")


def check_admin_status():
    """Verificar estado del admin Django."""
    print_header("ESTADO DEL ADMIN DJANGO")

    # Verificar usuario admin
    admin_users = User.objects.filter(is_superuser=True)
    print(f"👑 Superusuarios: {admin_users.count()}")
    for user in admin_users:
        print(f"   - {user.username} ({user.email}) - Last login: {user.last_login or 'Nunca'}")

    # Verificar modelos registrados
    print_section("Modelos Registrados en Admin")
    models = [
        (User, "Usuarios"),
        (UserProfile, "Perfiles de Usuario"),
        (Product, "Productos"),
        # (RobotPosition, "Posiciones de Robot"),  # Disabled - no migrations
    ]

    for model, name in models:
        try:
            count = model.objects.count()
            print(f"✓ {name}: {count} registros")
        except Exception as e:
            print(f"⚠ {name}: Error - {str(e)}")

    # Verificar contenido en BD
    print_section("Contenido en Base de Datos")
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        for table in sorted(tables):
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count} filas")


def list_users():
    """Listar todos los usuarios."""
    print_header("LISTADO DE USUARIOS")

    users = User.objects.all().order_by('date_joined')
    print(f"Total de usuarios: {users.count()}\n")

    for user in users:
        status = []
        if user.is_superuser:
            status.append("Superuser")
        if user.is_staff:
            status.append("Staff")
        if user.is_active:
            status.append("Active")
        else:
            status.append("INACTIVE")

        print(f"👤 {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Status: {', '.join(status)}")
        print(f"   Joined: {user.date_joined.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Last Login: {user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Nunca'}")


def system_stats():
    """Mostrar estadísticas del sistema."""
    print_header("ESTADÍSTICAS DEL SISTEMA")

    # Usuarios
    print_section("Usuarios")
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    superusers = User.objects.filter(is_superuser=True).count()
    staff = User.objects.filter(is_staff=True).count()

    print(f"   Total: {total_users}")
    print(f"   Activos: {active_users}")
    print(f"   Superusuarios: {superusers}")
    print(f"   Staff: {staff}")

    # Modelos
    print_section("Registros por Modelo")
    print(f"   UserProfile: {UserProfile.objects.count()}")
    print(f"   Product: {Product.objects.count()}")
    # print(f"   RobotPosition: {RobotPosition.objects.count()}")  # Disabled

    # Idiomas
    print_section("Idiomas Preferidos (UserProfile)")
    languages = UserProfile.objects.values_list('preferred_language', flat=True)
    lang_count = Counter(languages)
    for lang, count in lang_count.most_common():
        print(f"   {lang}: {count}")

    # Temas
    print_section("Temas Preferidos (UserProfile)")
    themes = UserProfile.objects.values_list('preferred_theme', flat=True)
    theme_count = Counter(themes)
    for theme, count in theme_count.most_common():
        print(f"   {theme}: {count}")


def check_translations():
    """Verificar estado de traducciones."""
    print_header("ESTADO DE TRADUCCIONES")

    locale_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale')
    if not os.path.exists(locale_dir):
        print("❌ Directorio locale no encontrado")
        return

    languages = [d for d in os.listdir(locale_dir) if os.path.isdir(os.path.join(locale_dir, d))]
    print(f"Idiomas encontrados: {len(languages)}")

    for lang in sorted(languages):
        po_file = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.po')
        mo_file = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.mo')

        po_exists = os.path.exists(po_file)
        mo_exists = os.path.exists(mo_file)

        status = "✓✓" if (po_exists and mo_exists) else "⚠"
        print(f"   {status} {lang}: .po={'✓' if po_exists else '✗'} .mo={'✓' if mo_exists else '✗'}")


def database_health():
    """Verificar salud de la base de datos."""
    print_header("SALUD DE LA BASE DE DATOS")

    try:
        with connection.cursor() as cursor:
            # Verificar tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"✓ {len(tables)} tablas encontradas")

            # Verificar integridad
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            if result[0] == 'ok':
                print("✓ Integridad de BD: OK")
            else:
                print(f"⚠ Problema de integridad: {result[0]}")

            # Estadísticas de tablas principales
            print_section("Estadísticas Detalladas")
            main_tables = ['auth_user', 'landing_userprofile', 'shop_product', 'telemetry_robotposition']
            for table in main_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   {table}: {count} registros")
                except Exception as e:
                    print(f"   {table}: Error - {str(e)}")

    except Exception as e:
        print(f"❌ Error verificando BD: {str(e)}")


def run_all_checks():
    """Ejecutar todas las verificaciones."""
    print_header("ADMINISTRACIÓN COMPLETA - CROODY", "=")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Django: {django.get_version()}")

    check_admin_status()
    list_users()
    system_stats()
    check_translations()
    database_health()

    print_header("VERIFICACIÓN COMPLETA FINALIZADA", "=")


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Administración completa para Croody - ULTRATHINK',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python3 %(prog)s --check-admin    Verificar estado del admin
  python3 %(prog)s --list-users     Listar usuarios
  python3 %(prog)s --stats          Ver estadísticas
  python3 %(prog)s --translations   Verificar traducciones
  python3 %(prog)s --database       Ver salud de BD
  python3 %(prog)s --all            Todas las verificaciones
        """
    )

    parser.add_argument('--check-admin', action='store_true',
                       help='Verificar estado del admin Django')
    parser.add_argument('--list-users', action='store_true',
                       help='Listar todos los usuarios')
    parser.add_argument('--stats', action='store_true',
                       help='Mostrar estadísticas del sistema')
    parser.add_argument('--translations', action='store_true',
                       help='Verificar estado de traducciones')
    parser.add_argument('--database', action='store_true',
                       help='Verificar salud de la base de datos')
    parser.add_argument('--all', action='store_true',
                       help='Ejecutar todas las verificaciones')

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    if args.all or args.check_admin:
        check_admin_status()
    if args.all or args.list_users:
        list_users()
    if args.all or args.stats:
        system_stats()
    if args.all or args.translations:
        check_translations()
    if args.all or args.database:
        database_health()

    if args.all:
        print("\n" + "=" * 70)
        print("✅ Verificación completa finalizada")
        print("=" * 70)


if __name__ == '__main__':
    main()