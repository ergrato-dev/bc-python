"""Ejercicio 04: functools.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python functools_lab.py
"""

import functools

print("Ejercicio 04 · functools")

# ============================================
# PASO 1: partial fija argumentos
# ============================================
# Descomenta las siguientes líneas:
# def convert(value: float, factor: float, offset: float = 0.0) -> float:
#     return value * factor + offset
#
#
# to_fahrenheit = functools.partial(convert, factor=9 / 5, offset=32)
# to_ppb = functools.partial(convert, factor=0.509)
# print("10 °C en F:", to_fahrenheit(10.0), "· 55,1 µg/m³ en ppb:", round(to_ppb(55.1), 1))
# print("Qué guarda:", to_ppb.func.__name__, to_ppb.args, to_ppb.keywords)
# from_binary = functools.partial(int, base=2)
# print("int con base fija:", from_binary("1010"))

# ============================================
# PASO 2: cache recuerda resultados
# ============================================
# Descomenta las siguientes líneas:
# calls = 0
#
#
# def ways(steps: int) -> int:
#     """Formas de subir steps escalones de uno en uno o de dos en dos."""
#     global calls
#     calls += 1
#     return 1 if steps <= 1 else ways(steps - 1) + ways(steps - 2)
#
#
# print("Sin caché:", ways(25), "con", f"{calls:,}", "llamadas")
#
#
# @functools.cache
# def ways_cached(steps: int) -> int:
#     return 1 if steps <= 1 else ways_cached(steps - 1) + ways_cached(steps - 2)
#
#
# print("Con caché:", ways_cached(25), "·", ways_cached.cache_info())
# print("Otra vez:", ways_cached(25), "·", ways_cached.cache_info())

# ============================================
# PASO 3: lru_cache con tope y argumentos que no valen
# ============================================
# Descomenta las siguientes líneas:
# @functools.lru_cache(maxsize=2)
# def level(value: float) -> str:
#     print(f"    calculo el nivel de {value}")
#     return "alto" if value > 50 else "normal"
#
#
# for value in [55.1, 12.5, 55.1, 8.0, 55.1]:
#     level(value)
# print(level.cache_info())
#
#
# @functools.cache
# def total(values: tuple[float, ...]) -> float:
#     return sum(values)
#
#
# print("Con una tupla:", total((1.0, 2.5)))
# try:
#     total([1.0, 2.5])  # type: ignore[arg-type]
# except TypeError as error:
#     print("Con una lista:", error)

# ============================================
# PASO 4: reduce pliega una secuencia
# ============================================
# Descomenta las siguientes líneas:
# values = [12.5, 8.0, 55.1, 48.9]
# print("Suma con reduce:", functools.reduce(lambda acc, v: acc + v, values, 0.0))
# labels = ["Sur", "Centro", "Norte", "Oriente", "Este"]
# print("La más larga:", functools.reduce(lambda a, b: a if len(a) >= len(b) else b, labels))

# ============================================
# PASO 5: singledispatch elige por el tipo
# ============================================
# Descomenta las siguientes líneas:
# @functools.singledispatch
# def describe(item: object) -> str:
#     raise TypeError(f"describe no acepta {type(item).__name__}")
#
#
# @describe.register
# def _(item: float) -> str:
#     return f"un valor: {item}"
#
#
# @describe.register
# def _(item: str) -> str:
#     return f"una etiqueta: {item!r}"
#
#
# @describe.register
# def _(item: list) -> str:  # type: ignore[type-arg]
#     return f"una lista de {len(item)}: " + ", ".join(describe(x) for x in item)
#
#
# print(describe(12.5))
# print(describe("Norte"))
# print(describe([8.0, "Sur"]))
# for item in (3, None):
#     try:
#         describe(item)
#     except TypeError as error:
#         print("TypeError:", error)
