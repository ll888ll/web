Resumen

Este proyecto despliega un sensor transparente (bridge) con captura de PCAPs y extracción de flows con CICFlowMeter, más defensa y monitor de suplantación DNS. Está preparado para Kali/Debian.

Componentes

- Bridge L2: `br0` une `IFACE_LEFT` (atacante) y `IFACE_RIGHT` (víctima).
- Captura rotada: `tcpdump` escribe PCAPs en `/var/log/cicf/pcap`.
- Flows CSV: CICFlowMeter convierte cada PCAP en `/var/log/cicf/flows`.
- DNS Guard: nftables en el bridge (allowlist de resolvers).
- DNS Monitor: analiza PCAPs y alerta suplantaciones.
- Limpieza: purga periódica de PCAP/CSV.

Instalación rápida (Kali)

1) Ajusta NICs y DNS (opcional): edita `ops/cicf/env`.
2) Instala todo (depende de sudo/root):
   - `sudo ops/cicf/install.sh`
3) Auto‑configuración y arranque (elige NICs automáticamente o pasa dos):
   - `sudo ops/cicf/auto-configure.sh`
   - o: `sudo ops/cicf/auto-configure.sh enp1s0 enp2s0`

Servicios principales

- `cicf-bridge.service` (bridge `br0`): une NICs y desactiva offloads.
- `cicf-capture.service` (tcpdump): rotación por tiempo/tamaño configurable.
- `cicf-watch.service` (CICFlowMeter): genera `<pcap>_Flow.csv`.
- `cicf-dnsmon.service` (tshark): escribe alertas en `/var/log/cicf/alerts/dnsmon.log`.
- `dns-guard.service` (nftables): permite DNS solo hacia `ALLOWED_DNS`.
- `cicf-clean.timer` (diario): purga ficheros antiguos.

Configuración

- Fichero: `/etc/cicf/env` (se crea desde `ops/cicf/env`).
- Claves:
  - `IFACE_LEFT`, `IFACE_RIGHT`: NICs físicas (sin IP asignada).
  - `BRIDGE_ADMIN_IP`: IP/CIDR opcional en `br0` para gestión.
  - `ALLOWED_DNS`: lista blanca (coma-separado) de resolvers.
  - `DNS_GUARD_MODE`: `allowlist` para bloquear resto, `off` para desactivar.
  - `CAP_ROTATE_SECONDS` o `CAP_ROTATE_SIZE_MB`, `CAP_BPF` (filtro tcpdump).
  - Retención: define `PCAP_RET_DAYS` y `FLOWS_RET_DAYS` si quieres cambiarlo.

Rutas

- PCAPs: `/var/log/cicf/pcap`
- Flows CSV: `/var/log/cicf/flows`
- Alertas DNS: `/var/log/cicf/alerts/dnsmon.log`

Comandos útiles

- Instalación: `sudo ops/cicf/install.sh`
- Auto‑configurar y arrancar: `sudo ops/cicf/auto-configure.sh [IF_LEFT IF_RIGHT]`
- Verificación: `sudo /usr/local/bin/cicf-verify.sh`
- Informe en Markdown: `sudo /usr/local/bin/cicf-report.sh` (genera `/var/log/cicf/report-YYYYmmdd-HHMMSS.md`)
- Reglas DNS guard: `sudo nft list table bridge cicf`
- Logs servicios: `sudo journalctl -u cicf-bridge -u cicf-capture -u cicf-watch -u cicf-dnsmon -f`

Pruebas / Auto‑test

- Auto‑test integral: `sudo ops/cicf/selftest.sh`
  - Genera un PCAP con respuesta DNS spoof, convierte a CSV y valida alertas UNAUTH_SRC/LOW_TTL.
- Prueba sintética manual:
  - `sudo /usr/local/bin/test-dns-spoof.sh`
  - `sudo python3 /usr/local/bin/cicf-dnsmon.py /var/log/cicf/pcap/dns-spoof-test.pcap`

Notas y seguridad

- El bridge quita IP a las NICs miembro; asigna IP de gestión a `br0` o usa una tercera NIC para administración.
- `dns-guard` actúa a nivel L2 (familia bridge): limita estrictamente UDP/TCP 53 a `ALLOWED_DNS`.
- Para excluir servicios de captura, añade `CAP_BPF` (ej.: `not port 22`).
