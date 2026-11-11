"""Ejercicio 04 · Reproducible o no: el mismo notebook, dos ejecuciones, ¿el mismo resultado?

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import hashlib
from pathlib import Path

from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from nbformat.v4 import new_code_cell, new_notebook

print("Ejercicio 04 · Reproducible o no")

# salida/ no va a Git: el ejercicio escribe ahí sus datos en cada ejecución.
OUT = Path("salida")
OUT.mkdir(exist_ok=True)


def run(*cells: str, folder: Path = OUT) -> list[str]:
    """Ejecuta un notebook con esas celdas en un kernel nuevo; devuelve lo que escribe cada una.

    folder: la carpeta en la que se ejecuta, como la del notebook en JupyterLab.
    """
    notebook = new_notebook(cells=[new_code_cell(source) for source in cells])
    client = NotebookClient(notebook, timeout=60, kernel_name="python3",
                            resources={"metadata": {"path": str(folder)}})
    client.execute()
    return [
        "".join(output.get("text") or output["data"]["text/plain"] for output in cell.outputs).strip()
        for cell in notebook.cells
    ]


def twice(*cells: str) -> str:
    """Ejecuta el notebook dos veces y dice si las dos dan lo mismo."""
    first, second = run(*cells), run(*cells)
    return f"{first[-1]} | {second[-1]} → {'igual' if first == second else 'DISTINTO'}"


print("1 + 1 en un kernel nuevo:", run("1 + 1")[0])


# ============================================
# PASO 1: Números al azar
# ============================================
# Descomenta las siguientes líneas:
# print("sin semilla:", twice("import numpy as np", "round(np.random.default_rng().normal(20, 3), 3)"))
# print("con semilla:", twice("import numpy as np", "round(np.random.default_rng(29).normal(20, 3), 3)"))


# ============================================
# PASO 2: La hora de la ejecución
# ============================================
# Descomenta las siguientes líneas:
# print("ahora:", twice("from datetime import datetime", "datetime.now().strftime('%H:%M:%S.%f')"))
# print("fijada:", twice("from datetime import datetime", "TODAY = datetime(2026, 11, 10)", "TODAY.date()"))


# ============================================
# PASO 3: Rutas que solo existen en tu máquina
# ============================================
# Descomenta las siguientes líneas:
# (OUT / "medidas.csv").write_text("etiqueta,valor\nNorte,12.5\nSur,8.0\n", encoding="utf-8")
# try:
#     run("open('/home/ana/proyecto/notebooks/medidas.csv').read()")
# except CellExecutionError as problem:
#     print(f"ruta absoluta: {problem.ename}")
# print("ruta relativa:", run("open('medidas.csv').read().splitlines()[1]")[-1])


# ============================================
# PASO 4: Los datos cambian por debajo
# ============================================
# Descomenta las siguientes líneas:
# EXPECTED = hashlib.sha256((OUT / "medidas.csv").read_bytes()).hexdigest()
# check = (
#     "import hashlib\n"
#     f"EXPECTED = {EXPECTED!r}\n"
#     "assert hashlib.sha256(open('medidas.csv', 'rb').read()).hexdigest() == EXPECTED, 'otros datos'\n"
#     "'huella correcta'"
# )
# print("los mismos datos:", run(check)[-1])
# (OUT / "medidas.csv").write_text("etiqueta,valor\nNorte,12.5\nSur,8.1\n", encoding="utf-8")
# try:
#     run(check)
# except CellExecutionError as problem:
#     print(f"un valor cambiado: {problem.ename}: {problem.evalue}")


# ============================================
# PASO 5: Las versiones
# ============================================
# Descomenta las siguientes líneas:
# versions = run(
#     "import sys, importlib.metadata",
#     "print(f'Python {sys.version_info.major}.{sys.version_info.minor}')",
#     "print('numpy', importlib.metadata.version('numpy'))",
# )
# print(" · ".join(versions[1:]))
# pinned = [line for line in Path("pyproject.toml").read_text(encoding="utf-8").split('"') if "numpy==" in line]
# print("¿la de pyproject.toml?", versions[2].replace(" ", "==") in pinned)
