# 05 · NumPy en un proyecto

⏱️ 45 min

## 🎯 Objetivos

- Anotar funciones que reciben y devuelven arrays con `NDArray`, y pasar mypy estricto.
- Devolver tipos de Python en la frontera de tu código, no escalares de NumPy.
- Probar código numérico con tolerancia, con NaN y sin avisos, y comparar lo nuevo con lo viejo con Hypothesis.
- Importar NumPy solo en el comando que lo usa, y probar que el resto no lo carga.
- Medir dónde gana NumPy en tu Observatorio, y dónde **no**.

---

## 1. Tipos para arrays

NumPy trae sus propias anotaciones de tipos: mypy las entiende sin instalar nada más. La que vas a usar casi siempre es `NDArray[dtype]`, "un array con elementos de este tipo":

```python
import numpy as np
from numpy.typing import NDArray

# Un array de números de coma flotante de 64 bits, el tipo de casi todo lo que sigue.
Floats = NDArray[np.float64]
# Un array de enteros del tamaño de un índice: conteos y posiciones.
Counts = NDArray[np.intp]


def zscores(values: Floats) -> Floats: ...
def outliers(values: Floats, threshold: float) -> Counts: ...
def labels_array(series: Series) -> NDArray[np.str_]: ...
```

Los **alias** (`Floats`, `Counts`) son los de la semana 13: un nombre corto para un tipo largo, que además dice qué significa. `np.intp` es el entero que NumPy usa para posiciones y conteos (`int64` en una máquina de 64 bits); es lo que devuelven `np.flatnonzero` y `np.histogram`.

`NDArray` dice el `dtype`, pero no la forma: para mypy, un array de una dimensión y una tabla son el mismo tipo. La forma la documentas en el docstring y la compruebas en los tests.

mypy te avisa cuando mezclas tipos de array. En el proyecto, pasar los conteos de `np.histogram` a una función que pide `Floats` da:

```
error: Argument 1 to "histogram_lines" has incompatible type "ndarray[tuple[Any, ...], dtype[signedinteger[_32Bit | _64Bit]]]"; expected "ndarray[tuple[Any, ...], dtype[float64]]"  [arg-type]
```

El mensaje es largo, pero se lee por el final: esperaba `float64` y le das un entero con signo. La solución es el alias correcto, `Counts`.

---

## 2. Tipos de Python en la frontera

Un elemento sacado de un array no es un `float` de Python, sino un **escalar de NumPy**:

```python
type(np.float64(1.5) + 1)   # <class 'numpy.float64'>
```

`np.float64` hereda de `float` y casi siempre se comporta igual, pero no del todo: desde NumPy 2, su `repr` es `np.float64(1.5)`, no `1.5`, y lo ves en los mensajes de los tests, en los registros y en un `print` de una tupla (`(np.int64(2), np.int64(1))` en el ejercicio 02). Y `np.int64` no hereda de `int`: `json.dumps` no lo sabe escribir.

La regla del Observatorio: los arrays viven **dentro** de `core/arrays.py`; lo que sale hacia el resto del programa son tipos de Python. Por eso `stats_of` convierte cada campo con `float(...)` e `int(...)`, y `group_means` devuelve `dict(zip(names.tolist(), means.tolist()))`: `tolist()` convierte cada elemento en su tipo de Python.

```python
@dataclass(frozen=True)
class Stats:
    """El resumen de los valores presentes de una serie, los que no son NaN."""

    count: int
    missing: int
    mean: float
    ...
```

Así el resto del código (la CLI, la API, los tests) no necesita saber que debajo hay NumPy.

---

## 3. Probar código numérico

### Con tolerancia

Dos cálculos equivalentes pueden diferir en el último decimal (teoría 01). Las comparaciones de tus tests no pueden ser `==`:

| Herramienta | Para qué |
|---|---|
| `np.testing.assert_allclose(actual, esperado)` | Arrays de `float`, con tolerancia relativa de 1e-7. Trata NaN en la misma posición como iguales |
| `np.testing.assert_array_equal(actual, esperado)` | Arrays que deben ser idénticos: enteros, texto, `bool`, o `float` exactos. También acepta NaN en la misma posición |
| `pytest.approx(esperado)` | Un número, o los valores de un diccionario: `{"Norte": pytest.approx(30.7), "Sur": 8.0}` |
| `.tolist() == [...]` | Posiciones y conteos: enteros exactos, y el fallo se lee mejor |

Cuando falla, `assert_allclose` dice cuántos elementos y cuánto se separan:

```
Not equal to tolerance rtol=1e-07, atol=0

Mismatched elements: 1 / 1 (100%)
```

Y NaN no es igual a sí mismo (teoría 04): `assert (values == expected).all()` falla si hay NaN, aunque estén donde deben. Las funciones de `np.testing` lo saben.

### Sin avisos

Un test que pasa aunque el código avise no demuestra que el caso especial está tratado. Convierte los avisos en errores dentro del test:

```python
with warnings.catch_warnings():
    warnings.simplefilter("error")
    result = zscores(values)
```

Si `zscores` divide por 0, el `RuntimeWarning` se convierte en una excepción y el test falla. En el proyecto, un mutante que cambia `if std == 0:` por `if present.size == 0:` solo lo mata este test: con valores iguales, el resultado sigue siendo NaN, pero ahora con un aviso.

### Comparar lo nuevo con lo viejo

Tu Observatorio ya calcula la mediana (`trends.median`) y la media por etiqueta (`Series.means`) en Python puro, con sus tests. La forma más fuerte de probar la versión de NumPy es pedirle a Hypothesis (semana 14) cientos de casos y comprobar que las dos dan lo mismo:

```python
@given(MEASUREMENTS)
def test_group_means_agree_with_series_means(measurements: list[Measurement]) -> None:
    series = Series(measurements)
    means = group_means(labels_array(series), values_array(series))
    expected = series.means()
    assert means.keys() == expected.keys()
    for label, mean in expected.items():
        assert means[label] == pytest.approx(mean, abs=1e-6)
```

Hypothesis encuentra casos en los que no pensarías. Con `st.floats` en la prueba de que las z tienen media 0 y desviación 1, encontró `[0.0, 5e-324]`: dos números tan juntos que su desviación es un número **subnormal**, demasiado pequeño para dividir por él sin dar `inf`. No es un fallo de `zscores`, sino de la propiedad: con datos así no se cumple. El test usa enteros, con un comentario que lo explica. Leer el ejemplo de Hypothesis y decidir si el fallo está en el código o en lo que pides es parte del trabajo.

---

## 4. Importar solo donde hace falta

En la semana 22 mediste que importar NumPy cuesta alrededor de 0,1 s, más de lo que ahorraba en `informe`. Esta semana NumPy entra en el proyecto, pero solo para el comando nuevo, `estadisticas`. Que los demás no lo paguen exige tres cosas:

1. `core/arrays.py` **no** se reexporta en `core/__init__.py`. Si lo hiciera, `from observatorio.core import Series` cargaría NumPy.
2. La CLI lo importa **dentro** del comando, como `servir` importa uvicorn desde la semana 20:

   ```python
   @app.command()
   def estadisticas(...) -> None:
       # Importar aquí: NumPy tarda alrededor de 0,1 s en cargarse, y solo lo usa este comando.
       from observatorio.core import arrays
   ```

3. Las funciones auxiliares de la CLI que anotan `Stats` o `Counts` los importan **solo para mypy**:

   ```python
   from typing import TYPE_CHECKING

   if TYPE_CHECKING:
       from observatorio.core.arrays import Counts, Floats, Stats
   ```

   `TYPE_CHECKING` es `False` al ejecutar y `True` para mypy. Desde Python 3.14, las anotaciones no se evalúan al definir la función, sino cuando alguien las pide (PEP 649): `def stats_table(stats: Stats, unit: str)` funciona aunque `Stats` no exista en tiempo de ejecución. Typer sí lee las anotaciones de los **comandos**, así que los tipos de NumPy no pueden aparecer en sus parámetros; en las funciones auxiliares, sí.

¿Cómo pruebas que algo **no** se importa? En otro proceso, porque en el de pytest otros tests ya lo habrán importado:

```python
code = "import sys, observatorio.cli; print('numpy' in sys.modules)"
result = subprocess.run([sys.executable, "-c", code], check=False, capture_output=True, text=True)
assert result.stdout == "False\n"
```

Es el mismo patrón que `test_core_does_not_import_fastapi` de la semana 20. Si alguien sube el `import` al principio de `cli.py`, falla.

---

## 5. Dónde gana y dónde no

Medido en el proyecto con 100 000 medidas (paso 9):

| Operación | Python puro | NumPy |
|---|---|---|
| Media, desviación y mediana | 52 ms (`statistics` y `median`) | 1,6 ms (`stats_of`, con los cuartiles) |
| Puntuaciones z | 44 ms | 0,2 ms |
| Media por etiqueta | **7,8 ms** (`Series.means`) | 11,2 ms (`group_means`) |
| Convertir la serie | — | 4,1 ms (`values_array`) y 8,8 ms (`labels_array`) |

Con números, NumPy gana por 30 y por 200. Con **texto**, pierde: `group_means` usa `np.unique`, que **ordena** las 100 000 etiquetas para agruparlas, y comparar texto es lento; el diccionario de `Series.means` las agrupa en una pasada. NumPy brilla con números de un solo tipo; con etiquetas, los diccionarios de la semana 5 siguen siendo buenos. pandas resuelve esto guardando las etiquetas repetidas como **categorías**: enteros, y una tabla aparte con los textos (semana 25).

Y lo de siempre, por Amdahl: `estadisticas` tarda 0,84 s en total, y la mayor parte es arrancar Python, importar y analizar el texto. Las operaciones de NumPy son unos pocos milisegundos. El comando no es rápido **por** NumPy; NumPy hace que su parte numérica no cueste casi nada y se escriba en una línea.

NumPy también pesa en disco: la imagen `runtime` pasa de 301 a 395 MB, porque trae su propia biblioteca de álgebra lineal (OpenBLAS) compilada. Es el precio de entrar en la fase 4, y por eso esta semana la mides.

---

## 6. El puente a pandas

La semana que viene usas pandas. Casi todo lo de esta semana sigue valiendo:

| NumPy | pandas |
|---|---|
| `values_array(series)` con NaN | Una columna de un `DataFrame`: un array de NumPy con un índice |
| `np.nanmean`, quitar NaN con una máscara | `df["valor"].mean()` salta los NaN por defecto |
| Máscaras: `values[values > 50]` | `df[df["valor"] > 50]`, la misma idea |
| `group_means` con `np.unique` y `np.bincount` | `df.groupby("etiqueta")["valor"].mean()` |
| `std()` con `ddof=0` | `std()` con `ddof=1`: ojo |
| `np.histogram`, `np.percentile` | `df["valor"].describe()`, `.quantile()` |

Lo que escribes a mano esta semana es lo que pandas hace por debajo. Cuando un resultado de pandas te sorprenda, sabrás qué preguntarle.

---

## 7. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| Devolver `np.float64` o arrays fuera del módulo | `repr` raro, `json` que falla, NumPy en todo el programa | `float()`, `int()`, `.tolist()` en la frontera |
| `assert a == b` con arrays | Da un array de `bool`, no un `bool`: `ValueError` o un test que no prueba nada | `np.testing.assert_allclose` o `assert_array_equal` |
| Tests que pasan con avisos | El caso especial no está tratado, solo silenciado | `warnings.simplefilter("error")` dentro del test |
| Reexportar el módulo de NumPy en `core/__init__.py` | Todos los comandos pagan su importación | Importarlo solo donde se usa |
| Tipos de NumPy en los parámetros de un comando de Typer | Typer evalúa esas anotaciones y no encuentra el tipo | Solo en las funciones auxiliares, con `TYPE_CHECKING` |
| Dar por hecho que NumPy siempre gana | Con texto o pocos datos, pierde | Mide, como en la semana 22 |
| Creer a Hypothesis sin leer el ejemplo | A veces el fallo está en la propiedad, no en el código | Lee el caso mínimo y decide; si cambias el test, explica por qué |

---

## ✅ Qué debes saber al terminar

- [ ] Anotar con `NDArray[np.float64]` y alias como `Floats` y `Counts`, y leer un error de tipos de arrays.
- [ ] Por qué lo que sale de tu módulo son tipos de Python, y cómo convertir.
- [ ] Probar con `assert_allclose`, `assert_array_equal`, `pytest.approx`, avisos como errores y Hypothesis contra la versión vieja.
- [ ] Importar NumPy solo en el comando que lo usa, con `TYPE_CHECKING` para los tipos, y probarlo en otro proceso.
- [ ] Dónde gana NumPy en tu Observatorio, dónde pierde, y cuánto pesa.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Datos que faltan, estadística y azar](04-datos-que-faltan-estadistica-y-azar.md) | **05 · NumPy en un proyecto** | [Ejercicio 01 · Arrays y dtypes](../2-practicas/ejercicio-01-arrays-y-dtypes/README.md) |
