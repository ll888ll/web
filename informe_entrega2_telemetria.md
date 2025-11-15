# Entrega 2 – Telemetría en tiempo real (croody.app)

## Resumen

- Se desplegó un Gateway de Telemetría (FastAPI) y una Web (Django) en AWS con HTTPS válido (Let’s Encrypt), accesibles bajo `https://croody.app`.
- El sistema expone un punto de ingestión público y muestra en tiempo real posición y variables atmosféricas por robot sobre un mapa (Leaflet) y tarjetas informativas.
- Se entregan clientes de referencia para que el docente pruebe desde su ubicación.

## Endpoints públicos

- Ingesta (POST): `https://croody.app/api/telemetry/ingest`
  - Cuerpo JSON: `{ "robot_id": "robot-x", "ts": "ISO8601", "position": {"lat": 0, "lng": 0, "alt": 100}, "environment": "field", "status": "navigating", "data": {"TEMP": 23.1, ...} }`
  - Token (opcional): cabecera `X-API-Key: <TG_INGEST_TOKEN>` (no requerido por defecto).
- Live (GET): `https://croody.app/api/telemetry/live`
- Último (GET): `https://croody.app/api/telemetry/last?robot_id=...`

## Web de monitor en tiempo real

- URL: `https://croody.app/robots/monitor/`
- Mapa en tiempo real (Leaflet) y tarjetas por robot. Se refresca cada 4 s.
- Si el robot envía `position.lat/lng`, se actualizará su marcador.

## Cliente de referencia (docente)

### Python (CLI)

Ruta: `clients/python/robot_publisher.py`

Uso básico (cada 5 s):

```bash
python3 clients/python/robot_publisher.py \
  --url https://croody.app/api/telemetry/ingest \
  --robot robot-docente \
  --lat 4.7110 --lng -74.0721 --alt 2600 \
  --jitter 0.001 \
  --interval 5
```

Notas:
- `--lat/--lng`: su ubicación en grados decimales. `--alt` opcional.
- `--jitter`: mueve ligeramente la posición para simular movimiento.
- Si el Gateway exige token: añadir `--token <TG_INGEST_TOKEN>`.

### Ejemplo de payload JSON

```json
{
  "robot_id": "robot-docente",
  "ts": "2025-11-15T18:35:00Z",
  "position": {"lat": 4.7110, "lng": -74.0721, "alt": 2600},
  "environment": "field",
  "status": "navigating",
  "data": {"TEMP": 24.1, "HUM": 43.0}
}
```

## Implementación realizada

1) API de telemetría (FastAPI)
   - Endpoints `/ingest`, `/last`, `/live` con SQLite en volumen Docker.
   - Soporta `position` y deduce posición de `LAT/LON` si viene en `data`.

2) Web (Django)
   - Página `robots/monitor/` actualizada para incluir mapa Leaflet, marcadores por robot y tarjetas con variables ATM.
   - Refresco cada 4 s con `/api/telemetry/live`.

3) Robot de clases (simulador)
   - Servicio `robot-sim` (Docker) compila el servidor TCP heredado y puentea `DATA` → HTTP ingest automáticamente.

4) Despliegue y seguridad
   - Let’s Encrypt en origen (auto-renovación mensual por cron).
   - Cloudflare preparado: DNS/SSL auto-config y promoción a proxied + strict cuando la zona esté activa.
   - Auto-deploy por runner self-hosted en EC2 (cada push a `main`).

## Pruebas y validación

- `curl -s https://croody.app/api/telemetry/healthz` → `{ "status": "ok" }`
- Publicar desde CLI y verificar marcador en el mapa.
- `curl -s https://croody.app/api/telemetry/live` → incluye `robot-docente` y su última posición.

## Datos de conexión

- Dominio: `croody.app`
- Ingest: `https://croody.app/api/telemetry/ingest`
- Token: no requerido por defecto (añadir `--token` si se habilita).
- Intervalo recomendado de envío: 5–10 s.

## Anexos

- Código modificado principal:
  - `proyecto_integrado/Croody/templates/landing/monitor.html`: mapa Leaflet y markers.
  - `clients/python/robot_publisher.py`: flags `--lat/--lng/--alt/--jitter`.
  - `proyecto_integrado/docker-compose.yml`: volúmenes para SQLite (Croody, Telemetry).
  - Workflows de deploy y Cloudflare (auto).

