# 📖 Glosario - Semana 04

## Comprehensions y Funciones

Términos clave de la semana ordenados alfabéticamente.

---

### A

#### **Argument (Argumento)**
Valor que se pasa a una función cuando se llama. Puede ser posicional o por nombre (keyword).

```python
def greet(name: str) -> str:
    return f"Hola, {name}"

# "Python" es el argumento
greet("Python")
```

#### **`*args`**
Sintaxis especial que permite a una función aceptar un número variable de argumentos posicionales. Se empaquetan en una tupla.

```python
def sum_all(*args: int) -> int:
    return sum(args)

sum_all(1, 2, 3, 4, 5)  # 15
```

---

### B

#### **Built-in Function (Función Incorporada)**
Funciones que vienen incluidas en Python sin necesidad de importar módulos. Ejemplos: `print()`, `len()`, `range()`, `sum()`.

---

### C

#### **Callable (Invocable)**
Cualquier objeto que puede ser llamado con paréntesis `()`. Incluye funciones, métodos, clases y objetos con método `__call__`.

#### **Closure (Clausura)**
Función que recuerda el entorno léxico donde fue creada, capturando variables del scope externo incluso después de que la función externa haya terminado.

```python
def create_multiplier(n: int):
    def multiply(x: int) -> int:
        return x * n  # 'n' es capturada
    return multiply

double = create_multiplier(2)
double(5)  # 10
```

#### **Comprehension**
Sintaxis concisa para crear colecciones (listas, diccionarios, sets) a partir de iterables existentes.

---

### D

#### **Default Parameter (Parámetro por Defecto)**
Valor predeterminado asignado a un parámetro, usado cuando no se proporciona un argumento.

```python
def greet(name: str = "Usuario") -> str:
    return f"Hola, {name}"
```

#### **Dict Comprehension**
Sintaxis para crear diccionarios de forma concisa.

```python
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

#### **Docstring**
Cadena de documentación que describe qué hace una función, sus parámetros y valor de retorno.

```python
def add(a: int, b: int) -> int:
    """
    Suma dos números enteros.

    Args:
        a: Primer número
        b: Segundo número

    Returns:
        La suma de a y b
    """
    return a + b
```

---

### E

#### **Enclosing Scope (Ámbito Envolvente)**
El scope de una función externa que contiene una función anidada. Es la "E" en la regla LEGB.

---

### F

#### **Filter Expression (Expresión de Filtro)**
Condición `if` en una comprehension que filtra elementos.

```python
[x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
```

#### **First-Class Function (Función de Primera Clase)**
En Python, las funciones son objetos de primera clase: pueden asignarse a variables, pasarse como argumentos y retornarse de otras funciones.

#### **Function (Función)**
Bloque de código reutilizable que realiza una tarea específica. Se define con `def` y puede recibir parámetros y retornar valores.

---

### G

#### **Generator Expression (Expresión Generadora)**
Similar a una list comprehension pero con paréntesis. Produce valores bajo demanda (lazy evaluation).

```python
gen = (x**2 for x in range(1000000))  # No consume memoria
```

#### **Global Scope (Ámbito Global)**
Variables definidas a nivel de módulo, accesibles desde cualquier función del mismo módulo. Es la "G" en LEGB.

#### **`global` Keyword**
Palabra clave que permite modificar una variable global desde dentro de una función.

```python
counter = 0

def increment():
    global counter
    counter += 1
```

---

### H

#### **Higher-Order Function (Función de Orden Superior)**
Función que recibe otras funciones como argumentos o retorna una función.

```python
def apply_twice(func, value):
    return func(func(value))
```

---

### I

#### **Iterable (Iterable)**
Objeto que puede ser recorrido en un bucle `for`. Incluye listas, tuplas, strings, diccionarios, sets y generadores.

---

### K

#### **Keyword Argument (Argumento con Nombre)**
Argumento pasado a una función especificando el nombre del parámetro.

```python
greet(name="Ana", age=25)
```

#### **`**kwargs`**
Sintaxis especial que permite aceptar un número variable de argumentos con nombre. Se empaquetan en un diccionario.

```python
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
```

---

### L

#### **Lambda Function (Función Lambda)**
Función anónima definida en una sola línea.

```python
square = lambda x: x ** 2
```

#### **LEGB Rule (Regla LEGB)**
Orden en que Python busca variables: Local → Enclosing → Global → Built-in.

#### **List Comprehension**
Sintaxis concisa para crear listas.

```python
[expression for item in iterable if condition]
```

#### **Local Scope (Ámbito Local)**
Variables definidas dentro de una función, solo accesibles dentro de ella. Es la "L" en LEGB.

---

### N

#### **Nested Comprehension (Comprehension Anidada)**
Comprehension que contiene otra comprehension o múltiples cláusulas `for`.

```python
matrix = [[j for j in range(3)] for i in range(3)]
```

#### **Nested Function (Función Anidada)**
Función definida dentro de otra función.

#### **`nonlocal` Keyword**
Palabra clave que permite modificar una variable del scope enclosing desde una función anidada.

```python
def outer():
    count = 0
    def inner():
        nonlocal count
        count += 1
    return inner
```

---

### P

#### **Parameter (Parámetro)**
Variable declarada en la definición de una función que recibirá un valor (argumento) cuando se llame.

```python
def greet(name: str):  # 'name' es el parámetro
    return f"Hola, {name}"
```

#### **Positional Argument (Argumento Posicional)**
Argumento identificado por su posición en la llamada a la función.

#### **Positional-Only Parameter**
Parámetro que solo puede recibir argumentos por posición (antes de `/`).

```python
def func(x, /, y):  # 'x' es positional-only
    pass
```

---

### R

#### **Return Statement**
Sentencia que finaliza la ejecución de una función y opcionalmente devuelve un valor.

```python
def add(a, b):
    return a + b  # Devuelve la suma
```

#### **Return Value (Valor de Retorno)**
Valor que una función devuelve al código que la llamó.

---

### S

#### **Scope (Ámbito)**
Región del código donde una variable es accesible. Python usa scoping léxico (basado en la estructura del código).

#### **Set Comprehension**
Sintaxis para crear sets de forma concisa.

```python
unique_squares = {x**2 for x in [-1, 1, 2, -2]}
# {1, 4}
```

#### **Side Effect (Efecto Secundario)**
Modificación de estado fuera de la función (variables globales, archivos, etc.). Las funciones puras no tienen efectos secundarios.

---

### T

#### **Type Hint (Anotación de Tipo)**
Indicación del tipo esperado de parámetros y valores de retorno.

```python
def add(a: int, b: int) -> int:
    return a + b
```

---

### U

#### **Unpacking (Desempaquetado)**
Extraer valores de una colección en variables individuales.

```python
a, b, c = [1, 2, 3]
```

---

### V

#### **Variable Shadowing (Sombreado de Variable)**
Cuando una variable local tiene el mismo nombre que una variable en un scope exterior, "ocultándola".

```python
x = 10  # Global

def func():
    x = 5  # Local, "sombrea" la global
    print(x)  # 5
```

---

## 📚 Referencias

- [Python Glossary](https://docs.python.org/3/glossary.html)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstrings](https://peps.python.org/pep-0257/)
- [Real Python - Python Scope](https://realpython.com/python-scope-legb-rule/)

---

[← Volver a Semana 04](../README.md)
