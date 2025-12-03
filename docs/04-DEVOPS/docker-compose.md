# Docker & Docker Compose - Documentación Completa

## Resumen
La arquitectura Docker de Croody implementa un sistema multi-contenedor con separación por servicios: gateway (nginx), aplicación Django, servicios de telemetría, ML/IDS y simulación de robots. Utiliza múltiples archivos docker-compose para diferentes entornos (desarrollo, producción, SSL/ACME).

## Ubicación
- **Aplicación**: `/proyecto_integrado/Croody/Dockerfile`
- **Compose Desarrollo**: `/proyecto_integrado/docker-compose.yml`
- **Compose Producción**: `/proyecto_integrado/docker-compose.prod.yml`
- **Compose ACME**: `/proyecto_integrado/docker-compose.acme.yml`
- **Entrypoints**: `/proyecto_integrado/Croody/docker-entrypoint.sh`, `/entrypoint.prod.sh`
- **Nginx**: `/proyecto_integrado/gateway/nginx.conf`, `/nginx.prod.conf`
- **Variables**: `/proyecto_integrado/.env.example`

## Arquitectura de Contenedores

### Diagrama de Servicios
```
┌─────────────────────────────────────────────────────────────┐
│                     Gateway (Nginx)                         │
│                   ports: 80, 443, 8080                     │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐    ┌──────▼──────┐  ┌───▼────┐
   │ Croody  │    │ Telemetry   │  │ IDS-ML │
   │ Django  │    │ Gateway     │  │ ML     │
   │ :8000   │    │ :9000       │  │ :9100  │
   └─────────┘    └─────────────┘  └────────┘
        │                │                │
   ┌────▼────┐    ┌──────▼──────┐         │
   │ SQLite/ │    │   SQLite    │         │
   │ Postgres│    │   (data)    │         │
   └─────────┘    └─────────────┘         │
                                         │
                                 ┌───────▼──────┐
                                 │ Robot Sim    │
                                 │ (Telemetry   │
                                 │ Generator)   │
                                 └──────────────┘
```

### Servicios Implementados

#### 1. Gateway (Nginx)
- **Imagen**: `nginx:alpine`
- **Puertos**: 80, 443, 8080
- **Función**: Reverse proxy y load balancer
- **Responsabilidades**:
  - SSL/TLS termination
  - Rate limiting (100 req/s)
  - Routing a servicios backend
  - Headers de seguridad
  - Compression (gzip)

#### 2. Croody (Aplicación Django)
- **Build**: Dockerfile propio
- **Puerto**: 8000 (interno)
- **Expose**: 8000
- **Función**: Aplicación web principal
- **Responsabilidades**:
  - Renderizado de templates
  - APIs REST
  - Autenticación de usuarios
  - Gestión de productos
  - Procesamiento de formularios

#### 3. Telemetry Gateway
- **Build**: `./services/telemetry-gateway/Dockerfile`
- **Puerto**: 9000 (interno)
- **Función**: Ingesta y almacenamiento de telemetría
- **Responsabilidades**:
  - Recepción de datos de robots
  - Almacenamiento time-series
  - API para consultas
  - Health checks

#### 4. IDS-ML
- **Build**: `./services/ids-ml/Dockerfile`
- **Puerto**: 9100 (interno)
- **Función**: Detección de intrusiones basada en ML
- **Responsabilidades**:
  - Análisis de tráfico
  - Detección de anomalías
  - Modelos ML para seguridad
  - API de resultados

#### 5. Robot Sim
- **Build**: `./robots/telemetry-robot/Dockerfile`
- **Puertos**: 9090 (expuesto)
- **Función**: Simulador de telemetría
- **Responsabilidades**:
  - Generación de datos de prueba
  - Simulación de movimiento
  - Envío de telemetría
  - Testing de integración

## Dockerfile - Croody Application

### Configuración Base
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
```

**Características**:
- `python:3.11-slim`: Imagen optimizada, menor tamaño
- `PYTHONDONTWRITEBYTECODE=1`: No genera .pyc (mejora seguridad y performance)
- `PYTHONUNBUFFERED=1`: Logs en tiempo real
- `PIP_NO_CACHE_DIR=1`: Reduce tamaño de imagen

### Instalación de Dependencias
```dockerfile
COPY requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends wget openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r /app/requirements.txt
```

**Paquetes del Sistema**:
- `wget`: Health checks y tooling
- `openjdk-21-jre-headless`: CICFlowMeter para análisis de red
- `--no-install-recommends`: Minimiza tamaño

### Estructura de Archivos
```dockerfile
COPY . /app

EXPOSE 8000

COPY docker-entrypoint.sh /entrypoint.sh
COPY docker-entrypoint.prod.sh /entrypoint.prod.sh
RUN chmod +x /entrypoint.sh /entrypoint.prod.sh

CMD ["/entrypoint.sh"]
```

**Características**:
- Copia todo el código fuente
- Expone puerto 8000
- Scripts de entrada configurables
- Permisos de ejecución

## Docker Compose Configurations

### 1. Desarrollo - docker-compose.yml

#### Características Principales
```yaml
services:
  gateway:
    image: nginx:alpine
    container_name: gateway_new
    restart: unless-stopped
    ports:
      - "8080:80"
      - "80:80"
      - "8443:443"
```

**Configuración**:
- **Auto-restart**: `unless-stopped` (reinicia si se detiene excepto manualmente)
- **Múltiples puertos**: Dev (8080), standard (80), SSL (8443)
- **Container naming**: `_new` suffix para versionado

#### Gateway con Security
```yaml
read_only: true
tmpfs:
  - /var/cache/nginx
  - /var/run
mem_limit: 256m
cpus: "0.50"
```

**Hardening**:
- `read_only`: Sistema de archivos de solo lectura
- `tmpfs`: Archivos temporales en memoria
- Límites de recursos (memoria y CPU)

#### Croody Service
```yaml
croody:
  build:
    context: ./Croody
    dockerfile: Dockerfile
  environment:
    - DJANGO_SETTINGS_MODULE=croody.settings
    - DATABASE_URL=sqlite:////data/croody.db
  volumes:
    - ./Croody:/app
    - croody_data:/data
```

**Configuración Dev**:
- **Volume mounting**: `./Croody:/app` para hot reload
- **SQLite**: Base de datos local para desarrollo
- **Named volume**: `croody_data` para persistencia

#### Telemetry Gateway
```yaml
telemetry-gateway:
  build:
    context: ./services/telemetry-gateway
    dockerfile: Dockerfile
  environment:
    - TG_DB_PATH=/data/telemetry.db
  volumes:
    - telemetry_data:/data
```

#### Robot Simulator
```yaml
robot-sim:
  ports:
    - "9090:9090"
  environment:
    - TELEMETRY_INGEST_URL=http://telemetry-gateway:9000/api/telemetry/ingest
    - ROBOT_ID=robot-clases
```

**Features**:
- Puerto expuesto para debugging
- Variable de entorno para ID del robot
- URL de ingesta configurada

### 2. Producción - docker-compose.prod.yml

#### Diferencias Clave

**Base de Datos PostgreSQL**:
```yaml
db:
  image: postgres:15-alpine
  environment:
    - POSTGRES_USER=croody
    - POSTGRES_PASSWORD=croody
    - POSTGRES_DB=croody
  volumes:
    - db_data:/var/lib/postgresql/data
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER"]
```

**Variables de Entorno**:
```yaml
croody:
  environment:
    - SECRET_KEY=${SECRET_KEY}
    - DEBUG=false
    - ALLOWED_HOSTS=${ALLOWED_HOSTS}
    - DATABASE_URL=${DATABASE_URL}
    - GUNICORN_WORKERS=3
    - GUNICORN_THREADS=4
```

**Configuraciones**:
- **postgres:15-alpine**: PostgreSQL oficial
- **Healthcheck**: Verificación de readiness
- **Variables externas**: Cargar desde `.env`
- **Gunicorn**: WSGI server para producción
- **Sin volumes mounted**: Código embebido en imagen

#### Productor con Health Checks
```yaml
healthcheck:
  test: ["CMD", "wget", "-qO-", "http://localhost:8000/"]
  interval: 10s
  timeout: 5s
  retries: 10
```

**Parámetros**:
- `interval`: Frecuencia de chequeo (10s)
- `timeout`: Tiempo máximo por chequeo (5s)
- `retries`: Reintentos antes de marcar como unhealthy (10)

### 3. SSL/ACME - docker-compose.acme.yml

#### Let's Encrypt Integration
```yaml
gateway:
  volumes:
    - letsencrypt:/etc/letsencrypt
    - certbot-www:/var/www/certbot
    - ./gateway/nginx.prod.conf:/etc/nginx/conf.d/default.conf:ro

certbot:
  image: certbot/certbot:latest
  volumes:
    - letsencrypt:/etc/letsencrypt
    - certbot-www:/var/www/certbot
  entrypoint: sh
  command: -c "trap 'exit 0' INT TERM; sleep infinity"
```

**Características**:
- **Volúmenes nombrados**: Persistencia de certificados
- **Certbot**: Cliente automático de Let's Encrypt
- **Modo standalone**: Certificados temporales
- **Read-only config**: Configuración nginx protegida

## Environment Configuration

### .env.example
```env
# Django / Croody
SECRET_KEY=change-me-in-prod
DEBUG=false
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://croody:croody@db:5432/croody

# Telemetry
ALLOWED_ORIGINS=http://localhost:8080,https://localhost:8443
TG_DB_URL=
TG_INGEST_TOKEN=

# IDS-ML
IDS_API_TOKEN=
```

### Variables Requeridas en Producción

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta Django (generar nueva) | `django-insecure-...` |
| `DEBUG` | Modo debug (debe ser `false` en prod) | `false` |
| `ALLOWED_HOSTS` | Hosts permitidos | `croody.com,www.croody.com` |
| `DATABASE_URL` | URL conexión BD | `postgres://user:pass@db:5432/db` |
| `ALLOWED_ORIGINS` | CORS origins | `https://croody.com` |
| `TG_DB_URL` | URL BD telemetría | `sqlite:///data/telemetry.db` |
| `TG_INGEST_TOKEN` | Token autenticación | `abc123...` |

## Entrypoint Scripts

### Desarrollo - docker-entrypoint.sh
```bash
#!/usr/bin/env bash
set -euo pipefail

cd /app

# Migraciones y servidor de desarrollo
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
```

**Flujo**:
1. Cambiar al directorio `/app`
2. Ejecutar migraciones de BD (sin interacción)
3. Iniciar servidor Django dev en 0.0.0.0:8000
4. `set -euo pipefail`: Falla en cualquier error

### Producción - docker-entrypoint.prod.sh
```bash
#!/usr/bin/env bash
set -euo pipefail

cd /app

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn croody.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers ${GUNICORN_WORKERS:-3} \
  --threads ${GUNICORN_THREADS:-4} \
  --timeout ${GUNICORN_TIMEOUT:-60}
```

**Flujo**:
1. Migraciones de BD
2. Recolección de estáticos (WhiteNoise)
3. **exec gunicorn**: Reemplaza proceso shell
4. **Gunicorn workers**: Configurable via env
5. **Graceful shutdown**: Señales manejadas por gunicorn

## Nginx Configuration

### Desarrollo - nginx.conf

#### Compresión
```nginx
gzip on;
gzip_comp_level 5;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript
            text/xml application/xml application/xml+rss text/javascript;
```

**Beneficios**:
- Reduce bandwidth ~70%
- Mejora tiempos de carga
- Nivel 5: balance compresión/rendimiento

#### Rate Limiting
```nginx
limit_req_zone $binary_remote_addr zone=api_zone:10m rate=100r/s;
```

**Configuración**:
- **Zone size**: 10MB (memoría compartida)
- **Rate**: 100 requests/second
- **Key**: IP del cliente

#### WebSocket Support
```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}
```

#### Security Headers
```nginx
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options SAMEORIGIN;
add_header Referrer-Policy no-referrer-when-downgrade;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self' 'unsafe-inline' data: https:; object-src 'none'; frame-ancestors 'self';";
```

**Headers**:
- `nosniff`: Previene MIME sniffing
- `SAMEORIGIN`: Previene clickjacking
- `HSTS`: Fuerza HTTPS (31536000s = 1 año)
- `CSP`: Política de contenido

#### Location Blocks

**Aplicación Django**:
```nginx
location / {
    proxy_pass http://croody:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Request-ID $request_id;
    proxy_connect_timeout 5s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
    proxy_next_upstream error timeout http_502 http_503 http_504;
}
```

**API Telemetría**:
```nginx
location /api/telemetry/ {
    proxy_pass http://telemetry-gateway:9000;
    limit_req zone=api_zone burst=100 nodelay;
}
```

**IDS-ML**:
```nginx
location /api/ids/ {
    proxy_pass http://ids-ml:9100;
    limit_req zone=api_zone burst=100 nodelay;
}
```

## Comandos de Docker

### Desarrollo

#### Iniciar stack completo
```bash
docker-compose up -d
```

#### Ver logs
```bash
# Todos los servicios
docker-compose logs -f

# Servicio específico
docker-compose logs -f croody

# Últimas N líneas
docker-compose logs --tail=100 croody
```

#### Rebuild imagen
```bash
docker-compose up -d --build
```

#### Ejecutar comando en contenedor
```bash
# Shell interactivo
docker-compose exec croody bash

# Comando directo
docker-compose exec croody python manage.py createsuperuser
```

#### Reset completo
```bash
# Parar y eliminar contenedores y volúmenes
docker-compose down -v

# Rebuild desde cero
docker-compose up -d --build --force-recreate
```

### Producción

#### Iniciar con configuración de producción
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

#### Con SSL/ACME
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml -f docker-compose.acme.yml up -d
```

#### Variables de entorno
```bash
# Cargar desde .env
export $(cat .env | xargs)

# O inline
SECRET_KEY=xxx DEBUG=false docker-compose -f docker-compose.prod.yml up -d
```

#### Verificar health
```bash
# Health de todos los servicios
docker-compose ps

# Health específico
docker inspect --format='{{.State.Health.Status}}' croody_new

# Logs de healthcheck
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' croody_new
```

### Gestión de Volúmenes

#### Listar volúmenes
```bash
docker volume ls
```

#### Inspección
```bash
docker volume inspect proyecto_integrado_croody_data
```

#### Backup
```bash
# Crear backup
docker run --rm -v proyecto_integrado_croody_data:/data -v $(pwd):/backup alpine tar czf /backup/croody_data.tar.gz /data

# Restaurar
docker run --rm -v proyecto_integrado_croody_data:/data -v $(pwd):/backup alpine tar xzf /backup/croody_data.tar.gz -C /
```

#### Limpiar volúmenes huérfanos
```bash
docker volume prune
```

### Monitoreo

#### Stats en tiempo real
```bash
docker stats
```

#### Top procesos
```bash
docker-compose top
```

#### Inspección completa
```bash
docker inspect croody_new
```

#### Ver red
```bash
docker network ls
docker network inspect proyecto_integrado_default
```

## Networking

### Red Interna Automática
```yaml
# docker-compose crea automáticamente red 'proyecto_integrado_default'
services:
  croody:
    # Automaticamente en red proyecto_integrado_default
```

### Comunicación Entre Servicios

**Por nombre de servicio** (DNS automático):
```bash
# Desde croody → croody:8000
# Desde nginx → croody:8000
# Desde robot-sim → telemetry-gateway:9000
```

**Variables de red**:
- `http://croody:8000` → Django app
- `http://telemetry-gateway:9000` → Telemetry API
- `http://ids-ml:9100` → IDS service

### Puertos Expuestos

| Servicio | Interna | Externa | Uso |
|----------|---------|---------|-----|
| gateway | 80, 443 | 80, 443, 8080 | Web access |
| croody | 8000 | - | App |
| telemetry-gateway | 9000 | - | Internal API |
| ids-ml | 9100 | - | Internal API |
| robot-sim | 9090 | 9090 | Debug/Testing |

## Persistencia de Datos

### Named Volumes

**Croody Data**:
```yaml
volumes:
  croody_data:
```

**Telemetry Data**:
```yaml
volumes:
  telemetry_data:
```

**PostgreSQL (prod)**:
```yaml
volumes:
  db_data:
    driver: local
```

### Bind Mounts (Solo Desarrollo)

```yaml
volumes:
  - ./Croody:/app  # Código fuente (hot reload)
  - ./services/ids-ml/models:/models  # Modelos ML
```

### Backup y Restauración

#### PostgreSQL
```bash
# Backup
docker-compose exec db pg_dump -U croody croody > backup.sql

# Restore
docker-compose exec -T db psql -U croody croody < backup.sql
```

#### SQLite
```bash
# Backup
docker cp croody_new:/data/croody.db ./backup_croody.db

# Restore
docker cp ./backup_croody.db croody_new:/data/croody.db
```

## Optimizaciones

### Multi-stage Build (Futuro)
```dockerfile
# Build stage
FROM python:3.11-slim as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
```

### Layer Caching
```dockerfile
# Orden óptimo: menos frecuente → más frecuente
COPY requirements.txt /app/
RUN pip install -r requirements.txt  # Cacheable layer

COPY . /app  # Cambios frecuentes
```

### Imagen Base
- `python:3.11-slim` vs `alpine`: Trade-off tamaño vs compatibilidad
- `slim`: 150MB (más herramientas, mejor para debugging)
- `alpine`: 50MB (minimal, pero puede requerir más deps)

### Resource Limits

```yaml
services:
  croody:
    mem_limit: 512m  # Límite de memoria
    cpus: "0.50"     # Límite de CPU (50%)
    mem_reservation: 256m  # Reserva mínima
```

## Seguridad

### Buenas Prácticas Implementadas

1. **No root en producción**:
```dockerfile
USER 1000:1000  # User non-root
```

2. **Read-only filesystem**:
```yaml
read_only: true
tmpfs:
  - /var/cache/nginx
  - /var/run
```

3. **Secrets management**:
   - Variables de entorno (no hardcode)
   - .env para dev
   - Secret management para prod (AWS Secrets, Vault)

4. **Security headers** (nginx):
   - HSTS
   - CSP
   - X-Frame-Options
   - X-Content-Type-Options

5. **Rate limiting**:
   - 100 req/s por IP
   - Burst de 100 requests

6. **Health checks**:
   - Verificación proactiva
   - Auto-restart en fallo

### Recomendaciones Adicionales

```yaml
security_opt:
  - no-new-privileges:true

cap_drop:
  - ALL
cap_add:
  - CHOWN
  - SETGID
  - SETUID
```

## Troubleshooting

### Contenedor no inicia

**Ver logs**:
```bash
docker-compose logs croody
```

**Ejecutar manualmente**:
```bash
docker-compose run --rm croody bash
cd /app && python manage.py migrate
```

### Error de conexión DB

**Verificar red**:
```bash
docker network ls
docker inspect proyecto_integrado_default
```

**Test conectividad**:
```bash
docker-compose exec croody wget telemetry-gateway:9000/healthz
```

### Puerto ocupado
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8080:80"  # Usar 8080 en lugar de 80
```

### Permisos volumen
```bash
# Cambiar owner en Dockerfile
RUN chown -R 1000:1000 /data
```

### Out of memory
```yaml
# Aumentar swap o limits
mem_limit: 1g
```

## Escalabilidad

### Horizontal Scaling (Múltiples workers)

```yaml
croody:
  deploy:
    replicas: 3
  ports:
    - "8000-8002:8000"
```

**Consideraciones**:
- Session management (Redis)
- Database connections pooling
- Load balancing (nginx upstream)

### Vertical Scaling

```yaml
croody:
  mem_limit: 1g
  cpus: "1.0"
  environment:
    - GUNICORN_WORKERS=5
    - GUNICORN_THREADS=4
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/docker.yml
name: Docker Build
on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build
        run: |
          docker-compose build
          docker-compose push
```

### Automated Testing
```yaml
# docker-compose.test.yml
services:
  test:
    build: .
    command: pytest
    volumes:
      - .:/app
```

## Referencias

### Archivos Relacionados
- `Croody/Dockerfile` - Imagen de la aplicación
- `docker-compose.yml` - Configuración desarrollo
- `docker-compose.prod.yml` - Configuración producción
- `docker-compose.acme.yml` - SSL/ACME
- `docker-entrypoint.sh` - Script dev
- `docker-entrypoint.prod.sh` - Script prod
- `gateway/nginx.conf` - Configuración nginx
- `.env.example` - Variables de entorno

### Documentación Externa
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Nginx Proxy Configuration](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)

## Ver También
- [CI/CD Workflows](../ci-cd/workflows.md)
- [Infraestructura Terraform](../infraestructura/terraform.md)
- [Seguridad](../seguridad/hardening.md)
