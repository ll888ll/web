options {
    directory "/var/cache/bind";
    listen-on port 53 { ${LISTEN_ON} };
    listen-on-v6 { none; };
    allow-query { ${ALLOW_QUERY} };
    allow-recursion { none; };
    recursion no;
    dnssec-validation yes;
    auth-nxdomain no;
    minimal-responses yes;
    rate-limit {
        responses-per-second 100;
    };
};

include "/etc/bind/tsig.conf";
