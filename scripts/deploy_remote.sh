#!/usr/bin/env bash
# Deploys the current git HEAD to a remote server via SSH, mirroring the GitHub Action.
# Usage:
#   DEPLOY_HOST=18.224.180.61 DEPLOY_USER=ec2-user DEPLOY_KEY=~/croody.pem DEPLOY_PATH=/home/ec2-user ./scripts/deploy_remote.sh
set -euo pipefail

: "${DEPLOY_HOST:?set DEPLOY_HOST}"
: "${DEPLOY_USER:?set DEPLOY_USER}"
: "${DEPLOY_KEY:?set DEPLOY_KEY (path to PEM)}"
: "${DEPLOY_PATH:?set DEPLOY_PATH}"
DEPLOY_PORT="${DEPLOY_PORT:-22}"

REPO_ROOT="$(git rev-parse --show-toplevel)"
ARCHIVE="$(mktemp /tmp/telematicache.XXXXXX.tar.gz)"
trap 'rm -f "$ARCHIVE"' EXIT

( cd "$REPO_ROOT" && tar -czf "$ARCHIVE" . )

scp -P "$DEPLOY_PORT" -i "$DEPLOY_KEY" -o StrictHostKeyChecking=no "$ARCHIVE" "$DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH/telematicache.tar.gz"

env DEPLOY_ROOT="$DEPLOY_PATH" ssh -P "$DEPLOY_PORT" -i "$DEPLOY_KEY" -o StrictHostKeyChecking=no "$DEPLOY_USER@$DEPLOY_HOST" 'bash -s' <<'REMOTE'
set -euo pipefail
ARCHIVE="$DEPLOY_ROOT/telematicache.tar.gz"
REPO_DIR="$DEPLOY_ROOT/repo"
BACKUP_ENV="$DEPLOY_ROOT/.env.backup"

if [ -f "$REPO_DIR/proyecto_integrado/.env" ]; then
  cp "$REPO_DIR/proyecto_integrado/.env" "$BACKUP_ENV"
fi

rm -rf "$REPO_DIR"
mkdir -p "$REPO_DIR"
tar -xzf "$ARCHIVE" -C "$REPO_DIR"
rm -f "$ARCHIVE"
if [ -f "$BACKUP_ENV" ]; then
  mv "$BACKUP_ENV" "$REPO_DIR/proyecto_integrado/.env"
fi

cd "$REPO_DIR/proyecto_integrado"
docker compose down || true
docker compose up -d --build telemetry-gateway ids-ml robot-sim croody gateway

docker compose ps
REMOTE
