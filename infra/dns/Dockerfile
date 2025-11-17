FROM debian:12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    BIND_USER=bind \
    BIND_DIR=/etc/bind \
    ZONE_DIR=/zones \
    KEY_DIR=/keys

RUN apt-get update && \
    apt-get install -y --no-install-recommends bind9 bind9utils dnsutils ca-certificates gettext-base && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /etc/bind

COPY templates /templates
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

VOLUME ["/etc/bind", "/zones", "/keys", "/var/cache/bind"]

EXPOSE 53/tcp 53/udp

ENTRYPOINT ["/entrypoint.sh"]
CMD ["named", "-g", "-u", "bind"]
