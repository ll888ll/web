"""
Bridge simple: conecta al servidor C de telemetría (Entrega1_Telemetria)
y reenvía líneas DATA al Telemetry Gateway vía HTTP.

Uso:
  python3 telemetry_c_bridge.py --host 127.0.0.1 --port 9001 \
    --ingest http://localhost/api/telemetry/ingest --robot-id robot-alpha

Formato soportado:
  DATA <ts> TEMP=23.5;HUM=60.2;LAT=19.4;LON=-99.1;ROBOT=robot-alpha;ENV=lab
"""
from __future__ import annotations

import argparse
import re
import socket
import sys
from datetime import datetime
from typing import Dict

import requests


DATA_RE = re.compile(r"^DATA\s+(?P<ts>\d+)\s+(?P<pairs>.+)$")


def parse_data(line: str):
    m = DATA_RE.match(line.strip())
    if not m:
        return None
    ts = int(m.group("ts"))
    pairs = m.group("pairs").split(";")
    data: Dict[str, object] = {}
    robot_id = None
    environment = None
    status = None
    position: Dict[str, float] = {}

    for p in pairs:
        if not p or "=" not in p:
            continue
        k, v = p.split("=", 1)
        key_upper = k.upper()
        try:
            value: object = float(v)
        except Exception:
            value = v

        if key_upper in {"LAT", "LON", "LNG", "ALT"}:
            if key_upper in {"LON", "LNG"}:
                position["lng"] = float(value)
            elif key_upper == "LAT":
                position["lat"] = float(value)
            else:
                position["alt"] = float(value)
        elif key_upper == "ROBOT":
            robot_id = str(value)
        elif key_upper == "ENV":
            environment = str(value)
        elif key_upper == "STATUS":
            status = str(value)
        else:
            data[k] = value

    return datetime.utcfromtimestamp(ts), data, robot_id, environment, status, position


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True)
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--ingest", default="http://localhost/api/telemetry/ingest")
    ap.add_argument("--robot-id", default="robot-cli", help="Identificador por defecto si el stream no lo incluye")
    ap.add_argument("--environment", default=None, help="Sobrescribe ENV del stream")
    ap.add_argument("--api-key", default=None, help="Token opcional para cabecera X-API-Key")
    args = ap.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.host, args.port))
    print(f"Conectado a servidor C {args.host}:{args.port}")

    try:
        buf = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                line = line.decode("utf-8", errors="ignore")
                if not line.strip():
                    continue
                parsed = parse_data(line)
                if not parsed:
                    continue
                ts, data, robot_from_line, env, status, position = parsed
                body: Dict[str, object] = {
                    "ts": ts.isoformat(),
                    "data": data,
                    "robot_id": robot_from_line or args.robot_id,
                }
                if position.get("lat") is not None and position.get("lng") is not None:
                    body["position"] = position
                if args.environment or env:
                    body["environment"] = args.environment or env
                if status:
                    body["status"] = status

                headers = {"X-API-Key": args.api_key} if args.api_key else None
                r = requests.post(args.ingest, json=body, headers=headers, timeout=5)
                if r.status_code >= 300:
                    print("Error al ingerir:", r.status_code, r.text)
    finally:
        s.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
