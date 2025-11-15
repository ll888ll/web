FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# scikit-learn y joblib para un MVP de inferencia; FastAPI/Uvicorn para servir
RUN apt-get update \
    && apt-get install -y --no-install-recommends wget \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir fastapi uvicorn[standard] joblib pandas scikit-learn

COPY app /app

EXPOSE 9100

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9100"]
