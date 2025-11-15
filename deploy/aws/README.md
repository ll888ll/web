# Receta detallada: desplegar Croody en AWS (Entrega 3)

> Objetivo: tener en AWS la web completa (Gateway + Croody + Telemetry Gateway + IDS-ML),
> con dominio y tokens listos para monitoreo en tiempo real.

---

## 0. Mise en place (preparación)

| Ingrediente | Cómo conseguirlo |
| --- | --- |
| Cuenta AWS + CLI configurada | `aws configure` con tus credenciales |
| Git + SSH + Python en tu máquina | `sudo apt install git awscli` (o equivalente) |
| Este repositorio clonado | `git clone …` |
| Dominio (opcional) | Configura un registro A/CNAME a la IP o ALB |
| Tokens (`TG_INGEST_TOKEN`, `IDS_API_TOKEN`) | Define los valores que compartirás con alumnos/doctores |

Checklist rápido:
- Decide el nombre de la clave SSH (ej. `croody-key`).
- Ten tu IP pública a mano para limitar el puerto 22.
- Copia `proyecto_integrado/.env.example` a `.env` y rellena secretos reales.

---

## 1. Ingredientes base (Security Group + llave SSH)

```bash
# 1.1 Crear llave
aws ec2 create-key-pair --key-name croody-key \
  --query 'KeyMaterial' --output text > croody-key.pem
chmod 400 croody-key.pem

# 1.2 Security Group
aws ec2 create-security-group --group-name croody-sg --description "Croody stack"

# 1.3 Permitir SSH solo desde tu IP (ej. 1.2.3.4)
aws ec2 authorize-security-group-ingress --group-name croody-sg \
  --protocol tcp --port 22 --cidr 1.2.3.4/32

# 1.4 Abrir HTTP/HTTPS para el mundo
aws ec2 authorize-security-group-ingress --group-name croody-sg \
  --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-name croody-sg \
  --protocol tcp --port 443 --cidr 0.0.0.0/0
```

> Si necesitas otros puertos (e.g. 8080 para pruebas internas), agrégalos aquí.

---

## 2. Prepara la “marinada” (`.env`)

1. Duplica el ejemplo:
   ```bash
   cp proyecto_integrado/.env.example proyecto_integrado/.env
   ```
2. Edita la copia con valores reales:
   ```ini
   SECRET_KEY=super-clave
   ALLOWED_HOSTS=croody.midominio.com
   ALLOWED_ORIGINS=https://croody.midominio.com
   TG_INGEST_TOKEN=token-robots
   IDS_API_TOKEN=token-ids
   # Opcional si usarás Postgres externo
   TG_DB_URL=postgresql://telemetry:pass@rds:5432/telemetry
   DATABASE_URL=postgresql://croody:pass@rds:5432/croody
   ```
3. Guarda el archivo. Luego lo subirás a la instancia (paso 4).

---

## 3. Encender el horno: lanzar EC2 con user-data

El script [`deploy/aws/user-data.sh`](user-data.sh) ya instala Docker y ejecuta
`deploy_from_scratch.sh`. Usa Ubuntu 22.04 (AMI `ami-0fc5d935ebf8bc3bc` en
`us-east-1`; cambia la AMI si estás en otra región).

```bash
aws ec2 run-instances \
  --image-id ami-0fc5d935ebf8bc3bc \
  --instance-type t3.small \
  --key-name croody-key \
  --security-groups croody-sg \
  --user-data file://deploy/aws/user-data.sh \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=CroodyProd}]'
```

Obtén la IP pública:
```bash
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=CroodyProd" \
  --query 'Reservations[0].Instances[0].{State:State.Name,IP:PublicIpAddress}'
```

---

## 4. Montaje en la instancia (últimos pasos)

1. Conéctate:
   ```bash
   ssh -i croody-key.pem ubuntu@IP_PUBLICA
   ```
2. Copia el `.env` real desde tu máquina:
   ```bash
   scp -i croody-key.pem proyecto_integrado/.env \
     ubuntu@IP_PUBLICA:/home/ubuntu/repo/proyecto_integrado/.env
   ```
3. Dentro de la instancia, relanza el stack:
   ```bash
   cd /home/ubuntu/repo/proyecto_integrado
   docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env up -d --build
   docker compose ps
   ```

Si preferiste subir tu repo completo vía `scp`, recuerda ejecutar los mismos
comandos dentro de la carpeta `/home/ubuntu/nombre-del-repo`.

---

## 5. Certificados (presentación del plato)

- **Modo rápido**: usa los certificados dev ya montados (`gateway/ssl/dev.crt`).
  Verás un aviso en el navegador, pero es funcional.
- **Modo profesional**:
  - Configura un Load Balancer (ALB) con ACM y apunta el DNS al ALB.
  - O instala Certbot dentro de EC2 (`sudo snap install core; sudo snap install certbot --classic`) y reemplaza el par `dev.crt/dev.key` por
    `/etc/letsencrypt/live/tu-dominio/fullchain.pem` y `privkey.pem`.

---

## 6. Pruebas finales

1. Desde tu PC:
   ```bash
   curl -I https://croody.midominio.com/
   curl https://croody.midominio.com/api/telemetry/healthz
   curl https://croody.midominio.com/api/telemetry/live
   ```
2. Navegador:
   - `https://croody.midominio.com/es/cuenta/registro/` → crea un usuario.
   - `https://croody.midominio.com/robots/monitor/` → verifica telemetría.
3. Cliente Python:
   ```bash
   python3 clients/python/robot_publisher.py \
     --url https://croody.midominio.com/api/telemetry/ingest \
     --token token-robots \
     --robot robot-borealis
   ```
   En segundos deberías ver ese robot en el monitor público.

---

## 7. Mantenimiento y escalado

- **Logs rápidos**: `docker compose logs -f gateway`, `docker compose logs -f croody`, etc.
- **Monitoreo**: activa CloudWatch Logs o integra Prometheus/Loki según tu roadmap.
- **Backups**: si usas SQLite, copia periódicamente los volúmenes; con RDS bastan snapshots.
- **Alta disponibilidad**: empaqueta las imágenes, súbelas a ECR y usa ECS/Fargate o EKS.

---

## 8. Tabla de errores comunes

| Síntoma | Diagnóstico | Solución |
| --- | --- | --- |
| `ssh: Permission denied` | La clave no tiene permisos correctos | `chmod 400 croody-key.pem` |
| `Bad Gateway` desde `/api/telemetry` | Contenedores no levantaron/variables faltan | `docker compose ps` y revisa `.env` |
| `/api/ids/predict` responde 401 | Falta `IDS_API_TOKEN` en `.env` o en la cabecera | Añade el token y reinicia |
| Navegador dice "sitio no seguro" | Certificado dev | Configura Certbot o ALB + ACM |

---

## 9. Inspiración extra

- `deploy/aws/user-data.sh`: punto de partida si quieres personalizar lo que se
  ejecuta al crear la instancia (descarga repo, auto `docker compose up`, etc.).
- `clients/README.md`: explica cómo conectar robots/scripts de terceros.
- `informe_tecnico_entrega3.md`: resumen de cambios aplicados en esta entrega.

Con esto tienes la receta completa. Si en algún paso algo no queda “al dente”,
comparte el comando y el log obtenido para ayudarte a ajustar la sazón.
