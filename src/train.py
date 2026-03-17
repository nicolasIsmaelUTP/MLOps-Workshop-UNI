"""Script de entrenamiento del modelo de resistencia del concreto.

Uso:
    python src/train.py
    python src/train.py --config configs/params.yaml

Flujo:
    1. Carga la configuración desde configs/params.yaml
    2. Lee el dataset crudo (data/raw/concrete_data.csv)
    3. Divide en entrenamiento y prueba
    4. Crea el Pipeline (StandardScaler + RandomForestRegressor)
    5. Entrena el modelo
    6. Evalúa métricas (MAE, RMSE, R²)
    7. Exporta el Pipeline entrenado con joblib
"""

import argparse
import json
import os
import sys

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Agregar la raíz del proyecto al path para imports locales
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.pipeline import crear_pipeline


def cargar_configuracion(config_path="configs/params.yaml"):
    """Carga la configuración desde un archivo YAML.

    Args:
        config_path: Ruta al archivo de configuración.

    Returns:
        Diccionario con los parámetros del proyecto.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def cargar_datos(data_path, features, target):
    """Carga el dataset y separa features del target.

    Args:
        data_path: Ruta al archivo CSV.
        features: Lista de nombres de columnas de entrada.
        target: Nombre de la columna objetivo.

    Returns:
        Tupla (X, y) con las features y el target como DataFrames/Series.
    """
    df = pd.read_csv(data_path)

    # Limpiar nombres de columnas (remover espacios extra)
    df.columns = df.columns.str.strip()

    X = df[features]
    y = df[target]
    return X, y


def entrenar_modelo(config):
    """Ejecuta el flujo completo de entrenamiento.

    Args:
        config: Diccionario de configuración (cargado de params.yaml).

    Returns:
        Tupla (pipeline_entrenado, metricas_dict).
    """
    # --- Cargar datos ---
    print(f"Cargando datos desde: {config['data']['raw_path']}")
    X, y = cargar_datos(
        data_path=config["data"]["raw_path"],
        features=config["features"],
        target=config["target"],
    )
    print(f"  Registros: {len(X)} | Features: {X.shape[1]}")

    # --- Dividir en train/test ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config["data"]["test_size"],
        random_state=config["data"]["random_state"],
    )
    print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

    # --- Crear y entrenar el Pipeline ---
    print("Creando Pipeline (StandardScaler + RandomForestRegressor)...")
    pipeline = crear_pipeline(
        n_estimators=config["model"]["n_estimators"],
        max_depth=config["model"]["max_depth"],
        random_state=config["model"]["random_state"],
    )
    pipeline.fit(X_train, y_train)
    print("  Entrenamiento completado.")

    # --- Evaluar ---
    y_pred = pipeline.predict(X_test)
    metricas = {
        "mae": round(mean_absolute_error(y_test, y_pred), 4),
        "rmse": round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 4),
        "r2": round(r2_score(y_test, y_pred), 4),
    }
    print(f"\nMétricas en test:")
    print(f"  MAE:  {metricas['mae']}")
    print(f"  RMSE: {metricas['rmse']}")
    print(f"  R²:   {metricas['r2']}")

    # --- Exportar modelo ---
    model_path = config["output"]["model_path"]
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipeline, model_path)
    print(f"\nModelo exportado en: {model_path}")

    # --- Exportar métricas ---
    metrics_path = config["output"]["metrics_path"]
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metricas, f, indent=2, ensure_ascii=False)
    print(f"Métricas guardadas en: {metrics_path}")

    return pipeline, metricas


def main():
    """Punto de entrada principal del script de entrenamiento."""
    parser = argparse.ArgumentParser(
        description="Entrenar modelo de resistencia del concreto"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/params.yaml",
        help="Ruta al archivo de configuración YAML",
    )
    args = parser.parse_args()

    config = cargar_configuracion(args.config)
    entrenar_modelo(config)


if __name__ == "__main__":
    main()
