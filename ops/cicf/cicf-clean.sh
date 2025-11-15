#!/usr/bin/env bash
set -euo pipefail
CONF=${CONF:-/etc/cicf/env}
if [[ -f "$CONF" ]]; then . "$CONF"; fi
PCAP_DIR=${PCAP_DIR:-/var/log/cicf/pcap}
FLOWS_DIR=${FLOWS_DIR:-/var/log/cicf/flows}
PCAP_RET_DAYS=${PCAP_RET_DAYS:-7}
FLOWS_RET_DAYS=${FLOWS_RET_DAYS:-30}
find "$PCAP_DIR" -type f -name '*.pcap' -mtime +"$PCAP_RET_DAYS" -delete 2>/dev/null || true
find "$FLOWS_DIR" -type f -name '*_Flow.csv' -mtime +"$FLOWS_RET_DAYS" -delete 2>/dev/null || true

