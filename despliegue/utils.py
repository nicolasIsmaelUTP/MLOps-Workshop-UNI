"""Utilidades: carga del modelo y construcción del DataFrame de entrada."""

import cloudpickle
import pandas as pd

MODEL_PATH = "model.pkl"

FEATURE_NAMES = [
    "cement", "blast_furnace_slag", "fly_ash", "water",
    "superplasticizer", "coarse_aggregate", "fine_aggregate", "age",
]


def load_model(path: str = MODEL_PATH):
    """Carga el pipeline serializado desde disco."""
    with open(path, "rb") as f:
        return cloudpickle.load(f)


def build_dataframe(input_dict: dict) -> pd.DataFrame:
    """Convierte un diccionario de entrada en un DataFrame con las columnas esperadas."""
    return pd.DataFrame([input_dict], columns=FEATURE_NAMES)
