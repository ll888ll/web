# Security Audit - OWASP Top 10 Compliance

Ejecuta una auditoría de seguridad completa del proyecto Croody Web siguiendo OWASP Top 10 2021.

## Context

Este comando invoca al `security-auditor` agent para revisar la configuración de seguridad del proyecto, identificar vulnerabilidades y generar recomendaciones de hardening.

## Requirements

$ARGUMENTS

## Instructions

### Phase 1: Information Gathering

Recopilar información de configuración actual:

```bash
# Archivos a revisar
proyecto_integrado/Croody/croody/settings.py
proyecto_integrado/Croody/croody/settings/production.py
proyecto_integrado/gateway/nginx.conf
proyecto_integrado/gateway/nginx.prod.conf
docker-compose.yml
docker-compose.prod.yml
scripts/security/*.sh
```

### Phase 2: OWASP Top 10 Checklist

#### A01:2021 - Broken Access Control

```markdown
## Checklist
- [ ] Django `@login_required` en vistas protegidas
- [ ] `LoginRequiredMixin` en CBVs
- [ ] Verificación de ownership en operaciones de usuario
- [ ] Rate limiting configurado en nginx
- [ ] CORS configurado correctamente
- [ ] Session timeout configurado

## Verificación
```python
# Buscar vistas sin protección
grep -r "def get\|def post" --include="views.py" | grep -v "@login_required"

# Verificar mixins en CBVs
grep -r "class.*View" --include="views.py" | grep -v "LoginRequiredMixin"
```
```

#### A02:2021 - Cryptographic Failures

```markdown
## Checklist
- [ ] HTTPS forzado (SECURE_SSL_REDIRECT)
- [ ] HSTS habilitado (SECURE_HSTS_SECONDS)
- [ ] Cookies seguras (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- [ ] Passwords hasheados con algoritmo fuerte
- [ ] No secrets en código

## Verificación
```python
# En settings.py
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```
```

#### A03:2021 - Injection

```markdown
## Checklist
- [ ] Usar ORM de Django (no raw SQL)
- [ ] Parametrizar queries cuando sea necesario
- [ ] Validar/sanitizar input de usuario
- [ ] Escapar output en templates

## Verificación
```bash
# Buscar raw SQL
grep -r "raw\|execute\|cursor" --include="*.py" | grep -v "test"

# Buscar f-strings en queries (peligroso)
grep -r "f\".*SELECT\|f\".*INSERT\|f\".*UPDATE" --include="*.py"
```
```

#### A04:2021 - Insecure Design

```markdown
## Checklist
- [ ] Validación de negocio en modelos (Fat Model)
- [ ] Límites de rate en APIs
- [ ] Timeouts configurados
- [ ] Captcha en formularios públicos
```

#### A05:2021 - Security Misconfiguration

```markdown
## Checklist
- [ ] DEBUG = False en producción
- [ ] ALLOWED_HOSTS configurado
- [ ] SECRET_KEY no hardcodeado
- [ ] Admin URL no default (/admin/)
- [ ] Headers de seguridad en nginx

## Verificación nginx
```nginx
# Headers requeridos
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'..." always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```
```

#### A06:2021 - Vulnerable Components

```markdown
## Checklist
- [ ] Dependencias actualizadas
- [ ] No vulnerabilidades conocidas
- [ ] Docker images actualizadas

## Verificación
```bash
# Check Python dependencies
pip-audit
safety check

# Check npm (si aplica)
npm audit

# Docker images
docker scan proyecto_integrado-web
```
```

#### A07:2021 - Authentication Failures

```markdown
## Checklist
- [ ] Password validators configurados
- [ ] Account lockout después de intentos fallidos
- [ ] MFA disponible (si aplica)
- [ ] Session management seguro

## Django Settings
```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```
```

#### A08:2021 - Software and Data Integrity

```markdown
## Checklist
- [ ] Integridad de assets estáticos
- [ ] CI/CD seguro
- [ ] Subresource Integrity para CDN

## Verificación
```html
<!-- SRI en scripts externos -->
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-..."
        crossorigin="anonymous"></script>
```
```

#### A09:2021 - Security Logging

```markdown
## Checklist
- [ ] Logging de autenticación (login/logout/failed)
- [ ] Logging de acciones admin
- [ ] Logging de errores 4xx/5xx
- [ ] No loggear datos sensibles

## Django Logging
```python
LOGGING = {
    'handlers': {
        'security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/security.log',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security'],
            'level': 'INFO',
        },
    },
}
```
```

#### A10:2021 - Server-Side Request Forgery (SSRF)

```markdown
## Checklist
- [ ] Validar URLs de input de usuario
- [ ] Whitelist de dominios permitidos
- [ ] No permitir localhost/internal IPs

## Verificación
```bash
# Buscar requests con URLs de usuario
grep -r "requests.get\|requests.post\|urllib" --include="*.py"
```
```

### Phase 3: Infrastructure Security

#### Nginx Hardening

```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;

# Hide version
server_tokens off;

# SSL Configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
```

#### Docker Security

```yaml
# docker-compose security
services:
  web:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    user: "1000:1000"
```

#### Firewall (UFW)

```bash
# Verificar reglas
sudo ufw status verbose

# Reglas esperadas
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
```

### Phase 4: Generate Report

```markdown
# Security Audit Report - Croody Web

**Fecha**: [fecha]
**Auditor**: security-auditor agent
**Scope**: Full stack (Django, FastAPI, Nginx, Docker)

## Executive Summary

| Categoría | Critical | High | Medium | Low |
|-----------|----------|------|--------|-----|
| OWASP A01 | X | X | X | X |
| OWASP A02 | X | X | X | X |
| ... | | | | |

## Critical Findings

### [ID] [Título]
- **Severity**: Critical
- **Location**: [archivo:línea]
- **Description**: [descripción]
- **Remediation**: [pasos para corregir]
- **Reference**: [link OWASP/CWE]

## Recommendations

### Immediate Actions (24-48h)
1. [acción]

### Short-term (1 semana)
1. [acción]

### Long-term (1 mes)
1. [acción]

## Compliance Status

| Control | Status | Notes |
|---------|--------|-------|
| HTTPS | ✅ | Configured |
| HSTS | ⚠️ | Missing preload |
| CSP | ❌ | Not configured |

## Next Steps
1. Address critical findings
2. Schedule penetration test
3. Implement monitoring
```

## Output Format

1. **Executive Summary**: Resumen para stakeholders
2. **Detailed Findings**: Cada vulnerabilidad con remediación
3. **Compliance Matrix**: Estado de cada control
4. **Remediation Plan**: Acciones priorizadas
5. **Scripts**: Comandos de verificación automatizados

## Commands for Verification

```bash
# Test SSL configuration
nmap --script ssl-enum-ciphers -p 443 croody.app

# Test headers
curl -I https://croody.app

# Django check
python manage.py check --deploy

# Dependency audit
pip-audit
```

---

Argumento recibido: $ARGUMENTS

Si no hay argumento, ejecuta auditoría completa. Si hay argumento específico (ej: "headers", "auth", "injection"), enfócate en esa área.
