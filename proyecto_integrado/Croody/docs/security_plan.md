# Seguridad integral Croody Landing

## 1. Protección contra DDoS
- Script `scripts/security/setup_firewall.sh` instala reglas iptables para tráfico TCP/UDP, drop de paquetes inválidos, limitación por IP y habilita SYN cookies (`net.ipv4.tcp_syncookies=1`).
- Logging de implementación en `security/logs/implementacion_seguridad.txt`.
- Rate limiting configurable por hashlimit y límites por burst.

## 2. Logging avanzado
- `scripts/security/security_logger.py` genera entradas en `security/logs/eventos_seguridad.txt` en español con formato `[ISO8601] | tipo | ip | protocolo | acción | detalle`.
- Ejemplo: `./security_logger.py syn_flood 192.0.2.4 tcp bloqueado "Superó 40 SYN/s"`.

## 3. Protección DNS
- `scripts/security/dns_protection.sh` instala Unbound con DNSSEC, cache seguro y módulo Python que registra spoofing en `/var/log/dns-spoof.log`.
- Directrices para habilitar DNSSEC en servidores autoritativos y validar respuestas localmente.

## 4. Evidencia forense
- `scripts/security/forensics_capture.sh --iface eth0 --dur 120 --tag ataque` captura tráfico en `security/logs/captura_*.pcap` y documenta análisis en `evidencia_forense.txt`.
- Los reportes incluyen timestamp y estadísticos de `tshark` si está disponible.

## 5. Despliegue seguro
- `scripts/security/deploy_security.sh user@host:/ruta` verifica sysctl/iptables/dnssec antes de sincronizar scripts.
- Genera checksums SHA-256 para verificar integridad antes del despliegue.

## 6. Logs y documentación
- Carpeta `security/logs/` centraliza eventos, implementaciones y evidencias.
- Este plan + `docs/ui-audit.md` forman la documentación técnica actualizada.

> Nota: los scripts no se ejecutan automáticamente; deben revisarse y aplicarse con privilegios adecuados en Kali/producción.
