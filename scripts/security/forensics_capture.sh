#!/usr/bin/env bash
# Captura tráfico sospechoso y genera evidencias (pcap + reporte TXT)
# Uso: ./forensics_capture.sh --iface eth0 --dur 60 --tag syn-flood

set -euo pipefail
LOG_DIR="$(dirname "$0")/../../proyecto_integrado/Croody/security/logs"
mkdir -p "$LOG_DIR"
REPORT="$LOG_DIR/evidencia_forense.txt"

iface="eth0"
duration=60
tag="evento"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --iface) iface="$2"; shift;;
    --dur) duration="$2"; shift;;
    --tag) tag="$2"; shift;;
  esac
  shift
done

TS=$(date -Iseconds)
PCAP="$LOG_DIR/captura_${tag}_${TS}.pcap"
log(){ printf '[%s] %s\n' "$TS" "$1" | tee -a "$REPORT"; }

log "Iniciando captura PCAP ($duration s) en $iface etiquetada como $tag"
tcpdump -i "$iface" -G "$duration" -W 1 -w "$PCAP" 'tcp[tcpflags] & (tcp-syn) != 0 or udp' >/dev/null 2>&1 || log "tcpdump no disponible"
log "Captura finalizada en $PCAP"

if command -v tshark >/dev/null 2>&1; then
  SUMMARY=$(tshark -r "$PCAP" -q -z io,stat,5)
  log "Resumen estadístico:\n$SUMMARY"
else
  log "tshark no presente; salta resumen"
fi

log "Evidencia forense generada (PCAP + resumen)."
