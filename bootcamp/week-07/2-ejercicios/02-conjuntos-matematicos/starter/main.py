"""
Ejercicio 02: Operaciones Matemáticas de Conjuntos
==================================================
Aprende las operaciones de teoría de conjuntos en Python.

Instrucciones:
1. Lee cada sección
2. Descomenta el código indicado
3. Ejecuta el archivo para ver los resultados
"""

# ============================================
# PASO 1: Unión (|)
# ============================================
print("=== PASO 1: Unión (|) ===")

# La unión combina todos los elementos de ambos conjuntos
# Descomenta las siguientes líneas:

# a: set[int] = {1, 2, 3, 4, 5}
# b: set[int] = {4, 5, 6, 7, 8}
#
# print(f"Set A: {a}")
# print(f"Set B: {b}")
#
# # Unión con operador |
# union_result = a | b
# print(f"A | B (unión): {union_result}")
#
# # Unión con método union()
# union_method = a.union(b)
# print(f"A.union(B): {union_method}")

print()

# ============================================
# PASO 2: Intersección (&)
# ============================================
print("=== PASO 2: Intersección (&) ===")

# La intersección retorna elementos comunes a ambos conjuntos
# Descomenta las siguientes líneas:

# a: set[int] = {1, 2, 3, 4, 5}
# b: set[int] = {4, 5, 6, 7, 8}
#
# # Intersección con operador &
# intersection_result = a & b
# print(f"A & B (intersección): {intersection_result}")
#
# # Intersección con método intersection()
# intersection_method = a.intersection(b)
# print(f"A.intersection(B): {intersection_method}")

print()

# ============================================
# PASO 3: Diferencia (-)
# ============================================
print("=== PASO 3: Diferencia (-) ===")

# La diferencia retorna elementos en A pero no en B
# Descomenta las siguientes líneas:

# a: set[int] = {1, 2, 3, 4, 5}
# b: set[int] = {4, 5, 6, 7, 8}
#
# # Diferencia A - B
# diff_a_b = a - b
# print(f"A - B (en A pero no en B): {diff_a_b}")
#
# # Diferencia B - A (diferente resultado)
# diff_b_a = b - a
# print(f"B - A (en B pero no en A): {diff_b_a}")

print()

# ============================================
# PASO 4: Diferencia Simétrica (^)
# ============================================
print("=== PASO 4: Diferencia Simétrica (^) ===")

# La diferencia simétrica retorna elementos exclusivos de cada conjunto
# Descomenta las siguientes líneas:

# a: set[int] = {1, 2, 3, 4, 5}
# b: set[int] = {4, 5, 6, 7, 8}
#
# # Diferencia simétrica con operador ^
# sym_diff = a ^ b
# print(f"A ^ B (exclusivos): {sym_diff}")
#
# # Verificación: (A | B) - (A & B) = A ^ B
# verification = (a | b) - (a & b)
# print(f"Verificación (A|B) - (A&B): {verification}")

print()

# ============================================
# PASO 5: Subconjuntos y Superconjuntos
# ============================================
print("=== PASO 5: Subconjuntos y Superconjuntos ===")

# <= verifica subconjunto, >= verifica superconjunto
# Descomenta las siguientes líneas:

# small: set[int] = {1, 2}
# large: set[int] = {1, 2, 3, 4, 5}
#
# print(f"small: {small}")
# print(f"large: {large}")
#
# # Subconjunto: todos los elementos de small están en large
# print(f"¿small es subconjunto de large? {small <= large}")
# print(f"¿large es superconjunto de small? {large >= small}")
#
# # Subconjunto propio: < (no puede ser igual)
# print(f"¿{{1, 2}} < {{1, 2, 3}}? (subconjunto propio) {small < large}")
# print(f"¿{{1, 2}} < {{1, 2}}? (subconjunto propio de sí mismo) {small < small}")

print()

# ============================================
# PASO 6: Conjuntos Disjuntos
# ============================================
print("=== PASO 6: Conjuntos Disjuntos ===")

# isdisjoint() verifica si no hay elementos en común
# Descomenta las siguientes líneas:

# evens: set[int] = {2, 4, 6, 8}
# odds: set[int] = {1, 3, 5, 7}
# mixed: set[int] = {1, 2, 3}
#
# print(f"evens: {evens}")
# print(f"odds: {odds}")
# print(f"mixed: {mixed}")
#
# # Pares e impares no comparten elementos
# print(f"¿evens y odds son disjuntos? {evens.isdisjoint(odds)}")
#
# # Pares y mixed comparten el 2
# print(f"¿evens y mixed son disjuntos? {evens.isdisjoint(mixed)}")

print()

# ============================================
# PASO 7: Operaciones In-Place
# ============================================
print("=== PASO 7: Operaciones In-Place ===")

# |=, &=, -= modifican el set original
# Descomenta las siguientes líneas:

# numbers: set[int] = {1, 2, 3}
# print(f"numbers inicial: {numbers}")
#
# # Unión in-place
# numbers |= {4, 5}
# print(f"Después de |= {{4, 5}}: {numbers}")
#
# # Intersección in-place
# numbers &= {2, 3, 4, 6}
# print(f"Después de &= {{2, 3, 4, 6}}: {numbers}")
#
# # Diferencia in-place
# numbers -= {4}
# print(f"Después de -= {{4}}: {numbers}")

print()

# ============================================
# PASO 8: Caso Práctico - Análisis de Usuarios
# ============================================
print("=== PASO 8: Caso Práctico - Análisis de Usuarios ===")

# Analizar actividad de usuarios con operaciones de conjuntos
# Descomenta las siguientes líneas:

# # Usuarios activos ayer y hoy
# yesterday: set[str] = {"alice", "bob", "carol", "david"}
# today: set[str] = {"bob", "carol", "eve", "frank"}
#
# print("📊 Análisis de Actividad:")
# print(f"  Usuarios activos ayer: {yesterday}")
# print(f"  Usuarios activos hoy: {today}")
# print("  " + "─" * 35)
#
# # Usuarios que volvieron (activos ayer Y hoy)
# returning = yesterday & today
# print(f"  Usuarios que volvieron (intersección): {returning}")
#
# # Usuarios nuevos (activos hoy pero NO ayer)
# new_users = today - yesterday
# print(f"  Usuarios nuevos hoy (diferencia): {new_users}")
#
# # Usuarios que se fueron (activos ayer pero NO hoy)
# churned = yesterday - today
# print(f"  Usuarios que se fueron (diferencia): {churned}")
#
# # Total de usuarios únicos
# all_users = yesterday | today
# print(f"  Todos los usuarios únicos (unión): {all_users}")

print()

# ============================================
# ¡COMPLETADO!
# ============================================
print("=" * 50)
print("✅ ¡Ejercicio completado!")
print("Ahora dominas las operaciones matemáticas de conjuntos.")
print("Continúa con el ejercicio 03-algoritmos-basicos")
print("=" * 50)
