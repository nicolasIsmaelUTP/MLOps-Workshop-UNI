"""Script de inferencia local con el modelo empaquetado.

Uso:
    python src/predict.py
    python src/predict.py --model models/modelo_concreto.joblib

Carga el Pipeline exportado con joblib y realiza una predicción
de ejemplo para verificar que el modelo funciona correctamente.
"""

import argparse

import joblib
import numpy as np
import pandas as pd


# Nombres de las features en el orden esperado por el modelo
FEATURE_NAMES = [
    "cement",
    "blast_furnace_slag",
    "fly_ash",
    "water",
    "superplasticizer",
    "coarse_aggregate",
    "fine_aggregate",
    "age",
]

# Ejemplo de entrada: mezcla de concreto típica
MUESTRA_EJEMPLO = {
    "cement": 540.0,
    "blast_furnace_slag": 0.0,
    "fly_ash": 0.0,
    "water": 162.0,
    "superplasticizer": 2.5,
    "coarse_aggregate": 1040.0,
    "fine_aggregate": 676.0,
    "age": 28,
}


def cargar_modelo(model_path):
    """Carga el Pipeline serializado desde disco.

    Args:
        model_path: Ruta al archivo .joblib del modelo.

    Returns:
        Pipeline de Scikit-Learn entrenado.
    """
    pipeline = joblib.load(model_path)
    print(f"Modelo cargado desde: {model_path}")
    return pipeline


def predecir(pipeline, datos_entrada):
    """Realiza una predicción con el Pipeline cargado.

    Args:
        pipeline: Pipeline de Scikit-Learn entrenado.
        datos_entrada: Diccionario con los valores de las features.

    Returns:
        Valor numérico con la predicción (resistencia en MPa).
    """
    df = pd.DataFrame([datos_entrada], columns=FEATURE_NAMES)
    prediccion = pipeline.predict(df)
    return float(prediccion[0])


def main():
    """Punto de entrada principal del script de predicción."""
    parser = argparse.ArgumentParser(
        description="Inferencia con el modelo de resistencia del concreto"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="models/modelo_concreto.joblib",
        help="Ruta al modelo serializado (.joblib)",
    )
    args = parser.parse_args()

    # Cargar modelo
    pipeline = cargar_modelo(args.model)

    # Predicción de ejemplo
    print(f"\nDatos de entrada (ejemplo):")
    for nombre, valor in MUESTRA_EJEMPLO.items():
        print(f"  {nombre}: {valor}")

    resultado = predecir(pipeline, MUESTRA_EJEMPLO)
    print(f"\nResistencia predicha: {resultado:.2f} MPa")


if __name__ == "__main__":
    main()
