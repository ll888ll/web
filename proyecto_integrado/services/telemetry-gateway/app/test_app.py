from pathlib import Path
import importlib.util

from fastapi.testclient import TestClient

_MAIN = Path(__file__).with_name("main.py")
spec = importlib.util.spec_from_file_location("tg_main", _MAIN)
mod = importlib.util.module_from_spec(spec)  # type: ignore
assert spec and spec.loader
spec.loader.exec_module(mod)  # type: ignore
app = mod.app

if hasattr(mod, "TelemetryIn"):
    try:
        mod.TelemetryIn.model_rebuild()
        mod.TelemetryOut.model_rebuild()
    except Exception:
        pass

if hasattr(mod, "init_db"):
    mod.init_db()

client = TestClient(app)


def sample_payload(robot: str = "robot-alpha") -> dict:
    base = {
        "robot_id": robot,
        "data": {
            "TEMP": 22.2,
            "HUM": 40.0,
            "LAT": 19.4326,
            "LON": -99.1332,
        },
        "position": {"lat": 19.4326, "lng": -99.1332},
        "environment": "lab",
        "status": "idle",
    }
    if robot != "robot-alpha":
        base["data"].update({"LAT": 40.4168, "LON": -3.7038})
        base["position"] = {"lat": 40.4168, "lng": -3.7038}
    return base


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200


def test_ingest_and_last_with_robot_filter():
    r = client.post("/api/telemetry/ingest", json=sample_payload())
    assert r.status_code in (200, 201)
    latest = client.get("/api/telemetry/last", params={"robot_id": "robot-alpha"})
    assert latest.status_code == 200
    body = latest.json()
    assert body["robot_id"] == "robot-alpha"
    assert body["position"]["lat"] == 19.4326


def test_live_endpoint_groups_by_robot():
    client.post("/api/telemetry/ingest", json=sample_payload())
    client.post("/api/telemetry/ingest", json=sample_payload("robot-beta"))
    resp = client.get("/api/telemetry/live", params={"limit_per_robot": 5})
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["robots"]
    assert any(robot["robot_id"] == "robot-alpha" for robot in payload["robots"])
