# Terraform Infrastructure - Documentación Completa

## Resumen
La infraestructura de Croody implementa una arquitectura AWS multi-tier con red VPC, subnets públicas y privadas, NAT Gateway, security groups segmentados y un host bastion para administración segura. Utiliza Terraform 1.7+ con módulos reutilizables, AWS provider v5+, y sigue las mejores prácticas de seguridad de AWS.

## Ubicación
- **Infraestructura Principal**: `/infra/terraform/`
- **Módulos**: `/infra/terraform/modules/`
  - `network/` - VPC, Subnets, NAT Gateway, Route Tables
  - `security/` - Security Groups (ALB, App, DB, Bastion)
  - `bastion/` - EC2 Instance para SSH jump host
- **Configuración**: `main.tf`, `provider.tf`, `variables.tf`, `outputs.tf`

## Arquitectura General

### Diagrama de Infraestructura
```
┌─────────────────────────────────────────────────────────────────┐
│                          Internet Gateway                       │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                            VPC                                  │
│                      10.50.0.0/16                               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Public Subnet AZ-a (10.50.10.0/24)                       │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │          NAT Gateway + Elastic IP                │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │        Bastion Host (EC2 t3.micro)               │    │  │
│  │  │      ┌──────────────────────────────────┐       │    │  │
│  │  │      │  ALB Security Group              │       │    │  │
│  │  │      │  Port 80/443 from Internet       │       │    │  │
│  │  │      └──────────────────────────────────┘       │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │ Public Subnet AZ-b (10.50.20.0/24)               │    │  │
│  │  │  [Reserved for Multi-AZ redundancy]              │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Private Subnet AZ-a (10.50.110.0/24)                     │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │     App Security Group                           │    │  │
│  │  │  ┌────────────────────────────────────────┐     │    │  │
│  │  │  │   Port 80 from ALB                     │     │    │  │
│  │  │  │   Port 22 from Bastion (SSH)           │     │    │  │
│  │  │  └────────────────────────────────────────┘     │    │  │
│  │  │  [ECS/EKS/EC2 Instances - Future]              │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │     DB Security Group                            │    │  │
│  │  │  ┌────────────────────────────────────────┐     │    │  │
│  │  │  │   Port 5432 from App Tier Only         │     │    │  │
│  │  │  └────────────────────────────────────────┘     │    │  │
│  │  │  [RDS PostgreSQL - Future]                     │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Private Subnet AZ-b (10.50.210.0/24)                     │  │
│  │  [Reserved for Multi-AZ DB/App instances]                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Configuración de Provider

### Terraform Configuration
```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
```

**Versiones**:
- **Terraform**: >= 1.5.0 (mínimo requerido para nuevos features)
- **AWS Provider**: >= 5.0 (última versión estable)
- **Región por defecto**: us-east-1 (N. Virginia)

**Justificación de Versiones**:
- Terraform 1.5+: Soporte para `check` blocks y mejor manejo de drift
- AWS Provider 5.0+: Soporte para EC2 Instance Connect, mejoras en RDS

## Configuración de Variables

### Variables Globales
```hcl
variable "aws_region" {
  description = "AWS region donde se crearán los recursos"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefijo para el nombre/tag de todos los recursos"
  type        = string
  default     = "croody"
}

variable "vpc_cidr" {
  description = "Bloque CIDR para la VPC"
  type        = string
  default     = "10.50.0.0/16"
}

variable "public_subnets" {
  description = "Lista de subnets públicas (para ALB/NAT/Bastion)"
  type = list(object({
    cidr = string
    az   = string
  }))
  default = [
    { cidr = "10.50.10.0/24", az = "us-east-1a" },
    { cidr = "10.50.20.0/24", az = "us-east-1b" }
  ]
}

variable "private_subnets" {
  description = "Lista de subnets privadas (para app/db)"
  type = list(object({
    cidr = string
    az   = string
  }))
  default = [
    { cidr = "10.50.110.0/24", az = "us-east-1a" },
    { cidr = "10.50.210.0/24", az = "us-east-1b" }
  ]
}

variable "allowed_ssh_cidrs" {
  description = "Rangos CIDR permitidos para SSH al bastion"
  type        = list(string)
  default     = ["0.0.0.0/0"]  # ¡Cambiar en producción!
}

variable "bastion_instance_type" {
  description = "Tipo de instancia EC2 para el host bastion"
  type        = string
  default     = "t3.micro"
}

variable "bastion_key_pair" {
  description = "Nombre del key pair EC2 existente para bastion"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags adicionales aplicados a los recursos"
  type        = map(string)
  default     = {}
}
```

### Subnet Configuration

**Subnets Públicas** (2 AZs):
- **AZ-a**: `10.50.10.0/24` (us-east-1a)
- **AZ-b**: `10.50.20.0/24` (us-east-1b)
- **Uso**: NAT Gateway, Bastion Host, futuro ALB

**Subnets Privadas** (2 AZs):
- **AZ-a**: `10.50.110.0/24` (us-east-1a)
- **AZ-b**: `10.50.210.0/24` (us-east-1b)
- **Uso**: ECS/EKS/App instances, RDS

### Security Configuration

**SSH Access**:
- **Bastion**: Puerto 22, acceso controlado por `allowed_ssh_cidrs`
- **Recomendación Producción**: Limitar a IPs corporativas específicas
- **Ejemplo**:
  ```hcl
  allowed_ssh_cidrs = ["203.0.113.0/24", "198.51.100.0/24"]
  ```

## Módulo Network

### VPC Configuration
```hcl
resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = merge(local.base_tags, { Name = "${var.project_name}-vpc" })
}
```

**Características**:
- **DNS Support**: Habilitado para resolución interna
- **DNS Hostnames**: Habilitado para asignar DNS names a instancias
- **Naming**: `{project_name}-vpc` (ej: `croody-vpc`)

### Internet Gateway
```hcl
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.this.id
  tags   = merge(local.base_tags, { Name = "${var.project_name}-igw" })
}
```

**Propósito**: Conecta la VPC a Internet para subnets públicas

### Subnets

#### Public Subnets
```hcl
resource "aws_subnet" "public" {
  for_each = { for idx, subnet in var.public_subnets : idx => subnet }

  vpc_id                  = aws_vpc.this.id
  cidr_block              = each.value.cidr
  availability_zone       = each.value.az
  map_public_ip_on_launch = true  # ¡Importante para públicas!

  tags = merge(local.base_tags, {
    Name = "${var.project_name}-public-${each.value.az}"
    Tier = "public"
  })
}
```

**Configuración**:
- `map_public_ip_on_launch = true`: Asigna IP pública automáticamente
- **Tag Tier**: `public` para identificación

#### Private Subnets
```hcl
resource "aws_subnet" "private" {
  for_each = { for idx, subnet in var.private_subnets : idx => subnet }

  vpc_id                  = aws_vpc.this.id
  cidr_block              = each.value.cidr
  availability_zone       = each.value.az
  map_public_ip_on_launch = false  # No asigna IP pública

  tags = merge(local.base_tags, {
    Name = "${var.project_name}-private-${each.value.az}"
    Tier = "private"
  })
}
```

**Configuración**:
- `map_public_ip_on_launch = false`: Mantiene instancias privadas
- **Tag Tier**: `private` para identificación

### NAT Gateway

#### EIP for NAT
```hcl
resource "aws_eip" "nat" {
  domain = "vpc"
  tags   = merge(local.base_tags, { Name = "${var.project_name}-nat-eip" })
}
```

#### NAT Gateway Instance
```hcl
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = values(aws_subnet.public)[0].id  # Primera subnet pública
  tags          = merge(local.base_tags, { Name = "${var.project_name}-nat" })
  depends_on    = [aws_internet_gateway.igw]
}
```

**Características**:
- **Single NAT**: Despliegue en una AZ para reducir costos
- **EIP**: IP elástica para NAT Gateway
- **Dependencies**: Espera a que el IGW esté creado

**Costo**: NAT Gateway ~$45/mes + charges por data transfer

### Route Tables

#### Public Route Table
```hcl
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = merge(local.base_tags, { Name = "${var.project_name}-public-rt" })
}

resource "aws_route_table_association" "public" {
  for_each       = aws_subnet.public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}
```

**Configuración**:
- **Route**: `0.0.0.0/0` → Internet Gateway
- **Associations**: Todas las subnets públicas

#### Private Route Table
```hcl
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }

  tags = merge(local.base_tags, { Name = "${var.project_name}-private-rt" })
}

resource "aws_route_table_association" "private" {
  for_each       = aws_subnet.private
  subnet_id      = each.value.id
  route_table_id = aws_route_table.private.id
}
```

**Configuración**:
- **Route**: `0.0.0.0/0` → NAT Gateway
- **Associations**: Todas las subnets privadas
- **Beneficio**: Permite outbound Internet desde subnets privadas

### Network Module Outputs
```hcl
output "vpc_id" {
  value = aws_vpc.this.id
}

output "public_subnet_ids" {
  value = [for s in aws_subnet.public : s.id]
}

output "private_subnet_ids" {
  value = [for s in aws_subnet.private : s.id]
}

output "public_route_table_id" {
  value = aws_route_table.public.id
}

output "private_route_table_id" {
  value = aws_route_table.private.id
}

output "nat_gateway_id" {
  value = aws_nat_gateway.nat.id
}
```

## Módulo Security

### Arquitectura de Security Groups

#### 1. ALB Security Group
```hcl
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-alb-sg"
  description = "Allow HTTP/HTTPS from Internet"
  vpc_id      = var.vpc_id

  # Inbound rules
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound rules
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.base_tags, { Name = "${var.project_name}-alb-sg" })
}
```

**Permisos**:
- **Inbound**: Puerto 80/443 desde Internet
- **Outbound**: Todo el tráfico permitido
- **Uso**: Application Load Balancer (futuro)

#### 2. Bastion Security Group
```hcl
resource "aws_security_group" "bastion" {
  name        = "${var.project_name}-bastion-sg"
  description = "SSH access to bastion"
  vpc_id      = var.vpc_id

  # Inbound rules
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidrs
  }

  # Outbound rules
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.base_tags, { Name = "${var.project_name}-bastion-sg" })
}
```

**Permisos**:
- **Inbound**: Puerto 22 (SSH) desde CIDRs configurados
- **Outbound**: Todo el tráfico permitido
- **Uso**: EC2 Bastion Host

#### 3. App Security Group
```hcl
resource "aws_security_group" "app" {
  name        = "${var.project_name}-app-sg"
  description = "Allow traffic from ALB"
  vpc_id      = var.vpc_id

  # Inbound rules
  ingress {
    description     = "HTTP from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  ingress {
    description     = "SSH from bastion"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  # Outbound rules
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.base_tags, { Name = "${var.project_name}-app-sg" })
}
```

**Permisos**:
- **Inbound**: Puerto 80 desde ALB Security Group
- **Inbound**: Puerto 22 desde Bastion Security Group (SSH tunneling)
- **Outbound**: Todo el tráfico permitido
- **Uso**: ECS/EKS/EC2 instances para aplicaciones

#### 4. DB Security Group
```hcl
resource "aws_security_group" "db" {
  name        = "${var.project_name}-db-sg"
  description = "DB access from app tier only"
  vpc_id      = var.vpc_id

  # Inbound rules
  ingress {
    description     = "Postgres from app tier"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  # Outbound rules
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.base_tags, { Name = "${var.project_name}-db-sg" })
}
```

**Permisos**:
- **Inbound**: Puerto 5432 (PostgreSQL) solo desde App Security Group
- **Outbound**: Todo el tráfico permitido
- **Uso**: RDS PostgreSQL instance

### Security Group Outputs
```hcl
output "alb_sg_id" {
  value = aws_security_group.alb.id
}

output "bastion_sg_id" {
  value = aws_security_group.bastion.id
}

output "app_sg_id" {
  value = aws_security_group.app.id
}

output "db_sg_id" {
  value = aws_security_group.db.id
}
```

### Security Best Practices

#### Principle of Least Privilege
- **App SG**: Solo permite tráfico desde ALB y bastion
- **DB SG**: Solo permite tráfico desde app tier
- **No CIDR-based DB access**: Previene acceso directo a DB

#### Defense in Depth
1. **Network Level**: Subnets privadas para app/DB
2. **Instance Level**: Security groups por tier
3. **Protocol Level**: Solo puertos necesarios abiertos

#### Recomendaciones Adicionales
```hcl
# Para producción, añadir:
# 1. Security group rules más específicas
# 2. Network ACLs (NACLs) adicionales
# 3. VPC Flow Logs para auditoría
# 4. GuardDuty para threat detection

resource "aws_flow_log" "vpc" {
  count           = var.enable_flow_logs ? 1 : 0
  iam_role_arn    = aws_iam_role.vpc_flow_log.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_log.arn
  traffic_type    = "ALL"
  vpc_id          = var.vpc_id
}
```

## Módulo Bastion

### AMI Data Source
```hcl
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
```

**Características**:
- **Amazon Linux 2023**: Última versión LTS
- **HVM**: Virtualización Hardware Virtual Machine
- **Most Recent**: Siempre la AMI más nueva
- **Owners**: Solo AMIs oficiales de AWS

### EC2 Instance
```hcl
resource "aws_instance" "bastion" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [var.security_group_id]
  associate_public_ip_address = true
  key_name                    = var.key_name != "" ? var.key_name : null

  tags = merge(local.base_tags, { Name = "${var.project_name}-bastion" })
}

resource "aws_eip" "bastion" {
  domain   = "vpc"
  instance = aws_instance.bastion.id
  tags     = merge(local.base_tags, { Name = "${var.project_name}-bastion-eip" })
}
```

**Configuración**:
- **Instance Type**: `t3.micro` (configurable)
- **Subnet**: Primera subnet pública
- **Public IP**: Asociada vía Elastic IP
- **Key Pair**: Opcional, configurable
- **Purpose**: SSH jump host para acceso seguro a privados

### Bastion Variables
```hcl
variable "project_name" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "security_group_id" {
  type = string
}

variable "instance_type" {
  type = string
}

variable "key_name" {
  type    = string
  default = ""
}

variable "tags" {
  type    = map(string)
  default = {}
}
```

### Bastion Outputs
```hcl
output "instance_id" {
  value = aws_instance.bastion.id
}

output "public_ip" {
  value = aws_eip.bastion.public_ip
}

output "subnet_id" {
  value = var.subnet_id
}
```

## Configuración Principal

### Main.tf Composition
```hcl
# Módulo Network - VPC, Subnets, NAT
module "network" {
  source          = "./modules/network"
  project_name    = var.project_name
  vpc_cidr        = var.vpc_cidr
  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets
  tags            = var.tags
}

# Módulo Security - Security Groups
module "security" {
  source            = "./modules/security"
  project_name      = var.project_name
  vpc_id            = module.network.vpc_id
  allowed_ssh_cidrs = var.allowed_ssh_cidrs
  tags              = var.tags
}

# Módulo Bastion - EC2 Jump Host
module "bastion" {
  source            = "./modules/bastion"
  project_name      = var.project_name
  subnet_id         = module.network.public_subnet_ids[0]
  security_group_id = module.security.bastion_sg_id
  instance_type     = var.bastion_instance_type
  key_name          = var.bastion_key_pair
  tags              = var.tags
}
```

### Dependency Graph
```
main.tf
  ├─> module.network
  │      ├─> aws_vpc.this
  │      ├─> aws_internet_gateway.igw
  │      ├─> aws_subnet.public
  │      ├─> aws_subnet.private
  │      ├─> aws_nat_gateway.nat
  │      └─> aws_route_table.*
  │
  ├─> module.security
  │      ├─> aws_security_group.alb (requires vpc_id)
  │      ├─> aws_security_group.bastion (requires vpc_id)
  │      ├─> aws_security_group.app (requires vpc_id + bastion_sg_id)
  │      └─> aws_security_group.db (requires vpc_id + app_sg_id)
  │
  └─> module.bastion
         ├─> aws_instance.bastion (requires subnet_id + security_group_id)
         └─> aws_eip.bastion (requires instance_id)
```

## Outputs Globales

### Networking Outputs
```hcl
output "vpc_id" {
  value = module.network.vpc_id
}

output "public_subnet_ids" {
  value = module.network.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.network.private_subnet_ids
}

output "nat_gateway_id" {
  value = module.network.nat_gateway_id
}
```

### Security Outputs
```hcl
output "alb_security_group_id" {
  value = module.security.alb_sg_id
}

output "app_security_group_id" {
  value = module.security.app_sg_id
}

output "db_security_group_id" {
  value = module.security.db_sg_id
}
```

### Bastion Outputs
```hcl
output "bastion_public_ip" {
  value = module.bastion.public_ip
}

output "bastion_instance_id" {
  value = module.bastion.instance_id
}
```

## Deployment Guide

### Prerequisites
```bash
# 1. Instalar Terraform
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Verificar versión
terraform version

# 2. Configurar AWS CLI
aws configure
# AWS Access Key ID: ******
# AWS Secret Access Key: ******
# Default region name: us-east-1
# Default output format: json

# 3. Verificar credenciales
aws sts get-caller-identity
```

### Deployment Steps

#### 1. Inicializar Terraform
```bash
cd /infra/terraform

# Inicializar backend y descargar providers
terraform init

# Verificar configuración
terraform validate
```

#### 2. Plan de Deployment
```bash
# Generar plan de ejecución
terraform plan -out=tfplan

# Ver el plan
terraform show tfplan

# O ver directamente
terraform plan -var="project_name=myproject"
```

#### 3. Aplicar Configuración
```bash
# Aplicar cambios (confirma con 'yes')
terraform apply tfplan

# O directamente (con confirmación automática)
terraform apply -auto-approve

# Ver outputs
terraform output
```

#### 4. Verificar Deployment
```bash
# Ver recursos creados
terraform state list

# Ver output específico
terraform output vpc_id
terraform output bastion_public_ip

# Describir recursos AWS
aws ec2 describe-vpcs --vpc-ids $(terraform output -raw vpc_id)
aws ec2 describe-instances --filters "Name=tag:Name,Values=croody-bastion"
```

### Custom Variables

#### Usando terraform.tfvars
```hcl
# Crear archivo terraform.tfvars
cat > terraform.tfvars << EOF
aws_region         = "us-east-1"
project_name       = "croody-prod"
vpc_cidr           = "10.50.0.0/16"

public_subnets = [
  { cidr = "10.50.10.0/24", az = "us-east-1a" },
  { cidr = "10.50.20.0/24", az = "us-east-1b" }
]

private_subnets = [
  { cidr = "10.50.110.0/24", az = "us-east-1a" },
  { cidr = "10.50.210.0/24", az = "us-east-1b" }
]

allowed_ssh_cidrs = ["203.0.113.0/24", "198.51.100.0/24"]

bastion_instance_type = "t3.small"
bastion_key_pair      = "my-ec2-keypair"

tags = {
  Environment = "production"
  Owner       = "devops@croody.com"
  CostCenter  = "engineering"
}
EOF
```

#### Variables via Command Line
```bash
terraform plan \
  -var="project_name=staging" \
  -var="allowed_ssh_cidrs=[\"0.0.0.0/0\"]" \
  -var="bastion_instance_type=t3.micro"
```

#### Variables via Environment
```bash
export TF_VAR_project_name="croody-dev"
export TF_VAR_allowed_ssh_cidrs='["0.0.0.0/0"]'
terraform plan
```

### Estado Remoto (Recomendado)

#### S3 Backend
```hcl
# Añadir a provider.tf o crear backend.tf
terraform {
  backend "s3" {
    bucket = "croody-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
    # Habilitar estado bloqueado para prevenir modificaciones concurrentes
    lock_id = "prod-lock"
  }
}
```

#### Inicializar Estado Remoto
```bash
# Crear bucket S3 manualmente
aws s3 mb s3://croody-terraform-state

# Migrar estado local a remoto
terraform init -migrate-state

# Verificar
terraform state list
```

## Comandos Terraform

### Comandos Básicos
```bash
# Inicializar
terraform init

# Formatear código
terraform fmt -recursive

# Validar sintaxis
terraform validate

# Plan de cambios
terraform plan

# Aplicar cambios
terraform apply

# Destruir recursos
terraform destroy

# Ver estado
terraform show

# Listar recursos
terraform state list
```

### Comandos de Estado
```bash
# Pull estado remoto
terraform state pull > terraform.tfstate

# Push estado local
terraform state push terraform.tfstate

# Mover recurso entre estados
terraform state mv aws_instance.old aws_instance.new

# Reemplazar recurso
terraform apply -replace="aws_instance.bastion"

# Listar recursos remotos
terraform state list
```

### Comandos de Import
```bash
# Importar recurso existente
terraform import aws_instance.bastion i-0123456789abcdef0

# Import con ID específico
terraform import module.bastion.aws_instance.bastion i-0123456789abcdef0
```

### Comandos de Output
```bash
# Ver todos los outputs
terraform output

# Ver output específico
terraform output vpc_id

# Output en formato JSON
terraform output -json

# Raw output (sin formato)
terraform output -raw bastion_public_ip
```

### Comandos de Graph
```bash
# Generar gráfico de dependencias
terraform graph | dot -Tpng > infrastructure.png

# Ver dependencias
terraform graph | grep "aws_" | head -20
```

## Security Hardening

### 1. SSH Access Control
```hcl
# ❌ Mal: Acceso abierto al mundo
allowed_ssh_cidrs = ["0.0.0.0/0"]

# ✅ Bien: Solo IPs corporativas
allowed_ssh_cidrs = [
  "203.0.113.0/24",    # Office IP range
  "198.51.100.0/24",   # VPN IP range
]

# ✅ Mejor: Usar AWS Session Manager (sin SSH)
# Modificar security group para denegar puerto 22
# y usar Systems Manager para acceso
```

### 2. VPC Flow Logs
```hcl
resource "aws_flow_log" "vpc" {
  iam_role_arn    = aws_iam_role.vpc_flow_log.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_log.arn
  traffic_type    = "ALL"
  vpc_id          = module.network.vpc_id
}

resource "aws_iam_role" "vpc_flow_log" {
  name = "${var.project_name}-vpc-flow-log-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "vpc-flow-logs.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "vpc_flow_log" {
  name              = "/aws/vpc/flow-logs"
  retention_in_days = 30
}
```

### 3. Network ACLs (NACLs)
```hcl
resource "aws_network_acl" "private" {
  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.private_subnet_ids

  # Ephemeral ports para outbound
  ingress {
    rule_no    = 100
    protocol   = "tcp"
    from_port  = 1024
    to_port    = 65535
    cidr_block = "0.0.0.0/0"
    action     = "allow"
  }

  # SSH desde bastion solo
  ingress {
    rule_no         = 110
    protocol        = "tcp"
    from_port       = 22
    to_port         = 22
    cidr_block      = var.vpc_cidr
    action          = "allow"
  }

  # HTTP/HTTPS desde ALB
  ingress {
    rule_no         = 120
    protocol        = "tcp"
    from_port       = 80
    to_port         = 80
    cidr_block      = "10.50.0.0/16"
    action          = "allow"
  }

  egress {
    rule_no    = 100
    protocol   = "tcp"
    from_port  = 1024
    to_port    = 65535
    cidr_block = "0.0.0.0/0"
    action     = "allow"
  }

  tags = merge(local.base_tags, { Name = "${var.project_name}-private-nacl" })
}
```

### 4. GuardDuty Integration
```hcl
resource "aws_guardduty_detector" "this" {
  enable = true
  tags   = local.base_tags
}
```

### 5. VPC Endpoints (Futuro)
```hcl
# Para acceder a S3/DynamoDB desde subnets privadas
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = module.network.vpc_id
  service_name      = "com.amazonaws.${var.aws_region}.s3"
  route_table_ids   = module.network.private_route_table_ids
  vpc_endpoint_type = "Gateway"
}
```

## Monitoreo y Alertas

### CloudWatch Metrics
```hcl
resource "aws_cloudwatch_metric_alarm" "bastion_cpu" {
  alarm_name          = "${var.project_name}-bastion-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "Bastion host CPU utilization is high"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    InstanceId = module.bastion.instance_id
  }
}

resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-alerts"
}

resource "aws_sns_topic_subscription" "email_alerts" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = "devops@croody.com"
}
```

## Cost Optimization

### NAT Gateway Alternatives
```hcl
# ❌ Costo: $45/mes + data transfer
resource "aws_nat_gateway" "nat" {
  # ... configuración
}

# ✅ Alternativa 1: NAT Instance (~$5/mes)
resource "aws_instance" "nat" {
  ami           = data.aws_ami.amazon_linux_nat.id
  instance_type = "t3.small"
  subnet_id     = var.public_subnet_ids[0]
  # ... más config

  source_dest_check = false  # Importante para NAT
}

# ✅ Alternativa 2: Egress-only Internet Gateway (para IPv6)
resource "aws_egress_only_internet_gateway" "this" {
  vpc_id = var.vpc_id
}
```

### Spot Instances para Bastion
```hcl
resource "aws_instance" "bastion" {
  # ... otros configs

  # Para non-critical workloads
  # spot_config puede ahorrar 50-90%
  # ⚠️ ADVERTENCIA: No usar para producción crítica
}
```

## Troubleshooting

### Error: "Public IP not associated"
```bash
# Verificar subnet configuration
aws ec2 describe-subnets --subnet-ids subnet-12345678 \
  --query 'Subnets[0].MapPublicIpOnLaunch'
# Debe ser true

# Verificar instance
aws ec2 describe-instances --instance-id i-12345678 \
  --query 'Reservations[0].Instances[0].PublicIpAddress'
```

**Solución**:
```hcl
# En aws_subnet.public, asegurar:
map_public_ip_on_launch = true

# En aws_instance.bastion:
associate_public_ip_address = true
```

### Error: "Failed to create NAT Gateway"
```bash
# Verificar si hay suficientes EIPs disponibles
aws ec2 describe-addresses --query 'Addresses[?InstanceId==null]'
```

**Causa**: Límite de EIPs en la región

**Solución**:
1. Liberar EIPs no utilizadas
2. Solicitar aumento de límite
3. Usar NAT instance en su lugar

### Error: "Security group not found"
```hcl
# Problema: Orden de creación incorrecto
# El security group debe existir antes de crear instancias que lo usen

# ✅ Bien: Dependencias explícitas
resource "aws_instance" "app" {
  vpc_security_group_ids = [module.security.app_sg_id]
  depends_on = [module.security]
}
```

### Error: "Instance does not have the proper volume type"
```bash
# Verificar configuración EBS
aws ec2 describe-instances --instance-id i-12345678 \
  --query 'Reservations[0].Instances[0].BlockDeviceMappings'
```

**Solución**:
```hcl
resource "aws_instance" "bastion" {
  # ... otros configs

  ebs_block_device {
    device_name = "/dev/xvda"
    volume_type = "gp3"  # gp2/gp3/io1/io2
    volume_size = 20
    encrypted   = true
  }
}
```

### Terraform State Drift
```bash
# Detectar cambios fuera de Terraform
terraform plan

# Si hay drift, refresh estado
terraform refresh

# Ver diferencias detalladas
terraform show -json | jq '.planned_values.root_module'
```

### Error: "Circular dependency"
```hcl
# Problema común:
# SG permite tráfico desde instancia
# Instancia requiere SG

# ✅ Solución: Security group solo requiere VPC ID
resource "aws_security_group" "app" {
  vpc_id = var.vpc_id  # No depende de instancias
}

resource "aws_instance" "app" {
  vpc_security_group_ids = [aws_security_group.app.id]
  # No circular dependency
}
```

## Módulos Futuros

### RDS Module (Planificado)
```hcl
# futura implementación
module "rds" {
  source = "./modules/rds"
  # config aquí
}
```

### ECS Module (Planificado)
```hcl
# futura implementación
module "ecs" {
  source = "./modules/ecs"
  # config aquí
}
```

### ALB Module (Planificado)
```hcl
# futura implementación
module "alb" {
  source = "./modules/alb"
  # config aquí
}
```

## Mejores Prácticas

### ✅ Hacer
```hcl
# 1. Usar variables con defaults sensatos
variable "instance_type" {
  type    = string
  default = "t3.micro"
}

# 2. Taggear todos los recursos
tags = merge(
  { Project = var.project_name, Environment = var.environment },
  var.tags
)

# 3. Usar modules para reusabilidad
module "security" {
  source = "./modules/security"
  vpc_id = module.network.vpc_id
}

# 4. Outputs para cross-module communication
output "vpc_id" {
  value = aws_vpc.this.id
  description = "ID of the VPC"
}

# 5. Remote state para equipos
terraform {
  backend "s3" {
    bucket = "company-terraform-state"
    key    = "prod/terraform.tfstate"
  }
}

# 6. Version constraints
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

# 7. Validar con tfvars
# terraform.tfvars para dev
# terraform-prod.tfvars para prod
```

### ❌ Evitar
```hcl
# 1. Hardcode valores
resource "aws_instance" "bad" {
  instance_type = "t3.micro"  # ❌ Usar variable
}

# 2. No usar outputs
# ❌ Módulos sin outputs impiden composición

# 3. No tagged resources
resource "aws_vpc" "untagged" {
  cidr_block = "10.0.0.0/16"
  # ❌ Sin tags
}

# 4. Local state en producción
# ❌ terraform { } sin backend

# 5. Wildcard en version constraints
aws = {
  version = "*"  # ❌ Puede romper en deploys
}

# 6. No validation
variable "project_name" {
  type = string
  # ❌ Sin validación
}
# Mejor:
variable "project_name" {
  type        = string
  description = "Project name (lowercase, hyphens only)"
  validation {
    condition     = can(regex("^[a-z-]+$", var.project_name))
    error_message = "Project name must contain only lowercase letters and hyphens."
  }
}
```

## Referencias

### Archivos Relacionados
- `infra/terraform/main.tf` - Configuración principal
- `infra/terraform/provider.tf` - Provider AWS
- `infra/terraform/variables.tf` - Variables globales
- `infra/terraform/outputs.tf` - Outputs
- `infra/terraform/modules/network/` - Módulo de red
- `infra/terraform/modules/security/` - Módulo de seguridad
- `infra/terraform/modules/bastion/` - Módulo bastion
- `.github/workflows/terraform-ci.yml` - CI/CD para Terraform

### Documentación Externa
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [AWS Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

### AWS Services
- [Amazon VPC](https://aws.amazon.com/vpc/)
- [AWS NAT Gateway](https://aws.amazon.com/vpc/details/)
- [Amazon EC2](https://aws.amazon.com/ec2/)
- [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)

## Ver También
- [Docker Compose](../04-DEVOPS/docker-compose.md)
- [CI/CD Workflows](../04-DEVOPS/ci-cd-workflows.md)
- [Seguridad - Hardening](../06-SEGURIDAD/hardening.md)
