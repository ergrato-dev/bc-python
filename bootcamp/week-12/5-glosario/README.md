# 📖 Glosario - Semana 12

## Decoradores, Generadores y Expresiones Regulares

---

## A

### Accumulator
Patrón que acumula valores progresivamente. En generadores, se puede implementar con `send()` para mantener estado entre llamadas.

```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value
```

---

## B

### Backtracking
Mecanismo del motor de regex que retrocede para probar alternativas cuando un patrón no coincide. Puede causar problemas de rendimiento con patrones mal diseñados.

---

## C

### Capture Group
Grupo de captura en regex. Permite extraer partes específicas del texto coincidente usando paréntesis `()`.

```python
pattern = r"(\d{4})-(\d{2})-(\d{2})"  # Captura año, mes, día
match = re.match(pattern, "2024-01-15")
year = match.group(1)  # "2024"
```

### Character Class
Clase de caracteres en regex. Define un conjunto de caracteres que pueden coincidir en una posición.

```python
r"[aeiou]"    # Vocales
r"[0-9]"      # Dígitos
r"[A-Za-z]"   # Letras
```

### Closure
Función que "recuerda" el entorno en el que fue creada, incluyendo variables locales del ámbito exterior.

```python
def make_multiplier(n):
    def multiplier(x):
        return x * n  # 'n' viene del closure
    return multiplier

double = make_multiplier(2)
double(5)  # 10
```

### Coroutine
Generalización de generadores que pueden tanto producir como consumir valores usando `yield` como expresión y `send()`.

---

## D

### Decorator
Función que modifica o extiende el comportamiento de otra función sin cambiar su código fuente. Usa la sintaxis `@decorator`.

```python
@timer
def my_function():
    pass
# Equivale a: my_function = timer(my_function)
```

### Decorator Factory
Función que retorna un decorador. Se usa cuando el decorador necesita argumentos.

```python
def retry(max_attempts=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # lógica de retry
            pass
        return wrapper
    return decorator

@retry(max_attempts=5)  # retry() retorna el decorador
def my_function():
    pass
```

---

## E

### Eager Evaluation
Evaluación inmediata. Las listas se evalúan eagerly (todos los elementos se crean de inmediato). Contraste con lazy evaluation.

```python
squares = [x**2 for x in range(1000000)]  # Crea todos ahora
```

---

## F

### First-Class Function
Función tratada como cualquier otro objeto: puede asignarse a variables, pasarse como argumento y retornarse de otras funciones. Fundamento de los decoradores.

### Flag (Regex)
Modificador que cambia el comportamiento del motor de regex.

```python
re.IGNORECASE  # Ignora mayúsculas/minúsculas
re.MULTILINE   # ^ y $ coinciden por línea
re.DOTALL      # . coincide con newlines
re.VERBOSE     # Permite comentarios en el patrón
```

### functools.wraps
Decorador que preserva metadata (nombre, docstring) de la función original al crear wrappers.

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Preserva func.__name__, func.__doc__
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## G

### Generator
Función que usa `yield` para producir valores bajo demanda en lugar de retornar todos a la vez. Eficiente en memoria.

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1
```

### Generator Expression
Expresión que crea un generador. Similar a list comprehension pero con paréntesis.

```python
squares = (x**2 for x in range(1000000))  # No crea lista en memoria
```

### Greedy Quantifier
Cuantificador que coincide con el máximo posible de caracteres. Por defecto `*`, `+`, `?` son greedy.

```python
r"<.*>"   # Greedy: "<div>text</div>" → todo
r"<.*?>"  # Non-greedy: "<div>text</div>" → "<div>"
```

---

## H

### Higher-Order Function
Función que toma otra función como argumento o retorna una función. Los decoradores son higher-order functions.

---

## I

### Iterator
Objeto que implementa el protocolo iterador (`__iter__` y `__next__`). Puede recorrerse una sola vez.

```python
class Counter:
    def __init__(self, max):
        self.max = max
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n >= self.max:
            raise StopIteration
        self.n += 1
        return self.n
```

### Iterator Protocol
Protocolo que define cómo un objeto puede ser iterado. Requiere implementar `__iter__()` y `__next__()`.

### itertools
Módulo de biblioteca estándar con funciones para crear iteradores eficientes.

```python
from itertools import chain, cycle, count, permutations
```

---

## L

### Lazy Evaluation
Evaluación diferida. Los generadores evalúan elementos solo cuando se solicitan. Ahorra memoria.

```python
squares = (x**2 for x in range(1000000))  # No calcula nada aún
first = next(squares)  # Calcula solo el primero
```

### Lookahead
Aserción en regex que verifica lo que sigue sin consumirlo.

```python
r"foo(?=bar)"   # Positive: "foo" seguido de "bar"
r"foo(?!bar)"   # Negative: "foo" NO seguido de "bar"
```

### Lookbehind
Aserción en regex que verifica lo que precede sin consumirlo.

```python
r"(?<=\$)\d+"   # Positive: dígitos precedidos de "$"
r"(?<!\$)\d+"   # Negative: dígitos NO precedidos de "$"
```

---

## M

### Match Object
Objeto retornado por `re.match()`, `re.search()` cuando hay coincidencia. Contiene información del match.

```python
match = re.search(r"(\d+)", "abc123")
match.group(0)  # "123" (match completo)
match.group(1)  # "123" (primer grupo)
match.start()   # 3 (posición inicio)
```

### Metacharacter
Carácter con significado especial en regex: `. ^ $ * + ? { } [ ] \ | ( )`

---

## N

### Named Group
Grupo de captura con nombre en regex. Permite acceso por nombre en lugar de índice.

```python
pattern = r"(?P<year>\d{4})-(?P<month>\d{2})"
match = re.match(pattern, "2024-01")
match.group("year")  # "2024"
```

### Non-Greedy Quantifier
Cuantificador que coincide con el mínimo posible. Se agrega `?` después del cuantificador.

```python
r"<.*?>"  # Coincide con el menor string posible
```

---

## P

### ParamSpec
Type hint para decoradores que preserva la firma de la función decorada (Python 3.10+).

```python
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def decorator(func: Callable[P, R]) -> Callable[P, R]:
    ...
```

### Pattern Object
Objeto regex compilado. Mejora rendimiento cuando el patrón se usa múltiples veces.

```python
pattern = re.compile(r"\d+")
pattern.findall("a1b2c3")  # ['1', '2', '3']
```

### Pipeline
Cadena de generadores donde la salida de uno es la entrada del siguiente.

```python
lines = read_file("data.txt")
filtered = filter_lines(lines)
transformed = transform(filtered)
```

---

## Q

### Quantifier
Especifica cuántas veces debe coincidir el elemento anterior en regex.

```python
r"a*"      # 0 o más
r"a+"      # 1 o más
r"a?"      # 0 o 1
r"a{3}"    # Exactamente 3
r"a{2,5}"  # Entre 2 y 5
```

---

## R

### Raw String
String prefijado con `r` que no procesa secuencias de escape. Esencial para regex.

```python
r"\d+"     # El backslash es literal
"\\d+"     # Equivalente sin raw string
```

### re.compile()
Función que compila un patrón regex para uso repetido.

```python
EMAIL = re.compile(r"[\w.-]+@[\w.-]+\.\w+")
EMAIL.match("user@example.com")
```

### re.findall()
Encuentra todas las coincidencias no superpuestas de un patrón.

```python
re.findall(r"\d+", "a1b22c333")  # ['1', '22', '333']
```

### re.match()
Busca coincidencia solo al inicio del string.

### re.search()
Busca coincidencia en cualquier parte del string.

### re.sub()
Reemplaza coincidencias con un string o función.

```python
re.sub(r"\d+", "X", "a1b2")  # "aXbX"
```

---

## S

### send()
Método de generadores para enviar valores. El valor se asigna al resultado de `yield`.

```python
def echo():
    while True:
        received = yield
        print(f"Got: {received}")

gen = echo()
next(gen)       # Inicializar
gen.send("hi")  # Got: hi
```

### StopIteration
Excepción que señala el fin de un iterador. Capturada automáticamente por `for` loops.

---

## W

### Wrapper
Función que envuelve a otra, usualmente agregando comportamiento. Los decoradores crean wrappers.

```python
def wrapper(*args, **kwargs):
    print("Before")
    result = original(*args, **kwargs)
    print("After")
    return result
```

---

## Y

### yield
Keyword que convierte una función en generador. Produce un valor y pausa la ejecución.

```python
def gen():
    yield 1
    yield 2
    yield 3
```

### yield from
Delega a otro iterador, simplificando iteración anidada.

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
```

---

## 🔗 Referencias

- [Python Glossary](https://docs.python.org/3/glossary.html)
- [re — Regular expressions](https://docs.python.org/3/library/re.html)
- [functools — Higher-order functions](https://docs.python.org/3/library/functools.html)
- [itertools — Iterator functions](https://docs.python.org/3/library/itertools.html)
