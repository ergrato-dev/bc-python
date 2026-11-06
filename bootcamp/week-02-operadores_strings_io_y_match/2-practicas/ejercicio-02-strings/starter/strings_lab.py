"""Ejercicio 02: índices, slicing y métodos de str.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python strings_lab.py
"""

import unicodedata

print("Ejercicio 02 · Strings")

# ============================================
# PASO 1: índices y slicing
# ============================================
# s[inicio:fin] incluye inicio y excluye fin; -1 es el último carácter.
# Descomenta las siguientes líneas:
# s = "Observatorio"
# print("Primero y último:", s[0], s[-1])
# print("Slices:", s[:3], s[-5:], s[::-1])
# print("Fuera de rango:", repr(s[50:]))

# ============================================
# PASO 2: los str no cambian; los métodos devuelven uno nuevo
# ============================================
# Si no guardas el resultado de strip(), se pierde.
# Descomenta las siguientes líneas:
# code = "  ab 12 "
# code.strip()
# print("Sin guardar:", repr(code))
# code = code.strip().upper().replace(" ", "-")
# print("Guardado:", repr(code))

# ============================================
# PASO 3: partition y desempaquetar
# ============================================
# partition devuelve siempre 3 partes: antes, separador y después.
# Descomenta las siguientes líneas:
# def mask_email(email: str) -> str:
#     user, _, domain = email.strip().partition("@")
#     return f"{user[:1]}***@{domain}"
#
#
# def file_extension(filename: str) -> str:
#     _, dot, extension = filename.rpartition(".")
#     return extension.lower() if dot else ""
#
#
# print("Correo:", mask_email(" ana.perez@correo.co "))
# print("Extensiones:", file_extension("datos.final.CSV"), repr(file_extension("LEEME")))

# ============================================
# PASO 4: split y join
# ============================================
# split() parte por espacios y descarta los vacíos; split(";") parte por cada ;.
# Descomenta las siguientes líneas:
# line = "Norte;12,5;;µg/m³"
# print("Campos:", line.split(";"))
# print("Palabras:", len("  el   aire  de hoy ".split()))
# print("Unidas:", " / ".join(["PM2.5", "PM10", "O3"]))

# ============================================
# PASO 5: palíndromos con casefold y [::-1]
# ============================================
# Se ignoran mayúsculas y espacios antes de comparar con el texto al revés.
# Descomenta las siguientes líneas:
# def is_palindrome(text: str) -> bool:
#     clean = text.casefold().replace(" ", "")
#     return clean == clean[::-1]
#
#
# print("Palíndromos:", is_palindrome("Anita lava la tina"), is_palindrome("Python"))

# ============================================
# PASO 6: comparar texto que viene de fuera
# ============================================
# La misma é puede venir en 1 carácter (NFC) o en 2 (NFD). Normaliza antes de comparar.
# Descomenta las siguientes líneas:
# def normalize_text(text: str) -> str:
#     return unicodedata.normalize("NFC", text).strip().casefold()
#
#
# def same_text(a: str, b: str) -> bool:
#     return normalize_text(a) == normalize_text(b)
#
#
# decomposed = unicodedata.normalize("NFD", "Café")
# print("Longitudes:", len("Café"), len(decomposed))
# print("Con ==:", decomposed == "café")
# print("Con same_text:", same_text(decomposed, " café "))
