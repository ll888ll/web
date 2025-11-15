# Clientes de referencia Croody

Estos scripts permiten que docentes o equipos externos prueben el protocolo
expuesto en producción (AWS) o en entornos locales.

## Python · Publicador de telemetría

```
python3 clients/python/robot_publisher.py \
  --url https://YOUR_AWS_HOST/api/telemetry/ingest \
  --token <TOKEN_OPCIONAL> \
  --robot robot-borealis
```

Parámetros clave:
- `--url`: endpoint público (por ejemplo, `https://croody.example.com/api/telemetry/ingest`).
- `--token`: mismo valor que `TG_INGEST_TOKEN` o el token personal mostrado en el perfil del usuario.
- `--robot`: identificador que aparecerá en el dashboard (`robot-alpha`, `robot-beta`, etc.).

El script envía posición (`lat/lng`), variables atmosféricas y estado cada 5 s.

## cURL rápido

```
curl -X POST https://YOUR_AWS_HOST/api/telemetry/ingest \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: <TOKEN>' \
  -d '{
    "robot_id": "robot-cli",
    "position": {"lat": 19.43, "lng": -99.13},
    "data": {"TEMP": 22.4, "HUM": 40.1}
  }'
```

## Consultar datos

- `GET https://YOUR_AWS_HOST/api/telemetry/live` devuelve la última lectura por robot.
- `GET https://YOUR_AWS_HOST/api/telemetry/query?limit=100` devuelve histórico.
- `GET https://YOUR_AWS_HOST/api/ids/predict` permite probar el servicio IDS.

Incluye los tokens (`TG_INGEST_TOKEN`, `IDS_API_TOKEN`) si están configurados en el despliegue.
