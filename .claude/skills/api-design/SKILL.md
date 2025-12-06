---
name: api-design
description: Expert patterns for designing RESTful APIs with FastAPI and Django REST Framework. Use when creating endpoints, designing API contracts, implementing authentication, or optimizing API performance.
---

# API Design Patterns para Croody Web

Patrones expertos para diseño de APIs RESTful con FastAPI y Django.

## Cuándo Usar Este Skill

- Diseñando nuevos endpoints para microservicios
- Creando contratos de API (OpenAPI/Swagger)
- Implementando autenticación y autorización
- Optimizando performance de APIs
- Documentando APIs existentes
- Versionando APIs

## Arquitectura de APIs en Croody

```
┌─────────────────┐     ┌──────────────┐     ┌────────────────┐
│     Gateway     │────▶│   Django     │────▶│   PostgreSQL   │
│     (nginx)     │     │   (8000)     │     │                │
│     :80/:443    │     └──────────────┘     └────────────────┘
│                 │
│                 │     ┌──────────────┐
│                 │────▶│  Telemetry   │
│                 │     │  FastAPI     │
│                 │     │   (8001)     │
│                 │     └──────────────┘
│                 │
│                 │     ┌──────────────┐
│                 │────▶│   IDS API    │
│                 │     │  FastAPI     │
└─────────────────┘     │   (8002)     │
                        └──────────────┘
```

## FastAPI Patterns

### 1. Estructura de Proyecto

```
telemetry_api/
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── events.py
│   │   ├── stats.py
│   │   └── health.py
│   └── deps.py           # Dependencies compartidas
├── core/
│   ├── config.py         # Settings
│   ├── security.py       # Auth
│   └── exceptions.py     # Custom exceptions
├── models/
│   ├── event.py          # Pydantic models
│   └── response.py       # Response schemas
├── services/
│   └── event_service.py  # Business logic
├── db/
│   └── database.py       # DB connection
└── main.py               # Entry point
```

### 2. Router con Versionado

```python
# api/v1/__init__.py
from fastapi import APIRouter
from .events import router as events_router
from .stats import router as stats_router
from .health import router as health_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(events_router, prefix="/events", tags=["events"])
api_router.include_router(stats_router, prefix="/stats", tags=["stats"])
api_router.include_router(health_router, prefix="/health", tags=["health"])


# main.py
from fastapi import FastAPI
from api.v1 import api_router

app = FastAPI(
    title="Croody Telemetry API",
    description="API de telemetría para el ecosistema Croody",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_router)
```

### 3. Schemas con Pydantic

```python
# models/event.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    """Tipos de eventos soportados."""
    PAGE_VIEW = "page_view"
    CLICK = "click"
    FORM_SUBMIT = "form_submit"
    ERROR = "error"
    CUSTOM = "custom"

class EventBase(BaseModel):
    """Schema base de evento."""
    event_type: EventType
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "event_type": "page_view",
                "payload": {"page": "/shop", "referrer": "google.com"},
                "timestamp": "2024-12-05T10:30:00Z"
            }
        }
    )

class EventCreate(EventBase):
    """Schema para crear evento."""
    session_id: Optional[str] = None
    user_agent: Optional[str] = None

class EventResponse(EventBase):
    """Schema de respuesta."""
    id: str
    created_at: datetime
    processed: bool = False

    model_config = ConfigDict(from_attributes=True)

class EventList(BaseModel):
    """Lista paginada de eventos."""
    items: list[EventResponse]
    total: int
    page: int
    page_size: int
    pages: int
```

### 4. Endpoints RESTful

```python
# api/v1/events.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from datetime import datetime

from models.event import EventCreate, EventResponse, EventList, EventType
from services.event_service import EventService
from api.deps import get_event_service, get_api_key

router = APIRouter()

@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear evento",
    description="Registra un nuevo evento de telemetría"
)
async def create_event(
    event: EventCreate,
    service: EventService = Depends(get_event_service),
    api_key: str = Depends(get_api_key)
):
    """
    Crear un evento de telemetría.

    - **event_type**: Tipo de evento (page_view, click, etc.)
    - **payload**: Datos adicionales del evento
    - **timestamp**: Timestamp del evento (opcional, default: now)
    """
    return await service.create(event)

@router.get(
    "/",
    response_model=EventList,
    summary="Listar eventos",
    description="Obtiene lista paginada de eventos"
)
async def list_events(
    event_type: Optional[EventType] = Query(None, description="Filtrar por tipo"),
    start_date: Optional[datetime] = Query(None, description="Fecha inicio"),
    end_date: Optional[datetime] = Query(None, description="Fecha fin"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(20, ge=1, le=100, description="Items por página"),
    service: EventService = Depends(get_event_service)
):
    """Listar eventos con filtros y paginación."""
    return await service.list(
        event_type=event_type,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size
    )

@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Obtener evento",
    responses={
        404: {"description": "Evento no encontrado"}
    }
)
async def get_event(
    event_id: str,
    service: EventService = Depends(get_event_service)
):
    """Obtener un evento por ID."""
    event = await service.get_by_id(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evento {event_id} no encontrado"
        )
    return event

@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar evento"
)
async def delete_event(
    event_id: str,
    service: EventService = Depends(get_event_service),
    api_key: str = Depends(get_api_key)
):
    """Eliminar un evento."""
    deleted = await service.delete(event_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evento {event_id} no encontrado"
        )
```

### 5. Dependency Injection

```python
# api/deps.py
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Annotated
from functools import lru_cache

from core.config import Settings
from services.event_service import EventService
from db.database import get_db

security = HTTPBearer(auto_error=False)

@lru_cache
def get_settings() -> Settings:
    """Singleton de settings."""
    return Settings()

async def get_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    x_api_key: Optional[str] = Header(None),
    settings: Settings = Depends(get_settings)
) -> str:
    """
    Extrae y valida API key.
    Soporta Bearer token y header X-API-Key.
    """
    api_key = None

    if credentials:
        api_key = credentials.credentials
    elif x_api_key:
        api_key = x_api_key

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key requerida",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if api_key not in settings.valid_api_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key inválida"
        )

    return api_key

async def get_event_service(
    db=Depends(get_db),
    settings: Settings = Depends(get_settings)
) -> EventService:
    """Factory de EventService."""
    return EventService(db, settings)

# Type alias para inyección
CurrentAPIKey = Annotated[str, Depends(get_api_key)]
```

### 6. Error Handling

```python
# core/exceptions.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

class APIException(Exception):
    """Base exception para APIs."""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None
    ):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code or f"ERR_{status_code}"

class NotFoundError(APIException):
    def __init__(self, resource: str, id: str):
        super().__init__(
            status_code=404,
            detail=f"{resource} con id {id} no encontrado",
            error_code="NOT_FOUND"
        )

class ValidationError(APIException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=422,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )

# Exception handlers para main.py
async def api_exception_handler(request: Request, exc: APIException):
    """Handler para APIException."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
                "path": str(request.url)
            }
        }
    )

async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handler para errores de validación Pydantic."""
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Error de validación",
                "details": exc.errors()
            }
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Handler genérico para errores no manejados."""
    logger.exception(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Error interno del servidor"
            }
        }
    )


# En main.py
from core.exceptions import (
    APIException, api_exception_handler,
    validation_exception_handler, generic_exception_handler
)
from pydantic import ValidationError

app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
```

### 7. Middleware

```python
# core/middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
import uuid

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware de logging de requests."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        # Añadir request_id al state
        request.state.request_id = request_id

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000

        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"- {response.status_code} - {process_time:.2f}ms"
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting simple."""

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.rpm = requests_per_minute
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_minute = int(time.time() / 60)

        key = f"{client_ip}:{current_minute}"

        self.requests[key] = self.requests.get(key, 0) + 1

        if self.requests[key] > self.rpm:
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )

        return await call_next(request)
```

## Django REST Patterns

### 8. ViewSets con DRF

```python
# shop/api/viewsets.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q

from shop.models import Product, Category
from .serializers import ProductSerializer, ProductDetailSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para productos.

    list: Lista productos activos
    retrieve: Detalle de producto
    create: Crear producto (admin)
    update: Actualizar producto (admin)
    destroy: Eliminar producto (admin)
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Optimizar queries
        queryset = queryset.select_related('category')

        # Filtros
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Productos destacados."""
        featured = self.get_queryset().filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, slug=None):
        """Añadir producto al carrito."""
        product = self.get_object()
        quantity = request.data.get('quantity', 1)

        cart_service = CartService(request.user)
        item = cart_service.add_item(product, quantity)

        return Response({
            'message': f'{product.name} añadido al carrito',
            'cart_total': cart_service.get_total()
        })
```

### 9. Serializers

```python
# shop/api/serializers.py
from rest_framework import serializers
from shop.models import Product, Category, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer para lista de productos."""
    category = CategorySerializer(read_only=True)
    display_price = serializers.CharField(source='get_display_price', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'display_price',
            'image', 'category', 'is_featured'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'rating', 'comment', 'created_at']

class ProductDetailSerializer(ProductSerializer):
    """Serializer para detalle de producto."""
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + [
            'description', 'stock', 'reviews', 'average_rating',
            'created_at', 'updated_at'
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return sum(r.rating for r in reviews) / len(reviews)
```

## Best Practices

### Response Format Estándar

```python
# Éxito
{
    "data": {...},
    "meta": {
        "page": 1,
        "page_size": 20,
        "total": 100
    }
}

# Error
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Campo requerido",
        "details": [...]
    }
}
```

### Versionado

```
/api/v1/products/    # Versión actual
/api/v2/products/    # Nueva versión (cuando rompa compatibilidad)
```

### Rate Limiting (nginx)

```nginx
# gateway/nginx.conf
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location /api/ {
    limit_req zone=api_limit burst=20 nodelay;
    proxy_pass http://api_upstream;
}
```

### Documentación OpenAPI

```python
# FastAPI genera automáticamente en /docs y /redoc
# Para DRF usar drf-spectacular

# settings.py
SPECTACULAR_SETTINGS = {
    'TITLE': 'Croody API',
    'DESCRIPTION': 'API del ecosistema Croody',
    'VERSION': '1.0.0',
}
```

## Métricas de API

| Métrica | Objetivo |
|---------|----------|
| Latencia P95 | < 200ms |
| Disponibilidad | 99.9% |
| Error rate | < 0.1% |
| Rate limit | 100 req/min |

## Recursos

- OpenAPI Spec: `/docs` (FastAPI) o `/api/schema/` (DRF)
- Postman Collection: `docs/api/croody.postman_collection.json`
- Contratos: `docs/03-REFERENCIA/api-contracts/`
