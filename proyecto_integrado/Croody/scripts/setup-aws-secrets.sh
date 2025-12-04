#!/bin/bash
# ========================================
# CROODY - AWS Secrets Manager Setup
# ========================================
#
# INSTRUCCIONES:
# 1. Asegúrate de tener AWS CLI instalado y configurado
# 2. Edita las variables de abajo con tus valores reales
# 3. Ejecuta: chmod +x setup-aws-secrets.sh && ./setup-aws-secrets.sh
#
# ========================================

set -e

# ========================================
# CONFIGURA ESTOS VALORES
# ========================================

AWS_REGION="us-east-1"

# Database (RDS PostgreSQL)
DB_NAME="croody"
DB_USER="croody_admin"
DB_PASSWORD="CambiaEsto_ContraseñaSegura123!"  # CAMBIA ESTO
DB_HOST="tu-rds-endpoint.xxxxx.us-east-1.rds.amazonaws.com"  # CAMBIA ESTO
DB_PORT="5432"

# Redis (ElastiCache)
REDIS_URL="redis://tu-elasticache.xxxxx.cache.amazonaws.com:6379/1"  # CAMBIA ESTO

# ========================================
# NO EDITES DEBAJO DE ESTA LÍNEA
# ========================================

echo "=== Croody AWS Secrets Setup ==="
echo "Region: $AWS_REGION"
echo ""

# 1. Django Secret Key (generado automáticamente)
echo "[1/3] Creando Django Secret Key..."
DJANGO_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")

aws secretsmanager create-secret \
    --region "$AWS_REGION" \
    --name "croody/django-secret-key" \
    --description "Django SECRET_KEY for Croody production" \
    --secret-string "$DJANGO_SECRET_KEY" \
    2>/dev/null || \
aws secretsmanager update-secret \
    --region "$AWS_REGION" \
    --secret-id "croody/django-secret-key" \
    --secret-string "$DJANGO_SECRET_KEY"

echo "   ✓ Django Secret Key creado"

# 2. Database credentials
echo "[2/3] Creando credenciales de base de datos..."

aws secretsmanager create-secret \
    --region "$AWS_REGION" \
    --name "croody/database" \
    --description "RDS PostgreSQL credentials for Croody" \
    --secret-string "{
        \"db_name\": \"$DB_NAME\",
        \"username\": \"$DB_USER\",
        \"password\": \"$DB_PASSWORD\",
        \"host\": \"$DB_HOST\",
        \"port\": \"$DB_PORT\"
    }" \
    2>/dev/null || \
aws secretsmanager update-secret \
    --region "$AWS_REGION" \
    --secret-id "croody/database" \
    --secret-string "{
        \"db_name\": \"$DB_NAME\",
        \"username\": \"$DB_USER\",
        \"password\": \"$DB_PASSWORD\",
        \"host\": \"$DB_HOST\",
        \"port\": \"$DB_PORT\"
    }"

echo "   ✓ Database credentials creados"

# 3. Redis URL
echo "[3/3] Creando Redis URL..."

aws secretsmanager create-secret \
    --region "$AWS_REGION" \
    --name "croody/redis-url" \
    --description "ElastiCache Redis URL for Croody" \
    --secret-string "$REDIS_URL" \
    2>/dev/null || \
aws secretsmanager update-secret \
    --region "$AWS_REGION" \
    --secret-id "croody/redis-url" \
    --secret-string "$REDIS_URL"

echo "   ✓ Redis URL creado"

echo ""
echo "=== COMPLETADO ==="
echo ""
echo "Secrets creados en AWS Secrets Manager:"
echo "  - croody/django-secret-key"
echo "  - croody/database"
echo "  - croody/redis-url"
echo ""
echo "Verifica con: aws secretsmanager list-secrets --region $AWS_REGION --filter Key=name,Values=croody"
