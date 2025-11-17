# DNS autoritativo (BIND9 en contenedores)

Esta carpeta contiene la infraestructura necesaria para desplegar servidores DNS autoritativos primario/secundario con BIND9 usando Docker. Todo es parametrizable mediante variables de entorno y plantillas, permitiendo automatizar la generación de zonas, llaves TSIG y configuración.

## Componentes

- `Dockerfile`: imagen base (Debian + BIND9) que copia las plantillas y un `entrypoint` capaz de renderizarlas según variables.
- `templates/`: incluye `named.conf` para master/slave, opciones endurecidas y `zone.db.tpl`.
- `docker-compose.yml`: ejemplo local con servicios `bind-master` y `bind-slave`.
- `scripts/dns/setup_bind.sh`: script para generar llaves TSIG, plantillas de zona y unidades systemd para despliegues bare-metal.

## Requerimientos de red

- **Maestro**: desplegar en subred privada (ej. `10.0.120.0/24`) en AZ A. Sólo debe permitir tráfico entrante en puertos 53 TCP/UDP y AXFR (TCP 53) desde:
  - Load balancer/servidores internos (consultas).
  - Servidor esclavo (transferencias y notificaciones).
- **Esclavo**: desplegar en otra AZ (ej. `10.0.220.0/24`) para resiliencia. Debe abrir 53 TCP/UDP para resolutores externos mientras mantiene AXFR únicamente desde el maestro (TSIG obligatorio).
- Usar Security Groups distintos: uno para consultas públicas (esclavo) y otro restringido (maestro). Registrar glue records en el registrador apuntando a IPs públicas del esclavo (o ambos si se exponen).

## Variables clave

| Variable | Descripción |
| --- | --- |
| `DNS_ROLE` | `master` o `slave`. |
| `DNS_DOMAIN` | Dominio raíz (ej. `croody.app`). |
| `TSIG_KEY_NAME` / `TSIG_KEY_SECRET` | Datos de la llave HMAC-SHA256 para AXFR/NOTIFY. |
| `NS1_FQDN` / `NS2_FQDN` | Servidores de nombres declarados (terminar en `.`). |
| `ALLOW_QUERY` | ACL para consultas (ej. `any;` o rangos privados). |
| `ALLOW_TRANSFER` | ACL adicional además de TSIG (ej. `10.0.220.10;`). |
| `NOTIFY_TARGETS` | Lista IP esclavos a notificar. |
| `MASTER_IP` | Sólo esclavo: IP privada del maestro. |
| `A_RECORDS`, `AAAA_RECORDS`, `CNAME_RECORDS`, `MX_RECORDS`, `TXT_RECORDS`, `GLUE_RECORDS` | Bloques multilinea con registros específicos. |

## Flujo sugerido

1. Ejecuta `scripts/dns/setup_bind.sh --domain croody.app --master-ip 10.0.120.10 --slave-ip 10.0.220.10` para generar:
   - Llaves TSIG (`infra/dns/bind-master/keys/tsig.env` y `bind-slave/...`).
   - Plantilla de zona en `bind-master/zones/<dominio>.db`.
   - Plantillas de unidades systemd (`infra/dns/systemd/`).
2. Edita la zona generada, completando `A_RECORDS`, `GLUE_RECORDS`, etc.
3. Construye imágenes: `docker compose build bind-master bind-slave`.
4. Despliega en AWS:
   - Crea subred privada para `bind-master` (sin IP pública) y otra para `bind-slave` (puede tener EIP o detrás de ALB/UDP load balancer).
   - Usa `docker compose` o `systemd` en cada host (EC2) con las variables exportadas.
   - Asegura que sólo los puertos 53 TCP/UDP estén expuestos públicamente en el esclavo.
5. Registra glue records con el registrador (ej. `ns1.croody.app` -> IP `bind-master` si público; `ns2.croody.app` -> IP `bind-slave`).

## Validaciones

- Sintaxis: `named-checkconf /etc/bind/named.conf` y `named-checkzone croody.app /zones/croody.app.db`.
- Transferencias: `dig @<master-ip> croody.app AXFR -y <TSIG_KEY_NAME>:<TSIG_KEY_SECRET>`.
- Consultas externas: `dig @<slave-public-ip> api.croody.app A`.

## Bare-metal

Si prefieres evitar contenedores, copia `templates/*.tpl`, renderiza con `setup_bind.sh --bare` y utiliza las unidades systemd generadas en `infra/dns/systemd/`. Ajusta rutas a `/etc/bind` y `/var/cache/bind`.

Mantén los secretos (TSIG) fuera del repositorio y utiliza mecanismos como AWS Secrets Manager o SSM Parameter Store para inyectarlos en tiempo de despliegue.
