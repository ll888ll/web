# Apéndices - Documentación Completa

## Resumen
Los apéndices de la documentación de Croody incluyen un **Glosario Técnico** con términos específicos del proyecto, **Comandos Útiles** organizados por categoría (Django, Docker, FastAPI, CI/CD), y **Recursos** (documentación externa, herramientas, enlaces). Serve como referencia rápida para desarrolladores, DevOps y usuarios finales.

## Ubicación
- **Glosario**: Términos técnicos de Django, FastAPI, DevOps, ML/AI
- **Comandos**: Scripts y comandos para desarrollo, deployment, troubleshooting
- **Recursos**: Enlaces a documentación oficial, herramientas,社区

---

## I. Glosario Técnico

### A. Django & Backend

#### **CBV (Class-Based Views)**
Views basadas en clases que proporcionan una interfaz orientada a objetos para crear vistas HTTP. Ejemplo: `TemplateView`, `ListView`, `DetailView`.

#### **Model-View-Template (MVT)**
Patrón arquitectónico de Django:
- **Model**: Representación de datos (clases Python con campos)
- **View**: Lógica de negocio (maneja requests/responses)
- **Template**: Presentación (Django Template Language)

#### **QuerySet**
Colección de objetos de modelo que puede ser filtrada, ordenada o personalizada. Es lazy (no se ejecuta hasta ser evaluado).

```python
# Ejemplo
products = Product.objects.filter(is_published=True).order_by('name')
```

#### **Signal**
Sistema de despacho de eventos en Django que permite que ciertas partes de la aplicación sean notificadas cuando ocurre una acción en otra parte.

```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

#### **OneToOneField**
Relación de uno a uno entre modelos Django. Usado para extender el modelo User con UserProfile.

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
```

#### **Mixin**
Clase que contiene métodos para ser usada por otras clases múltiples. Permite herencia múltiple y reutilización de código.

```python
class LandingNavigationMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_links'] = self.get_nav_links()
        return context
```

#### **Form Composition**
Patrón de formulario que extiende formularios base de Django con campos y lógica personalizada.

```python
class CroodySignupForm(UserCreationForm):
    # Campos adicionales
    preferred_language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
```

#### **Type Hints (PEP 484)**
Anotaciones de tipo en Python que mejoran IDE support y detección de errores.

```python
def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    return {'key': 'value'}
```

### B. FastAPI & Microservicios

#### **FastAPI**
Framework web moderno y rápido para construir APIs con Python 3.6+ basado en Pydantic y Starlette.

#### **Pydantic**
Library de validación de datos usando type hints. Valida automáticamente requests/responses.

```python
from pydantic import BaseModel

class TelemetryIn(BaseModel):
    robot_id: str
    data: dict
```

#### **TestClient**
Cliente de testing para FastAPI que simula requests HTTP sin hacer conexiones reales de red.

```python
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.get("/healthz")
```

#### **Health Check**
Endpoint que verifica el estado de salud de un servicio. Retorna información sobre conectividad DB, memoria, etc.

```python
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
```

#### **CORS (Cross-Origin Resource Sharing)**
Mecanismo que permite recursos de una página web ser solicitados desde un dominio diferente.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
)
```

### C. Frontend & UI/UX

#### **Design System**
Sistema de diseño que define tokens, componentes y patrones visuales consistentes.

#### **Golden Ratio (φ = 1.618)**
Proporción matemática usada para definir espaciado, tipografía y layout en el design system.

#### **CSS Custom Properties**
Variables CSS que permiten reutilización de valores (colores, espaciado, fuentes).

```css
:root {
  --color-primary: #0066cc;
  --spacing-unit: 8px;
}
```

#### **FOUC (Flash of Unstyled Content)**
Flash momentáneo de contenido sin estilos antes de que CSS se cargue completamente.

#### **IIFE (Immediately Invoked Function Expression)**
Patrón de JavaScript para crear scope privado y evitar pollution del namespace global.

```javascript
(function() {
  'use strict';
  // Código del módulo
})();
```

#### **Data Attributes**
Atributos HTML que comienzan con `data-` para almacenar datos custom en elementos.

```html
<button data-product-id="123">Comprar</button>
```

#### **ARIA (Accessible Rich Internet Applications)**
Atributos que mejoran accesibilidad para usuarios con disabilities.

```html
<button aria-expanded="false" aria-controls="menu">Menú</button>
```

#### **Semantic HTML**
Uso de elementos HTML con significado específico (`<nav>`, `<main>`, `<article>`).

#### **Viewport Meta Tag**
Tag que controla cómo una página se muestra en dispositivos móviles.

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### D. Internacionalización (i18n)

#### **gettext**
Sistema de internacionalización que permite traducir texto en aplicaciones.

#### **Locale**
Combinación de idioma y región (ej: `es_ES`, `en_US`).

#### **.po File**
Archivo de texto que contiene strings traducibles y sus traducciones.

#### **.mo File**
Archivo binario compilado desde .po, usado por Django para traducciones runtime.

#### **RTL (Right-to-Left)**
Dirección de texto para idiomas como árabe y hebreo.

#### **i18n_patterns**
Función de Django para agregar prefijos de idioma a URLs.

```python
urlpatterns = i18n_patterns(
    path('', include('landing.urls')),
)
```

#### **Language Cookie**
Cookie que almacena preferencia de idioma del usuario.

#### **Translation String**
String envuelto en función `_(...)` para marcarlo como traducible.

```python
title = _('Título de la página')
```

### E. DevOps & Infrastructure

#### **Docker**
Platform que permite empaquetar aplicaciones en containers (aislados y portable).

#### **Docker Compose**
Herramienta para definir y ejecutar aplicaciones multi-container de Docker.

#### **Container**
Unidad de software que empaqueta código y sus dependencias.

#### **Image**
Template de solo lectura usado para crear containers.

#### **Volume**
Mecanismo para persistir datos generados por un container Docker.

#### **Port Mapping**
Mapeo de puertos del container al host (`-p 8000:8000`).

#### **Health Check**
Comando que verifica si un container está corriendo correctamente.

#### **CI/CD (Continuous Integration/Continuous Deployment)**
Automatización de build, test y deployment de código.

#### **GitHub Actions**
Platform de CI/CD integrada con GitHub para automatizar workflows.

#### **Workflow**
Archivo YAML que define jobs y steps para GitHub Actions.

#### **Artifact**
Archivo generado durante un workflow (binarios, logs, coverage).

#### **Matrix Strategy**
Estrategia para ejecutar jobs en múltiples configuraciones.

```yaml
strategy:
  matrix:
    python-version: [3.9, 3.10, 3.11]
```

#### **Action Reusable**
Action que puede ser usado por múltiples workflows.

#### **Secrets**
Variables sensibles almacenadas de forma segura (claves API, tokens).

#### **Cache**
Mecanismo para almacenar dependencias y acelerar builds.

#### **Timeout**
Tiempo máximo antes de que un step o job falle.

#### **Concurrency**
Control de ejecuciones simultáneas para evitar overlap.

#### **Workflow Dispatch**
Permitir trigger manual de workflows desde GitHub UI.

#### **Workflow Run**
Ejecución individual de un workflow.

#### **Runner**
Máquina que ejecuta jobs de GitHub Actions (hosted o self-hosted).

#### **Job**
Conjunto de steps que se ejecutan en el mismo runner.

#### **Step**
Tarea individual dentro de un job (checkout, setup, run).

#### **Workflow File**
Archivo YAML que define el workflow (.github/workflows/).

### F. Testing

#### **Unit Test**
Test que verifica una unidad individual de código (función, método).

#### **Integration Test**
Test que verifica cómo múltiples unidades trabajan juntas.

#### **E2E (End-to-End) Test**
Test que simula interacciones reales del usuario en toda la aplicación.

#### **Fixture**
Datos de test predefinidos que se cargan antes de ejecutar tests.

#### **Factory**
Pattern para generar datos de test dinámicamente (Factory Boy).

```python
UserFactory(username='test', email='test@example.com')
```

#### **Mock**
Objeto que simula comportamiento de dependencias reales en tests.

#### **Spy**
Mock que registra cómo fue llamado (qué argumentos, cuántas veces).

#### **TestCase**
Clase base para tests en Django que provee setup/teardown y assertions.

#### **TestClient**
Cliente HTTP de Django para testear views sin servidor real.

#### **Coverage**
Métrica que indica qué porcentaje del código fue ejecutado por tests.

#### **Parameterized Test**
Test que se ejecuta múltiples veces con diferentes parámetros.

```python
@pytest.mark.parametrize('theme', ['dark', 'light'])
def test_theme(theme):
    assert apply_theme(theme)
```

#### **Mock**
Simulación de dependencias externas para tests isolados.

```python
@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {'status': 'ok'}
```

#### **Test Pyramid**
Estrategia de testing con muchos unit tests, pocos integration tests, mínimos E2E tests.

#### **Arrange-Act-Assert**
Pattern de testing: preparar datos, ejecutar, verificar.

```python
# Arrange
user = UserFactory()

# Act
result = user.profile.get_token()

# Assert
assert len(result) == 32
```

### G. Security

#### **CSRF (Cross-Site Request Forgery)**
Ataque que fuerza a usuarios a ejecutar acciones no deseadas. Django incluye protección automática.

#### **CSRF Token**
Token aleatorio que verifica que request viene de formulario legítimo.

```html
{% csrf_token %}
```

#### **CORS**
Mecanismo que permite资源共享 entre diferentes orígenes (domains).

#### **XSS (Cross-Site Scripting)**
Ataque que injecta código malicioso en páginas web.

#### **SQL Injection**
Ataque que inserta SQL malicioso en queries. Django ORM previene esto.

#### **HSTS (HTTP Strict Transport Security)**
Header que fuerza navegadores a usar HTTPS.

#### **CSP (Content Security Policy)**
Header que especifica qué recursos puede cargar una página.

#### **X-Frame-Options**
Header que previene clickjacking especificando si site puede ser iframed.

#### **Rate Limiting**
Limitar número de requests que un usuario puede hacer en un período.

#### **Authentication**
Proceso de verificar identidad de usuario (login).

#### **Authorization**
Proceso de verificar permisos de usuario autenticado.

#### **JWT (JSON Web Token)**
Token firmado usado para autenticación stateless.

#### **Session**
Datos almacenados server-side que identifican usuario entre requests.

#### **Password Hashing**
Proceso de encriptar passwords de forma unidireccional.

#### **Salt**
Dato aleatorio añadido a password antes de hashing para prevenir rainbow tables.

#### **HTTPS**
Versión encriptada de HTTP usando TLS/SSL.

#### **SSL/TLS**
Protocolos criptográficos para comunicación segura en internet.

#### **Certificate**
Documento digital que verifica identidad de un sitio web.

#### **Firewall**
Sistema de seguridad que monitorea y controla traffic de red basado en reglas.

#### **iptables**
Interface de línea de comandos para configurar firewall de Linux.

#### **UFW (Uncomplicated Firewall)**
Wrapper simplificado para iptables.

#### **Port**
Endpoint de comunicación en una dirección IP específica.

#### **Rate Limit**
Número máximo de requests permitidos en un período.

### H. Machine Learning & AI

#### **IDS (Intrusion Detection System)**
Sistema que detecta actividades maliciosas en redes.

#### **ML Model**
Modelo de machine learning entrenado para hacer predicciones o clasificaciones.

#### **Feature**
Variable o característica usada por ML model para hacer predicciones.

#### **Prediction**
Output de ML model basado en input features.

#### **Inference**
Proceso de usar ML model entrenado para hacer predicciones.

#### **Model Metadata**
Información sobre ML model (versión, accuracy, features).

#### **Telemetry Data**
Datos de telemetría enviados por robots (temperatura, humedad, posición).

#### **Robot**
Dispositivo físico que envía datos de telemetría a la plataforma.

#### **Ingest**
Proceso de recibir y almacenar datos de telemetría.

#### **Aggregation**
Combinar múltiples datos en resumen o estadística.

#### **Real-time**
Procesamiento de datos inmediatamente después de recibirlo.

#### **Batch Processing**
Procesar grandes volúmenes de datos en intervalos programados.

#### **Classification**
Tipo de ML que categoriza datos en classes predefinidas.

#### **Supervised Learning**
ML que aprende de examples con answers conocidas.

#### **Algorithm**
Conjunto de reglas o instrucciones para resolver problema.

#### **Training Data**
Dataset usado para enseñar a ML model a hacer predicciones.

#### **Test Data**
Dataset separado usado para evaluar performance de ML model.

#### **Accuracy**
Porcentaje de predicciones correctas de un ML model.

### I. Base de Datos

#### **Migration**
Archivo que define cambios en schema de DB de forma versionada.

#### **ORM (Object-Relational Mapping)**
Técnica que permite trabajar con DB usando objetos Python.

#### **SQLite**
Base de datos ligera embebida en aplicaciones Python por defecto.

#### **PostgreSQL**
Base de datos open-source robusta y escalable.

#### **Query Optimization**
Mejorar queries para ejecutar más rápido.

#### **Index**
Estructura de datos que acelera lookups en columnas específicas.

#### **Foreign Key**
Campo que referencia a primary key de otra tabla.

#### **Primary Key**
Campo único que identifica cada fila en una tabla.

#### **Constraint**
Regla que enforced en datos (NOT NULL, UNIQUE, CHECK).

#### **Transaction**
Unidad de trabajo atómica en DB (all or nothing).

#### **ACID**
Propiedades de DB (Atomicity, Consistency, Isolation, Durability).

#### **Connection Pool**
Pool de connections a DB reutilizadas para performance.

#### **N+1 Query Problem**
Anti-pattern que ejecuta N queries adicionales en un loop.

#### **Eager Loading**
Cargar datos relacionados junto con query principal.

#### **Lazy Loading**
Cargar datos relacionados solo cuando se acceden.

#### **select_related()**
Django optimization que hace JOIN para ForeignKeys.

#### **prefetch_related()**
Django optimization que hace query separada para relaciones múltiples.

#### **Raw Query**
Query SQL escrito manualmente en lugar de usar ORM.

#### **Manager**
Interface QuerySet por defecto de Django models.

#### **QuerySet**
Colección de objects desde DB que puede ser filtrada y modificada.

### J. Performance

#### **Latency**
Tiempo entre request y response (delay).

#### **Throughput**
Número de requests procesados por unidad de tiempo.

#### **Response Time**
Tiempo total para completar request incluyendo procesamiento.

#### **Load Time**
Tiempo para cargar completamente una página web.

#### **Optimization**
Mejorar performance haciendo code or infrastructure más eficiente.

#### **Caching**
Almacenar datos frecuentemente accedidos para acceso rápido.

#### **Cache Hit**
Cuándo request puede ser servida desde cache en lugar de DB.

#### **Cache Miss**
Cuándo data no está en cache y debe ser fetcheada de source original.

#### **Redis**
Base de datos en memoria usada como cache y message broker.

#### **Memcached**
Sistema de caching distribuido en memoria de alto performance.

#### **CDN (Content Delivery Network)**
Red de servers geográficamente distribuidos para servir contenido.

#### **Compression**
Reducir tamaño de archivos para transferencia más rápida.

#### **Minification**
Remover caracteres innecesarios de JS/CSS (espacios, comments).

#### **Bundle**
Archivo único que contiene múltiples files concatenados.

#### **Lazy Loading**
Cargar recursos solo cuando son necesarios.

#### **Debounce**
Delay antes de ejecutar función para evitar ejecuciones excesivas.

#### **Throttle**
Limitar número de veces que función puede ser ejecutada.

#### **Profiling**
Analizar performance de code identificando bottlenecks.

#### **Benchmark**
Test que mide performance de system o componente.

#### **Benchmarking**
Proceso de comparar performance entre diferentes approaches.

### K. Logging & Monitoring

#### **Structured Logging**
Logging en formato consistente y machine-readable (JSON).

```python
logger.info("User logged in", extra={
    "user_id": 123,
    "ip": "192.168.1.1",
    "event_type": "login"
})
```

#### **Log Level**
Nivel de severidad de log message: DEBUG, INFO, WARNING, ERROR, CRITICAL.

#### **Log Formatter**
Configuración que define formato de log messages.

#### **Handler**
Componente que destination especificada para log messages.

#### **Logger**
Componente que recibe log requests y los rutea a handlers.

#### **Health Check**
Endpoint que verifica status de aplicación y dependencias.

#### **Metrics**
Medidas de performance o business (response time, errors, users).

#### **Monitoring**
Observar system en tiempo real para detectar issues.

#### **Alerting**
Notificar cuando metric exceed threshold o error occurs.

#### **Dashboard**
Visualización de metrics y logs en tiempo real.

#### **Centralized Logging**
Agregar logs de multiple sources en single location.

#### **Log Aggregation**
Coleccionar y indexar logs de multiple systems.

#### **ELK Stack**
Elasticsearch, Logstash, Kibana - popular log management solution.

#### **Graylog**
Alternative open-source para centralized logging.

#### **Splunk**
Commercial log analytics platform.

#### **Datadog**
SaaS monitoring y analytics platform.

#### **New Relic**
Commercial application performance monitoring (APM).

#### **Prometheus**
Open-source monitoring system con time-series DB.

#### **Grafana**
Visualization platform para metrics y logs.

#### **Uptime Monitoring**
Verificar que aplicaciones estén accesibles.

#### **Synthetic Monitoring**
Automatizar checks periódicos simulando user behavior.

#### **Real User Monitoring (RUM)**
Monitoring basado en real users interacting con app.

#### **APM (Application Performance Monitoring)**
Monitoreo detallado de application performance.

---

## II. Comandos Útiles

### A. Django

#### Gestión de Proyecto
```bash
# Crear proyecto Django
django-admin startproject proyecto_integrado

# Crear app
python manage.py startapp landing
python manage.py startapp shop

# Ejecutar servidor desarrollo
python manage.py runserver
python manage.py runserver 0.0.0.0:8000

# Puerto específico
python manage.py runserver 8080
```

#### Base de Datos
```bash
# Crear migraciones
python manage.py makemigrations
python manage.py makemigrations landing
python manage.py makemigrations shop

# Aplicar migraciones
python manage.py migrate
python manage.py migrate landing 0001

# Ver estado de migraciones
python manage.py showmigrations
python manage.py showmigrations landing

# SQL de migración
python manage.py sqlmigrate shop 0001

# Resetear BD (solo dev)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser

# Shell Django
python manage.py shell
python manage.py shell_plus  # Con django-extensions

# Acceso directo a DB
python manage.py dbshell
```

#### Datos
```bash
# Crear superuser
python manage.py createsuperuser

# Dump de datos
python manage.py dumpdata > backup.json
python manage.py dumpdata shop.Product > products.json

# Load fixture
python manage.py loaddata backup.json
python manage.py loaddata products.json

# Limpiar cache
python manage.py clear_cache
```

#### Assets
```bash
# Recopilar static files
python manage.py collectstatic --noinput

# Compilar mensajes i18n
python manage.py compilemessages

# Extraer strings de traducción
python manage.py makemessages -l es
python manage.py makemessages -a  # Todos los idiomas

# Verificar configuración
python manage.py check
python manage.py check --deploy
```

#### Testing
```bash
# Ejecutar tests
python manage.py test
python manage.py test shop
python manage.py test shop.tests.test_models

# Con coverage
pytest
pytest --cov=proyecto_integrado
pytest --cov=proyecto_integrado --cov-report=html

# Tests específicos
pytest tests/unit/test_models.py -v
pytest tests/unit/ -k "test_published"

# Tests con database
pytest --reuse-db
pytest tests/integration/ -s
```

#### Debugging
```bash
# Con Django Debug Toolbar
# settings.py debe incluir DEBUG_TOOLBAR

# SQL queries en shell
from django.db import connection
from shop.models import Product
products = Product.objects.all()
print(connection.queries)

# Listar URLs
python manage.py show_urls
```

#### Personalizados
```bash
# Crear management command
touch landing/management/__init__.py
touch landing/management/commands/__init__.py
touch landing/management/commands/runhttps.py

# Ejecutar comando personalizado
python manage.py runhttps
python manage.py clear_cache
```

#### Deployment
```bash
# Verificar preparación para producción
python manage.py check --deploy

# Recopilar static con compression
python manage.py collectstatic --noinput --clear

# Comprimir archivos estáticos
find staticfiles -name "*.css" -exec gzip {} \;
find staticfiles -name "*.js" -exec gzip {} \;
```

### B. Docker & Docker Compose

#### Build & Run
```bash
# Build imagen
docker build -t croody:latest .
docker build -t croody:latest proyecto_integrado/

# Ejecutar container
docker run -p 8000:8000 croody:latest
docker run -d -p 8000:8000 --name croody_new croody:latest

# Con variables de entorno
docker run -p 8000:8000 \
  -e SECRET_KEY='test-key' \
  -e DEBUG=1 \
  croody:latest

# Con volume mount
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  croody:latest
```

#### Docker Compose
```bash
# Ejecutar todos los servicios
docker-compose up
docker-compose up -d  # Modo daemon

# Reconstruir servicios
docker-compose up --build
docker-compose build croody

# Reconstruir sin cache
docker-compose build --no-cache

# Parar servicios
docker-compose down
docker-compose down -v  # También elimina volúmenes

# Ver logs
docker-compose logs -f croody
docker-compose logs --tail=100 croody

# Ejecutar comando en container
docker-compose exec croody python manage.py shell
docker-compose exec croody bash

# Ver estado
docker-compose ps
docker-compose ps -a  # Incluye stopped

# Ver uso de recursos
docker stats
docker-compose top
```

#### Cleanup
```bash
# Eliminar containers parados
docker container prune

# Eliminar imágenes no usadas
docker image prune
docker image prune -a  # Todas

# Eliminar volumes no usados
docker volume prune

# Limpiar todo (⚠️ CUIDADO)
docker system prune -a
docker system prune -a --volumes

# Resetear todo
docker-compose down -v
docker-compose rm -f
docker rmi $(docker images -q)
```

#### Troubleshooting
```bash
# Ver logs de container específico
docker logs croody_new
docker logs -f croody_new
docker logs --tail=50 croody_new

# Inspeccionar container
docker inspect croody_new

# Ejecutar shell en container running
docker exec -it croody_new bash

# Verificar si container está corriendo
docker ps | grep croody

# Verificar puerto en uso
lsof -i :8000
netstat -tulpn | grep 8000

# Verificar espacio en disco
docker system df

# Verificar configuración
docker-compose config
```

#### Images
```bash
# Listar imágenes
docker images
docker images -a

# Eliminar imagen
docker rmi imagen_id
docker rmi croody:latest

# Tag imagen
docker tag croody:latest croody:v1.0

# Push a registry
docker push usuario/croody:latest

# Pull de registry
docker pull usuario/croody:latest
```

### C. FastAPI

#### Desarrollo
```bash
# Ejecutar servidor desarrollo
uvicorn main:app --reload
uvicorn main:app --reload --host 0.0.0.0 --port 9000

# Con worker
uvicorn main:app --workers 4

# Modo debug
uvicorn main:app --reload --log-level debug

# Con hot reload para múltiples archivos
watchmedo auto-restart --directory=./app --pattern="*.py" -- uvicorn main:app --reload
```

#### Testing
```bash
# Instalar dependencias de test
pip install httpx pytest pytest-cov

# Ejecutar tests
pytest
pytest -v
pytest test_app.py
pytest tests/ -v --cov=.

# Con coverage
pytest --cov=app --cov-report=html --cov-report=term

# Tests específicos
pytest test_app.py::test_healthz -v

# Con fixtures
pytest tests/ -s  # Captura stdout
```

#### API Documentation
```bash
# Verificar OpenAPI schema
python -c "import json; from main import app; print(json.dumps(app.openapi(), indent=2))"

# Generar client SDK
curl -X GET http://localhost:9000/openapi.json > openapi.json
```

#### Database
```bash
# Conectar a SQLite
sqlite3 telemetry.db
.tables
SELECT * FROM telemetry LIMIT 5;

# Con PostgreSQL (si usa)
psql -h localhost -U postgres -d croody
\dt  # Listar tablas
SELECT * FROM telemetry LIMIT 5;
```

#### Profiling
```bash
# Instalar profiling tools
pip install py-spy

# Probar endpoint bajo carga
uvicorn main:app --reload &
sleep 2
py-spy -o profile.svg -- uvicorn main:app --port 9000

# Con locust para load testing
pip install locust
locust -f tests/performance/test_load.py --host http://localhost:9000
```

### D. CI/CD (GitHub Actions)

#### Workflow Management
```bash
# Ver workflow runs
gh run list
gh run list --workflow=test.yml

# Ver workflow logs
gh run view 1234567890
gh run view 1234567890 --log

# Re-run workflow
gh run rerun 1234567890
gh run rerun --failed  # Re-run failed jobs

# Cancelar workflow
gh run cancel 1234567890
```

#### Local Testing
```bash
# Instalar act para testing local
# macOS
brew install act

# Ubuntu/Debian
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Ejecutar workflow
act
act -j test  # Job específico

# Con secrets
act -s SECRET_KEY=mysecret

# Usar workflow file específico
act -W .github/workflows/test.yml
```

#### Debugging
```bash
# Ver workflow file
cat .github/workflows/test.yml

# Validar YAML
yamllint .github/workflows/*.yml

# Ver artifacts
gh api repos/:owner/:repo/actions/artifacts
```

### E. Git

#### Básico
```bash
# Inicializar repo
git init
git remote add origin https://github.com/user/repo.git

# Clonar
git clone https://github.com/user/repo.git
git clone https://github.com/user/repo.git --branch develop

# Status
git status
git diff
git diff --staged

# Commit
git add .
git commit -m "feat: añadir nueva funcionalidad"
git commit -am "update: modificar archivos tracked"

# Push
git push origin main
git push origin feature/nueva-funcionalidad
```

#### Branching
```bash
# Crear branch
git checkout -b feature/nueva-funcionalidad
git switch -c feature/nueva-funcionalidad

# Cambiar branch
git checkout main
git switch develop

# Merge
git checkout main
git merge feature/nueva-funcionalidad

# Eliminar branch
git branch -d feature/nueva-funcionalidad
git push origin --delete feature/nueva-funcionalidad
```

#### History
```bash
# Ver commit history
git log
git log --oneline
git log --graph --oneline --all

# Ver cambios específicos
git show HEAD
git show 123abc

# Ver diff de commit
git show 123abc --stat

# Undo last commit (pero mantener cambios)
git reset --soft HEAD~1
```

#### Stashing
```bash
# Guardar cambios temporalmente
git stash push -m "trabajo en progreso"
git stash

# Ver stashes
git stash list

# Aplicar stash
git stash pop
git stash apply stash@{0}

# Eliminar stash
git stash drop stash@{0}
```

#### Tags
```bash
# Crear tag
git tag v1.0.0
git tag -a v1.0.0 -m "Release 1.0.0"

# Push tag
git push origin v1.0.0
git push origin --tags

# Ver tags
git tag
git show v1.0.0
```

#### Advanced
```bash
# Cherry-pick
git cherry-pick 123abc

# Rebase
git checkout feature-branch
git rebase main
git rebase -i HEAD~3  # Interactivo

# Bisect (buscar commit que broke)
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect reset
```

### F. Seguridad

#### Firewall (UFW)
```bash
# Ver status
sudo ufw status
sudo ufw status verbose

# Habilitar firewall
sudo ufw enable

# Deshabilitar firewall
sudo ufw disable

# Permitir puerto
sudo ufw allow 22
sudo ufw allow 8000

# Denegar puerto
sudo ufw deny 8080

# Permitir desde IP
sudo ufw allow from 192.168.1.1

# Permitir rango de puertos
sudo ufw allow 8000:8010/tcp

# Reglas numeradas
sudo ufw status numbered

# Eliminar regla
sudo ufw delete allow 22
sudo ufw delete 2

# Reset
sudo ufw reset
```

#### SSL/TLS
```bash
# Generar certificate self-signed (dev)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Verificar certificate
openssl x509 -in cert.pem -text -noout

# Test SSL connection
openssl s_client -connect localhost:8000 -servername localhost

# Check certificate expiration
openssl x509 -in cert.pem -noout -enddate
```

#### SSH
```bash
# Generar SSH key
ssh-keygen -t ed25519 -C "tu@email.com"

# Agregar key a ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key a server
ssh-copy-id usuario@server.com

# Test SSH connection
ssh -i ~/.ssh/custom_key usuario@server.com
```

#### Passwords
```bash
# Generar password seguro
openssl rand -base64 32
pwgen -s 32 1  # Si pwgen instalado

# Hash password (Python)
python3 -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('password123'))"
```

#### File Permissions
```bash
# Ver permissions
ls -la archivo.txt
stat archivo.txt

# Cambiar permissions
chmod 644 archivo.txt  # rw-r--r--
chmod 755 directorio/  # rwxr-xr-x

# Cambiar owner
sudo chown usuario:grupo archivo.txt

# Permisos recursivos
chmod -R 755 directorio/
sudo chown -R usuario:grupo directorio/
```

### G. Monitoreo & Logs

#### Docker Logs
```bash
# Ver logs
docker logs croody_new
docker logs -f croody_new  # Follow
docker logs --tail=100 croody_new

# Logs con timestamp
docker logs -t croody_new

# Logs desde timestamp
docker logs --since 2024-01-15T10:00:00 croody_new
```

#### System Logs
```bash
# Logs de sistema (Linux)
sudo journalctl -u croody
sudo journalctl -u croody -f  # Follow
sudo journalctl -u croody --since "1 hour ago"

# Ver todos los logs
sudo journalctl
sudo journalctl --since today

# Logs por priority
sudo journalctl -p err
sudo journalctl -p warning
```

#### Nginx Logs
```bash
# Ver access log
tail -f /var/log/nginx/access.log

# Ver error log
tail -f /var/log/nginx/error.log

# Ver logs específicos
grep "404" /var/log/nginx/access.log

# Stats de access log
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -20
```

#### Python Logs
```bash
# Django logs
tail -f /var/log/croody/application.log

# Filtrar errores
grep "ERROR" /var/log/croody/application.log

# Logs JSON pretty print
cat /var/log/croody/application.log | jq 'select(.level == "ERROR")'
```

### H. Performance

#### System Resources
```bash
# CPU y memoria
top
htop
btop  # Mejor que htop

# Uso de memoria
free -h
cat /proc/meminfo

# Uso de CPU
cat /proc/cpuinfo
nproc  # Número de CPUs

# Disk usage
df -h
du -sh /var/log/croody/

# I/O
iotop
iostat -x 1
```

#### Django Performance
```bash
# Ver queries SQL en development
# settings.py
DEBUG_PROPAGATE_EXCEPTIONS = True
LOGGING['loggers']['django.db.backends']['level'] = 'DEBUG'

# Con django-debug-toolbar
pip install django-debug-toolbar
# Añadir a INSTALLED_APPS y MIDDLEWARE

# Profiling Django
pip install django-silk
# settings.py
INSTALLED_APPS += ['silk']
MIDDLEWARE += ['silk.middleware.SilkyMiddleware']
```

#### Docker Performance
```bash
# Ver recursos por container
docker stats

# Ver procesos en container
docker exec croody_new ps aux

# Ver uso de disco por container
docker system df -v

# Container info detallada
docker inspect croody_new | jq '.'
```

### I. Networking

#### Connectivity
```bash
# Test HTTP endpoint
curl -v http://localhost:8000/health/
curl -I http://localhost:8000/

# POST request
curl -X POST http://localhost:9000/api/telemetry/ingest \
  -H "Content-Type: application/json" \
  -d '{"robot_id": "test", "data": {"TEMP": 25}}'

# Con authentication
curl -H "Authorization: Bearer token123" http://localhost:8000/api/data

# Ver response headers
curl -i http://localhost:8000/

# Follow redirects
curl -L http://localhost:8000/
```

#### Ports
```bash
# Ver puertos en uso
netstat -tulpn | grep :8000
ss -tulpn | grep :8000

# Ver proceso en puerto específico
lsof -i :8000

# Kill process en puerto
kill -9 $(lsof -t -i:8000)
```

#### DNS
```bash
# Test DNS resolution
nslookup croody.app
dig croody.app

# Flush DNS cache (Linux)
sudo systemctl flush-dns

# Ver hosts file
cat /etc/hosts
```

### J. Database

#### SQLite
```bash
# Conectar a DB
sqlite3 db.sqlite3

# En sqlite3 shell
.tables
.schema shop_product
SELECT * FROM shop_product LIMIT 5;

# Backup DB
sqlite3 db.sqlite3 ".backup backup.sqlite3"

# Restore DB
sqlite3 new.db < backup.sqlite3

# Export to SQL
sqlite3 db.sqlite3 ".dump" > dump.sql

# Import from SQL
sqlite3 new.db < dump.sql

# SQL queries from command line
sqlite3 db.sqlite3 "SELECT COUNT(*) FROM shop_product;"
```

#### PostgreSQL
```bash
# Conectar
psql -h localhost -U postgres -d croody_db

# En psql shell
\dt  # Listar tablas
\d shop_product  # Describe tabla
\di  # Listar índices

# Backup
pg_dump -h localhost -U postgres croody_db > backup.sql

# Restore
psql -h localhost -U postgres -d new_db < backup.sql

# Query from command line
psql -h localhost -U postgres -d croody_db -c "SELECT COUNT(*) FROM shop_product;"
```

---

## III. Recursos

### A. Documentación Oficial

#### Django & Python
- **Django Documentation**: https://docs.djangoproject.com/en/stable/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Python Documentation**: https://docs.python.org/3/
- **PEP 8 (Python Style Guide)**: https://pep8.org/
- **PEP 484 (Type Hints)**: https://www.python.org/dev/peps/pep-0484/

#### FastAPI & APIs
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Documentation**: https://pydantic-docs.helpmanual.io/
- **OpenAPI Specification**: https://swagger.io/specification/

#### Frontend & UI
- **HTML Living Standard**: https://html.spec.whatwg.org/
- **CSS Specification**: https://www.w3.org/TR/CSS/
- **JavaScript Documentation**: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- **Web Accessibility Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/

#### Internationalization
- **Django i18n**: https://docs.djangoproject.com/en/stable/topics/i18n/
- **Unicode CLDR**: http://cldr.unicode.org/
- **RFC 5646 (Language Tags)**: https://tools.ietf.org/html/rfc5646

#### DevOps & Infrastructure
- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose Documentation**: https://docs.docker.com/compose/
- **GitHub Actions Documentation**: https://docs.github.com/en/actions
- **Terraform Documentation**: https://www.terraform.io/docs/
- **BIND9 Documentation**: https://bind9.readthedocs.io/

#### Testing
- **pytest Documentation**: https://docs.pytest.org/
- **Django Testing**: https://docs.djangoproject.com/en/stable/topics/testing/
- **Playwright Documentation**: https://playwright.dev/
- **Factory Boy Documentation**: https://factoryboy.readthedocs.io/

#### Security
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Django Security**: https://docs.djangoproject.com/en/stable/topics/security/
- **MDN Web Security**: https://developer.mozilla.org/en-US/docs/Web/Security

### B. Herramientas de Desarrollo

#### IDEs & Editors
- **PyCharm**: https://www.jetbrains.com/pycharm/
- **Visual Studio Code**: https://code.visualstudio.com/
- **Vim/Neovim**: https://www.vim.org/

#### Python Tools
- **Black (Code Formatter)**: https://black.readthedocs.io/
- **isort (Import Sorter)**: https://pycqa.github.io/isort/
- **flake8 (Linter)**: https://flake8.pycqa.org/
- **mypy (Type Checker)**: https://mypy.readthedocs.io/
- **pre-commit (Hooks)**: https://pre-commit.com/
- **pipenv (Dependency Manager)**: https://pipenv.pypa.io/

#### Django Tools
- **Django Extensions**: https://django-extensions.readthedocs.io/
- **Django Debug Toolbar**: https://django-debug-toolbar.readthedocs.io/
- **Django Silk (Profiler)**: https://github.com/jazzband/django-silk
- **Django Admin Tools**: https://django-admin-tools.readthedocs.io/

#### API & Testing Tools
- **HTTPie**: https://httpie.io/
- **Postman**: https://www.postman.com/
- **Insomnia**: https://insomnia.rest/

#### Database Tools
- **pgAdmin (PostgreSQL)**: https://www.pgadmin.org/
- **DBeaver**: https://dbeaver.io/
- **SQLite Browser**: https://sqlitebrowser.org/

#### Performance & Monitoring
- **django-silk**: Profiling Django
- **New Relic**: APM
- **Datadog**: Monitoring
- **Prometheus**: Metrics
- **Grafana**: Visualization

### C. Libraries & Frameworks

#### Backend
```python
# Django Ecosystem
Django==3.2+
djangorestframework==3.14+
django-cors-headers==4.0+  # CORS
django-filter==22.1  # Filtering
django-extensions==3.2  # Extensions
django-debug-toolbar==4.0  # Debug
django-crispy-forms==2.0  # Forms
crispy-bootstrap5==0.7  # Bootstrap5

# FastAPI Ecosystem
fastapi==0.100+
uvicorn==0.22+  # ASGI server
pydantic==2.0+  # Data validation
httpx==0.24+  # HTTP client
python-multipart==0.0.6  # Form parsing

# Utilities
python-decouple==3.8  # Environment variables
celery==5.2+  # Task queue
redis==4.5+  # Cache/message broker
psycopg2-binary==2.9+  # PostgreSQL adapter
```

#### Frontend
```html
<!-- CSS Framework (usado en templates) -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- JavaScript -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Icons (opcional) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
```

#### Testing
```python
# Testing Stack
pytest==7.4+
pytest-django==4.5+  # Django integration
pytest-cov==4.1+  # Coverage
pytest-xdist==3.3+  # Parallel tests
pytest-mock==3.11+  # Mocking
pytest-html==3.2+  # HTML reports
factory-boy==3.3+  # Test factories
faker==19.0+  # Fake data
freezegun==1.2+  # Time mocking
responses==4.2+  # HTTP mocking
httpx==0.24+  # Async HTTP testing
```

### D. Learning Resources

#### Django Learning
- **Django Official Tutorial**: https://docs.djangoproject.com/en/stable/intro/tutorial01/
- **Django for Beginners**: https://djangoforbeginners.com/
- **Django Girls Tutorial**: https://tutorial.djangogirls.org/
- **Effective Django**: http://www.effectivedjango.com/

#### FastAPI Learning
- **FastAPI Official Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **FastAPI Best Practices**: https://github.com/zhanymkanov/fastapi-best-practices

#### DevOps Learning
- **Docker Curriculum**: https://docker-curriculum.com/
- **GitHub Actions Tutorial**: https://docs.github.com/en/actions/learn-github-actions
- **Terraform Up & Running**: https://www.terraformupandrunning.com/

#### Security Learning
- **OWASP Django Security**: https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html
- **Django Security Checklist**: https://docs.djangoproject.com/en/stable/topics/security/

#### Testing Learning
- **Testing Django**: https://test-driven-django-development.readthedocs.io/
- **pytest Tutorial**: https://docs.pytest.org/en/latest/getting-started.html

### E. Community & Support

#### Forums & Communities
- **Django Forum**: https://forum.djangoproject.org/
- **Django Subreddit**: https://www.reddit.com/r/django/
- **FastAPI GitHub Discussions**: https://github.com/tiangolo/fastapi/discussions
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/django

#### Conferences & Events
- **DjangoCon**: https://djangocon.us/
- **PyCon**: https://us.pycon.org/
- **Django Europe**: https://djangoweurope.org/

### F. Cheat Sheets

#### Django Quick Reference
```python
# Models
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

# Views
from django.views.generic import ListView, DetailView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'shop/list.html'
    context_object_name = 'products'
    paginate_by = 20

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'

# URLs
from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='detail'),
]
```

#### Docker Quick Reference
```bash
# Essential commands
docker build -t tagname .
docker run -p 8000:8000 tagname
docker-compose up -d
docker-compose down -v
docker exec -it container_name bash

# Cleanup
docker system prune -a
```

#### Git Quick Reference
```bash
# Daily workflow
git status
git add .
git commit -m "message"
git push origin branch-name

# Branching
git checkout -b feature-name
git checkout main
git merge feature-name
git branch -d feature-name
```

### G. Configuration Templates

#### .gitignore for Django
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/staticfiles
staticfiles/
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
```

#### requirements.txt
```txt
# Django
Django==3.2.20
djangorestframework==3.14.0
django-cors-headers==4.2.0
django-filter==23.2

# FastAPI
fastapi==0.103.1
uvicorn==0.23.2
pydantic==2.3.0
httpx==0.24.1

# Database
psycopg2-binary==2.9.7
redis==4.6.0

# Utilities
python-decouple==3.8
celery==5.3.1

# Testing
pytest==7.4.0
pytest-django==4.5.2
pytest-cov==4.1.0
factory-boy==3.3.0
faker==19.3.0
```

#### docker-compose.yml template
```yaml
version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=1
      - SECRET_KEY=dev-secret-key
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: croody
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### H. Troubleshooting Checklists

#### Django Issues
- [ ] ¿DEBUG=True en development?
- [ ] ¿ALLOWED_HOSTS configurado?
- [ ] ¿Migraciones aplicadas?
- [ ] ¿SECRET_KEY configurada?
- [ ] ¿STATIC_URL y STATIC_ROOT correctos?
- [ ] ¿Base de datos existe y es accesible?

#### Docker Issues
- [ ] ¿Puertos no están en uso?
- [ ] ¿Variables de entorno configuradas?
- [ ] ¿Volumes montados correctamente?
- [ ] ¿Ports mapeados (-p 8000:8000)?
- [ ] ¿Context de build correcto?

#### CI/CD Issues
- [ ] ¿Workflow file syntax correcto?
- [ ] ¿Secrets configurados?
- [ ] ¿Runner tiene permisos?
- [ ] ¿Cache configurado?
- [ ] ¿Timeout suficiente?

### I. Best Practices References

#### Code Quality
- **PEP 8**: Python Style Guide
- **Django Coding Style**: https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/
- **Google Python Style Guide**: https://google.github.io/styleguide/pyguide.html
- **Clean Code Principles**: https://www.oreilly.com/library/view/clean-code/9780132350884/

#### Architecture
- **Django Best Practices**: https://docs.djangoproject.com/en/stable/misc/
- **12-Factor App**: https://12factor.net/
- **Microservices Patterns**: https://microservices.io/

#### Security
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Django Security**: https://docs.djangoproject.com/en/stable/topics/security/

---

## Ver También

### Documentos Relacionados
- [Modelos - Arquitectura de datos](../02-BACKEND/modelos.md)
- [Vistas - Lógica de negocio](../02-BACKEND/vistas.md)
- [Patrones de Desarrollo - CBV y Mixins](../08-PATRONES/desarrollo.md)
- [Testing - Estrategias multi-nivel](../09-TESTING/testing-general.md)
- [Troubleshooting - Problemas comunes](../11-TROUBLESHOOTING/guia-problemas-comunes.md)

### Recursos Adicionales
- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Nota**: Este glosario se actualiza continuamente. Para contribuciones o correcciones, consultar la documentación del proyecto en GitHub.
