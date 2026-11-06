# 03 · Hypothesis

⏱️ 55 min

## 🎯 Objetivos

- Distinguir un test de ejemplos de un test de propiedades.
- Escribir propiedades con `@given` y estrategias.
- Leer un contraejemplo encogido.
- Encontrar propiedades útiles: ida y vuelta, invariantes, "nunca falla".
- Declarar el dominio real de los datos y conocer los límites de los `float`.

---

## 1. Ejemplos frente a propiedades

Un test de **ejemplos** elige unos datos y comprueba un resultado concreto:

```python
def test_parse_record() -> None:
    assert parse_record("Norte;12,5") == ("Norte", 12.5)
```

Prueba lo que se te ocurrió. Y los bugs suelen estar justo en lo que no se te ocurrió. Tu Observatorio pasaba más de 300 tests con un bug desde la semana 2: `"Norte;abc"` tumbaba el programa. Ningún test probaba un valor roto con un `;` delante.

Un test de **propiedades** describe qué datos valen y qué debe cumplirse con **todos**:

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.lists(st.text() | st.builds("{};{}".format, st.text(), st.text())))
def test_process_lines_never_crashes_and_counts_every_data_line(lines: list[str]) -> None:
    rows, errors = process_lines(lines, "u", 10.0, 50.0)
    assert len(rows) + len(errors) == sum(is_data_line(line.strip()) for line in lines)
```

"Para cualquier lista de líneas, `process_lines` no lanza ninguna excepción, y cada línea de datos acaba en una fila o en un error". **Hypothesis** genera las listas, cien por defecto, y busca una que rompa la propiedad.

## 2. Estrategias

Una **estrategia** describe un conjunto de datos posibles. Están en `hypothesis.strategies`, que se importa como `st`:

| Estrategia | Genera |
|---|---|
| `st.integers(min_value=1, max_value=10)` | Enteros, con límites opcionales |
| `st.floats()` | Cualquier `float`: también `nan`, `inf`, `-0.0` y `1e308` |
| `st.floats(min_value=-1e6, max_value=1e6, allow_nan=False)` | Los números de tu dominio |
| `st.text()` | Cualquier texto Unicode, también vacío |
| `st.text(min_size=1, alphabet="abc;")` | Texto con límites |
| `st.none()` | Solo `None` |
| `st.lists(estrategia, min_size=1)` | Listas de lo que genere la otra estrategia |
| `st.sampled_from(["bajo", "medio", "alto"])` | Uno de esos valores |
| `a \| b` | Lo que genere `a` o lo que genere `b`: `st.none() \| st.floats()` |
| `st.builds(func, a, b)` | `func(x, y)` con `x` de `a` e `y` de `b`: `st.builds("{};{}".format, ...)` |
| `estrategia.filter(func)` | Solo lo que cumpla `func` |
| `estrategia.map(func)` | Lo generado, transformado: `st.floats().map(str)` |

`@given` recibe una estrategia por cada parámetro del test, en orden. Las estrategias son la **especificación** de la entrada: dicen qué datos son válidos.

## 3. El contraejemplo encogido

Cuando un ejemplo rompe la propiedad, Hypothesis no te lo enseña tal cual. Suele ser largo y feo, del estilo de `['Ω;\x1fñ', '', '7#']`. Primero lo **encoge** (*shrinking*): prueba versiones más simples (listas más cortas, textos más cortos, números más pequeños) y se queda con la más simple que **sigue fallando**. Lo que te enseña es el mínimo:

```
E       ValueError: could not convert string to float: ':'
E       Failing test case: test_process_lines_never_crashes_and_counts_every_data_line(
E           lines=['0;:'],
E       )
```

Una línea, una etiqueta de un carácter y un valor que no es un número. Mucho más fácil de entender que la primera.

![Hypothesis: la estrategia describe los datos; genera hasta 100 ejemplos; uno falla; lo encoge hasta ['0;:']; la carpeta .hypothesis lo guarda y la siguiente ejecución lo prueba primero](../0-assets/02-propiedad-y-encogimiento.svg)

Hypothesis guarda el contraejemplo en la carpeta `.hypothesis/`. En la siguiente ejecución lo prueba **primero**, así el fallo no desaparece por azar mientras lo arreglas. La carpeta va al `.gitignore`.

Si los cien ejemplos pasan, el test pasa. No demuestra que no haya bugs: solo que Hypothesis no encontró ninguno.

## 4. Qué propiedades escribir

La parte difícil no es Hypothesis, sino pensar qué se cumple **siempre**. Cinco patrones cubren casi todo:

| Patrón | Idea | En tu proyecto |
|---|---|---|
| **Ida y vuelta** | Escribir y leer da lo mismo | `Measurement.from_line(str(m)) == m` |
| **Nunca falla** | No lanza excepciones con datos de fuera | `process_lines` con cualquier lista de líneas |
| **Invariante** | Algo se conserva | `len(rows) + len(errors)` es el número de líneas de datos |
| **Límites** | El resultado está acotado | `min(values) <= median(values) <= max(values)` |
| **Oráculo** | Comparar con una versión lenta pero obvia | `moving_average` frente a `sum(ventana) / len(ventana)` |

```python
@given(LABELS, st.none() | NUMBERS)
def test_measurement_round_trips_through_str(label: str, value: float | None) -> None:
    measurement = Measurement(label, value)
    assert Measurement.from_line(str(measurement)) == measurement
```

No hace falta saber qué devuelve `str(measurement)` para cada caso: basta con saber que `from_line` lo deshace.

## 5. El dominio real

`st.floats()` genera **cualquier** `float`, y eso incluye números que tus datos nunca tendrán. Esta propiedad parece obvia:

```python
@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_median_is_between_min_and_max(values: list[float]) -> None:
    assert min(values) <= median(values) <= max(values)
```

Y falla, con algo como `values=[1e308, 1e308]`: `median` suma los dos del medio y divide entre 2, y `1e308 + 1e308` pasa del máximo de un `float` y da `inf`. ¿Es un bug? Para tu Observatorio, no: ninguna estación mide `1e308`. La solución es decir cuál es el dominio:

```python
# Números del dominio: finitos y de un tamaño razonable.
NUMBERS = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False)
```

Con límites, `allow_infinity` ya es falso. Hypothesis te obliga a decidir qué datos son válidos, y esa decisión es tan importante como el código. A veces el contraejemplo **sí** es un dato válido que no habías previsto, como `nan` en un archivo de medidas: entonces el que tiene que cambiar es el código.

## 6. `filter`, `assume` y `@example`

```python
# Etiquetas válidas: sin ";" y sin espacios a los lados.
LABELS = st.text(min_size=1).filter(lambda text: ";" not in text and text == text.strip())
```

`.filter` descarta lo que no cumple la condición. Si descarta casi todo, Hypothesis se rinde con un `FailedHealthCheck`: genera mejor lo que quieres desde el principio (`min_value`, `alphabet`...). `assume(condición)`, dentro del test, hace lo mismo cuando la condición depende de varios parámetros a la vez.

`@example(...)` añade un caso concreto que se prueba **siempre**, además de los generados:

```python
@given(st.lists(NUMBERS, min_size=1))
@example([12.5])
def test_median_is_between_min_and_max(values: list[float]) -> None:
    ...
```

Úsalo para el contraejemplo de un bug que ya arreglaste: así no vuelve.

## 7. Hypothesis y pytest

- **Fixtures**: un test con `@given` se ejecuta cien veces, pero sus fixtures de función se crean **una**. Hypothesis lo detecta y falla con `FailedHealthCheck` (`function_scoped_fixture`). Crea los datos dentro del test o con una estrategia.
- **Velocidad**: cada test con `@given` tarda lo que cien. `@settings(max_examples=500)` busca más, y `@settings(max_examples=20)`, menos.
- **Tiempo límite**: si un ejemplo tarda más de 200 ms, Hypothesis lo trata como un fallo (`DeadlineExceeded`), porque un test lento esconde problemas. `@settings(deadline=None)` lo quita.
- **Contenedores**: en Docker, `/app` no se puede escribir. La variable `HYPOTHESIS_STORAGE_DIRECTORY` lleva `.hypothesis/` a otra carpeta (paso 16 del proyecto).

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| La propiedad repite el código que prueba | `assert mean(v) == sum(v) / len(v)` no prueba nada | Busca una propiedad distinta: límites, ida y vuelta, invariantes |
| Fallos con `1e308`, `nan` o `-0.0` que no te importan | La estrategia es más amplia que tu dominio | `min_value`, `max_value`, `allow_nan=False` |
| `FailedHealthCheck` ... `filter_too_much` | El filtro descarta casi todo | Genera directamente lo que quieres |
| `FailedHealthCheck` ... `function_scoped_fixture` | `@given` con una fixture de función | Crea los datos dentro del test |
| `Flaky` | El resultado cambia con el mismo dato | El código depende de algo de fuera: la hora, el azar, un archivo |
| El contraejemplo cambia cada vez | Hay varias formas de romper la propiedad | Arregla la causa, no el ejemplo; después añade un `@example` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué encuentra un test de propiedades que un test de ejemplos no encuentra.
- [ ] Qué es una estrategia y cómo se combinan con `|`, `builds`, `filter` y `map`.
- [ ] Qué es el encogimiento y por qué ayuda.
- [ ] Cinco patrones de propiedades, con un ejemplo de tu proyecto para cada uno.
- [ ] Por qué hay que limitar los `float` al dominio real, y cuándo el contraejemplo es un bug de verdad.
- [ ] Qué guarda `.hypothesis/` y para qué sirve `@example`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Parametrize y marcas](02-parametrize-y-marcas.md) | **03 · Hypothesis** | [04 · Mocks y dobles](04-mocks-y-dobles.md) |
