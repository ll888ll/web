#!/usr/bin/env bash
# Bootstrap a GitHub Actions self-hosted runner on this machine (Linux x64).
# Usage (as ec2-user):
#   export GH_URL=https://github.com/ll333ll/telematicache
#   export RUNNER_TOKEN=YOUR_RUNNER_TOKEN
#   export RUNNER_LABELS=deploy
#   bash scripts/setup_self_hosted_runner.sh
set -euo pipefail

RUNNER_DIR="$HOME/actions-runner"
GH_URL="${GH_URL:?set GH_URL to your repository URL}"
RUNNER_TOKEN="${RUNNER_TOKEN:?set RUNNER_TOKEN from GitHub runner UI}"
RUNNER_LABELS="${RUNNER_LABELS:-deploy}"
RUNNER_VERSION="2.311.0"

mkdir -p "$RUNNER_DIR"
cd "$RUNNER_DIR"
if [ ! -f "actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz" ]; then
  curl -fsSL -o "actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz" \
    "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"
fi
tar xzf "actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"

./config.sh --url "$GH_URL" --token "$RUNNER_TOKEN" --labels "$RUNNER_LABELS" --unattended

sudo ./svc.sh install
sudo ./svc.sh start

echo "Runner installed and started. Labels: $RUNNER_LABELS"
