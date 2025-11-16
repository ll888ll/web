#!/usr/bin/env bash
# Configura cortafuegos y protecciones básicas para la landing Croody
# Uso previsto: ejecutar como root en Kali/Ubuntu.
# Registra cada acción en security/logs/implementacion_seguridad.txt

set -euo pipefail
LOG_FILE="$(dirname "$0")/../../proyecto_integrado/Croody/security/logs/implementacion_seguridad.txt"
mkdir -p "$(dirname "$LOG_FILE")"

log(){
  local msg="$1"
  printf '[%s] %s\n' "$(date -Iseconds)" "$msg" | tee -a "$LOG_FILE"
}

require_root(){
  if [[ $(id -u) -ne 0 ]]; then
    log "ERROR: este script requiere privilegios de root."
    exit 1
  fi
}

configure_sysctl(){
  log "Habilitando SYN cookies y endureciendo redes"
  sysctl -w net.ipv4.tcp_syncookies=1 >/dev/null
  sysctl -w net.ipv4.tcp_max_syn_backlog=4096 >/dev/null
  sysctl -w net.ipv4.conf.all.rp_filter=1 >/dev/null
  sysctl -w net.ipv4.conf.default.rp_filter=1 >/dev/null
}

clean_tables(){
  log "Limpiando reglas previas"
  iptables -F
  iptables -X
  iptables -t nat -F
  iptables -t nat -X
  iptables -t mangle -F
  iptables -t mangle -X
}

base_policy(){
  log "Estableciendo políticas por defecto"
  iptables -P INPUT DROP
  iptables -P FORWARD DROP
  iptables -P OUTPUT ACCEPT
  iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
  iptables -A INPUT -i lo -j ACCEPT
}

allow_services(){
  log "Permitiendo HTTP/HTTPS y SSH administrado"
  iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m limit --limit 4/min --limit-burst 4 -j ACCEPT
  iptables -A INPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate NEW -j ACCEPT
  iptables -A INPUT -p udp --dport 443 -m conntrack --ctstate NEW -j ACCEPT
}

rate_limiting(){
  log "Aplicando limitaciones de tasa"
  iptables -A INPUT -p tcp --syn -m limit --limit 40/second --limit-burst 80 -j ACCEPT
  iptables -A INPUT -p tcp --syn -j LOG --log-prefix "SYN-FLOOD "
  iptables -A INPUT -p tcp --syn -j DROP
  iptables -A INPUT -p udp -m hashlimit --hashlimit-above 25/sec --hashlimit-burst 50 --hashlimit-mode srcip --hashlimit-name udp-dos -j LOG --log-prefix "UDP-DOS "
  iptables -A INPUT -p udp -m hashlimit --hashlimit-above 25/sec --hashlimit-burst 50 --hashlimit-mode srcip --hashlimit-name udp-dos -j DROP
}

bad_actors(){
  log "Bloqueando puertos sensibles y paquetes inválidos"
  iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
  iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
  iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
  iptables -A INPUT -p tcp --tcp-flags SYN,RST SYN,RST -j DROP
}

log_summary(){
  log "Firewall configurado. Reglas activas:"
  iptables -L -n -v | tee -a "$LOG_FILE"
}

main(){
  require_root
  configure_sysctl
  clean_tables
  base_policy
  allow_services
  rate_limiting
  bad_actors
  log_summary
}

main "$@"
