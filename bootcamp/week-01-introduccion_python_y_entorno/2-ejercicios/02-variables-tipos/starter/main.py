"""
Ejercicio 02: Variables y Tipos de Datos

Instrucciones:
1. Lee cada sección y su explicación
2. Descomenta el código de cada paso
3. Ejecuta el programa para ver los resultados
4. Avanza al siguiente paso

Comando para ejecutar:
docker run -it --rm -v $(pwd):/app -w /app python:3.13-slim python starter/main.py
"""

# ============================================
# PASO 1: Variables con type hints
# ============================================
print("--- Paso 1: Variables con type hints ---")

# En Python moderno, indicamos el tipo de cada variable
# Esto hace el código más legible y ayuda a detectar errores
# Descomenta las siguientes líneas:
# nombre: str = "Ana"
# edad: int = 25
# altura: float = 1.65
#
# print(f"Nombre: {nombre}")
# print(f"Edad: {edad}")
# print(f"Altura: {altura}")

print()


# ============================================
# PASO 2: Tipos numéricos
# ============================================
print("--- Paso 2: Tipos numéricos ---")

# int: números enteros (sin decimales)
# float: números con decimales
# Puedes usar _ para hacer números grandes más legibles
# Descomenta las siguientes líneas:
# entero: int = 42
# decimal: float = 3.14159
# numero_grande: int = 1_000_000
#
# print(f"Entero: {entero} (tipo: {type(entero)})")
# print(f"Decimal: {decimal} (tipo: {type(decimal)})")
# print(f"Número grande: {numero_grande}")

print()


# ============================================
# PASO 3: Booleanos
# ============================================
print("--- Paso 3: Booleanos ---")

# bool: valores de verdad True o False
# ¡Importante! Van con mayúscula inicial
# Descomenta las siguientes líneas:
# activo: bool = True
# eliminado: bool = False
#
# print(f"¿Está activo? {activo}")
# print(f"¿Está eliminado? {eliminado}")

print()


# ============================================
# PASO 4: Verificar tipos con type()
# ============================================
print("--- Paso 4: Verificar tipos ---")

# type() retorna el tipo de una variable
# Muy útil para debugging y aprendizaje
# Descomenta las siguientes líneas:
# nombre: str = "Ana"
# edad: int = 25
# altura: float = 1.65
# activo: bool = True
#
# print(f"tipo de nombre: {type(nombre)}")
# print(f"tipo de edad: {type(edad)}")
# print(f"tipo de altura: {type(altura)}")
# print(f"tipo de activo: {type(activo)}")

print()


# ============================================
# PASO 5: Conversión de tipos (casting)
# ============================================
print("--- Paso 5: Conversión de tipos ---")

# Podemos convertir entre tipos usando:
# int()   - convierte a entero
# float() - convierte a decimal
# str()   - convierte a texto
# bool()  - convierte a booleano
# Descomenta las siguientes líneas:
# texto: str = "42"
# print(f"Texto original: {texto} (tipo: {type(texto)})")
#
# como_entero: int = int(texto)
# print(f"Convertido a int: {como_entero} (tipo: {type(como_entero)})")
#
# como_float: float = float(texto)
# print(f"Convertido a float: {como_float} (tipo: {type(como_float)})")
#
# numero: int = 100
# como_texto: str = str(numero)
# print(f"Número a texto: {como_texto} (tipo: {type(como_texto)})")

print()


# ============================================
# PASO 6: f-Strings
# ============================================
print("--- Paso 6: f-Strings ---")

# Los f-strings permiten incluir variables y expresiones
# dentro de strings usando {}
# Son la forma moderna y recomendada de formatear texto
# Descomenta las siguientes líneas:
# nombre: str = "Ana"
# edad: int = 25
# altura: float = 1.65
#
# # Variables simples
# print(f"Hola, soy {nombre} y tengo {edad} años")
# print(f"Mi altura es {altura} metros")
#
# # Expresiones dentro de f-strings
# print(f"El próximo año tendré {edad + 1} años")


# ============================================
# ¡FELICIDADES!
# ============================================
# Has completado el ejercicio de variables y tipos.
# Ahora sabes:
# - Declarar variables con type hints
# - Usar los tipos básicos: str, int, float, bool
# - Verificar tipos con type()
# - Convertir entre tipos
# - Formatear texto con f-strings
