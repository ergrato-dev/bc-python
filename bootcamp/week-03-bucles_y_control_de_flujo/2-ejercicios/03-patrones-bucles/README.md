# 🎨 Ejercicio 03: Patrones de Bucles

## 🎯 Objetivo

Practicar `break`, `continue`, la cláusula `else` en bucles, y patrones comunes de iteración como búsqueda, filtrado y transformación.

---

## 📋 Instrucciones

Abre el archivo `starter/main.py` y sigue los pasos descomentando el código correspondiente a cada sección.

---

## Paso 1: Break - Salir del Bucle

`break` termina el bucle inmediatamente:

```python
for i in range(10):
    if i == 5:
        break  # Sale del bucle
    print(i)
# Imprime: 0, 1, 2, 3, 4
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

## Paso 2: Continue - Saltar Iteración

`continue` salta a la siguiente iteración:

```python
for i in range(5):
    if i == 2:
        continue  # Salta el 2
    print(i)
# Imprime: 0, 1, 3, 4
```

**Descomenta** la sección del Paso 2.

---

## Paso 3: Else en Bucles

`else` se ejecuta si el bucle termina sin `break`:

```python
for i in range(5):
    if i == 10:  # Nunca se cumple
        break
else:
    print("Bucle completado sin break")
```

**Descomenta** la sección del Paso 3.

---

## Paso 4: Patrón Búsqueda

Buscar un elemento y retornar cuando se encuentre:

```python
def find_first_negative(numbers):
    for num in numbers:
        if num < 0:
            return num
    return None
```

**Descomenta** la sección del Paso 4.

---

## Paso 5: Patrón Filtrado

Seleccionar elementos que cumplen una condición:

```python
def filter_even(numbers):
    result = []
    for num in numbers:
        if num % 2 == 0:
            result.append(num)
    return result
```

**Descomenta** la sección del Paso 5.

---

## Paso 6: Patrón Transformación

Aplicar una operación a cada elemento:

```python
def square_all(numbers):
    result = []
    for num in numbers:
        result.append(num ** 2)
    return result
```

**Descomenta** la sección del Paso 6.

---

## Paso 7: Patrón Max/Min

Encontrar el valor extremo:

```python
def find_max(numbers):
    if not numbers:
        return None
    max_val = numbers[0]
    for num in numbers[1:]:
        if num > max_val:
            max_val = num
    return max_val
```

**Descomenta** la sección del Paso 7.

---

## Paso 8: Combinando Patrones

Combinar varios patrones en una función:

```python
def analyze(numbers):
    # Contador + Acumulador + Filtrado
    total = 0
    positives = []
    for num in numbers:
        total += num
        if num > 0:
            positives.append(num)
    return {"sum": total, "positives": positives}
```

**Descomenta** la sección del Paso 8.

---

## ✅ Verificación

Al completar todos los pasos, deberías ver resultados como:

```
--- Paso 4: Búsqueda ---
Primer negativo en [5, 3, -2, 8, -1]: -2
Primer negativo en [1, 2, 3]: None

--- Paso 5: Filtrado ---
Pares en [1, 2, 3, 4, 5, 6]: [2, 4, 6]

--- Paso 7: Max/Min ---
Máximo en [3, 7, 2, 9, 1]: 9
Mínimo en [3, 7, 2, 9, 1]: 1
```

---

## 🎯 Conceptos Clave

- `break`: Termina el bucle completamente
- `continue`: Salta a la siguiente iteración
- `else`: Se ejecuta si NO hubo break
- Patrones: búsqueda, filtrado, transformación, max/min
- Combinar patrones para resolver problemas complejos
