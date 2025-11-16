#!/usr/bin/env bash
# Configuración orientativa de DNSSEC + caché local usando Unbound
# Ejecutar como root en Kali/Ubuntu.
# Registra acciones en security/logs/implementacion_seguridad.txt

set -euo pipefail
LOG_FILE="$(dirname "$0")/../../proyecto_integrado/Croody/security/logs/implementacion_seguridad.txt"
mkdir -p "$(dirname "$LOG_FILE")"
log(){ printf '[%s] %s\n' "$(date -Iseconds)" "$1" | tee -a "$LOG_FILE"; }
[[ $(id -u) -eq 0 ]] || { log "ERROR: se requieren privilegios de root"; exit 1; }

log "Instalando dependencias DNSSEC (unbound, dnsutils)"
if command -v apt-get >/dev/null 2>&1; then
  apt-get update && apt-get install -y unbound dnsutils
fi

CONF=/etc/unbound/unbound.conf.d/croody.conf
log "Creando configuración segura en $CONF"
cat <<'CFG' > "$CONF"
server:
  interface: 0.0.0.0
  interface: ::0
  access-control: 127.0.0.0/8 allow
  access-control: 10.0.0.0/8 allow
  access-control: 192.168.0.0/16 allow
  access-control: 0.0.0.0/0 refuse
  verbosity: 1
  logfile: "/var/log/unbound-sec.log"
  log-servfail: yes
  hide-identity: yes
  hide-version: yes
  cache-min-ttl: 60
  cache-max-ttl: 86400
  prefetch: yes
  harden-dnssec-stripped: yes
  harden-below-nxdomain: yes
  do-ip4: yes
  do-ip6: no
  do-daemonize: yes
  val-clean-additional: yes
  qname-minimisation: yes
  serve-expired: yes
  tls-cert-bundle: "/etc/ssl/certs/ca-certificates.crt"
remote-control:
  control-enable: yes

# Registro de intentos de spoofing: cualquier validación DNSSEC fallida
python:
  def inform_super(module, qstate, qdata):
    if qstate.return_msg and qstate.return_msg.rep and qstate.return_msg.rep.security == 2:
      import datetime
      logline = f"[{datetime.datetime.utcnow().isoformat()}] | DNS spoof detectado | qname={qstate.qinfo.qname_str}"
      open("/var/log/dns-spoof.log", "a").write(logline + "\n")
      module.env.log_info(logline)
      return True
    return True
python-module: "inform_super"
CFG

log "Reiniciando servicio unbound"
systemctl enable unbound
systemctl restart unbound
log "Protección DNSSEC configurada. Registrar eventos en /var/log/dns-spoof.log"
