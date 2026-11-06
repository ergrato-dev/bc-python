"""Ejercicio 04: leer muchas líneas de la entrada estándar y resumirlas.

Descomenta cada PASO cuando el README te lo pida y ejecuta con el archivo como entrada:
    uv run python lines_lab.py < lecturas.txt
"""

import sys

print("Ejercicio 04 · Muchas líneas")

# ============================================
# PASO 1: leer todas las líneas de stdin
# ============================================
# readlines() lee hasta el final y devuelve una lista; cada línea conserva su "\n".
# Descomenta las siguientes líneas:
# lines = sys.stdin.readlines()
# print("Líneas leídas:", len(lines))
# for line in lines[:3]:
#     print("  ", repr(line))

# ============================================
# PASO 2: limpiar, numerar y saltar lo que no son datos
# ============================================
# number sigue contando las líneas saltadas: así coincide con la línea del archivo.
# Descomenta las siguientes líneas:
# skipped = 0
# for number, raw in enumerate(lines, start=1):
#     line = raw.strip()
#     if line == "" or line.startswith("#"):
#         skipped += 1
#         continue
#     print(f"  línea {number}: {line}")
# print("Saltadas:", skipped)

# ============================================
# PASO 3: acumular total, cantidad y máximo
# ============================================
# Las líneas sin ";" y las medidas que faltan no entran en las cuentas.
# Descomenta las siguientes líneas:
# total = 0.0
# count = 0
# missing = 0
# best_label = None
# best_value = None
# for raw in lines:
#     line = raw.strip()
#     label, separator, text = line.partition(";")
#     if line == "" or line.startswith("#") or separator == "":
#         continue
#     if text.strip() in ("", "NA"):
#         missing += 1
#         continue
#     value = float(text.replace(",", "."))
#     total += value
#     count += 1
#     if best_value is None or value > best_value:
#         best_label, best_value = label, value
# print(f"Medidas: {count} | sin dato: {missing} | promedio: {total / count:.2f}")
# print(f"Máximo: {best_label} con {best_value}")

# ============================================
# PASO 4: avisar de las líneas inválidas y terminar con su código
# ============================================
# Cada error va a stderr con su número de línea; el programa sigue con las demás.
# Descomenta las siguientes líneas:
# errors = 0
# for number, raw in enumerate(lines, start=1):
#     line = raw.strip()
#     if line == "" or line.startswith("#"):
#         continue
#     if ";" not in line:
#         print(f"error: línea {number}: {line!r}", file=sys.stderr)
#         errors += 1
# print("Líneas inválidas:", errors)
# raise SystemExit(1 if errors > 0 else 0)
