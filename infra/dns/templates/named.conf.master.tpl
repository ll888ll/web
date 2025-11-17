include "/etc/bind/named.conf.options";

acl "transfer_peers" {
    ${ALLOW_TRANSFER}
};

zone "${DNS_DOMAIN}" IN {
    type master;
    file "${ZONE_FILE_PATH}";
    allow-update { none; };
    allow-query { ${ALLOW_QUERY} };
    allow-transfer { key "${TSIG_KEY_NAME}"; ${ALLOW_TRANSFER} };
    also-notify { ${NOTIFY_TARGETS} };
};
