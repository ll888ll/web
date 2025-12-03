# Security Hardening - Documentación Completa

## Resumen
La implementación de seguridad de Croody utiliza un enfoque multi-capa que incluye headers HTTP de seguridad (HSTS, CSP, X-Frame-Options), configuración SSL/TLS, firewall con iptables/UFW, hardening de sistema, monitoreo de seguridad y protección contra ataques comunes (DDoS, XSS, CSRF). Implementa mejores prácticas de OWASP y CIS Benchmarks.

## Ubicación
- **Nginx Config**: `/proyecto_integrado/gateway/nginx.conf`, `/proyecto_integrado/gateway/nginx.prod.conf`
- **Django Settings**: `/proyecto_integrado/Croody/croody/settings.py` (líneas 136-145)
- **Security Scripts**: `/scripts/security/`
  - `hardening_auto.sh` - Hardening automático del sistema
  - `setup_firewall.sh` - Configuración de firewall
  - `security_logger.py` - Logger centralizado de eventos de seguridad
- **SSL Certificates**: `/proyecto_integrado/gateway/ssl/`, `/proyecto_integrado/ssl/`

## Arquitectura de Seguridad

### Diagrama de Capas
```
┌─────────────────────────────────────────────────────────────────┐
│                        CAPA 1: PERÍMETRO                       │
├─────────────────────────────────────────────────────────────────┤
│  Cloudflare / Load Balancer                                     │
│  - DDoS Protection                                              │
│  - WAF (Web Application Firewall)                               │
│  - Rate Limiting                                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    CAPA 2: WEB SERVER                           │
├─────────────────────────────────────────────────────────────────┤
│  Nginx (Reverse Proxy)                                          │
│  - SSL/TLS Termination (TLS 1.2/1.3)                           │
│  - Security Headers                                             │
│  - Rate Limiting (100-150 req/s)                               │
│  - Request ID Tracking                                          │
│  - gzip Compression                                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                  CAPA 3: APPLICATION                            │
├─────────────────────────────────────────────────────────────────┤
│  Django Framework                                               │
│  - CSRF Protection                                              │
│  - XSS Protection                                               │
│  - SQL Injection Prevention                                     │
│  - HSTS Headers                                                 │
│  - Secure Cookies                                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                  CAPA 4: FIREWALL                              │
├─────────────────────────────────────────────────────────────────┤
│  iptables / UFW                                                 │
│  - Default DROP Policy                                          │
│  - SYN Flood Protection                                         │
│  - Rate Limiting per IP                                         │
│  - Port Blocking                                                │
│  - Invalid Packet Drop                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   CAPA 5: MONITORING                            │
├─────────────────────────────────────────────────────────────────┤
│  Security Logger                                                │
│  - Centralized Logging                                          │
│  - Event Tracking                                               │
│  - Incident Response                                            │
│  - Audit Trails                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Security Headers

### HTTP Strict Transport Security (HSTS)

#### Nginx Configuration
```nginx
# Desarrollo
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# Producción (nginx.prod.conf)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

#### Django Settings
```python
# settings.py
if not DEBUG:
    # ... otras configs
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = False
```

**Propósito**:
- **max-age=31536000**: Fuerza HTTPS por 1 año (31536000 segundos)
- **includeSubDomains**: Aplica a todos los subdominios
- **Preload**: Permite precarga en navegadores (opcional, requiere verificación)

**Beneficios**:
- Previene ataques Man-in-the-Middle (MITM)
- Fuerza conexión HTTPS incluso si usuario escribe http://
- Protección contra SSL stripping attacks

**Verificación**:
```bash
# Verificar HSTS header
curl -I https://croody.app | grep Strict-Transport-Security

# Test HSTS preload
# https://hstspreload.org/
```

### Content Security Policy (CSP)

#### Nginx Configuration
```nginx
# Política general (base)
add_header Content-Security-Policy "default-src 'self' 'unsafe-inline' data: https:; object-src 'none'; frame-ancestors 'self';";

# Política específica para APIs con Swagger/ReDoc
location = /api/telemetry/docs {
  add_header Content-Security-Policy "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: https:; object-src 'none'; frame-ancestors 'self'";
  proxy_pass http://telemetry_upstream/docs;
}
```

#### CSP Directives

| Directiva | Valor | Propósito |
|-----------|-------|-----------|
| `default-src` | `'self'` 'unsafe-inline' data: https: | Política por defecto |
| `object-src` | `'none'` | Bloquea `<object>`, `<embed>`, `<applet>` |
| `frame-ancestors` | `'self'` | Previene clickjacking (permite solo frames del mismo origen) |
| `unsafe-inline` | N/A | Permite scripts inline (⚠️ evaluar remover en producción) |
| `unsafe-eval` | N/A | Permite `eval()` (solo para Swagger/ReDoc) |

**Beneficios**:
- **XSS Prevention**: Bloquea ejecución de scripts no autorizados
- **Clickjacking Protection**: Previene embedding malicioso
- **Data Injection**: Controla fuentes de datos permitidas

**Política Recomendada Producción**:
```nginx
# Sin 'unsafe-inline' para máximo security
add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https:; frame-ancestors 'self'; object-src 'none'";
```

### X-Frame-Options

#### Nginx Configuration
```nginx
add_header X-Frame-Options SAMEORIGIN;
```

#### Apache Configuration (hardening_auto.sh)
```apache
Header always set X-Frame-Options "DENY"
```

**Valores**:
- `DENY`: Bloquea framing completamente (más seguro)
- `SAMEORIGIN`: Permite frames solo del mismo origen (flexible)
- `ALLOW-FROM uri`: Permitir framing desde URI específico (deprecated, usar CSP)

**Uso**:
- Previene clickjacking attacks
- Protege contra UI redressing
- Bloquea sitios maliciosos que intentan frames de la aplicación

### X-Content-Type-Options

#### Nginx Configuration
```nginx
add_header X-Content-Type-Options nosniff;
```

**Propósito**:
- Previene MIME type sniffing
- Obliga al browser a respetar Content-Type headers
- Bloquea carga de scripts con contenido incorrecto

**Ataque Prevenido**:
```html
<!-- Malicioso: servir JS como imagen -->
<img src="malicious-script.js">
<!-- Con nosniff: browser no ejecutará el JS -->
```

### Referrer Policy

#### Nginx Configuration
```nginx
add_header Referrer-Policy no-referrer-when-downgrade;
```

**Valores**:
- `no-referrer`: Nunca envía referrer
- `no-referrer-when-downgrade`: Envía referrer solo en HTTPS→HTTPS
- `strict-origin-when-cross-origin`: Más estricto, recomendado
- `same-origin`: Envía referrer solo para mismo origen

**Beneficios**:
- Privacidad: Evita filtrar URLs sensibles en referrer
- Seguridad: No revela estructura interna de URLs

### X-XSS-Protection (Deprecated)

#### Apache Configuration
```apache
Header always set X-XSS-Protection "1; mode=block"
```

**Nota**: Header deprecated, usar CSP en su lugar

**Funcionalidad**:
- Habilita filtro XSS del browser
- `mode=block`: Bloquea página completa si detecta XSS

### Custom Headers

#### Request ID Tracking
```nginx
add_header X-Request-ID $req_id;
```

**Variables en nginx.conf**:
```nginx
map $http_x_request_id $req_id { default $http_x_request_id; }
```

**Beneficios**:
- Tracing de requests a través de múltiples servicios
- Debugging facilitado
- Correlación con logs de aplicación
- Auditoría de requests

## SSL/TLS Configuration

### Nginx SSL Configuration

#### Desarrollo (nginx.conf)
```nginx
server {
    listen 80;
    listen 443 ssl;
    server_name _;

    # TLS dev (self-signed)
    ssl_certificate     /etc/nginx/ssl/dev.crt;
    ssl_certificate_key /etc/nginx/ssl/dev.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;
}
```

#### Producción (nginx.prod.conf)
```nginx
server {
    listen 443 ssl http2;
    server_name croody.app www.croody.app;

    # Let's Encrypt certificates
    ssl_certificate     /etc/letsencrypt/live/croody.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/croody.app/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

#### SSL Configuration Details

**Protocolos**:
- `TLSv1.2`: Mínimo recomendado (PCI DSS compliance)
- `TLSv1.3`: Última versión, mejor performance y security

**Ciphers**:
```bash
# Ciphers fuertes (HIGH)
HIGH:!aNULL:!MD5
```

**HTTP/2**:
```nginx
listen 443 ssl http2;
```
- Multiplexing de requests
- Header compression
- Server push
- Mejor performance

**Redirect HTTP to HTTPS**:
```nginx
server {
    listen 80;
    server_name croody.app www.croody.app;

    location ^~ /.well-known/acme-challenge/ {
        root /var/www/certbot;
        default_type "text/plain";
        allow all;
    }

    location / { return 301 https://$host$request_uri; }
}
```

### Let's Encrypt SSL

#### Certbot Auto-Configuration
```bash
# En hardening_auto.sh
certbot --apache \
  --non-interactive \
  --agree-tos \
  --no-eff-email \
  --email mnzz.eafit@gmail.com \
  --redirect \
  --hsts \
  --staple-ocsp \
  -d croody.app \
  -d www.croody.app
```

**Flags**:
- `--redirect`: Auto-redirect HTTP→HTTPS
- `--hsts`: Habilita HSTS
- `--staple-ocsp`: OCSP Stapling (certificado online status)

**Auto-renovación**:
```bash
# Certbot añade cron job automáticamente
cat /etc/cron.d/certbot
```

**Manual renewal**:
```bash
# Verificar expiración
certbot certificates

# Renovar
certbot renew --quiet
```

### SSL Labs Testing

```bash
# Test SSL configuration
# https://www.ssllabs.com/ssltest/

# Verificación manual
openssl s_client -connect croody.app:443 -servername croody.app
```

**Objetivo**: Calificación A+ en SSL Labs

## Rate Limiting

### Nginx Rate Limiting

#### Development (nginx.conf)
```nginx
limit_req_zone $binary_remote_addr zone=api_zone:10m rate=100r/s;

location /api/telemetry/ {
    limit_req zone=api_zone burst=100 nodelay;
}
```

#### Production (nginx.prod.conf)
```nginx
limit_req_zone $binary_remote_addr zone=api_zone:20m rate=150r/s;

location /api/telemetry/ {
    limit_req zone=api_zone burst=150 nodelay;
}
```

**Configuración**:
- **Zone size**: 10m-20m (memoria compartida)
- **Rate**: 100-150 requests/second
- **Burst**: 100-150 requests adicionales permitidas
- **nodelay**: No delayed processing (fair queuing)

**Beneficios**:
- Previene API abuse
- Mitiga DDoS attacks
- Protege contra brute force
- Garantiza fair resource usage

#### Rate Limiting por Ubicación

| Location | Rate | Burst | Propósito |
|----------|------|-------|-----------|
| `/api/telemetry/` | 150 r/s | 150 | API endpoints |
| `/api/ids/` | 150 r/s | 150 | API endpoints |
| `/` | Default | Default | Web app |

### iptables Rate Limiting

#### Script: setup_firewall.sh
```bash
# SYN Flood Protection
iptables -A INPUT -p tcp --syn -m limit --limit 40/second --limit-burst 80 -j ACCEPT
iptables -A INPUT -p tcp --syn -j LOG --log-prefix "SYN-FLOOD "
iptables -A INPUT -p tcp --syn -j DROP

# UDP DoS Protection
iptables -A INPUT -p udp -m hashlimit --hashlimit-above 25/sec --hashlimit-burst 50 --hashlimit-mode srcip --hashlimit-name udp-dos -j LOG --log-prefix "UDP-DOS "
iptables -A INPUT -p udp -m hashlimit --hashlimit-above 25/sec --hashlimit-burst 50 --hashlimit-mode srcip --hashlimit-name udp-dos -j DROP

# SSH Rate Limiting
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m limit --limit 4/min --limit-burst 4 -j ACCEPT
```

**Protecciones**:
- **SYN Flood**: 40/second, burst 80
- **UDP Flood**: 25/sec, burst 50
- **SSH Brute Force**: 4/minute, burst 4

## Firewall Configuration

### UFW (Uncomplicated Firewall)

#### Script: hardening_auto.sh
```bash
configure_ufw() {
    log "Aplicando políticas UFW"
    ufw --force enable
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw deny 22/tcp
}
```

**Políticas**:
- **Default**: Deny incoming
- **Allow 80**: HTTP traffic
- **Allow 443**: HTTPS traffic
- **Deny 22**: SSH bloqueado (usar bastion)

**Recomendación Producción**:
```bash
# Permitir SSH solo desde IPs específicas
ufw allow from 203.0.113.0/24 to any port 22
```

### iptables Rules

#### Script: setup_firewall.sh

##### Base Policies
```bash
# Políticas por defecto
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Permitir tráfico establecido/relacionado
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Permitir loopback
iptables -A INPUT -i lo -j ACCEPT
```

##### Service Allow Rules
```bash
# Permitir servicios
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m limit --limit 4/min --limit-burst 4 -j ACCEPT
iptables -A INPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate NEW -j ACCEPT
iptables -A INPUT -p udp --dport 443 -m conntrack --ctstate NEW -j ACCEPT
```

##### Invalid Packet Protection
```bash
# Bloquear paquetes inválidos
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
iptables -A INPUT -p tcp --tcp-flags SYN,RST SYN,RST -j DROP
```

**Ataques Prevenidos**:
- **NULL packets**: Paquetes con flags inválidos
- **XMAS packets**: Todos los flags activados
- **Stealth scans**: Diversos tipos de port scanning

### System Hardening

#### sysctl Configuration
```bash
configure_sysctl(){
    # Habilitar SYN cookies
    sysctl -w net.ipv4.tcp_syncookies=1

    # Backlog para SYN
    sysctl -w net.ipv4.tcp_max_syn_backlog=4096

    # Reverse path filtering
    sysctl -w net.ipv4.conf.all.rp_filter=1
    sysctl -w net.ipv4.conf.default.rp_filter=1
}
```

**Configuraciones**:
- **SYN Cookies**: Protege contra SYN flood attacks
- **TCP Max SYN Backlog**: Maneja conexiones incompletas
- **Reverse Path Filtering**: Previene spoofing de IP

## Django Security Settings

### settings.py Security Configuration
```python
if not DEBUG:
    # === SECURITY SETTINGS ===
    SESSION_COOKIE_SECURE = True          # Cookies de sesión solo HTTPS
    CSRF_COOKIE_SECURE = True             # CSRF cookie solo HTTPS
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True # HSTS para subdominios
    SECURE_HSTS_PRELOAD = False           # HSTS preload (opcional)
    SECURE_SSL_REDIRECT = False           # TLS en gateway, no redirección doble
    SECURE_BROWSER_XSS_FILTER = True      # Filtro XSS del browser
    SECURE_CONTENT_TYPE_NOSNIFF = True    # No MIME sniffing
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

**Configuraciones Explicadas**:

#### Session & CSRF Cookies
```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```
- **Propósito**: Cookies solo se envían via HTTPS
- **Beneficio**: Previene interceptación de cookies en HTTP

#### HSTS Settings
```python
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False
```
- **Propósito**: Fuerza HTTPS en cliente
- **Include Subdomains**: Aplica a *.croody.app
- **Preload**: Registra en browser preload list (⚠️ reversible?)

#### SSL Redirect
```python
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```
- **False**: Gateway maneja redirect, Django no
- **Proxy SSL Header**: Detecta HTTPS desde proxy/nginx

#### XSS & Content Type Protection
```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```
- **XSS Filter**: Habilita filtro XSS del browser
- **NoSniff**: Previene MIME sniffing (como nginx header)

### CSRF Protection

#### CSRF Token in Forms
```html
<!-- Django template -->
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

**Verificación**:
```python
# Django middleware
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    # ...
]
```

**Beneficios**:
- Previene Cross-Site Request Forgery
- Token único por sesión
- Validación server-side

### Exempting CSRF (Solo APIs)
```python
# En views.py
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(['POST'])
def cart_add_api(request):
    # API endpoint sin CSRF
    # Solo si es realmente necesario y seguro
```

**⚠️ ADVERTENCIA**: Solo exempt endpoints que no modifican datos o tienen protección alternativa

## System Hardening

### Apache Hardening

#### Script: hardening_auto.sh

##### Security Configuration
```apache
# /etc/apache2/conf-available/security.conf
ServerTokens Prod           # Solo muestra "Apache" (no versión)
ServerSignature Off         # No firma del server en error pages
TraceEnable Off            # Deshabilita TRACE method
FileETag None              # No expone ETag en static files

# Headers
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "DENY"
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"

# Limitar métodos HTTP
<LimitExcept GET POST HEAD>
    Require all denied
</LimitExcept>

# Timeouts para prevenir DoS
Timeout 60
KeepAlive On
MaxKeepAliveRequests 100
KeepAliveTimeout 5
```

**Server Tokens**: `Prod` vs `Full` vs `Minimal`
```bash
# ❌ ServerTokens Full (expone versión)
Server: Apache/2.4.41 (Ubuntu)

# ✅ ServerTokens Prod (seguro)
Server: Apache
```

**Deshabilitar TRACE**:
- Previene Cross-Site Tracing (XST) attacks
- TRACE method permite reflection de requests

**Limit HTTP Methods**:
```apache
# Solo GET, POST, HEAD permitidos
# Bloquea: PUT, DELETE, PATCH, OPTIONS, TRACE, CONNECT
<LimitExcept GET POST HEAD>
    Require all denied
</LimitExcept>
```

### ModSecurity + OWASP CRS

#### ModSecurity Configuration
```bash
configure_modsecurity() {
    # Copiar configuración recomendada
    cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf

    # Habilitar rule engine
    sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/modsecurity/modsecurity.conf

    # Configurar OWASP CRS
    if [[ -d /usr/share/modsecurity-crs ]]; then
        cp /usr/share/modsecurity-crs/crs-setup.conf.example /usr/share/modsecurity-crs/crs-setup.conf
        ln -sf /usr/share/modsecurity-crs/rules /etc/modsecurity/
    fi
}
```

**OWASP CRS (Core Rule Set)**:
- WAF rules pre-configuradas
- Protección contra OWASP Top 10
- SQL Injection, XSS, Local File Inclusion, etc.

**Verificación**:
```bash
# Test ModSecurity
curl -H "User-Agent: () { :; }; echo; echo vulnerable" http://croody.app

# Ver logs
tail -f /var/log/apache2/error.log
```

## Logging y Monitoreo

### Security Logger (Python)

#### Script: security_logger.py
```python
#!/usr/bin/env python3
"""Registro centralizado de eventos de seguridad para Croody."""

from datetime import datetime, timezone

LOG_PATH = Path(__file__).resolve().parent.parent / "proyecto_integrado" / "Croody" / "security" / "logs" / "eventos_seguridad.txt"

def log_event(event_type: str, ip: str, proto: str, action: str, detail: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    line = f"[{timestamp}] | {event_type} | ip={ip} | protocolo={proto.upper()} | accion={action} | detalle={detail}\n"
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(line)
```

**Uso**:
```bash
# Log evento
python3 security_logger.py "SYN-FLOOD" "192.0.2.1" "tcp" "bloqueado" "Rate limiting activado"

# Resultado en log
[2025-12-02T10:30:00Z] | SYN-FLOOD | ip=192.0.2.1 | protocolo=TCP | accion=bloqueado | detalle=Rate limiting activado
```

**Tipos de Eventos**:
- `SYN-FLOOD`
- `UDP-DOS`
- `BRUTE-FORCE`
- `INVALID-PACKET`
- `XSS-ATTEMPT`
- `SQL-INJECTION-ATTEMPT`

### Nginx Access Logs

#### Formato JSON
```nginx
log_format json_combined escape=json '{"time":"$time_iso8601","remote":"$remote_addr","method":"$request_method","uri":"$request_uri","status":$status,"bytes":$bytes_sent,"req_id":"$req_id","ua":"$http_user_agent","rt":$request_time,"u_rt":"$upstream_response_time"}';

access_log /dev/stdout json_combined;
```

**Campos**:
- **time**: Timestamp ISO8601
- **remote**: IP del cliente
- **method**: HTTP method (GET, POST, etc.)
- **uri**: Request URI
- **status**: HTTP status code
- **bytes**: Bytes enviados
- **req_id**: Request ID único
- **ua**: User Agent
- **rt**: Request time (total)
- **u_rt**: Upstream response time

**Análisis**:
```bash
# Detectar rate limit violations
grep "429" /var/log/nginx/access.log

# Top IPs por requests
awk '{print $2}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -20

# Requests por endpoint
awk '{print $4}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -20
```

### Systemd Monitor Service

#### Script: hardening_auto.sh
```bash
deploy_monitor_script() {
    # Crear servicio systemd
    cat >"$MONITOR_SERVICE" <<'EOF'
[Unit]
Description=Monitor de seguridad Croody
After=apache2.service

[Service]
Type=simple
ExecStart=/usr/local/bin/monitor_seguridad.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable --now monitor-seguridad.service
}
```

**Monitor Script** (referencia):
- Monitorea logs de seguridad
- Detecta patrones anómalos
- Envía alertas
- Automatiza respuesta

### Log Locations

| Servicio | Log Path | Propósito |
|----------|----------|-----------|
| **Nginx** | `/var/log/nginx/access.log` | Access log JSON |
| **Nginx** | `/var/log/nginx/error.log` | Error log |
| **Apache** | `/var/log/apache2/access.log` | Access log |
| **Apache** | `/var/log/apache2/error.log` | Error log |
| **Django** | `/var/log/croody.log` | Application log |
| **Security** | `/var/log/croody_hardening.log` | Hardening actions |
| **UFW** | `/var/log/ufw.log` | Firewall log |
| **iptables** | `kernel log` | Firewal log (dmesg) |

## SSL Certificate Management

### Certbot Auto-Renewal

#### Automatic Renewal
```bash
# Certbot añade cron job
cat /etc/cron.d/certbot
# 0 12 * * * /usr/bin/certbot renew --quiet
```

**Renewal Process**:
1. Verifica expiración 30 días antes
2. Renueva automáticamente si está cerca de expirar
3. Recarga nginx/apache al renovar

#### Manual Renewal
```bash
# Ver certificados
certbot certificates

# Renovar
certbot renew --quiet

# Test renew (dry-run)
certbot renew --dry-run
```

### Certificate Chain

#### Let's Encrypt Chain
```
fullchain.pem
├── leaf_certificate.crt (croody.app)
└── intermediate_cert.pem (Let's Encrypt Authority X3)
    └── root_cert.pem (ISRG Root X1) [self-signed, usually not included]
```

**Verification**:
```bash
# Verificar chain
openssl s_client -connect croody.app:443 -servername croody.app \
  -showcerts < /dev/null 2>/dev/null | openssl x509 -text -noout

# Check expiration
echo | openssl s_client -connect croody.app:443 2>/dev/null | openssl x509 -noout -dates
```

### SSL Testing Tools

#### SSL Labs
```bash
# Test online: https://www.ssllabs.com/ssltest/
# Objetivo: Calificación A o A+

# Tests:
# - Protocol support (TLS 1.2, 1.3)
# - Cipher strength
# - HSTS enabled
# - Certificate chain valid
# - No vulnerabilities (POODLE, BEAST, etc.)
```

#### OpenSSL Manual Test
```bash
# Test protocolo
openssl s_client -connect croody.app:443 -tls1_2
openssl s_client -connect croody.app:443 -tls1_3

# Test cipher suites
openssl s_client -connect croody.app:443 -cipher 'HIGH'

# Verificar HSTS
curl -I https://croody.app | grep Strict-Transport-Security
```

## Security Automation

### Hardening Script

#### Script: hardening_auto.sh
```bash
#!/usr/bin/env bash
# Automatiza el endurecimiento básico documentado para el sitio Croody.

main() {
    require_root
    ensure_supported_system
    log "== Inicio de endurecimiento automático Croody =="
    apt_update
    install_dependencies
    enable_apache
    write_security_conf
    lock_server_status
    configure_ufw
    configure_rate_limiting
    deploy_monitor_script
    deploy_backup_script
    configure_modsecurity
    obtain_cert
    reload_apache
    log "== Endurecimiento completado =="
}
```

**Ejecución**:
```bash
# Ejecutar como root
sudo ./scripts/security/hardening_auto.sh

# Ver logs
tail -f /var/log/croody_hardening.log
```

### Deployment Integration

#### docker-compose.yml Integration
```yaml
services:
  gateway:
    image: nginx:alpine
    volumes:
      - ./gateway/nginx.prod.conf:/etc/nginx/conf.d/default.conf:ro
      - letsencrypt:/etc/letsencrypt:ro
      - certbot-www:/var/www/certbot:ro
```

#### CI/CD Integration
```yaml
# .github/workflows/deploy-selfhosted.yml
- name: Apply security hardening
  run: |
    sudo ./scripts/security/hardening_auto.sh
    sudo ./scripts/security/setup_firewall.sh
```

## Attack Prevention

### SQL Injection Prevention

#### Django ORM Protection
```python
# ✅ Bien: ORM queries (protegidas)
Product.objects.filter(name__icontains=query)

# ❌ Mal: Raw SQL (vulnerable)
Product.objects.raw(f"SELECT * FROM shop_product WHERE name LIKE '%{query}%'")
```

**Django ORM Features**:
- Parameterized queries
- Automatic escaping
- SQL injection prevention by design

### XSS Prevention

#### Template Auto-escaping
```html
<!-- Django template: auto-escape -->
{{ user_input }}
<!-- Sin necesidad de escaping manual -->
```

#### CSP Additional Protection
```nginx
# Política estricta
add_header Content-Security-Policy "default-src 'self'; script-src 'self'";
```

### CSRF Prevention

#### Form Protection
```python
# Django middleware automático
MIDDLEWARE = ['django.middleware.csrf.CsrfViewMiddleware']
```

#### AJAX Requests
```javascript
// Incluir CSRF token en AJAX
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
});
```

### Clickjacking Prevention

#### X-Frame-Options
```nginx
add_header X-Frame-Options SAMEORIGIN;
```

#### CSP frame-ancestors
```nginx
add_header Content-Security-Policy "frame-ancestors 'self'";
```

### Directory Traversal Prevention

#### Nginx Protection
```nginx
# Bloquear .. en paths
location ~ /\.\. {
    deny all;
}
```

#### Django Upload Validation
```python
# Validar nombre de archivo
from pathlib import Path

def validate_filename(filename):
    # Bloquear paths relativos
    if Path(filename).is_absolute():
        raise ValidationError("Absolute paths not allowed")

    # Bloquear ..
    if '..' in filename:
        raise ValidationError("Directory traversal not allowed")
```

### Command Injection Prevention

#### No Shell Execution
```python
# ❌ Mal: subprocess con user input
subprocess.run(f"ping {user_input}", shell=True)

# ✅ Bien: subprocess lista
subprocess.run(['ping', user_input])
```

#### Django Management Commands
```python
# Validar argumentos
def add_arguments(self, parser):
    parser.add_argument('name', type=str, validators=[validate_safe_name])

def validate_safe_name(value):
    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
        raise ValidationError("Only alphanumeric, underscore, hyphen allowed")
```

## Security Testing

### Vulnerability Scanning

#### Nikto
```bash
# Scan web application
nikto -h https://croody.app

# Scan specific ports
nikto -h croody.app -p 80,443
```

#### Nmap
```bash
# Port scan
nmap -sS -sV -O croody.app

# Vuln scan (with NSE scripts)
nmap --script vuln croody.app
```

#### SSLyze
```bash
# SSL/TLS assessment
sslyze --regular croody.app

# Test specific features
sslyze --certinfo=basic --http_headers croody.app
```

### Penetration Testing

#### OWASP ZAP
```bash
# Docker run ZAP
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://croody.app

# Full scan
docker run -t owasp/zap2docker-stable zap-full-scan.py -t https://croody.app
```

#### SQLMap
```bash
# Test SQL injection
sqlmap -u "https://croody.app/api/endpoint?id=1" --batch --risk=3

# Dump database
sqlmap -u "https://croody.app/api/endpoint?id=1" --dump
```

### Security Headers Testing

#### SecurityHeaders.com
```bash
# Online tool: https://securityheaders.com/
# Test URL: https://croody.app

# Objetivo: A+ grade
```

#### curl Testing
```bash
# Test all security headers
curl -I https://croody.app | grep -E "(Strict-Transport-Security|Content-Security-Policy|X-Frame-Options|X-Content-Type-Options|Referrer-Policy)"

# Test HSTS
curl -I https://croody.app | grep Strict-Transport-Security
# Expected: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

# Test CSP
curl -I https://croody.app | grep Content-Security-Policy
# Expected: Content-Security-Policy: default-src 'self'...
```

## Compliance

### OWASP Top 10

| OWASP Top 10 (2021) | Croody Implementation |
|---------------------|----------------------|
| **A01: Broken Access Control** | Django auth + permission system |
| **A02: Cryptographic Failures** | TLS 1.2/1.3, HSTS, Secure cookies |
| **A03: Injection** | ORM, parameterized queries |
| **A04: Insecure Design** | Security by design, CSP, headers |
| **A05: Security Misconfiguration** | Hardening scripts, security headers |
| **A06: Vulnerable Components** | Regular updates, dependency scanning |
| **A07: Identification Failures** | Django session management, CSRF |
| **A08: Software Integrity Failures** | CI/CD, code signing |
| **A09: Logging Failures** | Comprehensive logging system |
| **A10: SSRF** | Input validation, proxy restrictions |

### PCI DSS (Si aplica)

```python
# Si se manejan tarjetas de crédito
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

### GDPR Compliance

```python
# Cookies de analytics solo con consentimiento
COOKIE_BANNER = True

# Data encryption
DATA_ENCRYPTION = True
```

## Troubleshooting

### SSL Certificate Issues

#### Certificate Not Renewed
```bash
# Verificar cron job
systemctl status certbot.timer

# Manual renewal
certbot renew --verbose

# Verificar logs
tail -f /var/log/letsencrypt/letsencrypt.log
```

#### Mixed Content Errors
```html
<!-- ❌ Mal: HTTP resource en HTTPS page -->
<script src="http://cdn.example.com/script.js">

<!-- ✅ Bien: HTTPS resource -->
<script src="https://cdn.example.com/script.js">
```

#### HSTS Preload Issues
```bash
# Verificar HSTS preload
https://hstspreload.org/

# Si hay error:
# 1. Remover preload con cuidado
# 2. Esperar TTL
# 3. Re-apply
```

### Security Header Issues

#### Header Not Set
```bash
# Verificar configuración nginx
nginx -t

# Recargar nginx
docker compose exec gateway nginx -s reload

# Ver headers en response
curl -I https://croody.app
```

#### CSP Violations
```javascript
// Browser console errors
// Ref: Content-Security-Policy directive violated

// Solución: Añadir dominio a whitelist
add_header Content-Security-Policy "default-src 'self' https://cdn.example.com";
```

### Firewall Issues

#### Locked Out SSH
```bash
# Desde bastion host
ssh user@private-ip

# O via AWS Console
# EC2 > Instances > Connect > Session Manager

# Restore SSH access
ufw allow from YOUR_IP/32 to any port 22
```

#### Service Not Accessible
```bash
# Verificar rules
iptables -L -n -v

# UFW status
ufw status

# Test port connectivity
telnet croody.app 80
telnet croody.app 443
```

### Rate Limiting Issues

#### False Positives
```nginx
# Aumentar rate limit
limit_req zone=api_zone rate=200r/s burst=200;

# Whitelist specific IPs
geo $whitelist {
    default 0;
    203.0.113.0/24 1;
}

limit_req_zone $whitelist zone=api_zone:20m rate=1000r/s;
```

## Best Practices

### ✅ Hacer
```python
# 1. Siempre usar HTTPS en producción
SECURE_SSL_REDIRECT = True

# 2. Validar toda entrada
def validate_input(user_input):
    if not re.match(r'^[a-zA-Z0-9_-]+$', user_input):
        raise ValidationError("Invalid input")

# 3. Logging de seguridad
log_event("BRUTE-FORCE", ip, "tcp", "blocked", "Multiple failed logins")

# 4. Headers de seguridad
add_header X-Content-Type-Options "nosniff";
add_header X-Frame-Options "DENY";

# 5. Dependency updates
pip install --upgrade pip
pip-audit --fix

# 6. Secrets management
# Nunca hardcodear secrets
DATABASE_PASSWORD = os.getenv('DB_PASSWORD')

# 7. Principle of least privilege
# User minimal permissions
```

### ❌ Evitar
```python
# 1. No CSRF exemption sin razón
@csrf_exempt  # ❌ Solo para APIs públicas read-only
def unsafe_view(request):
    pass

# 2. No eval() o exec()
eval(user_input)  # ❌ Dangerous

# 3. No password en URL
https://user:pass@crocody.app  # ❌ Logs, caches

# 4. No SSLv3 o TLS 1.0
ssl_protocols TLSv1.2 TLSv1.3;  # ✅ Solo versiones seguras

# 5. No información en errores
# ❌ Mal
raise ValueError(f"DB connection failed: {db_password}")

# ✅ Bien
raise ValueError("Connection failed")
```

## Monitoring y Alertas

### Alert Rules

```bash
# /etc/security/monitoring/alerts.yml
rules:
  - name: high_failed_logins
    condition: "failed_logins > 10 in 5m"
    action: "block_ip"
    severity: "warning"

  - name: sql_injection_attempt
    condition: "match(regex, request, '(union|select|drop)')"
    action: "return_403"
    severity: "critical"

  - name: cert_expiring
    condition: "cert_days_remaining < 30"
    action: "email_alert"
    severity: "warning"
```

### Security Metrics

```bash
# Grafana Dashboard
# Métricas:
# - Failed login attempts
# - Requests per second
# - Error rate (4xx, 5xx)
# - Active connections
# - SSL certificate expiry
# - Security violations
```

## Referencias

### Archivos Relacionados
- `gateway/nginx.conf` - Configuración desarrollo
- `gateway/nginx.prod.conf` - Configuración producción
- `scripts/security/hardening_auto.sh` - Hardening automático
- `scripts/security/setup_firewall.sh` - Firewall configuration
- `scripts/security/security_logger.py` - Security logger
- `Croody/croody/settings.py` - Django security settings

### Documentación Externa
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [Mozilla Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)

### Tools
- [SecurityHeaders.com](https://securityheaders.com/) - Security headers test
- [SSL Labs](https://www.ssllabs.com/ssltest/) - SSL/TLS assessment
- [HSTS Preload](https://hstspreload.org/) - HSTS preload check
- [OWASP ZAP](https://www.zaproxy.org/) - Security testing

## Ver También
- [Nginx Configuration](../04-DEVOPS/docker-compose.md#nginx-configuration)
- [CI/CD Security](../04-DEVOPS/ci-cd-workflows.md)
- [Infrastructure Security](../05-INFRAESTRUCTURA/terraform.md#security-hardening)
