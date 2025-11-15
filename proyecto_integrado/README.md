Proyecto Integrado (aislado)

Estructura
- gateway/ (Nginx reverse proxy)
- services/
  - telemetry-gateway/ (FastAPI)
  - ids-ml/ (FastAPI)
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

Notas
- Esta carpeta es independiente del resto del repositorio. Puedes borrar el stack previo cuando valides que esto te funciona.
