#!/usr/bin/env bash
set -euo pipefail

CONF=${CONF:-/etc/cicf/env}
if [[ ! -f "$CONF" ]]; then
  echo "[cicf-watch] Falta fichero de configuración: $CONF" >&2
  exit 1
fi
# shellcheck disable=SC1090
. "$CONF"

PCAP_DIR=${PCAP_DIR:-/var/log/cicf/pcap}
FLOWS_DIR=${FLOWS_DIR:-/var/log/cicf/flows}
CICF_HOME=${CICF_HOME:-/opt/cicflowmeter}
JAR=${CICF_JAR:-$CICF_HOME/CICFlowMeter.jar}
JNI=${CICF_JNI_DIR:-$CICF_HOME/jnetpcap/linux/jnetpcap-1.4.r1425}
JNETJAR=${CICF_JNETPCAP_JAR:-$CICF_HOME/jnetpcap/linux/jnetpcap-1.4.r1425/jnetpcap.jar}
INTERVAL=${WATCH_INTERVAL_SECONDS:-10}

mkdir -p "$PCAP_DIR" "$FLOWS_DIR"

echo "[cicf-watch] Jar: $JAR"
echo "[cicf-watch] JNI: $JNI"

while true; do
  for f in "$PCAP_DIR"/*.pcap; do
    [[ -e "$f" ]] || break
    base=$(basename "$f")
    out="$FLOWS_DIR/${base}_Flow.csv"
    if [[ -f "$out" ]]; then
      continue
    fi
    echo "[cicf-watch] Procesando $f -> $out"
    # Ejecuta CLI sobre un único pcap y directorio de salida
    if ! java -Djava.library.path="$JNI" -cp "$JAR:$JNETJAR" cic.cs.unb.ca.ifm.Cmd "$f" "$FLOWS_DIR"; then
      echo "[cicf-watch] Error al procesar $f" >&2
    fi
  done
  sleep "$INTERVAL"
done

