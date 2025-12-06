# Deploy Check - Pre-deployment Verification

Verifica que el proyecto está listo para deploy a producción. Ejecuta checks de Django, Docker, SSL, y configuración de infraestructura.

## Context

Este comando invoca al `sysadmin-ops` agent para verificar el estado de deployment del proyecto Croody Web, identificando problemas antes de hacer deploy a AWS.

## Requirements

$ARGUMENTS

## Instructions

### Phase 1: Django Deploy Check

```bash
# Verificación completa de Django
cd proyecto_integrado/Croody
python manage.py check --deploy
```

**Checks que Django verifica:**
- SECURE_HSTS_SECONDS
- SECURE_CONTENT_TYPE_NOSNIFF
- SECURE_BROWSER_XSS_FILTER
- SECURE_SSL_REDIRECT
- SESSION_COOKIE_SECURE
- CSRF_COOKIE_SECURE
- DEBUG setting
- ALLOWED_HOSTS
- SECRET_KEY no es default

### Phase 2: Docker Build Verification

```bash
# Verificar que Docker builds funcionan
docker compose -f docker-compose.prod.yml config --quiet && echo "✅ Config válida"

# Build sin cache para verificar
docker compose -f docker-compose.prod.yml build --no-cache

# Verificar imágenes
docker images | grep croody
```

### Phase 3: Static Files Check

```bash
# Verificar collectstatic
cd proyecto_integrado/Croody
python manage.py collectstatic --dry-run --noinput

# Verificar que staticfiles existe y tiene contenido
ls -la staticfiles/
du -sh staticfiles/

# Verificar manifest
cat staticfiles/staticfiles.json | head -20
```

### Phase 4: Database Migrations

```bash
# Verificar migrations pendientes
python manage.py showmigrations | grep "\[ \]"

# Si hay pendientes, listarlas
python manage.py migrate --plan

# Verificar integridad
python manage.py check --database default
```

### Phase 5: SSL/TLS Verification

```bash
# Verificar certificados locales
ls -la proyecto_integrado/Croody/ssl/
ls -la proyecto_integrado/gateway/ssl/

# Verificar fechas de expiración
openssl x509 -in ssl/dev.crt -noout -dates

# Test SSL en producción (si está up)
# nmap --script ssl-enum-ciphers -p 443 croody.app
```

### Phase 6: Environment Variables

```markdown
## Variables Requeridas en Producción

### Django
- [ ] SECRET_KEY (no default)
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS
- [ ] DATABASE_URL

### PostgreSQL
- [ ] POSTGRES_USER
- [ ] POSTGRES_PASSWORD
- [ ] POSTGRES_DB

### AWS (si aplica)
- [ ] AWS_ACCESS_KEY_ID
- [ ] AWS_SECRET_ACCESS_KEY
- [ ] AWS_REGION

### Email
- [ ] EMAIL_HOST
- [ ] EMAIL_HOST_USER
- [ ] EMAIL_HOST_PASSWORD
```

### Phase 7: Nginx Configuration

```bash
# Verificar sintaxis de nginx
docker compose exec gateway nginx -t

# O localmente
nginx -t -c gateway/nginx.prod.conf
```

**Verificar en nginx.prod.conf:**
- [ ] SSL configurado correctamente
- [ ] Headers de seguridad presentes
- [ ] Rate limiting configurado
- [ ] Gzip habilitado
- [ ] Proxy pass correcto

### Phase 8: Service Health Checks

```bash
# Verificar que servicios responden
# Django
curl -f http://localhost:8000/health/ || echo "Django not responding"

# Telemetry API
curl -f http://localhost:8001/health || echo "Telemetry not responding"

# IDS API
curl -f http://localhost:8002/health || echo "IDS not responding"

# Gateway
curl -f http://localhost/health || echo "Gateway not responding"
```

### Phase 9: Resource Check

```bash
# Verificar recursos disponibles
docker system df

# Espacio en disco
df -h

# Memoria
free -h

# Verificar límites de Docker
docker compose -f docker-compose.prod.yml config | grep -A5 "deploy:"
```

### Phase 10: Generate Report

```markdown
# Deploy Readiness Report - Croody Web

**Fecha**: [fecha]
**Environment**: Production
**Target**: AWS ECS

## Summary

| Check | Status | Details |
|-------|--------|---------|
| Django deploy check | ✅/❌ | [message] |
| Docker build | ✅/❌ | [message] |
| Static files | ✅/❌ | [count] files |
| Migrations | ✅/❌ | [pending count] |
| SSL/TLS | ✅/❌ | Expires [date] |
| Env vars | ✅/❌ | [missing count] |
| Nginx config | ✅/❌ | [message] |
| Services health | ✅/❌ | [up/down count] |

## Critical Issues (Block Deploy)

1. [Issue description]
   - **Fix**: [solution]

## Warnings (Should Address)

1. [Warning description]

## Pre-Deploy Checklist

- [ ] All tests passing
- [ ] Coverage > 80%
- [ ] No security warnings
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Backup plan ready

## Deploy Commands

```bash
# 1. Build images
docker compose -f docker-compose.prod.yml build

# 2. Push to registry
docker compose -f docker-compose.prod.yml push

# 3. Deploy (AWS ECS)
aws ecs update-service --cluster croody --service web --force-new-deployment

# 4. Monitor
aws ecs describe-services --cluster croody --services web
```

## Rollback Plan

```bash
# Si algo falla
aws ecs update-service --cluster croody --service web --task-definition croody-web:[previous-version]
```

## Post-Deploy Verification

```bash
# Health check
curl -f https://croody.app/health/

# Smoke test
curl -f https://croody.app/
curl -f https://croody.app/shop/

# Monitor logs
aws logs tail /ecs/croody-web --follow
```
```

## Output Format

1. **Summary Table**: Estado de cada check
2. **Critical Issues**: Bloqueadores de deploy
3. **Warnings**: Problemas no críticos
4. **Commands**: Comandos de deploy y rollback
5. **Post-Deploy**: Verificación post-deploy

## Quick Commands

```bash
# Full check
/deploy-check

# Solo Django
/deploy-check django

# Solo Docker
/deploy-check docker

# Solo SSL
/deploy-check ssl
```

---

Argumento recibido: $ARGUMENTS

Si no hay argumento, ejecuta verificación completa.
Si hay argumento específico, enfócate en esa área.
