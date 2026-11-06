"""Ejercicio 02 · Comandos, callback y contexto con Typer.

Una aplicación con varios comandos, opciones globales en el callback, --version,
un grupo de comandos dentro de otro, stdin y una confirmación.
"""

import sys
from typing import Annotated

import typer

__version__ = "0.2.0"

DATOS = {"Norte": 12.5, "Sur": 8.0, "Oriente": 55.1}

app = typer.Typer(no_args_is_help=True, add_completion=False)


# ============================================
# PASO 1: Un solo comando
# ============================================
# Descomenta las siguientes líneas:
# @app.command()
# def listar() -> None:
#     """Escribe cada estación con su valor."""
#     for etiqueta, valor in DATOS.items():
#         print(f"{etiqueta}: {valor}")


# ============================================
# PASO 2: Un segundo comando
# ============================================
# Descomenta las siguientes líneas:
# @app.command()
# def media() -> None:
#     """Escribe la media de todas las estaciones."""
#     print(f"media: {sum(DATOS.values()) / len(DATOS):.1f}")


# ============================================
# PASO 3: El callback: opciones de toda la aplicación
# ============================================
# Descomenta las siguientes líneas:
# def mostrar_version(valor: bool) -> None:
#     if valor:
#         print(f"ejercicio-02 {__version__}")
#         raise typer.Exit()
#
#
# @app.callback()
# def principal(
#     ctx: typer.Context,
#     unidad: Annotated[str, typer.Option(help="La unidad de las medidas.")] = "µg/m³",
#     version: Annotated[
#         bool, typer.Option("--version", callback=mostrar_version, is_eager=True)
#     ] = False,
# ) -> None:
#     """Ejercicio 02 · Comandos, callback y contexto."""
#     print(f"[callback] unidad={unidad}")
#     ctx.obj = {"unidad": unidad}
#
#
# @app.command()
# def maximo(ctx: typer.Context) -> None:
#     """Escribe la estación con el valor más alto, en la unidad del callback."""
#     etiqueta = max(DATOS, key=DATOS.__getitem__)
#     print(f"máximo: {etiqueta} {DATOS[etiqueta]} {ctx.obj['unidad']}")


# ============================================
# PASO 4: Un grupo de comandos dentro de la aplicación
# ============================================
# Descomenta las siguientes líneas:
# escala = typer.Typer(help="Consulta y comprueba la escala.")
# app.add_typer(escala, name="escala")
#
#
# @escala.command("ver")
# def escala_ver() -> None:
#     """Escribe los umbrales."""
#     print("bajo < 10 ≤ medio ≤ 50 < alto")
#
#
# @escala.command("comprobar")
# def escala_comprobar(bajo: float, alto: float) -> None:
#     """Comprueba que el umbral bajo es menor que el alto."""
#     if bajo >= alto:
#         print(f"umbrales imposibles: {bajo} ≥ {alto}", file=sys.stderr)
#         raise typer.Exit(code=1)
#     print("umbrales correctos")


# ============================================
# PASO 5: Argumentos o stdin
# ============================================
# Descomenta las siguientes líneas:
# @app.command()
# def leer(lineas: Annotated[list[str] | None, typer.Argument()] = None) -> None:
#     """Cuenta las líneas que recibe como argumentos o, si no hay, por stdin."""
#     origen = "argumentos" if lineas else "stdin"
#     datos = lineas or [linea.strip() for linea in sys.stdin if linea.strip()]
#     print(f"{len(datos)} líneas de {origen}")


# ============================================
# PASO 6: Pedir confirmación
# ============================================
# Descomenta las siguientes líneas:
# @app.command()
# def borrar(
#     etiqueta: str,
#     si: Annotated[bool, typer.Option("--si", help="No preguntes.")] = False,
# ) -> None:
#     """Borra una estación (solo en memoria), después de confirmarlo."""
#     if not si:
#         typer.confirm(f"¿Borrar {etiqueta}?", abort=True)
#     DATOS.pop(etiqueta, None)
#     print(f"borrada: {etiqueta}; quedan {len(DATOS)}")


if __name__ == "__main__":
    app()
