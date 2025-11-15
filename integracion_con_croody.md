## Integración con Croody (Revisión e Incorporación)

Resumen
- Se incorporó Croody (Django) como servicio web principal dentro de `proyecto_integrado/Croody` con despliegue WSGI (Gunicorn) y optimización de estáticos (Whitenoise).
- Se añadió una página de integraciones (`/es/integraciones/`) para probar y demostrar los servicios de Telemetría e IDS-ML desde la UI.

Mejoras realizadas
- Contenerización con Docker; entrypoints separados para dev/prod.
- Configuración por variables (SECRET_KEY, ALLOWED_HOSTS, DATABASE_URL).
- Gateway Nginx con TLS dev, HSTS y CSP base; reverse proxy y rate limiting.

Buenas prácticas de Croody adoptadas
- i18n (multi-idioma), navegación accesible, plantillas limpias.
- Estructura de apps (landing/shop) y separación de estáticos/plantillas.

Siguientes pasos (profesionalización)
- Integrar autenticación corporativa (OIDC) y panel de administración endurecido.
- Migrar DB a Postgres gestionado; añadir backups/retención.
- Observabilidad (Sentry, Prometheus/Grafana) y CI/CD completo.

