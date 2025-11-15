from fastapi.testclient import TestClient
import importlib.util
from pathlib import Path

_MAIN = Path(__file__).with_name("main.py")
spec = importlib.util.spec_from_file_location("ids_main", _MAIN)
mod = importlib.util.module_from_spec(spec)  # type: ignore
assert spec and spec.loader
spec.loader.exec_module(mod)  # type: ignore
app = mod.app
if hasattr(mod, "PredictRequest"):
    try:
        mod.PredictRequest.model_rebuild()
        mod.PredictResponse.model_rebuild()
    except Exception:
        pass

client = TestClient(app)


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200


def test_predict_fallback():
    r = client.post("/api/ids/predict", json={"rows": [{"src_bytes": 1}]})
    assert r.status_code == 200
    body = r.json()
    assert "predictions" in body
