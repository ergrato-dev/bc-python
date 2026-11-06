"""Ejercicio 02: diccionarios y conjuntos.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python dicts_lab.py
"""

print("Ejercicio 02 · Diccionarios y conjuntos")

# ============================================
# PASO 1: crear un diccionario y leer por clave
# ============================================
# [clave] falla si la clave no existe; .get(clave) devuelve None o el valor por defecto.
# Descomenta las siguientes líneas:
# units = {"aire": "µg/m³", "ruido": "dB", "agua": "mg/L"}
# print("aire:", units["aire"], "| claves:", len(units))
# print("¿ruido?", "ruido" in units, "| ¿luz?", "luz" in units)
# print("luz con get:", units.get("luz"), "| con defecto:", units.get("luz", "sin unidad"))

# ============================================
# PASO 2: añadir, cambiar, borrar y recorrer
# ============================================
# Asignar a una clave nueva la añade; a una existente, cambia su valor.
# Descomenta las siguientes líneas:
# units["luz"] = "lx"
# units["agua"] = "mg/l"
# del units["ruido"]
# for domain, unit in units.items():
#     print(f"  {domain:<6}{unit}")

# ============================================
# PASO 3: contar con un diccionario
# ============================================
# get(level, 0) da 0 la primera vez que aparece un nivel.
# Descomenta las siguientes líneas:
# levels = ["alto", "bajo", "alto", "medio", "alto", "bajo"]
# counts: dict[str, int] = {}
# for level in levels:
#     counts[level] = counts.get(level, 0) + 1
# print("Conteo:", counts)
# print("Más frecuente:", max(counts, key=lambda level: counts[level]))

# ============================================
# PASO 4: agrupar con setdefault
# ============================================
# setdefault(clave, []) devuelve la lista de esa clave, y la crea vacía si no existía.
# Descomenta las siguientes líneas:
# records = [("Norte", 12.5), ("Sur", 8.0), ("Norte", 48.9), ("Sur", 9.5), ("Este", 30.0)]
# groups: dict[str, list[float]] = {}
# for label, value in records:
#     groups.setdefault(label, []).append(value)
# print("Grupos:", groups)
# for label, values in groups.items():
#     print(f"  {label}: media {sum(values) / len(values):.2f} de {len(values)}")

# ============================================
# PASO 5: una tupla como clave
# ============================================
# Las claves deben ser inmutables: una tupla sirve, una lista no.
# Descomenta las siguientes líneas:
# by_place_and_day = {("Norte", "lunes"): 12.5, ("Norte", "martes"): 14.0}
# print("Norte el martes:", by_place_and_day[("Norte", "martes")])

# ============================================
# PASO 6: conjuntos
# ============================================
# Un set no repite elementos y no guarda un orden: para mostrarlo, ordénalo.
# Descomenta las siguientes líneas:
# monday = {"Norte", "Sur", "Este"}
# tuesday = {"Sur", "Este", "Oeste"}
# print("Ambos días:", sorted(monday & tuesday))
# print("Alguno:", sorted(monday | tuesday))
# print("Solo lunes:", sorted(monday - tuesday))
# labels = ["Norte", "Sur", "Norte", "Norte", "Este"]
# print("Distintas:", len(set(labels)), "| ¿Sur?", "Sur" in set(labels))
# print("Vacíos:", type({}), type(set()))
