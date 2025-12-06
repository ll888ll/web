---
name: devops-automation
description: Expert patterns for Docker, nginx, CI/CD, and deployment automation in Croody Web. Use when configuring containers, setting up pipelines, optimizing builds, or managing infrastructure.
---

# DevOps Automation para Croody Web

Patrones expertos para Docker, nginx, CI/CD y automatización de deployment.

## Cuándo Usar Este Skill

- Configurando contenedores Docker
- Optimizando nginx como gateway
- Creando pipelines de CI/CD
- Automatizando deployments
- Configurando monitoreo y logging
- Manejando secrets y configuración

## Arquitectura de Infraestructura

```
┌─────────────────────────────────────────────────────────┐
│                     PRODUCTION                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐            │
│  │ CloudFront │→│   ALB    │→│  nginx   │            │
│  │   (CDN)    │  │  (AWS)   │  │ gateway  │            │
│  └─────────┘    └─────────┘    └────┬────┘            │
│                                      │                  │
│         ┌────────────────────────────┼───────┐         │
│         │                            │       │         │
│         ▼                            ▼       ▼         │
│    ┌─────────┐              ┌─────────┐ ┌─────────┐   │
│    │  Django │              │Telemetry│ │   IDS   │   │
│    │  (web)  │              │ FastAPI │ │ FastAPI │   │
│    └────┬────┘              └────┬────┘ └────┬────┘   │
│         │                        │           │         │
│         └────────────┬───────────┴───────────┘         │
│                      ▼                                  │
│               ┌───────────┐                            │
│               │ PostgreSQL │                            │
│               │   (RDS)    │                            │
│               └───────────┘                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Docker Patterns

### 1. Dockerfile Multi-stage (Django)

```dockerfile
# proyecto_integrado/Croody/Dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependencias de build
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

WORKDIR /app

# Instalar solo runtime deps
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN groupadd -r croody && useradd -r -g croody croody

# Copiar wheels y instalar
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

# Copiar código
COPY --chown=croody:croody . .

# Cambiar a usuario no-root
USER croody

# Collectstatic
RUN python manage.py collectstatic --noinput

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000

CMD ["gunicorn", "croody.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### 2. Dockerfile (FastAPI)

```dockerfile
# proyecto_integrado/telemetry_api/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Usuario no-root
RUN groupadd -r telemetry && useradd -r -g telemetry telemetry

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY --chown=telemetry:telemetry . .

USER telemetry

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "2"]
```

### 3. Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build:
      context: ./proyecto_integrado/Croody
      target: runtime
    container_name: croody-web
    ports:
      - "8000:8000"
    volumes:
      - ./proyecto_integrado/Croody:/app
      - static_volume:/app/staticfiles
    environment:
      - DEBUG=True
      - DATABASE_URL=postgres://croody:${DB_PASSWORD}@db:5432/croody_db
      - SECRET_KEY=${DJANGO_SECRET_KEY}
      - ALLOWED_HOSTS=localhost,127.0.0.1
    depends_on:
      db:
        condition: service_healthy
    networks:
      - croody-network
    restart: unless-stopped

  telemetry:
    build:
      context: ./proyecto_integrado/telemetry_api
    container_name: croody-telemetry
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgres://croody:${DB_PASSWORD}@db:5432/croody_db
      - API_KEY=${TELEMETRY_API_KEY}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - croody-network
    restart: unless-stopped

  ids:
    build:
      context: ./proyecto_integrado/ids_api
    container_name: croody-ids
    ports:
      - "8002:8002"
    environment:
      - API_KEY=${IDS_API_KEY}
    networks:
      - croody-network
    restart: unless-stopped

  gateway:
    image: nginx:alpine
    container_name: croody-gateway
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./proyecto_integrado/gateway/nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/var/www/static:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - web
      - telemetry
    networks:
      - croody-network
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: croody-db
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql:ro
    environment:
      - POSTGRES_DB=croody_db
      - POSTGRES_USER=croody
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U croody -d croody_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - croody-network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: croody-redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - croody-network
    restart: unless-stopped

networks:
  croody-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  static_volume:
```

### 4. Docker Compose (Production)

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    image: ${REGISTRY}/croody-web:${VERSION}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    environment:
      - DEBUG=False
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${DJANGO_SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - SENTRY_DSN=${SENTRY_DSN}
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  telemetry:
    image: ${REGISTRY}/croody-telemetry:${VERSION}
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  gateway:
    image: nginx:alpine
    deploy:
      replicas: 2
    volumes:
      - ./gateway/nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
```

## Nginx Configuration

### 5. nginx.conf (Development)

```nginx
# proyecto_integrado/gateway/nginx.conf
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log main;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript
               application/xml application/xml+rss text/javascript;

    # Upstreams
    upstream django {
        server web:8000;
        keepalive 32;
    }

    upstream telemetry {
        server telemetry:8001;
        keepalive 16;
    }

    upstream ids {
        server ids:8002;
        keepalive 16;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=general_limit:10m rate=30r/s;

    server {
        listen 80;
        server_name localhost;

        # Security headers
        add_header X-Frame-Options SAMEORIGIN always;
        add_header X-Content-Type-Options nosniff always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Static files
        location /static/ {
            alias /var/www/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        location /media/ {
            alias /var/www/media/;
            expires 7d;
        }

        # Telemetry API
        location /api/telemetry/ {
            limit_req zone=api_limit burst=20 nodelay;

            proxy_pass http://telemetry/;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Connection "";

            # Timeouts
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }

        # IDS API
        location /api/ids/ {
            limit_req zone=api_limit burst=10 nodelay;
            proxy_pass http://ids/;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Django app
        location / {
            limit_req zone=general_limit burst=50 nodelay;

            proxy_pass http://django;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Connection "";

            # WebSocket support (para HTMX)
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # Health check
        location /health {
            access_log off;
            return 200 "OK";
            add_header Content-Type text/plain;
        }
    }
}
```

### 6. nginx.prod.conf (Production)

```nginx
# proyecto_integrado/gateway/nginx.prod.conf
worker_processes auto;
error_log /var/log/nginx/error.log warn;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Security
    server_tokens off;

    # SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:20m rate=100r/m;
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

    # Upstreams con health checks
    upstream django {
        least_conn;
        server web:8000 weight=5;
        keepalive 64;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name croody.app www.croody.app;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS Server
    server {
        listen 443 ssl http2;
        server_name croody.app www.croody.app;

        ssl_certificate /etc/letsencrypt/live/croody.app/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/croody.app/privkey.pem;

        # Security Headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
        add_header X-Frame-Options SAMEORIGIN always;
        add_header X-Content-Type-Options nosniff always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://unpkg.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com; connect-src 'self' https://api.croody.app;" always;

        # Connection limits
        limit_conn conn_limit 50;

        # Resto de configuración...
        location / {
            proxy_pass http://django;
            # ... headers
        }
    }
}
```

## CI/CD Pipelines

### 7. GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-django

      - name: Run linting
        run: |
          pip install flake8 black isort
          flake8 proyecto_integrado/
          black --check proyecto_integrado/
          isort --check-only proyecto_integrado/

      - name: Run tests
        env:
          DATABASE_URL: postgres://test:test@localhost:5432/test_db
          SECRET_KEY: test-secret-key
        run: |
          cd proyecto_integrado/Croody
          pytest -v --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./proyecto_integrado/Croody/coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'

      - name: Run Bandit security linter
        run: |
          pip install bandit
          bandit -r proyecto_integrado/ -ll

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push Django image
        uses: docker/build-push-action@v5
        with:
          context: ./proyecto_integrado/Croody
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-web:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-web:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build and push Telemetry image
        uses: docker/build-push-action@v5
        with:
          context: ./proyecto_integrado/telemetry_api
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-telemetry:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-telemetry:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production

    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/croody
            docker compose -f docker-compose.prod.yml pull
            docker compose -f docker-compose.prod.yml up -d --remove-orphans
            docker system prune -f
```

## Makefile

### 8. Makefile

```makefile
# Makefile
.PHONY: help dev prod test lint clean deploy

# Variables
COMPOSE_DEV = docker compose
COMPOSE_PROD = docker compose -f docker-compose.prod.yml
DJANGO = $(COMPOSE_DEV) exec web python manage.py

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development
dev: ## Inicia entorno de desarrollo
	$(COMPOSE_DEV) up -d
	@echo "Croody Web running at http://localhost"

dev-build: ## Rebuild containers de desarrollo
	$(COMPOSE_DEV) up -d --build

logs: ## Muestra logs
	$(COMPOSE_DEV) logs -f

stop: ## Detiene containers
	$(COMPOSE_DEV) down

# Django
shell: ## Django shell
	$(DJANGO) shell_plus

migrate: ## Ejecuta migrations
	$(DJANGO) migrate

makemigrations: ## Crea migrations
	$(DJANGO) makemigrations

collectstatic: ## Collectstatic
	$(DJANGO) collectstatic --noinput

createsuperuser: ## Crea superusuario
	$(DJANGO) createsuperuser

# Testing
test: ## Ejecuta tests
	$(COMPOSE_DEV) exec web pytest -v --cov=.

test-fast: ## Tests sin coverage
	$(COMPOSE_DEV) exec web pytest -v -x

lint: ## Linting
	$(COMPOSE_DEV) exec web flake8 .
	$(COMPOSE_DEV) exec web black --check .
	$(COMPOSE_DEV) exec web isort --check-only .

format: ## Auto-format código
	$(COMPOSE_DEV) exec web black .
	$(COMPOSE_DEV) exec web isort .

# Production
prod-deploy: ## Deploy a producción
	$(COMPOSE_PROD) pull
	$(COMPOSE_PROD) up -d --remove-orphans
	$(COMPOSE_PROD) exec web python manage.py migrate --noinput
	$(COMPOSE_PROD) exec web python manage.py collectstatic --noinput

prod-logs: ## Logs de producción
	$(COMPOSE_PROD) logs -f

prod-restart: ## Restart producción
	$(COMPOSE_PROD) restart

# Database
db-backup: ## Backup de base de datos
	$(COMPOSE_DEV) exec db pg_dump -U croody croody_db > backups/backup_$$(date +%Y%m%d_%H%M%S).sql

db-restore: ## Restore de backup (uso: make db-restore FILE=backup.sql)
	$(COMPOSE_DEV) exec -T db psql -U croody croody_db < $(FILE)

# Cleanup
clean: ## Limpia containers y volúmenes
	$(COMPOSE_DEV) down -v --remove-orphans
	docker system prune -f

clean-all: ## Limpieza completa (incluye imágenes)
	$(COMPOSE_DEV) down -v --rmi all --remove-orphans
	docker system prune -af
```

## Monitoring

### 9. Health Checks

```python
# proyecto_integrado/Croody/croody/health.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis
import time

def health_check(request):
    """Endpoint de health check para load balancer."""
    health = {
        "status": "healthy",
        "timestamp": time.time(),
        "checks": {}
    }

    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health["checks"]["database"] = "ok"
    except Exception as e:
        health["checks"]["database"] = f"error: {str(e)}"
        health["status"] = "unhealthy"

    # Cache check
    try:
        cache.set("health_check", "ok", 10)
        if cache.get("health_check") == "ok":
            health["checks"]["cache"] = "ok"
        else:
            health["checks"]["cache"] = "error"
            health["status"] = "unhealthy"
    except Exception as e:
        health["checks"]["cache"] = f"error: {str(e)}"

    status_code = 200 if health["status"] == "healthy" else 503
    return JsonResponse(health, status=status_code)
```

## Best Practices

1. **Secrets**: Nunca en código, usar variables de entorno
2. **Builds**: Multi-stage para imágenes pequeñas
3. **Logs**: JSON estructurado, rotación configurada
4. **Health checks**: En todos los servicios
5. **Rate limiting**: En gateway, no en aplicación
6. **SSL**: Terminar en nginx, renovar automáticamente
7. **Backups**: Automatizados, probados regularmente

## Recursos

- `docs/04-DEVOPS/` - Documentación completa
- `scripts/deployment/` - Scripts de deployment
- `scripts/backup/` - Scripts de backup
