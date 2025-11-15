#!/usr/bin/env bash
# Despliegue completo desde cero (Ubuntu/Debian)
# - Instala dependencias de sistema (Docker, Git, curl, jq)
# - Obtiene el proyecto (remoto o local)
# - Prepara estructura y variables de entorno
# - Levanta servicios (gateway + Croody + APIs)
# - Valida el funcionamiento con healthchecks

set -euo pipefail

green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow() { printf "\033[33m%s\033[0m\n" "$*"; }
red() { printf "\033[31m%s\033[0m\n" "$*"; }

# Config por variables de entorno (personalizables)
GIT_URL="${GIT_URL:-}"
LOCAL_PATH="${LOCAL_PATH:-}"
TARGET_DIR="${TARGET_DIR:-/opt/proyecto_empresarial}"
USE_PROD="${USE_PROD:-false}"

ensure_root() {
  if [ "${EUID:-$(id -u)}" -ne 0 ]; then
    red "Este script requiere privilegios de root (sudo)."
    exit 1
  fi
}

detect_os() {
  if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_ID=$ID
  else
    OS_ID="unknown"
  fi
}

install_basics() {
  green "[1/7] Instalando paquetes base"
  case "$OS_ID" in
    ubuntu|debian)
      apt-get update -y
      apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg lsb-release \
        git jq openssl \
        ufw \
        software-properties-common
      ;;
    *)
      red "OS no soportado automáticamente ($OS_ID). Usa Ubuntu/Debian."
      exit 1
      ;;
  esac
}

install_docker() {
  green "[2/7] Instalando Docker Engine + Compose"
  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/$(. /etc/os-release && echo "$ID")/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  chmod a+r /etc/apt/keyrings/docker.gpg
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$(. /etc/os-release && echo "$ID") \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null
  apt-get update -y
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  systemctl enable --now docker

  # Añade el usuario actual al grupo docker si existe un usuario de sesión
  if [ -n "${SUDO_USER:-}" ]; then
    usermod -aG docker "$SUDO_USER" || true
  fi
}

obtain_project() {
  green "[3/7] Obteniendo el proyecto en $TARGET_DIR"
  mkdir -p "$TARGET_DIR"
  if [ -n "$GIT_URL" ]; then
    if [ -d "$TARGET_DIR/.git" ]; then
      yellow "Repositorio ya presente, actualizando..."
      git -C "$TARGET_DIR" fetch --all --tags
      git -C "$TARGET_DIR" reset --hard origin/HEAD || true
    else
      git clone "$GIT_URL" "$TARGET_DIR"
    fi
  elif [ -n "$LOCAL_PATH" ]; then
    rsync -aHAX --delete "$LOCAL_PATH"/ "$TARGET_DIR"/
  else
    yellow "No se especificó GIT_URL ni LOCAL_PATH. Se asumirá que el proyecto ya está en $TARGET_DIR"
  fi
}

prepare_structure() {
  green "[4/7] Preparando estructura y variables de entorno"
  cd "$TARGET_DIR"

  # Carpeta integrada esperada
  if [ ! -d proyecto_integrado ]; then
    red "No se encontró 'proyecto_integrado/'. Asegúrate de usar la versión con integración."
    exit 1
  fi

  mkdir -p proyecto_integrado/services/telemetry-gateway/data
  mkdir -p proyecto_integrado/services/ids-ml/models

  # .env base para prod
  if [ ! -f proyecto_integrado/.env ]; then
    cp proyecto_integrado/.env.example proyecto_integrado/.env || true
    # SECRET_KEY aleatoria
    sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$(openssl rand -hex 24)|" proyecto_integrado/.env || true
  fi

  # Cert dev si no existe
  if [ ! -f proyecto_integrado/gateway/ssl/dev.crt ]; then
    mkdir -p proyecto_integrado/gateway/ssl
    openssl req -x509 -newkey rsa:2048 -nodes \
      -keyout proyecto_integrado/gateway/ssl/dev.key \
      -out proyecto_integrado/gateway/ssl/dev.crt \
      -days 365 -subj "/CN=localhost"
  fi
}

bring_up() {
  green "[5/7] Levantando servicios con Docker Compose"
  cd "$TARGET_DIR/proyecto_integrado"

  # Dev por defecto (puertos 8080/8443). Prod necesita 80/443 libres.
  if [ "$USE_PROD" = "true" ]; then
    if ss -ltn '( sport = :80 )' | grep -q :80; then red "Puerto 80 en uso. Libéralo o usa dev (USE_PROD=false)."; exit 1; fi
    if ss -ltn '( sport = :443 )' | grep -q :443; then red "Puerto 443 en uso. Libéralo o usa dev (USE_PROD=false)."; exit 1; fi
    # Requiere .env con DATABASE_URL, ALLOWED_HOSTS, etc.
    docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env up -d --build
  else
    docker compose up -d --build
  fi
}

validate() {
  green "[6/7] Validando salud del despliegue"
  local BASE="http://localhost:8080"
  [ "$USE_PROD" = "true" ] && BASE="http://localhost" # prod publica en 80

  # Espera simple
  sleep 3
  for i in {1..20}; do
    if curl -sk "${BASE}/" -I | grep -q "HTTP/1.1 302"; then break; fi
    sleep 1
  done

  # Telemetry: ingest + last
  curl -sk "${BASE}/api/telemetry/docs" -o /dev/null || true
  curl -sk -X POST "${BASE}/api/telemetry/ingest" \
    -H 'Content-Type: application/json' \
    -d '{"data":{"TEMP":22.2,"HUM":50.1}}' | grep -q '"id"' || {
      red "Fallo ingest Telemetry"; exit 1; }
  curl -sk "${BASE}/api/telemetry/last" | grep -q '"data"' || {
      red "Fallo consulta Telemetry"; exit 1; }

  # IDS-ML: docs + predict
  curl -sk "${BASE}/api/ids/docs" -o /dev/null || true
  curl -sk -X POST "${BASE}/api/ids/predict" \
    -H 'Content-Type: application/json' \
    -d '{"rows":[{"src_bytes":600},{"src_bytes":10}]}' | grep -q '"predictions"' || {
      red "Fallo predict IDS-ML"; exit 1; }

  green "Validación OK: ${BASE}"
}

post_info() {
  green "[7/7] Despliegue exitoso"
  cat << INFO
Accesos:
- Web:           http://localhost:8080/  (dev)   | https://localhost:8443/
- Telemetry API: http://localhost:8080/api/telemetry/docs
- IDS-ML API:    http://localhost:8080/api/ids/docs

Modo producción (puertos 80/443):
  1) Edita proyecto_integrado/.env (SECRET_KEY, ALLOWED_HOSTS, DATABASE_URL, ALLOWED_ORIGINS, TG_DB_URL, tokens)
  2) docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env up -d --build
INFO
}

main() {
  ensure_root
  detect_os
  install_basics
  install_docker
  obtain_project
  prepare_structure
  bring_up
  validate
  post_info
}

main "$@"

