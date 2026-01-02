"""
Ejercicio 03: Diccionarios Anidados
===================================
Trabaja con estructuras de datos complejas: acceso, modificación,
iteración y transformación de diccionarios multinivel.

Instrucciones:
1. Lee cada sección para entender el concepto
2. Descomenta el código paso a paso
3. Ejecuta el archivo para ver los resultados
4. Experimenta modificando los valores
"""

# ============================================
# PASO 1: Acceso a Datos Anidados
# ============================================
print("=== PASO 1: Acceso a Datos Anidados ===")

# Los diccionarios anidados son comunes para representar
# datos jerárquicos como organigramas, configuraciones, JSON, etc.

# Descomenta las siguientes líneas:

# # Estructura de empresa: departamento -> empleado -> datos
# company: dict[str, dict[str, dict[str, str | int]]] = {
#     "engineering": {
#         "alice": {"role": "senior", "salary": 80000},
#         "bob": {"role": "junior", "salary": 50000}
#     },
#     "marketing": {
#         "carol": {"role": "manager", "salary": 90000}
#     }
# }
#
# # Acceso directo encadenado (si estamos seguros que existe)
# eng_employees = company["engineering"]
# print(f"Empleados en Engineering: {eng_employees.keys()}")
#
# alice_role: str = company["engineering"]["alice"]["role"]
# print(f"Rol de Alice: {alice_role}")
#
# alice_salary: int = company["engineering"]["alice"]["salary"]
# print(f"Salario de Alice: {alice_salary}")
#
# # Acceso seguro con get() encadenado
# # Útil cuando no sabemos si las claves existen
# alice_bonus: int = company.get("engineering", {}).get("alice", {}).get("bonus", 0)
# print(f"Bonus de Alice (seguro): {alice_bonus}")
#
# # Acceder a usuario que no existe
# unknown_name: str = company.get("sales", {}).get("unknown", {}).get("name", "Unknown")
# print(f"Nombre de usuario inexistente: {unknown_name}")

print()

# ============================================
# PASO 2: Modificación Segura
# ============================================
print("=== PASO 2: Modificación Segura ===")

# Modificar estructuras anidadas requiere cuidado.
# setdefault() es muy útil para crear niveles intermedios.

# Descomenta las siguientes líneas:

# # Copiar la estructura para no modificar la original
# import copy
# company_copy: dict = copy.deepcopy(company)
#
# # Modificar valor existente
# company_copy["engineering"]["alice"]["salary"] = 85000
# print(f"Después de modificar salario: {company_copy['engineering']['alice']['salary']}")
#
# # Crear estructura completa si no existe
# data: dict = {}
#
# # setdefault crea el nivel si no existe y retorna el diccionario
# data.setdefault("users", {}).setdefault("new_user", {})["name"] = "Charlie"
# data["users"]["new_user"]["role"] = "junior"
# print(f"Estructura creada: {data}")
#
# # Agregar a lista dentro de estructura anidada
# data["users"]["new_user"].setdefault("skills", []).append("python")
# print(f"Después de agregar skills: {data}")

print()

# ============================================
# PASO 3: Iteración Multinivel
# ============================================
print("=== PASO 3: Iteración Multinivel ===")

# Iterar sobre estructuras anidadas requiere bucles anidados.
# items() es tu mejor amigo aquí.

# Descomenta las siguientes líneas:

# # Usar la estructura company definida en Paso 1
# company: dict[str, dict[str, dict[str, str | int]]] = {
#     "engineering": {
#         "alice": {"role": "senior", "salary": 80000},
#         "bob": {"role": "junior", "salary": 50000}
#     },
#     "marketing": {
#         "carol": {"role": "manager", "salary": 90000}
#     }
# }
#
# # Iterar sobre todos los niveles
# for dept_name, employees in company.items():
#     print(f"📁 {dept_name.upper()}")
#     for emp_name, emp_data in employees.items():
#         role = emp_data["role"]
#         salary = emp_data["salary"]
#         print(f"  👤 {emp_name}: {role} (${salary:,})")
#
# # Calcular estadísticas
# total_employees: int = 0
# total_salaries: int = 0
#
# for dept_name, employees in company.items():
#     for emp_name, emp_data in employees.items():
#         total_employees += 1
#         total_salaries += emp_data["salary"]
#
# print(f"\nTotal empleados: {total_employees}")
# print(f"Nómina total: ${total_salaries:,}")

print()

# ============================================
# PASO 4: Aplanar Estructuras
# ============================================
print("=== PASO 4: Aplanar Estructuras ===")

# A veces necesitamos convertir estructuras anidadas
# en diccionarios planos (útil para configuraciones, CSV, etc.)

# Descomenta las siguientes líneas:

# # Configuración anidada
# config: dict[str, dict[str, str | int]] = {
#     "server": {
#         "host": "localhost",
#         "port": 8080
#     },
#     "database": {
#         "host": "db.local",
#         "name": "myapp"
#     }
# }
#
# # Aplanar usando dict comprehension
# flat_config: dict[str, str | int] = {
#     f"{section}.{key}": value
#     for section, settings in config.items()
#     for key, value in settings.items()
# }
# print(f"Aplanado: {flat_config}")
#
# # Reconstruir desde estructura plana
# reconstructed: dict[str, dict[str, str | int]] = {}
# for flat_key, value in flat_config.items():
#     section, key = flat_key.split(".")
#     if section not in reconstructed:
#         reconstructed[section] = {}
#     reconstructed[section][key] = value
#
# print(f"Reconstruido: {reconstructed}")

print()

# ============================================
# PASO 5: Dict Comprehensions Anidadas
# ============================================
print("=== PASO 5: Dict Comprehensions Anidadas ===")

# Las comprehensions pueden crear estructuras anidadas
# de forma concisa y elegante.

# Descomenta las siguientes líneas:

# # Crear tabla de multiplicar como diccionario anidado
# multiplication_table: dict[int, dict[int, int]] = {
#     x: {y: x * y for y in range(1, 4)}
#     for x in range(1, 4)
# }
#
# print("Tabla de multiplicar:")
# for x, row in multiplication_table.items():
#     print(f"{x}: {row}")
#
# # Acceder: 3 x 2
# print(f"3 x 2 = {multiplication_table[3][2]}")
#
# # Filtrar empleados senior de cada departamento
# company: dict[str, dict[str, dict[str, str | int]]] = {
#     "engineering": {
#         "alice": {"role": "senior", "salary": 80000},
#         "bob": {"role": "junior", "salary": 50000}
#     },
#     "marketing": {
#         "carol": {"role": "manager", "salary": 90000}
#     }
# }
#
# # Extraer nombres de seniors/managers por departamento
# senior_by_dept: dict[str, list[str]] = {
#     dept: [
#         name for name, data in employees.items()
#         if data["role"] in ("senior", "manager")
#     ]
#     for dept, employees in company.items()
# }
# print(f"Seniors: {senior_by_dept}")

# ============================================
# DESAFÍO EXTRA (Opcional)
# ============================================
# Crea un sistema de inventario multinivel:
# 1. Estructura: categoría -> producto -> {precio, stock, proveedor}
# 2. Agrega al menos 2 categorías con 2 productos cada una
# 3. Calcula el valor total del inventario (precio * stock)
# 4. Encuentra productos con stock bajo (< 10)
# 5. Agrupa productos por proveedor

# Tu código aquí:
# inventory: dict[str, dict[str, dict[str, str | int | float]]] = {}
