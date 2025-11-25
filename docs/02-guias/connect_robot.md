# Guía de Conexión para Robot de Telemetría

Esta guía explica cómo conectar un cliente robot al sistema "Mission Control" para enviar datos de posición y atmosféricos.

## Prerrequisitos
- Acceso de red al servidor `Croody` (Puerto 80/443 o 8000 en dev).
- Capacidad de realizar peticiones HTTP POST.

## Endpoint de Ingesta

**URL:** `POST /dashboard/api/robot-position/`
**Content-Type:** `application/json`

### Formato del Payload

El cuerpo de la petición debe ser un objeto JSON con la siguiente estructura:

```json
{
  "x": 50.5,              // Coordenada X (Float)
  "y": 20.0,              // Coordenada Y (Float)
  "atmosphere": {         // Objeto libre para datos ambientales
    "temperature": 24.5,
    "humidity": 60,
    "pressure": 1013
  }
  // Timestamp es generado automáticamente por el servidor si se omite
}
```

### Ejemplo en Python (requests)

```python
import requests
import time
import random

URL = "http://localhost:8000/dashboard/api/robot-position/"

while True:
    payload = {
        "x": random.uniform(0, 100),
        "y": random.uniform(0, 100),
        "atmosphere": {
            "temperature": 25 + random.random(),
            "status": "NOMINAL"
        }
    }
    
    try:
        response = requests.post(URL, json=payload)
        if response.status_code == 201:
            print("Datos enviados correctamente.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error de conexión: {e}")
        
    time.sleep(1)
```

## Verificación
Acceda a `/dashboard/` en su navegador. Deberá ver el indicador de "ROBOT POSITION" actualizándose en tiempo real.
