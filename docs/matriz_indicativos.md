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

| Requisito                                      | Estado | Gap detectado                                  | Notas                                                              |
| ---------------------------------------------- | ------ | ---------------------------------------------- | ------------------------------------------------------------------ |
| Servidor BIND primario configurado             | ❌     | No existe configuración ni carpeta específica. | Crear `infra/dns/bind-master/` y documentar.                       |
| Servidor BIND secundario (AXFR/TSIG)           | ❌     | Sin planes de failover ni TSIG definidos.      | Necesario cumplir exigencia de servidor secundario del indicativo. |
| Procedimientos de operación DNS / validaciones | ❌     | Falta runbook y scripts `dig/named-check*`.    | Añadir guía en `docs/` y automatizar pruebas.                      |

## Infraestructura en VPC (red pública/privada)

| Requisito                                            | Estado | Gap detectado                                                                       | Notas                                                    |
| ---------------------------------------------------- | ------ | ----------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Definición de topología (pública/privada, roles)     | 🟡     | Diagrama textual en `arquitectura.md` pero requiere mayor detalle (CIDR, SGs, NAT). | Añadir diagrama actualizado y tabla de direccionamiento. |
| Automatización IaC (Terraform/CloudFormation)        | ❌     | No hay código Terraform para VPC/ALB/EC2.                                           | Crear módulo `infra/terraform` y valídalo en CI.         |
| Evidencias de despliegue segmentado (logs/diagramas) | ❌     | Falta anexar diagramas y comprobantes de VPC funcionando.                           | Documentar en `informe_tecnico_entrega3.md`.             |

## Documentación técnica

| Requisito                              | Estado | Gap detectado                                                              | Notas                                                                                          |
| -------------------------------------- | ------ | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Manual técnico / operación             | 🟡     | Debe incluir procedimientos DNS/VPC pendientes.                            | `manual_tecnico.md:1-37`.                                                                      |
| Arquitectura detallada y decisiones    | 🟡     | Falta diagrama actualizado con DNS/VPC.                                    | `arquitectura.md:1-17`.                                                                        |
| Guías de validación / evidencias / RTM | 🟡     | Necesario anexar resultados de pruebas finales (AWS/DNS).                  | `informe_tecnico_entrega3.md`, `informe_entrega2_telemetria.md`, `docs/matriz_indicativos.md`. |
| Cumplimiento indicativos documentado   | 🟡     | Esta matriz debe mantenerse actualizada con evidencia (capturas, commits). | Referenciar cambios futuros y commits relevantes.                                              |
