#!/usr/bin/env python3
"""
Genera archivos AUDIT_<carpeta>.txt en la raíz, excluyendo 'Croody'.
El análisis se basa en heurísticas sobre el contenido: lenguajes, frameworks, endpoints, Dockerfiles, etc.
"""
from __future__ import annotations

import os
import re
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent


EXT_LANG = {
    ".py": "Python",
    ".c": "C",
    ".h": "C",
    ".sh": "Shell",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".md": "Markdown",
    ".html": "HTML",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    "Dockerfile": "Dockerfile",
}


FRAMEWORK_PATTERNS = {
    "Flask": [r"from\s+flask\s+import", r"Flask\("],
    "Django": [r"django\.", r"manage\.py"],
    "FastAPI": [r"from\s+fastapi\s+import", r"FastAPI\("],
    "Sockets": [r"socket\.", r"#include <sys/socket.h>", r"pthread_"],
    "ML/Sklearn": [r"sklearn\.", r"from\s+sklearn\s+import"],
    "Pandas": [r"import\s+pandas"],
    "CatBoost": [r"catboost"],
    "LightGBM": [r"lightgbm"],
    "Nginx": [r"server\s*\{"],
}


def detect_languages(files: List[Path]) -> Counter:
    c: Counter = Counter()
    for f in files:
        name = f.name
        ext = f.suffix
        if name == "Dockerfile":
            c["Dockerfile"] += 1
        elif ext in EXT_LANG:
            c[EXT_LANG[ext]] += 1
    return c


def read_text_safe(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def scan_frameworks(files: List[Path]) -> List[str]:
    found: List[str] = []
    for fw, patterns in FRAMEWORK_PATTERNS.items():
        for f in files:
            if f.is_dir():
                continue
            txt = read_text_safe(f)
            if any(re.search(pat, txt) for pat in patterns):
                found.append(fw)
                break
    return sorted(set(found))


def count_endpoints(files: List[Path]) -> Dict[str, int]:
    metrics = defaultdict(int)
    route_patterns = [r"@app\.route\(", r"@app\.get\(", r"@app\.post\(", r"@app\.delete\(", r"@router\."]
    for f in files:
        if f.suffix != ".py":
            continue
        txt = read_text_safe(f)
        for pat in route_patterns:
            metrics["routes"] += len(re.findall(pat, txt))
    return metrics


def has_security_hints(files: List[Path]) -> List[str]:
    hints = []
    for f in files:
        txt = read_text_safe(f)
        if "CORS" in txt or "flask_cors" in txt or "fastapi.middleware.cors" in txt:
            hints.append("CORS")
        if "ssl" in txt or "HTTPS" in txt or "gunicorn" in txt or "USER appuser" in txt:
            hints.append("prod-hardening")
        if "SECRET_KEY" in txt or "DATABASE_URL" in txt:
            hints.append("env-config")
    return sorted(set(hints))


def analyze_folder(folder: Path) -> str:
    files = [p for p in folder.rglob("*") if p.is_file() and not any(x in p.parts for x in [".git", ".venv", "__pycache__"])]
    langs = detect_languages(files)
    frameworks = scan_frameworks(files)
    endpoints = count_endpoints(files)
    security = has_security_hints(files)
    has_docker = any(f.name == "Dockerfile" or f.suffix in {".yml", ".yaml"} and "compose" in f.name for f in files)

    # Heurísticas de funcionalidades
    feats = []
    if "Flask" in frameworks or "FastAPI" in frameworks:
        feats.append("API REST")
    if "Sockets" in frameworks:
        feats.append("Servidor/cliente de sockets")
    if any(x in frameworks for x in ["ML/Sklearn", "Pandas", "CatBoost", "LightGBM"]):
        feats.append("Pipeline de Machine Learning")
    if any(f.suffix == ".html" for f in files):
        feats.append("Frontend estático")
    if has_docker:
        feats.append("Contenerización/Compose")

    # Debilidades rápidas
    weaknesses = []
    if endpoints.get("routes", 0) > 0 and "CORS" not in security:
        weaknesses.append("Falta de CORS/config de origenes en APIs")
    if any(f.name == "requirements.txt" for f in files) and not any("gunicorn" in read_text_safe(f) for f in files if f.name == "requirements.txt"):
        weaknesses.append("Falta WSGI/ASGI server para prod")

    # Recomendaciones
    rec_sec = ["Headers de seguridad en gateway/proxy", "Gestión de secretos por entorno", "Autenticación/autorización en endpoints"]
    rec_perf = ["Compresión y cache estáticos", "Workers/threads ajustados", "Índices si hay DB"]
    rec_scal = ["API versioning y OpenAPI", "Orquestación (K8s) y observabilidad", "Persistencia y particionado para datos"]

    # Metodología
    methodology = (
        "Heurístico estático: conteo de lenguajes, detección de frameworks y rutas, búsqueda de pistas de seguridad y contenerización; "
        "se leen requirements, Dockerfiles y fuentes para inferir funcionalidades y riesgos básicos."
    )

    out = []
    out.append(f"Auditoría técnica — {folder.name}")
    out.append("")
    out.append("Funcionalidades técnicas")
    out.append(f"- {', '.join(feats) if feats else 'Exploración de código y assets'}")
    out.append("")
    out.append("Objetivo funcional")
    out.append("- Derivado de estructura y dependencias: " + ", ".join(frameworks) if frameworks else "- No se detectan frameworks mayores")
    out.append("")
    out.append("Logros técnicos")
    out.append(f"- Lenguajes: {', '.join(f'{k}({v})' for k,v in langs.items()) or 'n/d'}")
    out.append(f"- Rutas/Endpoints detectados: {endpoints.get('routes', 0)}")
    out.append(f"- Seguridad detectada: {', '.join(security) or 'n/d'}")
    out.append("")
    out.append("Debilidades encontradas")
    out.extend([f"- {w}" for w in weaknesses] or ["- n/d"])
    out.append("")
    out.append("Mejoras sugeridas")
    out.append("Seguridad")
    out.extend([f"- {r}" for r in rec_sec])
    out.append("Rendimiento")
    out.extend([f"- {r}" for r in rec_perf])
    out.append("Escalabilidad")
    out.extend([f"- {r}" for r in rec_scal])
    out.append("")
    out.append("Metodología de análisis")
    out.append(f"- {methodology}")

    return "\n".join(out) + "\n"


def main():
    for entry in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        if entry.name in {"Croody", ".git", ".venv", "proyecto_integrado"}:
            continue
        report = analyze_folder(entry)
        out_path = ROOT / f"AUDIT_{entry.name}.txt"
        out_path.write_text(report, encoding="utf-8")
        print(f"Escrito {out_path}")


if __name__ == "__main__":
    main()

