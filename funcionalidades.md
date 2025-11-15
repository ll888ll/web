## Funcionalidades por Módulo

Gateway (Nginx)
- TLS dev (self-signed), HSTS configurable, CSP básica.
- Reverse proxy a `/`, `/api/telemetry/*`, `/api/ids/*`.
- Rate limiting para mitigar abuso.

Croody (Django)
- Landing y tienda (i18n), autenticación, estáticos optimizados.
- Despliegue con Gunicorn; configuración por variables de entorno.

Telemetry Gateway (FastAPI)
- `POST /api/telemetry/ingest` (token opcional), `GET /api/telemetry/{last,query}`.
- Almacenamiento SQLite (dev) o Postgres (prod).

IDS-ML (FastAPI)
- `POST /api/ids/predict`, `GET /api/ids/model`.
- Fallback sin modelo; admite joblib.

Bridge Telemetría (opcional)
- Cliente que lee líneas `DATA ...` de servidor C y las ingiere vía HTTP.

Despliegue desde cero
- `deploy_from_scratch.sh`: instala Docker/Compose, obtiene repo, configura y valida.

