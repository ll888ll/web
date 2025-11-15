#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
cd "$root_dir/proyecto_integrado"

RESULTS="${root_dir}/extras/quick_smoke_results.txt"
mkdir -p "${root_dir}/extras"
echo "# Quick smoke run ($(date -Is))" > "$RESULTS"

echo "[check] docker version" | tee -a "$RESULTS"
docker --version | tee -a "$RESULTS"

echo "[check] docker compose version" | tee -a "$RESULTS"
docker compose version | tee -a "$RESULTS"

echo "[up] dev compose (8080/8443)" | tee -a "$RESULTS"
docker compose up -d --build | tee -a "$RESULTS"

echo "[smoke] GET http://localhost:8080/ -> status" | tee -a "$RESULTS"
for i in {1..30}; do
  code=$(curl -sS -o /dev/null -w "%{http_code}\n" http://localhost:8080/ || echo "000")
  echo "attempt=$i dev_status=$code" | tee -a "$RESULTS"
  if [[ "$code" == "200" || "$code" == "302" ]]; then break; fi
  sleep 2
done
if [[ "$code" != "200" && "$code" != "302" ]]; then echo "WARN: Expected 200/302, got $code" | tee -a "$RESULTS"; fi

echo "[smoke] docs via gateway" | tee -a "$RESULTS"
curl -sS -o /dev/null -w "telemetry_docs=%{http_code}\n" http://localhost:8080/api/telemetry/docs | tee -a "$RESULTS" || true
curl -sS -o /dev/null -w "ids_docs=%{http_code}\n" http://localhost:8080/api/ids/docs | tee -a "$RESULTS" || true

# Optional prod stack if .env present
if [[ -f .env ]]; then
  echo "[up] prod local (80/443)" | tee -a "$RESULTS"
  docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env up -d --build | tee -a "$RESULTS"

  echo "[smoke-prod] HEAD https://localhost/ (insecure)" | tee -a "$RESULTS"
  for i in {1..30}; do
    if curl -skI https://localhost/ >> "$RESULTS" 2>/dev/null; then break; else echo "attempt=$i" | tee -a "$RESULTS"; fi
    sleep 2
  done
fi

echo "[ps] containers" | tee -a "$RESULTS"
docker compose ps | tee -a "$RESULTS"

echo "Done. Results at $RESULTS"
