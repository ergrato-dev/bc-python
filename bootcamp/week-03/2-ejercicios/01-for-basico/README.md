# 🔄 Ejercicio 01: Bucle For Básico

## 🎯 Objetivo

Practicar la sintaxis del bucle `for`, iteración sobre strings y rangos, y uso de `enumerate()`.

---

## 📋 Instrucciones

Abre el archivo `starter/main.py` y sigue los pasos descomentando el código correspondiente a cada sección.

---

## Paso 1: Iteración Simple sobre String

El bucle `for` puede recorrer cada carácter de un string:

```python
word = "Python"
for char in word:
    print(char)
# Imprime cada letra en una línea separada
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

## Paso 2: Iteración con range()

`range()` genera una secuencia de números:

```python
# range(5) genera: 0, 1, 2, 3, 4
for i in range(5):
    print(f"Iteración {i}")
```

**Descomenta** la sección del Paso 2 en `starter/main.py`.

---

## Paso 3: range() con Inicio y Fin

Puedes especificar dónde empezar y terminar:

```python
# range(1, 6) genera: 1, 2, 3, 4, 5
for i in range(1, 6):
    print(i)
```

**Descomenta** la sección del Paso 3.

---

## Paso 4: range() con Paso

El tercer argumento define el incremento:

```python
# range(0, 10, 2) genera números pares: 0, 2, 4, 6, 8
for i in range(0, 10, 2):
    print(i)
```

**Descomenta** la sección del Paso 4.

---

## Paso 5: Usando enumerate()

`enumerate()` da acceso al índice y valor simultáneamente:

```python
fruits = ["manzana", "banana", "cereza"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

**Descomenta** la sección del Paso 5.

---

## Paso 6: Patrón Contador

Contar elementos que cumplen una condición:

```python
def count_vowels(text: str) -> int:
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count
```

**Descomenta** la sección del Paso 6.

---

## Paso 7: Patrón Acumulador

Acumular valores en cada iteración:

```python
def sum_digits(number: int) -> int:
    total = 0
    for digit in str(number):
        total += int(digit)
    return total
```

**Descomenta** la sección del Paso 7.

---

## Paso 8: Construir Strings

Crear un nuevo string carácter por carácter:

```python
def reverse_string(text: str) -> str:
    result = ""
    for char in text:
        result = char + result  # Agregar al inicio
    return result
```

**Descomenta** la sección del Paso 8.

---

## ✅ Verificación

Al completar todos los pasos, deberías ver una salida similar a:

```
--- Paso 1: Iteración sobre string ---
P
y
t
h
o
n

--- Paso 2: range() básico ---
Iteración 0
Iteración 1
...

--- Paso 6: Contador de vocales ---
Vocales en 'Python': 1
Vocales en 'Programación': 5

--- Paso 7: Suma de dígitos ---
Suma de dígitos de 12345: 15

--- Paso 8: Invertir string ---
'Python' invertido: 'nohtyP'
```

---

## 🎯 Conceptos Clave

- `for variable in secuencia:` itera sobre cada elemento
- `range(n)` genera 0 hasta n-1
- `range(start, stop)` genera desde start hasta stop-1
- `range(start, stop, step)` permite definir incremento
- `enumerate()` retorna (índice, valor)
- Patrones: contador, acumulador, construcción
