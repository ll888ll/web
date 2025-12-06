# Modelo RobotPosition (PLANIFICADO)

> **ESTADO:** Este modelo esta **PLANIFICADO** pero **NO IMPLEMENTADO** actualmente.
>
> La app `telemetry` y el modelo `RobotPosition` no existen en el codebase.
> Esta documentacion se mantiene como referencia para futura implementacion.

## Estado de Implementacion

| Aspecto | Estado |
|---------|--------|
| **App** | `telemetry` - NO EXISTE |
| **Modelo** | `RobotPosition` - NO IMPLEMENTADO |
| **Migraciones** | No creadas |
| **Prioridad** | Futura fase del proyecto |

## Descripcion Planificada

El modelo `RobotPosition` almacenaria datos de telemetria de robots en tiempo real, incluyendo:
- Coordenadas de posicion (x, y)
- Datos atmosfericos en formato JSON
- Timestamps de lecturas

## Ubicacion Propuesta
`/proyecto_integrado/Croody/telemetry/models.py` (no existe)

## Estructura Propuesta

```python
# telemetry/models.py (PROPUESTO - NO IMPLEMENTADO)

from django.db import models

class RobotPosition(models.Model):
    """Posicion y telemetria del robot.

    NOTA: Este modelo esta PLANIFICADO pero no implementado.
    """
    x = models.FloatField(help_text="Coordenada X (latitud)")
    y = models.FloatField(help_text="Coordenada Y (longitud)")
    atmosphere = models.JSONField(default=dict, help_text="Datos atmosfericos")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['x', 'y']),
        ]

    def __str__(self) -> str:
        return f"Position({self.x}, {self.y}) @ {self.timestamp}"
```

## Ejemplo de Datos Atmosfericos

```json
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

## Pasos para Implementar

Si se decide implementar este modelo:

### 1. Crear la app telemetry
```bash
cd proyecto_integrado/Croody
python manage.py startapp telemetry
```

### 2. Agregar a INSTALLED_APPS
```python
# croody/settings.py
INSTALLED_APPS = [
    # ...
    'telemetry',
]
```

### 3. Crear el modelo
Copiar la estructura propuesta arriba a `telemetry/models.py`

### 4. Crear migraciones
```bash
python manage.py makemigrations telemetry
python manage.py migrate telemetry
```

### 5. Registrar en admin
```python
# telemetry/admin.py
from django.contrib import admin
from .models import RobotPosition

@admin.register(RobotPosition)
class RobotPositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'x', 'y', 'timestamp')
    list_filter = ('timestamp',)
    date_hierarchy = 'timestamp'
```

## Alternativas Actuales

Mientras el modelo no este implementado, considerar:

1. **Almacenamiento externo**: InfluxDB o TimescaleDB para datos de series temporales
2. **Microservicio FastAPI**: El servicio `telemetry-gateway` ya existe en `/services/`
3. **Cache temporal**: Redis para datos en tiempo real sin persistencia

## Ver Tambien

- [FastAPI Telemetry Gateway](../../../services/telemetry-gateway/) - Servicio existente
- [Arquitectura de Microservicios](../../01-ARQUITECTURA/overview.md)

---

**NOTA:** Esta documentacion se actualizara cuando el modelo sea implementado.
