"""Ejercicio 03: CSV y JSON.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python formats_lab.py
"""

import csv
import json
from pathlib import Path

print("Ejercicio 03 · CSV y JSON")

OUT = Path(__file__).parent / "salida"
OUT.mkdir(exist_ok=True)
CSV_PATH = OUT / "medidas.csv"
JSON_PATH = OUT / "resumen.json"

# ============================================
# PASO 1: escribir un CSV con csv.writer
# ============================================
# delimiter=";" porque los valores usan coma decimal; newline="" deja los saltos a csv.
# Descomenta las siguientes líneas:
# rows = [["Norte", "12,5"], ["Sur; centro", "8"], ["Centro", "NA"]]
# with CSV_PATH.open("w", encoding="utf-8", newline="") as file:
#     writer = csv.writer(file, delimiter=";")
#     writer.writerow(["etiqueta", "valor"])
#     writer.writerows(rows)
# print(CSV_PATH.read_text(encoding="utf-8"), end="")

# ============================================
# PASO 2: leerlo con csv.reader
# ============================================
# Cada fila es una lista de str; next() saca la cabecera y el for sigue desde la segunda.
# Descomenta las siguientes líneas:
# with CSV_PATH.open(encoding="utf-8", newline="") as file:
#     reader = csv.reader(file, delimiter=";")
#     header = next(reader)
#     print("Cabecera:", header)
#     for label, value in reader:
#         number = None if value == "NA" else float(value.replace(",", "."))
#         print(f"  {label!r}: {value!r} -> {number}")
# line = '"Sur; centro";8'
# print("Con split:", line.split(";"))

# ============================================
# PASO 3: leer por nombre con csv.DictReader
# ============================================
# La cabecera se convierte en las claves de cada fila.
# Descomenta las siguientes líneas:
# with CSV_PATH.open(encoding="utf-8", newline="") as file:
#     for row in csv.DictReader(file, delimiter=";"):
#         print(" ", row)

# ============================================
# PASO 4: Python <-> texto JSON con dumps y loads
# ============================================
# JSON conserva los tipos, pero no tiene tuplas y sus claves son siempre texto.
# Descomenta las siguientes líneas:
# data = {"registros": 3, "mediana": 10.2, "falta": None, "ok": True, "rango": (8.0, 12.5), 2026: "año"}
# text = json.dumps(data)
# print("dumps:", text)
# back = json.loads(text)
# print("loads:", back)
# print("¿Igual?", back == data)
# try:
#     json.dumps({"etiquetas": {"Norte", "Sur"}})
# except TypeError as error:
#     print("TypeError:", error)

# ============================================
# PASO 5: archivos JSON con dump y load
# ============================================
# indent=2 lo hace legible; ensure_ascii=False deja las tildes tal cual.
# Descomenta las siguientes líneas:
# summary = {"zona": "Peñalara", "registros": 3, "mediana": 10.2}
# with JSON_PATH.open("w", encoding="utf-8") as file:
#     json.dump(summary, file, ensure_ascii=False, indent=2)
#     file.write("\n")
# print(JSON_PATH.read_text(encoding="utf-8"), end="")
# with JSON_PATH.open(encoding="utf-8") as file:
#     print("load:", json.load(file))
# print("Sin ensure_ascii:", json.dumps(summary))
# try:
#     json.loads('{\n  "registros": 3,\n}')
# except json.JSONDecodeError as error:
#     print(f"JSONDecodeError en la línea {error.lineno}: {error.msg}")
