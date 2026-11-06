# 03 · Context managers

⏱️ 40 min

## 🎯 Objetivos

- Explicar qué hace `with` por dentro y por qué cierra también cuando hay errores.
- Abrir varios recursos en un solo `with`.
- Escribir un context manager propio con `contextlib.contextmanager`.
- Usar `contextlib.suppress` y saber cuándo no usarlo.

---

## 1. El problema: abrir y olvidar cerrar

Sin `with`, abrir un archivo es un par de llamadas que hay que emparejar a mano:

```python
file = path.open("w", encoding="utf-8")
file.write(text)      # si esto falla...
file.close()          # ...esto no se ejecuta
```

Si `write` lanza una excepción, `close` nunca llega. La versión segura necesita un `try` con `finally`:

```python
file = path.open("w", encoding="utf-8")
try:
    file.write(text)
finally:
    file.close()
```

Cuatro líneas de ceremonia por archivo, y basta olvidarlas una vez. `with` las escribe por ti.

## 2. Qué hace `with`

```python
with path.open("w", encoding="utf-8") as file:
    file.write(text)
```

El objeto que va detrás de `with` es un **context manager**: un objeto que sabe qué hacer al **entrar** en el bloque y qué hacer al **salir**. Python llama a su método `__enter__` al entrar, y lo que devuelve va a la variable de `as`. Al salir del bloque llama a `__exit__`, salga como salga: al terminar, con un `return` o con una excepción. Es el `try` y `finally` de arriba, empaquetado.

| Context manager | Al entrar | Al salir |
|---|---|---|
| `path.open(...)` | Abre el archivo | Lo cierra |
| Una conexión a PostgreSQL (semana 19) | Abre una transacción | La confirma, o la deshace si hubo error |
| `pytest.raises(ValueError)` | Empieza a vigilar | Falla el test si **no** saltó la excepción |
| `contextlib.suppress(...)` | — | Se traga la excepción indicada |

Después del bloque, la variable sigue existiendo, pero el archivo está cerrado: `file.write(...)` fuera del `with` da `ValueError: I/O operation on closed file.`

## 3. Varios a la vez

Para leer de un archivo y escribir en otro, un solo `with` con los dos, separados por comas:

```python
with (
    source.open(encoding="utf-8") as reader,
    target.open("w", encoding="utf-8") as writer,
):
    for line in reader:
        writer.write(line.upper())
```

Los paréntesis permiten partirlo en varias líneas. Al salir se cierran en orden inverso: primero `writer`, después `reader`.

## 4. Tu propio context manager

El módulo `contextlib` convierte una función generadora en context manager con el decorador `@contextmanager`. Lo que va antes del `yield` es la entrada, y lo que va después, la salida:

```python
import time
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def timer(name: str) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"{name}: {time.perf_counter() - start:.3f} s")


with timer("ordenar"):
    sorted(range(1_000_000), reverse=True)
# ordenar: 0.021 s
```

El `yield` es el momento en que corre el cuerpo del `with`. El `try` y `finally` alrededor del `yield` hacen que el tiempo se escriba también si el cuerpo lanza una excepción, y la excepción sigue subiendo. Sin ese `finally`, un error dentro del `with` se saltaría la salida. Si el `yield` da un valor (`yield conexion`), ese valor va a la variable de `as`.

Una línea de `@contextmanager` es un **decorador**: una función que transforma la función de debajo. Los verás a fondo en la semana 12; de momento basta con saber usar este. El tipo de retorno `Iterator[None]` dice que la función produce un único valor, `None`, en el `yield`.

## 5. `suppress`: ignorar un error a propósito

A veces un error concreto es justo lo que esperas y no hay nada que hacer con él. Por ejemplo, borrar un temporal que quizá ya no existe:

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    Path("resumen.tmp").unlink()
```

Es lo mismo que `try` con `except FileNotFoundError: pass`, en dos líneas y con la intención a la vista. Para este caso concreto, `Path.unlink(missing_ok=True)` es aún más corto. La regla de la teoría 02 sigue en pie: suprime solo un tipo concreto y solo cuando ignorarlo es la respuesta correcta.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `ValueError: I/O operation on closed file.` | Usaste el archivo fuera del `with` | Mueve ese código dentro del bloque |
| El archivo escrito sale vacío o cortado | Abriste sin `with` y no cerraste | Usa `with` |
| Tu context manager no hace su salida cuando hay error | Falta `try` y `finally` alrededor del `yield` | `try: yield` y la salida en `finally` |
| `TypeError: 'generator' object does not support the context manager protocol (missed __exit__ method)` | Falta `@contextmanager` encima de la función | Añade el decorador |
| `suppress(Exception)` esconde fallos que no esperabas | Suprimir una familia entera | Un tipo concreto |

## ✅ Qué debes saber al terminar

- [ ] Qué hace `with` al entrar y al salir, y por qué equivale a `try` con `finally`.
- [ ] Cómo abrir dos archivos en un solo `with`.
- [ ] Cómo escribir un context manager con `@contextmanager`, y por qué el `yield` va dentro de un `try`.
- [ ] Para qué sirve `suppress` y cuándo no usarlo.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Excepciones](02-excepciones.md) | **03 · Context managers** | [04 · CSV](04-csv.md) |
