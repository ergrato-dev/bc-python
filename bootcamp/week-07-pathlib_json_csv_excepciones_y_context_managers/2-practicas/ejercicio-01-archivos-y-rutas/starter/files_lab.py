"""Ejercicio 01: pathlib y archivos de texto.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python files_lab.py
"""

from pathlib import Path

print("Ejercicio 01 · Archivos y rutas")

# Qué: la carpeta salida/ junto a este archivo, para todo lo que el ejercicio escribe.
# Para qué: __file__ es la ruta de este .py; así salida/ no depende de desde dónde lo lances.
OUT = Path(__file__).parent / "salida"
OUT.mkdir(exist_ok=True)

# ============================================
# PASO 1: las piezas de una ruta
# ============================================
# parent, name, stem y suffix solo leen el texto: el archivo no tiene que existir.
# Descomenta las siguientes líneas:
# path = Path("/home/ana/proyectos/observatorio/medidas.csv")
# print("parent:", path.parent)
# print("name:", path.name, "| stem:", path.stem, "| suffix:", path.suffix)
# print("Unida con /:", Path("datos") / "2026" / "medidas.csv")
# print("Otra extensión:", path.with_suffix(".json").name)
# print("¿Existe?", path.exists())

# ============================================
# PASO 2: relativa o absoluta
# ============================================
# Una ruta relativa se resuelve desde la carpeta de trabajo, no desde la del .py.
# Descomenta las siguientes líneas:
# print("Carpeta de trabajo:", Path.cwd().name)
# print("Carpeta de este .py:", Path(__file__).parent.name)
# relative = Path("salida") / "notas.txt"
# print("¿Absoluta?", relative.is_absolute(), "->", relative.resolve().is_absolute())

# ============================================
# PASO 3: escribir y leer con with
# ============================================
# "w" vacía el archivo al abrirlo; write no añade el salto de línea.
# Descomenta las siguientes líneas:
# notes = OUT / "notas.txt"
# with notes.open("w", encoding="utf-8") as file:
#     file.write("Norte;12,5\n")
#     file.write("Peñalara;3,5\n")
# print("¿Cerrado tras el with?", file.closed)
# with notes.open(encoding="utf-8") as file:
#     print("read().splitlines():", file.read().splitlines())
# with notes.open(encoding="utf-8") as file:
#     print("readlines():", file.readlines())
# print("read_text:", repr(notes.read_text(encoding="utf-8")))

# ============================================
# PASO 4: los modos "a" y "w"
# ============================================
# "a" escribe detrás de lo que había; "w" empieza de cero.
# Descomenta las siguientes líneas:
# log = OUT / "registro.txt"
# log.write_text("", encoding="utf-8")
# for value in ["10", "20", "30"]:
#     with log.open("a", encoding="utf-8") as file:
#         file.write(f"{value}\n")
# print("Tras tres 'a':", log.read_text(encoding="utf-8").splitlines())
# with log.open("w", encoding="utf-8") as file:
#     file.write("40\n")
# print("Tras un 'w':", log.read_text(encoding="utf-8").splitlines())

# ============================================
# PASO 5: carpetas y glob
# ============================================
# mkdir(parents=True, exist_ok=True) crea la carpeta y las que falten, sin error si ya está.
# Descomenta las siguientes líneas:
# daily = OUT / "diarias" / "2026"
# daily.mkdir(parents=True, exist_ok=True)
# for day in ["03", "01", "02"]:
#     (daily / f"medidas-{day}.txt").write_text(f"Norte;{day}\n", encoding="utf-8")
# (daily / "leeme.md").write_text("notas\n", encoding="utf-8")
# found = sorted(daily.glob("*.txt"))
# print("Archivos .txt:", [path.name for path in found])
# print("Tamaño del primero:", found[0].stat().st_size, "bytes")
# print("Relativa a salida:", found[0].relative_to(OUT))
