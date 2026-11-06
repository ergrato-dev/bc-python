# Glosario — Semana 11

| Término | Definición |
|---|---|
| **`__add__` / `__radd__`** | Dunders de `a + b`: primero `a.__add__(b)`; si devuelve `NotImplemented`, `b.__radd__(a)` (la suma "por la derecha") |
| **`__bool__`** | Dunder de `if x:` y `bool(x)`. Si no existe, Python usa `__len__`; si tampoco, el objeto es verdadero |
| **`__contains__`** | Dunder de `v in x`. Si no existe, `in` recorre el objeto y compara con `==` |
| **`__eq__` / `__hash__`** | Dunders de `==` y de `hash()`. Al definir `__eq__`, Python pone `__hash__ = None`; objetos iguales deben tener el mismo *hash* |
| **`__getitem__`** | Dunder de `x[i]`. Con `x[1:3]` recibe un objeto `slice` |
| **`__iter__` / `__next__`** | `__iter__` da un iterador (`iter(x)`); `__next__` da el siguiente valor (`next(x)`) o lanza `StopIteration` |
| **`__len__`** | Dunder de `len(x)`; debe devolver un `int` mayor o igual que 0 |
| **`__repr__` / `__str__`** | Texto para quien programa (`repr`, listas, consola) y texto para quien lee (`print`, `str`, *f-strings*) |
| ***Data model*** | La lista de métodos especiales que Python llama con su sintaxis (`len`, `+`, `[]`, `for`...) |
| ***Dunder*** | *Double underscore*: método con dos guiones bajos a cada lado, como `__len__`. También "método mágico" o "especial" |
| **Expresión generadora** | Una *comprehension* entre paréntesis, `(x * x for x in datos)`, que crea un generador en lugar de una lista |
| **Función generadora** | Función con `yield` en el cuerpo; al llamarla devuelve un generador sin ejecutar nada |
| **Generador** | Iterador creado por una función generadora o una expresión generadora; calcula cada valor cuando se le pide |
| **Iterable** | Objeto que se puede recorrer: tiene `__iter__`, que devuelve un iterador nuevo. Se recorre muchas veces |
| **Iterador** | Cursor con `__next__` y un `__iter__` que devuelve `self`. Avanza una sola vez y se agota |
| **`itertools`** | Módulo con iteradores para tuberías: `islice`, `count`, `cycle`, `takewhile`, `chain`, `batched`... |
| **`NotImplemented`** | Constante que devuelve un operador que no sabe operar con el otro tipo, para que Python pruebe la operación al revés |
| **Perezoso (*lazy*)** | Que calcula cada valor solo cuando alguien lo pide. Lo contrario: ansioso (*eager*) |
| **Rebanada (*slice*)** | `x[inicio:fin:paso]`; llega a `__getitem__` como `slice(inicio, fin, paso)` |
| **Sobrecarga de operadores** | Dar significado a `+`, `*`, `<`... para una clase propia escribiendo sus dunders |
| **`StopIteration`** | Excepción con la que un iterador dice que no quedan valores; el `for` la captura y termina |
| **`total_ordering`** | Decorador de `functools` que deduce `<=`, `>` y `>=` a partir de `__eq__` y `__lt__` |
| **Tubería (*pipeline*)** | Cadena de generadores en la que cada etapa pide valores a la anterior, uno cada vez |
| **`yield`** | Entrega un valor y pausa la función generadora hasta el siguiente `next()` |
| **`yield from`** | Entrega, uno a uno, todos los valores de otro iterable |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
