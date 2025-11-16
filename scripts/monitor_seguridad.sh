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

    if echo "$line" | grep -Eiq "(union.*select|script\.php|\.\./|etc/passwd|base64_decode|select\s+.*from)"; then
        msg="INTENTO DE ATAQUE DETECTADO desde $ip -> $line"
        log_event "$msg"
        send_alert "Alerta intrusión" "$msg"
        add_blocklist "$ip"
    fi

done < <(tail -F "$APACHE_LOG")
