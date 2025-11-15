#!/usr/bin/env bash
set -euo pipefail

CONF=${CONF:-/etc/cicf/env}
export CONF
exec /usr/bin/env python3 /usr/local/bin/cicf-dnsmon.py
