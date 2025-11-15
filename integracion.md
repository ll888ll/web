## Integración del Sistema (Croody + APIs + Gateway)

Unificación
- Web (Croody/Django) como front principal: UI, i18n, tienda y punto de integración.
- APIs: Telemetría (ingesta/consulta) e IDS-ML (predicción) detrás de un gateway común (Nginx).
- Seguridad transversal en gateway (TLS, HSTS, CSP, rate limiting) y CORS/token en APIs.

Rutas
- `/` → Croody (Django/Gunicorn)
- `/api/telemetry/*` → Telemetry Gateway (FastAPI)
- `/api/ids/*` → IDS-ML (FastAPI)

Flujo de despliegue (dev)
- `proyecto_integrado/docker-compose.yml` expone 8080/8443.
- `deploy.sh` instala dependencias, levanta servicios y valida.

Flujo de despliegue (prod)
- `proyecto_integrado/docker-compose.prod.yml` publica 80/443 y añade Postgres.
- `.env` define `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL`, `TG_DB_URL`, tokens y CORS.

Mejoras aplicadas a Croody
- Contenerización con Docker, Gunicorn en prod, static con Whitenoise.
- Página `/es/integraciones/` para probar telemetría e IDS desde UI.

Siguientes pasos
- Certificados válidos (ACME) y CI/CD (build/scan/deploy).
- JWT/OIDC para SSO y llamadas entre servicios.

