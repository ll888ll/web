#!/usr/bin/env python
"""Crear superusuario para desarrollo."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'croody.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear superusuario con credenciales predeterminadas
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@croody.app',
        password='admin123',
        is_staff=True,
        is_superuser=True,
    )
    print("✅ Superusuario creado: admin / admin123")
else:
    print("ℹ️  El superusuario 'admin' ya existe")
