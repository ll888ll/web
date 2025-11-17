#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DNS_DIR="${ROOT_DIR}/infra/dns"
MASTER_DIR="${DNS_DIR}/bind-master"
SLAVE_DIR="${DNS_DIR}/bind-slave"
SYSTEMD_DIR="${DNS_DIR}/systemd"
KEY_ALGO="${KEY_ALGO:-hmac-sha256}"

usage() {
  cat <<EOF
Uso: $0 --domain ejemplo.com --master-ip 10.0.120.10 --slave-ip 10.0.220.10 [--email admin@ejemplo.com]

Genera llaves TSIG, plantillas de zona y unidades systemd para BIND9.
EOF
  exit 1
}

DOMAIN=""
MASTER_IP=""
SLAVE_IP=""
ADMIN_EMAIL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="$2"; shift ;;
    --master-ip) MASTER_IP="$2"; shift ;;
    --slave-ip) SLAVE_IP="$2"; shift ;;
    --email) ADMIN_EMAIL="$2"; shift ;;
    *) usage ;;
  esac
  shift
done

[[ -n "$DOMAIN" && -n "$MASTER_IP" && -n "$SLAVE_IP" ]] || usage
ADMIN_EMAIL="${ADMIN_EMAIL:-hostmaster@${DOMAIN}}"

mkdir -p "${MASTER_DIR}/zones" "${MASTER_DIR}/keys" \
         "${SLAVE_DIR}/zones" "${SLAVE_DIR}/keys" \
         "${SYSTEMD_DIR}"

KEY_NAME="${DOMAIN//./-}-xfer"
TSIG_FILE_MASTER="${MASTER_DIR}/keys/tsig.env"
TSIG_FILE_SLAVE="${SLAVE_DIR}/keys/tsig.env"

generate_secret() {
  if command -v tsig-keygen >/dev/null 2>&1; then
    tsig-keygen -a "${KEY_ALGO}" "${KEY_NAME}" | awk -F\" '/secret/ {print $2}'
  else
    openssl rand -base64 32
  fi
}

SECRET="$(generate_secret)"

cat > "${TSIG_FILE_MASTER}" <<EOF
TSIG_KEY_NAME=${KEY_NAME}
TSIG_KEY_SECRET=${SECRET}
EOF
cp "${TSIG_FILE_MASTER}" "${TSIG_FILE_SLAVE}"

ZONE_TEMPLATE="${DNS_DIR}/templates/zone.db.tpl"
ZONE_TARGET="${MASTER_DIR}/zones/${DOMAIN}.db"

if [[ ! -f "${ZONE_TARGET}" ]]; then
  SERIAL=$(date +%Y%m%d%H)
  GLUE_RECORDS=$'ns1    3600 IN A '"${MASTER_IP}"$'\nns2    3600 IN A '"${SLAVE_IP}"
  export DNS_DOMAIN="${DOMAIN}" NS1_FQDN="ns1.${DOMAIN}." NS2_FQDN="ns2.${DOMAIN}." \
    ZONE_DEFAULT_TTL=3600 SOA_EMAIL_DNS="${ADMIN_EMAIL//@/.}" SERIAL \
    A_RECORDS="; agrega tus registros A aquí" \
    AAAA_RECORDS="; agrega tus registros AAAA aquí" \
    CNAME_RECORDS="; agrega tus CNAME aquí" \
    MX_RECORDS="; agrega tus MX aquí" \
    TXT_RECORDS="; agrega TXT/SPF aquí" \
    GLUE_RECORDS
  envsubst < "${ZONE_TEMPLATE}" > "${ZONE_TARGET}"
fi

cat > "${MASTER_DIR}/env.example" <<EOF
# Export before running docker compose up bind-master
DNS_ROLE=master
DNS_DOMAIN=${DOMAIN}
NS1_FQDN=ns1.${DOMAIN}.
NS2_FQDN=ns2.${DOMAIN}.
ALLOW_QUERY="any;"
ALLOW_TRANSFER="${SLAVE_IP};"
NOTIFY_TARGETS="${SLAVE_IP};"
SOA_EMAIL=${ADMIN_EMAIL}
MASTER_IP=${MASTER_IP}
source ./keys/tsig.env
EOF

cat > "${SLAVE_DIR}/env.example" <<EOF
DNS_ROLE=slave
DNS_DOMAIN=${DOMAIN}
NS1_FQDN=ns1.${DOMAIN}.
NS2_FQDN=ns2.${DOMAIN}.
ALLOW_QUERY="any;"
MASTER_IP=${MASTER_IP}
source ./keys/tsig.env
EOF

cat > "${SYSTEMD_DIR}/bind-master.service" <<EOF
[Unit]
Description=BIND9 Master (${DOMAIN})
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=/etc/bind/master.env
ExecStart=/usr/sbin/named -4 -u bind -c /etc/bind/named.conf -f
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

cat > "${SYSTEMD_DIR}/bind-slave.service" <<EOF
[Unit]
Description=BIND9 Slave (${DOMAIN})
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=/etc/bind/slave.env
ExecStart=/usr/sbin/named -4 -u bind -c /etc/bind/named.conf -f
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF
Archivos generados:
- ${TSIG_FILE_MASTER} (TSIG) y copia en ${TSIG_FILE_SLAVE}.
- Zona base: ${ZONE_TARGET}
- Env samples: ${MASTER_DIR}/env.example, ${SLAVE_DIR}/env.example
- Systemd units: ${SYSTEMD_DIR}/bind-master.service y bind-slave.service

Actualiza los registros en ${ZONE_TARGET}, exporta las variables y ejecuta docker compose o systemd.
EOF
