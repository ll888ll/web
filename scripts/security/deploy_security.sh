#!/usr/bin/env bash
# Valida protecciones en local y sincroniza scripts a servidores remotos
# Uso: ./deploy_security.sh user@server:/ruta/remota

set -euo pipefail
TARGET="${1:-}"
LOG_DIR="$(dirname "$0")/../../proyecto_integrado/Croody/security/logs"
VALIDATION_LOG="$LOG_DIR/validacion_previa.txt"
mkdir -p "$LOG_DIR"

validate_firewall(){
  echo "== Validando firewall y sysctl ==" | tee "$VALIDATION_LOG"
  sysctl net.ipv4.tcp_syncookies 2>/dev/null | tee -a "$VALIDATION_LOG"
  iptables -L INPUT -n -v | head -n 40 | tee -a "$VALIDATION_LOG"
}

validate_dns(){
  echo "== Validando DNSSEC ==" | tee -a "$VALIDATION_LOG"
  dig +dnssec croody.local @127.0.0.1 | grep -E "flags|ad" | tee -a "$VALIDATION_LOG" || true
}

sync_remote(){
  [[ -n "$TARGET" ]] || { echo "Skipping sync (sin destino)"; return; }
  echo "== Sincronizando scripts de seguridad a $TARGET ==" | tee -a "$VALIDATION_LOG"
  rsync -avz scripts/security "$TARGET"
}

integrity_check(){
  echo "== Verificando checksums ==" | tee -a "$VALIDATION_LOG"
  (cd scripts/security && sha256sum *.sh *.py) | tee "$LOG_DIR/checksums.txt"
}

validate_firewall
validate_dns
integrity_check
sync_remote

printf '\nValidación finalizada. Revisar %s para detalles.\n' "$VALIDATION_LOG"
