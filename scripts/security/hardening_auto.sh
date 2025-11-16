#!/usr/bin/env bash
# Automatiza el endurecimiento básico documentado para el sitio Croody.
# Debe ejecutarse con privilegios de root sobre un host Debian/Ubuntu/Kali.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_FILE="/var/log/croody_hardening.log"
DOMAIN="croody.app"
ALT_DOMAIN="www.croody.app"
ADMIN_EMAIL="mnzz.eafit@gmail.com"
APACHE_SECURITY_CONF="/etc/apache2/conf-available/security.conf"
MONITOR_SERVICE="/etc/systemd/system/monitor-seguridad.service"
BACKUP_CRON_ENTRY="0 2 * * * /usr/local/bin/backup_nocturno.sh"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
  printf '[%s] %s\n' "$(date -Iseconds)" "$1" | tee -a "$LOG_FILE"
}

require_root() {
  if [[ "$(id -u)" -ne 0 ]]; then
    echo "Este script requiere privilegios de root." >&2
    exit 1
  fi
}

apt_update() {
  export DEBIAN_FRONTEND=noninteractive
  log "Actualizando índices y paquetes del sistema"
  apt-get update -yq
  apt-get upgrade -yq
}

ensure_package() {
  local pkg="$1"
  if dpkg -s "$pkg" >/dev/null 2>&1; then
    log "Paquete $pkg ya instalado"
  else
    log "Instalando paquete $pkg"
    if ! apt-get install -yq "$pkg"; then
      log "ERROR: no se pudo instalar $pkg"
      exit 1
    fi
  fi
}

install_dependencies() {
  local packages=(
    apache2
    ufw
    mailutils
    certbot
    python3-certbot-apache
    libapache2-mod-security2
    modsecurity-crs
  )
  for pkg in "${packages[@]}"; do
    ensure_package "$pkg"
  done
}

enable_apache() {
  log "Habilitando y arrancando Apache"
  systemctl enable --now apache2
  a2enmod headers >/dev/null
  a2enmod ssl >/dev/null
  a2enmod rewrite >/dev/null
  a2enmod security2 >/dev/null
}

write_security_conf() {
  log "Aplicando configuración reforzada en $APACHE_SECURITY_CONF"
  cat >"$APACHE_SECURITY_CONF" <<'EOF'
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
EOF
  a2enconf security >/dev/null
}

lock_server_status() {
  log "Deshabilitando /server-status"
  a2dismod status >/dev/null 2>&1 || true
  rm -f /etc/apache2/conf-enabled/status.conf /etc/apache2/conf-available/status.conf || true
}

reload_apache() {
  log "Recargando Apache"
  systemctl reload apache2
}

configure_ufw() {
  if ! command -v ufw >/dev/null 2>&1; then
    log "UFW no instalado, saltando configuración de firewall"
    return
  fi
  log "Aplicando políticas UFW"
  ufw --force enable
  ufw allow 80/tcp
  ufw allow 443/tcp
  ufw deny 22/tcp
}

ensure_iptables_rule() {
  local chain=$1
  shift
  if iptables -C "$chain" "$@" >/dev/null 2>&1; then
    return
  fi
  iptables -A "$chain" "$@"
}

configure_rate_limiting() {
  if ! command -v iptables >/dev/null 2>&1; then
    log "iptables no disponible; saltando reglas de limitación"
    return
  fi
  log "Configurando limitación básica de tráfico HTTP"
  ensure_iptables_rule INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
  ensure_iptables_rule INPUT -p tcp --dport 80 -j DROP
}

deploy_monitor_script() {
  local source="$ROOT_DIR/scripts/monitor_seguridad.sh"
  if [[ ! -f "$source" ]]; then
    log "Script de monitoreo no encontrado en $source"
    return
  fi
  log "Instalando script de monitoreo en /usr/local/bin"
  install -m 750 "$source" /usr/local/bin/monitor_seguridad.sh

  log "Creando servicio systemd para monitor_seguridad"
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

deploy_backup_script() {
  local source="$ROOT_DIR/scripts/backup_nocturno.sh"
  if [[ ! -f "$source" ]]; then
    log "Script de backup no encontrado en $source"
    return
  fi
  log "Instalando script de backup en /usr/local/bin"
  install -m 750 "$source" /usr/local/bin/backup_nocturno.sh

  log "Registrando cron nocturno de backup"
  local existing
  existing="$(crontab -l 2>/dev/null || true)"
  echo "$existing" | grep -F "$BACKUP_CRON_ENTRY" >/dev/null 2>&1 || {
    (echo "$existing"; echo "$BACKUP_CRON_ENTRY") | crontab -
  }
}

configure_modsecurity() {
  if [[ ! -d /etc/modsecurity ]]; then
    log "ModSecurity no está instalado correctamente; omitiendo configuración"
    return
  fi
  log "Habilitando ModSecurity y OWASP CRS"
  cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf
  sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/modsecurity/modsecurity.conf
  if [[ -d /usr/share/modsecurity-crs ]]; then
    cp /usr/share/modsecurity-crs/crs-setup.conf.example /usr/share/modsecurity-crs/crs-setup.conf
    ln -sf /usr/share/modsecurity-crs/rules /etc/modsecurity/
  else
    log "OWASP CRS no disponible en /usr/share/modsecurity-crs"
  fi
}

obtain_cert() {
  if ! command -v certbot >/dev/null 2>&1; then
    log "Certbot no instalado; no se pueden gestionar certificados"
    return
  fi
  log "Solicitando/renovando certificado Let's Encrypt para $DOMAIN"
  if ! certbot certificates 2>/dev/null | grep -q "$DOMAIN"; then
    if ! certbot --apache --non-interactive --agree-tos --no-eff-email \
      --email "$ADMIN_EMAIL" --redirect --hsts --staple-ocsp \
      -d "$DOMAIN" -d "$ALT_DOMAIN"; then
      log "WARN: Certbot no pudo emitir certificado inicial (¿DNS/puerto 80 disponibles?)"
    fi
  else
    certbot renew --quiet
  fi
}

main() {
  require_root
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

main "$@"
