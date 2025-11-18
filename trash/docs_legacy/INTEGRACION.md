Integración unificada (Croody + Telemetry + IDS-ML)

Servicios
- gateway (Nginx): reverse proxy en `:80`.
- croody (Django): landing/tienda en `/`.
- telemetry-gateway (FastAPI): `/api/telemetry/*` (ingesta y consulta de telemetría).
- ids-ml (FastAPI): `/api/ids/*` (inferencias).

Cómo ejecutar (desarrollo)
1. Instala Docker y Docker Compose Plugin.
2. En la raíz del repo:
   ```bash
   docker compose up --build
   ```
3. Abre `http://localhost/` para Croody.
4. Abre `http://localhost/es/integraciones/` para probar las integraciones (ingesta/consulta de telemetría y predicción IDS).

Endpoints
- Telemetry:
  - `POST /api/telemetry/ingest` { ts?: ISO8601, data: { TEMP: number, HUM: number, ... } }
  - `GET /api/telemetry/last`
  - `GET /api/telemetry/query?limit=100`
- IDS-ML:
  - `GET /api/ids/model`
  - `POST /api/ids/predict` { rows: [ { feature: value, ... } ] }

Puente opcional con servidor C (telemetría)
Si corres el servidor C de `Entrega1_Telemetria/telemetria_robot/server` y quieres inyectar sus `DATA ...` al gateway:
```bash
python3 services/telemetry-gateway/tools/telemetry_c_bridge.py \
  --host 127.0.0.1 --port 9001 \
  --ingest http://localhost/api/telemetry/ingest
```

Notas
- Las imágenes de ML pueden tardar en construir (scikit-learn).
- `Croody/Dockerfile` intenta instalar dependencias completas; si alguna opcional falla, se instala un subconjunto mínimo (Django + DRF + sslserver) para no bloquear el entorno.
- Esto es un entorno de desarrollo (HTTP). Para producción, agrega TLS, CSP estricta, almacenamiento Postgres/Timeseries y CI/CD.

