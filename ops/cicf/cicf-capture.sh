#!/usr/bin/env bash
set -euo pipefail

CONF=${CONF:-/etc/cicf/env}
if [[ ! -f "$CONF" ]]; then
  echo "[cicf-capture] Falta fichero de configuración: $CONF" >&2
  exit 1
fi
# shellcheck disable=SC1090
. "$CONF"

BR=${BRIDGE_NAME:-br0}
CAP_IF=${CAP_INTERFACE:-}
PCAP_DIR=${PCAP_DIR:-/var/log/cicf/pcap}
FLOWS_DIR=${FLOWS_DIR:-/var/log/cicf/flows}
ROTATE_S=${CAP_ROTATE_SECONDS:-60}
ROTATE_MB=${CAP_ROTATE_SIZE_MB:-0}
SNAPLEN=${CAP_SNAPLEN:-0}
BPF=${CAP_BPF:-}

mkdir -p "$PCAP_DIR" "$FLOWS_DIR"

IFACE_TO_USE=${CAP_IF:-$BR}
if (( ROTATE_MB > 0 )); then
  exec tcpdump -i "$IFACE_TO_USE" -s "$SNAPLEN" -U -C "$ROTATE_MB" -w "$PCAP_DIR/cap-%Y%m%d-%H%M%S.pcap" ${BPF:+$BPF}
else
  exec tcpdump -i "$IFACE_TO_USE" -s "$SNAPLEN" -U -G "$ROTATE_S" -w "$PCAP_DIR/cap-%Y%m%d-%H%M%S.pcap" ${BPF:+$BPF}
fi
