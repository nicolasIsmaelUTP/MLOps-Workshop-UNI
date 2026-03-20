"""Entrenamiento del Pipeline de concreto con MLflow tracking.

Uso: python src/train.py
Flujo: carga datos → Pipeline(FE→Scaler→RF) → MLflow → export local.
"""

import json
import sys
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

# Añadir src/ al path para que los imports locales funcionen igual
# tanto ejecutando `python src/train.py` como importando el módulo.
_src = Path(__file__).resolve().parent
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from config import (  # noqa: E402
    FEATURES, FIGURES_DIR, MAX_DEPTH, MODELS_DIR,
    MODEL_RANDOM_STATE, MLFLOW_EXPERIMENT, MLFLOW_TRACKING_URI,
    N_ESTIMATORS, RANDOM_STATE, RAW_DATA_DIR, REPORTS_DIR, TARGET, TEST_SIZE,
)
from features import build_features  # noqa: E402
from plots import plot_predicted_vs_actual  # noqa: E402


def _build_pipeline() -> Pipeline:
    """Construye el Pipeline: FunctionTransformer → StandardScaler → RandomForest.

    Returns:
        Pipeline configurado con los hiperparámetros de config.py.
    """
    return Pipeline([
        ("features", FunctionTransformer(build_features)),
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(
            n_estimators=N_ESTIMATORS,
            max_depth=MAX_DEPTH,
            random_state=MODEL_RANDOM_STATE,
        )),
    ])


def main() -> None:
    """Carga datos, entrena el Pipeline y loguea el experimento en MLflow."""
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT)

    df = pd.read_csv(RAW_DATA_DIR / "concrete_data.csv")
    df.columns = df.columns.str.strip()
    X, y = df[FEATURES], df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    print(f"Train: {X_train.shape} | Test: {X_test.shape}")

    with mlflow.start_run(run_name="pipeline_rf"):
        mlflow.log_params({
            "n_estimators": N_ESTIMATORS,
            "max_depth": str(MAX_DEPTH),
            "test_size": TEST_SIZE,
            "random_state": RANDOM_STATE,
        })

        pipeline = _build_pipeline()
        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        metrics = {
            "mae": round(mean_absolute_error(y_test, y_pred), 4),
            "rmse": round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 4),
            "r2": round(r2_score(y_test, y_pred), 4),
        }
        mlflow.log_metrics(metrics)

        X_f64 = X_train.astype("float64")
        signature = mlflow.models.infer_signature(X_f64, pipeline.predict(X_train))
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            name="pipeline_rf",
            signature=signature,
            input_example=X_f64.head(5),
        )

        fig = plot_predicted_vs_actual(
            y_test, y_pred, metrics["r2"],
            save_path=FIGURES_DIR / "predicho_vs_real.png",
        )
        mlflow.log_figure(fig, artifact_file="predicho_vs_real.png")

        model_path = MODELS_DIR / "modelo_concreto.joblib"
        model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, model_path)

        metrics_path = REPORTS_DIR / "metricas.json"
        metrics_path.parent.mkdir(parents=True, exist_ok=True)
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)

        print(
            f"MAE: {metrics['mae']} | RMSE: {metrics['rmse']} | R²: {metrics['r2']}"
        )


if __name__ == "__main__":
    main()
