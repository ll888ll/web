## Seguridad y Escalabilidad

Seguridad (implementado)
- TLS dev, HSTS básico, CSP mínima, rate limiting en gateway.
- CORS configurable; tokens opcionales para ingest/predict; secretos via env.
- Whitenoise reduce superficie de ataque en estáticos.

Seguridad (pendiente/producción)
- Certificados válidos y rotación; headers CSP por ruta estrictos.
- OIDC (Keycloak/Auth0) para SSO; JWT firmado entre servicios.
- Secret manager (Vault/SM) y políticas de acceso por entorno.

Escalabilidad
- Contenerización y separación de responsabilidades.
- BD gestionada (Postgres), particionamiento/índices; timeseries si el volumen crece.
- HPA/KEDA en K8s; cachés Redis; colas para desacoplar picos.

Capacidad y performance
- Ajuste de workers/threads; gzip/brotli; cache estáticos con hash.
- Pruebas de carga (k6/Locust) y profiling.

