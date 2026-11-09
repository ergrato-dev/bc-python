# 05 · pandas en un proyecto

⏱️ 50 min

## 🎯 Objetivos

- Darle a mypy los tipos de pandas con `pandas-stubs`, y saber qué comprueba y qué no.
- Devolver tipos de Python, no de NumPy, en lo que sale de tus funciones.
- Probar funciones que devuelven tablas con `pandas.testing` y con Hypothesis.
- Importar pandas solo en el comando que lo usa, como NumPy en la semana 23.
- Decidir entre `read_csv` y tu propio lector, y medir dónde gana pandas.

---

## 1. Tipos para pandas

NumPy trae sus tipos dentro. pandas, no: con mypy estricto, el primer `import pandas` falla.

```
m.py:1: error: Library stubs not installed for "pandas"  [import-untyped]
```

Los tipos están en un paquete aparte, `pandas-stubs`, que mantiene el propio equipo de pandas. mypy añade una pista para instalarlos sin uv: ignórala y añádelos con uv, solo para desarrollo, con la versión que corresponde a tu pandas:

```bash
uv add --dev pandas-stubs==3.1.0.261029
```

El número es la versión de pandas (`3.1.0`) más la fecha de publicación de los tipos (29 de octubre de 2026). En la imagen `runtime` no hace falta: los tipos solo los lee mypy.

Con los tipos, mypy sabe que `pd.read_csv` devuelve un `DataFrame`, que `frame["value"]` es una `Series` y que `frame.loc[mask]` es otro `DataFrame`. Lo que **no** sabe es qué columnas tiene tu tabla ni de qué tipo es cada una: para mypy, `frame["valro"]` es tan válido como `frame["valor"]`. Eso lo vigilan los tests.

---

## 2. Tipos de Python en la frontera

Lo que sale de pandas son tipos de NumPy, aunque parezcan de Python:

```python
counts = frame["label"].value_counts()
type(counts.iloc[0])                   # numpy.int64
json.dumps({"Norte": counts.iloc[0]})  # TypeError: Object of type int64 is not JSON serializable
type(frame["value"].max())             # numpy.float64
```

Igual que en la semana 23, la regla es: dentro del módulo, pandas; en lo que devuelve a quien no sabe de pandas, tipos de Python.

```python
def label_counts(frame: pd.DataFrame) -> dict[str, int]:
    counts = frame["label"].value_counts()
    return {str(label): int(count) for label, count in counts.items()}
```

Otras salidas a tipos de Python:

| Desde | Con |
|---|---|
| Una columna | `.tolist()`: `[12.5, 8.0, nan]`, de `float` |
| Un valor | `float(...)`, `int(...)`, `str(...)` |
| Las filas | `frame.itertuples(index=False)`: tuplas con un valor por columna |
| ¿Falta este valor? | `pd.isna(valor)`: sirve para NaN, `None` y `pd.NA` |

`test_label_counts_types_are_python` lo comprueba con `type(n) is int`. Con `isinstance` no bastaría siempre: `numpy.int64` no hereda de `int`, pero `numpy.float64` sí hereda de `float`, así que `isinstance(frame["value"].max(), float)` da `True` aunque sea de NumPy.

---

## 3. Probar tablas

Con tablas, `==` no sirve para un `assert`: compara celda a celda y devuelve **otra tabla** de `bool`. Y `assert tabla` da `ValueError: The truth value of a DataFrame is ambiguous`.

`pandas.testing` compara tablas enteras: valores, tipos de cada columna, nombres e índice, con NaN en el mismo sitio contando como iguales.

```python
import pandas as pd

pd.testing.assert_frame_equal(select(frame, labels=["Norte"]), expected)
pd.testing.assert_series_equal(frame["value"], expected_values)
```

Cuando falla, dice qué es distinto:

```
DataFrame.index are different

DataFrame.index values are different (100.0 %)
[left]:  RangeIndex(start=1, stop=7, step=3, name='position')
[right]: Index([0, 1], dtype='int64', name='position')
At positional index 0, first diff: 1 != 0
```

Aquí la selección conserva las posiciones 1 y 4 del archivo, y la tabla esperada se escribió con 0 y 1. Que el índice de la izquierda sea un `RangeIndex` (de 1 a 7, de 3 en 3) es un detalle de pandas: 1 y 4 siguen un paso fijo y no necesita guardarlos en una lista.

Y si lo distinto da igual en ese test, se lo dices: `check_index_type=False` (un `RangeIndex` frente a un `Index` de enteros con los mismos números), `check_dtype=False`, `check_exact=False` con `rtol` para coma flotante.

La mejor red, como en la semana 23, es **comparar lo nuevo con lo que ya tenías**. Tu Observatorio ya sabe clasificar, filtrar y contar sin pandas, y Hypothesis genera series al azar para comprobar que los dos caminos dicen lo mismo:

```python
@given(MEASUREMENTS)
def test_with_levels_agrees_with_scale_level(measurements: list[Measurement]) -> None:
    levels = with_levels(frame_of(Series(measurements)), SCALE)["level"].tolist()
    assert levels == [SCALE.level(m.value) for m in measurements]
```

Si te equivocas con `right=False`, Hypothesis encuentra enseguida un valor igual a 10 o a 50.

---

## 4. Importar solo donde hace falta

pandas tarda en cargarse más que NumPy, porque lo incluye:

```bash
uv run python -X importtime -c "import pandas" 2>&1 | tail -1
```

```
import time:       589 |     286874 | pandas
```

Casi 0,3 s, frente a 0,1 s de NumPy. Lo mismo que hiciste con `arrays.py`:

1. `core/frames.py` **no** se reexporta en `core/__init__.py`.
2. La CLI lo importa **dentro** del comando: `from observatorio.core import frames`.
3. Los tipos van en el bloque `if TYPE_CHECKING:`, que solo lee mypy:

```python
if TYPE_CHECKING:
    import pandas as pd

    from observatorio.core.arrays import Counts, Floats, Stats


def frame_text(frame: pd.DataFrame) -> str: ...
```

Desde Python 3.14 las anotaciones se evalúan solo cuando alguien las pide (PEP 649), así que `pd.DataFrame` en una firma no necesita pandas importado de verdad. Un test arranca otro proceso, importa `observatorio.cli` y comprueba que `'pandas' in sys.modules` es `False`.

---

## 5. `read_csv` o tu propio lector

`read_csv` está escrito en C, y se nota. Con las 100 000 medidas de la semana 22:

| Leer `perfil/grande.txt` | Tiempo |
|---|---|
| `Series.parse(open_file(path).lines())` | 103 ms |
| `pd.read_csv(path, sep=";", decimal=",", header=None, ...)` | 11 ms |

Diez veces más rápido. Y aun así, tu Observatorio sigue leyendo con `Series.parse` y convierte después con `frame_of`. ¿Por qué?

Por lo que viste en la teoría 02: `read_csv` no valida. El `medidas.csv` de tu proyecto tiene una línea sin `;` (`Sur 9,5`). `Series.parse` la aparta y `filtrar` escribe `error: línea 7: 'Sur 9,5'` y acaba con código 1. `read_csv`, en cambio, la convierte en una fila con la etiqueta `"Sur 9,5"` y el valor vacío, y si hubiera un valor como `19,8 C`, toda la columna pasaría a ser texto. Tu proyecto ya tiene un lector que valida: lo reutilizas y pagas 11 ms de conversión.

`read_csv` es la elección cuando los archivos son enormes y vienen de una fuente en la que confías, o cuando los validas después con reglas sobre la tabla entera (cuántos NaN, rangos, tipos). En la semana 26 verás Polars y Parquet, pensados para ese caso.

---

## 6. Dónde gana pandas y dónde no

Ejercicio 04, 100 000 medidas, el mejor de 5 intentos:

| Operación | Python puro | pandas |
|---|---|---|
| Convertir la lista de medidas en tabla | — | 13,5 ms |
| Niveles | 6,4 ms (`classify` en una comprensión) | 1,6 ms (`pd.cut`) |
| Filtrar por etiqueta y valor | **2,3 ms** (comprensión) | 4,2 ms (máscaras) |
| Contar etiquetas | **4,1 ms** (`Counter`) | 5,9 ms (`value_counts`) |

Con **números**, pandas gana, como NumPy. Con **texto**, pierde o empata: comparar 100 000 cadenas es trabajo de Python también dentro de pandas. Y convertir la serie a tabla cuesta más que todo lo demás junto.

Si no es por velocidad, ¿para qué pandas? Por lo que se escribe:

- un filtro de tres condiciones es una línea, y se lee como la pregunta;
- leer y escribir CSV, Excel, Parquet o SQL es una línea;
- la tabla se mira (`info`, `describe`) antes de usarla;
- y es lo que esperan scikit-learn, matplotlib, seaborn y casi toda la fase 4.

Tiene un precio fuera del tiempo: la imagen `runtime` de tu proyecto pasa de 395 MB a 508 MB.

---

## 7. Lo que viene

La semana 25 sigue con pandas:

| Esta semana | La que viene |
|---|---|
| `value_counts` por etiqueta | `groupby`: cualquier medida por grupo, como tu `group_means` de la semana 23 |
| Una tabla | `merge` y `concat`: juntar tablas por una columna |
| `dia` como entero | Fechas de verdad: `to_datetime`, índices de tiempo y `resample` |

---

## 8. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| mypy: `Library stubs not installed for "pandas"` | pandas no trae sus tipos | `uv add --dev pandas-stubs==...` con la versión de tu pandas |
| Instalar los tipos como dice la pista de mypy | Fuera de uv: no quedan en `uv.lock` | `uv add --dev` |
| Devolver `numpy.int64` o `numpy.float64` desde el módulo | `json.dumps` falla y los tests de tipo también | `int()`, `float()` o `tolist()` en la frontera |
| `assert df1 == df2` | `==` da una tabla; `assert` de una tabla, `ValueError` | `pd.testing.assert_frame_equal` |
| `import pandas` al principio de la CLI | Todos los comandos pagan 0,3 s | Importarlo dentro del comando; tipos en `TYPE_CHECKING` |
| Cambiar tu lector por `read_csv` porque es más rápido | Pierdes la validación línea a línea | Mídelo, y valida la tabla si lo cambias |

---

## ✅ Qué debes saber al terminar

- [ ] Por qué hace falta `pandas-stubs`, cómo se añade y qué no comprueba mypy.
- [ ] Qué tipos salen de pandas, y cómo devolver tipos de Python.
- [ ] Comparar tablas con `assert_frame_equal` y sus opciones `check_*`, y comparar con Hypothesis contra el código que ya tenías.
- [ ] Las tres cosas que mantienen pandas fuera del arranque de la CLI, y el test que lo vigila.
- [ ] Cuándo usar `read_csv` y cuándo tu propio lector, y dónde gana pandas con tus números.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Ordenar, contar y copy-on-write](04-ordenar-contar-y-copy-on-write.md) | **05 · pandas en un proyecto** | [Ejercicio 01 · Series, índice y tipos](../2-practicas/ejercicio-01-series-indice-y-tipos/README.md) |
