#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DNS_DIR="${ROOT_DIR}/infra/dns"
EVIDENCE_DIR="${ROOT_DIR}/extras"
EVIDENCE_FILE="${EVIDENCE_DIR}/evidencias_finales.md"
BASE_URL="${BASE_URL:-http://localhost:8080}"
ZONE_FILE="${DNS_DIR}/bind-master/zones/${BIND_DOMAIN:-${DNS_DOMAIN:-example.com}}.db"

mkdir -p "${EVIDENCE_DIR}"
: > "${EVIDENCE_FILE}"

log_section() {
  local title="$1"
  printf '\n## %s\n\n' "$title" >> "${EVIDENCE_FILE}"
}

capture_cmd() {
  local title="$1"; shift
  log_section "$title"
  printf '```bash\n$ %s\n```\n\n' "$*" >> "${EVIDENCE_FILE}"
  printf '```\n' >> "${EVIDENCE_FILE}"
  "$@" >> "${EVIDENCE_FILE}" 2>&1 || true
  printf '\n```\n' >> "${EVIDENCE_FILE}"
}

log_section "Inicio"
printf "Fecha: %s\nRepositorio: %s\n\n" "$(date -Is)" "$(git rev-parse HEAD)" >> "${EVIDENCE_FILE}"

# 1. Terraform plan/apply (opcional -plan only).
cd "${ROOT_DIR}/infra/terraform"
capture_cmd "terraform fmt" terraform fmt -recursive
capture_cmd "terraform validate" terraform validate
capture_cmd "terraform plan (dry-run)" terraform plan -input=false -lock=false || true
cd "${ROOT_DIR}"

# 2. Levantar DNS (docker compose)
cd "${DNS_DIR}"
capture_cmd "docker compose up bind-master" docker compose up -d bind-master
sleep 5
capture_cmd "docker compose up bind-slave" docker compose up -d bind-slave
sleep 5
# Logs PS
capture_cmd "docker compose ps (DNS)" docker compose ps

# 3. Pruebas DIG
capture_cmd "dig SOA (master)" dig @127.0.0.1 "${BIND_DOMAIN:-${DNS_DOMAIN:-example.com}}" SOA
capture_cmd "dig AXFR (master->slave)" dig @127.0.0.1 "${BIND_DOMAIN:-${DNS_DOMAIN:-example.com}}" AXFR || true

# 4. Pruebas APP (curl + e2e)
capture_cmd "curl /healthz" curl -sk "${BASE_URL}/api/telemetry/healthz"
capture_cmd "curl /api/telemetry/live" curl -sk "${BASE_URL}/api/telemetry/live" || true

if command -v pytest >/dev/null 2>&1; then
  capture_cmd "pytest tests/e2e/test_gateway_smoke.py" \
    BASE_URL="${BASE_URL}" pytest tests/e2e/test_gateway_smoke.py
else
  printf "pytest not installed; skipping e2e tests\n" >> "${EVIDENCE_FILE}"
fi

# 5. Recopilar logs DNS
LOG_MASTER="${DNS_DIR}/bind-master/logs/named.log"
if [[ -f "${LOG_MASTER}" ]]; then
  capture_cmd "named.log (master)" tail -n 200 "${LOG_MASTER}"
fi

# 6. Estado final docker compose (app stack si aplica)
cd "${ROOT_DIR}/proyecto_integrado"
if command -v docker >/dev/null 2>&1; then
  capture_cmd "docker compose ps (app)" docker compose ps || true
fi

printf "\nValidación completada. Evidencias en %s\n" "${EVIDENCE_FILE}"
