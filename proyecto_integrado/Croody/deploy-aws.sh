#!/bin/bash
# ========================================
# AWS DEPLOYMENT SCRIPT - Croody
# ========================================
# Automatiza el deployment en AWS ECS
# Requiere: AWS CLI, jq instalado y configurado
# Uso: ./deploy-aws.sh [environment]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
ENVIRONMENT=${1:-production}
AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPOSITORY="croody-app"
ECS_CLUSTER="croody-cluster"
ECS_SERVICE="croody-service"
TASK_DEFINITION="croody-task"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🚀 Croody AWS Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Environment: ${GREEN}$ENVIRONMENT${NC}"
echo -e "Region: ${GREEN}$AWS_REGION${NC}"
echo ""

# Verificar que AWS CLI esté instalado
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI no está instalado${NC}"
    exit 1
fi

# Verificar que jq esté instalado
if ! command -v jq &> /dev/null; then
    echo -e "${RED}❌ jq no está instalado${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 1. Verificando configuración AWS...${NC}"
aws sts get-caller-identity > /dev/null 2>&1 || {
    echo -e "${RED}❌ No se pudo autenticar con AWS. Ejecuta 'aws configure'${NC}"
    exit 1
}
echo -e "${GREEN}✅ Autenticación AWS OK${NC}"

echo ""
echo -e "${YELLOW}📋 2. Creando repositorio ECR si no existe...${NC}"
aws ecr describe-repositories --repository-names $ECR_REPOSITORY --region $AWS_REGION > /dev/null 2>&1 || {
    echo "   Creando repositorio ECR..."
    aws ecr create-repository \
        --repository-name $ECR_REPOSITORY \
        --region $AWS_REGION \
        --image-scanning-configuration scanOnPush=true \
        --encryption-configuration encryptionType=AES256 > /dev/null
    echo -e "${GREEN}✅ Repositorio ECR creado${NC}"
}

# Obtener URL del registry
ECR_REGISTRY=$(aws ecr describe-repositories --repository-names $ECR_REPOSITORY --region $AWS_REGION --query 'repositories[0].repositoryUri' --output text)
IMAGE_TAG=$(date +%Y%m%d-%H%M%S)
IMAGE_URI="$ECR_REGISTRY:$IMAGE_TAG"

echo ""
echo -e "${YELLOW}📋 3. Construyendo imagen Docker...${NC}"
docker build -t $ECR_URI .
echo -e "${GREEN}✅ Imagen construida: $IMAGE_URI${NC}"

echo ""
echo -e "${YELLOW}📋 4. Subiendo imagen a ECR...${NC}"
# Obtener token de autenticación
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Taggear y push
docker tag $ECR_REPOSITORY:latest $IMAGE_URI
docker push $IMAGE_URI
echo -e "${GREEN}✅ Imagen subida a ECR${NC}"

echo ""
echo -e "${YELLOW}📋 5. Registrando task definition...${NC}"
# Reemplazar placeholder en task definition
sed "s|REPLACE_WITH_ECR_IMAGE_URI|$IMAGE_URI|g" ecs-task-definition.json | \
sed "s|REGION|$AWS_REGION|g" > ecs-task-definition-temp.json

aws ecs register-task-definition \
    --cli-input-json file://ecs-task-definition-temp.json \
    --query 'taskDefinition.taskDefinitionArn' --output text

TASK_DEFINITION_ARN=$(aws ecs describe-task-definition \
    --task-definition $TASK_DEFINITION \
    --region $AWS_REGION \
    --query 'taskDefinition.taskDefinitionArn' --output text)

echo -e "${GREEN}✅ Task definition registrado: $TASK_DEFINITION_ARN${NC}"

echo ""
echo -e "${YELLOW}📋 6. Actualizando servicio ECS...${NC}"
aws ecs update-service \
    --cluster $ECS_CLUSTER \
    --service $ECS_SERVICE \
    --task-definition $TASK_DEFINITION_ARN \
    --desired-count 2 \
    --region $AWS_REGION > /dev/null

echo -e "${GREEN}✅ Servicio actualizado${NC}"

echo ""
echo -e "${YELLOW}📋 7. Esperando que el deployment esté estable...${NC}"
aws ecs wait services-stable \
    --cluster $ECS_CLUSTER \
    --services $ECS_SERVICE \
    --region $AWS_REGION

echo -e "${GREEN}✅ Deployment completado${NC}"

echo ""
echo -e "${YELLOW}📋 8. Ejecutando health check...${NC}"
sleep 30
for i in {1..10}; do
    response=$(curl -s -o /dev/null -w "%{http_code}" https://croody.app/health/ || echo "000")
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✅ Health check passed${NC}"
        break
    fi
    echo "   ⏳ Esperando... ($i/10)"
    sleep 10
done

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}🎉 Deployment exitoso!${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "URL: ${GREEN}https://croody.app${NC}"
echo -e "Imagen: ${GREEN}$IMAGE_URI${NC}"
echo -e "Task Definition: ${GREEN}$TASK_DEFINITION_ARN${NC}"
echo ""

# Limpiar archivos temporales
rm -f ecs-task-definition-temp.json

echo -e "${YELLOW}📊 Logs disponibles en CloudWatch${NC}"
echo -e "Cluster: ${GREEN}$ECS_CLUSTER${NC}"
echo -e "Service: ${GREEN}$ECS_SERVICE${NC}"
echo ""
