# Arquitectura General - Proyecto Croody

## Resumen
Documentación completa de la arquitectura del sistema Croody, un ecosistema completo de entrenamiento AI personalizado con comercio electrónico, microservicios de telemetría y análisis de seguridad basado en ML.

## Ubicación
- **Aplicación Principal**: `/proyecto_integrado/Croody/`
- **Microservicios**: `/proyecto_integrado/services/`
- **Documentación**: `/proyecto_integrado/docs/`

## Stack Tecnológico

### Backend
- **Django 3.2+**: Framework web con patrón MVT (Model-View-Template)
- **Django REST Framework**: APIs RESTful
- **FastAPI**: Microservicios asíncronos (Python 3.11+)
- **PostgreSQL 13+**: Base de datos principal
- **SQLite**: Base de datos para microservicios (desarrollo)
- **Redis 6+**: Cache y gestión de sesiones
- **Python 3.11**: Lenguaje de programación

### Frontend
- **Django Templates**: Sistema de templates con herencia
- **HTML5 + CSS3**: Estructura y estilos modernos
- **JavaScript ES6+**: Interactividad del lado del cliente
- **Bootstrap 5.3**: Framework CSS (vía CDN)
- **CSS Custom Properties**: Variables CSS para tokens de diseño
- **IIFE Pattern**: Prevención de FOUC (Flash of Unstyled Content)

### DevOps e Infraestructura
- **Docker + Docker Compose**: Contenedorización y orquestación
- **GitHub Actions**: CI/CD (7 workflows automatizados)
- **Terraform**: Infraestructura como código (IaC)
- **AWS**: Cloud provider
  - ECS (Elastic Container Service)
  - RDS (Relational Database Service)
  - ElastiCache (Redis)
  - S3 (Simple Storage Service)
  - CloudFront (CDN)
  - VPC (Virtual Private Cloud)
- **BIND9**: DNS interno para la infraestructura

### Seguridad
- **SSL/TLS**: Cifrado en tránsito
- **HSTS**: HTTP Strict Transport Security
- **CSP**: Content Security Policy
- **UFW**: Uncomplicated Firewall
- **Django Security**: CSRF, XSS, SQL Injection protection
- **CORS**: Configuración para APIs
- **Rate Limiting**: Limitación de requests

### Testing
- **pytest**: Framework de testing principal
- **pytest-django**: Integración con Django
- **pytest-cov**: Reporting de coverage
- **pytest-xdist**: Testing paralelo
- **pytest-mock**: Mocking para tests
- **Playwright**: End-to-End testing
- **Factory Boy**: Test factories para datos

### Monitoreo y Observabilidad
- **Structured JSON Logging**: Logs estructurados y parseables
- **Prometheus**: Recolección de métricas
- **Grafana**: Visualización de métricas
- **Health Checks**: Endpoints de salud (/health/, /healthz)
- **Centralized Logging**: Agregación de logs
- **Security Event Logging**: Logs de eventos de seguridad

## Arquitectura del Sistema

### Visión General
```
┌─────────────────────────────────────────────────────────────┐
│                        Croody System                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Landing    │  │     Buddy    │  │    Shop      │       │
│  │   (Hero)     │  │  (AI Coach)  │  │  (E-commerce)│       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│         └─────────────────┼─────────────────┘                │
│                             │                                │
│                      ┌──────▼────────┐                      │
│                      │ Django (MVT)  │                      │
│                      │   Models      │                      │
│                      └──────┬────────┘                      │
│                             │                                │
│         ┌───────────────────┼───────────────────┐           │
│         │                   │                   │           │
│  ┌──────▼───────┐  ┌────────▼──────┐  ┌────────▼──────┐    │
│  │ PostgreSQL   │  │    Redis      │  │      S3       │    │
│  │  (Primary)   │  │ (Cache/Sessions)│  │  (Static)    │    │
│  └──────────────┘  └───────────────┘  └───────────────┘    │
│                                                               │
│  ┌──────────────┐              ┌──────────────┐             │
│  │ Telemetry    │              │   IDS ML     │             │
│  │ Gateway      │              │   Service    │             │
│  │ FastAPI :9000│              │ FastAPI :9100│             │
│  └──────┬───────┘              └──────┬───────┘             │
│         │                             │                     │
│         └─────────────┬───────────────┘                     │
│                       │                                   │
│                ┌──────▼──────────┐                        │
│                │  SQLite (Dev)   │                        │
│                │  PostgreSQL (Prod)│                       │
│                └─────────────────┘                        │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Prometheus   │  │   Grafana    │  │  Logs        │       │
│  │ (Metrics)    │  │ (Dashboard)  │  │(Centralized) │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Componentes Principales

#### 1. Aplicación Django (Puerto 8000)
**Apps**: `landing`, `shop`

**Models**:
- `UserProfile` (OneToOne → User): Perfil extendido con tokens
- `Product`: Catálogo de productos con QuerySet personalizado
- `RobotPosition`: Posición de robots para telemetría

**Views**:
- **Landing**: HomeView, BuddyView, AboutView
- **Shop**: ProductListView, ProductDetailView (con filtros y búsqueda)
- **Profile**: ProfileView con 3 formularios (perfil, preferencias, token)

**Features**:
- Class-Based Views (CBV) con Mixins
- Django Signals para automatización
- Type Hints (PEP 484) en todo el código
- Internacionalización (i18n) con 8 idiomas

#### 2. Microservicio Telemetry Gateway (Puerto 9000)
**FastAPI** con endpoints:
- `POST /api/telemetry/ingest`: Ingesta de datos
- `GET /api/telemetry/last`: Último dato
- `GET /api/telemetry/live`: Datos en vivo
- `GET /api/telemetry/query`: Consulta histórica
- `GET /healthz`: Health check

**Storage**:
- SQLite (desarrollo)
- PostgreSQL (producción opcional)

#### 3. Microservicio IDS ML Service (Puerto 9100)
**FastAPI** con endpoints:
- `POST /api/ids/predict`: Predicción ML
- `GET /healthz`: Health check

**Features**:
- Modelo ML serializado (pickle)
- Metadata JSON (versión, accuracy)
- Inference en tiempo real

#### 4. Base de Datos Principal (PostgreSQL)
**Esquema**:
- `auth.User`: Usuarios Django
- `landing_userprofile`: Perfiles extendidos
- `shop_product`: Catálogo de productos
- `landing_robotposition`: Posiciones de robots

**Features**:
- Índices optimizados
- Conexión pooling
- Backups automáticos
- Multi-AZ (producción)

#### 5. Cache y Sesiones (Redis)
**Uso**:
- Cache de consultas frecuentes
- Sesiones de usuario
- Rate limiting (opcional)
- Message broker (opcional)

#### 6. Almacenamiento Estático (S3)
**Contenido**:
- Imágenes de productos
- CSS compilado
- JavaScript minificado
- Fuentes web
- Archivos de medios

**Features**:
- CDN integrado (CloudFront)
- Compresión automática
- Versionado

### Arquitectura Docker

#### Servicios (docker-compose.yml)
1. **nginx**: Gateway, SSL termination
2. **django**: Aplicación web principal
3. **telemetry-gateway**: Microservicio telemetría
4. **ids-ml-service**: Microservicio ML
5. **robot-simulator**: Simulador para testing

#### Volúmenes
1. **postgres_data**: Datos persistentes PostgreSQL
2. **redis_data**: Datos persistentes Redis
3. **static_volume**: Archivos estáticos
4. **telemetry_db**: Base de datos telemetría

#### Networks
- **croody-network**: Red interna para comunicación

### Arquitectura CI/CD (GitHub Actions)

#### Workflows (7 total)
1. **test.yml**: Tests unitarios e integración
2. **e2e.yml**: Tests end-to-end con Playwright
3. **build.yml**: Build de imágenes Docker
4. **deploy.yml**: Deploy a producción
5. **i18n.yml**: Gestión de traducciones
6. **security.yml**: Security scanning
7. **docs.yml**: Generación de documentación

#### Pipeline de Deploy
```
Push/PR → Tests → Build → Push Image → Approval → Deploy → Health Check
```

### Arquitectura AWS (Terraform)

#### VPC (Virtual Private Cloud)
- **Public Subnet**: Load Balancer, Nginx Bastion, BIND9 DNS
- **Private Subnet**: ECS Tasks (Django, FastAPI)
- **Database Subnet**: RDS PostgreSQL Multi-AZ
- **ElastiCache Subnet**: Redis Cluster

#### Servicios AWS
- **ECS**: Orquestación de contenedores
- **RDS**: PostgreSQL con backups automáticos
- **ElastiCache**: Redis cluster
- **S3**: Storage estático y backups
- **CloudFront**: CDN global
- **ALB**: Application Load Balancer
- **CloudWatch**: Monitoreo y logs
- **X-Ray**: Distributed tracing
- **IAM**: Roles y políticas de acceso

#### Security Groups
- **ALB SG**: Puertos 80, 443
- **ECS SG**: Puertos 8000, 9000, 9100
- **RDS SG**: Puerto 5432
- **Redis SG**: Puerto 6379

### Arquitectura de Seguridad (Multi-Capa)

#### 1. Edge Layer (Cloudflare)
- DDoS Protection
- WAF (Web Application Firewall)
- Bot Management
- SSL/TLS termination

#### 2. Application Layer (Django)
- CSRF Protection
- XSS Prevention (auto-escaping)
- SQL Injection Prevention (ORM)
- Authentication & Authorization
- Session Security

#### 3. API Layer (FastAPI)
- CORS Configuration
- Rate Limiting
- API Key Authentication
- Input Validation (Pydantic)

#### 4. Network Layer
- VPC Isolation
- Security Groups
- Firewall Rules (UFW)
- Port Configuration

#### 5. Data Layer
- Encryption at Rest (RDS, S3)
- Encryption in Transit (SSL/TLS)
- Password Hashing (bcrypt/Argon2)
- Secrets Management (Environment Variables)

#### 6. Security Headers
- HSTS (HTTP Strict Transport Security)
- CSP (Content Security Policy)
- X-Frame-Options (Clickjacking Protection)
- X-Content-Type-Options

### Arquitectura de Internacionalización

#### Idiomas Soportados (8 total)
1. **Español (es)** - Idioma por defecto
2. **English (en)**
3. **Français (fr)**
4. **Português (pt)**
5. **العربية (ar)** - RTL (Right-to-Left)
6. **简体中文 (zh_Hans)** - Chinese Simplified
7. **日本語 (ja)** - Japanese
8. **हिन्दी (hi)** - Hindi

#### Componentes i18n
- **LocaleMiddleware**: Detección automática de idioma
- **Language Cookie**: Preferencia persistente
- **URL Prefixes**: `/es/`, `/en/`, etc.
- **Message Files**: `.po` (fuente) y `.mo` (compilado)
- **Translation Strings**: Función `_()` para marcar

#### Flujo de Traducción
```
Template {% trans %} → .po file → Translate → .mo file → Runtime
```

### Arquitectura de Testing (Pirámide)

#### Distribución de Tests
- **75% Unit Tests**: pytest, coverage alto
- **20% Integration Tests**: pytest-django, DB testing
- **5% E2E Tests**: Playwright, flujos completos

#### Frameworks
- **pytest**: Runner principal
- **pytest-django**: Django integration
- **pytest-cov**: Coverage reporting
- **factory-boy**: Test data factories
- **faker**: Datos falsos realistas
- **Playwright**: Browser automation
- **TestClient**: Django/FastAPI testing

### Arquitectura de Monitoreo

#### Logs (Structured JSON)
- **Django Logs**: INFO, DEBUG, ERROR
- **FastAPI Logs**: Request/Response
- **Security Logs**: Auth, threats
- **Application Logs**: Business logic

#### Métricas (Prometheus)
- Response Time (HTTP latency)
- Error Rate (% 5xx responses)
- CPU Usage
- Memory Usage
- Database Queries (count & time)
- Custom Business Metrics

#### Dashboards (Grafana)
- Application Performance
- Business Metrics
- Infrastructure Monitoring
- Security Dashboard
- Error Tracking

#### Health Checks
- `/health/` (Django): DB, Redis, disk
- `/healthz` (FastAPI): DB, memory
- Docker Health Checks
- Load Balancer Health Checks

### Arquitectura de Frontend

#### Design System
- **Golden Ratio**: φ = 1.618 para proporciones
- **4 Paletas**: Gator, Jungle, Sand, Crimson
- **2 Temas**: Dark y Light
- **CSS Custom Properties**: Tokens (colores, spacing, typography)
- **Component Library**: Botones, Cards, Formularios

#### CSS Architecture
- **base.css**: Reset + Typography
- **components.css**: UI Components
- **tokens.css**: CSS Variables
- **animations.css**: Transiciones y animaciones

#### JavaScript Modules
- **theme.js**: Theme toggle (dark/light/system)
- **language-selector.js**: i18n language switcher
- **navigation.js**: Mobile menu
- **search.js**: Búsqueda y filtros

#### Templates (Django)
- **base.html**: Layout común, navigation, footer
- **landing/home.html**: Hero, metrics, ecosystem
- **landing/buddy.html**: Feature explanation
- **shop/catalogue.html**: Product list + filters
- **shop/detail.html**: Product detail
- **account/profile.html**: User profile

## Decisiones Arquitectónicas

### 1. Django MVT vs MVC
**Decisión**: MVT (Model-View-Template)
**Razón**: Django es nativo MVT, simplifica desarrollo, separación clara de concerns

### 2. Class-Based Views vs Function-Based Views
**Decisión**: CBV (Class-Based Views)
**Razón**: Reutilización via Mixins, mantenibilidad, mejor organization

### 3. FastAPI vs Django para Microservicios
**Decisión**: FastAPI
**Razón**: Performance superior, validación automática Pydantic, documentación OpenAPI

### 4. PostgreSQL vs SQLite
**Decisión**: PostgreSQL (producción), SQLite (desarrollo/microservicios)
**Razón**: Escalabilidad, features avanzadas, ACID compliance

### 5. Docker Compose vs Kubernetes
**Decisión**: Docker Compose
**Razón**: Simplicidad, desarrollo local, AWS ECS para producción

### 6. Terraform vs CloudFormation
**Decisión**: Terraform
**Razón**: Multi-cloud, mejor syntax, state management

### 7. Redis vs Memcached
**Decisión**: Redis
**Razón**: Data structures avanzadas, persistencia, ecosystem

### 8. pytest vs unittest
**Decisión**: pytest
**Razón**: Fixtures, parametrización, plugins, readability

### 9. CSS Framework: Custom vs Bootstrap
**Decisión**: Custom Design System + Bootstrap CDN
**Razón**: Control total + componentes готовos

### 10. i18n: Django Built-in vs babel
**Decisión**: Django i18n
**Razón**: Integración nativa, middleware, URL routing

## Patrones de Diseño Implementados

### 1. Model-View-Template (Django)
Separación clara entre datos, lógica y presentación

### 2. Repository Pattern
QuerySets personalizados para abstracción de DB

### 3. Factory Pattern (Factory Boy)
Generación de datos de test

### 4. Observer Pattern (Django Signals)
Event-driven programming para perfil automático

### 5. Mixin Pattern (CBV)
Reutilización de funcionalidad

### 6. Template Inheritance
Base template + child templates

### 7. Dependency Injection
Inyección de dependencias via settings

### 8. Service Layer Pattern
Lógica de negocio separada en servicios

### 9. Circuit Breaker Pattern
Health checks y fail-fast

### 10. Strategy Pattern
Configuración flexible via settings

## Principios Aplicados

### 1. SOLID
- **S**: Responsabilidad única por clase
- **O**: Open/Closed via herencia
- **L**: Liskov Substitution en modelos
- **I**: Interfaces claras (Forms, Serializers)
- **D**: Dependency injection

### 2. DRY (Don't Repeat Yourself)
- Mixins para funcionalidad común
- Template inheritance
- Reutilización de componentes

### 3. KISS (Keep It Simple, Stupid)
- Configuraciones simples
- Menos dependencias
- Código legible

### 4. YAGNI (You Aren't Gonna Need It)
- No over-engineering
- Features basadas en necesidades reales

### 5. Clean Code
- Nombres descriptivos
- Funciones pequeñas
- Comentarios útiles
- Consistencia en estilo

## Escalabilidad

### Horizontal Scaling
- Stateless application servers (ECS)
- Load balancing (ALB)
- Microservices (FastAPI)
- Database read replicas

### Vertical Scaling
- RDS instance sizing
- ECS task memory/CPU
- Redis cluster sizing

### Caching Strategy
- Redis para hot data
- CDN (CloudFront) para static
- Database query caching
- Application-level cache

### Database Optimization
- Índices en campos consultados
- Connection pooling
- Query optimization (select_related, prefetch_related)
- Pagination para listas grandes

## Performance

### Frontend Performance
- Lazy loading de imágenes
- CSS/JS minification
- Gzip compression
- CDN distribution
- Critical CSS inlining

### Backend Performance
- Database query optimization
- Redis caching
- Async processing (FastAPI)
- Connection pooling
- Pagination

### Infrastructure Performance
- Auto Scaling (ECS)
- Load balancing
- Multi-AZ deployment
- Read replicas
- SSD storage

## Disponibilidad (Availability)

### High Availability
- Multi-AZ deployment (AWS)
- Load balancing (ALB)
- Health checks automáticos
- Auto-recovery
- Backup & restore

### Disaster Recovery
- Automated backups (RDS)
- Cross-region replication
- Infrastructure as Code (Terraform)
- Documented runbooks
- RTO/RPO definidos

### Monitoring & Alerting
- Prometheus + Grafana
- CloudWatch alarms
- Centralized logging
- Error tracking
- Uptime monitoring

## Seguridad (Security)

### Defense in Depth
- Multiple security layers
- Principle of least privilege
- Regular security updates
- Vulnerability scanning
- Penetration testing

### Compliance
- OWASP Top 10
- GDPR compliance
- Data encryption
- Audit logging
- Access controls

## Flujo de Desarrollo

### 1. Local Development
```bash
git clone → docker-compose up → python manage.py runserver
```

### 2. Feature Development
```bash
git branch → develop → write code → write tests → commit → PR
```

### 3. CI/CD Pipeline
```bash
push → GitHub Actions → tests → build → push → deploy
```

### 4. Production Deployment
```bash
merge to main → approval → Terraform apply → ECS update
```

## Documentación y Conocimiento

### Documentación Técnica
- 25 secciones completas
- 7000+ líneas
- 12 diagramas arquitectónicos
- Glosario con 200+ términos
- Guías de troubleshooting

### Conocimiento Compartido
- README navegable
- Flujos de lectura por rol
- Comandos de referencia rápida
- Templates y ejemplos
- Mejores prácticas

## Próximas Mejoras

### Técnicas
- [ ] GraphQL API
- [ ] Event-driven architecture (Kafka)
- [ ] gRPC para microservicios
- [ ] Serverless functions (AWS Lambda)
- [ ] Kubernetes migration
- [ ] Service mesh (Istio)
- [ ] Chaos engineering
- [ ] A/B testing platform

### Funcionales
- [ ] Multi-tenancy
- [ ] Real-time notifications (WebSockets)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics
- [ ] ML personalization
- [ ] Video streaming
- [ ] Gamification
- [ ] Social features

## Referencias

### Documentación Interna
- [Modelos - Backend](../02-BACKEND/modelos.md)
- [Vistas - Backend](../02-BACKEND/vistas.md)
- [APIs - Backend](../02-BACKEND/apis.md)
- [Design System - Frontend](../07-DESIGN-System/design-system.md)
- [Docker - DevOps](../04-DEVOPS/docker.md)
- [CI/CD - DevOps](../04-DEVOPS/cicd.md)
- [Seguridad - Hardening](../06-SEGURIDAD/hardening.md)
- [Monitoreo](../10-MONITOREO/logs-sistema.md)
- [Testing](../09-TESTING/testing-general.md)
- [Diagramas Arquitectónicos](../14-DIAGRAMAS/arquitectura.md)

### Documentación Externa
- [Django Documentation](https://docs.djangoproject.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Terraform Documentation](https://www.terraform.io/docs/)
- [AWS Architecture](https://aws.amazon.com/architecture/)

---

## Ver También

### Secciones Relacionadas
- [Diagramas de Arquitectura](../14-DIAGRAMAS/arquitectura.md) - Visualización completa
- [Modelos de Datos](../02-BACKEND/modelos.md) - Esquema detallado
- [Vistas y Lógica](../02-BACKEND/vistas.md) - Implementación
- [Infraestructura](../04-DEVOPS/infraestructura.md) - AWS y Terraform

### Recursos Adicionales
- [Apéndices](../13-APENDICES/apendices.md) - Comandos y glosario
- [Troubleshooting](../11-TROUBLESHOOTING/guia-problemas-comunes.md) - Solución de problemas

---

**Nota**: Esta arquitectura evoluciona continuamente. Para contribuir con mejoras o cambios, consultar las guías de desarrollo en la documentación del proyecto.
