#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXTRAS_DIR="${ROOT_DIR}/extras"
LOG_FILE="${EXTRAS_DIR}/local_ci_report.md"
mkdir -p "${EXTRAS_DIR}"
: > "${LOG_FILE}"

echo "# Local CI dry-run" >> "${LOG_FILE}"
echo >> "${LOG_FILE}"
echo "- Fecha: $(date -Is)" >> "${LOG_FILE}"
echo "- Commit: $(git -C "${ROOT_DIR}" rev-parse HEAD 2>/dev/null || echo "N/A")" >> "${LOG_FILE}"
echo >> "${LOG_FILE}"

declare -a SUCCESSES=()
declare -a FAILURES=()
declare -a SKIPPED=()
OVERALL_STATUS=0

run_step() {
  local label="$1"
  shift
  if [[ "${1:-}" == "--skip" ]]; then
    local reason="$2"
    {
      echo "### ${label}"
      echo "_SKIPPED: ${reason}_"
      echo
    } >> "${LOG_FILE}"
    SKIPPED+=("${label}")
    return 0
  fi

  local cmd=("$@")
  {
    echo "### ${label}"
    echo '```bash'
    printf '$ %q ' "${cmd[@]}"
    echo
    echo '```'
    echo
    echo '```'
  } >> "${LOG_FILE}"

  if "${cmd[@]}" >> "${LOG_FILE}" 2>&1; then
    echo '```' >> "${LOG_FILE}"
    echo >> "${LOG_FILE}"
    SUCCESSES+=("${label}")
  else
    echo '```' >> "${LOG_FILE}"
    echo >> "${LOG_FILE}"
    FAILURES+=("${label}")
    OVERALL_STATUS=1
  fi
}

command_available() {
  command -v "$1" >/dev/null 2>&1
}

DOMAIN="${BIND_DOMAIN:-${DNS_DOMAIN:-croody.app}}"
MASTER_IP="${BIND_MASTER_PRIVATE_IP:-172.31.42.77}"
SLAVE_IP="${BIND_SLAVE_PRIVATE_IP:-172.31.71.231}"
NS1_FQDN="ns1.${DOMAIN}."
NS2_FQDN="ns2.${DOMAIN}."

if [[ -f "${ROOT_DIR}/infra/dns/bind-master/keys/tsig.env" ]]; then
  # shellcheck source=/dev/null
  source "${ROOT_DIR}/infra/dns/bind-master/keys/tsig.env"
fi
TSIG_KEY_NAME="${TSIG_KEY_NAME:-croody-app-xfer}"
TSIG_KEY_SECRET="${TSIG_KEY_SECRET:-ZmFrZQ==}"

GIT_SHA="$(git -C "${ROOT_DIR}" rev-parse --short HEAD 2>/dev/null || date +%s)"
MASTER_IMAGE="local/bind-master:${GIT_SHA}"
SLAVE_IMAGE="local/bind-slave:${GIT_SHA}"

HAS_DOCKER=0
DOCKER_REASON=""
if command_available docker; then
  if docker info >/dev/null 2>&1; then
    HAS_DOCKER=1
  else
    DOCKER_REASON="Docker daemon no accesible (requiere permisos)."
  fi
else
  DOCKER_REASON="Docker no está instalado."
fi

DOCKER_COMPOSE=()
COMPOSE_REASON=""
if (( HAS_DOCKER )); then
  if docker compose version >/dev/null 2>&1; then
    DOCKER_COMPOSE=(docker compose)
  elif command_available docker-compose; then
    DOCKER_COMPOSE=(docker-compose)
  else
    COMPOSE_REASON="docker compose plugin no disponible."
  fi
else
  COMPOSE_REASON="${DOCKER_REASON:-Docker no disponible.}"
fi

HAS_DIG=0
if command_available dig; then
  HAS_DIG=1
fi

HAS_TERRAFORM=0
if command_available terraform; then
  HAS_TERRAFORM=1
fi

cleanup() {
  if (( HAS_DOCKER )) && [[ ${#DOCKER_COMPOSE[@]} -gt 0 ]]; then
    "${DOCKER_COMPOSE[@]}" -f "${ROOT_DIR}/infra/dns/docker-compose.yml" down --remove-orphans >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

echo "## Terraform" >> "${LOG_FILE}"
if (( HAS_TERRAFORM )); then
  run_step "Terraform fmt" bash -lc "cd '${ROOT_DIR}/infra/terraform' && terraform fmt -recursive"
  run_step "Terraform validate" bash -lc "cd '${ROOT_DIR}/infra/terraform' && terraform validate"
  run_step "Terraform plan" bash -lc "cd '${ROOT_DIR}/infra/terraform' && terraform plan -input=false -lock=false"
else
  run_step "Terraform suite" --skip "Instala Terraform (>=1.5) para ejecutar fmt/validate/plan."
fi

echo "## DNS lint (bind-master/slave)" >> "${LOG_FILE}"
if (( HAS_DOCKER )); then
  run_step "Build BIND image" docker build -t "${MASTER_IMAGE}" "${ROOT_DIR}/infra/dns"
  run_step "Tag slave image" docker tag "${MASTER_IMAGE}" "${SLAVE_IMAGE}"
  run_step "named-checkconf (master)" docker run --rm \
    -e DNS_ROLE=master \
    -e DNS_DOMAIN="${DOMAIN}" \
    -e TSIG_KEY_NAME="${TSIG_KEY_NAME}" \
    -e TSIG_KEY_SECRET="${TSIG_KEY_SECRET}" \
    -e NS1_FQDN="${NS1_FQDN}" \
    -e NS2_FQDN="${NS2_FQDN}" \
    -e ALLOW_QUERY="any;" \
    -e ALLOW_TRANSFER="${SLAVE_IP};" \
    -e NOTIFY_TARGETS="${SLAVE_IP};" \
    -e MASTER_IP="${MASTER_IP}" \
    -v "${ROOT_DIR}/infra/dns/bind-master/zones:/zones" \
    "${MASTER_IMAGE}" \
    named-checkconf /etc/bind/named.conf
  run_step "named-checkzone (master)" docker run --rm \
    -e DNS_ROLE=master \
    -e DNS_DOMAIN="${DOMAIN}" \
    -e TSIG_KEY_NAME="${TSIG_KEY_NAME}" \
    -e TSIG_KEY_SECRET="${TSIG_KEY_SECRET}" \
    -e NS1_FQDN="${NS1_FQDN}" \
    -e NS2_FQDN="${NS2_FQDN}" \
    -v "${ROOT_DIR}/infra/dns/bind-master/zones:/zones" \
    "${MASTER_IMAGE}" \
    named-checkzone "${DOMAIN}" "/zones/${DOMAIN}.db"
  run_step "named-checkconf (slave)" docker run --rm \
    -e DNS_ROLE=slave \
    -e DNS_DOMAIN="${DOMAIN}" \
    -e TSIG_KEY_NAME="${TSIG_KEY_NAME}" \
    -e TSIG_KEY_SECRET="${TSIG_KEY_SECRET}" \
    -e NS1_FQDN="${NS1_FQDN}" \
    -e NS2_FQDN="${NS2_FQDN}" \
    -e MASTER_IP="${MASTER_IP}" \
    -v "${ROOT_DIR}/infra/dns/bind-slave/zones:/zones" \
    "${SLAVE_IMAGE}" \
    named-checkconf /etc/bind/named.conf
else
  run_step "Docker build/lint" --skip "${DOCKER_REASON:-Docker no disponible.}"
fi

if (( HAS_DOCKER )) && [[ ${#DOCKER_COMPOSE[@]} -gt 0 ]]; then
  run_step "docker compose up bind-master" "${DOCKER_COMPOSE[@]}" -f "${ROOT_DIR}/infra/dns/docker-compose.yml" up -d bind-master
  run_step "docker compose up bind-slave" "${DOCKER_COMPOSE[@]}" -f "${ROOT_DIR}/infra/dns/docker-compose.yml" up -d bind-slave
else
  run_step "docker compose stack" --skip "${COMPOSE_REASON:-docker compose no disponible.}"
fi

if (( HAS_DIG )) && (( HAS_DOCKER )) && [[ ${#DOCKER_COMPOSE[@]} -gt 0 ]]; then
  sleep 5
  run_step "dig SOA" dig @127.0.0.1 "${DOMAIN}" SOA
  run_step "dig AXFR" dig @127.0.0.1 "${DOMAIN}" AXFR
else
  if (( ! HAS_DIG )); then
    run_step "dig validations" --skip "Instala 'dig' (bind9-dnsutils) para ejecutar pruebas."
  else
    run_step "dig validations" --skip "${COMPOSE_REASON:-Servicio DNS no levantado.}"
  fi
fi

echo "## Full stack validations" >> "${LOG_FILE}"
if (( HAS_DOCKER )); then
  if [[ -x "${ROOT_DIR}/scripts/validate_full_stack.sh" ]]; then
    run_step "scripts/validate_full_stack.sh" "${ROOT_DIR}/scripts/validate_full_stack.sh"
  else
    run_step "scripts/validate_full_stack.sh" --skip "Script no ejecutable o ausente."
  fi
else
  run_step "scripts/validate_full_stack.sh" --skip "${DOCKER_REASON:-Docker no disponible.}"
fi

{
  echo "## Resumen"
  echo
  echo "- ✅ Éxitos: ${#SUCCESSES[@]}"
  echo "- ⚠️ Pendientes: ${#FAILURES[@]}"
  echo "- ⏭️ Omitidos: ${#SKIPPED[@]}"
  echo
  if ((${#FAILURES[@]} > 0)); then
    echo "### Pasos con error"
    for item in "${FAILURES[@]}"; do
      echo "- ${item}"
    done
    echo
  fi
  if ((${#SKIPPED[@]} > 0)); then
    echo "### Pasos omitidos"
    for item in "${SKIPPED[@]}"; do
      echo "- ${item}"
    done
    echo
  fi
} >> "${LOG_FILE}"

echo "Reporte guardado en ${LOG_FILE}"
exit "${OVERALL_STATUS}"
