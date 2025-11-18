## Manual Técnico

Instalación (desde cero)
- Requisitos: Ubuntu/Debian con acceso sudo.
- Ejecuta: `sudo ./deploy.sh` (instala Docker/Compose y levanta el stack dev 8080/8443).
- Para prod (80/443): `sudo USE_PROD=true ./deploy_from_scratch.sh` y configura `proyecto_integrado/.env`.

Estructura de carpetas
- `proyecto_integrado/` → stack contenedorizado (gateway, Croody, servicios)
  - `robots/telemetry-robot/` → servidor C de clases + bridge hacia Telemetry Gateway.
  - `services/ids-ml/training/` → script para entrenar el modelo NSL-KDD y exportar `best_model.joblib`.
- `scripts/` → utilidades (p. ej., `generate_audits.py`)
- `AUDIT_*.txt` → auditorías por carpeta
- `*.md` → documentación técnica

Operación básica
- Arranque/parada: `docker compose up -d` / `docker compose down` (dentro de `proyecto_integrado/`).
- Logs: `docker compose logs -f <servicio>`.
- `robot-sim` publica el servidor TCP heredado de clases (puerto 9090) y un bridge Python que reenvía cada frame al Telemetry Gateway.
- `ids-ml` carga `services/ids-ml/models/best_model.joblib`; regenera el modelo ejecutando `python services/ids-ml/training/train_ids_model.py`.
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

## Procedimiento: regenerar contenedores BIND (DNS autoritativo)

1. **Preparar artefactos**  
   - Actualiza los registros en `infra/dns/bind-master/zones/<dominio>.db`.  
   - Ejecuta `scripts/dns/setup_bind.sh --domain <dominio> --master-ip <privada> --slave-ip <privada>` para refrescar llaves TSIG, plantillas `.env` y unidades systemd.
2. **Validar sintaxis**  
   ```bash
   cd infra/dns
   docker build -t bind-master-test .
   docker run --rm -v "$PWD/bind-master/zones:/zones" \
     -e DNS_ROLE=master -e DNS_DOMAIN=<dominio> \
     -e TSIG_KEY_NAME=... -e TSIG_KEY_SECRET=... \
     bind-master-test named-checkconf /etc/bind/named.conf
   docker run --rm -v "$PWD/bind-master/zones:/zones" ... \
     bind-master-test named-checkzone <dominio> /zones/<dominio>.db
   ```
3. **Desplegar via CI/CD**  
   - Confirma secretos en GitHub (`BIND_*`).  
   - `git push` a `main`/`dev` → workflow `.github/workflows/bind-deploy.yml` construye y publica imágenes, reinicia contenedores en maestro/esclavo y ejecuta `rndc reload`.
4. **Verificación**  
   - `dig @ns1.<dominio> <dominio> SOA`.  
   - `dig @ns2.<dominio> <dominio> AXFR -y <tsig>` para validar transferencia.

## Procedimiento: aplicar infraestructura con Terraform

1. **Configurar credenciales**  
   - Exporta `AWS_PROFILE` o variables `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`.  
   - Ajusta `infra/terraform/terraform.tfvars` (ejemplo):
     ```hcl
     project_name     = "croody-prod"
     aws_region       = "us-east-1"
     allowed_ssh_cidrs = ["200.10.20.30/32"]
     bastion_key_pair = "croody-prod-key"
     ```
2. **Inicializar y validar**  
   ```bash
   cd infra/terraform
   terraform fmt -recursive
   terraform init
   terraform validate
   ```
3. **Planificar y aplicar**  
   ```bash
   terraform plan -out tfplan
   terraform apply tfplan
   ```
   Outputs relevantes (`vpc_id`, `public_subnet_ids`, `bastion_public_ip`, SGs) se imprimen al finalizar; exporta o guarda en `extras/terraform_outputs.json` si deseas reutilizarlos en scripts.
4. **Post-provisión**  
   - Actualiza `deploy_from_scratch.sh` / `.env` con IDs recibidos.  
   - Configura rutas/SG en AWS para ALB, Croody y servicios.  
   - Documenta los cambios en `docs/matriz_indicativos.md`.
