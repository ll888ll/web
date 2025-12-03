# Testing - Documentación Completa

## Resumen
El sistema de testing de Croody implementa un enfoque multi-nivel con tests unitarios (pytest/Django TestCase), tests de integración (FastAPI TestClient), tests end-to-end (Playwright), y validación automática via GitHub Actions CI. Cubre 100% del código crítico, con patterns específicos para models, views, forms, APIs, señales y middleware.

## Ubicación
- **Django Tests**: Por módulo (`landing/tests/`, `shop/tests/`)
- **API Tests**: `/proyecto_integrado/services/telemetry-gateway/app/test_app.py`, `/proyecto_integrado/services/ids-ml/app/test_ids_app.py`
- **E2E Tests**: `tests/e2e/` (Playwright)
- **CI Integration**: `/.github/workflows/ci.yml`
- **Test Runner**: `scripts/validate_full_stack.sh`

## Pirámide de Testing

### Estrategia Multi-Nivel
```
                    ┌─────────────────────────────────────┐
                    │        E2E Tests (5%)               │
                    │     Playwright, Selenium            │
                    │     - User journeys                 │
                    │     - Full stack validation         │
                    └────────────┬────────────────────────┘
                                 │
                    ┌────────────▼────────────────────────┐
                    │   Integration Tests (20%)           │
                    │   FastAPI TestClient, Django Client │
                    │   - API endpoints                   │
                    │   - DB integration                  │
                    │   - External services               │
                    └────────────┬────────────────────────┘
                                 │
                    ┌────────────▼────────────────────────┐
                    │     Unit Tests (75%)                │
                    │   pytest, Django TestCase          │
                    │   - Models                          │
                    │   - Views (CBV)                     │
                    │   - Forms                           │
                    │   - Utils                           │
                    │   - Signals                         │
                    └─────────────────────────────────────┘
```

## Herramientas de Testing

### Stack Principal
```bash
# Python/Django Testing
pip install pytest pytest-django pytest-cov pytest-xdist
pip install django-test-migrations

# FastAPI Testing
pip install httpx fastapi

# E2E Testing
npm install -D playwright @playwright/test
npx playwright install

# Utilities
pip install factory-boy faker  # Test factories
pip install freezegun          # Time mocking
pip install responses          # HTTP request mocking
```

### Configuración pytest.ini
```ini
# pytest.ini
[tool:pytest]
testpaths = tests proyecto_integrado
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts =
    -v --tb=short
    --strict-markers
    --cov=proyecto_integrado
    --cov-report=term-missing:skip-covered
    --cov-fail-under=80
    --cov-branch
    --reuse-db  # pytest-django
markers =
    slow: marks tests as slow
    integration: marks tests as integration
    e2e: marks tests as end-to-end
    api: marks tests as API tests
```

## Unit Testing

### 1. Model Tests

#### Pattern: Testing Custom QuerySet
```python
# shop/tests/test_models.py
from django.test import TestCase
from shop.models import Product

class ProductQuerySetTest(TestCase):
    """Test custom QuerySet methods."""

    def setUp(self):
        """Crear datos de prueba."""
        self.published = Product.objects.create(
            name="Producto publicado",
            slug="prod-pub",
            price=Decimal("99.99"),
            is_published=True,
        )
        self.unpublished = Product.objects.create(
            name="Producto borrador",
            slug="prod-borr",
            price=Decimal("49.99"),
            is_published=False,
        )

    def test_published_only(self):
        """Test filtro de productos publicados."""
        published = Product.objects.published()
        self.assertEqual(published.count(), 1)
        self.assertEqual(published.first(), self.published)

    def test_search_by_name(self):
        """Test búsqueda por nombre."""
        results = Product.objects.search("publicado")
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first(), self.published)

    def test_search_teaser(self):
        """Test búsqueda por teaser."""
        self.published.teaser = "Producto increíble"
        self.published.save()

        results = Product.objects.search("increíble")
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first(), self.published)

    def test_empty_query(self):
        """Test query vacía retorna todos."""
        results = Product.objects.search("")
        self.assertEqual(results.count(), 2)

    def test_no_match(self):
        """Test query sin coincidencias."""
        results = Product.objects.search("xyz123")
        self.assertEqual(results.count(), 0)
```

#### Pattern: Testing OneToOne Relationships
```python
# landing/tests/test_models.py
from django.contrib.auth import get_user_model
from landing.models import UserProfile

User = get_user_model()

class UserProfileTest(TestCase):
    """Test UserProfile model."""

    def test_profile_created_on_user_creation(self):
        """Test que se crea perfil automáticamente."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com"
        )
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, UserProfile)
        self.assertEqual(user.profile.user, user)

    def test_profile_related_name(self):
        """Test related_name para acceso reverse."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com"
        )
        profile = user.profile
        # Acceso desde profile a user
        self.assertEqual(profile.user, user)
        # Acceso desde user a profile
        self.assertEqual(user.profile, profile)

    def test_profile_token_generation(self):
        """Test generación de token."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com"
        )
        token = user.profile.ingest_token
        self.assertEqual(len(token), 32)  # 16 hex chars * 2
        # Token único por perfil
        self.assertIsNotNone(token)

    def test_token_regeneration(self):
        """Test regeneración de token."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com"
        )
        old_token = user.profile.ingest_token
        user.profile.regenerate_token()
        new_token = user.profile.ingest_token
        self.assertNotEqual(old_token, new_token)
        self.assertEqual(len(new_token), 32)

    def test_str_representation(self):
        """Test __str__ del modelo."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com"
        )
        self.assertIn("testuser", str(user.profile))
        self.assertIn("Perfil", str(user.profile))
```

### 2. Signal Tests

#### Pattern: Testing Django Signals
```python
# landing/tests/test_signals.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from landing.models import UserProfile

User = get_user_model()

class UserProfileSignalTest(TestCase):
    """Test signal handlers."""

    def test_create_user_profile_on_user_creation(self):
        """Test señal post_save crea perfil."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com"
        )
        # Verificar que se creó perfil
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.user, user)

    def test_save_user_profile_on_user_update(self):
        """Test señal post_save actualiza perfil."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com"
        )
        profile = user.profile
        old_display_name = profile.display_name

        # Actualizar usuario
        user.first_name = "Nuevo"
        user.save()

        # Verificar que perfil se guardó
        profile.refresh_from_db()
        # El perfil no cambió porque no tenía cambios específicos
        self.assertEqual(profile.display_name, old_display_name)

    def test_multiple_users_have_separate_profiles(self):
        """Test múltiples usuarios tienen perfiles separados."""
        user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com"
        )
        user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com"
        )

        self.assertNotEqual(user1.profile.id, user2.profile.id)
        self.assertNotEqual(user1.profile.ingest_token, user2.profile.ingest_token)
```

### 3. Form Tests

#### Pattern: Testing Custom Forms
```python
# landing/tests/test_forms.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from landing.forms import CroodySignupForm, CroodyLoginForm, ProfileForm

User = get_user_model()

class CroodySignupFormTest(TestCase):
    """Test formulario de registro."""

    def test_form_fields(self):
        """Test que formulario tiene campos correctos."""
        form = CroodySignupForm()
        required_fields = [
            'full_name', 'email', 'preferred_language',
            'preferred_theme', 'password1', 'password2', 'accept_terms'
        ]
        for field in required_fields:
            self.assertIn(field, form.fields)

    def test_clean_email_duplicate(self):
        """Test validación email duplicado."""
        # Crear usuario existente
        User.objects.create_user(
            username="existing",
            email="test@example.com"
        )

        # Intentar crear usuario con mismo email
        form = CroodySignupForm({
            'full_name': 'Test User',
            'email': 'test@example.com',
            'preferred_language': 'es',
            'preferred_theme': 'system',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'accept_terms': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('Ya existe una cuenta', form.errors['email'][0])

    def test_clean_email_valid(self):
        """Test validación email válido."""
        form = CroodySignupForm({
            'full_name': 'Test User',
            'email': 'test@example.com',
            'preferred_language': 'es',
            'preferred_theme': 'system',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'accept_terms': True,
        })

        self.assertTrue(form.is_valid())

    def test_save_creates_user_and_profile(self):
        """Test save() crea usuario y perfil."""
        form = CroodySignupForm({
            'full_name': 'Test User',
            'email': 'test@example.com',
            'preferred_language': 'es',
            'preferred_theme': 'dark',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'accept_terms': True,
        })

        self.assertTrue(form.is_valid())
        user = form.save()

        # Verificar usuario
        self.assertEqual(user.username, 'test-user')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

        # Verificar perfil
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.preferred_language, 'es')
        self.assertEqual(user.profile.preferred_theme, 'dark')
        self.assertEqual(user.profile.display_name, 'Test User')

    def test_build_username_unique(self):
        """Test generación username único."""
        # Crear usuario existente
        User.objects.create_user(username='test-user', email='test1@example.com')

        # Form con mismo username base
        form = CroodySignupForm({
            'full_name': 'Test User',
            'email': 'test2@example.com',
            'preferred_language': 'es',
            'preferred_theme': 'system',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'accept_terms': True,
        })

        user = form.save()
        # Username con sufijo
        self.assertEqual(user.username, 'test-user-1')

    def test_required_fields(self):
        """Test campos requeridos."""
        form = CroodySignupForm({})
        self.assertFalse(form.is_valid())

        required_errors = {
            'full_name', 'email', 'preferred_language',
            'preferred_theme', 'password1', 'password2', 'accept_terms'
        }
        self.assertEqual(set(form.errors.keys()), required_errors)

class CroodyLoginFormTest(TestCase):
    """Test formulario de login."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='ComplexPass123!'
        )

    def test_login_with_username(self):
        """Test login con username."""
        form = CroodyLoginForm({
            'username': 'testuser',
            'password': 'ComplexPass123!'
        })
        self.assertTrue(form.is_valid())

    def test_login_with_email(self):
        """Test login con email."""
        form = CroodyLoginForm({
            'username': 'test@example.com',
            'password': 'ComplexPass123!'
        })
        self.assertTrue(form.is_valid())
        # Email convertido a username
        self.assertEqual(form.cleaned_data['username'], 'testuser')

    def test_login_email_not_exists(self):
        """Test login con email inexistente."""
        form = CroodyLoginForm({
            'username': 'nonexistent@example.com',
            'password': 'ComplexPass123!'
        })
        # Validación pasa, pero autenticación fallará
        self.assertTrue(form.is_valid())

    def test_invalid_password(self):
        """Test password incorrecto."""
        form = CroodyLoginForm({
            'username': 'testuser',
            'password': 'WrongPassword'
        })
        self.assertTrue(form.is_valid())
        # Autenticación fallará en view
```

### 4. View Tests (CBV)

#### Pattern: Testing Class-Based Views
```python
# landing/tests/test_views.py
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from landing.views import HomeView, ProfileView, CroodySignupView

User = get_user_model()

class HomeViewTest(TestCase):
    """Test HomeView."""

    def test_template_name(self):
        """Test template correcto."""
        request = RequestFactory().get('/')
        view = HomeView()
        view.setup(request)
        self.assertEqual(view.template_name, 'landing/home.html')

    def test_get_context_data(self):
        """Test contexto de datos."""
        request = RequestFactory().get('/')
        view = HomeView()
        view.setup(request)

        context = view.get_context_data()

        # Verificar elementos del contexto
        self.assertIn('hero', context)
        self.assertIn('metrics', context)
        self.assertIn('vectors', context)
        self.assertIn('buddy_products', context)
        self.assertIn('nav_links', context)
        self.assertTrue(context['show_global_shortcuts'])

    def test_hero_structure(self):
        """Test estructura del hero."""
        request = RequestFactory().get('/')
        view = HomeView()
        view.setup(request)
        context = view.get_context_data()
        hero = context['hero']

        # Verificar campos del hero
        self.assertIn('eyebrow', hero)
        self.assertIn('title', hero)
        self.assertIn('lead', hero)
        self.assertIn('primary_cta', hero)
        self.assertIn('secondary_cta', hero)
        self.assertIn('tertiary_cta', hero)
        self.assertIn('image', hero)

        # Verificar CTA
        self.assertIn('label', hero['primary_cta'])
        self.assertIn('url', hero['primary_cta'])

    def test_buddy_products_from_db(self):
        """Test productos desde base de datos."""
        # Crear productos
        Product.objects.create(
            name="Test Product",
            slug="test-product",
            price=Decimal("99.99"),
            is_published=True,
        )

        request = RequestFactory().get('/')
        view = HomeView()
        view.setup(request)
        context = view.get_context_data()

        # Verificar productos
        self.assertGreater(len(context['buddy_products']), 0)

    def test_buddy_products_fallback(self):
        """Test productos por defecto cuando no hay DB."""
        request = RequestFactory().get('/')
        view = HomeView()
        view.setup(request)
        context = view.get_context_data()

        # Verificar que hay productos (fallback)
        self.assertGreater(len(context['buddy_products']), 0)

class ProfileViewTest(TestCase):
    """Test ProfileView (LoginRequired)."""

    def test_login_required(self):
        """Test que vista requiere login."""
        # Sin autenticación
        response = self.client.get('/perfil/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_view_authenticated(self):
        """Test vista con usuario autenticado."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        self.client.force_login(user)

        response = self.client.get('/perfil/')
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        """Test contexto incluye formularios."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        self.client.force_login(user)

        response = self.client.get('/perfil/')
        context = response.context

        self.assertIn('profile_form', context)
        self.assertIn('preferences_form', context)
        self.assertIn('token_form', context)
        self.assertIn('ingest_token', context)

    def test_post_profile_form(self):
        """Test actualización perfil."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Old'
        )
        self.client.force_login(user)

        response = self.client.post('/perfil/', {
            'form': 'profile',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'test@example.com'
        })

        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'New')

    def test_post_token_reset(self):
        """Test regeneración token."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        old_token = user.profile.ingest_token
        self.client.force_login(user)

        response = self.client.post('/perfil/', {
            'form': 'token'
        })

        self.assertEqual(response.status_code, 200)
        user.profile.refresh_from_db()
        self.assertNotEqual(user.profile.ingest_token, old_token)

class CroodySignupViewTest(TestCase):
    """Test vista de registro."""

    def test_get_success_url(self):
        """Test URL de éxito."""
        request = RequestFactory().get('/signup/')
        view = CroodySignupView()
        view.setup(request)
        self.assertEqual(view.get_success_url(), reverse('landing:profile'))

    def test_form_valid(self):
        """Test formulario válido."""
        request = RequestFactory().post('/signup/', {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'preferred_language': 'es',
            'preferred_theme': 'system',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'accept_terms': True,
        })

        view = CroodySignupView()
        view.setup(request)

        form = CroodySignupForm(request.POST)
        self.assertTrue(form.is_valid())

        response = view.form_valid(form)
        # Redirige a profile
        self.assertEqual(response.status_code, 302)
```

### 5. Model Factory Pattern

#### Pattern: Using Factory Boy
```python
# tests/factories.py
import factory
from django.contrib.auth import get_user_model
from shop.models import Product

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'landing.UserProfile'

    user = factory.SubFactory(UserFactory)
    display_name = factory.LazyAttribute(lambda obj: f'{obj.user.first_name} {obj.user.last_name}')
    preferred_language = 'es'
    preferred_theme = 'system'

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(' ', '-'))
    teaser = factory.Faker('sentence')
    description = factory.Faker('text')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    delivery_estimate = 'Entrega 3 días'
    badge_label = factory.Faker('word')
    is_published = True
    sort_order = 0

# Uso en tests
class ProductQuerySetTest(TestCase):
    def setUp(self):
        # En lugar de create manual
        self.published = ProductFactory(is_published=True)
        self.unpublished = ProductFactory(is_published=False)

    def test_published_only(self):
        published = Product.objects.published()
        self.assertEqual(published.count(), 1)
        self.assertEqual(published.first(), self.published)
```

## Integration Testing

### 1. FastAPI Service Tests

#### Pattern: Dynamic Module Loading
```python
# services/telemetry-gateway/app/test_app.py
from pathlib import Path
import importlib.util

from fastapi.testclient import TestClient

# Cargar módulo dinámicamente (sin instalación)
_MAIN = Path(__file__).with_name("main.py")
spec = importlib.util.spec_from_file_location("tg_main", _MAIN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
app = mod.app

# Rebuild Pydantic models si es necesario
if hasattr(mod, "TelemetryIn"):
    try:
        mod.TelemetryIn.model_rebuild()
        mod.TelemetryOut.model_rebuild()
    except Exception:
        pass

# Inicializar DB si es necesario
if hasattr(mod, "init_db"):
    mod.init_db()

# Cliente de test
client = TestClient(app)

def test_healthz():
    """Test health check endpoint."""
    r = client.get("/healthz")
    assert r.status_code == 200

def test_ingest_and_last_with_robot_filter():
    """Test ingest → last con filtro robot."""
    # Enviar datos
    payload = sample_payload("robot-alpha")
    r = client.post("/api/telemetry/ingest", json=payload)
    assert r.status_code in (200, 201)

    # Consultar últimos datos
    latest = client.get("/api/telemetry/last", params={"robot_id": "robot-alpha"})
    assert latest.status_code == 200
    body = latest.json()
    assert body["robot_id"] == "robot-alpha"
    assert body["position"]["lat"] == 19.4326

def sample_payload(robot: str = "robot-alpha") -> dict:
    """Genera payload de prueba."""
    return {
        "robot_id": robot,
        "data": {
            "TEMP": 22.2,
            "HUM": 40.0,
            "LAT": 19.4326,
            "LON": -99.1332,
        },
        "position": {"lat": 19.4326, "lng": -99.1332},
        "environment": "lab",
        "status": "idle",
    }

def test_live_endpoint_groups_by_robot():
    """Test endpoint live agrupa por robot."""
    # Enviar datos de múltiples robots
    client.post("/api/telemetry/ingest", json=sample_payload("robot-alpha"))
    client.post("/api/telemetry/ingest", json=sample_payload("robot-beta"))

    # Consultar live
    resp = client.get("/api/telemetry/live", params={"limit_per_robot": 5})
    assert resp.status_code == 200
    payload = resp.json()

    # Verificar múltiples robots
    assert payload["robots"]
    assert any(robot["robot_id"] == "robot-alpha" for robot in payload["robots"])
    assert any(robot["robot_id"] == "robot-beta" for robot in payload["robots"])

def test_live_empty_state():
    """Test endpoint live sin datos."""
    resp = client.get("/api/telemetry/live")
    assert resp.status_code == 200
    payload = resp.json()
    assert "robots" in payload
    assert len(payload["robots"]) == 0
```

#### Pattern: IDS Service Testing
```python
# services/ids-ml/app/test_ids_app.py
from fastapi.testclient import TestClient
import importlib.util
from pathlib import Path

# Cargar módulo dinámicamente
_MAIN = Path(__file__).with_name("main.py")
spec = importlib.util.spec_from_file_location("ids_main", _MAIN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
app = mod.app

client = TestClient(app)

def test_healthz():
    """Test health check."""
    r = client.get("/healthz")
    assert r.status_code == 200

def test_predict_fallback():
    """Test predict con datos mínimos (fallback)."""
    r = client.post("/api/ids/predict", json={"rows": [{"src_bytes": 1}]})
    assert r.status_code == 200
    body = r.json()
    assert "predictions" in body

def test_predict_with_full_data():
    """Test predict con datos completos."""
    payload = {
        "rows": [
            {
                "src_bytes": 1000,
                "dst_bytes": 500,
                "src_port": 12345,
                "dst_port": 80,
                "protocol": 6,  # TCP
                "duration": 10.5,
                "src_packets": 10,
                "dst_packets": 8,
            }
        ]
    }
    r = client.post("/api/ids/predict", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "predictions" in body
    assert len(body["predictions"]) == 1

def test_predict_invalid_data():
    """Test predict con datos inválidos."""
    r = client.post("/api/ids/predict", json={"rows": [{"invalid": "data"}]})
    assert r.status_code == 422  # Validation error
```

### 2. Database Integration Tests

#### Pattern: Testing with Real Database
```python
# tests/integration/test_db_queries.py
from django.test import TestCase, TransactionTestCase
from django.db import connection
from shop.models import Product

class ProductIntegrationTest(TransactionTestCase):
    """Test integration con DB real."""

    def setUpTestData(self):
        """Datos compartidos para todos los tests."""
        # Esto se ejecuta una vez por TestCase
        self.products = [
            Product.objects.create(
                name=f"Producto {i}",
                slug=f"producto-{i}",
                price=Decimal(f"{i * 10}.00"),
                is_published=True
            )
            for i in range(1, 6)
        ]

    def test_bulk_create(self):
        """Test creación masiva."""
        Product.objects.bulk_create([
            Product(name="Bulk 1", slug="bulk-1", price=Decimal("10.00"), is_published=True),
            Product(name="Bulk 2", slug="bulk-2", price=Decimal("20.00"), is_published=True),
        ])
        self.assertEqual(Product.objects.count(), 7)  # 5 de setUp + 2 nuevos

    def test_update_query(self):
        """Test actualización masiva."""
        updated = Product.objects.filter(price__lt=Decimal("30.00")).update(is_published=False)
        self.assertEqual(updated, 3)  # Productos 1, 2, 3

    def test_annotate_query(self):
        """Test query con annotate."""
        from django.db.models import Count
        products = Product.objects.annotate(
            order_count=Count('id')  # Placeholder
        ).filter(is_published=True)

        self.assertEqual(products.count(), 5)

    def test_raw_query(self):
        """Test raw SQL query."""
        products = Product.objects.raw("SELECT * FROM shop_product WHERE price > %s", [25.00])
        product_list = list(products)
        self.assertEqual(len(product_list), 2)  # Productos 3, 4, 5 (> 25)
```

### 3. External Service Integration

#### Pattern: Mocking External APIs
```python
# tests/integration/test_external_api.py
import responses
from django.test import TestCase
from django.conf import settings

class ExternalAPITest(TestCase):
    """Test integración con servicios externos."""

    @responses.activate
    def test_captcha_verification(self):
        """Test verificación de captcha."""
        # Mock response de servicio externo
        responses.add(
            responses.POST,
            "https://www.google.com/recaptcha/api/siteverify",
            json={"success": True, "challenge_ts": "timestamp"},
            status=200
        )

        # Hacer petición
        import requests
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': 'test-token'
            }
        )

        self.assertEqual(response.json()["success"], True)

    @responses.activate
    def test_email_service(self):
        """Test servicio de email."""
        # Mock email provider
        responses.add(
            responses.POST,
            "https://api.sendgrid.com/v3/mail/send",
            json={},
            status=202
        )

        # Enviar email (código de la app)
        send_email(
            to='test@example.com',
            subject='Test',
            body='Test email'
        )

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, "https://api.sendgrid.com/v3/mail/send")
```

## End-to-End (E2E) Testing

### 1. Playwright Configuration

#### Pattern: Playwright Config
```javascript
// playwright.config.js
/** @type {import('@playwright/test').PlaywrightTestConfig} */
const config = {
  testDir: './tests/e2e',
  timeout: 30 * 1000,
  expect: {
    timeout: 5000
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', { outputFile: 'results.json' }],
    ['junit', { outputFile: 'results.xml' }]
  ],
  use: {
    actionTimeout: 0,
    trace: 'on-first-retry',
    baseURL: 'http://localhost:8000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
  webServer: {
    command: 'cd proyecto_integrado && python manage.py runserver',
    port: 8000,
    reuseExistingServer: !process.env.CI,
  },
};

module.exports = config;
```

### 2. Page Object Model

#### Pattern: POM for Django Templates
```javascript
// tests/e2e/pages/ProductPage.js
const { expect } = require('@playwright/test');

class ProductPage {
  constructor(page) {
    this.page = page;
    this.nameSelector = '[data-testid="product-name"]';
    this.priceSelector = '[data-testid="product-price"]';
    this.addToCartButton = '[data-testid="add-to-cart"]';
    this.quantityInput = '[data-testid="quantity"]';
  }

  async navigateToProduct(slug) {
    await this.page.goto(`/tienda/${slug}/`);
  }

  async getProductName() {
    return await this.page.textContent(this.nameSelector);
  }

  async getProductPrice() {
    return await this.page.textContent(this.priceSelector);
  }

  async addToCart(quantity = 1) {
    if (quantity > 1) {
      await this.page.fill(this.quantityInput, quantity.toString());
    }
    await this.page.click(this.addToCartButton);
  }

  async shouldBeOnProductPage(slug) {
    await expect(this.page).toHaveURL(new RegExp(`/tienda/${slug}/`));
  }

  async shouldShowSuccessMessage() {
    await expect(this.page.locator('[data-testid="success-message"]')).toBeVisible();
  }
}

module.exports = ProductPage;
```

#### Pattern: Test Suite
```javascript
// tests/e2e/tests/shop.spec.js
const { test, expect } = require('@playwright/test');
const ProductPage = require('../pages/ProductPage');

test.describe('Shop Flow', () => {
  test('should view product list', async ({ page }) => {
    await page.goto('/tienda/');

    // Verificar productos visibles
    await expect(page.locator('[data-testid="product-list"]')).toBeVisible();
    await expect(page.locator('[data-testid="product-item"]').first()).toBeVisible();
  });

  test('should view product detail', async ({ page }) => {
    const productPage = new ProductPage(page);
    await productPage.navigateToProduct('buddy-starter');

    // Verificar elementos del producto
    await expect(page.locator('[data-testid="product-name"]')).toBeVisible();
    await expect(page.locator('[data-testid="product-price"]')).toBeVisible();
    await expect(page.locator('[data-testid="product-description"]')).toBeVisible();
  });

  test('should add product to cart', async ({ page }) => {
    const productPage = new ProductPage(page);
    await productPage.navigateToProduct('buddy-starter');

    await productPage.addToCart(2);
    await productPage.shouldShowSuccessMessage();
  });

  test('should search products', async ({ page }) => {
    await page.goto('/tienda/');

    // Buscar producto
    await page.fill('[data-testid="search-input"]', 'buddy');
    await page.press('[data-testid="search-input"]', 'Enter');

    // Verificar resultados
    await expect(page.locator('[data-testid="search-results"]')).toBeVisible();
    await expect(page.locator('[data-testid="product-item"]').first()).toBeVisible();
  });
});
```

### 3. Authentication Flow Testing

#### Pattern: Login/E2E Tests
```javascript
// tests/e2e/tests/auth.spec.js
const { test, expect } = require('@playwright/test');

test.describe('Authentication', () => {
  test('should register new user', async ({ page }) => {
    await page.goto('/registro/');

    // Llenar formulario
    await page.fill('[name="full_name"]', 'Test User');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password1"]', 'ComplexPass123!');
    await page.fill('[name="password2"]', 'ComplexPass123!');
    await page.check('[name="accept_terms"]');

    // Enviar
    await page.click('[type="submit"]');

    // Verificar redirect a perfil
    await expect(page).toHaveURL('/perfil/');
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
  });

  test('should login existing user', async ({ page }) => {
    // Crear usuario en DB (fixture o factory)
    await createTestUser();

    await page.goto('/login/');

    // Llenar login
    await page.fill('[name="username"]', 'testuser');
    await page.fill('[name="password"]', 'ComplexPass123!');
    await page.click('[type="submit"]');

    // Verificar autenticado
    await expect(page).toHaveURL('/perfil/');
    await expect(page.locator('[data-testid="profile-form"]')).toBeVisible();
  });

  test('should logout', async ({ page }) => {
    // Login primero
    await loginAsTestUser(page);

    // Ir a perfil
    await page.goto('/perfil/');

    // Logout
    await page.click('[data-testid="logout-button"]');

    // Verificar redirect
    await expect(page).toHaveURL('/');
    await expect(page.locator('[data-testid="login-link"]')).toBeVisible();
  });
});
```

### 4. Theme Toggle E2E

#### Pattern: Testing JavaScript Features
```javascript
// tests/e2e/tests/theme.spec.js
const { test, expect } = require('@playwright/test');

test.describe('Theme Toggle', () => {
  test('should toggle theme', async ({ page }) => {
    await page.goto('/');

    // Verificar tema por defecto (system)
    const html = page.locator('html');
    await expect(html).toHaveAttribute('data-theme', 'system');

    // Hacer clic en toggle
    await page.click('[data-testid="theme-toggle"]');

    // Verificar cambio a dark
    await expect(html).toHaveAttribute('data-theme', 'dark');

    // Toggle otra vez
    await page.click('[data-testid="theme-toggle"]');

    // Verificar cambio a light
    await expect(html).toHaveAttribute('data-theme', 'light');
  });

  test('should persist theme in localStorage', async ({ page }) => {
    await page.goto('/');

    // Cambiar a dark
    await page.click('[data-testid="theme-toggle"]');
    await page.click('[data-testid="theme-toggle"]'); // dark

    // Verificar localStorage
    const theme = await page.evaluate(() => localStorage.getItem('theme'));
    expect(theme).toBe('dark');

    // Recargar página
    await page.reload();

    // Verificar que tema se mantuvo
    const html = page.locator('html');
    await expect(html).toHaveAttribute('data-theme', 'dark');
  });
});
```

### 5. Language Selector E2E

#### Pattern: Testing i18n in Browser
```javascript
// tests/e2e/tests/language.spec.js
const { test, expect } = require('@playwright/test');

test.describe('Language Selector', () => {
  test('should change language', async ({ page }) => {
    await page.goto('/');

    // Verificar texto en español por defecto
    await expect(page.locator('h1')).toContainText('Croody');

    // Cambiar idioma a inglés
    await page.click('[data-testid="language-selector"]');
    await page.click('[data-value="en"]');

    // Verificar cambio
    await expect(page.locator('h1')).toContainText('Croody');

    // Verificar lang attribute
    const html = page.locator('html');
    await expect(html).toHaveAttribute('lang', 'en');

    // Verificar URLs con prefijo
    await expect(page).toHaveURL(/\/en\//);
  });

  test('should switch language on product page', async ({ page }) => {
    await page.goto('/tienda/');

    // Cambiar a inglés
    await page.click('[data-testid="language-selector"]');
    await page.click('[data-value="en"]');

    // Ir a producto
    await page.click('[data-testid="product-item"]');

    // Verificar URL con /en/
    await expect(page).toHaveURL(/\/en\/tienda\/.+/);
  });
});
```

## API Testing

### 1. REST API Tests

#### Pattern: Testing REST Endpoints
```python
# tests/api/test_telemetry.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from telemetry.models import TelemetryData

User = get_user_model()

class TelemetryAPITest(APITestCase):
    """Test REST API endpoints."""

    def setUp(self):
        """Crear usuario y token."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_ingest_telemetry(self):
        """Test endpoint ingest."""
        data = {
            'robot_id': 'robot-alpha',
            'data': {
                'TEMP': 22.5,
                'HUM': 45.0,
                'LAT': 19.4326,
                'LON': -99.1332,
            },
            'position': {'lat': 19.4326, 'lng': -99.1332},
            'environment': 'lab',
            'status': 'idle',
        }

        response = self.client.post('/api/telemetry/ingest/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verificar en DB
        self.assertTrue(
            TelemetryData.objects.filter(robot_id='robot-alpha').exists()
        )

    def test_last_telemetry(self):
        """Test endpoint last."""
        # Crear datos
        TelemetryData.objects.create(
            robot_id='robot-alpha',
            data={'TEMP': 20.0}
        )

        response = self.client.get('/api/telemetry/last/?robot_id=robot-alpha')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['robot_id'], 'robot-alpha')

    def test_live_telemetry(self):
        """Test endpoint live."""
        # Crear datos de múltiples robots
        TelemetryData.objects.create(robot_id='robot-alpha', data={'TEMP': 20.0})
        TelemetryData.objects.create(robot_id='robot-beta', data={'TEMP': 22.0})

        response = self.client.get('/api/telemetry/live/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('robots', response.data)

    def test_query_telemetry(self):
        """Test endpoint query con filtros."""
        # Crear datos con timestamp
        TelemetryData.objects.create(
            robot_id='robot-alpha',
            data={'TEMP': 20.0},
            timestamp=datetime.now() - timedelta(hours=2)
        )
        TelemetryData.objects.create(
            robot_id='robot-alpha',
            data={'TEMP': 25.0},
            timestamp=datetime.now()
        )

        response = self.client.get('/api/telemetry/query/?robot_id=robot-alpha')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 2)
```

### 2. Authentication Tests

#### Pattern: Testing Token Authentication
```python
# tests/api/test_auth.py
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthAPITest(APITestCase):
    """Test authentication endpoints."""

    def test_token_obtain(self):
        """Test obtener token."""
        user = User.objects.create_user(
            username='testuser',
            password='ComplexPass123!'
        )

        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'ComplexPass123!'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

        # Verificar que token existe en DB
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_token_refresh(self):
        """Test refresh token."""
        user = User.objects.create_user(
            username='testuser',
            password='ComplexPass123!'
        )
        token = Token.objects.create(user=user)

        response = self.client.post('/api/token/refresh/', {
            'token': token.key
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_unauthorized_access(self):
        """Test acceso sin token."""
        response = self.client.get('/api/telemetry/ingest/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token(self):
        """Test token inválido."""
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        response = self.client.get('/api/telemetry/last/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

## Performance Testing

### 1. Load Testing

#### Pattern: Using Locust
```python
# tests/performance/test_load.py
from locust import HttpUser, task, between

class CroodyUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Login al iniciar."""
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.json()['token']

    @task(3)
    def view_home(self):
        """Visitar home."""
        self.client.get('/')

    @task(2)
    def view_product_list(self):
        """Ver lista de productos."""
        self.client.get('/tienda/')

    @task(1)
    def view_product_detail(self):
        """Ver detalle de producto."""
        self.client.get('/tienda/buddy-starter/')

    @task(1)
    def api_health(self):
        """Health check API."""
        self.client.get('/api/telemetry/healthz/')

# Ejecutar
# locust -f tests/performance/test_load.py --host=http://localhost:8000
```

### 2. Query Performance

#### Pattern: Testing N+1 Queries
```python
# tests/performance/test_queries.py
from django.test import TestCase
from django.db import connection
from django.test.utils import override_settings

class QueryPerformanceTest(TestCase):
    """Test performance de queries."""

    def assertNumQueries(self, num, func=None, *args, **kwargs):
        """Override para logging."""
        result = super().assertNumQueries(num, func, *args, **kwargs)
        if func and num > 5:  # Log si hay más de 5 queries
            print(f"\nQuery count: {num}")
            for query in connection.queries:
                print(f"  {query['sql'][:100]}...")
        return result

    def test_product_list_no_n_plus_one(self):
        """Test que no hay N+1 en lista de productos."""
        # Crear productos con categorías
        for i in range(10):
            create_product_with_category(f'Product {i}')

        with self.assertNumQueries(2):  # 1 para productos, 1 para categorías
            products = Product.objects.select_related('category').all()
            list(products)  # Forzar evaluación

    def test_user_profile_efficient(self):
        """Test query eficiente para perfil de usuario."""
        user = User.objects.create_user(username='testuser')

        with self.assertNumQueries(1):  # Solo una query con select_related
            profile = User.objects.select_related('profile').get(id=user.id)
            _ = profile.profile.display_name  # Usar datos
```

## Coverage & Reporting

### 1. Coverage Configuration

#### Pattern: Coverage Settings
```ini
# .coveragerc
[run]
source = proyecto_integrado
omit =
    */tests/*
    */migrations/*
    */venv/*
    */settings/*
    */wsgi.py
    */asgi.py
    */manage.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov
```

#### Pattern: Generate Coverage Report
```bash
#!/bin/bash
# scripts/test-coverage.sh

set -e

echo "Running tests with coverage..."

# Instalar dependencias de test
pip install -q pytest pytest-django pytest-cov

# Ejecutar tests
pytest proyecto_integrado \
    --cov=proyecto_integrado \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml \
    --cov-fail-under=80 \
    -v

echo "Coverage report generated at htmlcov/index.html"
```

### 2. Test Organization

#### Pattern: Directory Structure
```
tests/
├── __init__.py
├── conftest.py                  # Fixtures globales
├── factories/                   # Test factories
│   ├── __init__.py
│   ├── user.py
│   └── product.py
├── unit/                        # Unit tests
│   ├── __init__.py
│   ├── test_models/
│   │   ├── __init__.py
│   │   ├── test_product.py
│   │   └── test_user_profile.py
│   ├── test_views/
│   │   ├── __init__.py
│   │   ├── test_landing.py
│   │   └── test_shop.py
│   └── test_forms/
│       ├── __init__.py
│       └── test_auth_forms.py
├── integration/                 # Integration tests
│   ├── __init__.py
│   ├── test_db_queries.py
│   └── test_external_api.py
├── api/                         # API tests
│   ├── __init__.py
│   ├── test_telemetry_api.py
│   └── test_auth_api.py
└── e2e/                        # End-to-end tests
    ├── __init__.py
    ├── pages/
    │   ├── __init__.py
    │   └── base.py
    └── tests/
        ├── __init__.py
        ├── test_auth.py
        └── test_shop_flow.py
```

### 3. Global Fixtures

#### Pattern: conftest.py
```python
# tests/conftest.py
import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from shop.models import Product

User = get_user_model()

@pytest.fixture
def user():
    """Crear usuario de prueba."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='ComplexPass123!'
    )

@pytest.fixture
def authenticated_client(client, user):
    """Client autenticado."""
    client.force_login(user)
    return client

@pytest.fixture
def product():
    """Crear producto de prueba."""
    return Product.objects.create(
        name='Test Product',
        slug='test-product',
        price=Decimal('99.99'),
        is_published=True
    )

@pytest.fixture
def request_factory():
    """RequestFactory fixture."""
    return RequestFactory()

@pytest.fixture
def api_client():
    """Client para API tests."""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture(autouse=True)
def reset_country():
    """Reset override settings después de cada test."""
    yield
    from django.conf import settings
    settings.COUNTRY_OVERRIDE = None

# Parametrized fixture
@pytest.fixture(params=[
    ('es', 'Español'),
    ('en', 'English'),
    ('fr', 'Français'),
])
def supported_language(request):
    """Idiomas soportados para tests."""
    return request.param
```

## Continuous Integration

### 1. GitHub Actions Integration

#### Pattern: CI Test Workflow
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: croody_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -q -r requirements.txt
          pip install -q -r requirements-test.txt

      - name: Run migrations
        run: |
          cd proyecto_integrado
          python manage.py migrate --settings=croody.settings.test
          python manage.py collectstatic --noinput

      - name: Run unit tests
        run: |
          cd proyecto_integrado
          pytest ../tests/unit/ -v --cov=. --cov-report=xml

      - name: Run integration tests
        run: |
          cd proyecto_integrado
          pytest ../tests/integration/ -v

      - name: Run API tests
        run: |
          cd proyecto_integrado/services/telemetry-gateway/app
          pytest test_app.py -v

      - name: Run E2E tests
        run: |
          cd proyecto_integrado
          docker-compose up -d
          sleep 10
          cd ../../tests/e2e
          npx playwright install --with-deps
          npx playwright test
          cd ../../proyecto_integrado
          docker-compose down

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./proyecto_integrado/coverage.xml
```

### 2. Pre-commit Hooks

#### Pattern: Pre-commit Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        types: [python]
        args: [tests/]
        pass_filenames: false
        always_run: true
```

## Testing Best Practices

### ✅ Hacer

#### 1. Usar Descriptive Test Names
```python
def test_published_queryset_excludes_unpublished_products():
    """Test que QuerySet published excluye productos no publicados."""
    pass
```

#### 2. Arrange-Act-Assert Pattern
```python
def test_user_profile_creation():
    # Arrange
    user = User.objects.create_user(username='test')

    # Act
    profile = user.profile

    # Assert
    assert profile.user == user
```

#### 3. Test One Thing per Test
```python
def test_product_name_required():
    """Test que name es requerido."""
    with pytest.raises(ValidationError):
        Product.objects.create(name='', slug='test', price=Decimal('10.00'))
```

#### 4. Use Fixtures for Setup
```python
@pytest.fixture
def published_product():
    return Product.objects.create(
        name='Test',
        slug='test',
        price=Decimal('10.00'),
        is_published=True
    )

def test_product_list(published_product):
    assert Product.objects.published().count() == 1
```

#### 5. Mock External Dependencies
```python
@patch('requests.post')
def test_send_email(mock_post):
    mock_post.return_value.json.return_value = {'status': 'sent'}
    send_email('test@example.com', 'Subject', 'Body')
    mock_post.assert_called_once()
```

#### 6. Test Edge Cases
```python
def test_search_empty_query():
    """Test búsqueda con query vacía."""
    results = Product.objects.search('')
    assert results.count() == Product.objects.count()
```

#### 7. Use Database Transactions for Performance
```python
from django.test import TransactionTestCase

class BulkCreateTest(TransactionTestCase):
    """Test creación masiva (más rápido que TestCase)."""
    def test_bulk_create(self):
        Product.objects.bulk_create([...])
```

### ❌ Evitar

#### 1. No Testing Implementation Details
```python
# ❌ Mal
def test_profile_has_ingest_token():
    profile = UserProfile()
    assert hasattr(profile, 'ingest_token')  # Testing implementation

# ✅ Bien
def test_profile_generates_unique_token():
    user = User.objects.create_user(username='test')
    assert len(user.profile.ingest_token) == 32
    assert user.profile.ingest_token.isalnum()
```

#### 2. No Brittle Tests
```python
# ❌ Mal - Brittle test
def test_home_page_contains_exact_text():
    response = client.get('/')
    assert 'Croody' in response.content.decode()

# ✅ Bien - Less brittle
def test_home_page_has_title():
    response = client.get('/')
    assert response.context['page_title'] is not None
```

#### 3. No Network Calls in Unit Tests
```python
# ❌ Mal
def test_send_email():
    send_email('test@example.com', 'Subject', 'Body')  # Real network call

# ✅ Bien
@patch('email_service.send')
def test_send_email(mock_send):
    send_email('test@example.com', 'Subject', 'Body')
    mock_send.assert_called_once()
```

#### 4. No Database in Unit Tests
```python
# ❌ Mal
class ProductModelTest(TestCase):
    def test_something(self):
        # Using DB
        Product.objects.create(...)

# ✅ Bien (para tests unitarios puros)
from django.test import TestCase
from shop.models import Product

class ProductModelTest(TestCase):
    # Con DB (integration test)
    pass

# Para unit tests puros:
def test_product_str():
    product = Product(name='Test')
    assert str(product) == 'Test'
```

## Debugging Tests

### 1. Verbose Output
```bash
# Tests con output detallado
pytest -v --tb=long

# Tests con print statements
pytest -s

# Tests con coverage detallado
pytest --cov=proyecto_integrado --cov-report=term-missing --cov-report=html
```

### 2. Interactive Debugging
```python
def test_something():
    import pdb; pdb.set_trace()  # Breakpoint
    # O
    from ipdb import set_trace; set_trace()  # Mejor debugger
```

### 3. Test Selection
```bash
# Solo tests de un módulo
pytest tests/unit/test_models/

# Solo un test específico
pytest tests/unit/test_models.py::test_product_published

# Tests con marker
pytest -m "not slow"

# Tests que fallen
pytest --lf  # Last failed
```

## Common Patterns

### 1. Factory Pattern
```python
# Usar factory-boy para datos de test
from tests.factories import ProductFactory

def test_product_list():
    products = ProductFactory.create_batch(5)
    assert Product.objects.count() == 5
```

### 2. Mock Pattern
```python
from unittest.mock import patch, MagicMock

@patch('module.external_service')
def test_external_call(mock_service):
    mock_service.return_value = {'result': 'success'}
    result = call_external_service()
    assert result['result'] == 'success'
```

### 3. Parameterized Tests
```python
import pytest

@pytest.mark.parametrize('theme', ['system', 'dark', 'light'])
def test_theme_choices(theme):
    user = UserFactory()
    profile = UserProfileFactory(user=user, preferred_theme=theme)
    assert profile.preferred_theme == theme
```

### 4. Database Cleanup
```python
# En pytest-django
@pytest.mark.django_db
def test_with_db():
    # DB se limpia automáticamente
    pass

# En TestCase
class MyTest(TestCase):
    def test_something(self):
        # DB se limpia automáticamente
        pass
```

## Referencias

### Archivos Relacionados
- `services/telemetry-gateway/app/test_app.py` - FastAPI tests con TestClient
- `services/ids-ml/app/test_ids_app.py` - IDS ML service tests
- `tests/unit/` - Unit tests
- `tests/integration/` - Integration tests
- `tests/e2e/` - End-to-end tests

### Herramientas
- [pytest](https://docs.pytest.org/) - Test framework
- [pytest-django](https://pytest-django.readthedocs.io/) - Django integration
- [Playwright](https://playwright.dev/) - E2E testing
- [Factory Boy](https://factoryboy.readthedocs.io/) - Test factories
- [Coverage.py](https://coverage.readthedocs.io/) - Code coverage

### Documentación Externa
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

## Ver También
- [Patrones de Desarrollo](../08-PATRONES/desarrollo.md)
- [CI/CD Workflows](../04-DEVOPS/ci-cd-workflows.md)
