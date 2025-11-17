# Terraform — AWS VPC pública/privada

Este módulo provisiona la infraestructura base descrita en los indicativos: VPC con separación de redes, NAT Gateway, subredes para ALB/NAT y para instancias privadas, grupos de seguridad y un bastión para administrar las cargas en la subred privada.

## Estructura

- `provider.tf`, `variables.tf`, `main.tf`, `outputs.tf`: Definición principal que consume módulos internos.
- `modules/network`: Crea VPC, subredes públicas/privadas, IGW, NAT y tablas de enrutamiento.
- `modules/security`: Security Groups para ALB, bastión, capa de aplicación y base de datos.
- `modules/bastion`: EC2 Amazon Linux 2023 con IP pública y SG restringido.

## Variables principales

| Variable | Descripción | Default |
| --- | --- | --- |
| `aws_region` | Región AWS | `us-east-1` |
| `project_name` | Prefijo de tags/nombres | `croody` |
| `vpc_cidr` | CIDR global del VPC | `10.50.0.0/16` |
| `public_subnets` | Lista `{cidr, az}` para subredes públicas | `10.50.10.0/24`, `10.50.20.0/24` |
| `private_subnets` | Lista `{cidr, az}` para subredes privadas | `10.50.110.0/24`, `10.50.210.0/24` |
| `allowed_ssh_cidrs` | CIDRs con acceso SSH al bastión | `["0.0.0.0/0"]` |
| `bastion_instance_type` | Tipo de instancia para el bastión | `t3.micro` |
| `bastion_key_pair` | Nombre del key pair existente | `""` |

## Uso

```bash
cd infra/terraform

# 1. Inicializar providers/módulos
terraform init

# 2. Revisar plan con las variables deseadas
terraform plan -var="project_name=croody-prod" \
               -var="aws_region=us-east-1" \
               -out tfplan

# 3. Aplicar cambios
terraform apply tfplan
```

Para destruir el entorno:

```bash
terraform destroy -var="project_name=croody-prod"
```

## Outputs relevantes

- `vpc_id`, `public_subnet_ids`, `private_subnet_ids`: usados por scripts de despliegue (`deploy_from_scratch.sh`).
- `alb_security_group_id`, `app_security_group_id`, `db_security_group_id`: conectar ALB, ECS/EC2 y bases de datos.
- `bastion_public_ip`: acceso SSH seguro a recursos privados.
- `nat_gateway_id`: para monitoreo de costos/alertas.

## Validación

Incluye un helper simple (`make terraform-plan`) usando comandos estándar:

```bash
terraform fmt -recursive
terraform validate
terraform plan
```

Integra estos pasos en CI/CD antes de aplicar en entornos productivos. Ajusta los CIDRs y la lista de `allowed_ssh_cidrs` según tu política.
