"""Feature engineering sobre el dataset procesado.

Flujo:
    1. Lee dataset.csv desde data/processed
    2. Genera nuevas features derivadas
    3. Guarda features.csv en data/processed
"""

from pathlib import Path

import pandas as pd

from config import PROCESSED_DATA_DIR


def build_features(
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
) -> None:
    """Genera features derivadas y guarda el resultado.

    Args:
        input_path: Ruta al dataset limpio.
        output_path: Ruta de destino para las features.
    """
    df = pd.read_csv(input_path)

    df["water_cement_ratio"] = df["water"] / (df["cement"] + 1e-9)
    df["binder_total"] = df["cement"] + df["blast_furnace_slag"] + df["fly_ash"]
    df["aggregate_total"] = df["coarse_aggregate"] + df["fine_aggregate"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Features guardadas: {output_path}  ({df.shape[1]} columnas)")


if __name__ == "__main__":
    build_features()
