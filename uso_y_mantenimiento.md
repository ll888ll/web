## Uso y Mantenimiento (Equipo Interno)

Operación
- Dev: `docker compose up -d` en `proyecto_integrado/`.
- Prod: `docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env up -d`.
- Variables en `proyecto_integrado/.env` (prod).

Tareas rutinarias
- Backups Postgres (pg_dump + cron/systemd timers); rotación de logs.
- Renovación de certificados; actualización de imágenes (CI o cron).
- Revisión de métricas y alertas (cuando se integren Prometheus/Sentry).

Actualizaciones
- Pull del repo y rebuild (`docker compose build`); migraciones Django automáticas en entrypoint prod.
- Versionado semántico de imágenes y promoción por entornos (dev→staging→prod).

Soporte y resolución
- Healthchecks: `/healthz` APIs y `/` web (302 a /es/); `docker compose ps` y `logs`.
- Escalamiento: incrementar workers Gunicorn/Uvicorn; añadir réplicas detrás del gateway.

