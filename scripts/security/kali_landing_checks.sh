#!/usr/bin/env bash
# Checks básicos de la landing Croody desde Kali.
# No genera carga agresiva: solo validaciones rápidas y logging detallado.

set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
OUT_DIR="$(dirname "$0")/../../proyecto_integrado/Croody/security/logs"
mkdir -p "$OUT_DIR"
LOG_FILE="$OUT_DIR/tests_landing_kali.txt"

log(){
  local msg="$1"
  printf '[%s] %s\n' "$(date -Iseconds)" "$msg" | tee -a "$LOG_FILE"
}

record_security_event(){
  local tipo="$1"
  local accion="$2"
  local detalle="$3"
  local ip="${KALI_SOURCE_IP:-127.0.0.1}"
  local proto="tcp"
  local logger="$(dirname "$0")/security_logger.py"
  if [[ -f "$logger" ]]; then
    python3 "$logger" "$tipo" "$ip" "$proto" "$accion" "$detalle" || true
  fi
}

check_endpoint(){
  local path="$1"
  local label="$2"
  local url="${BASE_URL%/}$path"
  log "Comprobando endpoint ${label} -> ${url}"
  local result
  result=$(curl -k -s -o /dev/null -w "code=%{http_code} tiempo=%{time_total}s bytes=%{size_download}" "$url" || echo "code=000 tiempo=0 bytes=0")
  log "Resultado ${label}: ${result}"
}

check_headers(){
  local path="$1"
  local label="$2"
  local url="${BASE_URL%/}$path"
  log "Inspeccionando cabeceras de seguridad en ${label} -> ${url}"
  local headers
  headers=$(curl -k -s -D - -o /dev/null "$url" || true)
  log "Cabeceras relevantes (${label}):"
  printf '%s\n' "$headers" | grep -iE 'strict-transport-security|content-security-policy|x-frame-options|x-content-type-options|referrer-policy|permissions-policy' | tee -a "$LOG_FILE" || true
}

check_telemetry(){
  local url="${BASE_URL%/}/api/telemetry/ingest"
  if ! command -v python3 >/dev/null 2>&1; then
    log "Python3 no disponible; salto prueba de telemetría"
    return
  fi
  local client="$(dirname "$0")/../../clients/python/robot_publisher.py"
  if [[ ! -f "$client" ]]; then
    log "Cliente de telemetría no encontrado; salto prueba de telemetría"
    return
  fi
  log "Ejecutando prueba corta de telemetría hacia ${url}"
  KALI_SOURCE_IP="${KALI_SOURCE_IP:-127.0.0.1}" \
  python3 "$client" --url "$url" --interval 2 --robot "robot-kali-test" --jitter 0.0005 --lat 19.4326 --lng -99.1332 &
  local pid=$!
  sleep 8
  kill "$pid" 2>/dev/null || true
  log "Prueba de telemetría finalizada (robot-kali-test)"
}

main(){
  log "=== Inicio de batería de tests desde Kali sobre ${BASE_URL} ==="
  record_security_event "test_landing" "inicio" "Inicio de comprobaciones básicas desde Kali contra la landing."

  check_endpoint "/" "home"
  check_endpoint "/buddy/" "buddy"
  check_endpoint "/buddy/suscripciones/" "buddy-suscripciones"
  check_endpoint "/luks/" "luks"
  check_endpoint "/integraciones/" "integraciones"
  check_endpoint "/cuenta/acceder/" "login"
  check_endpoint "/cuenta/registro/" "signup"

  check_headers "/" "home"

  check_telemetry

  record_security_event "test_landing" "fin" "Fin de comprobaciones básicas desde Kali contra la landing."
  log "=== Fin de batería de tests desde Kali ==="
}

main "$@"
