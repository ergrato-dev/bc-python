"""Ejercicio 01: tu primer programa ejecutado con uv."""

import platform


def greet(name: str) -> str:
    """Devuelve "Hola, <name>", o "Hola, mundo" si name está vacío o solo tiene espacios."""
    raise NotImplementedError("Paso 4: implementa greet")


def python_summary() -> str:
    """Devuelve "Python X.Y.Z" con la versión del intérprete que ejecuta este archivo."""
    raise NotImplementedError("Paso 5: implementa python_summary")


# Solo se ejecuta con `uv run python main.py`, no cuando pytest importa el archivo.
if __name__ == "__main__":
    print(greet("mundo"))
    print(python_summary())
