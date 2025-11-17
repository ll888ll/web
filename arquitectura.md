## Arquitectura del Sistema (Empresarial)

Componentes
- Gateway (Nginx): reverse proxy, TLS, rate limiting, compresión y rutas a servicios.
- Croody (Django + Gunicorn): landing, tienda y vistas; estáticos con Whitenoise.
- Telemetry Gateway (FastAPI): endpoints de ingesta y consulta; SQLite (dev) o Postgres (prod).
- IDS-ML (FastAPI): inferencia de IDS; modelo versionable; fallback simple en ausencia de artefacto.
- Base de datos (prod): Postgres para Croody y opcionalmente telemetría.

Topología
- Dev: `gateway:8080/8443` → `croody:8000`, `telemetry-gateway:9000`, `ids-ml:9100`.
- Prod: gateway en 80/443; certificados válidos.

Flujos
- Web: Cliente → Gateway → Croody; estáticos caché → Whitenoise.
- Telemetría: Cliente/Bridge → Gateway `/api/telemetry/*` → FastAPI → DB.
- IDS: Cliente/Sistema → Gateway `/api/ids/*` → FastAPI → Modelo.

Configuración por entorno
- `.env` (prod): `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL`, `ALLOWED_ORIGINS`, `TG_DB_URL`, `TG_INGEST_TOKEN`, `IDS_API_TOKEN`.

Disponibilidad y recuperación
- Stateless en servicios; datos en Postgres/volúmenes.
- Backups de DB (cron/pg_dump) y claves TLS.

Observabilidad (base y extensiones)
- Logs centralizables; rate limiting; healthz por servicio.
- Extensión: Prometheus/Grafana/Loki, Sentry.

## Red AWS (VPC pública/privada)

| Capa | Recursos | Descripción |
| --- | --- | --- |
| Pública | `subnets` 10.50.10.0/24 y 10.50.20.0/24 | ALB, NAT Gateway, Bastion (Amazon Linux 2023 + SG SSH). |
| Privada | `subnets` 10.50.110.0/24 y 10.50.210.0/24 | ECS/EC2 para gateway Croody, Telemetry Gateway, IDS, DB/Postgres. |
| Seguridad | SGs (`alb-sg`, `app-sg`, `db-sg`) | HTTP/HTTPS público, SSH restringido via bastion, puertos internos sólo entre SG confiables. |
| Salida | NAT Gateway + route tables | Subred privada roteada por NAT para actualizaciones sin exponer IP pública. |

### Diagrama (terraform graph)

Generar el gráfico actualizado tras cada cambio IaC:

```bash
cd infra/terraform
terraform graph | dot -Tpng > extras/diagrama_vpc.png
```

Anexa la imagen en entregables (ej. `extras/diagrama_vpc.png`) y referencia la última versión en informes.

## Flujo DNS autoritativo (BIND9)

1. Contenedores `bind-master` y `bind-slave` (Docker) se despliegan en subredes privadas separadas.
2. Zona `croody.app` reside en el maestro (`/zones/croody.app.db`); esclavo sincroniza vía AXFR/IXFR protegido con TSIG (HMAC-SHA256).
3. `bind-master` notifica cambios (`also-notify`) hacia la IP privada del esclavo; `rndc reload` se ejecuta tras cada despliegue CI/CD.
4. Glue records (`ns1`, `ns2`) apuntan a IPs públicas asignadas (si aplica) o a entradas Cloudflare (si se usa proxy).
5. Consultas externas golpean `ns2` (esclavo) ubicado en una AZ distinta; en caso de caída, `ns1` puede exponerse temporalmente activando SG y EIP.

## Seguridad y hardening

- **TSIG/ACL**: transferencias limitadas a `bind-slave` IP + clave TSIG (`scripts/dns/setup_bind.sh`).
- **Logs DNS**: `/var/log/named` montado en volúmenes; integra con CloudWatch/ELK para alertar sobre AXFR anómalos.
- **Bastion**: única entrada SSH; SG `allowed_ssh_cidrs` configurable. Bastion se usa para túneles hacia subred privada.
- **Infra**: terraform outputs (`alb_security_group_id`, `app_security_group_id`, `db_security_group_id`) se consumen por scripts de despliegue para garantizar segmentación consistente.

## Referencias cruzadas

- `infra/terraform/README.md`: detalle IaC.
- `infra/dns/README.md`: topología BIND y procedimientos.
- `docs/dns_operacion.md`: runbooks de DNS.
