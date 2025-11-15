from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

import psycopg2  # type: ignore
from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


DB_PATH = os.getenv("TG_DB_PATH", "/tmp/telemetry.db")
DB_URL = os.getenv("TG_DB_URL")


class Position(BaseModel):
    lat: float
    lng: float
    alt: Optional[float] = Field(None, description="Altitud en metros")


class TelemetryIn(BaseModel):
    robot_id: str = Field(..., min_length=3, max_length=64, description="Identificador único del robot")
    ts: Optional[datetime] = Field(None, description="Timestamp ISO8601; usa now si no viene")
    data: Dict[str, Any] = Field(..., description="Diccionario de métricas, p.ej. {\"TEMP\": 23.5}")
    position: Optional[Position] = Field(
        default=None,
        description="Posición geográfica enviada por el robot",
    )
    environment: Optional[str] = Field(
        default=None,
        description="Modo/entorno operativo (indoor, outdoor, test-lab, etc.)",
    )
    status: Optional[str] = Field(default=None, description="Mensaje corto de estado actual")


class TelemetryOut(BaseModel):
    id: int
    ts: datetime
    data: Dict[str, Any]
    robot_id: str
    position: Optional[Position]
    environment: Optional[str]
    status: Optional[str]


class RobotTrail(BaseModel):
    robot_id: str
    last: TelemetryOut
    trail: List[TelemetryOut]


class LiveResponse(BaseModel):
    robots: List[RobotTrail]
    total_points: int
    updated_at: datetime


TelemetryIn.model_rebuild()
TelemetryOut.model_rebuild()
RobotTrail.model_rebuild()
Position.model_rebuild()
TelemetryIn.model_rebuild()
TelemetryOut.model_rebuild()
RobotTrail.model_rebuild()
LiveResponse.model_rebuild()


app = FastAPI(title="Telemetry Gateway", version="0.2.0")

# CORS configurable; por defecto permite cualquier origen (gateway controla TLS)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
origins = [o.strip() for o in ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def startup() -> None:
    init_db()


def init_db() -> None:
    columns = {
        "robot_id": "TEXT",
        "position_lat": "DOUBLE PRECISION" if DB_URL else "REAL",
        "position_lng": "DOUBLE PRECISION" if DB_URL else "REAL",
        "position_alt": "DOUBLE PRECISION" if DB_URL else "REAL",
        "environment": "TEXT",
        "status": "TEXT",
    }

    if DB_URL:
        conn = psycopg2.connect(DB_URL)
        try:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS telemetry (
                    id SERIAL PRIMARY KEY,
                    ts TIMESTAMP NOT NULL,
                    data TEXT NOT NULL,
                    robot_id TEXT NOT NULL,
                    position_lat DOUBLE PRECISION,
                    position_lng DOUBLE PRECISION,
                    position_alt DOUBLE PRECISION,
                    environment TEXT,
                    status TEXT
                )
                """
            )
            ensure_columns_postgres(cur, columns)
            conn.commit()
        finally:
            cur.close()
            conn.close()
    else:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with sqlite3.connect(DB_PATH) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT NOT NULL,
                    data TEXT NOT NULL,
                    robot_id TEXT NOT NULL,
                    position_lat REAL,
                    position_lng REAL,
                    position_alt REAL,
                    environment TEXT,
                    status TEXT
                )
                """
            )
            ensure_columns_sqlite(con, columns)
            con.commit()


def ensure_columns_postgres(cur: Any, required: Dict[str, str]) -> None:
    cur.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name='telemetry'"
    )
    existing = {row[0] for row in cur.fetchall()}
    for name, ddl in required.items():
        if name not in existing:
            cur.execute(f"ALTER TABLE telemetry ADD COLUMN {name} {ddl}")


def ensure_columns_sqlite(con: sqlite3.Connection, required: Dict[str, str]) -> None:
    cur = con.cursor()
    cur.execute("PRAGMA table_info(telemetry)")
    existing = {row[1] for row in cur.fetchall()}
    for name, ddl in required.items():
        if name not in existing:
            cur.execute(f"ALTER TABLE telemetry ADD COLUMN {name} {ddl}")
    cur.close()


@app.get("/healthz")
def healthz() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/telemetry/ingest", response_model=TelemetryOut)
def ingest(payload: TelemetryIn, x_api_key: Optional[str] = Header(default=None, convert_underscores=True)) -> TelemetryOut:
    required = os.getenv("TG_INGEST_TOKEN")
    if required and (x_api_key or "") != required:
        raise HTTPException(status_code=401, detail="API key inválida o ausente")

    ts = (payload.ts or datetime.now(timezone.utc)).isoformat()
    robot_id = (payload.robot_id or payload.data.get("robot_id") or "robot-unknown").strip()
    if not robot_id:
        raise HTTPException(status_code=422, detail="robot_id requerido")

    position = payload.position or build_position_from_data(payload.data)

    try:
        data_json = json.dumps(payload.data, ensure_ascii=False)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=400, detail=f"Datos no serializables: {exc}")

    coords = (
        position.lat if position else None,
        position.lng if position else None,
        position.alt if position else None,
    )

    if DB_URL:
        conn = psycopg2.connect(DB_URL)
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO telemetry(ts, data, robot_id, position_lat, position_lng, position_alt, environment, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, ts, data, robot_id, position_lat, position_lng, position_alt, environment, status
                """,
                (ts, data_json, robot_id, coords[0], coords[1], coords[2], payload.environment, payload.status),
            )
            row = cur.fetchone()
            conn.commit()
        finally:
            cur.close()
            conn.close()
    else:
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute(
                """
                INSERT INTO telemetry(ts, data, robot_id, position_lat, position_lng, position_alt, environment, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (ts, data_json, robot_id, coords[0], coords[1], coords[2], payload.environment, payload.status),
            )
            rowid = cur.lastrowid
            cur.execute(
                "SELECT id, ts, data, robot_id, position_lat, position_lng, position_alt, environment, status FROM telemetry WHERE id = ?",
                (rowid,),
            )
            row = cur.fetchone()

    return serialize_row(row)


@app.get("/api/telemetry/last", response_model=TelemetryOut)
def last(robot_id: Optional[str] = Query(default=None, description="Filtra por robot")) -> TelemetryOut:
    row = fetch_one(robot_id)
    if not row:
        raise HTTPException(status_code=404, detail="Sin datos")
    return serialize_row(row)


@app.get("/api/telemetry/query", response_model=List[TelemetryOut])
def query(limit: int = 100, robot_id: Optional[str] = Query(default=None)) -> List[TelemetryOut]:
    limit = max(1, min(limit, 1000))
    rows = fetch_many(limit=limit, robot_id=robot_id)
    return [serialize_row(r) for r in rows]


@app.get("/api/telemetry/live", response_model=LiveResponse)
def live(limit_per_robot: int = Query(10, ge=1, le=100)) -> LiveResponse:
    rows = fetch_many(limit=limit_per_robot * 10)
    grouped: Dict[str, List[Sequence[Any]]] = {}
    for row in rows:
        robot = row[3] or "robot-unknown"
        grouped.setdefault(robot, []).append(row)

    robots: List[RobotTrail] = []
    total_points = 0
    for robot_id, robot_rows in grouped.items():
        robot_rows_sorted = sorted(robot_rows, key=lambda r: r[1] or r[0], reverse=True)
        trimmed = robot_rows_sorted[:limit_per_robot]
        total_points += len(trimmed)
        serialized = [serialize_row(r) for r in trimmed]
        robots.append(
            RobotTrail(robot_id=robot_id, last=serialized[0], trail=list(reversed(serialized)))
        )

    robots.sort(key=lambda r: r.last.ts, reverse=True)
    return LiveResponse(
        robots=robots,
        total_points=total_points,
        updated_at=datetime.now(timezone.utc),
    )


def fetch_one(robot_id: Optional[str]) -> Optional[Sequence[Any]]:
    if DB_URL:
        conn = psycopg2.connect(DB_URL)
        try:
            cur = conn.cursor()
            if robot_id:
                cur.execute(
                    "SELECT id, ts, data, robot_id, position_lat, position_lng, position_alt, environment, status "
                    "FROM telemetry WHERE robot_id = %s ORDER BY id DESC LIMIT 1",
                    (robot_id,),
                )
            else:
                cur.execute(
                    "SELECT id, ts, data, robot_id, position_lat, position_lng, position_alt, environment, status "
                    "FROM telemetry ORDER BY id DESC LIMIT 1"
                )
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()
    else:
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            if robot_id:
                cur.execute(
                    "SELECT id, ts, data, robot_id, position_lat, position_lng, position_alt, environment, status "
                    "FROM telemetry WHERE robot_id = ? ORDER BY id DESC LIMIT 1",
                    (robot_id,),
                )
            else:
                cur.execute(
                    "SELECT id, ts, data, robot_id, position_lat, position_lng, position_alt, environment, status "
                    "FROM telemetry ORDER BY id DESC LIMIT 1"
                )
            return cur.fetchone()


def fetch_many(limit: int, robot_id: Optional[str] = None) -> List[Sequence[Any]]:
    if DB_URL:
        conn = psycopg2.connect(DB_URL)
        try:
            cur = conn.cursor()
            if robot_id:
                cur.execute(
                    "SELECT id, ts, data, robot_id, position_lat, position_lng, position_alt, environment, status "
                    "FROM telemetry WHERE robot_id = %s ORDER BY id DESC LIMIT %s",
                    (robot_id, limit),
                )
            else:
                cur.execute(
                    "SELECT id, ts, data, robot_id, position_lat, position_lng, position_alt, environment, status "
                    "FROM telemetry ORDER BY id DESC LIMIT %s",
                    (limit,),
                )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()
    else:
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            if robot_id:
                cur.execute(
                    "SELECT id, ts, data, robot_id, position_lat, position_lng, position_alt, environment, status "
                    "FROM telemetry WHERE robot_id = ? ORDER BY id DESC LIMIT ?",
                    (robot_id, limit),
                )
            else:
                cur.execute(
                    "SELECT id, ts, data, robot_id, position_lat, position_lng, position_alt, environment, status "
                    "FROM telemetry ORDER BY id DESC LIMIT ?",
                    (limit,),
                )
            return cur.fetchall()


def build_position_from_data(data: Dict[str, Any]) -> Optional[Position]:
    lat = data.get("LAT") or data.get("lat")
    lng = data.get("LON") or data.get("lon") or data.get("lng")
    alt = data.get("ALT") or data.get("alt")
    if lat is None or lng is None:
        return None
    try:
        return Position(lat=float(lat), lng=float(lng), alt=float(alt) if alt is not None else None)
    except Exception:
        return None


def serialize_row(row: Sequence[Any]) -> TelemetryOut:
    tsval = row[1]
    dt = datetime.fromisoformat(tsval) if isinstance(tsval, str) else tsval
    payload = json.loads(row[2]) if isinstance(row[2], str) else row[2]
    position = None
    if row[4] is not None and row[5] is not None:
        position = Position(
            lat=float(row[4]),
            lng=float(row[5]),
            alt=float(row[6]) if row[6] is not None else None,
        )
    return TelemetryOut(
        id=row[0],
        ts=dt,
        data=payload,
        robot_id=row[3] or "robot-unknown",
        position=position,
        environment=row[7],
        status=row[8],
    )
