# REST API Endpoints - Documentación Completa

## Resumen
La API de Croody implementa endpoints REST para funcionalidades específicas del proyecto, incluyendo manejo del carrito, telemetría de robots y análisis de tráfico de red. Utiliza tanto vistas tradicionales Django como Django REST Framework (DRF) para diferentes casos de uso.

## Ubicación
- **Endpoints Shop**: `/proyecto_integrado/Croody/shop/urls.py`
- **Endpoints Telemetry**: `/proyecto_integrado/Croody/telemetry/urls.py`
- **Vistas Shop**: `/proyecto_integrado/Croody/shop/views.py` (líneas 214-258)
- **Vistas Telemetry**: `/proyecto_integrado/Croody/telemetry/views.py`
- **Model**: `/proyecto_integrado/Croody/telemetry/models.py`

## Arquitectura de la API

### Patrones de Diseño

#### 1. Vistas Tradicionales Django (Simples)
```python
# shop/views.py
@csrf_exempt
@require_http_methods(['POST'])
def cart_add_api(request):
    # Implementación directa con JsonResponse
```

**Ventajas**:
- Simplicidad para endpoints básicos
- Control total sobre la respuesta
- Sin dependencias adicionales de DRF
- Fácil implementación de excepciones custom

**Casos de uso**: Endpoints simples, flujos específicos sin necesidad de serialización

#### 2. Django REST Framework (ViewSets)
```python
# telemetry/views.py
class RobotPositionViewSet(viewsets.ModelViewSet):
    queryset = RobotPosition.objects.all().order_by('-timestamp')
    serializer_class = RobotPositionSerializer
```

**Ventajas**:
- CRUD automático
- Serialización/deserialización
- Manejo de ViewSets y Routers
- Documentación automática con Swagger
- Filtros y paginación integrados

**Casos de uso**: Entidades completas, operaciones CRUD, recursos relacionados

### Configuración de URLs

#### Shop URLs (`shop/urls.py`)
```python
urlpatterns = [
    path('', ProductListView.as_view(), name='catalogue'),
    path('api/cart/add/', cart_add_api, name='cart-add-api'),
    path('checkout-preview/', CheckoutPreviewView.as_view(), name='checkout-preview'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
]
```

#### Telemetry URLs (`telemetry/urls.py`)
```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'robot-position', views.RobotPositionViewSet)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/', include(router.urls)),
    path('api/traffic/', views.traffic_data, name='traffic_data'),
]
```

**Estructura generada automáticamente por DRF Router**:
```
GET    /telemetry/api/robot-position/           → list
POST   /telemetry/api/robot-position/           → create
GET    /telemetry/api/robot-position/{id}/      → retrieve
PUT    /telemetry/api/robot-position/{id}/      → update
PATCH  /telemetry/api/robot-position/{id}/      → partial_update
DELETE /telemetry/api/robot-position/{id}/      → destroy
GET    /telemetry/api/robot-position/latest/    → custom action
```

## Endpoints Detallados

### 1. Cart Add API

#### Información General
- **URL**: `/shop/api/cart/add/`
- **Método**: `POST`
- **Content-Type**: `application/json`
- **Autenticación**: No requerida
- **Rate Limiting**: No configurado

#### Parámetros del Request
```json
{
    "product_id": 123
}
```

#### Parámetros Requeridos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `product_id` | integer | ID del producto a agregar |

#### Respuestas Exitosas

**201 - Producto Agregado**
```json
{
    "success": true,
    "message": "Cofre Premium agregado al carrito",
    "product": {
        "id": 123,
        "name": "Cofre Premium",
        "price": 29.99,
        "slug": "cofre-premium"
    }
}
```

#### Respuestas de Error

**400 - Datos Inválidos**
```json
{
    "success": false,
    "error": "product_id es requerido"
}
```

**400 - JSON Inválido**
```json
{
    "success": false,
    "error": "JSON inválido"
}
```

**404 - Producto No Encontrado**
```json
{
    "success": false,
    "error": "Producto no encontrado"
}
```

**500 - Error del Servidor**
```json
{
    "success": false,
    "error": "Error del servidor: <mensaje de error>"
}
```

#### Validaciones Implementadas
```python
def cart_add_api(request):
    # 1. Validar JSON
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    # 2. Validar product_id presente
    product_id = data.get('product_id')
    if not product_id:
        return JsonResponse({'success': False, 'error': 'product_id es requerido'}, status=400)

    # 3. Validar producto existe y está publicado
    product = Product.objects.filter(id=product_id, is_published=True).first()
    if not product:
        return JsonResponse({'success': False, 'error': 'Producto no encontrado'}, status=404)

    # 4. Respuesta exitosa
    return JsonResponse({
        'success': True,
        'message': f'{product.name} agregado al carrito',
        'product': {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'slug': product.slug
        }
    })
```

#### Consideraciones de Seguridad
- `@csrf_exempt`: Exento de token CSRF (consideración: evaluar riesgo)
- Validación estricta de entrada
- Sanitización de datos de salida
- Filtro por `is_published=True` para seguridad

### 2. RobotPosition ViewSet

#### Información General
- **Base URL**: `/telemetry/api/robot-position/`
- **Modelo**: `RobotPosition`
- **Serializer**: `RobotPositionSerializer`
- **Orden**: Por timestamp descendente

#### Serializer
```python
class RobotPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobotPosition
        fields = ['x', 'y', 'atmosphere', 'timestamp']
```

#### Operaciones CRUD

##### GET - Listar Posiciones
**Request**:
```http
GET /telemetry/api/robot-position/
Authorization: Bearer <token>  # Si se requiere auth
```

**Response**:
```json
[
    {
        "x": 40.7128,
        "y": -74.0060,
        "atmosphere": {
            "temperature": 23.5,
            "humidity": 45,
            "pressure": 1013.25
        },
        "timestamp": "2025-12-02T10:30:00Z"
    },
    {
        "x": 40.7589,
        "y": -73.9851,
        "atmosphere": {
            "temperature": 22.1,
            "humidity": 48,
            "pressure": 1012.80
        },
        "timestamp": "2025-12-02T10:25:00Z"
    }
]
```

**Query Parameters**:
- `limit`: Número de resultados (paginación)
- `offset`: Offset para paginación

##### POST - Crear Posición
**Request**:
```http
POST /telemetry/api/robot-position/
Content-Type: application/json

{
    "x": 40.7128,
    "y": -74.0060,
    "atmosphere": {
        "temperature": 23.5,
        "humidity": 45,
        "pressure": 1013.25
    },
    "timestamp": "2025-12-02T10:30:00Z"
}
```

**Response**:
```json
{
    "x": 40.7128,
    "y": -74.0060,
    "atmosphere": {
        "temperature": 23.5,
        "humidity": 45,
        "pressure": 1013.25
    },
    "timestamp": "2025-12-02T10:30:00Z"
}
```

**Status Code**: 201 Created

##### GET - Obtener Posición Específica
**Request**:
```http
GET /telemetry/api/robot-position/{id}/
```

**Response**:
```json
{
    "x": 40.7128,
    "y": -74.0060,
    "atmosphere": {
        "temperature": 23.5,
        "humidity": 45,
        "pressure": 1013.25
    },
    "timestamp": "2025-12-02T10:30:00Z"
}
```

##### PUT - Actualizar Posición Completa
**Request**:
```http
PUT /telemetry/api/robot-position/{id}/
Content-Type: application/json

{
    "x": 40.7589,
    "y": -73.9851,
    "atmosphere": {
        "temperature": 22.1,
        "humidity": 48,
        "pressure": 1012.80
    },
    "timestamp": "2025-12-02T10:35:00Z"
}
```

**Response**: 200 OK con datos actualizados

##### PATCH - Actualización Parcial
**Request**:
```http
PATCH /telemetry/api/robot-position/{id}/
Content-Type: application/json

{
    "atmosphere": {
        "temperature": 24.0
    }
}
```

##### DELETE - Eliminar Posición
**Request**:
```http
DELETE /telemetry/api/robot-position/{id}/
```

**Response**: 204 No Content

#### Acciones Personalizadas

##### GET /latest - Última Posición
**Request**:
```http
GET /telemetry/api/robot-position/latest/
```

**Response**:
```json
{
    "x": 40.7128,
    "y": -74.0060,
    "atmosphere": {
        "temperature": 23.5,
        "humidity": 45,
        "pressure": 1013.25
    },
    "timestamp": "2025-12-02T10:30:00Z"
}
```

**Implementación**:
```python
@action(detail=False, methods=['get'])
def latest(self, request):
    latest = RobotPosition.objects.first()
    if latest:
        serializer = self.get_serializer(latest)
        return Response(serializer.data)
    return Response({})
```

**Casos de uso**:
- Dashboard en tiempo real
- Verificación de estado actual
- Monitoreo de actividad reciente

### 3. Traffic Data API

#### Información General
- **URL**: `/telemetry/api/traffic/`
- **Método**: `GET`
- **Tipo**: Datos de flujo de red
- **Fuente**: CICFlowMeter (análisis de PCAP)

#### Función del Endpoint
```python
def traffic_data(request):
    data = get_mock_traffic_data()
    return JsonResponse({'flows': data})
```

#### Response Structure
```json
{
    "flows": [
        {
            "src_ip": "192.168.1.5",
            "dst_ip": "8.8.8.8",
            "protocol": "UDP",
            "length": 120
        },
        {
            "src_ip": "192.168.1.10",
            "dst_ip": "10.0.0.1",
            "protocol": "TCP",
            "length": 500
        }
    ]
}
```

#### Datos de Flujo (Flow Fields)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `src_ip` | string | IP de origen |
| `dst_ip` | string | IP de destino |
| `protocol` | string | Protocolo (TCP/UDP/ICMP) |
| `length` | integer | Tamaño en bytes |

#### Implementación CICFlowMeter

**Wrapper Class**:
```python
class CICFlowMeterWrapper:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run_analysis(self):
        """Ejecuta CICFlowMeter en archivos PCAP"""
        if not os.path.exists(BIN_PATH):
            raise FileNotFoundError(f"CICFlowMeter JAR not found at {BIN_PATH}")

        cmd = ['java', '-jar', BIN_PATH, self.input_dir, self.output_dir]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"CICFlowMeter failed: {result.stderr}")

        return self._get_latest_results()
```

**Procesamiento CSV**:
```python
def _get_latest_results(self):
    results = []
    if not os.path.exists(self.output_dir):
        return results

    for filename in os.listdir(self.output_dir):
        if filename.endswith('.csv'):
            path = os.path.join(self.output_dir, filename)
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    results.append(row)
    return results
```

**Datos Mock**:
```python
def get_mock_traffic_data():
    """Datos de prueba para desarrollo/testing"""
    return [
        {"src_ip": "192.168.1.5", "dst_ip": "8.8.8.8", "protocol": "UDP", "length": 120},
        {"src_ip": "192.168.1.10", "dst_ip": "10.0.0.1", "protocol": "TCP", "length": 500},
    ]
```

#### Casos de Uso
- **Análisis de seguridad**: Detección de patrones anómalos
- **Monitoreo de red**: Métricas de rendimiento
- **Investigación forense**: Análisis post-incidente
- **流量整形**: QoS y optimización de ancho de banda

## Serializers

### RobotPositionSerializer
```python
class RobotPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobotPosition
        fields = ['x', 'y', 'atmosphere', 'timestamp']

    def validate_atmosphere(self, value):
        """Validación personalizada para datos atmosféricos"""
        required_fields = ['temperature', 'humidity', 'pressure']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(f"Campo {field} requerido en atmosphere")
        return value
```

**Características**:
- Serialización automática de Model a JSON
- Validación de campos
- Soporte para campos JSON (atmosphere)
- Timestamps automáticos

## Autenticación y Permisos

### Estado Actual
- **No configurado**: Los endpoints actualmente no requieren autenticación
- **Consideración**: Evaluar necesidad de autenticación según sensibilidad de datos

### Configuración Recomendada (Django REST Framework)

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

### Tokens de Autenticación
```python
# usage
from rest_framework.authtoken.views import obtain_auth_token

# Obtener token
POST /api-auth/login/
{
    "username": "usuario",
    "password": "contraseña"
}

# Respuesta
{
    "token": "abc123def456..."
}
```

### Permission Classes Personalizadas
```python
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Lectura permitida para todos
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Escritura solo para el propietario
        return obj.owner == request.user
```

## Paginación

### Page Number Pagination
```python
# Request
GET /telemetry/api/robot-position/?page=1

# Response
{
    "count": 100,
    "next": "http://localhost:8000/telemetry/api/robot-position/?page=2",
    "previous": null,
    "results": [...]
}
```

### Limit Offset Pagination
```python
# Request
GET /telemetry/api/robot-position/?limit=10&offset=20

# Response
{
    "count": 100,
    "next": "http://localhost:8000/telemetry/api/robot-position/?offset=30&limit=10",
    "previous": "http://localhost:8000/telemetry/api/robot-position/?offset=10&limit=10",
    "results": [...]
}
```

## Filtros y Búsqueda

### Filtros Personalizados
```python
from rest_framework import filters

class RobotPositionViewSet(viewsets.ModelViewSet):
    queryset = RobotPosition.objects.all().order_by('-timestamp')
    serializer_class = RobotPositionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['atmosphere']
    ordering_fields = ['timestamp', 'x', 'y']
    ordering = ['-timestamp']
```

### Búsqueda por JSON Fields
```python
# GET /telemetry/api/robot-position/?search=temperature:23
# Filtra por contenido en atmosphere

from django_filters import rest_framework as filters

class AtmosphereFilter(filters.FilterSet):
    min_temp = filters.NumberFilter(field_name='atmosphere__temperature', lookup_expr='gte')
    max_temp = filters.NumberFilter(field_name='atmosphere__temperature', lookup_expr='lte')

    class Meta:
        model = RobotPosition
        fields = ['atmosphere']
```

## Manejo de Errores

### Formato de Error Estándar
```python
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Datos inválidos",
        "details": [
            {
                "field": "product_id",
                "message": "Este campo es requerido"
            }
        ]
    }
}
```

### Custom Exception Handler
```python
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['error'] = {
            'code': response.status_code,
            'message': str(exc)
        }

    return response
```

### Status Codes Utilizados
| Código | Uso | Descripción |
|--------|-----|-------------|
| 200 | OK | Operación exitosa (GET, PUT) |
| 201 | Created | Recurso creado (POST) |
| 204 | No Content | Eliminación exitosa (DELETE) |
| 400 | Bad Request | Datos inválidos |
| 404 | Not Found | Recurso no encontrado |
| 500 | Internal Server Error | Error del servidor |

## Rate Limiting

### Configuración Recomendada
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'cart_add': '10/minute'
    }
}
```

### Aplicación a Endpoints
```python
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle

class CartAddThrottle(UserRateThrottle):
    rate = '10/minute'

@throttle_classes([CartAddThrottle])
def cart_add_api(request):
    # ...
```

## Versionado de API

### URL Path Versioning
```python
# urls.py
from rest_framework.versioning import URLPathVersioning

class Versioning:
    version_class = URLPathVersioning
    default_version = 'v1'
    allowed_versions = ['v1', 'v2']
    version_param = 'version'

# Views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning

class RobotPositionViewSet(viewsets.ModelViewSet):
    versioning_class = URLPathVersioning

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return RobotPositionSerializerV2
        return RobotPositionSerializerV1
```

### Header Versioning
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.HeaderVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'VERSION_PARAM': 'version'
}

# Request
GET /telemetry/api/robot-position/
Version: v1
```

## Documentación Automática

### OpenAPI/Swagger
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# Instalar: pip install drf-yasg
# URLs
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Croody API",
        default_version='v1',
        description="API para Croody Platform",
    ),
    public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]
```

### Documentación Generada
- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`
- **JSON Schema**: `/swagger/?format=json`

## Testing

### Unit Tests
```python
# tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from .models import RobotPosition

class RobotPositionAPITest(APITestCase):
    def setUp(self):
        self.robot = RobotPosition.objects.create(
            x=40.7128,
            y=-74.0060,
            atmosphere={'temperature': 23.5}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_latest_position(self):
        response = self.client.get('/telemetry/api/robot-position/latest/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_position(self):
        data = {
            'x': 40.7589,
            'y': -73.9851,
            'atmosphere': {'temperature': 22.1}
        }
        response = self.client.post('/telemetry/api/robot-position/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data(self):
        data = {'x': 'invalid'}
        response = self.client.post('/telemetry/api/robot-position/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

### Integration Tests
```python
# tests_integration.py
from django.test import TestCase
from django.urls import reverse

class CartAPIIntegrationTest(TestCase):
    def test_add_product_to_cart(self):
        product = Product.objects.create(name="Test", price=29.99)
        response = self.client.post(
            reverse('shop:cart-add-api'),
            {'product_id': product.id},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()['success'])
```

### Testing con Pytest
```python
# conftest.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

# test_cart.py
@pytest.mark.django_db
def test_cart_add_api(authenticated_client, product):
    response = authenticated_client.post(
        '/shop/api/cart/add/',
        {'product_id': product.id},
        format='json'
    )
    assert response.status_code == 201
    assert response.json()['success'] is True
```

## Ejemplos de Uso

### Cliente JavaScript (Fetch)
```javascript
// Agregar al carrito
async function addToCart(productId) {
    try {
        const response = await fetch('/shop/api/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ product_id: productId })
        });

        const data = await response.json();

        if (data.success) {
            showNotification(data.message, 'success');
            updateCartCount();
        } else {
            showNotification(data.error, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error de conexión', 'error');
    }
}

// Obtener última posición del robot
async function getLatestPosition() {
    try {
        const response = await fetch('/telemetry/api/robot-position/latest/');
        const data = await response.json();
        updateRobotDashboard(data);
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### Cliente Python (Requests)
```python
import requests

# Agregar producto al carrito
def add_to_cart(product_id):
    response = requests.post(
        'http://localhost:8000/shop/api/cart/add/',
        json={'product_id': product_id},
        headers={'Content-Type': 'application/json'}
    )
    return response.json()

# Obtener posiciones del robot
def get_robot_positions():
    response = requests.get('http://localhost:8000/telemetry/api/robot-position/')
    return response.json()

# Obtener última posición
def get_latest_position():
    response = requests.get('http://localhost:8000/telemetry/api/robot-position/latest/')
    return response.json()
```

### Cliente cURL
```bash
# Agregar al carrito
curl -X POST http://localhost:8000/shop/api/cart/add/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 123}'

# Listar posiciones
curl http://localhost:8000/telemetry/api/robot-position/

# Obtener última posición
curl http://localhost:8000/telemetry/api/robot-position/latest/

# Crear nueva posición
curl -X POST http://localhost:8000/telemetry/api/robot-position/ \
  -H "Content-Type: application/json" \
  -d '{
    "x": 40.7128,
    "y": -74.0060,
    "atmosphere": {
      "temperature": 23.5,
      "humidity": 45,
      "pressure": 1013.25
    }
  }'

# Obtener tráfico
curl http://localhost:8000/telemetry/api/traffic/
```

## Configuración de Entorno

### Instalar Dependencias
```bash
pip install djangorestframework
pip install django-filter
pip install drf-yasg
pip install requests  # Para cliente Python
```

### URLs Globales
```python
# urls.py (proyecto principal)
from django.urls import path, include

urlpatterns = [
    path('shop/', include('shop.urls')),
    path('telemetry/', include('telemetry.urls')),
]
```

### Middleware para Logs
```python
# middleware.py
import logging

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('api')

    def __call__(self, request):
        # Log request
        self.logger.info(f"API Request: {request.method} {request.path}")

        response = self.get_response(request)

        # Log response
        self.logger.info(f"API Response: {response.status_code}")

        return response
```

## Mejores Prácticas

### ✅ Hacer
```python
# Validar datos de entrada
data = json.loads(request.body)
if not data.get('product_id'):
    return JsonResponse({'error': 'product_id requerido'}, status=400)

# Usar filtros de seguridad
product = Product.objects.filter(id=product_id, is_published=True).first()

# Manejar excepciones específicas
try:
    # lógica
except json.JSONDecodeError:
    return JsonResponse({'error': 'JSON inválido'}, status=400)

# Usar serializers para datos complejos
serializer = RobotPositionSerializer(data=request.data)
if serializer.is_valid():
    serializer.save()

# Implementar paginación
class RobotPositionViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    page_size = 20

# Documentar endpoints
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def cart_add_api(request):
    """Agregar producto al carrito de compras"""
```

### ❌ Evitar
```python
# No usar eval() o exec()
data = eval(request.body)  # ❌ Inseguro

# No exponer datos sensibles en respuestas
return JsonResponse({
    'user_password': user.password,  # ❌
    'api_key': 'secret123'  # ❌
})

# No usar consultas N+1
for position in positions:
    robot = position.robot  # ❌ N+1 queries
# Mejor: positions = RobotPosition.objects.select_related('robot')

# No omitir validación
def create_view(request):
    data = json.loads(request.body)
    Model.objects.create(**data)  # ❌ Sin validación
    # Mejor: serializer.is_valid()

# No hardcodear URLs
url = 'http://localhost:8000/api/...'  # ❌
# Mejor: reverse('api:endpoint')
```

## Consideraciones de Rendimiento

### Optimización de Queries
```python
# Prefetch para evitar N+1
RobotPosition.objects.select_related('related_model').all()

# Indexar campos query
# models.py
class RobotPosition(models.Model):
    timestamp = models.DateTimeField(db_index=True)  # Índice
    x = models.FloatField(db_index=True)
    y = models.FloatField(db_index=True)

# Paginación para grandes datasets
class RobotPositionViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    page_size = 50  # Tamaño razonable
```

### Caching
```python
# Cache para endpoints frecuentes
from django.core.cache import cache

@action(detail=False)
def latest(self, request):
    cache_key = 'robot_latest_position'
    position = cache.get(cache_key)

    if not position:
        position = RobotPosition.objects.first()
        cache.set(cache_key, position, timeout=300)  # 5 minutos

    serializer = self.get_serializer(position)
    return Response(serializer.data)
```

### Async Views (Django 3.1+)
```python
# Para operaciones I/O intensivas
import asyncio
from django.http import JsonResponse

async def async_traffic_analysis(request):
    # Simular operación asíncrona
    await asyncio.sleep(0.1)
    data = get_heavy_analysis()
    return JsonResponse(data)
```

## Seguridad

### Validación de Entrada
```python
# Validación estricta con cerberus/pydantic
import cerberus

schema = {
    'product_id': {
        'type': 'integer',
        'min': 1,
        'max': 999999
    }
}

def cart_add_api(request):
    data = json.loads(request.body)
    v = cerberus.Validator(schema)

    if not v.validate(data):
        return JsonResponse({'errors': v.errors}, status=400)
```

### Sanitización de Salida
```python
# Evitar inyección XSS en respuestas
from django.utils.html import escape

def custom_view(request):
    data = {
        'user_input': escape(user_input)  # Sanitizar
    }
    return JsonResponse(data)
```

### Rate Limiting
```python
# Implementar rate limiting personalizado
from django.core.cache import cache

def check_rate_limit(request, limit=10):
    ip = request.META.get('REMOTE_IP')
    key = f'rate_limit_{ip}'
    count = cache.get(key, 0)

    if count >= limit:
        return False

    cache.set(key, count + 1, timeout=60)
    return True
```

## Monitoreo y Métricas

### Logging de APIs
```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'api_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'api.log',
        },
    },
    'loggers': {
        'api': {
            'handlers': ['api_file'],
            'level': 'INFO',
        },
    },
}
```

### Métricas
```python
# views.py
import time
from prometheus_client import Counter, Histogram

# Métricas personalizadas
REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['endpoint', 'method'])
REQUEST_LATENCY = Histogram('api_request_duration_seconds', 'API request latency')

def cart_add_api(request):
    start_time = time.time()

    # lógica...

    REQUEST_COUNT.labels(endpoint='cart_add', method='POST').inc()
    REQUEST_LATENCY.observe(time.time() - start_time)
```

## Extensibilidad Futura

### Endpoints Planificados
- **Autenticación**: `/api/auth/login/`, `/api/auth/refresh/`
- **Productos**: CRUD completo con ViewSet
- **Ordenes**: Gestión de órdenes de compra
- **Usuarios**: `/api/users/profile/`
- **Analytics**: `/api/analytics/`

### Mejoras Recomendadas
1. **Implementar autenticación JWT**
2. **Configurar rate limiting**
3. **Añadir pruebas automatizadas**
4. **Documentación con Swagger**
5. **Logging estructurado**
6. **Monitoreo con Prometheus**
7. **Caché Redis para alta concurrencia**
8. **WebSockets para datos en tiempo real**

## Referencias

### Archivos Relacionados
- `shop/urls.py` - Rutas de la tienda
- `shop/views.py` - Vistas y API del carrito
- `telemetry/urls.py` - Rutas de telemetría
- `telemetry/views.py` - ViewSet de RobotPosition
- `telemetry/utils.py` - Análisis de tráfico
- `telemetry/models.py` - Modelo RobotPosition

### Documentación Externa
- [Django REST Framework](https://www.django-rest-framework.org/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Django Filters](https://django-filter.readthedocs.io/)
- [JSON Web Tokens](https://jwt.io/)

## Ver También
- [Modelos - RobotPosition](../modelos/robotposition.md)
- [Vistas - Shop Views](../vistas/shop-views.md)
- [Testing - APIs](../testing/testing-apis.md)
