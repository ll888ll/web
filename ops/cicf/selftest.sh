#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "[selftest] Ejecuta como root: sudo ops/cicf/selftest.sh" >&2
  exit 1
fi

BASE_DIR=$(cd "$(dirname "$0")" && pwd)
CONF=/etc/cicf/env

echo "[selftest] Instalando y preparando entorno..."
bash "$BASE_DIR/install.sh"

# Asegura parámetros mínimos para test
mkdir -p /var/log/cicf/pcap /var/log/cicf/flows /var/log/cicf/alerts
if ! grep -q '^ALLOWED_DNS=' "$CONF" 2>/dev/null; then
  echo 'ALLOWED_DNS=8.8.8.8,1.1.1.1' >> "$CONF"
fi
if ! grep -q '^DNS_GUARD_MODE=' "$CONF" 2>/dev/null; then
  echo 'DNS_GUARD_MODE=allowlist' >> "$CONF"
fi

echo "[selftest] Aplicando defensa DNS (nftables)..."
/usr/local/bin/dns-guard.sh || true

echo "[selftest] Generando PCAP de prueba DNS spoof..."
CONF=$CONF /usr/local/bin/test-dns-spoof.sh

PCAP=/var/log/cicf/pcap/dns-spoof-test.pcap
if [[ ! -f "$PCAP" ]]; then
  echo "[selftest] No se generó $PCAP" >&2
  exit 2
fi

echo "[selftest] Convirtiendo PCAP a flows (CICFlowMeter)..."
# shellcheck disable=SC1091
. "$CONF"
JAR=${CICF_JAR:-/opt/cicflowmeter/CICFlowMeter.jar}
JNI=${CICF_JNI_DIR:-/opt/cicflowmeter/jnetpcap/linux/jnetpcap-1.4.r1425}
JNETJAR=${CICF_JNETPCAP_JAR:-/opt/cicflowmeter/jnetpcap/linux/jnetpcap-1.4.r1425/jnetpcap.jar}
OUT=${FLOWS_DIR:-/var/log/cicf/flows}

java -Djava.library.path="$JNI" -cp "$JAR:$JNETJAR" cic.cs.unb.ca.ifm.Cmd "$PCAP" "$OUT"

CSV="$OUT/$(basename "$PCAP")_Flow.csv"
if [[ ! -f "$CSV" ]]; then
  echo "[selftest] No se generó CSV esperado: $CSV" >&2
  exit 3
fi
head -n1 "$CSV" | grep -qi 'src_ip' || true

echo "[selftest] Ejecutando DNS monitor en una pasada..."
/usr/bin/env python3 /usr/local/bin/cicf-dnsmon.py "$PCAP" || true

ALERTS=/var/log/cicf/alerts/dnsmon.log
if [[ -f "$ALERTS" ]]; then
  echo "[selftest] Últimas alertas:"
  tail -n5 "$ALERTS" || true
  # Busca al menos dos tipos de alerta en el PCAP sintético
  grep -q 'UNAUTH_SRC' "$ALERTS" && grep -q 'LOW_TTL' "$ALERTS" && OK=1 || OK=0
else
  OK=0
fi

if [[ $OK -eq 1 ]]; then
  echo "[selftest] OK: flujo CSV generado y alertas DNS detectadas."
  exit 0
else
  echo "[selftest] WARNING: No se detectaron todas las alertas esperadas. Revisa $ALERTS" >&2
  exit 4
fi

