# Sistema de Monitoreo y Logs - Documentación Completa

## Resumen
El sistema de monitoreo de Croody implementa un enfoque multi-capa que incluye logging estructurado para Django y FastAPI, health checks proactivos, métricas de aplicación, log aggregation centralizado, y monitoreo de infraestructura. Utiliza JSON logging para parseo automático, health endpoints para detección temprana de problemas, y scripts de seguridad para tracking de eventos.

## Ubicación
- **Django Config**: `/proyecto_integrado/Croody/croody/settings.py` (configuración de logging)
- **FastAPI Services**:
  - `/proyecto_integrado/services/telemetry-gateway/app/main.py` (healthz endpoint)
  - `/proyecto_integrado/services/ids-ml/app/main.py` (healthz endpoint)
- **Security Logger**: `/scripts/security/security_logger.py`
- **Docker Healthchecks**: `/proyecto_integrado/docker-compose.yml`
- **Nginx Logs**: `/proyecto_integrado/gateway/nginx.conf` (JSON logging)

## Arquitectura de Monitoreo

### Diagrama de Flujo
```
┌─────────────────────────────────────────────────────────────────┐
│                     APLICACIÓN LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  Django (Croody)          FastAPI Services                     │
│  - Request logging         - Health checks                      │
│  - Error tracking          - Structured logging                 │
│  - SQL query logging       - Performance metrics                │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                  CONTAINER ORCHESTRATION                       │
├─────────────────────────────────────────────────────────────────┤
│  Docker Compose                                                 │
│  - Health checks per container                                  │
│  - Restart policies                                             │
│  - Resource limits (mem/cpu)                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                     INFRASTRUCTURE                             │
├─────────────────────────────────────────────────────────────────┤
│  Nginx (Gateway)        Application Logs                       │
│  - Access logs (JSON)   - Django logs                          │
│  - Error logs           - Security events                      │
│  - Health monitoring    - FastAPI logs                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                  LOG AGGREGATION                               │
├─────────────────────────────────────────────────────────────────┤
│  Centralized Storage                                            │
│  - JSON log parsing                                              │
│  - Search and filtering                                         │
│  - Alerting rules                                                │
│  - Analytics and reporting                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Django Logging Configuration

### LOGGING Setup

#### Basic Configuration (settings.py)
```python
import os
from pathlib import Path

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple' if DEBUG else 'json',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 15728640,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django_error.log',
            'maxBytes': 15728640,
            'backupCount': 10,
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'shop': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'landing': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'telemetry': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

#### Production Configuration
```python
# settings/production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d %(thread)d %(request_id)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/croody/application.log',
            'formatter': 'json',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/croody/error.log',
            'formatter': 'json',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'croody': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### Custom Logger Usage

#### In Views
```python
# landing/views.py
from __future__ import annotations
import logging
from typing import Any

logger = logging.getLogger(__name__)

class HomeView(LandingNavigationMixin, TemplateView):
    template_name = 'landing/home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        logger.info("HomeView accessed", extra={
            'user_id': self.request.user.id if self.request.user.is_authenticated else None,
            'ip': self.request.META.get('REMOTE_ADDR'),
            'user_agent': self.request.META.get('HTTP_USER_AGENT'),
        })
        # ... rest of method
```

#### In Models
```python
# landing/models.py
import logging

logger = logging.getLogger(__name__)

class UserProfile(models.Model):
    # ... fields ...

    def regenerate_token(self) -> None:
        old_token = self.ingest_token
        self.ingest_token = _generate_ingest_token()
        self.save(update_fields=["ingest_token"])

        logger.info("Token regenerated", extra={
            'user_id': self.user_id,
            'old_token_exists': bool(old_token),
            'new_token_length': len(self.ingest_token),
        })
```

#### In Forms
```python
# landing/forms.py
import logging

logger = logging.getLogger(__name__)

class CroodySignupForm(UserCreationForm):
    # ... fields ...

    def save(self, commit: bool = True):
        user = super().save(commit=False)

        try:
            # Processing logic
            user.save()

            # Create profile
            profile = user.profile
            profile.preferred_language = self.cleaned_data['preferred_language']
            profile.preferred_theme = self.cleaned_data['preferred_theme']
            profile.save()

            logger.info("User registered successfully", extra={
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
            })

            return user
        except Exception as e:
            logger.error("User registration failed", exc_info=True, extra={
                'email': self.cleaned_data.get('email'),
                'error_type': type(e).__name__,
            })
            raise
```

### SQL Query Logging

#### Django Settings for Query Logging
```python
# settings/debug.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

#### Custom Query Logging
```python
# utils/db_logging.py
import logging
from django.db import connection
from django.conf import settings

class SQLQueryLogger:
    def __init__(self):
        self.logger = logging.getLogger('django.db.backends.sql')

    def log_query(self, sql: str, params: tuple, duration: float):
        """Log SQL query with performance metrics."""
        if settings.DEBUG:
            self.logger.debug(
                "SQL Query executed",
                extra={
                    'sql': sql,
                    'params': params,
                    'duration_ms': round(duration * 1000, 2),
                    'queries_count': len(connection.queries),
                }
            )

# Usage in views
from utils.db_logging import SQLQueryLogger

logger = SQLQueryLogger()

def my_view(request):
    start_time = time.time()
    # Execute queries
    products = Product.objects.all()
    duration = time.time() - start_time
    logger.log_query("SELECT * FROM shop_product", (), duration)
```

## FastAPI Logging

### Structured Logging Implementation

#### Telemetry Gateway Logger
```python
# services/telemetry-gateway/app/main.py
from __future__ import annotations
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("telemetry-gateway")

@app.post("/api/telemetry/ingest", response_model=TelemetryOut)
def ingest(payload: TelemetryIn, x_api_key: Optional[str] = Header(default=None)):
    """Ingest telemetry data from robots."""
    start_time = datetime.now(timezone.utc)

    try:
        # Log incoming request
        logger.info(
            "Telemetry ingest started",
            extra={
                "event_type": "telemetry_ingest",
                "robot_id": payload.robot_id,
                "data_keys": list(payload.data.keys()) if payload.data else [],
                "has_position": payload.position is not None,
                "api_key_provided": x_api_key is not None,
            }
        )

        # ... processing logic ...

        # Log successful ingestion
        duration_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
        logger.info(
            "Telemetry ingested successfully",
            extra={
                "event_type": "telemetry_success",
                "robot_id": robot_id,
                "record_id": row[0] if USE_POSTGRES else result.lastrowid,
                "duration_ms": duration_ms,
                "db_type": "postgres" if USE_POSTGRES else "sqlite",
            }
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Telemetry ingestion failed",
            exc_info=True,
            extra={
                "event_type": "telemetry_error",
                "robot_id": payload.robot_id,
                "error_type": type(e).__name__,
                "error_message": str(e),
            }
        )
        raise HTTPException(status_code=500, detail="Internal server error")
```

#### IDS ML Service Logger
```python
# services/ids-ml/app/main.py
import logging
from datetime import datetime

logger = logging.getLogger("ids-ml")

@app.post("/api/ids/predict")
def predict(req: PredictRequest, x_api_key: str | None = Header(default=None)):
    """ML-based intrusion detection prediction."""
    request_id = f"pred-{datetime.now().timestamp()}"

    logger.info(
        "Prediction request received",
        extra={
            "request_id": request_id,
            "rows_count": len(req.rows),
            "api_key_provided": x_api_key is not None,
        }
    )

    model = _load_model()

    if model is None:
        logger.warning(
            "Model not available, using fallback",
            extra={
                "request_id": request_id,
                "model_path": MODEL_PATH,
            }
        )
        # Fallback prediction logic
        return PredictResponse(predictions=preds, model={"path": None})

    try:
        logger.info(
            "Using ML model for prediction",
            extra={
                "request_id": request_id,
                "model_type": type(model).__name__,
            }
        )
        # ML inference logic
        return PredictResponse(predictions=predictions, model=model_info)

    except Exception as e:
        logger.error(
            "Prediction failed",
            exc_info=True,
            extra={
                "request_id": request_id,
                "error_type": type(e).__name__,
            }
        )
        raise HTTPException(status_code=500, detail="Prediction error")
```

### Request Logging Middleware

#### Custom Middleware for FastAPI
```python
# services/telemetry-gateway/app/middleware.py
from __future__ import annotations
import time
import uuid
from typing import Callable

from fastapi import Request, Response

async def logging_middleware(request: Request, call_next: Callable) -> Response:
    """Log all incoming requests."""
    start_time = time.time()

    # Generate request ID
    request_id = str(uuid.uuid4())

    # Add request ID to state
    request.state.request_id = request_id

    # Log request
    logger.info(
        "Request started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
        }
    )

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration_ms = (time.time() - start_time) * 1000

    # Log response
    logger.info(
        "Request completed",
        extra={
            "request_id": request_id,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        }
    )

    return response
```

#### Register Middleware
```python
# services/telemetry-gateway/app/main.py
from middleware import logging_middleware

app = FastAPI(title="Telemetry Gateway")
app.middleware("http")(logging_middleware)
```

## Health Checks

### Django Health Check

#### Endpoint Implementation
```python
# landing/views.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request):
    """Comprehensive health check endpoint."""
    health_status = {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {},
    }

    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status["checks"]["database"] = {"status": "ok"}
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "error",
            "error": str(e)
        }
        health_status["status"] = "degraded"

    # Cache check
    try:
        cache.set("health_check", "ok", 10)
        result = cache.get("health_check")
        health_status["checks"]["cache"] = {
            "status": "ok" if result == "ok" else "error"
        }
    except Exception as e:
        health_status["checks"]["cache"] = {
            "status": "error",
            "error": str(e)
        }

    status_code = 200 if health_status["status"] == "ok" else 503
    return JsonResponse(health_status, status=status_code)

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... other urls
    path('health/', views.health_check, name='health_check'),
]
```

### FastAPI Health Checks

#### Telemetry Gateway Health
```python
# services/telemetry-gateway/app/main.py
import os
from datetime import datetime

@app.get("/healthz")
def healthz() -> Dict[str, str]:
    """Basic health check."""
    return {"status": "ok"}

@app.get("/health")
def health() -> Dict[str, Any]:
    """Detailed health check with system info."""
    health_status = {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": app.version,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "checks": {},
    }

    # Database connectivity
    try:
        if USE_POSTGRES:
            conn = psycopg2.connect(DB_URL)
            conn.close()
            health_status["checks"]["database"] = {"status": "ok"}
        else:
            # SQLite check
            if os.path.exists(DB_PATH):
                health_status["checks"]["database"] = {"status": "ok"}
            else:
                health_status["checks"]["database"] = {
                    "status": "error",
                    "error": "Database file not found"
                }
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "error",
            "error": str(e)
        }

    # Disk space
    try:
        stat = os.statvfs(DB_PATH if USE_POSTGRES else os.path.dirname(DB_PATH))
        free_space_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        health_status["checks"]["disk"] = {
            "status": "ok" if free_space_gb > 1 else "warning",
            "free_space_gb": round(free_space_gb, 2)
        }
    except Exception:
        health_status["checks"]["disk"] = {"status": "unknown"}

    return health_status
```

#### IDS ML Health
```python
# services/ids-ml/app/main.py
@app.get("/healthz")
def healthz():
    """Basic health check."""
    return {"status": "ok"}

@app.get("/health")
def health():
    """Detailed health check with model info."""
    health_status = {
        "status": "ok",
        "model": {
            "path": MODEL_PATH,
            "available": os.path.exists(MODEL_PATH),
            "size_bytes": os.path.getsize(MODEL_PATH) if os.path.exists(MODEL_PATH) else None,
        }
    }

    # Test model loading
    try:
        model = _load_model()
        health_status["checks"] = {
            "model_loadable": {"status": "ok" if model else "error"},
        }
    except Exception as e:
        health_status["checks"] = {
            "model_loadable": {"status": "error", "error": str(e)}
        }

    return health_status
```

## Security Event Logging

### Security Logger Implementation

#### Centralized Security Logger
```python
#!/usr/bin/env python3
# scripts/security/security_logger.py
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "proyecto_integrado" / "Croody" / "security" / "logs" / "eventos_seguridad.txt"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log_event(event_type: str, ip: str, proto: str, action: str, detail: str) -> None:
    """Log security events in structured format."""
    timestamp = datetime.now(timezone.utc).isoformat()
    line = f"[{timestamp}] | {event_type} | ip={ip} | protocolo={proto.upper()} | accion={action} | detalle={detail}\n"
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(line)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Registrar eventos de seguridad")
    parser.add_argument("tipo", help="Tipo de ataque o evento")
    parser.add_argument("ip", help="IP origen")
    parser.add_argument("protocolo", choices=["tcp", "udp", "icmp", "otro"])
    parser.add_argument("accion", help="Acción tomada")
    parser.add_argument("detalle", help="Descripción del evento")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    log_event(args.tipo, args.ip, args.protocolo, args.accion, args.detalle)
    print(f"Evento registrado en {LOG_PATH}")

if __name__ == "__main__":
    main()
```

#### Security Event Types
```python
# Security event categories
SECURITY_EVENTS = {
    "AUTHENTICATION": {
        "failed_login": "Intento de login fallido",
        "successful_login": "Login exitoso",
        "password_reset": "Reset de contraseña",
        "token_refresh": "Refresh de token",
    },
    "AUTHORIZATION": {
        "access_denied": "Acceso denegado",
        "privilege_escalation": "Escalación de privilegios",
        "unauthorized_api_access": "Acceso no autorizado a API",
    },
    "INJECTION": {
        "sql_injection_attempt": "Intento de SQL injection",
        "xss_attempt": "Intento de XSS",
        "command_injection_attempt": "Intento de command injection",
    },
    "NETWORK": {
        "syn_flood": "SYN flood attack",
        "port_scan": "Port scanning",
        "ddos_attempt": "Intento de DDoS",
        "suspicious_traffic": "Tráfico sospechoso",
    },
    "DATA": {
        "data_breach_attempt": "Intento de exfiltración",
        "unauthorized_access": "Acceso no autorizado a datos",
        "mass_download": "Descarga masiva",
    },
}
```

#### Usage in Django Middleware
```python
# middleware/security.py
import logging
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("security")

class SecurityLoggingMiddleware(MiddlewareMixin):
    """Log security-related events."""

    def process_request(self, request):
        """Check for suspicious requests."""
        # Check for SQL injection patterns
        sql_patterns = ['union', 'select', 'drop', 'insert', 'update', 'delete']
        request_text = request.body.decode('utf-8', errors='ignore').lower()

        for pattern in sql_patterns:
            if pattern in request_text:
                logger.warning(
                    "SQL injection attempt detected",
                    extra={
                        "event_type": "SQL_INJECTION_ATTEMPT",
                        "ip": self.get_client_ip(request),
                        "method": request.method,
                        "path": request.path,
                        "pattern": pattern,
                    }
                )
                return HttpResponseForbidden("Request blocked")

        return None

    def get_client_ip(self, request):
        """Get real client IP considering proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
```

## Docker Health Checks

### Docker Compose Configuration

#### Individual Service Health Checks
```yaml
# docker-compose.yml
services:
  gateway:
    image: nginx:alpine
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1"]
      interval: 10s
      timeout: 3s
      retries: 5
      start_period: 10s

  croody:
    build:
      context: ./Croody
      dockerfile: Dockerfile
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8000/health/"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 40s

  telemetry-gateway:
    build:
      context: ./services/telemetry-gateway
      dockerfile: Dockerfile
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:9000/healthz"]
      interval: 10s
      timeout: 3s
      retries: 5
      start_period: 10s

  ids-ml:
    build:
      context: ./services/ids-ml
      dockerfile: Dockerfile
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:9100/healthz"]
      interval: 10s
      timeout: 3s
      retries: 5
      start_period: 15s
```

#### Health Check Dependencies
```yaml
services:
  croody:
    depends_on:
      telemetry-gateway:
        condition: service_healthy
      ids-ml:
        condition: service_healthy

  robot-sim:
    depends_on:
      telemetry-gateway:
        condition: service_healthy
```

### Custom Health Check Scripts

#### Django Health Check Script
```python
#!/usr/bin/env python3
# scripts/health/django_health.py
import sys
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'croody.settings')
sys.path.append('/app')
django.setup()

from django.db import connection
from django.core.cache import cache

def check_database():
    """Check database connectivity."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True, "Database connection OK"
    except Exception as e:
        return False, f"Database error: {e}"

def check_cache():
    """Check cache connectivity."""
    try:
        cache.set("health_check", "ok", 10)
        result = cache.get("health_check")
        if result == "ok":
            return True, "Cache connection OK"
        return False, "Cache read/write failed"
    except Exception as e:
        return False, f"Cache error: {e}"

def main():
    """Run all health checks."""
    checks = {
        "database": check_database(),
        "cache": check_cache(),
    }

    all_ok = True
    for name, (status, message) in checks.items():
        print(f"{name}: {message}")
        if not status:
            all_ok = False

    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
```

#### FastAPI Health Check Script
```bash
#!/bin/bash
# scripts/health/fastapi_health.sh

# Check if service is responding
if wget -qO- http://localhost:9000/healthz > /dev/null 2>&1; then
    echo "Service is healthy"
    exit 0
else
    echo "Service is not responding"
    exit 1
fi
```

## Log Aggregation

### Nginx Access Logs (JSON Format)

#### Nginx Configuration
```nginx
# gateway/nginx.conf

# JSON logging format
log_format json_combined escape=json
    '{'
    '"time":"$time_iso8601",'
    '"remote_addr":"$remote_addr",'
    '"remote_user":"$remote_user",'
    '"request_method":"$request_method",'
    '"request_uri":"$request_uri",'
    '"request_path":"$request_uri",'
    '"request_query":"$args",'
    '"request_length":$request_length,'
    '"request_time":$request_time,'
    '"status":$status,'
    '"body_bytes_sent":$body_bytes_sent,'
    '"bytes_sent":$bytes_sent,'
    '"http_referrer":"$http_referer",'
    '"http_user_agent":"$http_user_agent",'
    '"http_x_forwarded_for":"$http_x_forwarded_for",'
    '"request_id":"$req_id",'
    '"upstream_addr":"$upstream_addr",'
    '"upstream_status":"$upstream_status",'
    '"upstream_response_time":$upstream_response_time'
    '}';

# Use JSON format for all logs
access_log /var/log/nginx/access.log json_combined;
error_log /var/log/nginx/error.log warn;

# Log to stdout for Docker
access_log /dev/stdout json_combined;
error_log /dev/stderr warn;
```

#### Log Analysis Commands
```bash
# Extract status codes
grep -o '"status":[0-9]*' /var/log/nginx/access.log | sort | uniq -c | sort -rn

# Top requesting IPs
grep -o '"remote_addr":"[^"]*"' /var/log/nginx/access.log | \
    cut -d'"' -f4 | sort | uniq -c | sort -rn | head -20

# Slow requests (>1s)
grep -o '"request_time":[0-9.]*' /var/log/nginx/access.log | \
    awk -F':' '$2 > 1' | wc -l

# Error requests (4xx, 5xx)
grep -o '"status":[45][0-9][0-9]' /var/log/nginx/access.log | sort | uniq -c
```

### Centralized Log Collection

#### Logrotate Configuration
```bash
# /etc/logrotate.d/croody
/var/log/croody/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 0644 www-data www-data
    postrotate
        systemctl reload croody
    endscript
}

/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0644 www-data www-data
    postrotate
        systemctl reload nginx
    endscript
}
```

#### ELK Stack Integration (Optional)
```python
# monitoring/logstash_config.py
import json

LOGSTASH_CONFIG = {
    "input": {
        "file": {
            "path": "/var/log/croody/*.log",
            "start_position": "beginning",
            "sincedb_path": "/dev/null",
        }
    },
    "filter": {
        "json": {
            "source": "message"
        },
        "date": {
            "match": ["timestamp", "ISO8601"]
        }
    },
    "output": {
        "elasticsearch": {
            "hosts": ["elasticsearch:9200"],
            "index": "croody-logs-%{+YYYY.MM.dd}"
        },
        "stdout": {}
    }
}
```

## Metrics and Performance Monitoring

### Application Metrics

#### Custom Metrics Collection
```python
# monitoring/metrics.py
from __future__ import annotations
import time
import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger("metrics")

def timer(func: Callable) -> Callable:
    """Decorator to time function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        duration_ms = (time.time() - start_time) * 1000

        logger.info(
            "Function execution time",
            extra={
                "event_type": "execution_time",
                "function": func.__name__,
                "duration_ms": round(duration_ms, 2),
            }
        )

        return result
    return wrapper

class MetricsCollector:
    """Collect and log application metrics."""

    def __init__(self):
        self.metrics = {}

    def increment(self, name: str, value: int = 1, tags: dict = None):
        """Increment a counter metric."""
        logger.info(
            "Counter metric",
            extra={
                "metric_type": "counter",
                "metric_name": name,
                "value": value,
                "tags": tags or {},
            }
        )

    def gauge(self, name: str, value: float, tags: dict = None):
        """Set a gauge metric."""
        logger.info(
            "Gauge metric",
            extra={
                "metric_type": "gauge",
                "metric_name": name,
                "value": value,
                "tags": tags or {},
            }
        )

    def histogram(self, name: str, value: float, tags: dict = None):
        """Record a histogram value."""
        logger.info(
            "Histogram metric",
            extra={
                "metric_type": "histogram",
                "metric_name": name,
                "value": value,
                "tags": tags or {},
            }
        )

# Global metrics collector
metrics = MetricsCollector()

# Usage in views
@timer
def product_list(request):
    # Count active users
    metrics.increment("active_requests", tags={"endpoint": "/shop/", "method": request.method})

    products = Product.objects.all()
    metrics.gauge("products_count", products.count())

    return render(request, 'shop/list.html', {'products': products})
```

#### Database Query Metrics
```python
# monitoring/db_metrics.py
import logging
from django.db import connection
from django.conf import settings

logger = logging.getLogger("metrics")

class QueryMetricsMiddleware:
    """Collect database query metrics."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_queries = len(connection.queries

        response = self.get_response(request)

        end_queries = len(connection.queries)
        num_queries = end_queries - start_queries

        if num_queries > 0:
            total_time = sum(float(q['time']) for q in connection.queries[start_queries:])

            logger.info(
                "Database queries executed",
                extra={
                    "event_type": "db_queries",
                    "request_path": request.path,
                    "query_count": num_queries,
                    "total_time_ms": round(total_time, 2),
                }
            )

            # Alert if too many queries
            if num_queries > 50:
                logger.warning(
                    "High number of database queries",
                    extra={
                        "event_type": "n_plus_one_alert",
                        "request_path": request.path,
                        "query_count": num_queries,
                    }
                )

        return response

# Add to settings
MIDDLEWARE = [
    # ...
    'monitoring.db_metrics.QueryMetricsMiddleware',
    # ...
]
```

### FastAPI Metrics

#### Prometheus Integration
```python
# services/telemetry-gateway/app/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)

# Middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response

@app.get("/metrics")
def get_metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type="text/plain")
```

## Alerting

### Log-Based Alerts

#### Log Analysis Script
```bash
#!/bin/bash
# scripts/monitoring/alert_checker.sh

LOG_FILE="/var/log/croody/application.log"
ALERT_LOG="/var/log/croody/alerts.log"

# Check for errors
ERROR_COUNT=$(grep -c '"level":"ERROR"' "$LOG_FILE" | tail -1)

if [ "$ERROR_COUNT" -gt 10 ]; then
    echo "[$(date)] ALERT: High error rate detected ($ERROR_COUNT errors)" >> "$ALERT_LOG"
    # Send notification
    curl -X POST "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK" \
         -d "{\"text\":\"High error rate detected: $ERROR_COUNT errors\"}"
fi

# Check for authentication failures
AUTH_FAILURES=$(grep -c '"event_type":"failed_login"' "$LOG_FILE" | tail -1)

if [ "$AUTH_FAILURES" -gt 5 ]; then
    echo "[$(date)] ALERT: Multiple authentication failures ($AUTH_FAILURES)" >> "$ALERT_LOG"
fi
```

#### Cron Job for Alert Checking
```bash
# /etc/cron.d/croody-alerts
# Check every 5 minutes
*/5 * * * * root /scripts/monitoring/alert_checker.sh >> /var/log/croody/alerts.log 2>&1
```

### Health Check Monitoring

#### Monitor Script
```bash
#!/bin/bash
# scripts/health/monitor_services.sh

SERVICES=(
    "croody:http://localhost:8000/health/"
    "telemetry:http://localhost:9000/healthz"
    "ids-ml:http://localhost:9100/healthz"
)

ALERT_EMAIL="admin@croody.app"

for service in "${SERVICES[@]}"; do
    name="${service%%:*}"
    url="${service#*:}"

    if ! curl -sf "$url" > /dev/null 2>&1; then
        echo "$(date): Service $name is DOWN" >> /var/log/croody/service_alerts.log
        # Send email alert
        echo "Service $name is down. URL: $url" | mail -s "Service Down Alert" "$ALERT_EMAIL"
    else
        echo "$(date): Service $name is UP" >> /var/log/croody/service_status.log
    fi
done
```

## Structured Logging Best Practices

### Log Format Standards

#### JSON Log Structure
```python
STANDARD_LOG_FIELDS = {
    "timestamp": "ISO8601 formatted timestamp",
    "level": "Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    "logger": "Logger name (e.g., 'shop', 'landing')",
    "module": "Python module name",
    "function": "Function name",
    "line": "Line number",
    "message": "Log message",
    "request_id": "Unique request identifier",
    "user_id": "User ID (if authenticated)",
    "ip": "Client IP address",
    "event_type": "Event category (e.g., 'user_login', 'api_call')",
    "duration_ms": "Duration in milliseconds (for performance logs)",
    "error_type": "Exception type (for error logs)",
    "error_message": "Exception message (for error logs)",
}
```

#### Example Log Entries
```json
{
  "timestamp": "2025-01-15T10:30:45.123Z",
  "level": "INFO",
  "logger": "landing",
  "module": "views",
  "function": "HomeView.get_context_data",
  "line": 125,
  "message": "HomeView accessed",
  "request_id": "req-550e8400-e29b-41d4-a716-446655440000",
  "user_id": 42,
  "ip": "192.0.2.1",
  "user_agent": "Mozilla/5.0...",
  "event_type": "page_view"
}

{
  "timestamp": "2025-01-15T10:30:46.456Z",
  "level": "ERROR",
  "logger": "telemetry",
  "module": "main",
  "function": "ingest",
  "line": 203,
  "message": "Telemetry ingestion failed",
  "request_id": "req-6ba7b810-9b2a-4b7e-8d5c-2f3e1b0a9b8c",
  "event_type": "telemetry_error",
  "robot_id": "robot-alpha",
  "error_type": "DatabaseError",
  "error_message": "connection refused",
  "duration_ms": 245.67
}
```

### Log Levels Usage

#### When to Use Each Level
```python
# DEBUG - Detailed information for diagnosing problems
logger.debug(
    "Processing user query",
    extra={
        "query": query,
        "filters": filters,
        "query_params": request.GET.dict(),
    }
)

# INFO - General operational events
logger.info(
    "User registered successfully",
    extra={
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
    }
)

# WARNING - Something unexpected happened but not an error
logger.warning(
    "User attempted invalid action",
    extra={
        "user_id": user.id,
        "action": "delete_admin_user",
        "blocked": True,
    }
)

# ERROR - A serious problem occurred
logger.error(
    "Failed to save user profile",
    exc_info=True,
    extra={
        "user_id": user.id,
        "error_type": type(e).__name__,
    }
)

# CRITICAL - A very serious error
logger.critical(
    "Database connection failed",
    exc_info=True,
    extra={
        "error_type": "DatabaseConnectionError",
        "retry_attempt": 3,
    }
)
```

## Monitoring Dashboard

### Key Metrics to Track

#### Application Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| **Response Time** | Average request duration | > 2 seconds |
| **Error Rate** | Percentage of 5xx responses | > 5% |
| **Request Rate** | Requests per minute | Sudden spikes |
| **Database Queries** | Queries per request | > 50 per request |
| **Active Users** | Currently logged in users | < 1 (unexpected) |

#### Infrastructure Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| **CPU Usage** | CPU utilization per service | > 80% |
| **Memory Usage** | RAM utilization | > 85% |
| **Disk Space** | Available disk space | < 10% |
| **Database Connections** | Active DB connections | > 80% of max |
| **Cache Hit Rate** | Redis/memcached hit % | < 90% |

#### Security Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| **Failed Logins** | Authentication failures/min | > 10 |
| **SQL Injection Attempts** | Blocked injection attempts | > 0 |
| **Rate Limit Violations** | Blocked requests | > 100/hour |
| **Suspicious IPs** | IPs with many requests | Top 10 |
| **Security Events** | Logged security events | Any |

### Grafana Dashboard Configuration (Optional)

#### Dashboard JSON
```json
{
  "dashboard": {
    "title": "Croody Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status_code=~\"5..\"}[5m]) / rate(http_requests_total[5m])",
            "legendFormat": "Error rate"
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting Logs

### Common Log Analysis Commands

#### Django Application Logs
```bash
# View recent errors
tail -f /var/log/croody/application.log | grep "ERROR"

# Filter by user
grep "user_id.*123" /var/log/croody/application.log

# Find slow queries
grep "duration_ms" /var/log/croody/application.log | awk -F'"duration_ms":' '$2 > 1000'

# Count errors by type
grep '"level":"ERROR"' /var/log/croody/application.log | \
    grep -o '"error_type":"[^"]*"' | sort | uniq -c
```

#### Nginx Access Logs
```bash
# Most active IPs
awk '{print $4}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -20

# Status code distribution
grep -o '"status":[0-9]*' /var/log/nginx/access.log | \
    awk -F':' '{print $2}' | sort | uniq -c

# Peak traffic hours
grep -o '"time":"[^"]*"' /var/log/nginx/access.log | \
    awk -F'T' '{print $2}' | cut -d':' -f1 | sort | uniq -c
```

#### Security Logs
```bash
# View security events
tail -f /var/log/croody/security.log

# Count events by type
grep "event_type" /var/log/croody/security.log | \
    awk -F'event_type=' '{print $2}' | awk -F'|' '{print $1}' | \
    sort | uniq -c

# Find repeated failed logins from same IP
grep "failed_login" /var/log/croody/security.log | \
    awk -F'ip=' '{print $2}' | awk -F'|' '{print $1}' | \
    sort | uniq -c | awk '$1 > 5'
```

### Log Analysis Tools

#### Using jq for JSON Logs
```bash
# Pretty print JSON log
cat /var/log/croody/application.log | jq '.'

# Filter ERROR level logs
cat /var/log/croody/application.log | jq 'select(.level == "ERROR")'

# Extract specific fields
cat /var/log/croody/application.log | jq '.timestamp, .message, .user_id'

# Group by event type
cat /var/log/croody/application.log | jq 'group_by(.event_type) | length'

# Calculate average response time
cat /var/log/croody/application.log | jq 'select(.duration_ms?) | .duration_ms' | \
    awk '{sum+=$1; count++} END {print "Average:", sum/count "ms"}'
```

## Performance Optimization

### Log Volume Management

#### Log Levels by Environment
```python
# settings/development.py
LOGGING = {
    'root': {'level': 'DEBUG'},
    'loggers': {
        'django': {'level': 'DEBUG'},
        'shop': {'level': 'DEBUG'},
        'landing': {'level': 'DEBUG'},
    }
}

# settings/production.py
LOGGING = {
    'root': {'level': 'INFO'},
    'loggers': {
        'django': {'level': 'INFO'},
        'shop': {'level': 'WARNING'},
        'landing': {'level': 'WARNING'},
    }
}
```

#### Async Logging (For High Throughput)
```python
# monitoring/async_logger.py
import asyncio
import logging
from queue import Queue
from threading import Thread

class AsyncLogger:
    def __init__(self):
        self.queue = Queue()
        self.thread = Thread(target=self._process_logs)
        self.thread.daemon = True
        self.thread.start()

    def log(self, record):
        self.queue.put(record)

    def _process_logs(self):
        while True:
            record = self.queue.get()
            # Process log synchronously
            self.queue.task_done()

# Usage
async_logger = AsyncLogger()

# In application code
async_logger.log({
    "level": "INFO",
    "message": "High throughput event",
    "timestamp": datetime.now().isoformat(),
})
```

## Best Practices

### ✅ Hacer
```python
# 1. Usar logging estructurado
logger.info("User action", extra={
    "user_id": user.id,
    "action": "product_purchase",
    "product_id": product.id,
    "amount": amount,
})

# 2. Incluir request ID para trazabilidad
request_id = str(uuid.uuid4())
logger.info("Request started", extra={"request_id": request_id})

# 3. Usar niveles de log apropiados
logger.debug("Debug info")  # Development only
logger.info("Normal operation")
logger.warning("Unexpected but handled")
logger.error("Error occurred", exc_info=True)
logger.critical("System failure", exc_info=True)

# 4. Loggar métricas de performance
logger.info("Query executed", extra={
    "query_time_ms": duration_ms,
    "query_type": "SELECT",
})

# 5. Usar health checks en todos los servicios
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
```

### ❌ Evitar
```python
# 1. No usar print() en producción
print("Debug message")  # ❌ Usar logger.debug()

# 2. No loggar datos sensibles
logger.info("User password: " + password)  # ❌ Nunca
logger.info("User login", extra={"password": password})  # ❌ No

# 3. No crear logs sin estructura
logger.info("User did something")  # ❌ No es útil

# 4. No ignorar excepciones
try:
    risky_operation()
except Exception:
    pass  # ❌ Siempre loggear errores

# 5. No usar niveles incorrectos
logger.info("Database connection failed")  # ❌ Debe ser ERROR
logger.error("Debug info")  # ❌ Debe ser DEBUG
```

## Referencias

### Archivos Relacionados
- `scripts/security/security_logger.py` - Centralized security event logging
- `services/telemetry-gateway/app/main.py` - FastAPI health checks and logging
- `services/ids-ml/app/main.py` - ML service health checks
- `docker-compose.yml` - Health check configurations
- `gateway/nginx.conf` - JSON access logging

### Herramientas de Monitoreo
- **Prometheus** - Metrics collection and alerting
- **Grafana** - Visualization dashboard
- **ELK Stack** - Log aggregation and analysis
- **CloudWatch** - AWS monitoring service
- **DataDog** - SaaS monitoring platform

### Documentación Externa
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Django Logging Configuration](https://docs.djangoproject.com/en/stable/topics/logging/)
- [FastAPI Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- [Docker Health Checks](https://docs.docker.com/engine/reference/builder/#healthcheck)
- [Prometheus Python Client](https://github.com/prometheus/client_python)

## Ver También
- [Seguridad - Hardening](../06-SEGURIDAD/hardening.md)
- [CI/CD Workflows](../04-DEVOPS/ci-cd-workflows.md)
- [Testing - Validación](../09-TESTING/testing-general.md)
