# Documentacion Completa - Proyecto Croody

## Indice General

### Introduccion y Vision General
- **[01-ARQUITECTURA/overview.md](01-ARQUITECTURA/overview.md)** - Arquitectura general del sistema, decisiones tecnicas, stack tecnologico

### Backend - Core y APIs
- **[02-BACKEND/accounts/](02-BACKEND/accounts/)** - App accounts: UserProfile, Subscription, Inventory, WalletTransaction
- **[02-BACKEND/modelos/](02-BACKEND/modelos/)** - Modelos de datos (Product, Order, Transaction)
- **[02-BACKEND/vistas/](02-BACKEND/vistas/)** - Class-Based Views (CBV), Mixins, logica de negocio
- **[02-BACKEND/api/](02-BACKEND/api/)** - Endpoints REST, serializadores, ViewSets

### Frontend y Diseno
- **[03-FRONTEND/design-system/](03-FRONTEND/design-system/)** - Sistema de diseno, tokens, Golden Ratio, colores, tipografia
- **[03-FRONTEND/componentes/](03-FRONTEND/componentes/)** - Componentes UI reutilizables (botones, cards, formularios)
- **[03-FRONTEND/javascript/](03-FRONTEND/javascript/)** - JavaScript modulos (theme toggle, language selector, navegacion movil)

### DevOps e Infraestructura
- **[04-DEVOPS/docker-compose.md](04-DEVOPS/docker-compose.md)** - Configuracion Docker, Docker Compose, multi-servicio, volumenes
- **[04-DEVOPS/ci-cd-workflows.md](04-DEVOPS/ci-cd-workflows.md)** - 7 workflows de CI/CD con GitHub Actions
- **[04-INFRAESTRUCTURA/](04-INFRAESTRUCTURA/)** - Terraform, AWS (VPC, ECS, RDS, ElastiCache), BIND9 DNS

### Seguridad
- **[06-SEGURIDAD/hardening.md](06-SEGURIDAD/hardening.md)** - HSTS, CSP, SSL/TLS, firewall, rate limiting, headers de seguridad

### Internacionalizacion
- **[07-INTERNACIONALIZACION/sistema-traduccion.md](07-INTERNACIONALIZACION/sistema-traduccion.md)** - Sistema i18n con 8 idiomas (ES, EN, FR, PT, AR RTL, ZH-Hans, JA, HI)

### Patrones y Mejores Practicas
- **[08-PATRONES/](08-PATRONES/)** - Patrones Django (CBV, Mixins, Signals), Type Hints, composicion de formularios

### Desarrollo y Testing
- **[08-DESARROLLO/](08-DESARROLLO/)** - Guias de desarrollo, testing, contribucion

### Usuario y Flujos
- **[09-USUARIO/](09-USUARIO/)** - Casos de uso, flujos de trabajo, funcionalidades

### Operativo
- **[10-OPERATIVO/](10-OPERATIVO/)** - Troubleshooting, mantenimiento, runbooks, monitoreo

### Apendices
- **[11-APENDICES/](11-APENDICES/)** - Glosario tecnico, comandos utiles, recursos

### Diagramas Arquitectonicos
- **[14-DIAGRAMAS/](14-DIAGRAMAS/)** - Diagramas Mermaid (sistema, Django MVT, microservicios, DB, Docker, CI/CD)

---

## Inicio Rapido

### Para Desarrolladores Backend
```bash
# 1. App accounts (perfiles, suscripciones, wallet Solana)
cat docs/02-BACKEND/accounts/README.md

# 2. Modelos de tienda (Product, Order)
cat docs/02-BACKEND/modelos/product.md

# 3. Vistas y logica de negocio
cat docs/02-BACKEND/vistas/

# 4. CI/CD y Docker
cat docs/04-DEVOPS/ci-cd-workflows.md
```

### Para Desarrolladores Frontend
```bash
# 1. Sistema de diseno y colores
cat docs/03-FRONTEND/design-system/colores.md

# 2. Tokens CSS
cat docs/03-FRONTEND/design-system/tokens.md

# 3. Componentes UI
cat docs/03-FRONTEND/componentes/
```

### Para DevOps
```bash
# 1. Docker y contenedores
cat docs/04-DEVOPS/docker-compose.md

# 2. CI/CD pipelines (7 workflows)
cat docs/04-DEVOPS/ci-cd-workflows.md

# 3. Seguridad y hardening
cat docs/06-SEGURIDAD/hardening.md
```

---

## Estructura del Proyecto

```
proyecto_integrado/
├── Croody/                          # Aplicacion Django principal
│   ├── accounts/                    # App: Perfiles, Suscripciones, Wallet
│   │   ├── models.py                # UserProfile, Subscription, UserInventory, WalletTransaction
│   │   ├── views.py                 # ProfileView, SubscriptionView
│   │   └── forms.py                 # Formularios de perfil
│   ├── landing/                     # App: Landing page, Buddy
│   │   ├── models.py                # LegacyUserProfile (deprecated)
│   │   └── views.py                 # HomeView, BuddyView
│   ├── shop/                        # App: Catalogo y checkout
│   │   ├── models.py                # Product, Order, OrderItem, Transaction
│   │   └── views.py                 # ProductListView, CheckoutView
│   ├── templates/                   # Templates Django
│   └── static/                      # Archivos estaticos (CSS, JS)
│
├── services/                        # Microservicios FastAPI
│   ├── telemetry-gateway/           # Servicio de telemetria
│   └── ids-ml/                      # Servicio de deteccion IDS
│
├── docs/                            # Documentacion (este directorio)
│   ├── 01-ARQUITECTURA/             # Arquitectura general
│   ├── 02-BACKEND/                  # Backend Django
│   │   ├── accounts/                # Documentacion app accounts
│   │   ├── modelos/                 # Documentacion de modelos
│   │   ├── vistas/                  # Documentacion de vistas
│   │   └── api/                     # Documentacion de APIs
│   ├── 03-FRONTEND/                 # Frontend y diseno
│   │   ├── design-system/           # Colores, tipografia, espaciado
│   │   ├── componentes/             # Componentes UI
│   │   └── javascript/              # Modulos JS
│   ├── 04-DEVOPS/                   # DevOps
│   ├── 04-INFRAESTRUCTURA/          # Terraform, AWS, DNS
│   ├── 06-SEGURIDAD/                # Seguridad
│   ├── 07-INTERNACIONALIZACION/     # i18n (8 idiomas)
│   └── ...                          # Otros directorios
│
├── .github/workflows/               # GitHub Actions CI/CD (7 workflows)
├── infra/terraform/                 # Infraestructura como codigo
└── docker-compose.yml               # Orquestacion multi-servicio
```

---

## Tecnologias Clave

### Backend
- **Django 4.x** - Framework web con patron MVT
- **Django REST Framework** - APIs REST
- **FastAPI** - Microservicios (telemetria, IDS)
- **PostgreSQL** - Base de datos principal
- **Redis** - Cache y sesiones

### Frontend
- **Django Templates** - Sistema de templates
- **Tailwind CSS** - Framework CSS (design system Nocturne)
- **JavaScript (ES6+)** - Interactividad
- **Golden Ratio (phi=1.618)** - Proporciones de diseno

### DevOps
- **Docker + Docker Compose** - Contenedores
- **GitHub Actions** - CI/CD (7 workflows)
- **Terraform** - Infraestructura como codigo
- **Cloudflare** - DNS, CDN, SSL

### Blockchain
- **Solana** - Pagos con wallet (suscripciones, compras)
- **Solana Pay** - Integracion de pagos

---

## Modelos Principales

### App `accounts` (POST-LOGIN)
| Modelo | Descripcion |
|--------|-------------|
| `UserProfile` | Perfil extendido: datos fisicos, avatar, wallet Solana, gamificacion |
| `UserInventory` | Items adquiridos (productos, personajes) |
| `Subscription` | Suscripciones (Starter €19.99, Pro €59.99, Elite €199.99) |
| `WalletTransaction` | Transacciones Solana |

### App `shop` (E-COMMERCE)
| Modelo | Descripcion |
|--------|-------------|
| `Product` | Productos de la tienda |
| `Order` | Ordenes de compra |
| `OrderItem` | Items de una orden |
| `Transaction` | Pagos (Stripe, PayPal, etc.) |

### App `landing` (LEGACY)
| Modelo | Descripcion |
|--------|-------------|
| `LegacyUserProfile` | DEPRECATED - usar `accounts.UserProfile` |

---

## Sistema de Gamificacion

### Puntos
| Accion | Puntos |
|--------|--------|
| Perfil 100% completo | +500 |
| Wallet Solana verificada | +200 |
| Foto de perfil | +100 |
| Personaje activo | +50 |
| Cada item en inventario | +50 |
| Suscripcion Starter | +300 |
| Suscripcion Pro | +500 |
| Suscripcion Elite | +1000 |

### Rangos
| Rango | Puntos |
|-------|--------|
| Novato | 0-499 |
| Aprendiz | 500-1499 |
| Guerrero | 1500-2999 |
| Maestro | 3000-4999 |
| Leyenda | 5000+ |

---

## Comandos de Desarrollo

### Django
```bash
# Servidor desarrollo
python manage.py runserver

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Testing
pytest

# Shell Django
python manage.py shell

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
```

---

## Workflows CI/CD

| Workflow | Descripcion |
|----------|-------------|
| `ci.yml` | Linting, Testing, Security scans |
| `deploy.yml` | Deploy por SSH |
| `terraform-ci.yml` | Validacion Terraform |
| `full-stack-validate.yml` | Validacion end-to-end |
| `bind-deploy.yml` | Deploy DNS BIND9 |
| `dns-lint.yml` | Linting DNS |
| `deploy-selfhosted.yml` | Deploy self-hosted + Cloudflare |

---

## Contribuir

### Antes de Empezar
1. Leer **[01-ARQUITECTURA/overview.md](01-ARQUITECTURA/overview.md)**
2. Configurar entorno con **[04-DEVOPS/docker-compose.md](04-DEVOPS/docker-compose.md)**
3. Revisar **[06-SEGURIDAD/hardening.md](06-SEGURIDAD/hardening.md)**

### Para Cambios de Codigo
1. Seguir patrones existentes en el codebase
2. Escribir tests (pytest)
3. Documentar cambios significativos

---

## Soporte

### Troubleshooting
- Ver carpeta **[10-OPERATIVO/troubleshooting/](10-OPERATIVO/troubleshooting/)**
- Health endpoints: `/health/` (Django), `/healthz` (FastAPI)

### Recursos
- Ver carpeta **[11-APENDICES/](11-APENDICES/)**
- Documentacion externa en cada seccion

---

**Documentacion completa del proyecto Croody**

Para mas informacion, consultar las secciones especificas en el indice superior.
