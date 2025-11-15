#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
task="${1:-check}"

log() { echo "[check_env] $*"; }
pass() { echo "[PASS] $*"; }
fail() { echo "[FAIL] $*"; exit 1; }

check_cmd() { command -v "$1" >/dev/null 2>&1 && pass "cmd: $1" || fail "cmd missing: $1"; }

port_free() {
  local port="$1"
  if ss -ltn 2>/dev/null | awk '{print $4}' | grep -q ":${port}$"; then
    fail "port ${port} ocupado"
  else
    pass "port ${port} libre"
  fi
}

compile_server() {
  cd "$ROOT_DIR"
  check_cmd gcc
  make
  pass "server compilado"
}

run_smoke_test() {
  cd "$ROOT_DIR"
  local port=9090
  port_free "$port" || true
  ./server $port logs.txt &
  local spid=$!
  # esperar a que escuche
  for i in {1..30}; do
    if (echo >/dev/tcp/127.0.0.1/$port) >/dev/null 2>&1; then break; fi
    sleep 0.2
  done
  set +e
  out=$(python3 test_client.py 127.0.0.1 $port 2>&1)
  rc=$?
  kill $spid 2>/dev/null || true
  wait $spid 2>/dev/null || true
  set -e
  echo "$out"
  [ $rc -eq 0 ] || fail "test_client fallo rc=$rc"
  pass "smoke test OK"
}

case "${task}" in
  check)
    check_cmd python3
    check_cmd make
    check_cmd gcc
    python3 - <<'PY' && pass "tkinter disponible" || echo "[WARN] tkinter no disponible (solo afecta GUI)"
try:
    import tkinter
except Exception as e:
    raise SystemExit(1)
PY
    ;;
  test)
    compile_server
    run_smoke_test
    ;;
  *)
    echo "Uso: $0 [check|test]"; exit 2;
    ;;
esac

