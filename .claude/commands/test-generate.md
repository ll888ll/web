# Automated Test Generation for Django/FastAPI

You are a test automation expert specializing in generating comprehensive, maintainable tests for Python web applications. Create tests that maximize coverage, catch edge cases, and follow Django/pytest best practices.

## Context

The user needs automated test generation that analyzes code structure, identifies test scenarios, and creates high-quality tests with proper mocking, assertions, and edge case coverage for Django and FastAPI applications.

## Requirements

$ARGUMENTS

## Instructions

### 1. Analyze Code for Test Generation

Scan the specified file(s) to identify testable units:

```python
# Analysis targets
- Django Models: fields, methods, properties, Meta options
- Django Views: GET/POST handling, permissions, context
- Django Forms: validation, clean methods
- FastAPI Endpoints: request/response, status codes, auth
- Service classes: business logic methods
- Utility functions: edge cases, error handling
```

### 2. Generate Django Model Tests

```python
import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal

from shop.models import Product, Order

@pytest.mark.django_db
class TestProductModel:
    """Tests para el modelo Product."""

    @pytest.fixture
    def product(self):
        """Fixture de producto válido."""
        return Product.objects.create(
            name="Test Product",
            slug="test-product",
            price=Decimal("99.99"),
            is_active=True
        )

    def test_product_creation(self, product):
        """Verifica creación básica de producto."""
        assert product.pk is not None
        assert product.name == "Test Product"
        assert product.is_active is True

    def test_product_str_representation(self, product):
        """Verifica __str__ del modelo."""
        assert str(product) == "Test Product"

    def test_product_get_display_price(self, product):
        """Verifica método de formateo de precio."""
        assert product.get_display_price() == "$99.99"

    def test_product_slug_unique(self, product):
        """Verifica constraint de slug único."""
        with pytest.raises(Exception):  # IntegrityError
            Product.objects.create(
                name="Another Product",
                slug="test-product",  # Duplicate
                price=Decimal("50.00")
            )

    def test_product_price_validation(self):
        """Verifica que precio no puede ser negativo."""
        with pytest.raises(ValidationError):
            product = Product(
                name="Invalid",
                slug="invalid",
                price=Decimal("-10.00")
            )
            product.full_clean()
```

### 3. Generate Django View Tests

```python
import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestProductListView:
    """Tests para ProductListView."""

    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def products(self):
        """Crear productos de prueba."""
        from shop.models import Product
        return [
            Product.objects.create(
                name=f"Product {i}",
                slug=f"product-{i}",
                price=Decimal("10.00") * i,
                is_active=True
            )
            for i in range(1, 4)
        ]

    def test_list_view_status_code(self, client, products):
        """Verifica status 200 en listado."""
        url = reverse('shop:product-list')
        response = client.get(url)
        assert response.status_code == 200

    def test_list_view_template_used(self, client, products):
        """Verifica template correcto."""
        url = reverse('shop:product-list')
        response = client.get(url)
        assert 'shop/product_list.html' in [t.name for t in response.templates]

    def test_list_view_context_contains_products(self, client, products):
        """Verifica que context tiene productos."""
        url = reverse('shop:product-list')
        response = client.get(url)
        assert 'products' in response.context
        assert len(response.context['products']) == 3

    def test_list_view_only_active_products(self, client):
        """Verifica que solo muestra productos activos."""
        from shop.models import Product
        Product.objects.create(name="Active", slug="active", price=Decimal("10"), is_active=True)
        Product.objects.create(name="Inactive", slug="inactive", price=Decimal("10"), is_active=False)

        url = reverse('shop:product-list')
        response = client.get(url)
        assert len(response.context['products']) == 1

    def test_list_view_pagination(self, client):
        """Verifica paginación."""
        from shop.models import Product
        for i in range(15):
            Product.objects.create(name=f"P{i}", slug=f"p-{i}", price=Decimal("10"), is_active=True)

        url = reverse('shop:product-list')
        response = client.get(url)
        assert response.context['is_paginated'] is True
        assert len(response.context['products']) == 12  # paginate_by
```

### 4. Generate FastAPI Endpoint Tests

```python
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import Mock, patch

from telemetry_api.main import app

client = TestClient(app)

class TestTelemetryEndpoints:
    """Tests para endpoints de telemetría."""

    def test_create_event_success(self):
        """Verifica creación de evento exitosa."""
        response = client.post(
            "/telemetry/events",
            json={
                "event_type": "page_view",
                "payload": {"page": "/home", "duration": 1500}
            }
        )
        assert response.status_code == 201
        assert response.json()["status"] == "created"

    def test_create_event_missing_type(self):
        """Verifica validación de event_type requerido."""
        response = client.post(
            "/telemetry/events",
            json={"payload": {"page": "/home"}}
        )
        assert response.status_code == 422  # Validation error

    def test_create_event_invalid_json(self):
        """Verifica manejo de JSON inválido."""
        response = client.post(
            "/telemetry/events",
            content="not valid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_get_events_empty(self):
        """Verifica listado vacío."""
        response = client.get("/telemetry/events")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_async_event_processing(self):
        """Test async con httpx."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/telemetry/events",
                json={"event_type": "async_test", "payload": {}}
            )
        assert response.status_code == 201
```

### 5. Generate Form Tests

```python
import pytest
from shop.forms import ProductForm, CheckoutForm

class TestProductForm:
    """Tests para ProductForm."""

    def test_valid_form(self):
        """Verifica form válido."""
        data = {
            'name': 'Test Product',
            'price': '99.99',
            'description': 'A test product'
        }
        form = ProductForm(data=data)
        assert form.is_valid()

    def test_invalid_price_negative(self):
        """Verifica validación de precio negativo."""
        data = {
            'name': 'Test',
            'price': '-10.00'
        }
        form = ProductForm(data=data)
        assert not form.is_valid()
        assert 'price' in form.errors

    def test_name_max_length(self):
        """Verifica límite de caracteres en name."""
        data = {
            'name': 'x' * 300,  # Excede max_length
            'price': '10.00'
        }
        form = ProductForm(data=data)
        assert not form.is_valid()
        assert 'name' in form.errors
```

### 6. Coverage Gap Detection

```python
# Analizar coverage actual
# pytest --cov=shop --cov-report=term-missing

# Identificar líneas sin cobertura
def identify_untested_code():
    """
    Líneas típicamente sin tests:
    - Exception handlers (except blocks)
    - Edge cases en validaciones
    - Métodos de modelo poco usados
    - Código de integración con servicios externos
    """
    pass
```

### 7. Mock Generation for External Services

```python
import pytest
from unittest.mock import Mock, patch, MagicMock

@pytest.fixture
def mock_stripe():
    """Mock para Stripe API."""
    with patch('shop.services.stripe') as mock:
        mock.PaymentIntent.create.return_value = MagicMock(
            id='pi_test_123',
            status='succeeded',
            client_secret='secret_test'
        )
        yield mock

@pytest.fixture
def mock_email_service():
    """Mock para servicio de email."""
    with patch('shop.services.send_mail') as mock:
        mock.return_value = True
        yield mock

@pytest.fixture
def mock_redis():
    """Mock para Redis cache."""
    with patch('django.core.cache.cache') as mock:
        mock.get.return_value = None
        mock.set.return_value = True
        yield mock
```

## Output Format

1. **Test Files**: Complete test suites ready to run
2. **Fixtures**: Reusable pytest fixtures
3. **Mocks**: Mock objects for external dependencies
4. **Coverage Commands**: `pytest --cov` commands
5. **CI Integration**: GitHub Actions snippet if needed

## Conventions for Croody

- **Docstrings**: En español
- **Fixtures**: Usar `@pytest.fixture` sobre `setUp`
- **Markers**: Usar `@pytest.mark.django_db` para tests con DB
- **Naming**: `test_[method]_[scenario]` pattern
- **Factory Boy**: Preferir factories sobre fixtures manuales para modelos complejos

## Example Usage

```bash
# Generar tests para un modelo
/test-generate proyecto_integrado/Croody/shop/models.py

# Generar tests para una vista
/test-generate proyecto_integrado/Croody/shop/views.py

# Generar tests para endpoint FastAPI
/test-generate proyecto_integrado/services/telemetry-gateway/app/routes.py
```

---

Argumento recibido: $ARGUMENTS

Analiza el archivo especificado y genera tests comprehensivos siguiendo los patrones anteriores.
