# 📖 Glosario - Semana 3: Bucles y Control de Flujo

Términos técnicos ordenados alfabéticamente relacionados con bucles e iteración en Python.

---

## A

### Acumulador (Accumulator)
Patrón de programación donde una variable acumula valores a través de iteraciones.
```python
total = 0
for num in [1, 2, 3, 4, 5]:
    total += num  # Acumula la suma
print(total)  # 15
```

---

## B

### Break
Sentencia que termina inmediatamente el bucle más interno.
```python
for i in range(10):
    if i == 5:
        break  # Sale del bucle
    print(i)  # Imprime 0, 1, 2, 3, 4
```

### Bucle (Loop)
Estructura de control que repite un bloque de código múltiples veces.

### Bucle Anidado (Nested Loop)
Un bucle dentro de otro bucle.
```python
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})")
```

### Bucle Infinito (Infinite Loop)
Bucle que nunca termina porque su condición siempre es verdadera.
```python
# ❌ Evitar - bucle infinito
# while True:
#     print("Esto nunca termina")
```

---

## C

### Condición de Salida (Exit Condition)
Expresión booleana que determina cuándo termina un bucle `while`.

### Contador (Counter)
Variable que cuenta iteraciones o elementos que cumplen una condición.
```python
count = 0
for char in "hello":
    if char == "l":
        count += 1
print(count)  # 2
```

### Continue
Sentencia que salta a la siguiente iteración del bucle.
```python
for i in range(5):
    if i == 2:
        continue  # Salta el 2
    print(i)  # Imprime 0, 1, 3, 4
```

---

## E

### Else (en bucles)
Cláusula que se ejecuta si el bucle termina normalmente (sin `break`).
```python
for i in range(5):
    if i == 10:
        break
else:
    print("Bucle completado")  # Se ejecuta
```

### Enumerate
Función que retorna índice y valor al iterar.
```python
for i, char in enumerate("ABC"):
    print(f"{i}: {char}")
# 0: A, 1: B, 2: C
```

---

## F

### Flag (Bandera)
Variable booleana usada para controlar el flujo de un bucle.
```python
found = False
while not found:
    # buscar algo
    if condition:
        found = True
```

### For Loop
Bucle que itera sobre cada elemento de una secuencia.
```python
for item in [1, 2, 3]:
    print(item)
```

---

## I

### Incremento (Increment)
Aumento del valor de una variable, típicamente en cada iteración.
```python
i = 0
while i < 5:
    print(i)
    i += 1  # Incremento
```

### Iterable
Objeto que puede ser recorrido con un bucle `for`.
```python
# Ejemplos de iterables:
# - strings: "hello"
# - listas: [1, 2, 3]
# - rangos: range(10)
# - diccionarios: {"a": 1}
```

### Iteración (Iteration)
Una ejecución del bloque de código dentro de un bucle.

---

## O

### Off-by-One Error
Error común al usar rangos, donde se incluye o excluye un elemento por error.
```python
# Quiero 1 al 10
range(10)      # ❌ Da 0-9
range(1, 10)   # ❌ Da 1-9
range(1, 11)   # ✅ Da 1-10
```

---

## P

### Paso (Step)
Incremento entre elementos consecutivos en `range()`.
```python
range(0, 10, 2)  # 0, 2, 4, 6, 8 (paso de 2)
range(10, 0, -1) # 10, 9, 8, ... 1 (paso negativo)
```

### Patrón de Búsqueda (Search Pattern)
Técnica para encontrar un elemento que cumple una condición.
```python
def find_first_negative(nums):
    for num in nums:
        if num < 0:
            return num
    return None
```

### Patrón de Filtrado (Filter Pattern)
Técnica para seleccionar elementos que cumplen una condición.
```python
evens = []
for num in [1, 2, 3, 4, 5]:
    if num % 2 == 0:
        evens.append(num)
```

---

## R

### Range
Función que genera una secuencia de números enteros.
```python
range(5)        # 0, 1, 2, 3, 4
range(1, 6)     # 1, 2, 3, 4, 5
range(0, 10, 2) # 0, 2, 4, 6, 8
```

### Reversed
Función que invierte el orden de iteración.
```python
for i in reversed(range(5)):
    print(i)  # 4, 3, 2, 1, 0
```

---

## S

### Secuencia (Sequence)
Tipo de dato ordenado que puede ser iterado (string, lista, tupla, range).

### Sentinela (Sentinel Value)
Valor especial que indica el fin de la entrada.
```python
while True:
    value = input("Número (0 para salir): ")
    if value == "0":  # Sentinela
        break
```

---

## T

### Transformación (Mapping Pattern)
Patrón que aplica una operación a cada elemento.
```python
squares = []
for num in [1, 2, 3]:
    squares.append(num ** 2)
# [1, 4, 9]
```

---

## U

### Underscore (_)
Convención para indicar una variable que no se usa.
```python
for _ in range(5):
    print("Hola")  # No necesitamos el índice
```

---

## V

### Variable de Control
Variable que determina la continuación del bucle.
```python
count = 0  # Variable de control
while count < 5:
    print(count)
    count += 1
```

---

## W

### While Loop
Bucle que repite mientras una condición sea verdadera.
```python
while condition:
    # código
    # actualizar condición
```

---

## Z

### Zip
Función que combina múltiples iterables elemento a elemento.
```python
names = ["Ana", "Bob"]
ages = [25, 30]
for name, age in zip(names, ages):
    print(f"{name}: {age}")
```

---

## 📊 Resumen de Términos Clave

| Término | Descripción |
|---------|-------------|
| `for` | Itera sobre secuencias |
| `while` | Repite mientras condición sea True |
| `range()` | Genera secuencias numéricas |
| `break` | Sale del bucle |
| `continue` | Salta a siguiente iteración |
| `else` | Se ejecuta si no hay break |
| `enumerate()` | Retorna (índice, valor) |
| `zip()` | Combina iterables |
