# Documentación Completa - Proyecto Croody

## 📋 Índice General

### 🎯 Introducción y Visión General
- **[01-ARQUITECTURA/overview.md](01-ARQUITECTURA/overview.md)** - Arquitectura general del sistema, decisiones técnicas, stack tecnológico

### 🔧 Backend - Core y APIs
- **[02-BACKEND/modelos.md](02-BACKEND/modelos.md)** - Modelos de datos (UserProfile, Product, RobotPosition), relaciones, QuerySets personalizados
- **[02-BACKEND/vistas.md](02-BACKEND/vistas.md)** - Class-Based Views (CBV), Mixins, lógica de negocio, vistas de landing, shop y perfil
- **[02-BACKEND/apis.md](02-BACKEND/apis.md)** - Endpoints REST, serializadores, ViewSets, APIs para telemetría e IDS

### 🎨 Frontend y Diseño
- **[07-DESIGN-System/design-system.md](07-DESIGN-System/design-system.md)** - Sistema de diseño, tokens, Golden Ratio, colores, tipografía
- **[07-DESIGN-System/componentes.md](07-DESIGN-System/componentes.md)** - Componentes UI reutilizables (botones, cards, formularios)
- **[07-DESIGN-System/javascript.md](07-DESIGN-System/javascript.md)** - JavaScript módulos (theme toggle, language selector, navegación móvil)
- **[12-USUARIO/aplicacion.md](12-USUARIO/aplicacion.md)** - Aplicación completa: Landing, Buddy, Shop, Perfil de usuario

### ⚙️ DevOps e Infraestructura
- **[04-DEVOPS/docker.md](04-DEVOPS/docker.md)** - Configuración Docker, Docker Compose, multi-servicio, volúmenes
- **[04-DEVOPS/cicd.md](04-DEVOPS/cicd.md)** - 7 workflows de CI/CD con GitHub Actions, testing, build, deploy
- **[04-DEVOPS/infraestructura.md](04-DEVOPS/infraestructura.md)** - Terraform, AWS (VPC, ECS, RDS, ElastiCache), BIND9 DNS

### 🔒 Seguridad
- **[06-SEGURIDAD/hardening.md](06-SEGURIDAD/hardening.md)** - HSTS, CSP, SSL/TLS, firewall, rate limiting, headers de seguridad

### 🌍 Internacionalización
- **[05-INTERNACIONALIZACION/i18n-completo.md](05-INTERNACIONALIZACION/i18n-completo.md)** - Sistema i18n con 8 idiomas (ES, EN, FR, PT, AR RTL, ZH-Hans, JA, HI)

### 🧪 Testing
- **[09-TESTING/testing-general.md](09-TESTING/testing-general.md)** - Estrategia multi-nivel (unit, integración, E2E), pytest, Playwright, coverage

### 📊 Monitoreo y Operación
- **[10-MONITOREO/logs-sistema.md](10-MONITOREO/logs-sistema.md)** - Logging estructurado, métricas, health checks, alertas, Prometheus/Grafana

### 🔍 Patrones y Mejores Prácticas
- **[08-PATRONES/desarrollo.md](08-PATRONES/desarrollo.md)** - Patrones Django (CBV, Mixins, Signals), Type Hints, composición de formularios

### 🚨 Soporte y Mantenimiento
- **[11-TROUBLESHOOTING/guia-problemas-comunes.md](11-TROUBLESHOOTING/guia-problemas-comunes.md)** - Troubleshooting para Django, FastAPI, Docker, CI/CD, base de datos

### 📐 Diagramas Arquitectónicos
- **[14-DIAGRAMAS/arquitectura.md](14-DIAGRAMAS/arquitectura.md)** - 12 diagramas Mermaid (sistema, Django MVT, microservicios, DB, Docker, CI/CD, frontend, i18n, usuario, monitoreo, AWS, seguridad)

### 📚 Referencia y Recursos
- **[13-APENDICES/apendices.md](13-APENDICES/apendices.md)** - Glosario técnico (200+ términos), comandos útiles, recursos, templates

---

## 🎯 Inicio Rápido

### Para Desarrolladores Backend
```bash
# 1. Modelo de datos y relaciones
cat docs/02-BACKEND/modelos.md

# 2. Vistas y lógica de negocio
cat docs/02-BACKEND/vistas.md

# 3. APIs y endpoints
cat docs/02-BACKEND/apis.md

# 4. Patrones de desarrollo
cat docs/08-PATRONES/desarrollo.md
```

### Para Desarrolladores Frontend
```bash
# 1. Sistema de diseño
cat docs/07-DESIGN-System/design-system.md

# 2. Componentes UI
cat docs/07-DESIGN-System/componentes.md

# 3. JavaScript y funcionalidades
cat docs/07-DESIGN-System/javascript.md

# 4. Aplicación de usuario
cat docs/12-USUARIO/aplicacion.md
```

### Para DevOps
```bash
# 1. Docker y contenedores
cat docs/04-DEVOPS/docker.md

# 2. CI/CD pipelines
cat docs/04-DEVOPS/cicd.md

# 3. Infraestructura AWS
cat docs/04-DEVOPS/infraestructura.md

# 4. Monitoreo y logs
cat docs/10-MONITOREO/logs-sistema.md
```

### Para Seguridad
```bash
# 1. Hardening y seguridad
cat docs/06-SEGURIDAD/hardening.md

# 2. Infraestructura segura
cat docs/04-DEVOPS/infraestructura.md

# 3. Diagrama de seguridad
cat docs/14-DIAGRAMAS/arquitectura.md
```

---

## 📁 Estructura del Proyecto

```
proyecto_integrado/
├── Croody/                          # Aplicación Django principal
│   ├── landing/                     # App: Landing page, Buddy, Profile
│   │   ├── models.py                # UserProfile, signals
│   │   ├── views.py                 # HomeView, BuddyView, ProfileView
│   │   ├── forms.py                 # Formularios personalizados
│   │   └── signals.py               # Django signals
│   ├── shop/                        # App: Catálogo de productos
│   │   ├── models.py                # Product, ProductQuerySet
│   │   └── views.py                 # ProductListView, ProductDetailView
│   ├── templates/                   # Templates Django
│   │   ├── base.html                # Template base
│   │   ├── landing/                 # Templates de landing
│   │   └── shop/                    # Templates de shop
│   └── static/                      # Archivos estáticos
│       ├── css/                     # Estilos (tokens, components, base)
│       └── js/                      # JavaScript (theme, language)
│
├── services/                        # Microservicios FastAPI
│   ├── telemetry-gateway/           # Servicio de telemetría
│   │   └── main.py                  # Endpoints /api/telemetry/*
│   └── ids-ml-service/              # Servicio de detección IDS
│       └── main.py                  # Endpoint /api/ids/predict
│
├── docs/                            # Documentación completa (este directorio)
│   ├── 01-ARQUITECTURA/             # Arquitectura general
│   ├── 02-BACKEND/                  # Backend Django
│   ├── 04-DEVOPS/                   # DevOps y despliegue
│   ├── 05-INTERNACIONALIZACION/     # Sistema i18n
│   ├── 06-SEGURIDAD/                # Seguridad
│   ├── 07-DESIGN-System/            # Frontend y diseño
│   ├── 08-PATRONES/                 # Patrones de desarrollo
│   ├── 09-TESTING/                  # Testing
│   ├── 10-MONITOREO/                # Monitoreo
│   ├── 11-TROUBLESHOOTING/          # Solución de problemas
│   ├── 12-USUARIO/                  # Aplicación de usuario
│   ├── 13-APENDICES/                # Glosario y recursos
│   └── 14-DIAGRAMAS/                # Diagramas de arquitectura
│
├── .github/workflows/               # GitHub Actions CI/CD
│   ├── test.yml                     # Tests automatizados
│   ├── build.yml                    # Build de imágenes Docker
│   ├── deploy.yml                   # Deploy a producción
│   └── i18n.yml                     # Gestión de traducciones
│
├── terraform/                       # Infraestructura como código
│   ├── main.tf                      # Recursos AWS principales
│   ├── vpc.tf                       # Configuración VPC
│   ├── ecs.tf                       # Configuración ECS
│   └── dns.tf                       # Configuración BIND9
│
└── docker-compose.yml               # Orquestación multi-servicio
```

---

## 🚀 Tecnologías Clave

### Backend
- **Django 3.2+** - Framework web con patrón MVT
- **Django REST Framework** - APIs REST
- **FastAPI** - Microservicios (telemetría, IDS)
- **PostgreSQL** - Base de datos principal
- **SQLite** - Base de datos para microservicios
- **Redis** - Cache y sesiones

### Frontend
- **Django Templates** - Sistema de templates
- **HTML5 + CSS3** - Estructura y estilos
- **JavaScript (ES6+)** - Interactividad
- **Bootstrap 5.3** - Framework CSS (CDN)
- **Golden Ratio (φ=1.618)** - Proporciones de diseño

### DevOps
- **Docker + Docker Compose** - Contenedores
- **GitHub Actions** - CI/CD (7 workflows)
- **Terraform** - Infraestructura como código
- **AWS** - Cloud (ECS, RDS, ElastiCache, S3, CloudFront)
- **BIND9** - DNS interno

### Seguridad
- **SSL/TLS** - Cifrado en tránsito
- **HSTS** - HTTP Strict Transport Security
- **CSP** - Content Security Policy
- **UFW** - Firewall
- **CSRF** - Protección Django

### Testing
- **pytest** - Framework de testing
- **pytest-django** - Integración Django
- **pytest-cov** - Coverage reports
- **Playwright** - E2E testing
- **Factory Boy** - Test factories

### Monitoreo
- **Structured JSON Logging** - Logs estructurados
- **Prometheus** - Métricas
- **Grafana** - Visualización
- **Health Checks** - Endpoints de salud

---

## 📖 Flujo de Lectura Sugerido

### 1. Para Nuevos Desarrolladores
1. **[01-ARQUITECTURA/overview.md](01-ARQUITECTURA/overview.md)** - Visión general
2. **[02-BACKEND/modelos.md](02-BACKEND/modelos.md)** - Entender datos
3. **[02-BACKEND/vistas.md](02-BACKEND/vistas.md)** - Entender lógica
4. **[07-DESIGN-System/design-system.md](07-DESIGN-System/design-system.md)** - Entender frontend
5. **[04-DEVOPS/docker.md](04-DEVOPS/docker.md)** - Entender despliegue local

### 2. Para Cambios de Backend
1. **[02-BACKEND/modelos.md](02-BACKEND/modelos.md)** - Modelos existentes
2. **[08-PATRONES/desarrollo.md](08-PATRONES/desarrollo.md)** - Patrones a seguir
3. **[09-TESTING/testing-general.md](09-TESTING/testing-general.md)** - Testing requirements
4. **[02-BACKEND/apis.md](02-BACKEND/apis.md)** - APIs REST

### 3. Para Cambios de Frontend
1. **[07-DESIGN-System/design-system.md](07-DESIGN-System/design-system.md)** - Tokens y estilos
2. **[07-DESIGN-System/componentes.md](07-DESIGN-System/componentes.md)** - Componentes disponibles
3. **[07-DESIGN-System/javascript.md](07-DESIGN-System/javascript.md)** - JS modules
4. **[12-USUARIO/aplicacion.md](12-USUARIO/aplicacion.md)** - Contexto de aplicación

### 4. Para Deploy a Producción
1. **[04-DEVOPS/docker.md](04-DEVOPS/docker.md)** - Docker configuration
2. **[04-DEVOPS/cicd.md](04-DEVOPS/cicd.md)** - CI/CD pipelines
3. **[04-DEVOPS/infraestructura.md](04-DEVOPS/infraestructura.md)** - AWS infrastructure
4. **[06-SEGURIDAD/hardening.md](06-SEGURIDAD/hardening.md)** - Security checklist
5. **[10-MONITOREO/logs-sistema.md](10-MONITOREO/logs-sistema.md)** - Monitoring setup

### 5. Para Solución de Problemas
1. **[11-TROUBLESHOOTING/guia-problemas-comunes.md](11-TROUBLESHOOTING/guia-problemas-comunes.md)** - Problemas comunes
2. **[10-MONITOREO/logs-sistema.md](10-MONITOREO/logs-sistema.md)** - Logs y diagnósticos
3. **[13-APENDICES/apendices.md](13-APENDICES/apendices.md)** - Comandos útiles

---

## 🔑 Conceptos Clave

### Backend - Django MVT
- **Model**: UserProfile (OneToOne → User), Product, RobotPosition
- **View**: Class-Based Views (CBV) con Mixins
- **Template**: Sistema de templates con herencia y blocks
- **Signals**: Automatización (post_save User → create UserProfile)
- **QuerySet**: Custom managers (ProductQuerySet.published())

### Backend - FastAPI Microservicios
- **Telemetry Gateway** (puerto 9000): Ingesta de datos de robots
- **IDS ML Service** (puerto 9100): Detección de intrusiones con ML
- **Health Checks**: Endpoints /healthz
- **Pydantic**: Validación de datos

### Frontend - Design System
- **Golden Ratio**: φ = 1.618 para proporciones
- **4 Paletas**: Gator, Jungle, Sand, Crimson
- **2 Temas**: Dark y Light
- **CSS Custom Properties**: Variables para tokens
- **IIFE Pattern**: Prevención de FOUC

### Internacionalización - 8 Idiomas
- **Idiomas**: ES (por defecto), EN, FR, PT, AR (RTL), ZH-Hans, JA, HI
- **Archivos .po**: Strings traducibles
- **Archivos .mo**: Strings compilados
- **i18n_patterns**: URLs con prefijo de idioma
- **RTL**: Soporte para árabe (Right-to-Left)

### DevOps - Multi-Servicio
- **5 Servicios**: Nginx, Django, Telemetry Gateway, IDS ML, Robot Simulator
- **4 Volumes**: PostgreSQL, Redis, Static files, Telemetry DB
- **7 Workflows**: test, build, deploy, i18n, security, performance, docs
- **Terraform**: VPC, ECS, RDS, ElastiCache, S3

### Seguridad - Multi-Capa
- **Edge**: Cloudflare (DDoS, WAF)
- **Application**: Django security (CSRF, XSS, SQL injection)
- **API**: FastAPI security (CORS, rate limiting, API keys)
- **Network**: Firewall, VPC isolation, security groups
- **Data**: Encryption, password hashing, secrets management
- **Headers**: HSTS, CSP, X-Frame-Options

---

## 🛠️ Comandos de Desarrollo

### Django
```bash
# Servidor desarrollo
python manage.py runserver

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Testing
pytest
pytest --cov=proyecto_integrado

# Shell Django
python manage.py shell

# Collect static
python manage.py collectstatic --noinput

# Compilar traducciones
python manage.py compilemessages
```

### Docker
```bash
# Ejecutar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Rebuild
docker-compose up --build

# Ejecutar comando en container
docker-compose exec croody python manage.py shell

# Cleanup
docker-compose down -v
```

### FastAPI
```bash
# Servidor desarrollo
uvicorn main:app --reload --host 0.0.0.0 --port 9000

# Testing
pytest tests/ -v --cov=.
```

### CI/CD
```bash
# GitHub Actions local testing
act

# Ver workflow runs
gh run list
```

---

## 📊 Métricas del Proyecto

### Documentación
- **25 secciones** de documentación completa
- **7000+ líneas** de documentación técnica
- **200+ términos** en el glosario
- **12 diagramas** arquitectónicos Mermaid
- **8 idiomas** soportados (i18n)

### Código
- **2 aplicaciones** Django (landing, shop)
- **2 microservicios** FastAPI
- **5 servicios** Docker
- **7 workflows** CI/CD
- **100% type hints** en Python

### Testing
- **75% Unit Tests** - pytest
- **20% Integration Tests** - pytest-django
- **5% E2E Tests** - Playwright
- **Coverage reporting** - pytest-cov

### Seguridad
- **Multi-layer security** - Edge, App, API, Network, Data
- **OWASP Top 10** compliance
- **SSL/TLS** encryption
- **HSTS, CSP** headers
- **CSRF protection**

---

## 🤝 Cómo Contribuir

### 1. Antes de Empezar
- Leer **[01-ARQUITECTURA/overview.md](01-ARQUITECTURA/overview.md)**
- Entender **[08-PATRONES/desarrollo.md](08-PATRONES/desarrollo.md)**
- Configurar entorno según **[04-DEVOPS/docker.md](04-DEVOPS/docker.md)**

### 2. Para Cambios de Código
- Seguir patrones de **[08-PATRONES/desarrollo.md](08-PATRONES/desarrollo.md)**
- Escribir tests según **[09-TESTING/testing-general.md](09-TESTING/testing-general.md)**
- Verificar **[06-SEGURIDAD/hardening.md](06-SEGURIDAD/hardening.md)**

### 3. Para Nuevas Features
- Documentar en **[12-USUARIO/aplicacion.md](12-USUARIO/aplicacion.md)**
- Actualizar diagramas en **[14-DIAGRAMAS/arquitectura.md](14-DIAGRAMAS/arquitectura.md)**
- Añadir tests E2E si es UI

### 4. Para Documentación
- Mantener estilo consistente
- Incluir ejemplos de código
- Añadir referencias cruzadas
- Actualizar este README

---

## 📞 Soporte

### Problemas Comunes
- **[11-TROUBLESHOOTING/guia-problemas-comunes.md](11-TROUBLESHOOTING/guia-problemas-comunes.md)** - Guía completa de troubleshooting

### Monitoreo
- **[10-MONITOREO/logs-sistema.md](10-MONITOREO/logs-sistema.md)** - Logs y métricas
- **Health endpoints**: `/health/` (Django), `/healthz` (FastAPI)

### Recursos
- **[13-APENDICES/apendices.md](13-APENDICES/apendices.md)** - Glosario y comandos
- Documentación externa en cada sección

---

## 📝 Changelog

### v1.0.0 (Actual)
- ✅ 25 secciones de documentación completa
- ✅ 12 diagramas arquitectónicos Mermaid
- ✅ Sistema i18n con 8 idiomas
- ✅ 7 workflows CI/CD
- ✅ Infraestructura Terraform completa
- ✅ Guía de troubleshooting completa
- ✅ Testing multi-nivel (unit, integration, E2E)
- ✅ Seguridad multi-capa (HSTS, CSP, firewall)

### Próximas Versiones
- [ ] Documentación de APIs interactiva (Swagger/OpenAPI)
- [ ] Guías de deployment específicas por entorno
- [ ] Benchmarks de performance
- [ ] Documentación de migraciones de datos
- [ ] Guías de rollback y disaster recovery

---

## 🎓 Aprendizaje

### Para Aprender Django
1. **[02-BACKEND/modelos.md](02-BACKEND/modelos.md)** - Models y ORM
2. **[02-BACKEND/vistas.md](02-BACKEND/vistas.md)** - Views y CBV
3. **[08-PATRONES/desarrollo.md](08-PATRONES/desarrollo.md)** - Patrones avanzados
4. **[09-TESTING/testing-general.md](09-TESTING/testing-general.md)** - Testing

### Para Aprender FastAPI
1. **services/telemetry-gateway/main.py** - Ejemplo de API
2. **[02-BACKEND/apis.md](02-BACKEND/apis.md)** - APIs REST
3. **[11-TROUBLESHOOTING/guia-problemas-comunes.md](11-TROUBLESHOOTING/guia-problemas-comunes.md)** - FastAPI troubleshooting

### Para Aprender DevOps
1. **[04-DEVOPS/docker.md](04-DEVOPS/docker.md)** - Docker y Compose
2. **[04-DEVOPS/cicd.md](04-DEVOPS/cicd.md)** - CI/CD
3. **[04-DEVOPS/infraestructura.md](04-DEVOPS/infraestructura.md)** - Terraform/AWS
4. **[10-MONITOREO/logs-sistema.md](10-MONITOREO/logs-sistema.md)** - Monitoreo

### Para Aprender Seguridad
1. **[06-SEGURIDAD/hardening.md](06-SEGURIDAD/hardening.md)** - Hardening guide
2. **[14-DIAGRAMAS/arquitectura.md](14-DIAGRAMAS/arquitectura.md)** - Security diagram
3. **[11-TROUBLESHOOTING/guia-problemas-comunes.md](11-TROUBLESHOOTING/guia-problemas-comunes.md)** - Security issues

---

## 🏗️ Arquitectura en una Mirada

```
┌─────────────────────────────────────────────────────────────┐
│                     Croody Ecosystem                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  🌐 Frontend (Django Templates)                             │
│  ├── Landing (Hero, Metrics, Ecosystem)                     │
│  ├── Buddy (Step-by-step, Benefits)                         │
│  ├── Shop (Catalogue, Filters, Detail)                      │
│  └── Profile (Info, Preferences, Token)                     │
│                                                               │
│  🔧 Backend (Django MVT)                                    │
│  ├── Models (UserProfile, Product)                          │
│  ├── Views (CBV, Mixins)                                    │
│  ├── Templates (Inheritance, Blocks)                        │
│  └── APIs (REST, Serializers)                               │
│                                                               │
│  ⚡ Microservicios (FastAPI)                                │
│  ├── Telemetry Gateway (Port 9000)                          │
│  └── IDS ML Service (Port 9100)                             │
│                                                               │
│  💾 Storage                                                 │
│  ├── PostgreSQL (Primary DB)                                │
│  ├── SQLite (Telemetry)                                     │
│  ├── Redis (Cache, Sessions)                                │
│  └── S3 (Static Files)                                      │
│                                                               │
│  🐳 DevOps                                                  │
│  ├── Docker (5 services)                                    │
│  ├── CI/CD (7 workflows)                                    │
│  └── Terraform (AWS Infrastructure)                         │
│                                                               │
│  🔒 Security                                                │
│  ├── SSL/TLS, HSTS, CSP                                     │
│  ├── Firewall, VPC                                          │
│  └── CSRF, XSS Protection                                   │
│                                                               │
│  🌍 i18n (8 languages)                                      │
│  ├── ES, EN, FR, PT, AR (RTL), ZH-Hans, JA, HI             │
│  └── .po/.mo files                                          │
│                                                               │
│  🧪 Testing                                                 │
│  ├── Unit (pytest, 75%)                                     │
│  ├── Integration (pytest-django, 20%)                       │
│  └── E2E (Playwright, 5%)                                   │
│                                                               │
│  📊 Monitoring                                              │
│  ├── Structured Logging (JSON)                              │
│  ├── Prometheus (Metrics)                                   │
│  ├── Grafana (Visualization)                                │
│  └── Health Checks                                          │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📄 Licencia

Este proyecto y su documentación son parte del ecosistema Croody.

---

## 🙏 Agradecimientos

- **Django Team** - Framework web robusto
- **FastAPI Team** - Microservicios modernos
- **GitHub** - CI/CD y colaboración
- **AWS** - Infraestructura en la nube
- **Terraform** - Infraestructura como código
- **Mermaid** - Diagramas beautiful

---

**Documentación completa del proyecto Croody - Versión 1.0.0**

Para más información, consultar las secciones específicas en el índice superior.
