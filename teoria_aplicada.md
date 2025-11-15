## Teoría Aplicada

Patrones y conceptos
- MVC (Django): separación de vistas, modelos y plantillas; WSGI con Gunicorn.
- REST: recursos JSON, verbos HTTP, códigos y validaciones.
- CORS: controlado por allowlist en FastAPI.
- Seguridad web: TLS, HSTS, CSP, CSRF (Django), rate limiting (Nginx).
- Concurrencia: Gunicorn workers/threads; Uvicorn ASGI.
- Almacenamiento: SQLite dev vs Postgres prod; Whitenoise para estáticos.
- ML clásico: clasificación NSL-KDD; persistencia `joblib`; cuidado con `pickle`/cargas.
- Observabilidad: health endpoints y logs; extensible a métricas/tracing.

Justificación
- Reverse proxy unifica TLS, cabeceras y rutas; separa responsabilidades.
- Variables de entorno facilitan 12-factor app.
- Imágenes Docker reproducibles y Compose orquestan servicios.

