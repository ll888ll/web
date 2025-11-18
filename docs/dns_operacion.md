# Operación DNS Autoritativo (BIND9)

## Alta/modificación de registros

1. Edita la zona relevante (`infra/dns/bind-master/zones/<dominio>.db`). Usa comentarios por bloque y mantén el serial (`YYYYMMDDnn`).  
2. Ejecuta `scripts/dns/setup_bind.sh` si se requieren nuevas llaves o plantillas.  
3. Validación local:
   ```bash
   cd infra/dns
   docker build -t bind-master-test .
   docker run --rm -v "$PWD/bind-master/zones:/zones" \
     -e DNS_ROLE=master -e DNS_DOMAIN=<dominio> \
     -e TSIG_KEY_NAME=... -e TSIG_KEY_SECRET=... \
     bind-master-test named-checkzone <dominio> /zones/<dominio>.db
   ```
4. Para repetir lo mismo que en GitHub Actions sin depender de la nube, ejecuta `scripts/run_local_ci.sh`. Este script compila las imágenes, corre `named-checkconf`, `named-checkzone`, levanta `docker compose` y genera un reporte en `extras/local_ci_report.md`.
5. Commit + push → workflow `bind-deploy` construye imágenes, publica cambios y ejecuta `rndc reload` en maestro/esclavo.

## Variables críticas / secrets

| Dato                            | Valor actual | Cómo refrescar                                                                                              |
| ------------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------- |
| `BIND_DOMAIN`                   | `croody.app` | —                                                                                                           |
| `BIND_MASTER_PRIVATE_IP` (`ns1`) | `172.31.42.77` | `aws ec2 describe-instances --instance-ids i-0571eebcb74dfcdb7 --query 'Reservations[0].Instances[0].PrivateIpAddress' --output text --region us-east-2` |
| `BIND_SLAVE_PRIVATE_IP` (`ns2`)  | `172.31.71.231` | `aws ec2 describe-instances --instance-ids i-074507051ca06113e --query 'Reservations[0].Instances[0].PrivateIpAddress' --output text --region us-east-2` |
| `BIND_TSIG_KEY_NAME/SECRET`     | `croody-app-xfer` / `MIIaa4Xqmccq+sbYfk0O7bTR9BJd1k4/Gsi/rnCEmIk=` | `scripts/dns/setup_bind.sh` genera llaves nuevas si se requiere rotación. |

El resto de secretos (ECR, SSH, Cloudflare) están mapeados en `docs/secrets_map.md`.

## Failover maestro/esclavo

| Escenario | Acción |
| --- | --- |
| Caída del esclavo (`ns2`) | 1) Promueve temporalmente `ns1` (maestro) exponiendo su IP mediante EIP/SG público. 2) Actualiza glue en registrador si el downtime será prolongado. |
| Caída del maestro (`ns1`) | 1) Forzar `ns2` a cargar la zona existente (`named-checkzone`). 2) Reconfigurar `also-notify` a la IP del nuevo maestro temporal. 3) Restaurar maestro original y ejecutar `rndc retransfer <dominio>`. |
| Rotación de TSIG | Regenera con `scripts/dns/setup_bind.sh`, actualiza `bind-master/keys/tsig.env` y `bind-slave/keys/tsig.env`, redeploy. |

## Pruebas operativas (`dig`)

| Comando | Propósito |
| --- | --- |
| `dig @ns1.<dominio> <dominio> SOA` | Confirmar que el maestro responde y serial correcto. |
| `dig @ns2.<dominio> <dominio> AXFR -y name:key` | Validar transferencias AXFR/TSIG. |
| `dig @ns2.<dominio> api.<dominio> A +trace` | Confirmar resolución pública vía esclavo. |
| `rndc status` (en cada host) | Estado del servicio, número de zonas y eventos de recarga. |

## Logs y alertas

- Maestros/esclavos montan `/var/log/named`; envía a CloudWatch o ELK.  
- Configura alertas en CloudWatch Metric Filters: *AXFR fallidos*, *rndc reload errors*, *query spikes*.  
- Usa `scripts/security/security_logger.py` o similar para registrar eventos críticos.

## Checklist post-cambio

1. Serial incrementado y commit documentado.  
2. Validación `named-checkzone` y `named-checkconf` OK (`scripts/run_local_ci.sh`).  
3. Workflow `bind-deploy` finaliza sin errores.  
4. `dig SOA`, `dig A`, `dig AXFR` apuntando a ambas IPs responde con nuevos datos.  
5. Dashboard de monitoreo (CloudWatch/ELK) sin eventos críticos posteriores al despliegue.
