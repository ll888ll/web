# Build stage to compile the C robot server from clases
FROM gcc:13 AS builder
WORKDIR /src
COPY server.c Makefile ./
RUN make server

# Runtime stage with Python bridge + compiled server
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /src/server /app/server
COPY bridge_ingest.py entrypoint.sh /app/
RUN chmod +x /app/server /app/entrypoint.sh \
    && pip install --no-cache-dir requests
EXPOSE 9090
CMD ["/app/entrypoint.sh"]
