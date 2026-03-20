"""Configuración central de paths y parámetros del proyecto.

Concentra en un solo lugar todos los valores que antes estaban
distribuidos en configs/params.yaml y otros módulos.
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJ_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
TEST_SIZE: float = 0.2
RANDOM_STATE: int = 42

# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
MODEL_TYPE: str = "RandomForestRegressor"
N_ESTIMATORS: int = 50
MAX_DEPTH: int = 15
MODEL_RANDOM_STATE: int = 42

# ---------------------------------------------------------------------------
# Features / Target
# ---------------------------------------------------------------------------
FEATURES: list[str] = [
    "cement",
    "blast_furnace_slag",
    "fly_ash",
    "water",
    "superplasticizer",
    "coarse_aggregate",
    "fine_aggregate",
    "age",
]
TARGET: str = "concrete_compressive_strength"

# ---------------------------------------------------------------------------
# MLflow / Databricks
# ---------------------------------------------------------------------------
MLFLOW_TRACKING_URI: str = "databricks"
MLFLOW_EXPERIMENT: str = "/Users/nalayo@itmeet.org/concrete-strength"
