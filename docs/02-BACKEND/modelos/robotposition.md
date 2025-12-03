# Modelo RobotPosition - Documentación Completa

## Resumen
El modelo `RobotPosition` almacena datos de telemetría de robots en tiempo real, incluyendo coordenadas de posición (x, y) y datos atmosféricos en formato JSON. Diseñado para ser escalable en escenarios de Big Data con alto volumen de lecturas.

## Ubicación
`/proyecto_integrado/Croody/telemetry/models.py`

## Estructura del Modelo

### Campos

| Campo | Tipo | Descripción | Por Defecto |
|-------|------|-------------|-------------|
| `x` | FloatField | Coordenada X (latitud) | REQUIRED |
| `y` | FloatField | Coordenada Y (longitud) | REQUIRED |
| `atmosphere` | JSONField | Datos atmosféricos (temp, humedad, etc.) | {} (dict vacío) |
| `timestamp` | DateTimeField | Timestamp de la lectura | auto_now_add |

### Ejemplo de атмосфера JSON
```python
{
    "temperature": 23.5,
    "humidity": 65.0,
    "pressure": 1013.25,
    "air_quality": "good",
    "wind_speed": 5.2,
    "battery": 87,
    "sensors": {
        "proximity": 1.2,
        "lidar": 45.6,
        "camera": "active"
    }
}
```

## Características Principales

### 1. JSONField para Flexibilidad
El campo `atmosphere` permite almacenar datos heterogéneos sin migraciones:

```python
# Ejemplo de creación
position = RobotPosition.objects.create(
    x=40.7128,
    y=-74.0060,
    atmosphere={
        "temperature": 25.3,
        "humidity": 60,
        "battery": 95
    }
)

# Acceso a datos
temp = position.atmosphere['temperature']
battery = position.atmosphere.get('battery', 0)
```

### 2. Ordenamiento Automático
```python
class Meta:
    ordering = ['-timestamp']  # Más reciente primero
```

**Ventaja:** `objects.latest('timestamp')` retorna la posición más reciente automáticamente.

### 3. Optimización para Series Temporales

**Consultas frecuentes:**
```python
# Última posición
latest = RobotPosition.objects.latest('timestamp')

# Últimas N posiciones
recent = RobotPosition.objects.all()[:100]

# Posiciones en rango de tiempo
from datetime import timedelta
now = timezone.now()
last_hour = now - timedelta(hours=1)
recent_positions = RobotPosition.objects.filter(
    timestamp__gte=last_hour
)
```

## Casos de Uso

### 1. Monitoreo en Tiempo Real
```python
def get_latest_position():
    """Obtiene la última posición registrada."""
    return RobotPosition.objects.first()

def get_position_history(hours=24):
    """Obtiene historial de posiciones de las últimas N horas."""
    from datetime import timedelta
    since = timezone.now() - timedelta(hours=hours)
    return RobotPosition.objects.filter(timestamp__gte=since)
```

### 2. Análisis de Trayectoria
```python
def get_trajectory(robot_id=None, limit=1000):
    """Obtiene trayectoria del robot."""
    positions = RobotPosition.objects.all()[:limit]
    return [(p.x, p.y) for p in positions]
```

### 3. Filtros Geográficos
```python
def get_positions_in_bounds(min_x, max_x, min_y, max_y):
    """Filtra posiciones en un área rectangular."""
    return RobotPosition.objects.filter(
        x__gte=min_x,
        x__lte=max_x,
        y__gte=min_y,
        y__lte=max_y
    )
```

### 4. Análisis Atmosférico
```python
def get_avg_temperature(days=7):
    """Calcula temperatura promedio de los últimos N días."""
    from datetime import timedelta
    since = timezone.now() - timedelta(days=days)

    positions = RobotPosition.objects.filter(
        timestamp__gte=since
    ).values_list('atmosphere', flat=True)

    temps = [p.get('temperature') for p in positions if p.get('temperature')]
    return sum(temps) / len(temps) if temps else 0
```

## API Serializers

### Serializer Simple
```python
from rest_framework import serializers

class RobotPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobotPosition
        fields = '__all__'

    def validate_atmosphere(self, value):
        """Valida que atmosphere sea un dict."""
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "Atmosphere debe ser un diccionario JSON."
            )
        return value
```

### Serializer con Datos Calculados
```python
class RobotPositionWithDistanceSerializer(serializers.ModelSerializer):
    distance_from_origin = serializers.SerializerMethodField()

    class Meta:
        model = RobotPosition
        fields = '__all__'

    def get_distance_from_origin(self, obj) -> float:
        """Calcula distancia desde origen (0,0)."""
        import math
        return math.sqrt(obj.x**2 + obj.y**2)
```

## Endpoints API

### Crear Posición (POST)
```python
# views.py
from rest_framework import viewsets
from .models import RobotPosition
from .serializers import RobotPositionSerializer

class RobotPositionViewSet(viewsets.ModelViewSet):
    queryset = RobotPosition.objects.all().order_by('-timestamp')
    serializer_class = RobotPositionSerializer

    def perform_create(self, serializer):
        # Validación adicional antes de guardar
        instance = serializer.save()
        logger.info(f"Position saved: {instance.id}")
```

### Obtener Última Posición (GET /latest)
```python
@api_view(['GET'])
def get_latest_position(request):
    """Retorna la posición más reciente."""
    latest = RobotPosition.objects.first()
    if latest:
        serializer = RobotPositionSerializer(latest)
        return Response(serializer.data)
    return Response({'error': 'No positions found'}, status=404)
```

### Listar Posiciones (GET)
```python
# Con filtros opcionales
@api_view(['GET'])
def list_positions(request):
    """Lista posiciones con filtros."""
    queryset = RobotPosition.objects.all()

    # Filtro por timestamp
    if start_date := request.GET.get('start_date'):
        queryset = queryset.filter(timestamp__gte=start_date)

    if end_date := request.GET.get('end_date'):
        queryset = queryset.filter(timestamp__lte=end_date)

    # Paginación
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 100))
    start = (page - 1) * per_page
    end = start + per_page

    serializer = RobotPositionSerializer(queryset[start:end], many=True)
    return Response({
        'results': serializer.data,
        'count': queryset.count(),
        'page': page,
        'per_page': per_page
    })
```

## Optimización para Big Data

### 1. Indexación
```python
class Meta:
    ordering = ['-timestamp']
    indexes = [
        # Índice compuesto para consultas frecuentes
        models.Index(fields=['timestamp']),
        models.Index(fields=['x', 'y']),  # Filtrado geográfico
    ]
```

### 2. Particionado de Tabla (PostgreSQL)
```python
# Para grandes volúmenes, particionar por timestamp mensual
class Migration(migrations.Migration):
    operations = [
        # Crear tabla particionada
        migrations.RunSQL(
            """
            CREATE TABLE telemetry_robotposition_p (
                LIKE telemetry_robotposition INCLUDING ALL
            ) PARTITION BY RANGE (timestamp);
            """,
            reverse_sql="DROP TABLE telemetry_robotposition_p;"
        )
    ]
```

### 3. Archivado
```python
def archive_old_positions(days=90):
    """Archiva posiciones antiguas a tabla de archivo."""
    cutoff = timezone.now() - timedelta(days=days)

    # Obtener registros antiguos
    old_positions = RobotPosition.objects.filter(
        timestamp__lt=cutoff
    )

    # Archivar (opcional: mover a tabla de archivo)
    count = old_positions.count()
    old_positions.delete()

    logger.info(f"Archived {count} positions older than {cutoff}")
    return count
```

### 4. Agregación
```python
from django.db.models import Avg, Max, Min

def get_position_stats(days=30):
    """Obtiene estadísticas de posiciones."""
    since = timezone.now() - timedelta(days=days)

    stats = RobotPosition.objects.filter(
        timestamp__gte=since
    ).aggregate(
        avg_x=Avg('x'),
        max_x=Max('x'),
        min_x=Min('x'),
        avg_y=Avg('y'),
        max_y=Max('y'),
        min_y=Min('y'),
        total=Count('id')
    )

    return stats
```

## Testing

### Unit Tests
```python
# tests/unit/models/test_robotposition.py
import pytest
from django.utils import timezone
from telemetry.models import RobotPosition

@pytest.mark.django_db
class TestRobotPosition:
    def test_create_position(self):
        """Test creación de posición."""
        position = RobotPosition.objects.create(
            x=10.5,
            y=20.3,
            atmosphere={'temperature': 25.0}
        )
        assert position.x == 10.5
        assert position.y == 20.3
        assert position.atmosphere['temperature'] == 25.0

    def test_ordering(self):
        """Test ordenamiento por timestamp descendente."""
        p1 = RobotPosition.objects.create(x=1, y=1, atmosphere={})
        p2 = RobotPosition.objects.create(x=2, y=2, atmosphere={})

        positions = list(RobotPosition.objects.all())
        assert positions[0] == p2  # Más reciente primero
        assert positions[1] == p1

    def test_atmosphere_json(self):
        """Test almacenamiento JSON flexible."""
        position = RobotPosition.objects.create(
            x=0,
            y=0,
            atmosphere={
                'temperature': 20.0,
                'humidity': 65,
                'nested': {'key': 'value'}
            }
        )

        position.refresh_from_db()
        assert position.atmosphere['temperature'] == 20.0
        assert position.atmosphere['nested']['key'] == 'value'
```

### Factory
```python
# factories.py
import factory
from telemetry.models import RobotPosition
from django.utils import timezone
import random

class RobotPositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RobotPosition

    x = factory.LazyFunction(lambda: random.uniform(-180, 180))
    y = factory.LazyFunction(lambda: random.uniform(-90, 90))
    atmosphere = factory.LazyFunction(lambda: {
        'temperature': round(random.uniform(15, 30), 1),
        'humidity': random.randint(40, 80)
    })

@pytest.fixture
def robot_position(db):
    return RobotPositionFactory()
```

## Migraciones

### Migración Inicial
```python
# 0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name='RobotPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('atmosphere', models.JSONField(default=dict)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
```

### Migración de Datos de Prueba
```python
# 0002_seed_positions.py
from django.db import migrations
import random
from datetime import timedelta

def create_sample_positions(apps, schema_editor):
    RobotPosition = apps.get_model('telemetry', 'RobotPosition')
    base_time = timezone.now() - timedelta(hours=100)

    for i in range(100):
        RobotPosition.objects.create(
            x=round(random.uniform(-180, 180), 4),
            y=round(random.uniform(-90, 90), 4),
            atmosphere={
                'temperature': round(random.uniform(15, 30), 1),
                'humidity': random.randint(40, 80),
                'battery': random.randint(10, 100)
            },
            timestamp=base_time + timedelta(hours=i)
        )

def reverse_create_sample_positions(apps, schema_editor):
    RobotPosition = apps.get_model('telemetry', 'RobotPosition')
    RobotPosition.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('telemetry', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_positions, reverse_create_sample_positions),
    ]
```

## Consideraciones de Performance

### 1. Consultas Eficientes
```python
# Good: Solo campos necesarios
positions = RobotPosition.objects.values('x', 'y', 'timestamp')

# Avoid: Traer todos los campos
# positions = RobotPosition.objects.all()
```

### 2. Paginación
```python
from django.core.paginator import Paginator

def paginate_positions(request, queryset):
    paginator = Paginator(queryset, 1000)  # 1000 por página
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
```

### 3. Caché
```python
from django.core.cache import cache

def get_cached_latest_position():
    cache_key = 'latest_robot_position'
    position = cache.get(cache_key)

    if not position:
        position = RobotPosition.objects.first()
        if position:
            cache.set(cache_key, position, 30)  # 30 segundos

    return position
```

## Integración con FastAPI

### Dependency para Autenticación por Token
```python
# services/telemetry-gateway/main.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_position(token: str = Depends(security)):
    """Autenticación por token de ingestión."""
    from landing.models import UserProfile

    try:
        profile = UserProfile.objects.get(ingest_token=token.credentials)
        return profile
    except UserProfile.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

### Endpoint FastAPI
```python
# services/telemetry-gateway/main.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="Telemetry Gateway")

class PositionData(BaseModel):
    x: float
    y: float
    atmosphere: Dict[str, Any]

@app.post("/api/telemetry/ingest")
async def ingest_position(
    data: PositionData,
    profile=Depends(get_current_position)
):
    """Ingere posición de telemetría."""
    position = RobotPosition.objects.create(
        x=data.x,
        y=data.y,
        atmosphere=data.atmosphere
    )
    return {
        "success": True,
        "position_id": position.id,
        "timestamp": position.timestamp
    }
```

## Seguridad

### Validación de Coordenadas
```python
def clean_coordinates(self):
    x = self.cleaned_data.get('x')
    y = self.cleaned_data.get('y')

    # Validar rangos geográficos
    if x < -180 or x > 180:
        raise forms.ValidationError("X debe estar entre -180 y 180.")
    if y < -90 or y > 90:
        raise forms.ValidationError("Y debe estar entre -90 y 90.")

    return x, y
```

### Limitación de Rate
```python
# middleware.py
from django.core.cache import cache
from django.http import JsonResponse

class TelemetryRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/telemetry/'):
            # Rate limiting: 100 requests per minute per token
            token = request.headers.get('X-Token')
            if token:
                key = f'telemetry_rate:{token}'
                count = cache.get(key, 0)

                if count >= 100:
                    return JsonResponse(
                        {'error': 'Rate limit exceeded'},
                        status=429
                    )

                cache.set(key, count + 1, 60)

        return self.get_response(request)
```

## Monitoreo

### Métricas Prometheus
```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge

positions_total = Counter(
    'robot_positions_total',
    'Total positions ingested',
    ['source']
)

position_age = Histogram(
    'position_age_seconds',
    'Age of positions'
)

active_robots = Gauge(
    'active_robots',
    'Number of active robots'
)
```

### Alertas
```python
# alerts.py
def check_for_stale_positions(threshold_hours=1):
    """Verifica si hay posiciones recientes."""
    cutoff = timezone.now() - timedelta(hours=threshold_hours)
    recent_count = RobotPosition.objects.filter(
        timestamp__gte=cutoff
    ).count()

    if recent_count == 0:
        send_alert("No recent positions received!")

    return recent_count
```

## Referencias

### Archivos Relacionados
- `telemetry/views.py` - API endpoints
- `services/telemetry-gateway/main.py` - FastAPI gateway
- `landing/models.py` - UserProfile (tokens)

### Documentación Externa
- [Django JSONField](https://docs.djangoproject.com/en/stable/ref/models/fields/#jsonfield)
- [PostgreSQL JSON Functions](https://www.postgresql.org/docs/current/functions-json.html)
- [FastAPI](https://fastapi.tiangolo.com/)

## Ver También
- [Telemetry API Views](../vistas/telemetry-views.md)
- [FastAPI Gateway Integration](../api/rest-endpoints.md)
- [Rate Limiting Middleware](../../06-SEGURIDAD/configuraciones.md#rate-limiting)
