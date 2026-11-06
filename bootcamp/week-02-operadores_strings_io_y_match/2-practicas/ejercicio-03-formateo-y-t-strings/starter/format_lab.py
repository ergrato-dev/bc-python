"""Ejercicio 03: formato de números, tablas alineadas y t-strings.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python format_lab.py
"""

import html
from string.templatelib import Interpolation, Template, convert

print("Ejercicio 03 · Formateo y t-strings")

# ============================================
# PASO 1: decimales, miles y porcentaje
# ============================================
# Lo que va después de : es la especificación de formato.
# Descomenta las siguientes líneas:
# print("Decimales:", f"{3.14159:.2f}", f"{2.5:.0f}", f"{3.5:.0f}")
# print("Miles:", f"{1234567.5:,.2f}", f"{1000000:_}")
# print("Porcentaje:", f"{0.125:.1%}", f"{7 / 9:.0%}")
# decimals = 3
# print("Precisión variable:", f"{3.14159:.{decimals}f}")

# ============================================
# PASO 2: dinero en formato colombiano
# ============================================
# El mini-lenguaje usa , para miles y . para decimales: se intercambian.
# Descomenta las siguientes líneas:
# def money(amount: float) -> str:
#     text = f"{amount:,.2f}"
#     return "$ " + text.replace(",", "_").replace(".", ",").replace("_", ".")
#
#
# print("Dinero:", money(1234567.5), "|", money(950))

# ============================================
# PASO 3: columnas con ancho y alineación
# ============================================
# Textos a la izquierda (<), números a la derecha (>).
# Descomenta las siguientes líneas:
# def table_row(label: str, value: float) -> str:
#     return f"{label:<12}|{value:>9.2f}"
#
#
# print(f"{'Estación':<12}|{'PM2.5':>9}")
# print(table_row("Norte", 12.5))
# print(table_row("Centro", 131.04))
# print(table_row("Sur", 7))

# ============================================
# PASO 4: depurar con =
# ============================================
# f"{x=}" escribe la expresión y su valor.
# Descomenta las siguientes líneas:
# value = 12.345
# print(f"{value=}", f"{value * 2 = }", f"{value=:.1f}")

# ============================================
# PASO 5: una t-string no es un str
# ============================================
# t"..." produce un Template: partes fijas y valores por separado.
# Descomenta las siguientes líneas:
# name = "<b>Ana</b>"
# greeting = t"Hola, {name}"
# print("Tipo:", type(greeting).__name__)
# print("Partes fijas:", greeting.strings)
# print("Valores:", greeting.values)
# print("Con f-string:", f"Hola, {name}")

# ============================================
# PASO 6: procesar la plantilla escapando HTML
# ============================================
# to_html recorre la plantilla (el `for` es de la semana 3 y la lista `parts`,
# de la 5): copia las partes fijas tal cual y a cada valor le aplica su
# formato y después html.escape.
# Descomenta las siguientes líneas:
# def to_html(template: Template) -> str:
#     parts = []
#     for item in template:
#         match item:
#             case str() as text:
#                 parts.append(text)
#             case Interpolation(value, _, conversion, format_spec):
#                 formatted = format(convert(value, conversion), format_spec)
#                 parts.append(html.escape(formatted))
#     return "".join(parts)
#
#
# pm25 = 12.345
# print("HTML:", to_html(t"<p>Hola, {name}: {pm25:.1f} µg/m³</p>"))
