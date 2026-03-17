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

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

# ============================================================
# Esquema de entrada (validación automática con Pydantic)
# ============================================================


class ConcreteInput(BaseModel):
    """Datos de entrada para la predicción de resistencia del concreto."""

    cement: float = Field(..., ge=0, description="Cemento (kg/m³)")
    blast_furnace_slag: float = Field(..., ge=0, description="Escoria de alto horno (kg/m³)")
    fly_ash: float = Field(..., ge=0, description="Ceniza volante (kg/m³)")
    water: float = Field(..., ge=0, description="Agua (kg/m³)")
    superplasticizer: float = Field(..., ge=0, description="Superplastificante (kg/m³)")
    coarse_aggregate: float = Field(..., ge=0, description="Agregado grueso (kg/m³)")
    fine_aggregate: float = Field(..., ge=0, description="Agregado fino (kg/m³)")
    age: int = Field(..., ge=1, description="Edad de curado (días)")


class PredictionOutput(BaseModel):
    """Respuesta de la API con la predicción."""

    concrete_compressive_strength_mpa: float
    model_version: str = "1.0"


# ============================================================
# Aplicación FastAPI
# ============================================================

app = FastAPI(
    title="API Resistencia del Concreto",
    description="Predice la resistencia a la compresión del concreto (MPa) — Taller MLOps UNI",
    version="1.0.0",
)

# Cargar modelo al iniciar la aplicación
MODEL_PATH = "modelo/modelo_concreto.joblib"
pipeline = joblib.load(MODEL_PATH)

FEATURE_NAMES = [
    "cement", "blast_furnace_slag", "fly_ash", "water",
    "superplasticizer", "coarse_aggregate", "fine_aggregate", "age",
]


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
    input_dict = data.model_dump()
    df = pd.DataFrame([input_dict], columns=FEATURE_NAMES)
    prediction = pipeline.predict(df)

    return PredictionOutput(
        concrete_compressive_strength_mpa=round(float(prediction[0]), 2),
    )
