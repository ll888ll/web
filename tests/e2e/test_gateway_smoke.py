import os
import time
import httpx


BASE = os.getenv("BASE_URL", "http://localhost:8080")


def wait_ready(url: str, timeout: float = 15.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = httpx.get(url, timeout=2.0)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def test_home_headers():
    assert wait_ready(BASE + "/"), "Gateway not ready"
    r = httpx.get(BASE + "/", timeout=5.0, follow_redirects=False)
    assert r.status_code in (200, 302)
    # Security headers present
    assert "x-content-type-options" in r.headers
    assert "x-frame-options" in r.headers


def test_telemetry_ingest_last_and_live():
    payload = {
        "robot_id": "robot-e2e",
        "data": {"TEMP": 20.5, "HUM": 41.2, "LAT": 19.4, "LON": -99.1},
        "position": {"lat": 19.4, "lng": -99.1},
        "status": "navigating",
    }
    r = httpx.post(BASE + "/api/telemetry/ingest", json=payload, timeout=5.0)
    assert r.status_code in (200, 201)
    rid = r.json().get("id")
    assert isinstance(rid, int)
    r2 = httpx.get(BASE + "/api/telemetry/last", params={"robot_id": "robot-e2e"}, timeout=5.0)
    assert r2.status_code == 200
    assert "data" in r2.json()
    live = httpx.get(BASE + "/api/telemetry/live", timeout=5.0)
    assert live.status_code == 200
    assert live.json().get("robots")


def test_ids_predict_fallback():
    r = httpx.post(BASE + "/api/ids/predict", json={"rows": [{"src_bytes": 10}]}, timeout=5.0)
    assert r.status_code == 200
    body = r.json()
    assert "predictions" in body
