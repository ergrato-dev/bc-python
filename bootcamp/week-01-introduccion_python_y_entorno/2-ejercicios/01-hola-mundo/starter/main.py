"""
Ejercicio 01: Hola Mundo y print()

Instrucciones:
1. Lee cada sección y su explicación
2. Descomenta el código de cada paso
3. Ejecuta el programa para ver los resultados
4. Avanza al siguiente paso

Comando para ejecutar:
docker run -it --rm -v $(pwd):/app -w /app python:3.13-slim python starter/main.py
"""

# ============================================
# PASO 1: Hola Mundo
# ============================================
print("--- Paso 1: Hola Mundo ---")

# El programa más simple: imprimir un mensaje
# Descomenta la siguiente línea:
# print("¡Hola, Mundo!")

print()  # Línea en blanco para separar secciones


# ============================================
# PASO 2: Múltiples valores
# ============================================
print("--- Paso 2: Múltiples valores ---")

# print() puede recibir varios argumentos separados por coma
# Python los imprime con un espacio entre ellos
# Descomenta la siguiente línea:
# print("Hola", "Python", "3.13")

print()


# ============================================
# PASO 3: Parámetro sep
# ============================================
print("--- Paso 3: Parámetro sep ---")

# El parámetro sep cambia el separador entre argumentos
# Por defecto es un espacio " "
# Descomenta las siguientes líneas:
# print("2026", "01", "02", sep="-")
# print("a", "b", "c", sep=" -> ")

print()


# ============================================
# PASO 4: Parámetro end
# ============================================
print("--- Paso 4: Parámetro end ---")

# El parámetro end cambia lo que se imprime al final
# Por defecto es "\n" (nueva línea)
# Descomenta las siguientes líneas:
# print("Cargando", end="...")
# print("Listo!")

print()


# ============================================
# PASO 5: Caracteres especiales
# ============================================
print("--- Paso 5: Caracteres especiales ---")

# \n = nueva línea
# \t = tabulación
# Descomenta las siguientes líneas:
# print("Línea 1\nLínea 2\nLínea 3")
# print("Nombre:\tAna")
# print("Edad:\t25")

print()


# ============================================
# PASO 6: Tarjeta de presentación
# ============================================
print("--- Paso 6: Tarjeta de presentación ---")

# Combina todo lo aprendido
# El operador * repite strings: "=" * 5 produce "====="
# Descomenta las siguientes líneas:
# print("=" * 30)
# print("TARJETA DE PRESENTACIÓN")
# print("=" * 30)
# print("Nombre:\tTu Nombre")
# print("Rol:\tEstudiante Python")
# print("=" * 30)


# ============================================
# ¡FELICIDADES!
# ============================================
# Si llegaste aquí y descomentaste todo el código,
# has completado tu primer ejercicio de Python.
# Ahora entiendes cómo funciona print() con sus
# diferentes parámetros y formatos.
