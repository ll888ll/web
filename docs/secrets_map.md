# Mapeo de secretos y variables sensibles

| Secreto / variable                      | ¿Dónde se usa?                             | Valor actual / cómo obtenerlo                                                                                           |
| --------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `BIND_DOMAIN`                           | Todos los workflows (`dns-lint`, `bind-*`) | `croody.app`.                                                                                                          |
| `BIND_MASTER_PRIVATE_IP`                | `bind-deploy`, `docs`                      | IP privada del maestro. Ejecutar `aws ec2 describe-instances --instance-ids i-0571eebcb74dfcdb7 --query 'Reservations[0].Instances[0].PrivateIpAddress' --output text`. Resultado actual: **172.31.42.77**. |
| `BIND_SLAVE_PRIVATE_IP`                 | `bind-deploy`, `dns-lint`                  | IP privada del esclavo. Instancia `i-074507051ca06113e`, IP **172.31.71.231**. Misma consulta que arriba cambiando el ID. |
| `BIND_MASTER_HOST` / `BIND_SLAVE_HOST`  | `bind-deploy` (SSH)                        | IP o DNS público para conectarse vía SSH. Maestro `18.118.22.122`, esclavo (asigna EIP o bastion).                      |
| `BIND_SSH_USER` / `BIND_SSH_KEY`        | `bind-deploy`                              | Usuario `ec2-user` y clave privada asociada al par `croody`. El contenido PEM **no** debe estar versionado; cargar como secret multi-line. |
| `BIND_TSIG_KEY_NAME` / `BIND_TSIG_KEY_SECRET` | Workflows + contenedores              | Generados con `scripts/dns/setup_bind.sh`. Últimos valores en `infra/dns/bind-master/keys/tsig.env` (`croody-app-xfer` + `MIIaa4X...`). |
| `AWS_REGION`                            | `bind-deploy` (`aws-actions/amazon-ecr-login`) | `us-east-2` (Ohio).                                                                                              |
| `AWS_ACCOUNT_ID`                        | Documentación / ECR                        | `599297130812`.                                                                                                          |
| `AWS_ECR_REGISTRY`                      | `bind-deploy`                              | `599297130812.dkr.ecr.us-east-2.amazonaws.com`. Se arma como `<account>.dkr.ecr.<region>.amazonaws.com`.                 |
| `BIND_MASTER_ECR_REPO` / `BIND_SLAVE_ECR_REPO` | `bind-deploy`                        | Crea repos en ECR (ej. `bind-master`, `bind-slave`). Ajusta según el nombre real en AWS.                                 |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | `bind-deploy` (login ECR)             | Generar desde IAM → Users → GH → *Create access key*. Guardar ambos valores como secrets.                               |
| `VALIDATION_BASE_URL`                   | `full-stack-validate` + `scripts/validate_full_stack.sh` | Base pública del gateway (ej. `https://croody.app` o `http://localhost:8080`).                                          |
| `CF_API_TOKEN` / `CF_ZONE_ID`           | Cloudflare automation (si aplica)          | Token con permisos DNS Write para la zona `croody.app`. `CF_ZONE_ID` se ve en Overview → API.                            |
| `DEPLOY_HOST/KEY/USER/PORT/PATH`        | Workflows legacy (`deploy*.yml`)           | Solo si se sigue usando despliegue SSH distinto al de BIND.                                                             |

## Cómo refrescar los valores de IP

1. Iniciar sesión en AWS (console o CLI) con el usuario `GH`.
2. Identificar los IDs de instancia (maestro `croody v1`, esclavo `bind-slave`).
3. Ejecutar:
   ```bash
   aws ec2 describe-instances \
     --instance-ids <INSTANCE_ID> \
     --query 'Reservations[0].Instances[0].PrivateIpAddress' \
     --output text \
     --region us-east-2
   ```
4. Actualizar `infra/dns/bind-master/zones/croody.app.db` (registros `ns1`/`ns2`), `infra/dns/*/env.example` y los secrets en GitHub.

## Orden sugerido para agregar/actualizar secrets

1. **DNS básicos:** `BIND_DOMAIN`, `BIND_MASTER_PRIVATE_IP`, `BIND_SLAVE_PRIVATE_IP`, `BIND_TSIG_*`.
2. **SSH/Hosts:** `BIND_MASTER_HOST`, `BIND_SLAVE_HOST`, `BIND_SSH_*`.
3. **AWS / ECR:** `AWS_REGION`, `AWS_ECR_REGISTRY`, `BIND_*_ECR_REPO`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.
4. **Pipelines adicionales:** `VALIDATION_BASE_URL`, `CF_*`, `DEPLOY_*`.

Repite el `scripts/run_local_ci.sh` (o los workflows desde GitHub) cada vez que cambies alguno para validar que no falte nada. 
