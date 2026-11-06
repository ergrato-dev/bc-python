"""Ejercicio 03: pyproject.toml y dependencias.

Lee los archivos del proyecto sondeo que creas en el paso 1. Descomenta cada PASO
cuando el README te lo pida y ejecuta, desde starter/:
    uv run python inspect_project.py
"""

import tomllib
import zipfile
from pathlib import Path

print("Ejercicio 03 · pyproject.toml y dependencias")

# sondeo/ está junto a este archivo, se ejecute desde donde se ejecute.
PROJECT = Path(__file__).parent / "sondeo"

# ============================================
# PASO 2: leer pyproject.toml
# ============================================
# TOML se lee con tomllib, de la biblioteca estándar, abriendo en binario ("rb").
# Descomenta las siguientes líneas:
# with (PROJECT / "pyproject.toml").open("rb") as file:
#     pyproject = tomllib.load(file)
# project = pyproject["project"]
# print("Nombre:", project["name"], "| versión:", project["version"])
# print("Python:", project["requires-python"])
# print("Dependencias:", project["dependencies"])
# print("Comandos:", project["scripts"])
# print("Se construye con:", pyproject["build-system"]["build-backend"])
# print("Grupos:", pyproject.get("dependency-groups", "ninguno"))

# ============================================
# PASO 3: leer uv.lock
# ============================================
# uv.lock también es TOML: una tabla [[package]] por paquete, con su versión exacta.
# Descomenta las siguientes líneas:
# with (PROJECT / "uv.lock").open("rb") as file:
#     lock = tomllib.load(file)
# print("Paquetes en el lock:", len(lock["package"]))
# for package in lock["package"]:
#     print(f"  {package['name']}=={package['version']}")

# ============================================
# PASO 4: abrir el wheel
# ============================================
# Un wheel es un zip con el código y una carpeta .dist-info con los metadatos.
# Descomenta las siguientes líneas:
# wheel = next((PROJECT / "dist").glob("*.whl"))
# print("Wheel:", wheel.name)
# with zipfile.ZipFile(wheel) as archive:
#     names = archive.namelist()
#     metadata = archive.read(next(n for n in names if n.endswith("METADATA"))).decode()
# for name in names:
#     print("  ", name)
# for line in metadata.splitlines():
#     if line.startswith(("Name:", "Version:", "Requires-Python:")):
#         print("  ", line)
