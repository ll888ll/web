# Análisis de Prácticas de Deployment: AWS + Cloudflare

## Resumen Ejecutivo

El repositorio **telematicache** implementa un sistema de deployment multi-capa que despliega la aplicación **Croody** en infraestructura AWS y la expone a usuarios finales a través de Cloudflare. El sistema incluye:

- **7 workflows de GitHub Actions** para CI/CD
- **Infraestructura como Código** con Terraform (3 módulos)
- **Sistema DNS autoritativo** con BIND9 (master/slave)
- **Contenedorización** con Docker y Docker Compose
- **Seguridad** con hardening automatizado y ModSecurity

---

## 1. Arquitectura del Sistema de Deployment

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              FLUJO DE DEPLOYMENT                             │
└──────────────────────────────────────────────────────────────────────────────┘

  GitHub Push (main)
        │
        ▼
  ┌─────────────────┐
  │  CI Validation  │──► Lint, Tests, Security Scans (Bandit, Gitleaks)
  │   (ci.yml)      │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐     ┌─────────────────┐
  │  Terraform CI   │     │    DNS Lint     │
  │ (terraform-ci)  │     │  (dns-lint.yml) │
  └────────┬────────┘     └────────┬────────┘
           │                       │
           ▼                       ▼
  ┌─────────────────────────────────────────┐
  │          Parallel Deployment            │
  ├─────────────────────────────────────────┤
  │  bind-deploy.yml  │  deploy-selfhosted  │
  │  (DNS BIND9)      │  (App Stack)        │
  └─────────────────────────────────────────┘
           │                       │
           ▼                       ▼
  ┌─────────────────┐     ┌─────────────────┐
  │  AWS ECR        │     │  AWS EC2        │
  │  (Images)       │     │  (Self-hosted)  │
  └─────────────────┘     └─────────────────┘
           │                       │
           ▼                       ▼
  ┌─────────────────────────────────────────┐
  │         CLOUDFLARE INTEGRATION          │
  │  - DNS Records (A, CNAME)               │
  │  - Cache Purge                          │
  │  - SSL Strict Mode                      │
  │  - Bot Fight Mode                       │
  └─────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────┐
  │   Usuarios      │
  │   (Internet)    │
  └─────────────────┘
```

---

## 2. Análisis de Prácticas por Categoría

### 2.1 CI/CD (GitHub Actions)

| Workflow | Trigger | Propósito | Buenas Prácticas |
|----------|---------|-----------|------------------|
| `ci.yml` | push/PR a main | Linting, typecheck, tests, security | ✅ Múltiples herramientas de seguridad |
| `deploy.yml` | manual | Deploy SSH remoto | ⚠️ Solo workflow_dispatch |
| `deploy-selfhosted.yml` | push a main | Deploy en runner self-hosted | ✅ Concurrencia controlada |
| `bind-deploy.yml` | push main/dev | DNS BIND9 a ECR + SSH | ✅ Validación de secretos |
| `dns-lint.yml` | push/PR | Validación sintaxis DNS | ✅ Early failure |
| `terraform-ci.yml` | push/PR | Validación Terraform | ✅ tflint integrado |
| `full-stack-validate.yml` | push main + manual | Healthchecks del stack | ✅ Genera evidencias |

**Prácticas Identificadas:**

1. **Concurrency control**: `deploy-selfhosted.yml:13-14`
   ```yaml
   concurrency:
     group: deploy-production
     cancel-in-progress: false
   ```
   - Previene deployments simultáneos conflictivos

2. **Validación de secretos**: `bind-deploy.yml:34-46`
   - Verifica variables requeridas antes de ejecutar
   - Falla temprano si faltan configuraciones

3. **Security scans integrados**: `ci.yml:49-54`
   - Bandit para análisis estático Python
   - pip-audit para vulnerabilidades en dependencias
   - Gitleaks para detectar secretos expuestos

### 2.2 Integración AWS

#### Servicios Utilizados:

| Servicio | Uso | Archivo de Configuración |
|----------|-----|--------------------------|
| **EC2** | Hosts de aplicación y DNS | `infra/terraform/modules/bastion/main.tf` |
| **VPC** | Red aislada con subnets públicas/privadas | `infra/terraform/modules/network/main.tf` |
| **ECR** | Registro de imágenes Docker | `bind-deploy.yml:63-72` |
| **NAT Gateway** | Salida a internet desde subnets privadas | `modules/network/main.tf` |

#### Arquitectura de Red (Terraform):

```
VPC: 10.50.0.0/16
├── Public Subnets (ALB/NAT/Bastion)
│   ├── 10.50.10.0/24 (us-east-1a)
│   └── 10.50.20.0/24 (us-east-1b)
└── Private Subnets (App/DB)
    ├── 10.50.110.0/24 (us-east-1a)
    └── 10.50.210.0/24 (us-east-1b)
```

#### Security Groups Definidos:

| SG | Propósito | Puertos |
|----|-----------|---------|
| `alb-sg` | Load Balancer público | 80, 443 inbound |
| `bastion-sg` | Acceso SSH administrativo | 22 inbound |
| `app-sg` | Aplicación (solo desde ALB/bastion) | 80 desde ALB, 22 desde bastion |
| `db-sg` | Base de datos PostgreSQL | 5432 solo desde app-sg |

**Buenas Prácticas Observadas:**
- ✅ Segregación de red (públicas/privadas)
- ✅ Principio de mínimo privilegio en Security Groups
- ✅ Bastion host para acceso SSH seguro
- ⚠️ `allowed_ssh_cidrs` default es `0.0.0.0/0` (debería restringirse)

### 2.3 Integración Cloudflare

#### Operaciones Automatizadas (`deploy-selfhosted.yml:55-152`):

1. **Purge de Cache Completo**
   ```bash
   curl -X POST https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/purge_cache \
     --data '{"purge_everything":true}'
   ```

2. **Configuración DNS Automática**
   - Upsert de registro A para dominio raíz
   - Upsert de CNAME para www subdomain
   - Detección automática de IP pública del host

3. **Configuración de Seguridad SSL**
   - Modo SSL: Full → Strict (cuando certificado activo)
   - Bot Fight Mode habilitado

4. **Promoción a Proxy (Orange Cloud)**
   - Solo cuando zona está activa Y hay certificado edge

**Flujo de Seguridad SSL:**
```
1. Deploy inicial → SSL "full" (permite self-signed)
2. Certbot obtiene LE cert
3. Próximo deploy → Verifica cert activo
4. Si activo → Promociona a "strict" + proxied=true
```

### 2.4 Contenedorización y Orchestration

#### Stack de Servicios (Docker Compose):

```
proyecto_integrado/
├── docker-compose.yml        # Dev (puertos 8080/8443)
├── docker-compose.prod.yml   # Prod (puertos 80/443, Postgres)
└── docker-compose.acme.yml   # Volúmenes Let's Encrypt
```

| Servicio | Puerto | Función |
|----------|--------|---------|
| `gateway` (Nginx) | 80/443 | Reverse proxy, SSL termination |
| `croody` (Django) | 8000 | Aplicación web principal |
| `telemetry-gateway` | 9000 | API FastAPI para telemetría |
| `ids-ml` | 9100 | API FastAPI para IDS con ML |
| `robot-sim` | - | Simulador de robots IoT |
| `db` (PostgreSQL) | 5432 | Base de datos (solo prod) |

#### Configuración de Producción (`docker-compose.prod.yml`):

**Buenas Prácticas:**
- ✅ Healthchecks en todos los servicios
- ✅ Límites de recursos (`mem_limit`, `cpus`)
- ✅ `restart: unless-stopped`
- ✅ Dependencias con `condition: service_healthy`
- ⚠️ Credenciales de BD hardcoded (croody/croody)

### 2.5 Configuración de Gateway (Nginx)

#### Producción (`gateway/nginx.prod.conf`):

**Headers de Seguridad:**
```nginx
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options SAMEORIGIN;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self' 'unsafe-inline' data: https:; ...";
```

**Rate Limiting:**
```nginx
limit_req_zone $binary_remote_addr zone=api_zone:20m rate=150r/s;
# Aplicado a /api/telemetry/ y /api/ids/
```

**Buenas Prácticas:**
- ✅ Redirect HTTP → HTTPS automático
- ✅ TLS 1.2/1.3 con ciphers seguros
- ✅ Logging en formato JSON estructurado
- ✅ Timeouts configurados para prevenir slow attacks
- ✅ ACME challenge para renovación automática de certs

### 2.6 Sistema DNS Autoritativo (BIND9)

#### Arquitectura:

```
┌─────────────────┐     AXFR/TSIG      ┌─────────────────┐
│  BIND Master    │─────────────────────│  BIND Slave     │
│  ns1.croody.app │                     │  ns2.croody.app │
│  172.31.42.77   │                     │  172.31.71.231  │
└─────────────────┘                     └─────────────────┘
```

**Seguridad DNS:**
- ✅ TSIG para autenticación de transferencias de zona
- ✅ Recursión deshabilitada (`recursion no;`)
- ✅ DNSSEC habilitado
- ✅ Rate limiting configurado
- ✅ Contenedorizado con entrypoint dinámico

### 2.7 Scripts de Hardening

#### `scripts/security/hardening_auto.sh`:

**Medidas Implementadas:**
1. Actualización de paquetes del sistema
2. Headers de seguridad Apache (ServerTokens Prod, etc.)
3. UFW firewall (80/443 allow, 22 deny)
4. Rate limiting con iptables (25/min en puerto 80)
5. ModSecurity con OWASP CRS
6. Certificados Let's Encrypt automáticos
7. Monitoreo de seguridad (systemd service)
8. Backups nocturnos (cron)

---

## 3. Evaluación de Prácticas

### 3.1 Fortalezas

| Área | Práctica | Impacto |
|------|----------|---------|
| **CI/CD** | Security scans integrados (Bandit, Gitleaks, pip-audit) | Alto |
| **CI/CD** | Concurrency control en deployments | Alto |
| **Infra** | IaC con Terraform modular | Alto |
| **Infra** | Network segregation (public/private subnets) | Alto |
| **DNS** | TSIG authentication para zone transfers | Alto |
| **SSL** | Promoción automática a SSL Strict | Alto |
| **Hardening** | ModSecurity + OWASP CRS | Alto |
| **Monitoring** | Healthchecks en todos los servicios | Medio |
| **Logging** | JSON structured logs en Nginx | Medio |

### 3.2 Áreas de Mejora

| Área | Issue | Severidad | Recomendación |
|------|-------|-----------|---------------|
| **Secrets** | Credenciales BD hardcoded en docker-compose.prod.yml | Alta | Usar secrets externos o vault |
| **SSH** | `allowed_ssh_cidrs` default `0.0.0.0/0` | Alta | Restringir a IPs conocidas |
| **DNS** | Sin monitoreo de propagación | Media | Agregar checks post-deploy |
| **Backups** | Solo configurado en hardening manual | Media | Automatizar en CI/CD |
| **Rollback** | Sin estrategia de rollback documentada | Media | Implementar blue-green o canary |
| **Terraform** | Sin remote state backend | Media | Usar S3 + DynamoDB |
| **CF Proxy** | Registros DNS con `proxied:false` inicial | Baja | Documentar progresión |

### 3.3 Matriz de Seguridad

```
┌────────────────────────────────────────────────────────────────────┐
│                    CAPAS DE SEGURIDAD                              │
├────────────────────────────────────────────────────────────────────┤
│  CAPA 1: Cloudflare                                                │
│  ├── Bot Fight Mode                                                │
│  ├── SSL Strict                                                    │
│  ├── DDoS Protection (implícito)                                   │
│  └── WAF (si habilitado)                                           │
├────────────────────────────────────────────────────────────────────┤
│  CAPA 2: AWS Security Groups                                       │
│  ├── ALB-SG: solo 80/443                                           │
│  ├── App-SG: solo desde ALB/bastion                                │
│  └── DB-SG: solo desde App-SG                                      │
├────────────────────────────────────────────────────────────────────┤
│  CAPA 3: Host Hardening                                            │
│  ├── UFW firewall                                                  │
│  ├── iptables rate limiting                                        │
│  └── ModSecurity + OWASP CRS                                       │
├────────────────────────────────────────────────────────────────────┤
│  CAPA 4: Application (Nginx)                                       │
│  ├── Security headers (HSTS, CSP, X-Frame, etc.)                   │
│  ├── Rate limiting (150r/s API)                                    │
│  └── TLS 1.2+ only                                                 │
├────────────────────────────────────────────────────────────────────┤
│  CAPA 5: Container Isolation                                       │
│  ├── Resource limits (mem_limit, cpus)                             │
│  ├── Network segregation (internal Docker network)                 │
│  └── Healthchecks for recovery                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## 4. Flujo de Deployment Detallado

### 4.1 Push a Main Branch

```bash
# 1. Developer pushes
git push origin main

# 2. GitHub Actions triggered (parallel)
├── ci.yml          → Lint, test, security
├── dns-lint.yml    → Validate BIND configs
├── terraform-ci.yml → Validate infra
└── deploy-selfhosted.yml → Deploy to EC2

# 3. deploy-selfhosted.yml sequence:
#    a) Clean workspace
#    b) Checkout code
#    c) Prepare .env (from persistent storage)
#    d) docker compose up -d --build
#    e) Apply hardening script
#    f) Purge Cloudflare cache
#    g) Configure DNS + SSL
#    h) Promote to proxied (if cert ready)
```

### 4.2 Deploy DNS (bind-deploy.yml)

```bash
# 1. Validate required secrets
# 2. Build Docker images (master/slave)
# 3. Validate BIND configs inside containers
# 4. Push images to ECR
# 5. SSH deploy to master host
# 6. SSH deploy to slave host
# 7. Reload zones via rndc
```

---

## 5. Inventario de Secretos Requeridos

| Categoría | Secret | Descripción |
|-----------|--------|-------------|
| **AWS** | `AWS_ACCESS_KEY_ID` | IAM credentials |
| **AWS** | `AWS_SECRET_ACCESS_KEY` | IAM credentials |
| **AWS** | `AWS_REGION` | us-east-2 |
| **AWS** | `AWS_ECR_REGISTRY` | ECR registry URL |
| **Cloudflare** | `CF_API_TOKEN` | Token con permisos DNS Write |
| **Cloudflare** | `CF_ZONE_ID` | Zone ID de croody.app |
| **DNS** | `BIND_DOMAIN` | croody.app |
| **DNS** | `BIND_MASTER_PRIVATE_IP` | IP privada master |
| **DNS** | `BIND_SLAVE_PRIVATE_IP` | IP privada slave |
| **DNS** | `BIND_MASTER_HOST` | IP pública para SSH |
| **DNS** | `BIND_SSH_USER` / `BIND_SSH_KEY` | Credenciales SSH |
| **DNS** | `BIND_TSIG_KEY_NAME` / `SECRET` | TSIG authentication |
| **Deploy** | `DEPLOY_HOST` / `USER` / `KEY` | SSH deploy legacy |
| **Validation** | `VALIDATION_BASE_URL` | URL para healthchecks |

---

## 6. Conclusiones

### Resumen de Madurez

| Aspecto | Nivel | Justificación |
|---------|-------|---------------|
| **CI/CD** | ⭐⭐⭐⭐ | Pipelines completos con security scanning |
| **Infraestructura** | ⭐⭐⭐ | Terraform modular, falta remote state |
| **Seguridad** | ⭐⭐⭐⭐ | Múltiples capas, hardening automatizado |
| **Monitoreo** | ⭐⭐⭐ | Healthchecks presentes, falta observabilidad |
| **Documentación** | ⭐⭐⭐ | Secrets documentados, falta runbook operacional |
| **Rollback** | ⭐⭐ | No hay estrategia documentada |

### Recomendaciones Prioritarias

1. **Crítico**: Externalizar credenciales de BD (usar AWS Secrets Manager o similar)
2. **Alto**: Restringir `allowed_ssh_cidrs` a IPs de administradores
3. **Medio**: Implementar remote state para Terraform (S3 + DynamoDB)
4. **Medio**: Documentar procedimiento de rollback
5. **Bajo**: Agregar dashboards de observabilidad (CloudWatch/Grafana)

---

*Documento generado automáticamente - Fecha: 2025-12-03*
