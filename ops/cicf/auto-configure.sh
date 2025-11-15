#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "[auto-configure] Ejecuta como root: sudo ops/cicf/auto-configure.sh [IFACE_LEFT IFACE_RIGHT]" >&2
  exit 1
fi

BASE_DIR=$(cd "$(dirname "$0")" && pwd)

# 1) Instalar
bash "$BASE_DIR/install.sh"

CONF=/etc/cicf/env
mkdir -p /var/log/cicf/alerts

choose_ifaces() {
  # Permite args explícitos
  if [[ $# -ge 2 ]]; then
    echo "$1" "$2"
    return 0
  fi
  # Heurística: dos primeras interfaces físicas (no lo, docker, veth, br-)
  mapfile -t CANDS < <(ip -br link | awk '{print $1" "$2}' \
    | grep -E -v '^(lo|docker0|br-|veth|virbr|tap|wg|tailscale)' \
    | awk '{print $1}')
  if [[ ${#CANDS[@]} -lt 2 ]]; then
    echo "" ""; return 1
  fi
  echo "${CANDS[0]}" "${CANDS[1]}"
}

IFL=${1:-}
IFR=${2:-}
read -r DETL DETR < <(choose_ifaces ${IFL:+"$IFL"} ${IFR:+"$IFR"} || true)
IFACE_LEFT=${IFL:-$DETL}
IFACE_RIGHT=${IFR:-$DETR}

SINGLE_NIC=0
if [[ -z "$IFACE_LEFT" || -z "$IFACE_RIGHT" || "$IFACE_LEFT" == "$IFACE_RIGHT" ]]; then
  # Modo 1 NIC: capturar sobre la interfaz activa (eth0 por defecto)
  IFACE_CAP=${IFACE_LEFT:-eth0}
  SINGLE_NIC=1
  echo "[auto-configure] Solo una NIC detectada. Usando modo espejo/captura en IFACE=$IFACE_CAP (sin bridge)."
else
  echo "[auto-configure] Usando IFACE_LEFT=$IFACE_LEFT IFACE_RIGHT=$IFACE_RIGHT"
fi

# Toma DNS de resolv.conf
ALLOWED=$(awk '/^nameserver/{print $2}' /etc/resolv.conf | paste -sd, -)
ALLOWED=${ALLOWED:-"8.8.8.8,1.1.1.1"}

# Asegura claves en /etc/cicf/env
if [[ $SINGLE_NIC -eq 0 ]]; then
  grep -q '^IFACE_LEFT=' "$CONF" && sed -i "s/^IFACE_LEFT=.*/IFACE_LEFT=$IFACE_LEFT/" "$CONF" || echo "IFACE_LEFT=$IFACE_LEFT" >> "$CONF"
  grep -q '^IFACE_RIGHT=' "$CONF" && sed -i "s/^IFACE_RIGHT=.*/IFACE_RIGHT=$IFACE_RIGHT/" "$CONF" || echo "IFACE_RIGHT=$IFACE_RIGHT" >> "$CONF"
  # elimina CAP_INTERFACE si estuviera
  sed -i '/^CAP_INTERFACE=/d' "$CONF" || true
else
  # modo 1 NIC
  grep -q '^CAP_INTERFACE=' "$CONF" && sed -i "s|^CAP_INTERFACE=.*|CAP_INTERFACE=$IFACE_CAP|" "$CONF" || echo "CAP_INTERFACE=$IFACE_CAP" >> "$CONF"
fi
grep -q '^ALLOWED_DNS=' "$CONF" && sed -i "s/^ALLOWED_DNS=.*/ALLOWED_DNS=$ALLOWED/" "$CONF" || echo "ALLOWED_DNS=$ALLOWED" >> "$CONF"
grep -q '^DNS_GUARD_MODE=' "$CONF" || echo "DNS_GUARD_MODE=allowlist" >> "$CONF"

systemctl daemon-reload || true

echo "[auto-configure] Arrancando servicios..."
if [[ $SINGLE_NIC -eq 0 ]]; then
  systemctl enable --now cicf-bridge.service || true
  systemctl enable --now dns-guard.service || true
else
  echo "[auto-configure] Omitiendo bridge/dns-guard (requieren bridge)."
fi
systemctl enable --now cicf-capture.service cicf-watch.service cicf-dnsmon.service || true
systemctl enable --now cicf-clean.timer || true

echo "[auto-configure] Verificando estado..."
/usr/local/bin/cicf-verify.sh || true

echo "[auto-configure] Hecho. Revisa /var/log/cicf/* y alertas DNS."
