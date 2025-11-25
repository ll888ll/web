#!/usr/bin/env bash
set -euo pipefail

: "${DNS_ROLE:?Set DNS_ROLE to master or slave}"
: "${DNS_DOMAIN:?Set DNS_DOMAIN (e.g., croody.app)}"
: "${TSIG_KEY_NAME:?Set TSIG_KEY_NAME}"
: "${TSIG_KEY_SECRET:?Set TSIG_KEY_SECRET (base64)}"
: "${NS1_FQDN:?Set NS1_FQDN (FQDN with trailing dot)}"
: "${NS2_FQDN:?Set NS2_FQDN (FQDN with trailing dot)}"

BIND_DIR=${BIND_DIR:-/etc/bind}
ZONE_DIR=${ZONE_DIR:-/zones}
KEY_DIR=${KEY_DIR:-/keys}
TEMPLATE_DIR=/templates
ZONE_FILE="${ZONE_DIR}/${DNS_DOMAIN}.db"
ROLE="$(echo "${DNS_ROLE,,}" | tr -d ' ')"

mkdir -p "${BIND_DIR}" "${ZONE_DIR}" "${KEY_DIR}" /var/cache/bind

ALLOW_QUERY="${ALLOW_QUERY:-any;}"
ALLOW_TRANSFER="${ALLOW_TRANSFER:-none;}"
NOTIFY_TARGETS="${NOTIFY_TARGETS:-}"
MASTERS="${MASTERS:-}"
LISTEN_ON="${LISTEN_ON:-any;}"

ZONE_DEFAULT_TTL="${ZONE_DEFAULT_TTL:-3600}"
SOA_EMAIL="${SOA_EMAIL:-hostmaster.${DNS_DOMAIN}}"
SOA_EMAIL_DNS="${SOA_EMAIL//@/.}"
SERIAL="${SERIAL:-$(date +%Y%m%d%H)}"
A_RECORDS="${A_RECORDS:-; add A records via env A_RECORDS}"
AAAA_RECORDS="${AAAA_RECORDS:-; add AAAA records via env AAAA_RECORDS}"
CNAME_RECORDS="${CNAME_RECORDS:-; add CNAME records via env CNAME_RECORDS}"
MX_RECORDS="${MX_RECORDS:-; add MX records via env MX_RECORDS}"
TXT_RECORDS="${TXT_RECORDS:-; add TXT records via env TXT_RECORDS}"
GLUE_RECORDS="${GLUE_RECORDS:-; add glue records via env GLUE_RECORDS}"
ZONE_FILE_PATH="${ZONE_FILE}"

export DNS_DOMAIN TSIG_KEY_NAME TSIG_KEY_SECRET ALLOW_QUERY ALLOW_TRANSFER \
  NOTIFY_TARGETS MASTERS LISTEN_ON NS1_FQDN NS2_FQDN \
  ZONE_DEFAULT_TTL SOA_EMAIL_DNS SERIAL A_RECORDS AAAA_RECORDS \
  CNAME_RECORDS MX_RECORDS TXT_RECORDS GLUE_RECORDS ZONE_FILE_PATH

render() {
  local tpl="$1"
  local dest="$2"
  envsubst <"${tpl}" >"${dest}"
}

render "${TEMPLATE_DIR}/named.conf.options.tpl" "${BIND_DIR}/named.conf.options"

if [[ "${ROLE}" == "master" ]]; then
  if [[ ! -f "${ZONE_FILE}" ]]; then
    echo "Generating initial zone file from template for ${DNS_DOMAIN}"
    # Explicitly generating zone file to ensure valid SOA and no leading whitespace
    cat > "${ZONE_FILE}" <<EOF
\$TTL ${ZONE_DEFAULT_TTL}
@ IN SOA ${NS1_FQDN} ${SOA_EMAIL_DNS}. (
    ${SERIAL}   ; Serial
    3600        ; Refresh
    900         ; Retry
    1209600     ; Expire
    86400       ; Minimum
)

@ IN NS ${NS1_FQDN}
@ IN NS ${NS2_FQDN}
${GLUE_RECORDS}

; ---- A Records ----
${A_RECORDS}

; ---- AAAA Records ----
${AAAA_RECORDS}

; ---- CNAME Records ----
${CNAME_RECORDS}

; ---- MX Records ----
${MX_RECORDS}

; ---- TXT Records ----
${TXT_RECORDS}
EOF
  fi
  render "${TEMPLATE_DIR}/named.conf.master.tpl" "${BIND_DIR}/named.conf"
elif [[ "${ROLE}" == "slave" ]]; then
  : "${MASTER_IP:?Set MASTER_IP (IPv4 of master)}"
  export MASTER_IP
  render "${TEMPLATE_DIR}/named.conf.slave.tpl" "${BIND_DIR}/named.conf"
else
  echo "Unsupported DNS_ROLE: ${DNS_ROLE}" >&2
  exit 1
fi

cat >"${BIND_DIR}/tsig.conf" <<EOF
key "${TSIG_KEY_NAME}" {
    algorithm hmac-sha256;
    secret "${TSIG_KEY_SECRET}";
};
EOF

exec "$@"