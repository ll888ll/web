#!/usr/bin/env python3
"""Cliente de referencia para publicar telemetría hacia Croody Gateway."""
from __future__ import annotations

import argparse
import json
import random
import time
from datetime import datetime, timezone
from typing import Dict, Any

import requests


def fake_payload(robot_id: str) -> Dict[str, Any]:
    lat = 19.4326 + random.uniform(-0.01, 0.01)
    lng = -99.1332 + random.uniform(-0.01, 0.01)
    return {
        "robot_id": robot_id,
        "ts": datetime.now(timezone.utc).isoformat(),
        "position": {"lat": lat, "lng": lng},
        "environment": "field",
        "status": random.choice(["navigating", "idle", "alert"]),
        "data": {
            "TEMP": round(random.uniform(19.0, 27.0), 2),
            "HUM": round(random.uniform(35.0, 55.0), 1),
            "AQI": random.randint(5, 40),
            "PRESS": round(random.uniform(990, 1015), 1),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Publica telemetría al endpoint expuesto en AWS/localhost")
    parser.add_argument('--url', default='https://example.com/api/telemetry/ingest', help='URL completa del endpoint')
    parser.add_argument('--token', default=None, help='Token X-API-Key si está configurado')
    parser.add_argument('--robot', default='robot-alpha', help='Identificador del robot')
    parser.add_argument('--interval', type=float, default=5.0, help='Segundos entre envíos')
    args = parser.parse_args()

    headers = {'Content-Type': 'application/json'}
    if args.token:
        headers['X-API-Key'] = args.token

    print(f"Publicando telemetría hacia {args.url} (Ctrl+C para salir)")
    try:
        while True:
            payload = fake_payload(args.robot)
            res = requests.post(args.url, headers=headers, data=json.dumps(payload), timeout=10)
            if res.status_code >= 300:
                print('Error', res.status_code, res.text)
            else:
                body = res.json()
                print(f"#{body['id']} -> {body['robot_id']} @ {body['ts']}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print('\nDetenido por el usuario')


if __name__ == '__main__':
    main()
