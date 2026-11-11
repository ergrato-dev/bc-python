"""Genera un archivo grande de medidas "etiqueta;valor" para medir el Observatorio.

Uso: uv run python scripts/generar_medidas.py 100000 perfil/grande.txt

La semilla es fija: con el mismo número de líneas sale siempre el mismo archivo, así tus
medidas de antes y de después comparan lo mismo. Uno de cada 20 valores es "NA".
Cambia LABELS por las etiquetas de tu dominio.
"""

import random
import sys
from pathlib import Path

LABELS = ["Norte", "Sur", "Centro", "Este", "Oeste"]


def main() -> None:
    count, path = int(sys.argv[1]), Path(sys.argv[2])
    rng = random.Random(22)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for _ in range(count):
            label = rng.choice(LABELS)
            value = "NA" if rng.random() < 0.05 else f"{rng.uniform(0, 80):.1f}".replace(".", ",")
            file.write(f"{label};{value}\n")


if __name__ == "__main__":
    main()
