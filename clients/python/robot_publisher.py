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


def fake_payload(robot_id: str, base_lat: float | None = None, base_lng: float | None = None, base_alt: float | None = None, jitter: float = 0.0) -> Dict[str, Any]:
    lat = (base_lat if base_lat is not None else 19.4326) + (random.uniform(-jitter, jitter) if jitter else 0)
    lng = (base_lng if base_lng is not None else -99.1332) + (random.uniform(-jitter, jitter) if jitter else 0)
    return {
        "robot_id": robot_id,
        "ts": datetime.now(timezone.utc).isoformat(),
        "position": ({"lat": lat, "lng": lng, **({"alt": base_alt} if base_alt is not None else {})}),
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
    parser.add_argument('--lat', type=float, default=None, help='Latitud fija del robot (grados decimales)')
    parser.add_argument('--lng', type=float, default=None, help='Longitud fija del robot (grados decimales)')
    parser.add_argument('--alt', type=float, default=None, help='Altitud opcional (metros)')
    parser.add_argument('--jitter', type=float, default=0.0, help='Jitter aleatorio alrededor de lat/lng en grados (p.ej. 0.001)')
    args = parser.parse_args()

    headers = {'Content-Type': 'application/json'}
    if args.token:
        headers['X-API-Key'] = args.token

    print(f"Publicando telemetría hacia {args.url} (Ctrl+C para salir)")
    try:
        while True:
            payload = fake_payload(args.robot, base_lat=args.lat, base_lng=args.lng, base_alt=args.alt, jitter=args.jitter)
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
