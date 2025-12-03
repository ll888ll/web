# ========================================
# DOCKERFILE CROODY - Producción optimizada
# ========================================

# Etapa 1: Build dependencies
FROM python:3.11-slim as builder

# Configurar variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
        wget \
        openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Etapa 2: Runtime
FROM python:3.11-slim as runtime

# Configurar variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=croody.settings.production

# Instalar runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
        wget \
        openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN groupadd -r django && useradd -r -g django django

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/staticfiles /app/media /app/logs \
    && chown -R django:django /app

# Permisos
RUN chmod +x /app/manage.py /app/entrypoint.sh /app/entrypoint.prod.sh

# Ejecutar como usuario no-root
USER django

# Puerto de la aplicación
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Comando por defecto para producción con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "gthread", "--threads", "2", "--max-requests", "1000", "--max-requests-jitter", "100", "--timeout", "120", "--keep-alive", "5", "--access-logfile", "-", "--error-logfile", "-", "croody.wsgi:application"]
