"""Ejercicio 02: excepciones.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python errors_lab.py
"""

from pathlib import Path

print("Ejercicio 02 · Excepciones")

# ============================================
# PASO 1: capturar con try y except
# ============================================
# Si float falla con ValueError, el except devuelve None; si no falla, el except no corre.
# Descomenta las siguientes líneas:
# def parse_number(text: str) -> float | None:
#     try:
#         return float(text.replace(",", "."))
#     except ValueError:
#         return None
#
#
# for text in ["12,5", "8", "NA", ""]:
#     print(f"  {text!r} -> {parse_number(text)}")
# try:
#     float("NA")
# except ValueError as error:
#     print("Mensaje:", error)

# ============================================
# PASO 2: else y finally
# ============================================
# else corre solo si el try no falló; finally corre siempre.
# Descomenta las siguientes líneas:
# def divide(total: float, count: int) -> None:
#     try:
#         mean = total / count
#     except ZeroDivisionError:
#         print("  except: no hay valores")
#     else:
#         print(f"  else: media {mean}")
#     finally:
#         print("  finally: siempre")
#
#
# print("divide(30, 3):")
# divide(30, 3)
# print("divide(30, 0):")
# divide(30, 0)

# ============================================
# PASO 3: una excepción sube por las llamadas
# ============================================
# La función se corta donde salta el error y la excepción sube hasta quien la capture.
# Descomenta las siguientes líneas:
# def read_value(text: str) -> float:
#     print("  read_value: empieza")
#     value = float(text)
#     print("  read_value: termina")
#     return value
#
#
# def read_all(texts: list[str]) -> list[float]:
#     print("  read_all: empieza")
#     values = [read_value(text) for text in texts]
#     print("  read_all: termina")
#     return values
#
#
# try:
#     read_all(["1", "x", "3"])
# except ValueError as error:
#     print("  capturado arriba:", error)

# ============================================
# PASO 4: excepción propia y raise ... from
# ============================================
# Traduce un error de bajo nivel en uno con sentido, y guarda el original como causa.
# Descomenta las siguientes líneas:
# class DataFileError(Exception):
#     """Un archivo de datos que no se puede leer."""
#
#
# def read_lines(path: Path) -> list[str]:
#     try:
#         with path.open(encoding="utf-8") as file:
#             return file.read().splitlines()
#     except FileNotFoundError as error:
#         raise DataFileError(f"no existe el archivo {path}") from error
#
#
# try:
#     read_lines(Path("no-existe.csv"))
# except DataFileError as problem:
#     print("Mensaje:", problem)
#     print("Tipo:", type(problem).__name__)
#     print("Causa:", repr(problem.__cause__))

# ============================================
# PASO 5: familias de excepciones
# ============================================
# except OSError captura toda la familia: FileNotFoundError, IsADirectoryError, PermissionError...
# Descomenta las siguientes líneas:
# for name in ["no-existe.txt", "."]:
#     try:
#         Path(name).read_text(encoding="utf-8")
#     except OSError as error:
#         print(f"  {name!r}: {type(error).__name__} | ¿es OSError? {isinstance(error, OSError)}")
# print("Familia de FileNotFoundError:", [cls.__name__ for cls in FileNotFoundError.__mro__])
