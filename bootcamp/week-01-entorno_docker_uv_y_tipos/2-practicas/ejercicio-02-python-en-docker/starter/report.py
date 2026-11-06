"""Ejercicio 02: informe del entorno donde corre Python (tu máquina o un contenedor)."""

import getpass
import os
import platform
from pathlib import Path


def python_version() -> str:
    """Devuelve la versión del intérprete, por ejemplo "3.14.10"."""
    raise NotImplementedError("Paso 3: implementa python_version")


def current_user() -> str:
    """Devuelve el nombre del usuario del sistema que ejecuta el proceso."""
    raise NotImplementedError("Paso 3: implementa current_user")


def is_root() -> bool:
    """True si el proceso corre como root (identificador de usuario efectivo 0)."""
    raise NotImplementedError("Paso 3: implementa is_root")


def inside_container() -> bool:
    """True si el proceso corre dentro de un contenedor de Docker."""
    # Docker crea el archivo /.dockerenv en cada contenedor; en tu máquina no existe.
    return Path("/.dockerenv").exists()


if __name__ == "__main__":
    print(f"Python:     {python_version()}")
    print(f"Usuario:    {current_user()}")
    print(f"Es root:    {is_root()}")
    print(f"Contenedor: {inside_container()}")
    print(f"Carpeta:    {os.getcwd()}")
    print(f"Sistema:    {platform.system()}")
