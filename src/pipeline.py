"""Definición del Pipeline de Scikit-Learn.

Este módulo construye un Pipeline que encapsula el preprocesamiento
(StandardScaler) y el modelo (RandomForestRegressor) en un solo objeto.

Al exportar el Pipeline completo con joblib, nos aseguramos de que los
datos de entrada en producción reciban las mismas transformaciones que
durante el entrenamiento, eliminando el problema de Train-Serve Skew.
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def crear_pipeline(n_estimators=100, max_depth=15, random_state=42):
    """Crea un pipeline de preprocesamiento + modelo.

    Args:
        n_estimators: Número de árboles en el Random Forest.
        max_depth: Profundidad máxima de cada árbol.
        random_state: Semilla para reproducibilidad.

    Returns:
        Pipeline de Scikit-Learn listo para entrenar con .fit().
    """
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
        )),
    ])
    return pipeline
