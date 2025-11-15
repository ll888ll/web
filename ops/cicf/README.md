Resumen rápido

- Esto despliega CICFlowMeter como sensor en puente transparente (bridge) entre atacante y víctima.
- Captura PCAPs rotados y convierte a CSV de flows automáticamente.
- Ajusta las NICs en `ops/cicf/env` (IFACE_LEFT/IFACE_RIGHT) y ejecuta `sudo ops/cicf/install.sh`.

Componentes

- Bridge: `cicf-bridge.service` crea `br0` y asocia las dos NICs físicas.
- Captura: `cicf-capture.service` (tcpdump) rota PCAPs en `/var/log/cicf/pcap`.
- Conversión: `cicf-watch.service` convierte PCAPs a CSV en `/var/log/cicf/flows` con CICFlowMeter.
 - DNS Monitor: `cicf-dnsmon.service` analiza PCAPs y alerta suplantaciones (tshark requerido).
 - DNS Guard: `dns-guard.sh` aplica lista blanca de DNS con nftables (opcional).

Rutas y ficheros

- Config: `/etc/cicf/env` (se crea desde `ops/cicf/env` si no existe).
- Binarios: `/usr/local/bin/cicf-*.sh`.
- Systemd: `/etc/systemd/system/cicf-*.service`.
- Datos: `/var/log/cicf/pcap` y `/var/log/cicf/flows`.
 - Alertas DNS: `/var/log/cicf/alerts/dnsmon.log`.

Instalación (Kali)

1) Edita `ops/cicf/env` y pon tus interfaces reales (ej. `enp1s0` y `enp2s0`).
2) Ejecuta: `sudo ops/cicf/install.sh` (instala dependencias en Kali: tshark, nftables, python3-scapy, maven, etc.)
3) Auto‑configurar y arrancar todo: `sudo ops/cicf/auto-configure.sh` (o pásale dos NICs: `sudo ops/cicf/auto-configure.sh enp1s0 enp2s0`).
4) (Opcional) Defensa activa DNS manual: `sudo /usr/local/bin/dns-guard.sh` o habilita `sudo systemctl enable --now dns-guard.service` (lee `/etc/cicf/env`).

Verificación

- Tráfico: `sudo tcpdump -i br0 -c 5`
- PCAPs: `ls -l /var/log/cicf/pcap`
- CSVs: `ls -l /var/log/cicf/flows`
 - DNS Monitor: `tail -f /var/log/cicf/alerts/dnsmon.log`

Autotest

- Ejecuta prueba integral en Kali: `sudo ops/cicf/selftest.sh`
  - Genera un PCAP con spoof DNS.
  - Convierte a CSV con CICFlowMeter.
  - Analiza con el DNS monitor (tshark) y valida alertas.
  - Muestra estado y rutas.

Defensa contra suplantación DNS

- Configura `ALLOWED_DNS` en `/etc/cicf/env` (coma-separado) y `DNS_GUARD_MODE=allowlist`.
- Aplica reglas: `sudo /usr/local/bin/dns-guard.sh`. Esto limita consultas/respuestas DNS a los servidores permitidos (nftables familia bridge).
- El monitor (`cicf-dnsmon.service`) genera alertas por:
  - Respuestas desde IP no permitida (UNAUTH_SRC).
  - Respuestas sin consulta correlacionada o fuera de ventana (TXID_MISS).
  - Cambios bruscos de A-record en ventana corta (MULTI_ANS).
  - TTL muy bajo (LOW_TTL) y respuestas a IP privada (PRIVATE_IP).

Pruebas

- Lanza tráfico real entre atacante y víctima y observa PCAP/CSV.
- Para pruebas sintéticas de DNS:
  - Genera y analiza un PCAP artificial: `sudo /usr/local/bin/test-dns-spoof.sh` (requiere `python3-scapy`).
  - O reproduce PCAPs por `tcpreplay` en `br0` o deja PCAPs en `/var/log/cicf/pcap`; el monitor los analizará automáticamente.

Requisitos (Kali)

- Paquetes APT (lista en `ops/cicf/requirements-apt-kali.txt`):
  - git, maven, openjdk-17-jdk, tcpdump, ethtool, inotify-tools, tshark, nftables, python3, python3-scapy.
- Python (opcional/pip): `ops/cicf/requirements.txt` (Scapy), aunque en Kali se instala por APT.
