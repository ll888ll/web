# Resumen de avances hacia `indicativos.txt`

## DNS autoritativo
- Implementamos `infra/dns/` con contenedores BIND9 (master/slave), plantillas `named.conf`, `zone.db.tpl`, scripts de despliegue y documentación.
- `scripts/dns/setup_bind.sh` genera llaves TSIG, zonas, `.env` y servicios systemd; se usó para crear la zona `croody.app` y las claves `croody-app-xfer`.
- Workflow `.github/workflows/bind-deploy.yml` construye imágenes, valida `named.conf/zone`, publica en ECR y despliega en EC2 vía SSH (`bind-master` y `bind-slave`), ejecutando `rndc reload`.
- `docs/dns_operacion.md` describe altas de registros, pruebas `dig`, failover y monitoreo.

## Infraestructura AWS (VPC pública/privada)
- Terraform modular (`infra/terraform/`) crea VPC, subredes públicas/privadas, NAT, tablas de ruteo, Security Groups y bastion.
- Outputs (`vpc_id`, subredes, SGs, NAT, bastion IP) alimentan scripts y documentación (`arquitectura.md`, `manual_tecnico.md`).
- Guía `Readme` en Terraform explica `init/plan/apply` y cómo incorporar los outputs en despliegues.

## Documentación actualizada
- `manual_tecnico.md` ahora incluye procedimientos para regenerar BIND y aplicar Terraform.
- `arquitectura.md` documenta la topología VPC, flujo AXFR, controles de seguridad y diagrama (`terraform graph`).
- `informe_tecnico_entrega3.md` agrega matriz de cumplimiento, sección DNS autoritativo y monitoreo.
- `docs/dns_operacion.md` y `plan_practico_endurecimiento.md` complementan los runbooks y controles de hardening.

## Pipelines CI/CD
- Workflows añadidos: `dns-lint`, `bind-deploy`, `terraform-ci`, `full-stack-validate`.
- `scripts/validate_full_stack.sh` levanta BIND, ejecuta `dig`, `curl`, `pytest` y recopila evidencias en `extras/evidencias_finales.md`.
- Secrets requeridos documentados (IPs privadas, TSIG, AWS/ECR, SSH, Cloudflare).

## Próximos pasos
- Confirmar que los secrets (`BIND_SLAVE_PRIVATE_IP`, `AWS_*`) reflejan los valores reales de las nuevas instancias.
- Ejecutar `terraform plan/apply` en AWS y registrar outputs finales en `extras/`.
- Mantener `docs/matriz_indicativos.md` actualizada con evidencias (capturas, artefactos) antes de la entrega.
