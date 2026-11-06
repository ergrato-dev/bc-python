"""Ejercicio 01: definir funciones, parámetros, valores por defecto y return.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python functions_lab.py
"""

print("Ejercicio 01 · Definir funciones")

# ============================================
# PASO 1: def define, la llamada ejecuta
# ============================================
# Definir una función no ejecuta su cuerpo: solo lo guarda con un nombre.
# Descomenta las siguientes líneas:
# def greet(name: str) -> str:
#     print("  (dentro de greet)")
#     return f"Hola, {name}"
#
#
# print("Definida:", greet)
# message = greet("Ana")
# print("Devolvió:", message)

# ============================================
# PASO 2: sin return, la función devuelve None
# ============================================
# print MUESTRA un valor; return lo ENTREGA a quien llamó para que lo use.
# Descomenta las siguientes líneas:
# def show_double(n: int) -> None:
#     print("  el doble es", n * 2)
#
#
# def double(n: int) -> int:
#     return n * 2
#
#
# shown = show_double(4)
# returned = double(4)
# print("show_double devolvió:", shown, "| double devolvió:", returned)
# print("double(double(3)) =", double(double(3)))

# ============================================
# PASO 3: argumentos por posición y por nombre
# ============================================
# Por posición importa el orden; por nombre, no. Los de posición van primero.
# Descomenta las siguientes líneas:
# def describe(label: str, value: float, unit: str) -> str:
#     return f"{label}: {value} {unit}"
#
#
# print(describe("Norte", 12.5, "µg/m³"))
# print(describe(unit="µg/m³", label="Sur", value=8.0))
# print(describe("Centro", unit="µg/m³", value=40.2))

# ============================================
# PASO 4: valores por defecto y parámetros solo por nombre
# ============================================
# decimals tiene valor por defecto; el * obliga a pasar sign por nombre.
# Descomenta las siguientes líneas:
# def money(amount: float, decimals: int = 2, *, sign: str = "$") -> str:
#     return f"{sign}{amount:,.{decimals}f}"
#
#
# print(money(1234.5))
# print(money(1234.5, 0))
# print(money(1234.5, sign="€"))

# ============================================
# PASO 5: devolver varios valores
# ============================================
# return a, b devuelve una tupla; quien llama la desempaqueta en dos nombres.
# Descomenta las siguientes líneas:
# def split_minutes(total: int) -> tuple[int, int]:
#     return total // 60, total % 60
#
#
# hours, minutes = split_minutes(135)
# print("135 min =", hours, "h", minutes, "min | tupla completa:", split_minutes(135))

# ============================================
# PASO 6: return termina la función en cuanto se ejecuta
# ============================================
# Las "cláusulas de guarda" descartan los casos raros primero y dejan el caso normal al final.
# Descomenta las siguientes líneas:
# def grade(score: float) -> str:
#     if score < 0 or score > 5:
#         return "fuera de rango"
#     if score < 3:
#         return "insuficiente"
#     return "aprobado"
#
#
# print("Notas:", grade(-1), "|", grade(2.9), "|", grade(4.5))
