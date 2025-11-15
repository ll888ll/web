#!/usr/bin/env python3
"""Conecta al servidor C del robot (sockets) y reenvía lecturas al Telemetry Gateway."""
from __future__ import annotations

import json
import os
import socket
import sys
import time
from datetime import datetime, timezone
from typing import Dict

import requests

ROBOT_HOST = os.getenv("ROBOT_SIM_HOST", "127.0.0.1")
ROBOT_PORT = int(os.getenv("ROBOT_SIM_PORT", "9090"))
INGEST_URL = os.getenv("TELEMETRY_INGEST_URL", "http://telemetry-gateway:9000/api/telemetry/ingest")
ROBOT_ID = os.getenv("ROBOT_ID", "robot-clases")
TOKEN = os.getenv("TG_INGEST_TOKEN", "")
RETRY_SECONDS = int(os.getenv("ROBOT_RETRY_SECONDS", "5"))
STATUS_HIGH_TEMP = float(os.getenv("ROBOT_TEMP_ALERT", "28"))


def log(msg: str) -> None:
    sys.stdout.write(f"[robot-bridge] {msg}\n")
    sys.stdout.flush()


def connect_stream() -> tuple[socket.socket, any]:
    """Abre socket TCP contra el servidor C y devuelve (socket, archivo)."""
    while True:
        try:
            sock = socket.create_connection((ROBOT_HOST, ROBOT_PORT), timeout=10)
            log(f"Conectado a {ROBOT_HOST}:{ROBOT_PORT}")
            sock.sendall(b"LOGIN USER -\n")
            sock.settimeout(None)
            return sock, sock.makefile('r')
        except OSError as exc:
            log(f"No se pudo conectar ({exc}), reintentando en {RETRY_SECONDS}s")
            time.sleep(RETRY_SECONDS)


def parse_data_line(line: str) -> Dict[str, float] | None:
    parts = line.strip().split(' ', 2)
    if len(parts) < 3 or parts[0] != 'DATA':
        return None
    ts = datetime.fromtimestamp(float(parts[1]), tz=timezone.utc)
    metrics: Dict[str, float] = {}
    for chunk in parts[2].split(';'):
        if not chunk or '=' not in chunk:
            continue
        key, value = chunk.split('=', 1)
        try:
            metrics[key] = float(value)
        except ValueError:
            continue
    return {
        'ts': ts.isoformat(),
        'metrics': metrics,
    }


def forward(payload: Dict[str, float]) -> None:
    metrics = payload['metrics']
    status = 'alert' if metrics.get('TEMP', 0) >= STATUS_HIGH_TEMP else 'ok'
    body = {
        'robot_id': ROBOT_ID,
        'ts': payload['ts'],
        'status': status,
        'data': metrics,
    }
    headers = {'Content-Type': 'application/json'}
    if TOKEN:
        headers['x-api-key'] = TOKEN
    resp = requests.post(INGEST_URL, headers=headers, data=json.dumps(body), timeout=10)
    resp.raise_for_status()
    log(f"Ingestado {body['robot_id']} -> {metrics}")


def main() -> None:
    while True:
        sock, stream = connect_stream()
        try:
            for raw in stream:
                parsed = parse_data_line(raw)
                if parsed:
                    try:
                        forward(parsed)
                    except Exception as exc:  # pragma: no cover
                        log(f"Error al enviar telemetría: {exc}")
        except Exception as exc:
            log(f"Conexión caída ({exc}), reintentando...")
        finally:
            try:
                stream.close()
            except Exception:
                pass
            try:
                sock.close()
            except Exception:
                pass
        time.sleep(RETRY_SECONDS)


if __name__ == '__main__':
    main()
