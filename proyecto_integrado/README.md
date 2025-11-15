Proyecto Integrado (aislado)

Estructura
- gateway/ (Nginx reverse proxy)
- services/
  - telemetry-gateway/ (FastAPI)
  - ids-ml/ (FastAPI)
- robots/
  - telemetry-robot/ (servidor TCP legado + bridge HTTP)
- Croody/ (Django, copia aislada)
- docker-compose.yml (este stack)

Arranque
1) Requisitos: Docker + Docker Compose
2) Desde esta carpeta:
   docker compose up --build
3) Navega:
   - http://localhost:8080/ (Croody)
   - http://localhost:8080/es/integraciones/ (panel de prueba)

## Arranque rápido

- Linux
  - `bash scripts/run_all.sh` — levanta dev, valida y registra resultados en `extras/quick_smoke_results.txt`.
  - Instalación desde cero: `bash scripts/setup_from_scratch.sh` (Ubuntu/Debian).
  - Comandos manuales: ver `extras/manual_commands_linux.txt`.

- Windows
  - `powershell -ExecutionPolicy Bypass -File scripts\run_all.ps1` — levanta dev y valida.
  - Instalación desde cero: `powershell -ExecutionPolicy Bypass -File scripts\setup_from_scratch.ps1`.
  - Comandos manuales: ver `extras\manual_commands_windows.txt`.

Endpoints
- Telemetry: POST /api/telemetry/ingest, GET /api/telemetry/last, GET /api/telemetry/query?limit=100
- IDS-ML: GET /api/ids/model, POST /api/ids/predict
- Robot demo: servidor TCP heredado (puerto 9090) accesible vía `robot-sim` + bridge automático a Telemetry Gateway.

## Robot heredado (clases)
- Carpeta: `robots/telemetry-robot/`
- Construcción: `docker compose up robot-sim`
- El container compila `server.c`, abre `9090` y ejecuta `bridge_ingest.py` que hace LOGIN USER y reenvía cada frame como JSON a `/api/telemetry/ingest`.
- Para probar manualmente: `nc localhost 9090` → `LOGIN USER -` → espera `DATA ...`.

## Modelo IDS-ML
- Script portado desde `clases/CiberTelepatia/run_ids_ml.py`: `services/ids-ml/training/train_ids_model.py`.
- Ejecuta `python services/ids-ml/training/train_ids_model.py` (requiere pandas/scikit-learn) para regenerar `services/ids-ml/models/best_model.joblib` y `model_metadata.json`.
- El front de monitor muestra Accuracy/F1 leídos de `model_metadata.json`.

## Despliegue automatizado

### GitHub Actions
- Workflow: `.github/workflows/deploy.yml` (push a `main`).
- Secretos necesarios en el repositorio:
  - `DEPLOY_HOST`: IP o dominio del servidor (ej. `18.224.180.61`).
  - `DEPLOY_USER`: usuario SSH (ej. `ec2-user`).
  - `DEPLOY_KEY`: clave privada en formato PEM (contenido completo).
  - `DEPLOY_PATH`: carpeta raíz donde vive el proyecto (ej. `/home/ec2-user`).
  - `DEPLOY_PORT` (opcional, default 22).
- Hasta que los cuatro secretos obligatorios estén definidos, el job se omite automáticamente para evitar fallos.
- El workflow empaqueta el repo (`git archive`), lo copia a `$DEPLOY_PATH`, preserva `proyecto_integrado/.env` si ya existe y ejecuta `docker compose up -d --build telemetry-gateway ids-ml robot-sim croody gateway`.
- Asegúrate de que el servidor tenga Docker + Docker Compose instalados y que `proyecto_integrado/.env` exista con los secretos reales (no se versiona).

### Script manual
- `scripts/deploy_remote.sh` reproduce la misma lógica desde tu máquina local.
- Requiere las variables `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_KEY` (ruta al PEM), `DEPLOY_PATH` y opcionalmente `DEPLOY_PORT`.
- Ejemplo:
  ```bash
  DEPLOY_HOST=18.224.180.61 \
  DEPLOY_USER=ec2-user \
  DEPLOY_KEY=~/croody.pem \
  DEPLOY_PATH=/home/ec2-user \
  ./scripts/deploy_remote.sh
  ```
- El script preserva `proyecto_integrado/.env` y relanza el stack completo.

Notas
- Esta carpeta es independiente del resto del repositorio. Puedes borrar el stack previo cuando valides que esto te funciona.
