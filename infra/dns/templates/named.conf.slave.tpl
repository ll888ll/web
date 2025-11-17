include "/etc/bind/named.conf.options";

server ${MASTER_IP} {
    keys { "${TSIG_KEY_NAME}"; };
};

zone "${DNS_DOMAIN}" IN {
    type slave;
    masters { ${MASTER_IP} key "${TSIG_KEY_NAME}"; };
    file "${ZONE_FILE_PATH:-/zones/slave-${DNS_DOMAIN}.db}";
    allow-query { ${ALLOW_QUERY} };
    allow-transfer { none; };
};
