#!/usr/bin/env bash
set -euo pipefail

CONF=${CONF:-/etc/cicf/env}
if [[ ! -f "$CONF" ]]; then
  echo "[dns-guard] Falta fichero de configuración: $CONF" >&2
  exit 1
fi
# shellcheck disable=SC1090
. "$CONF"

MODE=${DNS_GUARD_MODE:-off}
ALLOWED=${ALLOWED_DNS:-}

if [[ "$MODE" == "off" ]]; then
  echo "[dns-guard] Modo off, no se aplican reglas."
  exit 0
fi

if ! command -v nft >/dev/null 2>&1; then
  echo "[dns-guard] nftables no disponible. Instálalo para usar guardado de DNS." >&2
  exit 1
fi

modprobe br_netfilter 2>/dev/null || true
sysctl -w net.bridge.bridge-nf-call-iptables=1 >/dev/null 2>&1 || true
sysctl -w net.bridge.bridge-nf-call-ip6tables=1 >/dev/null 2>&1 || true
sysctl -w net.bridge.bridge-nf-call-arptables=1 >/dev/null 2>&1 || true

map_ips="{ }"
if [[ -n "$ALLOWED" ]]; then
  # Construye set literal {ip1, ip2, ...}
  s="{"
  IFS=',' read -ra arr <<< "$ALLOWED"
  for ip in "${arr[@]}"; do
    ip_trim=$(echo "$ip" | xargs)
    [[ -z "$ip_trim" ]] && continue
    if [[ "$s" != "{" ]]; then s+=", "; fi
    s+="$ip_trim"
  done
  s+="}"
  map_ips="$s"
fi

echo "[dns-guard] Activando modo $MODE; DNS permitidos: $ALLOWED"

# (Re)crea tabla/chain en familia bridge para tráfico en el bridge L2
nft list table bridge cicf >/dev/null 2>&1 && nft delete table bridge cicf || true
nft -f - <<EOF
table bridge cicf {
  set allowed_dns {
    type ipv4_addr;
    elements $map_ips
  }
  chain forward {
    type filter hook forward priority 0; policy accept;
    # Permite consultas hacia DNS permitidos
    udp dport 53 ip daddr @allowed_dns accept
    tcp dport 53 ip daddr @allowed_dns accept
    # Permite respuestas desde DNS permitidos
    udp sport 53 ip saddr @allowed_dns accept
    tcp sport 53 ip saddr @allowed_dns accept
    # Si modo allowlist, bloquea el resto de DNS (53)
    $( [[ "$MODE" == "allowlist" ]] && echo "udp dport 53 drop" )
    $( [[ "$MODE" == "allowlist" ]] && echo "tcp dport 53 drop" )
    $( [[ "$MODE" == "allowlist" ]] && echo "udp sport 53 drop" )
    $( [[ "$MODE" == "allowlist" ]] && echo "tcp sport 53 drop" )
  }
}
EOF

echo "[dns-guard] Reglas aplicadas en tabla bridge/cicf"
