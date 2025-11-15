## Manual Técnico

Instalación (desde cero)
- Requisitos: Ubuntu/Debian con acceso sudo.
- Ejecuta: `sudo ./deploy.sh` (instala Docker/Compose y levanta el stack dev 8080/8443).
- Para prod (80/443): `sudo USE_PROD=true ./deploy_from_scratch.sh` y configura `proyecto_integrado/.env`.

Estructura de carpetas
- `proyecto_integrado/` → stack contenedorizado (gateway, Croody, servicios)
- `scripts/` → utilidades (p. ej., `generate_audits.py`)
- `AUDIT_*.txt` → auditorías por carpeta
- `*.md` → documentación técnica

Operación básica
- Arranque/parada: `docker compose up -d` / `docker compose down` (dentro de `proyecto_integrado/`).
- Logs: `docker compose logs -f <servicio>`.
- Salud: `/api/telemetry/healthz` (200), home `/` (302 a `/es/`).

Configuración
- `.env` (prod): `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL`, `ALLOWED_ORIGINS`, `TG_DB_URL`, `TG_INGEST_TOKEN`, `IDS_API_TOKEN`.
- Cambia workers Gunicorn por env: `GUNICORN_WORKERS`, `GUNICORN_THREADS`.

Mantenimiento
- Backups DB (pg_dump + cron), rotación de logs (Loki/ELK recomendado).
- Renovación de certificados y actualización de imágenes (CI).

Desarrollo
- Modifica código y usa `docker compose up --build`.
- Tests e2e: curl contra endpoints; integrar k6/pytest próximamente.

Seguridad y cumplimiento
- Activa tokens/headers y CORS restrictivo en prod.
- Gestiona secretos fuera del repo (Vault/SM).

