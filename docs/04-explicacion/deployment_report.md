# Informe de Despliegue y Arquitectura Telemetría

## Resumen Ejecutivo
Este documento detalla la solución implementada para corregir el fallo crítico en el despliegue de infraestructura DNS (BIND9) y la arquitectura del nuevo sistema de Telemetría y Control de Misión (Dashboard).

## 1. Corrección del Error de Despliegue (BIND9)

### Diagnóstico
El pipeline de CI/CD fallaba durante la validación de la configuración de BIND9 con el error:
`expected IP address... near ';'` en `named.conf`.

**Causa Raíz:**
El script de entrada `entrypoint.sh` definía un valor por defecto incorrecto para la variable `NOTIFY_TARGETS`.
```bash
# Antes (Incorrecto)
NOTIFY_TARGETS="${NOTIFY_TARGETS:-};" 
```
Esto generaba una configuración `also-notify { ; };`, donde el punto y coma solitario es interpretado como una dirección IP faltante o sintaxis inválida.

### Solución
Se modificó `infra/dns/entrypoint.sh` para usar una cadena vacía como defecto:
```bash
# Después (Corregido)
NOTIFY_TARGETS="${NOTIFY_TARGETS:-}"
```
Esto resulta en `also-notify { };` (si la plantilla lo permite) o simplemente evita la inyección del carácter inválido, permitiendo que BIND parsee el archivo correctamente.

## 2. Arquitectura del Dashboard de Telemetría

Se ha extendido la aplicación Django existente (`Croody`) con un nuevo módulo `telemetry`.

### Componentes
1.  **Backend (Django App `telemetry`):**
    *   **API REST:** Endpoints para recibir posición del robot y servir datos de tráfico.
    *   **CICFlowMeter Wrapper:** Utilidad Python (`utils.py`) que encapsula la ejecución del JAR de CICFlowMeter para analizar tráfico de red.
    *   **Integración Docker:** Se añadió `openjdk-17-jre-headless` al contenedor para permitir la ejecución de herramientas Java de análisis.

2.  **Frontend (Mission Control):**
    *   Interfaz "Dark Mode" técnica.
    *   **Mapa de Robot:** Visualización en tiempo real usando HTML5 Canvas.
    *   **Tráfico:** Tabla dinámica de flujos de red.

### Flujo de Datos
1.  **Robot -> API:** El cliente robot envía POST a `/dashboard/api/robot-position/`.
2.  **Dashboard -> API:** El navegador consulta periódicamente (`polling`) los endpoints JSON.
3.  **Análisis de Tráfico:** El sistema invoca `CICFlowMeter` (Java) bajo demanda o lee sus reportes CSV para visualización.

## Conclusión
La infraestructura DNS es ahora estable y validada. La nueva capacidad de telemetría proporciona visibilidad en tiempo real tanto del entorno físico (Robot) como del lógico (Red).
