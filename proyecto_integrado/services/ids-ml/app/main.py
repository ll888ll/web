from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

MODEL_PATH = os.getenv("MODEL_PATH", "/models/best_model.joblib")

app = FastAPI(title="IDS ML Inference", version="0.1.0")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
origins = [o.strip() for o in ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class PredictRequest(BaseModel):
    rows: List[Dict[str, Any]] = Field(..., description="Filas con características para inferencia")


class PredictResponse(BaseModel):
    predictions: List[Any]
    model: Dict[str, Optional[str]]


def _load_model():
    try:
        import joblib  # type: ignore
        if os.path.exists(MODEL_PATH):
            return joblib.load(MODEL_PATH)
    except Exception:
        return None
    return None


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/api/ids/model")
def model_info():
    exists = os.path.exists(MODEL_PATH)
    return {"path": MODEL_PATH, "available": exists}


@app.post("/api/ids/predict", response_model=PredictResponse)
def predict(req: PredictRequest, x_api_key: str | None = Header(default=None, convert_underscores=True)) -> PredictResponse:
    required = os.getenv("IDS_API_TOKEN")
    if required and (x_api_key or "") != required:
        raise HTTPException(status_code=401, detail="API key inválida o ausente")
    model = _load_model()
    if model is None:
        # Fallback: clasificador trivial por umbral si existe feature conocida, si no 0
        preds = []
        for row in req.rows:
            # ejemplo trivial: si 'src_bytes' > 500 predice 1, si no 0
            v = row.get("src_bytes")
            try:
                preds.append(1 if v is not None and float(v) > 500.0 else 0)
            except Exception:
                preds.append(0)
        return PredictResponse(predictions=preds, model={"path": None})

    # Inferencia con modelo real: requiere columnas alineadas al entrenamiento
    try:
        import pandas as pd  # type: ignore
        df = pd.DataFrame(req.rows)
        preds = model.predict(df)
        return PredictResponse(predictions=[int(x) for x in preds], model={"path": MODEL_PATH})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error de inferencia: {e}")
