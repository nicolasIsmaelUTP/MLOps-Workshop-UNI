"""API de predicción con FastAPI.

Expone un endpoint POST /predict que recibe la composición de una mezcla
de concreto y devuelve la resistencia predicha en MPa.

Uso local:
    uvicorn app:app --reload --host 0.0.0.0 --port 8000

Prueba con curl:
    curl -X POST http://localhost:8000/predict \
      -H "Content-Type: application/json" \
      -d '{"cement": 540, "blast_furnace_slag": 0, "fly_ash": 0,
           "water": 162, "superplasticizer": 2.5,
           "coarse_aggregate": 1040, "fine_aggregate": 676, "age": 28}'
"""

from fastapi import FastAPI

from schemas import ConcreteInput, PredictionOutput
from utils import build_dataframe, load_model

app = FastAPI(
    title="API Resistencia del Concreto",
    description="Predice la resistencia a la compresión del concreto (MPa) — Taller MLOps UNI",
    version="1.0.0",
)

pipeline = load_model()


@app.get("/")
def root():
    """Endpoint de verificación (health check)."""
    return {"status": "ok", "message": "API Resistencia del Concreto — Taller MLOps UNI"}


@app.post("/predict", response_model=PredictionOutput)
def predict(data: ConcreteInput):
    """Predice la resistencia a la compresión del concreto.

    Args:
        data: Composición de la mezcla de concreto.

    Returns:
        Predicción de la resistencia en MPa.
    """
    df = build_dataframe(data.model_dump())
    prediction = pipeline.predict(df)

    return PredictionOutput(
        concrete_compressive_strength_mpa=round(float(prediction[0]), 2),
    )
