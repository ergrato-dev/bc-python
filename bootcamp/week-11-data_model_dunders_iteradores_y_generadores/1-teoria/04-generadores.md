# 04 · Generadores

⏱️ 50 min

## 🎯 Objetivos

- Escribir funciones generadoras con `yield` y explicar cómo se pausan.
- Usar expresiones generadoras en lugar de listas cuando no hace falta guardar los datos.
- Delegar en otro iterable con `yield from`.
- Prever cuándo se ejecuta el código de un generador, también el que lanza errores o cierra archivos.

---

## 1. `yield`: una función que se pausa

Escribir un iterador como clase (teoría 03) obliga a guardar el estado en `self` y a lanzar `StopIteration` a mano. Un **generador** hace lo mismo con una función normal que, en lugar de `return`, usa `yield`:

```python
from collections.abc import Iterator


def countdown(start: int) -> Iterator[int]:
    while start > 0:
        yield start
        start -= 1


list(countdown(3))     # [3, 2, 1]
```

Una función con `yield` en el cuerpo es una **función generadora**. Al llamarla, **no ejecuta nada**: devuelve un objeto generador, que es un iterador.

1. El primer `next()` ejecuta desde el principio hasta el primer `yield`, entrega el valor y **pausa** la función, con sus variables intactas.
2. Cada `next()` siguiente reanuda justo después del `yield` donde se paró.
3. Cuando la función termina (llega al final o a un `return`), el generador lanza `StopIteration`.

```python
gen = countdown(2)     # no se ha ejecutado ni una línea
next(gen)              # ejecuta hasta el primer yield: 2
next(gen)              # resta 1, vuelve al while: 1
next(gen)              # sale del while y termina: StopIteration
```

Es la `Countdown` de la teoría 03 en cuatro líneas: el estado son las variables locales (`start`) y `StopIteration` llega sola.

### Generadores con estado

Las variables locales sobreviven entre un `yield` y el siguiente. Es lo que usa `running_mean` en tu proyecto:

```python
def running_mean(values: Iterable[float]) -> Iterator[float]:
    total = 0.0
    for count, value in enumerate(values, start=1):
        total += value
        yield total / count


list(running_mean([10.0, 20.0, 30.0]))     # [10.0, 15.0, 20.0]
```

Un generador, como cualquier iterador, **se gasta**: tras una vuelta, `list(gen)` da `[]`.

---

## 2. Expresiones generadoras

Una *comprehension* con paréntesis en lugar de corchetes es una **expresión generadora**:

```python
squares_list = [n * n for n in range(1_000_000)]    # una lista: ~8 MB de referencias
squares_gen = (n * n for n in range(1_000_000))     # un generador: ~200 bytes
```

La lista calcula y guarda el millón de valores **antes** de que los uses. El generador calcula cada valor cuando se lo piden y no guarda ninguno. Si solo vas a recorrerlos una vez (sumarlos, buscar el máximo, escribirlos), el generador hace lo mismo con una memoria que no crece con los datos.

Cuando es el único argumento de una función, los paréntesis sobran:

```python
total = sum(v * v for v in values)
any(v > 50 for v in values)            # para en el primero que cumple
```

`any` y `all` paran en cuanto saben la respuesta: con una expresión generadora, los valores que quedan **ni se calculan**.

| Usa una lista cuando... | Usa un generador cuando... |
|---|---|
| Vas a recorrer los datos más de una vez | Los recorres una sola vez |
| Necesitas `len()`, índices o rebanadas | Te basta con ir de uno en uno |
| Son pocos datos y quieres verlos al depurar | Son muchos, o no terminan nunca |

---

## 3. `yield from`

`yield from iterable` entrega, uno a uno, todos los valores de otro iterable:

```python
def all_values(groups: dict[str, list[float]]) -> Iterator[float]:
    for values in groups.values():
        yield from values          # = for value in values: yield value
```

Tu `Series.__iter__` lo usa: `yield from self.measurements`. Como es una función con `yield`, cada `iter(serie)` crea un generador **nuevo**: la serie es un iterable que se recorre las veces que quieras, sin escribir una clase iterador aparte.

---

## 4. Cuándo se ejecuta el código de un generador

Como el cuerpo no empieza hasta el primer `next()`, **todo** llega tarde, también los errores:

```python
def iter_lines(path: Path) -> Iterator[str]:
    try:
        with path.open(encoding="utf-8") as file:
            for line in file:
                yield line.rstrip("\n")
    except FileNotFoundError as error:
        raise DataFileError(f"no existe el archivo {path}") from error


lines = iter_lines(Path("no-existe.txt"))    # no falla: no se ha abierto nada
next(lines)                                  # DataFileError: no existe el archivo no-existe.txt
```

Es bueno (crear el generador es gratis) y es una trampa (el error sale lejos de donde escribiste la ruta). Si necesitas que una ruta mala falle en el momento, compruébala antes, fuera del generador.

### `with` dentro de un generador

El archivo se abre en el primer `next()` y se cierra cuando el `for` de dentro termina. ¿Y si quien recorre se detiene a mitad, con `islice` o un `break`? Cuando el generador ya no se usa, Python lo cierra con `gen.close()`, que lanza `GeneratorExit` en el `yield` donde estaba pausado; el `with` sale y cierra el archivo. Para cerrarlo en un momento exacto, recórrelo dentro de otro `with`: `with contextlib.closing(iter_lines(ruta)) as lines:`.

### `return` en un generador

Un `return valor` dentro de un generador no lo recibe el `for`: termina el generador y el valor viaja en `StopIteration.value`. Casi nunca lo necesitarás; si lo usas, el tipo es `Generator[Da, Recibe, Devuelve]` en lugar de `Iterator[Da]`:

```python
def numbered(lines: list[str]) -> Generator[str, None, str]:
    yield from (f"{n}: {line}" for n, line in enumerate(lines, start=1))
    return "sin más líneas"
```

---

## 5. Tipos de un generador

| Anotación | Cuándo |
|---|---|
| `Iterator[T]` | Lo normal: el generador da valores de tipo `T` |
| `Generator[T, None, None]` | Lo mismo, escrito largo |
| `Generator[T, None, R]` | El generador hace `return` con un valor de tipo `R` |
| `Iterable[T]` | También válido, pero promete menos: no se podría llamar a `next()` |

Anotar un generador con `-> list[T]` es un error: `The return type of a generator function should be "Generator" or one of its supertypes`.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| La función no imprime nada al llamarla | Tiene `yield`: devuelve un generador sin ejecutarse | Recórrelo (`for`, `list`, `next`) |
| La segunda vuelta sale vacía | El generador se gastó | Vuelve a llamar a la función, o guarda una lista |
| `TypeError: 'generator' object is not subscriptable` | `gen[0]` | `next(gen)` o `itertools.islice` |
| `TypeError: object of type 'generator' has no len()` | `len(gen)` | Un generador no sabe cuántos dará: `len(list(gen))` si de verdad lo necesitas |
| El error de una ruta mala sale tarde y lejos | El cuerpo del generador corre en el primer `next()` | Comprueba la ruta antes, o acepta que falle al recorrer |
| `mypy`: `The return type of a generator function should be "Generator"...` | Anotaste `-> list[...]` | `-> Iterator[...]` |
| `mypy`: `No return value expected` | `return valor` en un generador anotado con `Iterator[...]` | `Generator[T, None, R]`, o quita el valor del `return` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué devuelve una función con `yield` al llamarla y qué pasa en cada `next()`.
- [ ] La diferencia entre `[x for ...]` y `(x for ...)` y cuándo usar cada una.
- [ ] Qué hace `yield from` y por qué con él `Series.__iter__` crea un generador nuevo cada vez.
- [ ] Por qué `iter_lines(ruta_mala)` no falla hasta el primer `next()`.
- [ ] Cómo se anota un generador.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Iteradores](03-iteradores.md) | **04 · Generadores** | [05 · Pipelines perezosos](05-pipelines-perezosos.md) |
