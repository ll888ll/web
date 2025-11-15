#!/usr/bin/env bash
set -euo pipefail

CONF=${CONF:-/etc/cicf/env}
TS=$(date +%Y%m%d-%H%M%S)
OUT_DIR=/var/log/cicf
OUT_FILE="$OUT_DIR/report-$TS.md"

mkdir -p "$OUT_DIR"

host=$(hostname)
os=$(grep ^PRETTY_NAME= /etc/os-release 2>/dev/null | cut -d= -f2- | tr -d '"')

PCAP_DIR=/var/log/cicf/pcap
FLOWS_DIR=/var/log/cicf/flows
ALERT_DIR=/var/log/cicf/alerts

sec() { echo -e "\n## $1\n" >> "$OUT_FILE"; }
kv() { printf -- "- %s: %s\n" "$1" "$2" >> "$OUT_FILE"; }

{
  echo "# CICF Sensor Report"
  echo
  echo "Generado: $(date -Is)"
  echo "Host: $host"
  echo "SO: ${os:-desconocido}"
} > "$OUT_FILE"

sec "Versiones"
kv "java" "$(java -version 2>&1 | head -n1 || echo N/A)"
kv "tshark" "$(tshark -v 2>&1 | head -n1 || echo N/A)"
kv "python3" "$(python3 -V 2>&1 | head -n1 || echo N/A)"
kv "tcpdump" "$(tcpdump --version 2>&1 | head -n1 || echo N/A)"

sec "Configuración (/etc/cicf/env)"
if [[ -f "$CONF" ]]; then
  echo '```' >> "$OUT_FILE"
  sed 's/^/  /' "$CONF" >> "$OUT_FILE"
  echo '```' >> "$OUT_FILE"
else
  echo "(no existe $CONF)" >> "$OUT_FILE"
fi

sec "Estado de servicios"
for s in cicf-bridge.service cicf-capture.service cicf-watch.service cicf-dnsmon.service dns-guard.service cicf-clean.timer; do
  st=$(systemctl is-enabled "$s" 2>/dev/null || echo disabled)
  ac=$(systemctl is-active "$s" 2>/dev/null || echo inactive)
  kv "$s" "$st / $ac"
done

sec "Interfaces y bridge"
echo '```' >> "$OUT_FILE"
ip -br link >> "$OUT_FILE" 2>/dev/null || true
echo >> "$OUT_FILE"
bridge link >> "$OUT_FILE" 2>/dev/null || true
echo '```' >> "$OUT_FILE"

sec "Captura (PCAP)"
kv "Directorio" "$PCAP_DIR"
kv "Tamaño" "$(du -sh "$PCAP_DIR" 2>/dev/null | awk '{print $1}')"
kv "Ficheros" "$(ls -1 "$PCAP_DIR"/*.pcap 2>/dev/null | wc -l)"
echo '```' >> "$OUT_FILE"
ls -ltr "$PCAP_DIR" 2>/dev/null | tail -n 20 >> "$OUT_FILE"
echo '```' >> "$OUT_FILE"

sec "Flows (CSV)"
kv "Directorio" "$FLOWS_DIR"
kv "Tamaño" "$(du -sh "$FLOWS_DIR" 2>/dev/null | awk '{print $1}')"
kv "Ficheros" "$(ls -1 "$FLOWS_DIR"/*_Flow.csv 2>/dev/null | wc -l)"
latest_csv=$(ls -1t "$FLOWS_DIR"/*_Flow.csv 2>/dev/null | head -n1 || true)
if [[ -n "${latest_csv:-}" ]]; then
  kv "Último CSV" "$latest_csv"
  kv "Líneas" "$(wc -l < "$latest_csv" 2>/dev/null || echo 0)"
fi

sec "DNS Guard (nftables bridge/cicf)"
echo '```' >> "$OUT_FILE"
nft list table bridge cicf 2>/dev/null >> "$OUT_FILE" || echo "(sin tabla bridge/cicf)" >> "$OUT_FILE"
echo '```' >> "$OUT_FILE"

sec "Alertas DNS"
kv "Directorio" "$ALERT_DIR"
echo '```' >> "$OUT_FILE"
tail -n 50 "$ALERT_DIR"/dnsmon.log 2>/dev/null || echo "(sin alertas)" >> "$OUT_FILE"
echo '```' >> "$OUT_FILE"
for k in UNAUTH_SRC TXID_MISS LOW_TTL PRIVATE_IP MULTI_ANS; do
  c=$(grep -c "$k" "$ALERT_DIR"/dnsmon.log 2>/dev/null || echo 0)
  kv "$k" "$c"
done

sec "Logs de servicios (últimas 50 líneas)"
for u in cicf-bridge cicf-capture cicf-watch cicf-dnsmon; do
  echo "### $u" >> "$OUT_FILE"
  echo '```' >> "$OUT_FILE"
  journalctl -u "$u" -n 50 2>/dev/null >> "$OUT_FILE" || echo "(sin logs)" >> "$OUT_FILE"
  echo '```' >> "$OUT_FILE"
done

echo "$OUT_FILE"

