"""Ejercicio 02 · Integración continua con GitHub Actions.

Un programa pequeño con sus tests: lo que importa es dónde se ejecutan. En este
ejercicio, en una máquina de GitHub, en cada push y en cada pull request.
"""

import sys

LOW, HIGH = 20.0, 50.0


def level(value: float) -> str:
    """Nivel de una medida: bajo por debajo de LOW, alto desde HIGH."""
    if value < LOW:
        return "bajo"
    if value > HIGH:
        return "alto"
    return "medio"


if __name__ == "__main__":
    print("Ejercicio 02 · Integración continua con GitHub Actions")
    print("Python", sys.version.split()[0])
    for value in (12.5, 30.0, 55.1):
        print(f"{value} -> {level(value)}")
