FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
# Intento instalar requerimientos completos; si falla por dependencias opcionales,
# instala un subconjunto mínimo para desarrollo.
RUN apt-get update \
    && apt-get install -y --no-install-recommends wget openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Puerto de Django dev server
EXPOSE 8000

COPY docker-entrypoint.sh /entrypoint.sh
COPY docker-entrypoint.prod.sh /entrypoint.prod.sh
RUN chmod +x /entrypoint.sh /entrypoint.prod.sh

CMD ["/entrypoint.sh"]
