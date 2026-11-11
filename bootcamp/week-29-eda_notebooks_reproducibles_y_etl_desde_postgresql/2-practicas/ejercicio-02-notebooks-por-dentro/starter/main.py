"""Ejercicio 02 · Los notebooks por dentro: un JSON, un kernel y el orden en que ejecutas.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import json
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

print("Ejercicio 02 · Los notebooks por dentro")

# salida/ no va a Git: los notebooks se vuelven a escribir en cada ejecución.
OUT = Path("salida")
OUT.mkdir(exist_ok=True)

# Un notebook de tres celdas de código, escrito desde Python en lugar de desde JupyterLab.
notebook = new_notebook(
    cells=[
        new_markdown_cell("# Medidas de la estación Norte"),
        new_code_cell("values = [12.5, 14.0, 13.0]\ntotal = 0"),
        new_code_cell("for value in values:\n    total = total + value"),
        new_code_cell('print(f"media {total / len(values):.2f}")\nlen(values)'),
    ]
)
notebook.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
print(f"{len(notebook.cells)} celdas, nbformat {notebook.nbformat}.{notebook.nbformat_minor}")


# ============================================
# PASO 1: Un notebook es un archivo JSON
# ============================================
# Descomenta las siguientes líneas:
# path = OUT / "norte.ipynb"
# nbformat.write(notebook, path)
# data = json.loads(path.read_text(encoding="utf-8"))
# print(f"{path.name}: {path.stat().st_size} bytes · claves {sorted(data)}")
# cell = data["cells"][2]
# print({key: cell[key] for key in ["cell_type", "execution_count", "outputs", "source"]})


# ============================================
# PASO 2: Ejecutarlo con un kernel
# ============================================
# Descomenta las siguientes líneas:
# NotebookClient(notebook, timeout=60, kernel_name="python3").execute()
# for cell in notebook.cells[1:]:
#     kinds = [output["output_type"] for output in cell.outputs]
#     print(f"[{cell.execution_count}] {kinds}")
# for output in notebook.cells[3].outputs:
#     print(output["output_type"], "→", repr(output.get("text") or output["data"]["text/plain"]))
# nbformat.write(notebook, path)
# print(f"con salidas: {path.stat().st_size} bytes")


# ============================================
# PASO 3: Estado oculto
# ============================================
# Descomenta las siguientes líneas:
# messy = nbformat.from_dict(json.loads(json.dumps(notebook)))
# client = NotebookClient(messy, timeout=60, kernel_name="python3")
# with client.setup_kernel():
#     # Como en JupyterLab: ejecutas la segunda celda dos veces, por error, y luego la tercera.
#     for index in [1, 2, 2, 3]:
#         client.execute_cell(messy.cells[index], index)
# print("en desorden:", messy.cells[3].outputs[0]["text"].strip(),
#       "· contadores", [cell.execution_count for cell in messy.cells[1:]])
# NotebookClient(messy, timeout=60, kernel_name="python3").execute()
# print("de arriba abajo:", messy.cells[3].outputs[0]["text"].strip(),
#       "· contadores", [cell.execution_count for cell in messy.cells[1:]])


# ============================================
# PASO 4: Una celda borrada
# ============================================
# Descomenta las siguientes líneas:
# broken = nbformat.from_dict(json.loads(json.dumps(notebook)))
# # Borras la celda que define `values`: en tu sesión, `values` sigue en memoria...
# del broken.cells[1]
# try:
#     # ...pero un kernel nuevo no la tiene.
#     NotebookClient(broken, timeout=60, kernel_name="python3").execute()
# except CellExecutionError as problem:
#     print(f"kernel nuevo: {problem.ename}: {problem.evalue}")


# ============================================
# PASO 5: Quitar las salidas antes de Git
# ============================================
# Descomenta las siguientes líneas:
# big = nbformat.from_dict(json.loads(json.dumps(notebook)))
# big.cells.append(new_code_cell("for day in range(2000):\n    print(day, 12.5 + day / 100)"))
# NotebookClient(big, timeout=60, kernel_name="python3").execute()
# nbformat.write(big, OUT / "grande.ipynb")
# print(f"grande.ipynb con salidas: {(OUT / 'grande.ipynb').stat().st_size} bytes")
# for cell in big.cells:
#     if cell.cell_type == "code":
#         cell.outputs, cell.execution_count = [], None
# nbformat.validate(big)
# nbformat.write(big, OUT / "grande.ipynb")
# print(f"grande.ipynb sin salidas: {(OUT / 'grande.ipynb').stat().st_size} bytes")
