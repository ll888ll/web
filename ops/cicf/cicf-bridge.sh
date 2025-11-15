#!/usr/bin/env bash
set -euo pipefail

CONF=${CONF:-/etc/cicf/env}
if [[ ! -f "$CONF" ]]; then
  echo "[cicf-bridge] Falta fichero de configuración: $CONF" >&2
  exit 1
fi
# shellcheck disable=SC1090
. "$CONF"

: "${IFACE_LEFT:?Define IFACE_LEFT en $CONF}"
: "${IFACE_RIGHT:?Define IFACE_RIGHT en $CONF}"
BR=${BRIDGE_NAME:-br0}
STP=${BRIDGE_STP:-off}

ip link show "$IFACE_LEFT" >/dev/null
ip link show "$IFACE_RIGHT" >/dev/null

if ! ip link show "$BR" >/dev/null 2>&1; then
  ip link add "$BR" type bridge
fi

# STP (1 on, 0 off)
if [[ "$STP" == "on" ]]; then
  ip link set dev "$BR" type bridge stp_state 1 || true
else
  ip link set dev "$BR" type bridge stp_state 0 || true
fi

# Quita IPs de miembros (nos quedamos en L2)
ip addr flush dev "$IFACE_LEFT" || true
ip addr flush dev "$IFACE_RIGHT" || true

# Añade al bridge
ip link set "$IFACE_LEFT" master "$BR" || true
ip link set "$IFACE_RIGHT" master "$BR" || true

# Desactiva offloads para captura fiel
ethtool -K "$IFACE_LEFT" gro off gso off tso off lro off 2>/dev/null || true
ethtool -K "$IFACE_RIGHT" gro off gso off tso off lro off 2>/dev/null || true

# Sube interfaces
ip link set "$IFACE_LEFT" up
ip link set "$IFACE_RIGHT" up
ip link set "$BR" up

# IP de gestión opcional en el bridge
if [[ -n "${BRIDGE_ADMIN_IP:-}" ]]; then
  ip addr add "$BRIDGE_ADMIN_IP" dev "$BR" || true
fi

echo "[cicf-bridge] Bridge $BR listo: $IFACE_LEFT <-> $IFACE_RIGHT"

