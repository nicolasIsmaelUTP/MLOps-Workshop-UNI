"""Esquemas de validación de entrada y salida de la API (Pydantic)."""

from pydantic import BaseModel, Field


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
