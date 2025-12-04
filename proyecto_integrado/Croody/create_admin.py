#!/usr/bin/env python
"""Script para crear usuario admin de Django de forma no interactiva."""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'croody.settings.development')
django.setup()

from django.contrib.auth.models import User

# Verificar si el usuario ya existe
username = '888'
email = 'admin@croody.app'
password = '12345*JoseAdmin280905'

if User.objects.filter(username=username).exists():
    print(f"⚠️  Usuario '{username}' ya existe. Actualizando...")
    user = User.objects.get(username=username)
    user.email = email
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"✅ Usuario '{username}' actualizado exitosamente")
else:
    print(f"🔧 Creando usuario admin '{username}'...")
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print(f"✅ Usuario '{username}' creado exitosamente")

print(f"""
📋 CREDENCIALES DE ACCESO ADMIN:
   Username: {username}
   Password: {password}
   Email: {email}
   URL Admin: http://localhost:8000/admin/
""")