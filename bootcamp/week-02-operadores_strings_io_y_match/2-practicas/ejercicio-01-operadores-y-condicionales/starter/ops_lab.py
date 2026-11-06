"""Ejercicio 01: operadores, condicionales y match.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python ops_lab.py
"""

print("Ejercicio 01 · Operadores y condicionales")

# ============================================
# PASO 1: // y % reparten minutos en horas
# ============================================
# total // 60 son las horas completas; total % 60, los minutos que sobran.
# Descomenta las siguientes líneas:
# def minutes_to_text(total: int) -> str:
#     hours = total // 60
#     minutes = total % 60
#     return f"{hours} h {minutes} min"
#
#
# print("135 minutos:", minutes_to_text(135))
# print("59 minutos:", minutes_to_text(59))
# print("-7 // 2 =", -7 // 2, "y -7 % 2 =", -7 % 2)

# ============================================
# PASO 2: and, or y el orden de las condiciones
# ============================================
# Bisiesto: múltiplo de 4 y no de 100, salvo que sea múltiplo de 400.
# Descomenta las siguientes líneas:
# def is_leap_year(year: int) -> bool:
#     return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
#
#
# print("Bisiestos:", is_leap_year(2024), is_leap_year(1900), is_leap_year(2000), is_leap_year(2026))

# ============================================
# PASO 3: or para dar un valor por defecto
# ============================================
# "" es falso: `texto or "por defecto"` lo reemplaza. Cuidado con 0.
# Descomenta las siguientes líneas:
# def label_or_default(label: str) -> str:
#     return label.strip() or "sin etiqueta"
#
#
# print("Etiquetas:", label_or_default("  Norte "), "|", label_or_default("   "))
# print("La trampa del or:", 0 or 10, "|", 0.0 or "sin dato")

# ============================================
# PASO 4: if / elif / else por rangos
# ============================================
# De menor a mayor: cada elif ya sabe que las condiciones anteriores fallaron.
# Descomenta las siguientes líneas:
# def grade(score: float) -> str:
#     if score < 3.0:
#         return "insuficiente"
#     elif score < 4.0:
#         return "aceptable"
#     else:
#         return "sobresaliente"
#
#
# print("Notas:", grade(2.9), "|", grade(3.0), "|", grade(3.99), "|", grade(4.0))

# ============================================
# PASO 5: expresión condicional
# ============================================
# Elige un valor en una línea: None si no se puede dividir.
# Descomenta las siguientes líneas:
# def safe_ratio(a: float, b: float) -> float | None:
#     return None if b == 0 else a / b
#
#
# print("Divisiones:", safe_ratio(10, 4), safe_ratio(10, 0))

# ============================================
# PASO 6: match con literales y alternativas
# ============================================
# case 6 | 7 encaja con 6 o con 7; case _ recoge cualquier otro valor.
# Descomenta las siguientes líneas:
# def day_type(day: int) -> str:
#     match day:
#         case 1 | 2 | 3 | 4 | 5:
#             return "laborable"
#         case 6 | 7:
#             return "fin de semana"
#         case _:
#             return "inválido"
#
#
# print("Días:", day_type(3), "|", day_type(7), "|", day_type(9))
