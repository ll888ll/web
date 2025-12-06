---
name: security-hardening
description: Guía de seguridad y hardening para Croody. Use cuando trabaje en configuración de seguridad, headers, SSL, firewall, o auditorías de seguridad.
---

# Security Hardening Guide - Croody Web

> Guía de seguridad siguiendo OWASP Top 10 2021 para el ecosistema Croody.

---

## Filosofía

La seguridad en Croody sigue el principio de **Defense in Depth**:
- Múltiples capas de protección
- Fail-secure (fallar de forma segura)
- Least privilege (mínimo privilegio necesario)
- Security by default (seguro por defecto)

---

## 1. Django Security Settings

### Settings de Producción

```python
# croody/settings/production.py

import os

# CRITICAL: Nunca True en producción
DEBUG = False

# Solo dominios permitidos
ALLOWED_HOSTS = [
    'croody.app',
    'www.croody.app',
    '*.croody.app',  # Subdomains
]

# Secret key desde variable de entorno
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY must be set")

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Content Security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### Content Security Policy

```python
# Usando django-csp
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")  # HTMX requiere inline
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_FORM_ACTION = ("'self'",)
```

---

## 2. Nginx Security Headers

### nginx.prod.conf

```nginx
server {
    listen 443 ssl http2;
    server_name croody.app;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/croody.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/croody.app/privkey.pem;

    # Modern SSL Config
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # Content Security Policy
    add_header Content-Security-Policy "
        default-src 'self';
        script-src 'self' 'unsafe-inline';
        style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
        font-src 'self' https://fonts.gstatic.com;
        img-src 'self' data: https:;
        connect-src 'self';
        frame-ancestors 'none';
        form-action 'self';
        base-uri 'self';
        object-src 'none';
    " always;

    # Hide nginx version
    server_tokens off;

    # Rate Limiting
    limit_req zone=api burst=20 nodelay;
    limit_req zone=login burst=5 nodelay;

    # Request limits
    client_max_body_size 10M;
    client_body_timeout 10s;
    client_header_timeout 10s;

    # Proxy settings
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Security headers for proxied content
        proxy_hide_header X-Powered-By;
    }
}

# Rate limit zones
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
```

---

## 3. Firewall (UFW)

### Configuración Base

```bash
#!/bin/bash
# scripts/security/setup_firewall.sh

# Reset UFW
sudo ufw --force reset

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH (limitar intentos)
sudo ufw limit ssh

# HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Docker internal (si es necesario)
# sudo ufw allow from 172.16.0.0/12

# Enable
sudo ufw --force enable

# Verify
sudo ufw status verbose
```

### Fail2ban

```ini
# /etc/fail2ban/jail.local

[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
```

---

## 4. Input Validation

### Django Forms

```python
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import bleach

class SafeContactForm(forms.Form):
    """Form con validación de seguridad."""

    name = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                r'^[a-zA-Z\s]+$',
                message='Solo letras y espacios permitidos'
            )
        ]
    )

    email = forms.EmailField()

    message = forms.CharField(
        widget=forms.Textarea,
        max_length=1000
    )

    def clean_message(self):
        """Sanitizar HTML/scripts del mensaje."""
        message = self.cleaned_data.get('message', '')
        # Remover tags HTML peligrosos
        return bleach.clean(
            message,
            tags=[],  # No permitir ningún tag
            strip=True
        )
```

### FastAPI Validation

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class UserInput(BaseModel):
    """Schema con validación estricta."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        regex=r'^[a-zA-Z0-9_]+$'
    )

    email: str = Field(..., max_length=254)

    @validator('email')
    def validate_email(cls, v):
        """Validación adicional de email."""
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('Email inválido')
        return v.lower()

    @validator('username')
    def no_sql_injection(cls, v):
        """Prevenir SQL injection básico."""
        dangerous = ["'", '"', ';', '--', '/*', '*/']
        if any(char in v for char in dangerous):
            raise ValueError('Caracteres no permitidos')
        return v
```

---

## 5. Authentication Security

### Protección de Login

```python
# Usando django-axes
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(hours=1)
AXES_LOCK_OUT_AT_FAILURE = True
AXES_LOCKOUT_TEMPLATE = 'account/locked.html'
AXES_RESET_ON_SUCCESS = True

# Logging de intentos
AXES_HANDLER = 'axes.handlers.database.AxesDatabaseHandler'
```

### Session Security

```python
# Regenerar session ID después de login
from django.contrib.auth import login as auth_login

def secure_login(request, user):
    """Login con regeneración de session."""
    auth_login(request, user)
    request.session.cycle_key()  # Nueva session ID
```

### CSRF Protection

```python
# views.py
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

@ensure_csrf_cookie
def get_csrf_token(request):
    """Endpoint para obtener CSRF token (SPAs)."""
    return JsonResponse({'detail': 'CSRF cookie set'})

# En templates
{% csrf_token %}

# En AJAX (jQuery)
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
```

---

## 6. SQL Injection Prevention

### ORM Siempre

```python
# ❌ NUNCA: SQL crudo con interpolación
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ❌ NUNCA: format() en queries
query = "SELECT * FROM products WHERE name = '{}'".format(name)

# ✅ SIEMPRE: ORM
user = User.objects.get(id=user_id)

# ✅ Si raw SQL es necesario, parametrizar
cursor.execute(
    "SELECT * FROM users WHERE id = %s",
    [user_id]
)

# ✅ Extra con Raw
Product.objects.raw(
    'SELECT * FROM shop_product WHERE category_id = %s',
    [category_id]
)
```

---

## 7. XSS Prevention

### Templates

```html
<!-- ✅ Auto-escape (default en Django) -->
{{ user_input }}

<!-- ❌ PELIGROSO: Deshabilitar escape -->
{{ user_input|safe }}  <!-- Solo si el contenido es 100% confiable -->

<!-- ✅ Escape explícito -->
{{ user_input|escape }}

<!-- ✅ Para JavaScript -->
<script>
    var data = {{ json_data|escapejs }};
</script>
```

### JSON Responses

```python
from django.http import JsonResponse

def api_response(request):
    # JsonResponse escapa automáticamente
    return JsonResponse({
        'message': user_input,  # Escapado
    })
```

---

## 8. File Upload Security

```python
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import magic

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'pdf']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_file(file):
    """Validación completa de archivo."""

    # Validar extensión
    ext = file.name.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'Extensión no permitida: {ext}')

    # Validar tamaño
    if file.size > MAX_FILE_SIZE:
        raise ValidationError('Archivo muy grande (max 5MB)')

    # Validar MIME type real
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)

    allowed_mimes = ['image/jpeg', 'image/png', 'application/pdf']
    if mime not in allowed_mimes:
        raise ValidationError(f'Tipo de archivo no permitido: {mime}')

    return True
```

---

## 9. Logging Security

### Django Logging Config

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'security': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/croody/security.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'security',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'axes': {
            'handlers': ['security_file'],
            'level': 'WARNING',
        },
    },
}
```

### Qué Loggear

```python
import logging

security_logger = logging.getLogger('django.security')

# ✅ Loggear
security_logger.warning(f"Failed login attempt for user: {username}")
security_logger.warning(f"Suspicious request from IP: {ip}")
security_logger.error(f"CSRF validation failed for: {request.path}")

# ❌ NUNCA loggear
logger.info(f"User {username} logged in with password {password}")  # NUNCA
logger.debug(f"Token: {secret_token}")  # NUNCA
logger.info(f"Credit card: {card_number}")  # NUNCA
```

---

## 10. Secrets Management

### Environment Variables

```python
# settings.py
import os
from pathlib import Path

# ✅ BIEN: Desde environment
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
STRIPE_KEY = os.environ.get('STRIPE_SECRET_KEY')

# ❌ MAL: Hardcodeado
SECRET_KEY = 'my-super-secret-key-123'  # NUNCA
```

### .env File

```bash
# .env (NUNCA commitear)
DJANGO_SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://user:pass@host:5432/db
STRIPE_SECRET_KEY=sk_live_xxx

# .gitignore
.env
*.pem
*.key
secrets/
```

---

## 11. Docker Security

### Dockerfile

```dockerfile
# Usar imagen oficial slim
FROM python:3.11-slim

# No correr como root
RUN useradd -m -u 1000 croody
USER croody

# No instalar packages innecesarios
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1
```

### docker-compose.prod.yml

```yaml
services:
  web:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

---

## Checklist de Auditoría

```markdown
## Pre-Deploy Security Checklist

### Django
- [ ] DEBUG = False
- [ ] SECRET_KEY único y desde env
- [ ] ALLOWED_HOSTS configurado
- [ ] Todas las SECURE_* settings habilitadas
- [ ] PASSWORD_VALIDATORS configurados
- [ ] CSRF habilitado

### Nginx
- [ ] SSL/TLS configurado (TLS 1.2+)
- [ ] HSTS habilitado
- [ ] Headers de seguridad presentes
- [ ] Rate limiting configurado
- [ ] server_tokens off

### Infrastructure
- [ ] Firewall configurado (UFW)
- [ ] Fail2ban activo
- [ ] Logs configurados
- [ ] Backups automáticos

### Code
- [ ] No SQL raw sin parametrizar
- [ ] Input validation en todos los forms
- [ ] File upload validation
- [ ] No secrets en código
- [ ] Dependencias actualizadas
```

---

## Recursos

- **OWASP Top 10**: https://owasp.org/Top10/
- **Django Security**: https://docs.djangoproject.com/en/5.0/topics/security/
- **Mozilla Observatory**: https://observatory.mozilla.org/
- **SSL Labs**: https://www.ssllabs.com/ssltest/
