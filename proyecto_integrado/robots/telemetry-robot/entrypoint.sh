#!/usr/bin/env bash
set -euo pipefail
LOG_PATH=${ROBOT_LOG_PATH:-/tmp/robot.log}
PORT=${ROBOT_PORT:-9090}
./server "$PORT" "$LOG_PATH" &
exec python /app/bridge_ingest.py
