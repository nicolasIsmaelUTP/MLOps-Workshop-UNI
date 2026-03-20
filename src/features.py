"""Feature engineering sobre el dataset de resistencia del concreto.

Genera features derivadas (ratios, totales) para usar en un sklearn Pipeline.
"""

from pathlib import Path

import pandas as pd

from config import PROCESSED_DATA_DIR


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Genera features derivadas a partir del DataFrame de entrada.

    Args:
        df: DataFrame con las columnas crudas del dataset.

    Returns:
        Copia del DataFrame con columnas adicionales derivadas.
    """
    df = df.copy()
    df["water_cement_ratio"] = df["water"] / (df["cement"] + 1e-9)
    df["binder_total"] = df["cement"] + df["blast_furnace_slag"] + df["fly_ash"]
    df["aggregate_total"] = df["coarse_aggregate"] + df["fine_aggregate"]
    return df


def main(
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
) -> None:
    """Lee el dataset limpio, aplica feature engineering y guarda el resultado.

    Args:
        input_path: Ruta al dataset limpio.
        output_path: Ruta de destino para las features.
    """
    df = pd.read_csv(input_path)
    out = build_features(df)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)
    print(f"Features guardadas: {output_path}  ({out.shape[1]} columnas)")


if __name__ == "__main__":
    main()
