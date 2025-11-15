#!/usr/bin/env bash
set -euo pipefail

ROOT_REQ_MSG="Este script requiere root (sudo)."
if [[ $EUID -ne 0 ]]; then
  echo "$ROOT_REQ_MSG" >&2
  exit 1
fi

BASE_DIR=$(cd "$(dirname "$0")" && pwd)

# Archivos origen
SRC_ENV="$BASE_DIR/env"
SRC_BRIDGE_SH="$BASE_DIR/cicf-bridge.sh"
SRC_CAPTURE_SH="$BASE_DIR/cicf-capture.sh"
SRC_WATCH_SH="$BASE_DIR/cicf-watch.sh"
SRC_VERIFY_SH="$BASE_DIR/cicf-verify.sh"
SRC_DNSMON_PY="$BASE_DIR/cicf-dnsmon.py"
SRC_DNSMON_SH="$BASE_DIR/cicf-dnsmon.sh"
SRC_DNS_GUARD_SH="$BASE_DIR/dns-guard.sh"
SRC_CLEAN_SH="$BASE_DIR/cicf-clean.sh"
SRC_TEST_DNS="$BASE_DIR/test-dns-spoof.sh"
SRC_REPORT_SH="$BASE_DIR/cicf-report.sh"
UNIT_BRIDGE="$BASE_DIR/cicf-bridge.service"
UNIT_CAPTURE="$BASE_DIR/cicf-capture.service"
UNIT_WATCH="$BASE_DIR/cicf-watch.service"
UNIT_DNSMON="$BASE_DIR/cicf-dnsmon.service"
UNIT_DNS_GUARD="$BASE_DIR/dns-guard.service"
UNIT_CLEAN_SVC="$BASE_DIR/cicf-clean.service"
UNIT_CLEAN_TMR="$BASE_DIR/cicf-clean.timer"

# Destinos
CONF_DIR=/etc/cicf
BIN_DIR=/usr/local/bin
SYSTEMD_DIR=/etc/systemd/system
DATA_PCAP=/var/log/cicf/pcap
DATA_FLOWS=/var/log/cicf/flows
APP_DIR=/opt/cicflowmeter

mkdir -p "$CONF_DIR" "$BIN_DIR" "$SYSTEMD_DIR" "$DATA_PCAP" "$DATA_FLOWS" "$APP_DIR"
mkdir -p /var/log/cicf/alerts

# Instala dependencias si hay apt-get (opcional)
if command -v apt-get >/dev/null 2>&1; then
  echo "[install] Instalando dependencias (Kali/Debian) si faltan..."
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y || true
  apt-get install -y git maven default-jdk tcpdump ethtool inotify-tools tshark nftables python3 python3-scapy libpcap0.8 libpcap-dev || true
fi

# Copia config si no existe
if [[ ! -f "$CONF_DIR/env" ]]; then
  cp "$SRC_ENV" "$CONF_DIR/env"
  echo "[install] Copiado config base en $CONF_DIR/env (edítalo para poner IFACE_LEFT/RIGHT)"
else
  echo "[install] Manteniendo config existente en $CONF_DIR/env"
fi

# Copia scripts
install -m 0755 "$SRC_BRIDGE_SH" "$BIN_DIR/"
install -m 0755 "$SRC_CAPTURE_SH" "$BIN_DIR/"
install -m 0755 "$SRC_WATCH_SH" "$BIN_DIR/"
install -m 0755 "$SRC_VERIFY_SH" "$BIN_DIR/"
install -m 0755 "$SRC_DNSMON_PY" "$BIN_DIR/"
install -m 0755 "$SRC_DNSMON_SH" "$BIN_DIR/"
install -m 0755 "$SRC_DNS_GUARD_SH" "$BIN_DIR/"
install -m 0755 "$SRC_CLEAN_SH" "$BIN_DIR/"
install -m 0755 "$SRC_TEST_DNS" "$BIN_DIR/"
install -m 0755 "$SRC_REPORT_SH" "$BIN_DIR/"

# Instala systemd units
install -m 0644 "$UNIT_BRIDGE" "$SYSTEMD_DIR/"
install -m 0644 "$UNIT_CAPTURE" "$SYSTEMD_DIR/"
install -m 0644 "$UNIT_WATCH" "$SYSTEMD_DIR/"
install -m 0644 "$UNIT_DNSMON" "$SYSTEMD_DIR/"
install -m 0644 "$UNIT_DNS_GUARD" "$SYSTEMD_DIR/"
install -m 0644 "$UNIT_CLEAN_SVC" "$SYSTEMD_DIR/"
install -m 0644 "$UNIT_CLEAN_TMR" "$SYSTEMD_DIR/"

# Prepara CICFlowMeter
JAR_DST="$APP_DIR/CICFlowMeter.jar"
JNI_DIR_DST="$APP_DIR/jnetpcap/linux/jnetpcap-1.4.r1425"
mkdir -p "$JNI_DIR_DST"

# Si tenemos el repo ya compilado en el workspace, usamos ese JAR; si no, intentamos compilar
WS_ROOT=$(cd "$BASE_DIR/../.." && pwd)
JAR_SRC="$WS_ROOT/CICFlowMeter/target/CICFlowMeterV3-0.0.4-SNAPSHOT.jar"
JNET_SRC_DIR="$WS_ROOT/CICFlowMeter/jnetpcap/linux/jnetpcap-1.4.r1425"

if [[ -f "$JAR_SRC" ]]; then
  cp "$JAR_SRC" "$JAR_DST"
  echo "[install] Copiado JAR desde workspace: $JAR_SRC"
else
  echo "[install] No se encontró JAR en workspace. Intentando compilar...
  - Clonando repo y ejecutando mvn package (requiere mvn y java)."
  TMP_BUILD=$(mktemp -d)
  git clone --depth=1 https://github.com/ahlashkari/CICFlowMeter.git "$TMP_BUILD/CICFlowMeter"
  (cd "$TMP_BUILD/CICFlowMeter/jnetpcap/linux/jnetpcap-1.4.r1425" && mvn -q install:install-file -Dfile=jnetpcap.jar -DgroupId=org.jnetpcap -DartifactId=jnetpcap -Dversion=1.4.1 -Dpackaging=jar)
  (cd "$TMP_BUILD/CICFlowMeter" && mvn -q -DskipTests package)
  cp "$TMP_BUILD/CICFlowMeter/target/"CICFlowMeterV3-*.jar "$JAR_DST"
  JNET_SRC_DIR="$TMP_BUILD/CICFlowMeter/jnetpcap/linux/jnetpcap-1.4.r1425"
fi

# Copia JNI/jnetpcap
cp -a "$JNET_SRC_DIR/"* "$JNI_DIR_DST/"

systemctl daemon-reload || true
echo "[install] Instalación completada. Revisa y edita /etc/cicf/env antes de habilitar servicios."
echo "Sugerencia: systemctl enable --now cicf-bridge.service cicf-capture.service cicf-watch.service cicf-dnsmon.service"
echo "Sugerencia: systemctl enable --now dns-guard.service"
echo "Sugerencia: systemctl enable --now cicf-clean.timer"
