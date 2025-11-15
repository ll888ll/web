Rúbrica — Entrega 1 (Robot de Telemetría)

Autor: Jose Alejandro Jimenez Vasquez

Autoevaluación (criterios):

- [x] Definí el protocolo (comandos, roles, formatos) de forma clara.
- [x] Implementé servidor concurrente (C, hilos y sincronización con mutex).
- [x] Manejé seguridad básica: contraseña ADMIN por `ENV`/`.env`, ignorar `SIGPIPE`, send_all robusto, rate limit.
- [x] Implementé clientes (CLI y GUI) en Python con logs y controles.
- [x] Incluí `test_client.py` para pruebas funcionales (login, ping, get_data, logout).
- [x] Documentación completa en primera persona y en español.
- [x] Script `check_env.sh` para compilar y probar automáticamente.

Evidencias:

- `server.c`: hilos, mutex, rotación de logs, snapshot de sockets.
- `client_cli.py` y `client_gui.py`: pruebas de interacción y GUI.
- `test_client.py`: flujo automatizado (USER) que validé.
- `README.md`: guía de ejecución y notas de seguridad.

Observaciones personales:

Priorizo claridad en el protocolo y seguridad básica en red, con pruebas reproducibles para defensa y evaluación.
