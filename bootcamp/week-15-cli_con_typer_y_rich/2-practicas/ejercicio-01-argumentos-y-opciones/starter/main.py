"""Ejercicio 01 · Argumentos y opciones con Typer.

Cada paso añade un comando. Typer lee los parámetros de la función y sus anotaciones,
y con eso construye el analizador de la línea de comandos, la ayuda y los errores.
"""

from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.callback()
def main() -> None:
    """Ejercicio 01 · Argumentos y opciones."""
    # Con un callback, cada comando se llama por su nombre: `main.py clasificar 12`.
    # Lo verás a fondo en el ejercicio 02.


# ============================================
# PASO 1: Un argumento con tipo
# ============================================
# Descomenta las siguientes líneas:
# @app.command()
# def clasificar(valor: float) -> None:
#     """Dice el nivel de un valor con los umbrales 10 y 50."""
#     nivel = "bajo" if valor < 10 else "alto" if valor > 50 else "medio"
#     print(f"{valor} → {nivel}")


# ============================================
# PASO 2: Opciones con valor por defecto
# ============================================
# Descomenta las siguientes líneas:
# @app.command()
# def umbrales(valor: float, bajo: float = 10.0, alto: float = 50.0) -> None:
#     """Como clasificar, pero con umbrales que puedes cambiar."""
#     nivel = "bajo" if valor < bajo else "alto" if valor > alto else "medio"
#     print(f"{valor} entre {bajo} y {alto} → {nivel}")


# ============================================
# PASO 3: Annotated, ayuda, nombres cortos y una opción booleana
# ============================================
# Descomenta las siguientes líneas:
# @app.command()
# def etiquetar(
#     etiqueta: Annotated[str, typer.Argument(help="El nombre de la estación.")],
#     mayusculas: Annotated[
#         bool,
#         typer.Option("--mayusculas", "-m", help="Escribe la etiqueta en mayúsculas."),
#     ] = False,
# ) -> None:
#     """Escribe una etiqueta limpia."""
#     limpia = etiqueta.strip()
#     print(limpia.upper() if mayusculas else limpia)


# ============================================
# PASO 4: Una lista de argumentos
# ============================================
# Descomenta las siguientes líneas:
# @app.command()
# def media(valores: list[float]) -> None:
#     """Calcula la media de uno o varios valores."""
#     print(f"media de {len(valores)}: {sum(valores) / len(valores):.2f}")


# ============================================
# PASO 5: Un archivo que debe existir
# ============================================
# Descomenta las siguientes líneas:
# @app.command()
# def contar(
#     ruta: Annotated[
#         Path, typer.Argument(exists=True, dir_okay=False, help="Un archivo de texto.")
#     ],
# ) -> None:
#     """Cuenta las líneas de un archivo."""
#     lineas = ruta.read_text(encoding="utf-8").splitlines()
#     print(f"{ruta.name}: {len(lineas)} líneas")


# ============================================
# PASO 6: Elegir entre unos valores fijos
# ============================================
# Descomenta las siguientes líneas:
# class Nivel(StrEnum):
#     BAJO = "bajo"
#     MEDIO = "medio"
#     ALTO = "alto"
#
#
# @app.command()
# def umbral(
#     nivel: Annotated[Nivel, typer.Option(help="El nivel que buscas.")] = Nivel.ALTO,
# ) -> None:
#     """Dice a partir de qué valor empieza un nivel."""
#     limites = {
#         Nivel.BAJO: "menos de 10",
#         Nivel.MEDIO: "de 10 a 50",
#         Nivel.ALTO: "más de 50",
#     }
#     print(f"{nivel.value}: {limites[nivel]}")


# ============================================
# PASO 7: Códigos de salida
# ============================================
# Descomenta las siguientes líneas:
# @app.command()
# def comprobar(valor: float) -> None:
#     """Termina con código 0 si el valor está entre 10 y 50, y con 1 si no."""
#     if valor < 0:
#         raise typer.BadParameter("no puede ser negativo", param_hint="VALOR")
#     if not 10 <= valor <= 50:
#         print(f"{valor} está fuera del rango")
#         raise typer.Exit(code=1)
#     print(f"{valor} está dentro del rango")


if __name__ == "__main__":
    app()
