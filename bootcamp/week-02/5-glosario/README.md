# 📖 Glosario - Semana 02: Condicionales y Control de Flujo

Términos clave de esta semana ordenados alfabéticamente.

---

## A

### `and` (operador)
Operador lógico que retorna `True` solo si **ambas** condiciones son verdaderas.
```python
age = 25
has_license = True
can_drive = age >= 18 and has_license  # True
```

---

## B

### `bool` (tipo)
Tipo de dato que representa valores de verdad: `True` o `False`.
```python
is_active: bool = True
is_empty: bool = False
```

### Bloque de código
Conjunto de instrucciones que se ejecutan juntas, identificadas por su **indentación**.
```python
if condition:
    # Este es un bloque de código
    print("Línea 1")
    print("Línea 2")
```

### Boolean expression
Ver *Expresión booleana*.

### Branch (rama)
Camino de ejecución que el programa puede tomar según una condición.
```python
if score >= 60:
    print("Aprobado")  # Rama 1
else:
    print("Reprobado")  # Rama 2
```

---

## C

### `case` (keyword)
Palabra clave que define un patrón dentro de un `match` statement.
```python
match command:
    case "start":  # Este es un case
        print("Iniciando")
```

### Comparison operators
Ver *Operadores de comparación*.

### Condicional
Estructura que ejecuta código diferente según se cumpla o no una condición.
```python
if temperature > 30:
    print("Hace calor")
```

### Control de flujo
Mecanismos que determinan el orden en que se ejecutan las instrucciones de un programa.

---

## D

### Default case
Caso por defecto en un `match` statement, representado por `_`.
```python
match value:
    case 1:
        print("Uno")
    case _:  # Default case
        print("Otro valor")
```

---

## E

### `elif` (keyword)
Abreviatura de "else if". Permite encadenar múltiples condiciones.
```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
```

### `else` (keyword)
Bloque que se ejecuta cuando ninguna condición anterior es verdadera.
```python
if is_raining:
    print("Lleva paraguas")
else:
    print("Disfruta el sol")
```

### Expresión booleana
Expresión que evalúa a `True` o `False`.
```python
x > 5           # Expresión de comparación
x > 5 and y < 3  # Expresión lógica compuesta
```

---

## F

### `False` (literal)
Valor booleano que representa falsedad.
```python
is_active = False
```

### Falsy
Valores que Python evalúa como `False` en contexto booleano.
```python
# Valores falsy:
False, None, 0, 0.0, "", [], {}, set()

if not "":  # "" es falsy
    print("String vacío es falsy")
```

---

## G

### Guard (guarda)
Condición adicional en un `case` usando `if`.
```python
match age:
    case n if n < 0:      # Guard: n < 0
        print("Inválido")
    case n if n < 18:     # Guard: n < 18
        print("Menor")
```

---

## I

### `if` (keyword)
Palabra clave que inicia una estructura condicional.
```python
if condition:
    # código a ejecutar si condition es True
```

### Indentación
Espacios al inicio de una línea que definen bloques de código en Python. Se usan **4 espacios** por nivel.
```python
if True:
    print("Indentado 4 espacios")
    if True:
        print("Indentado 8 espacios")
```

---

## L

### Literal pattern
Patrón en `match` que coincide con un valor específico.
```python
match status:
    case 200:       # Literal numérico
        print("OK")
    case "error":   # Literal string
        print("Error")
```

### Logical operators
Ver *Operadores lógicos*.

---

## M

### `match` (keyword)
Palabra clave que inicia un pattern matching statement (Python 3.10+).
```python
match command:
    case "start":
        print("Iniciando")
    case "stop":
        print("Deteniendo")
```

---

## N

### Nested conditionals
Condicionales anidados (uno dentro de otro).
```python
if is_member:
    if has_premium:
        discount = 0.30
    else:
        discount = 0.10
```

### `not` (operador)
Operador lógico que invierte el valor booleano.
```python
is_active = True
is_inactive = not is_active  # False
```

---

## O

### Operadores de comparación
Operadores que comparan valores y retornan booleanos.
```python
==  # Igual a
!=  # Diferente de
<   # Menor que
>   # Mayor que
<=  # Menor o igual
>=  # Mayor o igual
```

### Operadores lógicos
Operadores que combinan expresiones booleanas.
```python
and  # Ambos True
or   # Al menos uno True
not  # Invierte el valor
```

### `or` (operador)
Operador lógico que retorna `True` si **al menos una** condición es verdadera.
```python
is_weekend = day == "saturday" or day == "sunday"
```

### OR pattern
Patrón en `match` que combina múltiples opciones con `|`.
```python
match day:
    case "saturday" | "sunday":
        print("Fin de semana")
```

---

## P

### Pattern matching
Característica de Python 3.10+ que permite comparar estructuras de datos.
```python
match data:
    case pattern1:
        # acción 1
    case pattern2:
        # acción 2
```

---

## S

### Short-circuit evaluation
Evaluación perezosa de operadores lógicos: Python deja de evaluar cuando el resultado está determinado.
```python
# Si x es False, y nunca se evalúa
result = x and y

# Si x es True, y nunca se evalúa
result = x or y
```

### Statement
Instrucción que Python puede ejecutar. Los condicionales son statements compuestos.

---

## T

### Ternary operator
Ver *Expresión condicional*.

### `True` (literal)
Valor booleano que representa verdad.
```python
is_valid = True
```

### Truthy
Valores que Python evalúa como `True` en contexto booleano.
```python
# Valores truthy (ejemplos):
True, 1, "hello", [1, 2], {"a": 1}

if "hello":  # String no vacío es truthy
    print("Es truthy")
```

---

## W

### Wildcard pattern
Patrón `_` en `match` que coincide con cualquier valor.
```python
match value:
    case 1:
        print("Uno")
    case _:  # Wildcard - coincide con todo
        print("Otro")
```

---

## Símbolos

### `_` (underscore)
En pattern matching, coincide con cualquier valor (wildcard).
```python
match x:
    case _:
        print("Coincide con todo")
```

### `|` (pipe)
En pattern matching, combina múltiples patrones (OR).
```python
match color:
    case "red" | "blue" | "green":
        print("Color primario")
```

### `==` vs `=`
- `=` es **asignación**: `x = 5`
- `==` es **comparación**: `x == 5`

---

## 📚 Referencias

- [Python Glossary](https://docs.python.org/3/glossary.html)
- [PEP 634 - Pattern Matching](https://peps.python.org/pep-0634/)
- [Real Python - Conditional Statements](https://realpython.com/python-conditional-statements/)
