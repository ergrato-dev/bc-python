"""Ejercicio 02: informe del entorno donde corre Python (tu máquina o un contenedor).

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python report.py                  # en tu máquina
    docker compose run --build --rm app      # en el contenedor
"""

import getpass
import os
import platform
from pathlib import Path

# Docker crea el archivo /.dockerenv en cada contenedor; en tu máquina no existe.
print(f"Contenedor: {Path('/.dockerenv').exists()}")
print(f"Carpeta:    {os.getcwd()}")

# ============================================
# PASO 3: quién ejecuta el programa
# ============================================
# getpass.getuser() da el nombre del usuario del proceso. En Linux, root es el
# usuario con identificador 0: os.geteuid() == 0 da True o False.
# Descomenta las siguientes líneas:
# print(f"Python:     {platform.python_version()}")
# print(f"Usuario:    {getpass.getuser()}")
# print(f"Es root:    {os.geteuid() == 0}")
