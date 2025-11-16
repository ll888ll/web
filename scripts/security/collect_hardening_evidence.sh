#!/usr/bin/env bash
# Recolecta la evidencia solicitada tras ejecutar el hardening automático.
# Debe ejecutarse con privilegios de root en el mismo host donde corre el workflow.

set -euo pipefail

DEFAULT_OUTPUT="$PWD/hardening_evidence-$(date -Iseconds).log"
OUTPUT_FILE="${1:-$DEFAULT_OUTPUT}"

require_root() {
  if [[ "$(id -u)" -ne 0 ]]; then
    echo "Este recolector requiere privilegios de root (sudo collect_hardening_evidence.sh ...)." >&2
    exit 1
  fi
}

section() {
  local title="$1"
  shift
  local cmd_display
  printf -v cmd_display '%q ' "$@"
  {
    printf '\n========== %s ==========\n' "$title"
    printf '[%s] $ %s\n' "$(date -Iseconds)" "$cmd_display"
  } | tee -a "$OUTPUT_FILE"
  "$@" 2>&1 | tee -a "$OUTPUT_FILE"
}

section_shell() {
  local title="$1"
  local inline_cmd="$2"
  section "$title" bash -lc "$inline_cmd"
}

main() {
  require_root
  : >"$OUTPUT_FILE"
  echo "Guardando evidencia en $OUTPUT_FILE"

  section "Logs íntegros de /var/log/croody_hardening.log" cat /var/log/croody_hardening.log
  section "Últimas 50 líneas de /var/log/croody_hardening.log" tail -n 50 /var/log/croody_hardening.log
  section "systemctl status monitor-seguridad.service" systemctl status monitor-seguridad.service
  section "Crontab de root" crontab -l
  section "certbot certificates" certbot certificates
  section "sudo ufw status" ufw status verbose
  section_shell "sudo iptables -L INPUT -n -v | head -n 40" "iptables -L INPUT -n -v | head -n 40"
  section_shell "apachectl -M | grep security2" "apachectl -M | grep -i security2 || true"
  section "Listado de /etc/modsecurity" ls -al /etc/modsecurity
  section "systemctl status apache2" systemctl status apache2
  section "tail -n 50 /var/log/seguridad_web.log" tail -n 50 /var/log/seguridad_web.log

  echo "Evidencia recopilada. Adjunta $OUTPUT_FILE en el informe."
}

main "$@"
