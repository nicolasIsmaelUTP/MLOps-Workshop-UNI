"""Utilidades de visualización para resultados del modelo."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_predicted_vs_actual(
    y_true: pd.Series,
    y_pred,
    r2: float,
    save_path: Path | None = None,
) -> plt.Figure:
    """Genera un scatter plot de valores predichos frente a reales.

    Args:
        y_true: Valores reales del conjunto de prueba.
        y_pred: Array de predicciones del modelo.
        r2: Coeficiente de determinación R² (se muestra en el título).
        save_path: Ruta opcional para guardar la figura en disco (PNG).

    Returns:
        Figura de matplotlib lista para mostrar o loguear en MLflow.
    """
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(y_true, y_pred, alpha=0.6, edgecolors="k", linewidths=0.4)
    lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
    ax.plot(lims, lims, "r--", linewidth=1.5, label="Predicción perfecta")
    ax.set_xlabel("Valor real (MPa)")
    ax.set_ylabel("Predicción (MPa)")
    ax.set_title(f"Predicho vs Real  |  R²={r2:.3f}")
    ax.legend()
    plt.tight_layout()
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150)
    return fig
