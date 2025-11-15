#!/usr/bin/env bash
# Instalación y despliegue desde cero (Ubuntu/Debian) para desarrolladores
# - Instala dependencias base, Docker + Compose
# - Prepara proyecto integrado
# - Levanta servicios en modo dev (8080/8443)
# - Ejecuta validaciones
# - Genera auditorías .txt automáticamente (excepto /Croody)

set -euo pipefail

log() { printf "\033[32m[OK]\033[0m %s\n" "$*"; }
warn() { printf "\033[33m[WARN]\033[0m %s\n" "$*"; }
err() { printf "\033[31m[ERR]\033[0m %s\n" "$*"; }

ensure_root() { if [ "${EUID:-$(id -u)}" -ne 0 ]; then err "Ejecuta con sudo"; exit 1; fi; }

install_system_deps() {
  log "Instalando dependencias de sistema"
  apt-get update -y
  apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg lsb-release \
    git jq openssl python3 python3-venv python3-pip \
    make
}

install_docker() {
  log "Instalando Docker y Compose"
  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/$(. /etc/os-release && echo "$ID")/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  chmod a+r /etc/apt/keyrings/docker.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$(. /etc/os-release && echo "$ID") $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
    > /etc/apt/sources.list.d/docker.list
  apt-get update -y
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  systemctl enable --now docker
}

prepare_integrated_stack() {
  log "Preparando stack integrado (dev)"
  cd "$(dirname "$0")"
  if [ ! -d proyecto_integrado ]; then
    err "No existe proyecto_integrado/. Asegúrate de usar la rama con integración."
    exit 1
  fi
  mkdir -p proyecto_integrado/services/telemetry-gateway/data
  mkdir -p proyecto_integrado/services/ids-ml/models
  if [ ! -f proyecto_integrado/gateway/ssl/dev.crt ]; then
    mkdir -p proyecto_integrado/gateway/ssl
    openssl req -x509 -newkey rsa:2048 -nodes \
      -keyout proyecto_integrado/gateway/ssl/dev.key \
      -out proyecto_integrado/gateway/ssl/dev.crt \
      -days 365 -subj "/CN=localhost"
  fi
  log "Levantando servicios (docker compose up)"
  (cd proyecto_integrado && docker compose up -d --build)
}

validate_stack() {
  log "Validando endpoints"
  local BASE=http://localhost:8080
  sleep 3
  curl -s -I $BASE/ | grep -q "302" || { err "Home no respondió 302"; exit 1; }
  curl -s -X POST $BASE/api/telemetry/ingest -H 'Content-Type: application/json' -d '{"data":{"TEMP":21.1,"HUM":48.3}}' | jq -e '.id' >/dev/null || { err "Ingest fallo"; exit 1; }
  curl -s $BASE/api/telemetry/last | jq -e '.data' >/dev/null || { err "Last fallo"; exit 1; }
  curl -s -X POST $BASE/api/ids/predict -H 'Content-Type: application/json' -d '{"rows":[{"src_bytes":600}]}' | jq -e '.predictions' >/dev/null || { err "Predict fallo"; exit 1; }
  log "Validación OK"
}

generate_audits() {
  log "Generando auditorías automáticas (.txt)"
  python3 scripts/generate_audits.py || {
    warn "Instalando dependencias de auditoría (Python stdlib)"; 
    python3 scripts/generate_audits.py;
  }
}

main() {
  ensure_root
  install_system_deps
  install_docker
  prepare_integrated_stack
  validate_stack
  generate_audits
  log "Entorno listo. Web: http://localhost:8080/ | https://localhost:8443/"
}

main "$@"

