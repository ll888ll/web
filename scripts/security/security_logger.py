#!/usr/bin/env python3
"""Registro centralizado de eventos de seguridad para Croody."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "proyecto_integrado" / "Croody" / "security" / "logs" / "eventos_seguridad.txt"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log_event(event_type: str, ip: str, proto: str, action: str, detail: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    line = f"[{timestamp}] | {event_type} | ip={ip} | protocolo={proto.upper()} | accion={action} | detalle={detail}\n"
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(line)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Registrar eventos de seguridad en español")
    parser.add_argument("tipo", help="Tipo de ataque o evento detectado")
    parser.add_argument("ip", help="Dirección IP origen")
    parser.add_argument("protocolo", choices=["tcp", "udp", "icmp", "otro"], help="Protocolo asociado")
    parser.add_argument("accion", help="Acción tomada (bloqueado, mitigado, monitoreo, etc.)")
    parser.add_argument("detalle", help="Descripción humana del evento")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    log_event(args.tipo, args.ip, args.protocolo, args.accion, args.detalle)
    print(f"Evento registrado en {LOG_PATH}")


if __name__ == "__main__":
    main()
