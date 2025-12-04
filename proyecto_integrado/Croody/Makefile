# ========================================
# MAKEFILE - Croody Development
# ========================================

.PHONY: help install dev test lint format clean migrate createsuperuser deploy docker-build docker-run

# Colores
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

# Configuración
VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

help: ## Mostrar ayuda
	@echo "$(GREEN)Croody Development Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Instalar dependencias
	@echo "$(GREEN)Instalando dependencias...$(NC)"
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Instalación completada$(NC)"

dev: install ## Configurar entorno de desarrollo
	@echo "$(GREEN)Configurando entorno de desarrollo...$(NC)"
	$(PYTHON) manage.py migrate
	$(PYTHON) create_superuser.py
	@echo "$(GREEN)✅ Entorno listo$(NC)"

dev-server: ## Ejecutar servidor de desarrollo
	@echo "$(GREEN)🚀 Iniciando servidor de desarrollo...$(NC)"
	$(PYTHON) manage.py runserver 0.0.0.0:8000

test: ## Ejecutar tests
	@echo "$(GREEN)Ejecutando tests...$(NC)"
	$(PYTHON) -m pytest --verbose

lint: ## Ejecutar linters (flake8, isort)
	@echo "$(GREEN)Ejecutando linters...$(NC)"
	flake8 --max-line-length=88 .
	isort --profile black --check-only .
	@echo "$(GREEN)✅ Linting completado$(NC)"

format: ## Formatear código (black, isort)
	@echo "$(GREEN)Formateando código...$(NC)"
	black --line-length=88 .
	isort --profile black .
	@echo "$(GREEN)✅ Formateo completado$(NC)"

typecheck: ## Verificar tipos (mypy)
	@echo "$(GREEN)Verificando tipos...$(NC)"
	$(PYTHON) -m mypy croody/ || true
	@echo "$(GREEN)✅ Typecheck completado$(NC)"

security: ## Verificar seguridad (bandit)
	@echo "$(GREEN)Ejecutando verificación de seguridad...$(NC)"
	$(PYTHON) -m bandit -r croody/ -f json -o bandit-report.json || true
	@echo "$(GREEN)✅ Verificación de seguridad completada$(NC)"

clean: ## Limpiar archivos temporales
	@echo "$(GREEN)Limpiando archivos temporales...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

migrate: ## Ejecutar migraciones
	@echo "$(GREEN)Ejecutando migraciones...$(NC)"
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate
	@echo "$(GREEN)✅ Migraciones completadas$(NC)"

createsuperuser: ## Crear superusuario
	@echo "$(GREEN)Creando superusuario...$(NC)"
	$(PYTHON) create_superuser.py
	@echo "$(GREEN)✅ Superusuario creado$(NC)"

collectstatic: ## Recopilar archivos estáticos
	@echo "$(GREEN)Recopilando archivos estáticos...$(NC)"
	$(PYTHON) manage.py collectstatic --noinput
	@echo "$(GREEN)✅ Archivos estáticos recopilados$(NC)"

shell: ## Abrir shell Django
	@echo "$(GREEN)Abriendo shell Django...$(NC)"
	$(PYTHON) manage.py shell

db-shell: ## Abrir shell de base de datos
	@echo "$(GREEN)Abriendo shell de base de datos...$(NC)"
	$(PYTHON) manage.py dbshell

dumpdata: ## Exportar datos
	@echo "$(GREEN)Exportando datos...$(NC)"
	$(PYTHON) manage.py dumpdata > backup.json
	@echo "$(GREEN)✅ Datos exportados a backup.json$(NC)"

loaddata: ## Importar datos
	@echo "$(GREEN)Importando datos...$(NC)"
	$(PYTHON) manage.py loaddata backup.json
	@echo "$(GREEN)✅ Datos importados$(NC)"

# Docker
docker-build: ## Construir imagen Docker
	@echo "$(GREEN)Construyendo imagen Docker...$(NC)"
	docker build -t croody:latest .
	@echo "$(GREEN)✅ Imagen construida$(NC)"

docker-run: ## Ejecutar contenedor Docker
	@echo "$(GREEN)Ejecutando contenedor Docker...$(NC)"
	docker-compose up -d db web
	@echo "$(GREEN)✅ Contenedor ejecutándose$(NC)"

docker-stop: ## Detener contenedores
	@echo "$(YELLOW)Deteniendo contenedores...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Contenedores detenidos$(NC)"

docker-logs: ## Ver logs de Docker
	docker-compose logs -f web

# Deploy
deploy: ## Deploy a AWS ECS
	@echo "$(GREEN)Deploying a AWS ECS...$(NC)"
	./deploy-aws.sh production
	@echo "$(GREEN)✅ Deployment completado$(NC)"

# Pre-commit
pre-commit-install: ## Instalar hooks de pre-commit
	@echo "$(GREEN)Instalando hooks de pre-commit...$(NC)"
	$(PIP) install pre-commit
	pre-commit install
	@echo "$(GREEN)✅ Hooks instalados$(NC)"

pre-commit-run: ## Ejecutar pre-commit en todos los archivos
	@echo "$(GREEN)Ejecutando pre-commit...$(NC)"
	pre-commit run --all-files
	@echo "$(GREEN)✅ Pre-commit completado$(NC)"

# Health check
health: ## Verificar salud de la aplicación
	@echo "$(GREEN)Verificando salud...$(NC)"
	curl -f http://localhost:8000/health/ || echo "$(RED)❌ Aplicación no responde$(NC)"

# Admin
admin: ## Abrir admin en el navegador
	@echo "$(GREEN)Abriendo admin...$(NC)"
	@which xdg-open > /dev/null && xdg-open http://localhost:8000/admin/ || open http://localhost:8000/admin/

# Status
status: ## Mostrar estado del proyecto
	@echo "$(GREEN)=== Croody Status ===$(NC)"
	@echo "$(YELLOW)Python:$(NC) $$(python3 --version)"
	@echo "$(YELLOW)Django:$(NC) $$(cd croody && $(PYTHON) -c 'import django; print(django.get_version())')"
	@echo "$(YELLOW)Virtualenv:$(NC) $$(test -d $(VENV) && echo '✅ Activo' || echo '❌ Inactivo')"
	@echo "$(YELLOW)Dependencias:$(NC) $$(test -f requirements.txt && echo '✅ requirements.txt existe' || echo '❌ requirements.txt no encontrado')"
	@echo "$(YELLOW)Base de datos:$(NC) $$(test -f db.sqlite3 && echo '✅ db.sqlite3 existe' || echo '❌ db.sqlite3 no encontrado')"
	@echo ""
	@echo "$(YELLOW)Servicios:${NC}"
	@curl -s http://localhost:8000/health/ | jq -r '.status' 2>/dev/null && echo "  ✅ Web service: Running" || echo "  ❌ Web service: Not running"
