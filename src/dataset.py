"""Procesa datos crudos y los guarda en la carpeta processed.

Flujo:
    1. Lee concrete_data.csv desde data/raw
    2. Elimina filas duplicadas y nulos
    3. Guarda dataset.csv en data/processed
"""

from pathlib import Path

import pandas as pd

from config import PROCESSED_DATA_DIR, RAW_DATA_DIR


def process_dataset(
    input_path: Path = RAW_DATA_DIR / "concrete_data.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
) -> None:
    """Lee, limpia y guarda el dataset crudo.

    Args:
        input_path: Ruta al CSV crudo.
        output_path: Ruta de destino en processed.
    """
    df = pd.read_csv(input_path)

    df = df.drop_duplicates().dropna()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset guardado: {output_path}  ({len(df)} filas)")


if __name__ == "__main__":
    process_dataset()
