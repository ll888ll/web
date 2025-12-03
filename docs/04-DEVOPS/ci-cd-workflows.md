# CI/CD Workflows - Documentación Completa

## Resumen
El sistema CI/CD de Croody implementa 7 workflows automatizados que cubren linting, testing, validación, despliegue, infraestructura y DNS. Utiliza GitHub Actions con estrategias multi-stage, validaciones cruzadas y despliegues seguros.

## Ubicación
- **Workflows Directory**: `/.github/workflows/`
- **7 Workflows**:
  1. `ci.yml` - Linting, Testing, Security
  2. `deploy.yml` - Despliegue por SSH
  3. `terraform-ci.yml` - Validación Terraform
  4. `full-stack-validate.yml` - Validación end-to-end
  5. `bind-deploy.yml` - Despliegue DNS BIND9
  6. `dns-lint.yml` - Linting DNS
  7. `deploy-selfhosted.yml` - Despliegue self-hosted con Cloudflare

## Arquitectura General de CI/CD

### Flujo de Desarrollo
```
┌─────────────────────────────────────────────────────────┐
│                     Develop/PR                           │
└────────────────────────┬──────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────┐
│ 1. DNS Lint (bind-dns-lint.yml)                          │
│    - Validación configuraciones BIND                     │
│    - named-checkconf, named-checkzone                    │
└────────────────────────┬──────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────┐
│ 2. CI (ci.yml)                                           │
│    - Linting (ruff, black, isort)                        │
│    - Type checking (mypy)                                │
│    - Unit tests (FastAPI health checks)                  │
│    - Security (bandit, pip-audit, gitleaks)              │
└────────────────────────┬──────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────┐
│ 3. Terraform CI (terraform-ci.yml)                       │
│    - Terraform fmt, init, validate                       │
│    - TFLint para best practices                          │
└────────────────────────┬──────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────┐
│ 4. Full Stack Validate (full-stack-validate.yml)         │
│    - End-to-end testing                                  │
│    - Docker Compose integration                          │
│    - Evidencias de testing                               │
└────────────────────────┬──────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────┐
│ 5. Merge to Main                                         │
└────────────────────────┬──────────────────────────────────┘
                         │
    ┌───────────────────┼───────────────────┐
    │                   │                   │
┌───▼───┐         ┌─────▼─────┐     ┌──────▼──────┐
│Deploy │         │ Terraform │     │   Bind      │
│SSH   │         │   Deploy  │     │  Deploy     │
└───┬───┘         └───────────┘     └──────┬──────┘
    │                                   │
    └───────────────────┬───────────────┘
                        │
                 ┌──────▼────────┐
                 │  Self-Hosted  │
                 │  Deploy       │
                 └───────────────┘
```

## Workflow 1: CI (Linting, Testing, Security)

### Trigger
```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

### Job: build-test
**Runner**: `ubuntu-latest`

#### Step 1: Checkout
```yaml
- uses: actions/checkout@v4
```
- **Propósito**: Descarga el código del repositorio
- **Versión**: v4 (última estable)

#### Step 2: Setup Python
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
```
- **Propósito**: Configura Python 3.11
- **Versión**: v5 (última)

#### Step 3: Install Tooling
```bash
pip install ruff black isort mypy pytest httpx bandit pip-audit
      fastapi uvicorn pydantic
```

**Herramientas Instaladas**:
- `ruff`: Linter ultrarrápido (reemplaza flake8 + pyflakes + pep8)
- `black`: Code formatter
- `isort`: Import sorter
- `mypy`: Type checker
- `pytest`: Test framework
- `httpx`: HTTP client para tests
- `bandit`: Security linter
- `pip-audit`: Vulnerabilidades en dependencias
- `fastapi`, `uvicorn`, `pydantic`: Para tests FastAPI

#### Step 4: Linting
```bash
ruff check proyecto_integrado || true
black --check proyecto_integrado || true
isort --check-only proyecto_integrado || true
```

**Validaciones**:
- **ruff**: Sintaxis, estilo, complejidad
- **black**: Formato de código consistente
- **isort**: Orden de imports
- **`|| true`**: No falla el build por warnings

#### Step 5: Type Checking
```bash
mypy proyecto_integrado/services/telemetry-gateway/app \
     proyecto_integrado/services/ids-ml/app || true
```

**Validación**:
- Solo servicios FastAPI (telemetry, ids-ml)
- Verificación de tipos estáticos
- Detecta errores de tipo antes de runtime

#### Step 6: Unit Tests (FastAPI Apps)
```python
import importlib.util
from pathlib import Path
from fastapi.testclient import TestClient

# Test telemetry gateway healthz
p = Path('proyecto_integrado/services/telemetry-gateway/app/main.py')
spec = importlib.util.spec_from_file_location('tg_main', p)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
c = TestClient(m.app)
r = c.get('/healthz'); assert r.status_code == 200

# Test IDS-ML healthz
p2 = Path('proyecto_integrado/services/ids-ml/app/main.py')
spec2 = importlib.util.spec_from_file_location('ids_main', p2)
m2 = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(m2)
c2 = TestClient(m2.app)
r2 = c2.get('/healthz'); assert r2.status_code == 200
```

**Características**:
- **Dynamic import**: Carga módulos sin instalación
- **TestClient**: Simula HTTP client sin servidor real
- **Health endpoints**: Verifica que servicios respondan
- **Assertions**: status_code == 200

#### Step 7: Security Scans
```bash
bandit -q -r proyecto_integrado/services || true
pip-audit -r proyecto_integrado/Croody/requirements.txt || true
```

**Scans**:
- **bandit**: Vulnerabilidades de seguridad en código Python
- **pip-audit**: CVEs en dependencias
- **`-q`**: Modo silencioso (quiet)
- **`|| true`**: Continúa si encuentra issues

#### Step 8: Gitleaks
```yaml
- name: Gitleaks
  uses: zricethezav/gitleaks-action@master
  continue-on-error: true
  with:
    args: detect --no-git --redact --exclude-file .gitleaksignore
```

**Características**:
- **Detecta secrets**: API keys, passwords, tokens
- **`--no-git`**: Escanea archivos directamente (no historial)
- **`--redact`**: Oculta secrets en logs
- **`.gitleaksignore`**: Excluye falsos positivos
- **`continue-on-error`**: No falla build por warnings

## Workflow 2: Deploy (SSH)

### Trigger
```yaml
on:
  workflow_dispatch:
```
- **Manual trigger**: Solo se ejecuta manualmente
- **Usos**: Deploys a producción bajo demanda

### Concurrency
```yaml
concurrency:
  group: deploy-production
  cancel-in-progress: false
```

**Configuración**:
- **group**: `deploy-production` - Agrupa todas las ejecuciones
- **cancel-in-progress**: `false` - No cancela deployments en curso

### Environment Variables
```yaml
env:
  DEPLOY_HOST: ${{ secrets.DEPLOY_HOST }}
  DEPLOY_USER: ${{ secrets.DEPLOY_USER }}
  DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
  DEPLOY_PATH: ${{ secrets.DEPLOY_PATH }}
  DEPLOY_PORT: ${{ secrets.DEPLOY_PORT || '22' }}
```

**Secrets Requeridos**:
- `DEPLOY_HOST`: IP/hostname del servidor
- `DEPLOY_USER`: Usuario SSH
- `DEPLOY_KEY`: Clave privada SSH (base64)
- `DEPLOY_PATH`: Directorio de despliegue
- `DEPLOY_PORT`: Puerto SSH (default: 22)

### Job: deploy

#### Step 1: Checkout
```yaml
- name: Checkout
  uses: actions/checkout@v4
```

#### Step 2: Create Release Archive
```bash
tar -c -z --ignore-failed-read -f telematicache.tar.gz .
```

**Características**:
- **`-c`**: Crear archive
- **`-z`**: Comprimir con gzip
- **`--ignore-failed-read`**: Ignora archivos faltantes
- **`-f`**: Nombre del archivo: `telematicache.tar.gz`

#### Step 3: Upload Bundle to Server
```yaml
uses: appleboy/scp-action@master
with:
  host: ${{ env.DEPLOY_HOST }}
  username: ${{ env.DEPLOY_USER }}
  key: ${{ env.DEPLOY_KEY }}
  port: ${{ env.DEPLOY_PORT }}
  source: telematicache.tar.gz
  target: ${{ env.DEPLOY_PATH }}/telematicache.tar.gz
```

**Action**: `appleboy/scp-action`
- SCP (Secure Copy Protocol) para transferir archivos
- Cifrado SSH automático
- Manejo de clave privada desde secrets

#### Step 4: Deploy on Server
```bash
set -euo pipefail
DEPLOY_ROOT="${{ env.DEPLOY_PATH }}"
ARCHIVE="$DEPLOY_ROOT/telematicache.tar.gz"
REPO_DIR="$DEPLOY_ROOT/repo"
BACKUP_ENV="$DEPLOY_ROOT/.env.backup"

# Backup .env si existe
if [ -f "$REPO_DIR/proyecto_integrado/.env" ]; then
  cp "$REPO_DIR/proyecto_integrado/.env" "$BACKUP_ENV"
fi

# Limpiar y extraer
rm -rf "$REPO_DIR"
mkdir -p "$REPO_DIR"
tar -xzf "$ARCHIVE" -C "$REPO_DIR"
rm -f "$ARCHIVE"

# Restaurar .env
if [ -f "$BACKUP_ENV" ]; then
  mv "$BACKUP_ENV" "$REPO_DIR/proyecto_integrado/.env"
fi

# Deploy con Docker Compose
cd "$REPO_DIR/proyecto_integrado"
docker compose down
docker compose up -d --build telemetry-gateway ids-ml robot-sim croody gateway

# Verificar status
docker compose ps
```

**Flujo de Deploy**:
1. **Backup**: `.env` para preservar configuración
2. **Limpieza**: Remove directorio anterior
3. **Extracción**: Descomprime nuevo código
4. **Restore**: Restaura `.env`
5. **Docker**: Down + up con rebuild
6. **Verification**: `docker compose ps`

## Workflow 3: Terraform CI

### Trigger
```yaml
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]
```

**Branches**: main, dev

### Jobs

#### Job 1: terraform-validate

**Terraform Setup**:
```yaml
- name: Setup Terraform
  uses: hashicorp/setup-terraform@v3
  with:
    terraform_version: 1.7.0
```

**Steps**:

1. **Terraform fmt**:
```bash
terraform fmt -recursive
working-directory: infra/terraform
```
- Formateo automático de archivos .tf
- **`-recursive`**: Incluye subdirectorios

2. **Terraform init**:
```bash
terraform init
working-directory: infra/terraform
```
- Inicializa backend (S3, local)
- Descarga providers
- Configura módulos

3. **Terraform validate**:
```bash
terraform validate
working-directory: infra/terraform
```
- Valida sintaxis
- Verifica configuración
- Carga y valida módulos

#### Job 2: tflint

**Setup**:
```yaml
needs: terraform-validate
runs-on: ubuntu-latest
```

**Steps**:

1. **Install TFLint**:
```yaml
- name: Install TFLint
  uses: terraform-linters/setup-tflint@v4
```

2. **Run TFLint**:
```bash
tflint --init
tflint
working-directory: infra/terraform
```
- **`--init`**: Descarga plugins
- **Linting**: Best practices, validaciones

**TFLint Checks**:
- Variables no utilizadas
- Tipos de datos incorrectos
- Resource naming conventions
- Required fields missing
- Deprecated syntax

## Workflow 4: Full Stack Validate

### Trigger
```yaml
on:
  workflow_dispatch:
  push:
    branches: [main]
```

**Puede ser manual o automático en main**

### Environment Variables
```yaml
env:
  BIND_DOMAIN: ${{ secrets.BIND_DOMAIN || 'example.com' }}
  BASE_URL: ${{ secrets.VALIDATION_BASE_URL || 'http://localhost:8080' }}
```

### Job: validate-full-stack

#### Dependencies Installation
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip docker-compose
pip install pytest httpx
```

#### Run validate_full_stack.sh
```bash
chmod +x scripts/validate_full_stack.sh
./scripts/validate_full_stack.sh
```

**Script de Validación**:
- Levanta stack completo con Docker Compose
- Ejecuta tests end-to-end
- Verifica health de todos los servicios
- Valida conectividad entre servicios
- Genera evidencia

#### Upload Evidences
```yaml
- name: Upload evidences
  uses: actions/upload-artifact@v4
  with:
    name: evidencias-full-stack
    path: extras/evidencias_finales.md
```

**Artifact**:
- Archivo: `evidencias_finales.md`
- Contiene logs, resultados, screenshots

## Workflow 5: Bind Deploy (DNS)

### Trigger
```yaml
on:
  push:
    branches: [main, dev]
```

### Permissions
```yaml
permissions:
  contents: read
  id-token: write
```

### Environment Variables
```yaml
env:
  DOMAIN: ${{ secrets.BIND_DOMAIN != '' && secrets.BIND_DOMAIN || 'example.com' }}
  MASTER_IP: ${{ secrets.BIND_MASTER_PRIVATE_IP != '' && secrets.BIND_MASTER_PRIVATE_IP || '127.0.0.1' }}
  SLAVE_IP: ${{ secrets.BIND_SLAVE_PRIVATE_IP != '' && secrets.BIND_SLAVE_PRIVATE_IP || '127.0.0.1' }}
  TSIG_KEY_NAME: ${{ secrets.BIND_TSIG_KEY_NAME != '' && secrets.BIND_TSIG_KEY_NAME || 'lint-key' }}
  TSIG_KEY_SECRET: ${{ secrets.BIND_TSIG_KEY_SECRET != '' && secrets.BIND_TSIG_KEY_SECRET || 'ZmFrZQ==' }}
  ECR_REGISTRY: ${{ secrets.AWS_ECR_REGISTRY != '' && secrets.AWS_ECR_REGISTRY || 'ecr.local' }}
  AWS_REGION: ${{ secrets.AWS_REGION != '' && secrets.AWS_REGION || 'us-east-1' }}
  MASTER_REPO: ${{ secrets.BIND_MASTER_ECR_REPO != '' && secrets.BIND_MASTER_ECR_REPO || 'bind-master' }}
  SLAVE_REPO: ${{ secrets.BIND_SLAVE_ECR_REPO != '' && secrets.BIND_SLAVE_ECR_REPO || 'bind-slave' }}
  NS1_FQDN: ns1.${{ secrets.BIND_DOMAIN != '' && secrets.BIND_DOMAIN || 'example.com' }}.
  NS2_FQDN: ns2.${{ secrets.BIND_DOMAIN != '' && secrets.BIND_DOMAIN || 'example.com' }}.
```

### Job: build-deploy

#### Step 1: Checkout
```yaml
- name: Checkout repo
  uses: actions/checkout@v4
```

#### Step 2: Validate Secrets
```bash
missing=0
for var in DOMAIN MASTER_IP SLAVE_IP TSIG_KEY_NAME TSIG_KEY_SECRET ECR_REGISTRY MASTER_REPO SLAVE_REPO; do
  if [[ -z "${!var}" ]]; then
    echo "Missing environment variable: $var"
    missing=1
  fi
done
if [[ $missing -eq 1 ]]; then
  echo "Configure the required secrets before running this workflow."
  exit 1
fi
```

**Validación**:
- Verifica que todos los secrets están configurados
- Falla temprano si falta alguno

#### Step 3: Export Computed Variables
```bash
echo "ZONE_FILE=infra/dns/bind-master/zones/${DOMAIN}.db" >> "$GITHUB_ENV"
echo "MASTER_IMAGE=${ECR_REGISTRY}/${MASTER_REPO}:${GITHUB_SHA}" >> "$GITHUB_ENV"
echo "SLAVE_IMAGE=${ECR_REGISTRY}/${SLAVE_REPO}:${GITHUB_SHA}" >> "$GITHUB_ENV"
```

#### Step 4: Ensure Zone File Exists
```bash
if [[ ! -f "${ZONE_FILE}" ]]; then
  echo "Zone file ${ZONE_FILE} not found. Generate it via scripts/dns/setup_bind.sh" >&2
  exit 1
fi
```

#### Step 5: Login to ECR
```yaml
- name: Login to Amazon ECR
  if: env.ECR_REGISTRY != ''
  uses: aws-actions/amazon-ecr-login@v2
  with:
    registry-type: private
    mask-password: true
```

#### Step 6-7: Build Images
```bash
docker build -f infra/dns/Dockerfile -t "$MASTER_IMAGE" infra/dns
docker build -f infra/dns/Dockerfile -t "$SLAVE_IMAGE" infra/dns
```

#### Step 8-9: Validate BIND Configs (Master)
```bash
# named-checkconf
docker run --rm \
  -e DNS_ROLE=master \
  -e DNS_DOMAIN="${DOMAIN}" \
  -e TSIG_KEY_NAME="${TSIG_KEY_NAME}" \
  -e TSIG_KEY_SECRET="${TSIG_KEY_SECRET}" \
  -e NS1_FQDN="${NS1_FQDN}" \
  -e NS2_FQDN="${NS2_FQDN}" \
  -e ALLOW_QUERY="any;" \
  -e ALLOW_TRANSFER="${SLAVE_IP};" \
  -e NOTIFY_TARGETS="${SLAVE_IP};" \
  -e MASTER_IP="${MASTER_IP}" \
  -v "${PWD}/infra/dns/bind-master/zones:/zones" \
  "$MASTER_IMAGE" \
  named-checkconf /etc/bind/named.conf

# named-checkzone
docker run --rm \
  -e DNS_ROLE=master \
  -e DNS_DOMAIN="${DOMAIN}" \
  -e TSIG_KEY_NAME="${TSIG_KEY_NAME}" \
  -e TSIG_KEY_SECRET="${TSIG_KEY_SECRET}" \
  -e NS1_FQDN="${NS1_FQDN}" \
  -e NS2_FQDN="${NS2_FQDN}" \
  -v "${PWD}/infra/dns/bind-master/zones:/zones" \
  "$MASTER_IMAGE" \
  named-checkzone "${DOMAIN}" "/zones/${DOMAIN}.db"
```

#### Step 10: Validate BIND Configs (Slave)
```bash
docker run --rm \
  -e DNS_ROLE=slave \
  -e DNS_DOMAIN="${DOMAIN}" \
  -e TSIG_KEY_NAME="${TSIG_KEY_NAME}" \
  -e TSIG_KEY_SECRET="${TSIG_KEY_SECRET}" \
  -e NS1_FQDN="${NS1_FQDN}" \
  -e NS2_FQDN="${NS2_FQDN}" \
  -e MASTER_IP="${MASTER_IP}" \
  -v "${PWD}/infra/dns/bind-slave/zones:/zones" \
  "$SLAVE_IMAGE" \
  named-checkconf /etc/bind/named.conf
```

#### Step 11-12: Push to ECR
```bash
docker push "$MASTER_IMAGE"
docker push "$SLAVE_IMAGE"
```

#### Step 13: Deploy to Master
```bash
set -euo pipefail
docker pull "$MASTER_IMAGE"
docker stop bind-master || true
docker rm bind-master || true
docker run -d \
  --name bind-master \
  --restart unless-stopped \
  -p 53:53/tcp -p 53:53/udp \
  -v /etc/bind/master/zones:/zones \
  -v /etc/bind/master/keys:/keys \
  -e DNS_ROLE=master \
  -e DNS_DOMAIN=${DOMAIN} \
  -e TSIG_KEY_NAME=${TSIG_KEY_NAME} \
  -e TSIG_KEY_SECRET=${TSIG_KEY_SECRET} \
  -e NS1_FQDN=${NS1_FQDN} \
  -e NS2_FQDN=${NS2_FQDN} \
  -e MASTER_IP=${MASTER_IP} \
  -e ALLOW_QUERY="any;" \
  -e ALLOW_TRANSFER="${SLAVE_IP};" \
  -e NOTIFY_TARGETS="${SLAVE_IP};" \
  "$MASTER_IMAGE"
docker exec bind-master rndc reload || true
```

#### Step 14: Deploy to Slave
```bash
set -euo pipefail
docker pull "$SLAVE_IMAGE"
docker stop bind-slave || true
docker rm bind-slave || true
docker run -d \
  --name bind-slave \
  --restart unless-stopped \
  -p 53:53/tcp -p 53:53/udp \
  -v /etc/bind/slave/zones:/zones \
  -v /etc/bind/slave/keys:/keys \
  -e DNS_ROLE=slave \
  -e DNS_DOMAIN=${DOMAIN} \
  -e TSIG_KEY_NAME=${TSIG_KEY_NAME} \
  -e TSIG_KEY_SECRET=${TSIG_KEY_SECRET} \
  -e NS1_FQDN=${NS1_FQDN} \
  -e NS2_FQDN=${NS2_FQDN} \
  -e MASTER_IP=${MASTER_IP} \
  "$SLAVE_IMAGE"
docker exec bind-slave rndc reload || true
```

**Deploy Features**:
- Pull de imagen desde ECR
- Stop y remove contenedores existentes
- Run con configuración de zona
- Recarga de zona con `rndc reload`
- Ports 53 (TCP/UDP) expuestos

## Workflow 6: DNS Lint

### Trigger
```yaml
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]
```

### Environment Variables
```yaml
env:
  DOMAIN: ${{ secrets.BIND_DOMAIN != '' && secrets.BIND_DOMAIN || 'example.com' }}
  TSIG_KEY_NAME: ${{ secrets.BIND_TSIG_KEY_NAME != '' && secrets.BIND_TSIG_KEY_NAME || 'lint-key' }}
  TSIG_KEY_SECRET: ${{ secrets.BIND_TSIG_KEY_SECRET != '' && secrets.BIND_TSIG_KEY_SECRET || 'ZmFrZQ==' }}
  NS1_FQDN: ns1.${{ secrets.BIND_DOMAIN != '' && secrets.BIND_DOMAIN || 'example.com' }}.
  NS2_FQDN: ns2.${{ secrets.BIND_DOMAIN != '' && secrets.BIND_DOMAIN || 'example.com' }}.
  SLAVE_IP: ${{ secrets.BIND_SLAVE_PRIVATE_IP != '' && secrets.BIND_SLAVE_PRIVATE_IP || '127.0.0.1' }}
```

### Job: dns-lint

#### Step 1: Checkout
```yaml
- uses: actions/checkout@v4
```

#### Step 2: Ensure Zone File Exists
```bash
ZONE_FILE="infra/dns/bind-master/zones/${DOMAIN}.db"
if [[ ! -f "$ZONE_FILE" ]]; then
  echo "Missing $ZONE_FILE. Run scripts/dns/setup_bind.sh and commit the zone file." >&2
  exit 1
fi
```

#### Step 3: Build BIND Image
```bash
docker build -t bind-lint infra/dns
```

#### Step 4: named-checkconf
```bash
docker run --rm \
  -e DNS_ROLE=master \
  -e DNS_DOMAIN="${DOMAIN}" \
  -e TSIG_KEY_NAME="${TSIG_KEY_NAME}" \
  -e TSIG_KEY_SECRET="${TSIG_KEY_SECRET}" \
  -e NS1_FQDN="${NS1_FQDN}" \
  -e NS2_FQDN="${NS2_FQDN}" \
  -e ALLOW_TRANSFER="${SLAVE_IP};" \
  -e ALLOW_QUERY="any;" \
  -v "${PWD}/infra/dns/bind-master/zones:/zones" \
  bind-lint named-checkconf /etc/bind/named.conf
```

#### Step 5: named-checkzone
```bash
docker run --rm \
  -e DNS_ROLE=master \
  -e DNS_DOMAIN="${DOMAIN}" \
  -e TSIG_KEY_NAME="${TSIG_KEY_NAME}" \
  -e TSIG_KEY_SECRET="${TSIG_KEY_SECRET}" \
  -e NS1_FQDN="${NS1_FQDN}" \
  -e NS2_FQDN="${NS2_FQDN}" \
  -v "${PWD}/infra/dns/bind-master/zones:/zones" \
  bind-lint named-checkzone "${DOMAIN}" "/zones/${DOMAIN}.db"
```

#### Step 6: dig @localhost (SOA)
```bash
docker compose -f infra/dns/docker-compose.yml up -d bind-master
sleep 5
dig @127.0.0.1 "${DOMAIN}" SOA
```

**Validación Final**:
- Levanta contenedor DNS real
- Query con `dig` para verificar SOA record
- Confirma que DNS responde

## Workflow 7: Deploy (Self-Hosted)

### Trigger
```yaml
on:
  push:
    branches: [ main ]
```

### Permissions
```yaml
permissions:
  contents: read
```

### Job: deploy

**Runner**: `[self-hosted, linux, deploy]`
- **Self-hosted runner**: Servidor propio de la organización
- **Etiquetas**: `linux`, `deploy`

### Concurrency
```yaml
concurrency:
  group: deploy-production
  cancel-in-progress: false
```

### Environment Variables
```yaml
env:
  CF_API_TOKEN: ${{ secrets.CF_API_TOKEN }}
  CF_ZONE_ID: ${{ secrets.CF_ZONE_ID }}
```

**Cloudflare Secrets**:
- `CF_API_TOKEN`: Token de Cloudflare
- `CF_ZONE_ID`: ID de la zona DNS

### Steps

#### Step 1: Clean Workspace
```bash
sudo rm -rf ./* || true
```
- Limpia workspace por seguridad
- `|| true`: No falla si no hay archivos

#### Step 2: Checkout
```yaml
- name: Checkout
  uses: actions/checkout@v4
```

#### Step 3: Prepare Environment File
```bash
set -euo pipefail
PERSIST_DIR="$HOME/.telematicache"
LEGACY_ENV="$HOME/repo/proyecto_integrado/.env"
mkdir -p "$PERSIST_DIR"

# Seed from legacy path if exists
if [ -f "$LEGACY_ENV" ]; then
  cp "$LEGACY_ENV" "$PERSIST_DIR/.env"
fi

# Ensure .env exists in persistent dir
if [ -f "$PERSIST_DIR/.env" ]; then
  cp "$PERSIST_DIR/.env" "$GITHUB_WORKSPACE/proyecto_integrado/.env"
else
  echo "WARNING: No persistent .env found; using defaults if any" >&2
fi
```

**Persistencia**:
- `PERSIST_DIR`: `$HOME/.telematicache`
- Preserva `.env` entre deployments
- Legacy support: `$HOME/repo/proyecto_integrado/.env`

#### Step 4: Build & Restart Stack
```bash
docker compose down || true
docker compose -f docker-compose.yml \
               -f docker-compose.prod.yml \
               -f docker-compose.acme.yml \
               --env-file .env \
               up -d --build telemetry-gateway ids-ml robot-sim croody gateway
docker compose ps
```

**Multi-file Compose**:
- `docker-compose.yml`: Base
- `docker-compose.prod.yml`: Producción
- `docker-compose.acme.yml`: SSL/ACME
- **`--env-file .env`**: Variables específicas

#### Step 5: Apply Hardening
```bash
sudo scripts/security/hardening_auto.sh
```

#### Step 6: Purge Cloudflare Cache
```bash
curl -fsSL -X POST \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/purge_cache \
  --data '{"purge_everything":true}'
```

#### Step 7: Configure Cloudflare DNS + SSL
```bash
set -euo pipefail

# Discover zone name and public IP
ZONE_NAME=$(curl -fsSL -H "Authorization: Bearer $CF_API_TOKEN" \
  https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID | jq -r '.result.name')
PUBIP=$(curl -fsSL https://checkip.amazonaws.com || \
         curl -fsSL https://api.ipify.org || \
         curl -fsSL http://ifconfig.me || echo '')

# Upsert A record for root
ROOT_REC_ID=$(curl -fsSL -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records?type=A&name=$ZONE_NAME" \
  | jq -r '.result[0].id // empty')

if [ -n "$ROOT_REC_ID" ]; then
  curl -fsSL -X PUT -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/$ROOT_REC_ID" \
    --data "{\"type\":\"A\",\"name\":\"$ZONE_NAME\",\"content\":\"$PUBIP\",\"proxied\":false}"
else
  curl -fsSL -X POST -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
    --data "{\"type\":\"A\",\"name\":\"$ZONE_NAME\",\"content\":\"$PUBIP\",\"proxied\":false}"
fi

# Upsert CNAME for www
WWW_NAME="www.$ZONE_NAME"
WWW_REC_ID=$(curl -fsSL -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records?type=CNAME&name=$WWW_NAME" \
  | jq -r '.result[0].id // empty')

if [ -n "$WWW_REC_ID" ]; then
  curl -fsSL -X PUT -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/$WWW_REC_ID" \
    --data "{\"type\":\"CNAME\",\"name\":\"$WWW_NAME\",\"content\":\"$ZONE_NAME\",\"proxied\":false}"
else
  curl -fsSL -X POST -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
    --data "{\"type\":\"CNAME\",\"name\":\"$WWW_NAME\",\"content\":\"$ZONE_NAME\",\"proxied\":false}"
fi

# SSL Strict
curl -fsSL -X PATCH -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/settings/ssl" \
  --data '{"value":"full"}'

# Bot Fight Mode ON
curl -fsSL -X PATCH -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/settings/bot_fight_mode" \
  --data '{"value":"on"}'
```

#### Step 8: Promote Cloudflare Proxy
```bash
set -euo pipefail

# Check zone active
ZONE=$(curl -fsSL -H "Authorization: Bearer $CF_API_TOKEN" \
  https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID | \
  jq -r '.result.status // empty')
if [ "$ZONE" != "active" ]; then
  echo "CF zone not active yet ($ZONE). Skipping proxy+strict promotion."
  exit 0
fi

# Check active certificates
CERT_ACTIVE=$(curl -fsSL -H "Authorization: Bearer $CF_API_TOKEN" \
  https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/ssl/certificate_packs | \
  jq -r '[.result[] | select(.status=="active")] | length')
if [ $CERT_ACTIVE -eq 0 ]; then
  echo "No active edge certificate yet. Skipping proxy+strict promotion."
  exit 0
fi

# Promote to proxied
ZONE_NAME=$(curl -fsSL -H "Authorization: Bearer $CF_API_TOKEN" \
  https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID | \
  jq -r '.result.name')

ROOT_ID=$(curl -fsSL -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records?type=A&name=$ZONE_NAME" \
  | jq -r '.result[0].id // empty')

[ -n "$ROOT_ID" ] && \
  curl -fsSL -X PATCH -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/$ROOT_ID" \
    --data '{"proxied":true}' || true

WWW_NAME="www.$ZONE_NAME"
WWW_ID=$(curl -fsSL -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records?type=CNAME&name=$WWW_NAME" \
  | jq -r '.result[0].id // empty')

[ -n "$WWW_ID" ] && \
  curl -fsSL -X PATCH -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/$WWW_ID" \
    --data '{"proxied":true}' || true

# SSL Strict
curl -fsSL -X PATCH -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/settings/ssl" \
  --data '{"value":"strict"}'
```

**Auto-configuración Cloudflare**:
1. Descubre IP pública del servidor
2. Upsert A record (root)
3. Upsert CNAME (www)
4. SSL mode: Full → Strict
5. Bot Fight Mode: ON
6. Promoción a proxied (orange cloud)
7. Validación de zona activa y certificados

## GitHub Secrets Requeridos

### Para Deploy (SSH)
```
DEPLOY_HOST=server.example.com
DEPLOY_USER=deploy
DEPLOY_KEY=<ssh-private-key-base64>
DEPLOY_PATH=/opt/telematicache
DEPLOY_PORT=22
```

### Para Bind Deploy
```
BIND_DOMAIN=example.com
BIND_MASTER_PRIVATE_IP=10.0.0.10
BIND_SLAVE_PRIVATE_IP=10.0.0.11
BIND_TSIG_KEY_NAME=tsig-key
BIND_TSIG_KEY_SECRET=<base64-encoded-secret>
BIND_MASTER_HOST=10.0.0.10
BIND_SLAVE_HOST=10.0.0.11
BIND_SSH_USER=admin
BIND_SSH_KEY=<ssh-private-key-base64>
BIND_SSH_PORT=22
AWS_ACCESS_KEY_ID=<key>
AWS_SECRET_ACCESS_KEY=<secret>
AWS_REGION=us-east-1
AWS_ECR_REGISTRY=<account>.dkr.ecr.<region>.amazonaws.com
BIND_MASTER_ECR_REPO=bind-master
BIND_SLAVE_ECR_REPO=bind-slave
```

### Para Full Stack Validation
```
BIND_DOMAIN=example.com
VALIDATION_BASE_URL=http://localhost:8080
```

### Para Self-Hosted Deploy
```
CF_API_TOKEN=<cloudflare-api-token>
CF_ZONE_ID=<zone-id>
```

## Configuración de Secrets

### En GitHub Repository
```bash
# Via GitHub CLI
gh secret set DEPLOY_HOST --body "server.example.com"
gh secret set DEPLOY_KEY --body-file ./deploy_key_base64.txt

# Via Web UI
# Settings > Secrets and variables > Actions > New repository secret
```

### GitHub Enterprise
```bash
# Organization level secrets
gh secret set SECRET_NAME --org myorg --visibility private --body "value"
```

## Monitoreo de Workflows

### GitHub Actions Tab
```
https://github.com/<owner>/<repo>/actions
```

### Workflow Runs
- **Status**: success, failure, cancelled
- **Timing**: Duración de cada job
- **Logs**: Logs detallados de cada step
- **Artifacts**: Archivos generados

### Notifications
```yaml
# Webhook para Slack
- name: Notify Slack
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    channel: '#deployments'
```

## Mejores Prácticas

### ✅ Hacer
```yaml
# Usar versiones específicas de actions
- uses: actions/checkout@v4  # No @v4.0.0

# Validar secrets antes de usar
if [[ -z "${SECRET}" ]]; then
  exit 1
fi

# Concurrency groups para evitar overlaps
concurrency:
  group: deploy-production
  cancel-in-progress: true

# continue-on-error para non-critical
- name: Optional scan
  continue-on-error: true

# Cache dependencies
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

# Self-hosted runners con etiquetas
runs-on: [self-hosted, linux, production]
```

### ❌ Evitar
```yaml
# No usar @main o @master (puede cambiar)
- uses: actions/checkout@main  # ❌

# No hardcodear secrets
env:
  API_KEY: "12345"  # ❌

# No ignorar errores
- name: Deploy
  run: docker push image  # ❌ Sin set -euo pipefail

# No usar secrets en logs
- name: Show secret
  run: echo ${{ secrets.API_KEY }}  # ❌ Visible en logs
```

## Troubleshooting

### Workflow falla con "No such file or directory"
```yaml
# Solución: Usar working-directory
- name: Run script
  working-directory: proyecto_integrado
  run: ./scripts/deploy.sh
```

### SSH key not valid
```bash
# Verificar formato (debe ser base64)
base64 -w 0 id_rsa > key_base64.txt

# Test manual
ssh -i <(echo $DEPLOY_KEY | base64 -d) user@host
```

### Docker build fails
```yaml
# Verificar path en context
build:
  context: ./proyecto_integrado  # Path correcto
  dockerfile: Dockerfile

# Verificar .dockerignore
echo "node_modules" >> .dockerignore
echo ".git" >> .dockerignore
```

### Workflow no se dispara
```yaml
# Verificar trigger syntax
on:
  push:
    branches: [ main ]  # Branch existe

# Para manual trigger
on:
  workflow_dispatch:  # Habilita "Run workflow"
```

## Artifacts y Caching

### Upload Artifact
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: test-results.xml
    retention-days: 30
```

### Download Artifact
```yaml
- uses: actions/download-artifact@v4
  with:
    name: test-results
    path: ./test-results/
```

### Cache
```yaml
- uses: actions/cache@v3
  with:
    path: |
      ~/.cache/pip
      ~/.cache/pre-commit
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

## Referencias

### Archivos Relacionados
- `/.github/workflows/ci.yml`
- `/.github/workflows/deploy.yml`
- `/.github/workflows/terraform-ci.yml`
- `/.github/workflows/full-stack-validate.yml`
- `/.github/workflows/bind-deploy.yml`
- `/.github/workflows/dns-lint.yml`
- `/.github/workflows/deploy-selfhosted.yml`

### Documentación Externa
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

## Ver También
- [Docker Compose](../docker-compose.md)
- [Infraestructura Terraform](../infraestructura/terraform.md)
- [Testing - APIs](../../testing/testing-apis.md)
