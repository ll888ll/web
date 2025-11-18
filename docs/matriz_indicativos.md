# Matriz de Cumplimiento Técnico (Indicativos)

> Plantilla editable para trazar cada requisito contra el estado actual del proyecto. Actualiza las celdas con ✅ (cumplido), 🟡 (parcial) o ❌ (pendiente) y añade notas claras con la evidencia o acciones requeridas.

## Sitios web / Django

| Requisito                                                     | Estado | Gap detectado                        | Notas                                                                                                                                             |
| ------------------------------------------------------------- | ------ | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dos sitios visibles (landing informativa + módulo CRUD)       | ✅     |                                      | Landing/tienda en `proyecto_integrado/Croody/templates` y módulo de cuentas/telemetría en `proyecto_integrado/Croody/landing/views.py:512-620`.   |
| Gestión de usuarios (registro, perfil, tokens)                | 🟡     | Falta evidencia de pruebas formales. | Flujo descrito en `proyecto_integrado/Croody/landing/forms.py:15-126` y `views.py:512-589`; documentar casos de prueba en informes.               |
| Integración UI con APIs (monitor tiempo real / integraciones) | ✅     |                                      | Monitoreo y página de integraciones documentados en `proyecto_integrado/Croody/landing/views.py:592-620` y `templates/landing/integrations.html`. |

## Telemetría / Base de datos / CRUD

| Requisito                                                                             | Estado | Gap detectado                            | Notas                                                                                                                 |
| ------------------------------------------------------------------------------------- | ------ | ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| API de ingesta (`POST /api/telemetry/ingest`) y consulta (`/last`, `/live`, `/query`) | ✅     |                                          | Implementación en `proyecto_integrado/services/telemetry-gateway/app/main.py:179-282` y pruebas en `app/test_app.py`. |
| Persistencia y compatibilidad SQLite/Postgres                                         | ✅     |                                          | Configuración dinámica `TG_DB_PATH/TG_DB_URL` en `main.py:20-152`. Ver `.env.example`.                                |
| CRUD de usuarios/telemetría visible (dashboard Django)                                | 🟡     | Falta documento de aceptación funcional. | Vista `/robots/monitor/` consume `/api/telemetry/live` (ver `landing/urls.py`); registrar screenshots/evidencias.     |

## Despliegue en AWS

| Requisito                                          | Estado | Gap detectado                                                                       | Notas                                                                      |
| -------------------------------------------------- | ------ | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Guía detallada de despliegue                       | ✅     |                                                                                     | Procedimiento paso a paso en `deploy/aws/README.md:1-180`.                 |
| Automatización (scripts/workflows CI/CD)           | 🟡     | Pipeline GitHub Actions existe pero requiere actualización tras nuevos componentes. | Ver `.github/workflows/deploy-selfhosted.yml` y `deploy_from_scratch.sh`.  |
| Evidencias de operación AWS (logs, URLs, capturas) | ❌     | Faltan anexos con pruebas reales desde AWS/Cloudflare.                              | Agregar sección en `informe_tecnico_entrega3.md` con enlaces a dominio/IP. |

## DNS BIND (Autoritativo primario/secundario)

| Requisito                                      | Estado | Gap detectado | Notas                                                                                                                                              |
| ---------------------------------------------- | ------ | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Servidor BIND primario configurado             | ✅     |               | Carpeta `infra/dns/bind-master/` + `setup_bind.sh` generan zona `croody.app` y llaves TSIG (`TSIG_KEY_NAME=croody-app-xfer`).                      |
| Servidor BIND secundario (AXFR/TSIG)           | ✅     |               | `infra/dns/bind-slave/` replica vía AXFR (IPs 172.31.42.77/172.31.71.231); workflows `bind-deploy.yml` y secretos documentados en `docs/secrets_map.md`. |
| Procedimientos de operación DNS / validaciones | ✅     |               | Runbook `docs/dns_operacion.md` + `scripts/run_local_ci.sh` / `scripts/validate_full_stack.sh` cubren `named-check*`, `dig`, `docker compose`.      |

## Infraestructura en VPC (red pública/privada)

| Requisito                                            | Estado | Gap detectado                             | Notas                                                                                                                      |
| ---------------------------------------------------- | ------ | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Definición de topología (pública/privada, roles)     | ✅     |                                           | `arquitectura.md` + `docs/indicativos_checklist.txt` documentan CIDR, SG `launch-bind` y dependencia con DNS/Bastion.      |
| Automatización IaC (Terraform/CloudFormation)        | ✅     |                                           | Módulos en `infra/terraform/` + workflow `terraform-ci.yml`; ejecución local con `scripts/run_local_ci.sh` (sección Terraform). |
| Evidencias de despliegue segmentado (logs/diagramas) | 🟡     | Falta anexar capturas de AWS console.     | `extras/local_ci_report.md` y `extras/evidencias_finales.md` guardan salidas; agregar screenshots antes de la entrega.     |

## Documentación técnica

| Requisito                              | Estado | Gap detectado                         | Notas                                                                                                                      |
| -------------------------------------- | ------ | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Manual técnico / operación             | ✅     |                                       | `manual_tecnico.md` + `docs/dns_operacion.md` describen despliegues, failover y mantenimiento.                             |
| Arquitectura detallada y decisiones    | ✅     |                                       | `arquitectura.md` incluye topología VPC, rutas y dependencias; se referencia desde `docs/indicativos_checklist.txt`.       |
| Guías de validación / evidencias / RTM | 🟡     | Añadir capturas finales (screenshots). | `scripts/run_local_ci.sh`, `scripts/validate_full_stack.sh` generan `extras/local_ci_report.md` y `extras/evidencias_finales.md`. |
| Cumplimiento indicativos documentado   | ✅     |                                       | `docs/matriz_indicativos.md` + `docs/indicativos_checklist.txt` concentran estados y tareas pendientes.                    |
