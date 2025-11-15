#!/usr/bin/env bash
set -euo pipefail

CONF=${CONF:-/etc/cicf/env}
if [[ ! -f "$CONF" ]]; then
  echo "[cicf-verify] Falta fichero de configuración: $CONF" >&2
  exit 1
fi
# shellcheck disable=SC1090
. "$CONF"

BR=${BRIDGE_NAME:-br0}
PCAP_DIR=${PCAP_DIR:-/var/log/cicf/pcap}
FLOWS_DIR=${FLOWS_DIR:-/var/log/cicf/flows}

echo "[verify] Bridge y miembros:"
ip -br link show "$BR" || true
bridge link 2>/dev/null || true

echo "[verify] Archivos de captura:"
ls -ltr "$PCAP_DIR" 2>/dev/null || echo "(aún no hay PCAPs)"

echo "[verify] Flows CSV:"
ls -ltr "$FLOWS_DIR" 2>/dev/null || echo "(aún no hay CSVs)"

echo "[verify] Servicios (si systemd):"
systemctl is-active cicf-bridge.service 2>/dev/null || true
systemctl is-active cicf-capture.service 2>/dev/null || true
systemctl is-active cicf-watch.service 2>/dev/null || true
systemctl is-active cicf-dnsmon.service 2>/dev/null || true

echo "[verify] Reglas nftables (bridge/cicf):"
nft list table bridge cicf 2>/dev/null || echo "(sin tabla bridge/cicf, ejecuta dns-guard.sh si deseas defensa activa)"
