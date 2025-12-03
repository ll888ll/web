# Troubleshooting y Problemas Comunes - Documentación Completa

## Resumen
Esta guía proporciona soluciones paso a paso para los problemas más comunes encontrados en el proyecto Croody, cubriendo errores de Django, FastAPI, Docker, base de datos, i18n, CI/CD, y producción. Incluye técnicas de debugging, herramientas de diagnóstico, comandos útiles, y estrategias de resolución de problemas.

## Ubicación
- **Django Errors**: `/proyecto_integrado/Croody/` - Aplicaciones Django
- **FastAPI Services**: `/proyecto_integrado/services/` - Microservicios
- **Docker Issues**: `/proyecto_integrado/` - Configuración Docker
- **CI/CD Workflows**: `/.github/workflows/` - GitHub Actions
- **Database**: `/proyecto_integrado/Croody/db.sqlite3` - SQLite local
- **Logs**: `/var/log/` - Logs del sistema

## Categorías de Problemas

### 1. Problemas de Django

#### 1.1 Errores de Base de Datos

##### Problema: "no such table"
```bash
# Error
django.db.utils.OperationalError: no such table: landing_userprofile

# Solución 1: Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Solución 2: Verificar settings
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Solución 3: Resetear BD (solo desarrollo)
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

##### Problema: "database is locked"
```bash
# Error
sqlite3.OperationalError: database is locked

# Causas y Soluciones:
# 1. Otro proceso usando la BD
ps aux | grep python
kill -9 <PID>

# 2. Demasiadas conexiones
# En Django shell:
from django.db import connection
connection.close()

# 3. Configurar timeout en SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
        }
    }
}
```

##### Problema: Migration conflicts
```bash
# Error
InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency landing.0001_initial on database 'default'.

# Solución:
# 1. Identificar conflictos
python manage.py showmigrations

# 2. Reset migraciones (solo dev)
python manage.py migrate landing zero
python manage.py migrate shop zero
python manage.py migrate

# 3. Si es crítico, forzar migraciones
# ⚠️ PELIGROSO - Solo en desarrollo
python manage.py migrate --fake-initial

# 4. Limpiar migraciones duplicadas
rm landing/migrations/0002_auto_*.py
python manage.py makemigrations landing
python manage.py migrate
```

#### 1.2 Errores de Modelos

##### Problema: "Related Object Can't Be Found"
```python
# Error
UserProfile.DoesNotExist: UserProfile matching query does not exist.

# Causa: Signal no ejecutó o User creado sin perfil

# Solución 1: Crear perfil manualmente
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='test')
from landing.models import UserProfile
UserProfile.objects.create(user=user)

# Solución 2: Re-trigger signal
from django.db.models.signals import post_save
from landing.models import UserProfile
from landing.signals import create_user_profile

user = User.objects.create(username='test', email='test@example.com')
create_user_profile(None, user, True, None)

# Solución 3: Override save() para asegurar perfil
# En User model personalizado (si existe)
def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if not hasattr(self, 'profile'):
        UserProfile.objects.create(user=self)
```

##### Problema: "null value in column violates not-null constraint"
```python
# Error
django.db.utils.IntegrityError: null value in column "user_id" violates not-null constraint

# Solución 1: Proporcionar valor por defecto
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        default=None,  # Añadir default si es necesario
    )
    # ... otros campos

# Solución 2: Marcar como nullable temporalmente
# En migración:
operations = [
    migrations.AlterField(
        model_name='userprofile',
        name='user',
        field=models.OneToOneField(
            blank=True,
            null=True,
            on_delete=models.CASCADE,
            related_name='profile',
        ),
    ),
]

# Solución 3: Data migration
def create_missing_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('landing', 'UserProfile')
    for user in User.objects.all():
        if not hasattr(user, 'profile'):
            UserProfile.objects.create(user=user)

# En migración:
migrations.RunPython(create_missing_profiles),
```

#### 1.3 Errores de Vistas (Views)

##### Problema: "TemplateDoesNotExist"
```python
# Error
django.template.TemplateDoesNotExist: landing/home.html

# Solución 1: Verificar estructura de directorios
proyecto_integrado/
└── Croody/
    └── landing/
        └── templates/
            └── landing/
                └── home.html  # Debe estar en esta estructura

# Solución 2: Configurar TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Añadir directorio global
        ],
        'APP_DIRS': True,  # Busca en apps/templates/
        # ...
    },
]

# Solución 3: Usar template_name correcto
class HomeView(TemplateView):
    template_name = 'landing/home.html'  # Correcto
    # NO: template_name = 'home.html' (a menos que esté en DIRS)
```

##### Problema: "AttributeError: GenericAPIView requires either a 'queryset'"
```python
# Error
AttributeError: GenericAPIView requires either a 'queryset' attribute or 'get_queryset()' method

# Solución 1: Definir queryset en la vista
from rest_framework import viewsets
from shop.models import Product

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()  # Añadir queryset
    serializer_class = ProductSerializer

# Solución 2: Usar get_queryset()
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()
```

##### Problema: "Reverse for 'detail' not found"
```python
# Error
NoReverseMatch: Reverse for 'detail' not found. 'detail' is not a valid view function or pattern name.

# Solución 1: Verificar name en urlpatterns
# shop/urls.py
app_name = 'shop'
urlpatterns = [
    path('products/', ProductListView.as_view(), name='catalogue'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='detail'),  # name='detail'
]

# Solución 2: Usar namespace en reverse
from django.urls import reverse

# Incorrecto:
reverse('detail', kwargs={'slug': 'product-1'})

# Correcto:
reverse('shop:detail', kwargs={'slug': 'product-1'})

# Solución 3: Verificar include() con namespace
# urls.py
path('tienda/', include('shop.urls', namespace='shop'))
```

#### 1.4 Errores de Formularios

##### Problema: "MANY-TO-MANY relationship"
```python
# Error
ValueError: Cannot assign "<QuerySet []>": "the value for a ManyToManyField must be a QuerySet"

# Causa: Asignar lista a ManyToMany

# Solución: Usar set() en lugar de asignar directamente
class Product(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)

# En vista:
product = Product.objects.get(id=1)
tags_to_add = Tag.objects.filter(name__in=['tag1', 'tag2'])
product.tags.set(tags_to_add)  # Usar set() en lugar de =
```

##### Problema: "CSRF verification failed"
```python
# Error
django.middleware.csrf.CsrfViewMiddleware: CSRF verification failed

# Solución 1: Incluir {% csrf_token %} en formularios
<form method="post">
    {% csrf_token %}  <!-- Esto es OBLIGATORIO -->
    {{ form.as_p }}
</form>

# Solución 2: Para APIs con AJAX
// Incluir token en headers
const csrftoken = getCookie('csrftoken');
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
});

# Solución 3: Exempt de CSRF (solo APIs públicas)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_endpoint(request):
    return JsonResponse({'status': 'ok'})
```

#### 1.5 Errores de Señales (Signals)

##### Problema: "maximum recursion depth exceeded"
```python
# Error
RuntimeError: maximum recursion depth exceeded

# Causa: Signal creando ciclo infinito
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        # Si la señal actualiza User, puede causar recursión

# Solución: Usar update_fields
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Evitar recursión con update_fields
    if hasattr(instance, 'profile'):
        instance.profile.save(update_fields=['display_name'])
```

#### 1.6 Errores de Configuración

##### Problema: "SECRET_KEY must not be empty"
```python
# Error
django.core.exceptions.ImproperlyConfigured: SECRET_KEY must not be empty

# Solución 1: En settings.py
import os
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-key-for-dev')

# Solución 2: En .env
SECRET_KEY=mi-clave-secreta-muy-larga

# Solución 3: Generar nueva clave
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

##### Problema: "Settings cannot be imported"
```python
# Error
ImportError: Settings cannot be imported, as environment variable DJANGO_SETTINGS_MODULE is undefined.

# Solución:
export DJANGO_SETTINGS_MODULE=proyecto_integrado.croody.settings
# O añadir a .bashrc

# O usar --settings
python manage.py runserver --settings=proyecto_integrado.croody.settings

# O en Dockerfile
ENV DJANGO_SETTINGS_MODULE=proyecto_integrado.croody.settings
```

### 2. Problemas de FastAPI

#### 2.1 Errores de Conexión

##### Problema: "connection refused"
```python
# Error
requests.exceptions.ConnectionError: Connection refused

# Solución 1: Verificar que el servicio esté corriendo
curl http://localhost:9000/healthz

# Solución 2: Verificar Dockerfile y EXPOSE
# Dockerfile
EXPOSE 9000  # Indicar puerto

# Solución 3: Verificar docker-compose
services:
  telemetry-gateway:
    ports:
      - "9000:9000"  # Exponer puerto
```

#### 2.2 Errores de Base de Datos (FastAPI)

##### Problema: "relation does not exist"
```python
# Error
psycopg2.errors.UndefinedTable: relation "telemetry" does not exist

# Solución 1: Ejecutar init_db()
# main.py
@app.on_event("startup")
def startup():
    init_db()  # Debe ejecutarse al inicio

# Solución 2: Crear tablas manualmente
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ...
            )
        ''')

# Solución 3: Verificar migración de PostgreSQL
# Ejecutar DDL manualmente
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f init.sql
```

#### 2.3 Errores de Pydantic

##### Problema: "Validation Error"
```python
# Error
pydantic.error_wrappers.ValidationError: 1 validation error

# Solución 1: Rebuild modelos
# main.py
TelemetryIn.model_rebuild()
TelemetryOut.model_rebuild()

# Solución 2: Validar datos antes de enviar
# Cliente
data = {
    "robot_id": "robot-1",
    "data": {"TEMP": 25.5},
    "position": {"lat": 19.43, "lng": -99.13}
}

# Enviar con validación
try:
    response = client.post("/api/telemetry/ingest", json=data)
except ValidationError as e:
    print(e.json())
```

#### 2.4 Errores de CORS

##### Problema: "CORS error"
```javascript
// Error en consola del browser
Access to fetch at 'http://localhost:9000/api/telemetry/ingest'
from origin 'http://localhost:8000' has been blocked by CORS policy

// Solución 1: Configurar CORS en FastAPI
from fastapi.middleware.cors import CORSMiddleware

ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "https://croody.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Solución 2: Permitir todos los orígenes (desarrollo)
ALLOWED_ORIGINS = ["*"]  # ⚠️ Solo para desarrollo
```

### 3. Problemas de Docker

#### 3.1 Container no inicia

##### Problema: "container exits immediately"
```bash
# Ver logs del container
docker logs croody_new

# Causas comunes:
# 1. Error en comando de inicio
# Dockerfile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# ⚠️ CMD vs ENTRYPOINT confict

# 2. Puerto ocupado
netstat -tulpn | grep 8000
# Cambiar puerto en docker-compose.yml
services:
  croody:
    ports:
      - "8001:8000"  # Cambiar host port

# 3. Variables de entorno faltantes
# Verificar en docker-compose.yml
environment:
  - DJANGO_SETTINGS_MODULE=proyecto_integrado.croody.settings
  - DATABASE_URL=sqlite:////data/croody.db
```

##### Problema: "port already in use"
```bash
# Error
Error starting userland proxy: listen tcp4 0.0.0.0:8000: bind: address already in use

# Solución 1: Usar puerto diferente
docker-compose.yml
ports:
  - "8001:8000"  # Usar 8001 en host

# Solución 2: Matar proceso
lsof -ti:8000 | xargs kill -9

# Solución 3: Usar opción -p específica
docker run -p 8001:8000 croody:latest
```

#### 3.2 Build errors

##### Problema: "failed to solve: python:3.11-slim: no such image"
```bash
# Error
failed to solve: python:3.11-slim: pull access denied, repository does not exist or may require 'docker login'

# Solución 1: Login en Docker Hub
docker login

# Solución 2: Usar imagen diferente
# Dockerfile
FROM python:3.11-alpine  # En lugar de slim

# Solución 3: Build local
docker build -t croody:latest .
```

##### Problema: "module not found"
```bash
# Error
ModuleNotFoundError: No module named 'django'

# Solución 1: Verificar COPY en Dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .  # ⚠️ COPIAR DESPUÉS de instalar requirements

# Solución 2: Usar contexto correcto
# Terminal
docker build -t croody:latest /path/to/proyecto_integrado/Croody

# Solución 3: Instalar dependencias en container
docker exec -it croody_new pip install -r requirements.txt
```

#### 3.3 Volumen no se monta

##### Problema: "database not persisted"
```bash
# Solución 1: Configurar volumes en docker-compose.yml
volumes:
  - croody_data:/data  # Named volume
  - ./local_dir:/app/data  # Bind mount

# Solución 2: Verificar permisos
# Linux/macOS
chmod 755 ./local_dir
chown $USER:$USER ./local_dir

# Solución 3: Usar bind mount absoluto
volumes:
  - /tmp/croody_data:/data  # Ruta absoluta
```

#### 3.4 Healthcheck falla

##### Problema: "health check failed"
```bash
# Verificar estado
docker-compose ps

# Debug health check
docker exec croody_new wget -qO- http://localhost:8000/

# Ajustar configuración en docker-compose.yml
healthcheck:
  test: ["CMD", "python", "manage.py", "check", "--deploy"]
  interval: 30s  # Aumentar intervalo
  timeout: 10s
  retries: 5
  start_period: 60s  # Dar tiempo al servicio
```

### 4. Problemas de CI/CD (GitHub Actions)

#### 4.1 Workflow no ejecuta

##### Problema: "workflow not running"
```yaml
# .github/workflows/test.yml
# ❌ Error: 'on' mal configurado
on:
  push:
    branches: [ main ]

# Solución:
on:
  push:
    branches: [ main, develop ]  # Añadir rama
  pull_request:
    branches: [ main ]

# Verificar permisos en GitHub:
# Settings > Actions > General > Workflow permissions
# ✅ Read and write permissions
```

##### Problema: "permission denied"
```bash
# Error
Error: Permission denied

# Solución 1: Configurar permisos de job
jobs:
  test:
    permissions:
      contents: read  # Necesario para checkout
      actions: read
      checks: write

# Solución 2: Usar PAT en lugar de GITHUB_TOKEN
# Settings > Developer settings > Personal access tokens

# Solución 3: Verificar secrets
# En workflow:
- name: Deploy
  env:
    SECRET_KEY: ${{ secrets.SECRET_KEY }}
  run: |
    echo $SECRET_KEY
```

#### 4.2 Tests fallan en CI

##### Problema: "database connection failed"
```yaml
# Error
django.db.utils.OperationalError: could not connect to server

# Solución 1: Configurar servicio PostgreSQL
jobs:
  test:
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.11'

      - name: Run migrations
        run: |
          cd Croody
          python manage.py migrate

# Solución 2: Usar SQLite para tests
# settings/test.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```

##### Problema: "ModuleNotFoundError"
```yaml
# Error
ModuleNotFoundError: No module named 'psycopg2'

# Solución: Instalar dependencias antes de tests
steps:
  - name: Install dependencies
    run: |
      pip install -r requirements.txt
      pip install -r requirements-test.txt

  - name: Run tests
    run: pytest
```

#### 4.3 Build de imagen falla

##### Problema: "no such file or directory"
```dockerfile
# Dockerfile
COPY . .  # Error si build context está mal

# Solución:
# 1. Usar .dockerignore
echo "node_modules" > .dockerignore
echo "__pycache__" >> .dockerignore
echo ".git" >> .dockerignore

# 2. Build con contexto correcto
docker build -t croody:latest proyecto_integrado/

# 3. Multi-stage build
FROM python:3.11-slim as builder
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
```

### 5. Problemas de Base de Datos

#### 5.1 Migraciones atascadas

##### Problema: "InconsistentMigrationHistory"
```python
# Error
InconsistentMigrationHistory: Migration admin.0001_initial is applied before...

# Solución 1: Limpiar historial de migraciones
python manage.py dbshell
# SQLite
.delete from django_migrations;

# PostgreSQL
TRUNCATE TABLE django_migrations RESTART IDENTITY CASCADE;

# Solución 2: Marcar migraciones como fake
python manage.py migrate --fake

# Solución 3: Reset completo (DEVELOPMENT ONLY)
rm -rf Croody/*/migrations/*.py
touch Croody/*/migrations/__init__.py
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

#### 5.2 Datos corruptos

##### Problema: "database disk image is malformed"
```bash
# Error
sqlite3.DatabaseError: database disk image is malformed

# Solución 1: Reparar SQLite
sqlite3 db.sqlite3 ".recover" | sqlite3 db_new.sqlite3
mv db_new.sqlite3 db.sqlite3

# Solución 2: Backup y restaurar
# Crear dump
python manage.py dumpdata > backup.json

# Restaurar
rm db.sqlite3
python manage.py migrate
python manage.py loaddata backup.json

# Solución 3: Integrity check
sqlite3 db.sqlite3 "PRAGMA integrity_check;"
```

#### 5.3 Performance: consultas lentas

##### Problema: "N+1 Query Problem"
```python
# Error: Múltiples queries cuando se podría usar una sola

# ❌ Problema
for product in products:
    print(product.category.name)  # N queries adicionales

# Solución 1: select_related()
products = Product.objects.select_related('category').all()
for product in products:
    print(product.category.name)  # 1 query sola

# Solución 2: prefetch_related()
products = Product.objects.prefetch_related('tags').all()
for product in products:
    for tag in product.tags.all():  # 1 query para todos los tags
        print(tag.name)

# Solución 3: Usar values()
categories = Category.objects.values('id', 'name')
# Una sola query, datos en diccionario
```

### 6. Problemas de Internacionalización (i18n)

#### 6.1 Traducciones no aparecen

##### Problema: "Strings not translated"
```html
<!-- Error: Texto aparece en español en todas las páginas -->

<!-- Solución 1: Cargar i18n -->
{% load i18n %}  <!-- DEBE estar en la primera línea -->

<!-- Solución 2: Usar trans correctamente -->
<h1>{% trans "Hello World" %}</h1>
<!-- NO: <h1>Hello World</h1> -->

<!-- Solución 3: Compilar mensajes -->
python manage.py compilemessages

<!-- Verificar archivos .mo -->
ls locale/*/LC_MESSAGES/
# Debe haber django.mo (compilado)
```

##### Problema: "Language code not in URLs"
```python
# Error: /es/product/ vs /product/

# Solución: Verificar i18n_patterns en urls.py
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # URLs sin prefijo
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', include('landing.urls', namespace='landing')),
    prefix_default_language=False,  # ⚠️ Clave para / sin prefijo
)

# Verificar LANGUAGE_CODE
LANGUAGE_CODE = 'es'  # Idioma por defecto
```

#### 6.2 Pluralización incorrecta

##### Problema: "1 productos" (singular mal)
```html
<!-- Solución: Usar blocktrans con count -->
{% blocktrans count counter=items|length %}
    Tienes {{ counter }} producto.
{% plural %}
    Tienes {{ counter }} productos.
{% endblocktrans %}

<!-- NO usar: -->
{{ count }} producto{{ count|pluralize }}  <!-- Puede fallar en algunos idiomas -->
```

### 7. Problemas de Seguridad

#### 7.1 SSL/TLS errors

##### Problema: "certificate verify failed"
```python
# Error
requests.exceptions.SSLError: certificate verify failed

# Solución 1: Verificar certificado
openssl s_client -connect croody.app:443 -servername croody.app

# Solución 2: Usar requests con verificación deshabilitada (solo dev)
import requests
from urllib3 import disable_warnings
disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get('https://croody.app', verify=False)  # ⚠️ Solo desarrollo

# Solución 3: Configurar CA bundle
export REQUESTS_CA_BUNDLE=/path/to/ca-bundle.crt

# Django settings
SECURE_SSL_REDIRECT = True  # Producción
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

##### Problema: "Mixed content warnings"
```html
<!-- Error: HTTP resource en HTTPS page -->

<!-- Solución: Usar HTTPS siempre -->
<script src="https://cdn.example.com/script.js">  <!-- ✅ HTTPS -->
<!-- NO: <script src="http://cdn.example.com/script.js"> -->

<!-- En Django settings -->
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
```

#### 7.2 CSRF errors

##### Problema: "CSRF token missing or incorrect"
```python
# Error: 403 Forbidden

# Solución 1: Incluir token en formularios
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
</form>

# Solución 2: Para APIs
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def api_view(request):
    return JsonResponse({'status': 'ok'})

# Solución 3: AJAX con token
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
});
```

### 8. Problemas de Performance

#### 8.1 Sitio lento

##### Problema: "High response time"
```python
# Diagnóstico:
# 1. Verificar consultas lentas
# En settings.py (development)
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

# 2. Usar django-debug-toolbar
pip install django-debug-toolbar

INSTALLED_APPS = ['debug_toolbar', ...]
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware', ...]
INTERNAL_IPS = ['127.0.0.1']

# 3. Identificar queries lentas
from django.db import connection
def get_queries():
    for query in connection.queries:
        print(f"{query['sql']} - {query['time']}ms")

# Solución: Optimizar
# - Añadir índices
# - Usar select_related/prefetch_related
# - Cachear resultados
# - Paginar listas largas
```

#### 8.2 Alto uso de memoria

##### Problema: "MemoryError" o servidor lento
```python
# Diagnóstico:
import tracemalloc
tracemalloc.start()

# Tu código aquí

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 1024 / 1024:.1f} MB")
print(f"Peak memory usage was {peak / 1024 / 1024:.1f} MB")

# Soluciones:
# 1. Generadores en lugar de listas
# ❌ Mal
data = [obj for obj in large_queryset]  # Carga todo en memoria

# ✅ Bien
data = (obj for obj in large_queryset)  # Generator, lazy loading

# 2. Usar iterator()
products = Product.objects.iterator()  # Django 1.11+

# 3. Bulk operations
Product.objects.bulk_create(objs)  # Mejor que create() en loop

# 4. Limitar resultados
products = Product.objects.all()[:100]  # LIMIT en SQL
```

### 9. Problemas de Configuración

#### 9.1 Variables de entorno

##### Problema: "Environment variable not set"
```python
# Error
KeyError: 'DATABASE_URL'

# Solución 1: Configurar .env
# .env
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=mi-clave-super-secreta

# Solución 2: Usar python-decouple
pip install python-decouple

# settings.py
from decouple import config
DATABASE_URL = config('DATABASE_URL', default='sqlite:///db.sqlite3')
SECRET_KEY = config('SECRET_KEY', default='dev-key')

# Solución 3: Valores por defecto
import os
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-for-dev')
```

#### 9.2 Static files

##### Problema: "Static files not served"
```python
# Error: 404 en /static/admin/css/base.css

# Solución 1: collectstatic
python manage.py collectstatic --noinput

# Solución 2: DEBUG=True (solo desarrollo)
DEBUG = True

# Solución 3: Verificar STATIC_URL y STATIC_ROOT
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Para producción

# Solución 4: Verificar Whitenoise (si se usa)
INSTALLED_APPS = ['whitenoise.runserver_nostatic', ...]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Después de Security
    ...
]

# En producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 10. Debugging Avanzado

#### 10.1 Python Debugger

##### Usar pdb/ipdb
```python
# En código
import pdb; pdb.set_trace()  # Breakpoint
# O mejor:
from ipdb import set_trace; set_trace()  # ipdb es mejor

# Comandos en pdb:
# n (next) - siguiente línea
# s (step) - entrar en función
# c (continue) - continuar hasta breakpoint
# l (list) - ver código actual
# p variable - imprimir variable
# pp variable - pretty print
# q (quit) - salir

# Con pytest
pytest --pdb  # Entra en pdb en fallos
pytest --pdbcls=IPython.terminal.debugger:Pdb  # Usar ipdb
```

##### Debugging en Django Shell
```bash
# Abrir shell con datos
python manage.py shell

# Desde shell_plus (si django-extensions)
pip install django-extensions
INSTALLED_APPS = ['django_extensions', ...]

python manage.py shell_plus

# Ejecutar queries
from shop.models import Product
products = Product.objects.all()
print(products.query)  # Ver SQL generado

# Verificar relaciones
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.first()
print(user.profile)  # Verificar OneToOne
```

#### 10.2 Logging avanzado

##### Configurar logging detallado
```python
# settings/debug.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'shop': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

#### 10.3 Django Debug Toolbar

##### Instalar y configurar
```bash
pip install django-debug-toolbar

# settings.py
INSTALLED_APPS = ['debug_toolbar', ...]
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware', ...]
INTERNAL_IPS = ['127.0.0.1', '192.168.1.100']

# urls.py
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
```

### 11. Herramientas de Diagnóstico

#### 11.1 Comandos Django útiles

```bash
# Verificar configuración
python manage.py check
python manage.py check --deploy  # Verificaciones de producción

# Ver migraciones
python manage.py showmigrations
python manage.py makemigrations  # Crear migraciones

# SQL de migraciones
python manage.py sqlmigrate shop 0001

# Django shell
python manage.py shell
python manage.py shell_plus  # Con django-extensions

# Limpiar cache
python manage.py clear_cache

# Crear superuser
python manage.py createsuperuser

# Dump de datos
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json

# Runserver con reload
python manage.py runserver

# Ejecutar tests
python manage.py test
python manage.py test shop.tests.test_models  # Tests específicos

# Collect static
python manage.py collectstatic --noinput

# Compile messages
python manage.py compilemessages

# Diff settings
python manage.py diffsettings
```

#### 11.2 Comandos Docker útiles

```bash
# Ver logs
docker logs -f croody_new  # Follow logs
docker logs --tail 100 croody_new  # Last 100 lines

# Ejecutar comandos en container
docker exec -it croody_new bash
docker exec -it croody_new python manage.py shell

# Ver estado
docker-compose ps
docker-compose ps -a  # Incluir stopped

# Reconstruir
docker-compose up --build
docker-compose build croody

# Limpiar
docker-compose down -v  # Con volumes
docker system prune -a  # Limpiar todo

# Ver recursos
docker stats

# Ver procesos dentro del container
docker exec croody_new ps aux
```

#### 11.3 Comandos de red

```bash
# Ver puertos en uso
netstat -tulpn | grep 8000
lsof -i :8000

# Test de conectividad
curl -v http://localhost:8000/health/
curl -I http://localhost:8000/  # Solo headers

# Test de API
curl -X POST http://localhost:9000/api/telemetry/ingest \
  -H "Content-Type: application/json" \
  -d '{"robot_id": "test", "data": {"TEMP": 25}}'

# Verificar certificado SSL
openssl s_client -connect croody.app:443 -servername croody.app
```

### 12. Checklist de Troubleshooting

#### ¿Qué revisar primero?

```markdown
### Paso 1: Verificar logs
- [ ] Django: `/var/log/croody/application.log`
- [ ] Nginx: `/var/log/nginx/error.log`
- [ ] Docker: `docker logs container_name`
- [ ] CI/CD: GitHub Actions logs

### Paso 2: Verificar configuración
- [ ] settings.py: DEBUG, ALLOWED_HOSTS, DATABASES
- [ ] .env: Variables de entorno configuradas
- [ ] urls.py: URLs correctas
- [ ] requirements.txt: Dependencias instaladas

### Paso 3: Verificar base de datos
- [ ] Migraciones ejecutadas: `python manage.py showmigrations`
- [ ] Conexión: `python manage.py dbshell`
- [ ] Datos: ¿Existen los registros?

### Paso 4: Verificar servicios
- [ ] Docker: `docker-compose ps`
- [ ] FastAPI: `curl http://localhost:9000/healthz`
- [ ] Base de datos: conexión activa

### Paso 5: Verificar red
- [ ] Puertos: `netstat -tulpn`
- [ ] Firewall: ufw status
- [ ] Conectividad: curl/wget

### Paso 6: Debugging
- [ ] Django shell: `python manage.py shell`
- [ ] Debug toolbar: visible en desarrollo
- [ ] pdb/ipdb: breakpoints en código
```

## Soluciones Rápidas

### "No module named 'django'"
```bash
pip install -r requirements.txt
# o
pip install django
```

### "TemplateDoesNotExist"
```bash
python manage.py collectstatic --noinput
# Verificar TEMPLATES en settings.py
```

### "Database is locked"
```bash
python manage.py migrate --run-syncdb
# o restart services
```

### "Port already in use"
```bash
lsof -ti:8000 | xargs kill -9
# o usar puerto diferente
```

### "Permission denied"
```bash
chmod +x manage.py
chown -R $USER:$USER ./
# verificar Docker user
```

### "CSRF verification failed"
```html
<!-- En template -->
{% csrf_token %}
```

### "SSL error"
```python
# Solo desarrollo
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## Contacto y Escalación

### Información para soporte
```markdown
Al reportar un problema, incluir:
- [ ] Error completo (traceback)
- [ ] Pasos para reproducir
- [ ] Configuración (settings, requirements)
- [ ] Versiones (Python, Django, FastAPI, Docker)
- [ ] Logs relevantes
- [ ] Screenshots (si aplica)
```

### Canales de soporte
```markdown
1. **Documentación**: docs/ (este documento)
2. **Logs**: /var/log/croody/
3. **Debug mode**: DEBUG=True (solo desarrollo)
4. **Herramientas**: Django shell, Debug Toolbar
5. **Comunidad**: Stack Overflow, Django Forum
```

## Referencias

### Documentación Externa
- [Django Troubleshooting](https://docs.djangoproject.com/en/stable/topics/db/)
- [FastAPI Errors](https://fastapi.tiangolo.com/tutorial/debugging/)
- [Docker Troubleshooting](https://docs.docker.com/engine/troubleshooting/)
- [GitHub Actions Troubleshooting](https://docs.github.com/en/actions)

### Herramientas
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [Django Extensions](https://github.com/django-extensions/django-extensions)
- [IPython Debugger](https://pypi.org/project/ipdb/)
- [Django Silk](https://github.com/jazzband/django-silk) - Profiler

## Ver También
- [Monitoreo y Logs](../10-MONITOREO/logs-sistema.md)
- [Testing - Validación](../09-TESTING/testing-general.md)
- [Seguridad - Hardening](../06-SEGURIDAD/hardening.md)
