# Informe Técnico – Entrega 3

## 1. Auditoría integral
- Se revisó la estructura completa (`gateway`, `services`, `Croody`, scripts, docs) validando estilo neofuturista, i18n y dependencias.
- Se detectaron áreas críticas: ausencia de registro/perfil, página de integraciones con bloque incorrecto, Telemetry Gateway sin soporte para posición/robot, falta de clientes de prueba y lineamientos de despliegue en nube.

## 2. Correcciones y mejoras
- **Telemetry Gateway**
  - Nuevos campos `robot_id`, `position_lat/lng/alt`, `environment`, `status` en SQLite/Postgres.
  - Modelos Pydantic `Position`, `TelemetryOut`, `LiveResponse` y endpoint `/api/telemetry/live` para monitoreo en tiempo real.
  - Filtro por `robot_id` en `/last` y `/query`, agrupación por robot, validaciones y compatibilidad con tokens.
  - Tests unitarios y e2e actualizados; bridge en Python ahora incluye `--robot-id`, coordenadas y cabecera `X-API-Key`.
- **Croody (Django)**
  - Nuevo modelo `UserProfile` + señales y migración `landing.0001`.
  - Formularios: registro con email, preferencias y reinicio de token; login acepta correo.
  - Vistas y rutas: `CroodySignupView`, `ProfileView` con formularios múltiples, `RobotMonitorView` y enlaces en navegación/nav drawer.
  - Página de perfil responsiva con cards para datos personales, preferencias, token y telemetría en vivo; mensajes flash globales.
  - Página de monitor público (`/robots/monitor/`) que consume los nuevos endpoints.
  - Plantilla de integraciones reparada (`block body`) y estilizada.
  - Se añadieron estilos CSS para los nuevos componentes y mensajes.
- **Clientes y documentación**
  - `clients/python/robot_publisher.py` y `clients/README.md` para pruebas externas.
  - Guía `deploy/aws/README.md` + `user-data.sh` describiendo despliegue en EC2, SGs y validaciones.
- **Robot de telemetría y modelo IDS (clases)**
  - Servicio `robot-sim` compila el servidor TCP legado y ejecuta un bridge Python que ingiere cada `DATA` en Telemetry Gateway; el monitor público muestra su estado.
  - Se portó el pipeline NSL-KDD a `services/ids-ml/training/train_ids_model.py` y se versionó `best_model.joblib` + métricas para que `/api/ids/predict` use el clasificador real.

## 3. Flujo de usuario completo
- **Registro**: formulario con nombre completo, email, idioma, tema, aceptación de términos y contraseñas; genera perfil y token personal.
- **Login**: admite usuario o correo; CTA directo hacia registro.
- **Perfil**: permite editar datos, preferencias, regenerar token y ver telemetría agregada por robot desde el nuevo gateway.
- **Monitor**: tablero público con métricas, cards por robot y ejemplo de payload para integradores.

## 4. Despliegue en AWS
- Se documentó cómo provisionar EC2, abrir puertos, correr `deploy_from_scratch.sh` y configurar `.env` con tokens (`TG_INGEST_TOKEN`, `IDS_API_TOKEN`).
- Instrucciones de verificación (`curl /api/telemetry/live`, script de clientes) garantizan accesibilidad global.

## 5. Pruebas ejecutadas
- `pytest services/telemetry-gateway/app/test_app.py`
- `python manage.py check` dentro de Croody.
- `pytest tests/e2e/test_gateway_smoke.py` para el gateway integrado.

## 6. Recomendaciones
- Automatizar despliegue AWS con Terraform/Ansible y emitir certificados válidos (ACM) detrás de un ALB.
- Conectar CloudWatch / Grafana para métricas del endpoint `/api/telemetry/live`.
- Añadir pruebas funcionales para el flujo de registro/perfil en Django.

## 7. Cumplimiento de Indicativos y gobierno DNS

| Indicativo | Evidencia | Estado |
| --- | --- | --- |
| Dos sitios web (informativo y CRUD) | Croody landing/tienda (`proyecto_integrado/Croody`), panel de cuentas/telemetría (`/cuenta/perfil/`, `/robots/monitor/`). | ✅ |
| API Telemetría + DB | FastAPI + SQLite/Postgres (`services/telemetry-gateway`), pruebas `tests/e2e/test_gateway_smoke.py`. | ✅ |
| Despliegue nube | Scripts `deploy_from_scratch.sh`, `deploy/aws/README.md`, runner self-hosted. | ✅ |
| DNS autoritativo (BIND9 primario/secundario) | `infra/dns/` (Docker + TSIG + AXFR), workflow `bind-deploy`. | 🟡 (pendiente despliegue productivo) |
| Infraestructura segregada (VPC) | Terraform (`infra/terraform`), outputs consumibles por scripts. | 🟡 (aplicar en AWS y adjuntar outputs) |

## 8. Configuración DNS autoritativa y monitoreo

- **Arquitectura**: `bind-master` (subred privada AZ A) mantiene la zona `croody.app`; `bind-slave` (AZ B) replica vía AXFR protegido con TSIG. Glue records para `ns1`/`ns2` se actualizan en el registrador tras cada despliegue.
- **Automatización**: `scripts/dns/setup_bind.sh` genera llaves/plantillas; `.github/workflows/bind-deploy.yml` construye imágenes, ejecuta `named-checkconf/named-checkzone`, publica en ECR y reinicia contenedores remoto vía SSH (con `rndc reload`).
- **Monitoreo**: logs de BIND montados en volúmenes para enviarlos a CloudWatch; validaciones operativas documentadas en `docs/dns_operacion.md` (`dig SOA`, `dig AXFR`, failover maestro/esclavo). Integrar alertas sobre `AXFR failed`, `rndc errors`, spikes de `queries`.
- **Seguimiento**: `docs/matriz_indicativos.md` actúa como checklist vivo; cada requisito se actualiza con referencias a commits, rutas y evidencias (capturas, logs). Mantenerla sincronizada con cada despliegue mayor.
