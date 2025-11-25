#!/usr/bin/env python3
"""Cliente de referencia para publicar telemetría hacia Croody Gateway (Dashboard Mission Control)."""
from __future__ import annotations

import argparse
import json
import random
import time
from typing import Dict, Any

import requests


def fake_payload(x_base: float = 50.0, y_base: float = 50.0) -> Dict[str, Any]:
    # Simulate movement within 0-100 grid
    x = max(0, min(100, x_base + random.uniform(-5, 5)))
    y = max(0, min(100, y_base + random.uniform(-5, 5)))
    
    return {
        "x": round(x, 2),
        "y": round(y, 2),
        "atmosphere": {
            "temperature": round(random.uniform(19.0, 27.0), 2),
            "humidity": round(random.uniform(35.0, 55.0), 1),
            "pressure": round(random.uniform(990, 1015), 1),
            "status": random.choice(["NOMINAL", "OPTIMAL", "WARNING"])
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Publica telemetría al endpoint del Dashboard")
    parser.add_argument('--url', default='http://localhost:8000/dashboard/api/robot-position/', help='URL del endpoint')
    parser.add_argument('--interval', type=float, default=1.0, help='Segundos entre envíos')
    args = parser.parse_args()

    headers = {'Content-Type': 'application/json'}

    print(f"Publicando telemetría a {args.url} (Ctrl+C para salir)")
    
    # Current pos
    curr_x, curr_y = 50.0, 50.0

    try:
        while True:
            payload = fake_payload(curr_x, curr_y)
            # Drift
            curr_x = payload['x']
            curr_y = payload['y']
            
            try:
                res = requests.post(args.url, headers=headers, json=payload, timeout=5)
                if res.status_code in [200, 201]:
                    print(f"TX OK: X={payload['x']} Y={payload['y']} Temp={payload['atmosphere']['temperature']}")
                else:
                    print(f"Error {res.status_code}: {res.text}")
            except requests.exceptions.RequestException as e:
                print(f"Connection Error: {e}")

            time.sleep(args.interval)
    except KeyboardInterrupt:
        print('\nDetenido por el usuario')


if __name__ == '__main__':
    main()
