## Arquitectura del Sistema (Empresarial)

Componentes
- Gateway (Nginx): reverse proxy, TLS, rate limiting, compresión y rutas a servicios.
- Croody (Django + Gunicorn): landing, tienda y vistas; estáticos con Whitenoise.
- Telemetry Gateway (FastAPI): endpoints de ingesta y consulta; SQLite (dev) o Postgres (prod).
- IDS-ML (FastAPI): inferencia de IDS; modelo versionable; fallback simple en ausencia de artefacto.
- Base de datos (prod): Postgres para Croody y opcionalmente telemetría.

Topología
- Dev: `gateway:8080/8443` → `croody:8000`, `telemetry-gateway:9000`, `ids-ml:9100`.
- Prod: gateway en 80/443; certificados válidos.

Flujos
- Web: Cliente → Gateway → Croody; estáticos caché → Whitenoise.
- Telemetría: Cliente/Bridge → Gateway `/api/telemetry/*` → FastAPI → DB.
- IDS: Cliente/Sistema → Gateway `/api/ids/*` → FastAPI → Modelo.

Configuración por entorno
- `.env` (prod): `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL`, `ALLOWED_ORIGINS`, `TG_DB_URL`, `TG_INGEST_TOKEN`, `IDS_API_TOKEN`.

Disponibilidad y recuperación
- Stateless en servicios; datos en Postgres/volúmenes.
- Backups de DB (cron/pg_dump) y claves TLS.

Observabilidad (base y extensiones)
- Logs centralizables; rate limiting; healthz por servicio.
- Extensión: Prometheus/Grafana/Loki, Sentry.

