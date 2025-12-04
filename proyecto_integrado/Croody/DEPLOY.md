# Croody - Deploy Guide

## AWS Infrastructure Setup

### Required AWS Services

1. **ECS Fargate** - Container orchestration
2. **ECR** - Docker image registry
3. **RDS PostgreSQL** - Database
4. **ElastiCache Redis** - Caching and sessions
5. **Secrets Manager** - Credential storage
6. **CloudWatch** - Logging and monitoring
7. **ALB** - Load balancer with HTTPS
8. **ACM** - SSL certificate for croody.app
9. **SES** - Email service (optional)

---

## GitHub Secrets Configuration

Add these secrets in: `GitHub Repo > Settings > Secrets and variables > Actions`

### Required Secrets

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key | `wJalrXUtnFEMI...` |

### IAM Policy Required

The IAM user needs these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecs:DescribeTaskDefinition",
        "ecs:RegisterTaskDefinition",
        "ecs:UpdateService",
        "ecs:DescribeServices"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": [
        "arn:aws:iam::*:role/ecsTaskExecutionRole",
        "arn:aws:iam::*:role/ecsTaskRole"
      ]
    }
  ]
}
```

---

## AWS Secrets Manager Configuration

Create these secrets in AWS Secrets Manager:

### 1. Django Secret Key
```bash
aws secretsmanager create-secret \
  --name croody/django-secret-key \
  --secret-string "$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
```

### 2. Database Credentials
```bash
aws secretsmanager create-secret \
  --name croody/database \
  --secret-string '{
    "db_name": "croody",
    "username": "croody_admin",
    "password": "YOUR_SECURE_PASSWORD",
    "host": "croody-db.xxxxx.us-east-1.rds.amazonaws.com",
    "port": "5432"
  }'
```

### 3. Redis URL
```bash
aws secretsmanager create-secret \
  --name croody/redis-url \
  --secret-string "redis://croody-cache.xxxxx.cache.amazonaws.com:6379/1"
```

---

## RDS PostgreSQL Setup

### Create RDS Instance

```bash
aws rds create-db-instance \
  --db-instance-identifier croody-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15 \
  --master-username croody_admin \
  --master-user-password YOUR_SECURE_PASSWORD \
  --allocated-storage 20 \
  --storage-type gp3 \
  --vpc-security-group-ids sg-xxxxx \
  --db-subnet-group-name croody-db-subnet \
  --backup-retention-period 7 \
  --storage-encrypted \
  --deletion-protection
```

### Security Group Rules

```
Inbound:
  - PostgreSQL (5432) from ECS Security Group
  - PostgreSQL (5432) from your IP (for admin access)

Outbound:
  - All traffic (for updates)
```

---

## ECS Cluster Setup

### Create Cluster

```bash
aws ecs create-cluster \
  --cluster-name croody-cluster \
  --capacity-providers FARGATE FARGATE_SPOT \
  --default-capacity-provider-strategy \
    capacityProvider=FARGATE,weight=1,base=1 \
    capacityProvider=FARGATE_SPOT,weight=3
```

### Create Service

```bash
aws ecs create-service \
  --cluster croody-cluster \
  --service-name croody-service \
  --task-definition croody-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={
    subnets=[subnet-xxxxx,subnet-yyyyy],
    securityGroups=[sg-xxxxx],
    assignPublicIp=ENABLED
  }" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=croody-container,containerPort=8000"
```

---

## ECR Repository Setup

```bash
aws ecr create-repository \
  --repository-name croody-app \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=AES256
```

---

## Application Load Balancer Setup

### Create Target Group

```bash
aws elbv2 create-target-group \
  --name croody-tg \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxxxx \
  --target-type ip \
  --health-check-path /health/ \
  --health-check-interval-seconds 30 \
  --healthy-threshold-count 2
```

### Create ALB with HTTPS

```bash
aws elbv2 create-load-balancer \
  --name croody-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx \
  --scheme internet-facing \
  --type application

aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:... \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...
```

---

## Environment Variables Reference

### Production Environment

| Variable | Description | Required |
|----------|-------------|----------|
| `DJANGO_SETTINGS_MODULE` | Django settings module | Yes |
| `SECRET_KEY` | Django secret key | Yes (from Secrets Manager) |
| `DEBUG` | Debug mode (always `false`) | Yes |
| `ALLOWED_HOSTS` | Allowed hostnames | Yes |
| `DB_NAME` | Database name | Yes (from Secrets Manager) |
| `DB_USER` | Database username | Yes (from Secrets Manager) |
| `DB_PASSWORD` | Database password | Yes (from Secrets Manager) |
| `DB_HOST` | Database host | Yes (from Secrets Manager) |
| `DB_PORT` | Database port | Yes (from Secrets Manager) |
| `REDIS_URL` | Redis connection URL | Yes (from Secrets Manager) |
| `SECURE_SSL_REDIRECT` | Force HTTPS | Yes |
| `AWS_SES_REGION_NAME` | SES region for email | Optional |
| `ENABLE_CLOUDWATCH` | Enable CloudWatch logging | Optional |
| `SENTRY_DSN` | Sentry error tracking | Optional |

---

## Deployment Checklist

### Pre-Deploy

- [ ] All secrets created in AWS Secrets Manager
- [ ] RDS PostgreSQL instance running
- [ ] ElastiCache Redis cluster running
- [ ] ECR repository created
- [ ] ECS cluster and service configured
- [ ] ALB with HTTPS listener configured
- [ ] DNS pointing to ALB (croody.app)
- [ ] GitHub Secrets configured

### Post-Deploy Verification

- [ ] `/health/` returns 200
- [ ] Admin panel accessible at `/admin/`
- [ ] Database migrations applied
- [ ] Static files serving correctly
- [ ] HTTPS redirect working
- [ ] CloudWatch logs appearing
- [ ] Error tracking (Sentry) connected

---

## Troubleshooting

### Container Won't Start

```bash
# Check ECS task logs
aws logs get-log-events \
  --log-group-name /ecs/croody-app \
  --log-stream-name ecs/croody-container/TASK_ID

# Check task stopped reason
aws ecs describe-tasks \
  --cluster croody-cluster \
  --tasks TASK_ARN \
  --query 'tasks[0].stoppedReason'
```

### Database Connection Issues

```bash
# Test from ECS task
aws ecs execute-command \
  --cluster croody-cluster \
  --task TASK_ARN \
  --container croody-container \
  --interactive \
  --command "/bin/bash"

# Inside container
python manage.py dbshell
```

### Health Check Failing

1. Check if gunicorn is running
2. Verify `/health/` endpoint returns 200
3. Check security group allows ALB -> ECS traffic
4. Review application logs for errors

---

## Security Audit Checklist

### OWASP Top 10 Mitigations

- [x] **A01 Broken Access Control** - LoginRequiredMixin on all views
- [x] **A02 Cryptographic Failures** - SSL/TLS enforced, secrets in Secrets Manager
- [x] **A03 Injection** - Django ORM, parameterized queries
- [x] **A04 Insecure Design** - Secure by default settings
- [x] **A05 Security Misconfiguration** - Hardened production.py
- [x] **A06 Vulnerable Components** - Dependency scanning with Safety/Bandit
- [x] **A07 Auth Failures** - Strong password validators
- [x] **A08 Integrity Failures** - CSRF protection, signed cookies
- [x] **A09 Logging Failures** - CloudWatch, Sentry integration
- [x] **A10 SSRF** - No external URL fetching without validation

### Django Security Headers

```python
# All enabled in production.py
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SECURE_CONTENT_TYPE_NOSNIFF = True
```

---

## Cost Estimation (Monthly)

| Service | Configuration | Est. Cost |
|---------|---------------|-----------|
| ECS Fargate | 2 tasks, 0.5 vCPU, 1GB | ~$30 |
| RDS PostgreSQL | db.t3.micro, 20GB | ~$15 |
| ElastiCache Redis | cache.t3.micro | ~$12 |
| ALB | Basic usage | ~$20 |
| ECR | 5GB storage | ~$1 |
| CloudWatch | Basic logs | ~$5 |
| **Total** | | **~$83/month** |

*Note: Costs vary by region and usage patterns.*
