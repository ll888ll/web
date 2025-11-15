#!/usr/bin/env bash
set -euo pipefail

# End-to-end setup on Ubuntu/Debian: installs Docker, clones repo if needed,
# prepares .env, brings up dev and (optionally) prod, and performs basic tests.

LOG_DIR="extras"
LOG_CMDS="$LOG_DIR/manual_commands_linux.txt"
mkdir -p "$LOG_DIR"

log_cmd() { echo "$*" >> "$LOG_CMDS"; }

run() { log_cmd "$*"; eval "$@"; }

# 1) Detect OS and install dependencies
if [[ -r /etc/os-release ]]; then . /etc/os-release; else ID=debian; fi

log_cmd "# Update package index and install dependencies"
if command -v sudo >/dev/null 2>&1; then PREFIX="sudo "; else PREFIX=""; fi

run ${PREFIX}apt-get update -y
run ${PREFIX}apt-get install -y git curl jq python3 ca-certificates gnupg lsb-release

# Docker Engine + compose plugin (Debian/Ubuntu official repo)
if ! command -v docker >/dev/null 2>&1; then
  log_cmd "# Install Docker Engine and Compose plugin"
  run ${PREFIX}install -m 0755 -d /etc/apt/keyrings
  run ${PREFIX}bash -c "curl -fsSL https://download.docker.com/linux/${ID}/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg"
  run ${PREFIX}chmod a+r /etc/apt/keyrings/docker.gpg
  run ${PREFIX}bash -c "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/${ID} $(. /etc/os-release && echo \$VERSION_CODENAME) stable\" > /etc/apt/sources.list.d/docker.list"
  run ${PREFIX}apt-get update -y
  run ${PREFIX}apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi

# Enable/start docker
if systemctl list-unit-files | grep -q docker.service; then
  run ${PREFIX}systemctl enable --now docker
fi

# Add user to docker group if needed
if [[ "${SUDO_USER:-$USER}" != "root" ]]; then
  log_cmd "# Add current user to docker group"
  run ${PREFIX}usermod -aG docker "${SUDO_USER:-$USER}" || true
fi

# 2) Clone repo if executed outside a git working copy
if [[ ! -d .git ]]; then
  : "${GIT_URL:=https://example.com/your/repo.git}"
  log_cmd "# Clone repository"; echo "Cloning $GIT_URL ..."
  run git clone "$GIT_URL" repo
  cd repo
fi

# 3) Prepare .env for production compose
cd proyecto_integrado
if [[ ! -f .env ]]; then
  log_cmd "# Prepare .env from sample"
  run cp .env.production.sample .env
  # Minimal auto-fill
  run sed -i "s/^ENV=.*/ENV=production/" .env
  run sed -i "s/^ALLOWED_HOSTS=.*/ALLOWED_HOSTS=localhost/" .env
  # SECRET_KEY 64+ random
  SECRET_KEY=$(openssl rand -base64 64 | tr -d '\n')
  log_cmd "export SECRET_KEY=***generated***"
  run sed -i "s/^SECRET_KEY=.*/SECRET_KEY=${SECRET_KEY}/" .env
fi

# 4) Bring up dev stack
log_cmd "# Bring up dev compose (8080/8443)"
run docker compose up -d --build

# 5) Smoke tests (dev)
log_cmd "# Smoke test dev homepage"
run bash -c "curl -sS -I http://localhost:8080/ | tee -a ../extras/smoke_dev.txt"
log_cmd "# Docs endpoints"
run bash -c "curl -sS -o /dev/null -w 'telemetry_docs=%{http_code}\n' http://localhost:8080/api/telemetry/docs | tee -a ../extras/smoke_dev.txt"
run bash -c "curl -sS -o /dev/null -w 'ids_docs=%{http_code}\n' http://localhost:8080/api/ids/docs | tee -a ../extras/smoke_dev.txt"

# 6) Optional prod stack
log_cmd "# Bring up prod local (80/443)"
run docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env up -d --build
log_cmd "# Smoke test prod homepage"
run bash -c "curl -k -sSI https://localhost/ | tee -a ../extras/smoke_prod.txt"

# 7) Post-deploy sample API calls
log_cmd "# Telemetry demo ingest"
run bash -c "curl -sS -X POST http://localhost:8080/api/telemetry/ingest -H 'Content-Type: application/json' -d '{\"client\":\"demo\",\"value\":42}' | tee -a ../extras/smoke_dev.txt"
log_cmd "# Telemetry last"
run bash -c "curl -sS http://localhost:8080/api/telemetry/last | tee -a ../extras/smoke_dev.txt"
log_cmd "# IDS predict (fallback)"
run bash -c "curl -sS -X POST http://localhost:8080/api/ids/predict -H 'Content-Type: application/json' -d '{\"features\":[0.1,0.2,0.3]}' | tee -a ../extras/smoke_dev.txt"

echo "Commands recorded in $LOG_CMDS"

