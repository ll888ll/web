$TTL ${ZONE_DEFAULT_TTL}
@   IN  SOA ${NS1_FQDN} ${SOA_EMAIL_DNS}. (
        ${SERIAL}   ; Serial
        3600        ; Refresh
        900         ; Retry
        1209600     ; Expire
        86400       ; Minimum
)

@           IN  NS      ${NS1_FQDN}
@           IN  NS      ${NS2_FQDN}
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