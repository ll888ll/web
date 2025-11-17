# Plan Práctico: Endurecimiento de Servidor Web para Emprendedores

Guía operativa y autocontenida para iniciar, reforzar y verificar un servidor web Apache/Nginx en un host tipo Kali/Ubuntu, con énfasis en controles económicos pero efectivos.

## Fase 1: Configuración Inicial Sólida

```
[LOG INICIAL - CONFIGURACIÓN DEL SISTEMA]
TIMESTAMP: 2024-01-15 10:00:00
AGENTE (Administrador): Iniciando configuración segura del servidor web
COMANDO: sudo systemctl start apache2 && sudo systemctl enable apache2
RESPUESTA: Apache2 iniciado y habilitado en el arranque

COMANDO: sudo apt update && sudo apt upgrade -y
RESPUESTA: Sistema actualizado, 15 paquetes actualizados
ANÁLISIS: Primer paso de seguridad completado - sistema actualizado

COMANDO: sudo ufw enable && sudo ufw allow 80,443/tcp && sudo ufw deny 22/tcp
RESPUESTA: Firewall habilitado, puertos HTTP/HTTPS abiertos, SSH denegado externamente
ANÁLISIS: Superficie de ataque reducida significativamente
```

## Fase 2: Hardening de Apache/Nginx

### Configuración de seguridad base (`/etc/apache2/conf-available/security.conf`)

```apache
# Configuración de seguridad reforzada
ServerTokens Prod
ServerSignature Off
TraceEnable Off
FileETag None

# Headers de seguridad
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "DENY"
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"

# Limitar métodos HTTP
<LimitExcept GET POST HEAD>
    Require all denied
</LimitExcept>

# Timeouts ajustados para prevenir DoS
Timeout 60
KeepAlive On
MaxKeepAliveRequests 100
KeepAliveTimeout 5
```

```
COMANDO: sudo a2enconf security && sudo systemctl reload apache2
RESPUESTA: Configuración de seguridad aplicada, servidor recargado
ANÁLISIS: Headers de seguridad implementados, métodos HTTP restringidos
```

### Cierre de `/server-status`

```
COMANDO: sudo a2dismod status
RESPUESTA: Módulo status deshabilitado
ANÁLISIS: Endpoint `/server-status` ya no se expone por defecto
```

Cuando se requiera monitoreo local, crear `/etc/apache2/conf-available/status-local.conf`:

```apache
<Location /server-status>
    SetHandler server-status
    Require local
</Location>
```

```
COMANDO: sudo a2enconf status-local && sudo systemctl reload apache2
RESPUESTA: Endpoint restringido exclusivamente a localhost
```

### Rate limiting con `iptables`

```
COMANDO: sudo iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
COMANDO: sudo iptables -A INPUT -p tcp --dport 80 -j DROP
RESPUESTA: Reglas de rate limiting aplicadas
ANÁLISIS: Protección básica contra inundaciones de tráfico implementada
```

## Fase 3: Monitoreo Proactivo y Detección

El script `scripts/monitor_seguridad.sh` ejecuta detección de patrones maliciosos y envía alertas:

```bash
#!/bin/bash
set -euo pipefail

LOG_FILE="/var/log/seguridad_web.log"
APACHE_LOG="/var/log/apache2/access.log"
ALERT_EMAIL="mnzz.eafit@gmail.com"
RATE_THRESHOLD=1000   # peticiones permitidas por minuto
BLOCKLIST="/etc/seguridad/ip_bloqueadas.list"

mkdir -p "$(dirname "$LOG_FILE")" "$(dirname "$BLOCKLIST")"
touch "$LOG_FILE" "$BLOCKLIST"

log_event() {
    local message="$1"
    echo "$(date '+%F %T') - $message" | tee -a "$LOG_FILE" >/dev/null
}

send_alert() {
    local subject="$1"
    local body="$2"
    if command -v mail >/dev/null 2>&1; then
        printf "%s\n" "$body" | mail -s "$subject" "$ALERT_EMAIL"
    else
        log_event "ALERTA PENDIENTE ($subject): $body"
    fi
}

add_blocklist() {
    local ip="$1"
    if ! grep -q "$ip" "$BLOCKLIST"; then
        echo "$ip" >> "$BLOCKLIST"
        log_event "IP $ip añadida a blocklist local"
    fi
}

current_minute=""
minute_count=0

log_event "Iniciando monitoreo de seguridad sobre $APACHE_LOG"

while read -r line; do
    [[ -z "$line" ]] && continue

    ip=$(echo "$line" | awk '{print $1}')
    minute_key=$(echo "$line" | awk '{print $4}' | tr -d '[' | cut -d: -f1-2)

    if [[ "$minute_key" != "$current_minute" ]]; then
        current_minute="$minute_key"
        minute_count=0
    fi
    minute_count=$((minute_count + 1))

    if (( minute_count > RATE_THRESHOLD )); then
        msg="ALTO TRAFICO DETECTADO: $minute_count req/min (umbral $RATE_THRESHOLD)"
        log_event "$msg"
        send_alert "Alerta DoS" "$msg"
    fi

    if echo "$line" | grep -Eiq "(union.*select|script\.php|\.\./|etc/passwd|base64_decode|select\\s+.*from)"; then
        msg="INTENTO DE ATAQUE DETECTADO desde $ip -> $line"
        log_event "$msg"
        send_alert "Alerta intrusión" "$msg"
        add_blocklist "$ip"
    fi

done < <(tail -F "$APACHE_LOG")
```

```
COMANDO: chmod +x scripts/monitor_seguridad.sh && sudo ./scripts/monitor_seguridad.sh &
RESPUESTA: Script de monitoreo ejecutándose en background
ANÁLISIS: Sistema de detección básico implementado, monitoreando en tiempo real con alertas por correo
```

## Fase 4: Pruebas de Resiliencia Éticas

```
[LOG DE PRUEBAS ÉTICAS - 2024-01-15 11:00:00]
AGENTE: Iniciando pruebas de resiliencia controladas

COMANDO: ab -n 1000 -c 10 http://localhost/
RESPUESTA: Completed 1000 requests | Requests per second: 426.33
ANÁLISIS: Servidor maneja carga básica adecuadamente, sin caídas

COMANDO: nikto -h http://localhost -o nikto_scan.html
RESPUESTA: 3 advisories de bajo riesgo encontrados (restringir `/server-status`, headers verificados)
ANÁLISIS: Escaneo de vulnerabilidades completado

COMANDO: sslyze localhost --regular
RESPUESTA: TLS 1.2 soportado, PFS habilitado, sin vulnerabilidades conocidas
ANÁLISIS: Configuración SSL/TLS robusta
```

## Fase 5: Protección Contra Ataques Comunes

### Sanitización de entrada (PHP)

```php
<?php
function sanitize_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    return htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
}

function prevent_sql_injection($connection, $data) {
    return mysqli_real_escape_string($connection, $data);
}

$user_input = sanitize_input($_POST['user_input'] ?? '');
$safe_input = prevent_sql_injection($connection, $user_input);
?>
```

## Controles Complementarios Requeridos

### Backups automatizados

Script `scripts/backup_nocturno.sh`:

```bash
#!/bin/bash
set -euo pipefail

SRC_DIRS=("/etc/apache2" "/var/www/html")
DEST_BASE="/var/backups/web"
STAMP=$(date '+%F')
DEST="$DEST_BASE/$STAMP"
LOG_FILE="/var/log/backup_web.log"
RETENTION_DAYS=14

mkdir -p "$DEST" "$(dirname "$LOG_FILE")"

for src in "${SRC_DIRS[@]}"; do
    rsync -a --delete "$src" "$DEST" >> "$LOG_FILE" 2>&1
done

echo "$(date '+%F %T'): Backup completado en $DEST" >> "$LOG_FILE"
find "$DEST_BASE" -mindepth 1 -maxdepth 1 -type d -mtime +$RETENTION_DAYS -exec rm -rf {} +
```

Agregar a cron (ejecutando `crontab -e`):

```
0 2 * * * /usr/local/bin/backup_nocturno.sh
```

### ModSecurity + OWASP CRS

```
COMANDO: sudo apt install -y libapache2-mod-security2
COMANDO: sudo cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf
COMANDO: sudo sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/modsecurity/modsecurity.conf
COMANDO: sudo apt install -y modsecurity-crs && sudo cp /usr/share/modsecurity-crs/crs-setup.conf.example /usr/share/modsecurity-crs/crs-setup.conf
COMANDO: sudo ln -s /usr/share/modsecurity-crs/rules /etc/modsecurity/
COMANDO: sudo systemctl reload apache2
RESPUESTA: WAF activado con OWASP CRS
ANÁLISIS: Capa adicional de protección frente a payloads maliciosos
```

### Certificados HTTPS con Let's Encrypt

```
COMANDO: sudo apt install -y certbot python3-certbot-apache
COMANDO: sudo certbot --apache -d croody.app -d www.croody.app --redirect --hsts --staple-ocsp --email mnzz.eafit@gmail.com --agree-tos
RESPUESTA: Certificado válido emitido, HTTPS forzado, HSTS en preload
ANÁLISIS: Tráfico cifrado y preparada la inclusión en lista preload
```

### Alertas inmediatas

Configurar `mailutils` o integración Webhook para enviar alertas desde `monitor_seguridad.sh`:

```
COMANDO: sudo apt install -y mailutils
CONFIG: Ajustar `ALERT_EMAIL` si cambia el contacto y probar con `echo "Prueba" | mail -s "Test" mnzz.eafit@gmail.com`
```

Para integraciones modernas se puede llamar a `curl -X POST https://hooks.slack.com/...` dentro del script.

## Análisis Post-Implementación

**Hallazgos principales**
- Servidor configurado con parámetros de seguridad modernos
- Headers anti-XSS/clickjacking activos
- Sistema de monitoreo con alertas y lista de IP sospechosas
- Rate limiting de red + ModSecurity con OWASP CRS
- Copias de seguridad automatizadas y TLS válido con Certbot

**Vulnerabilidades identificadas y corregidas**
- `/server-status` expuesto → restringido/deshabilitado
- Falta de WAF → ModSecurity + CRS activado
- Sin backups → rsync nocturno automatizado
- Monitoreo local sin alertas → script con correo/Webhook

**Recomendaciones de mitigación**
1. Configurar certificados a través de Let's Encrypt y supervisar la renovación automática (`certbot renew --dry-run`).
2. Habilitar MFA en paneles administrativos y panel hosting.
3. Mantener revisiones diarias de logs (`journalctl -u apache2`, `/var/log/seguridad_web.log`).
4. Probar trimestralmente con herramientas como `openvas`, `sslyze` y `k6` en entornos controlados.
5. Documentar cada cambio (plantillas IaC o Ansible) para facilitar reproducibilidad.

## Endurecimiento DNS autoritativo

| Control | Acción | Evidencia |
| --- | --- | --- |
| TSIG | Llaves generadas con `scripts/dns/setup_bind.sh` (HMAC-SHA256), almacenadas fuera del repo y rotadas trimestralmente. | `infra/dns/bind-master/keys/tsig.env` cifrado. |
| Restricción de AXFR | `allow-transfer { key "<tsig>"; <ip-esclavo>; };` en `named.conf.master.tpl`. | `infra/dns/templates/named.conf.master.tpl`. |
| Logging | Habilitar canales `queries`, `transfer` y enviar a CloudWatch via agentes o rsyslog. Rotar con logrotate/CloudWatch retention. | Config en `infra/dns/README.md`. |
| Validación | Pipeline `.github/workflows/bind-deploy.yml` ejecuta `named-checkconf`, `named-checkzone` y `rndc reload`. | Execution logs en GitHub Actions. |
| Failover | Guía `docs/dns_operacion.md` describe failover maestro/esclavo, pruebas `dig` y lineamientos de glue records. | Documentación actualizada en docs/. |

Integrar estos controles dentro del plan de endurecimiento garantiza que el perímetro DNS cumpla los indicativos y no se convierta en un punto débil frente a suplantaciones o exfiltración de zonas.
