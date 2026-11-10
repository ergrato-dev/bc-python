# 05 · pandas II en un proyecto

⏱️ 50 min

## 🎯 Objetivos

- Repartir el código nuevo entre `core` y la CLI sin que la CLI cargue pandas al arrancar.
- Escribir `groupby` y `rename_axis` de forma que mypy, con `pandas-stubs`, sepa qué tipo devuelven.
- Probar resúmenes, cruces y series de tiempo con `pandas.testing`, incluidos el orden, los tipos de una tabla vacía y la frecuencia del índice.
- Comparar con Hypothesis lo nuevo con lo que ya tenías, sin caer en una diferencia de orden que no es un error.
- Usar `datetime` y `timedelta` de Python en la frontera de tu código, y convertir duraciones escritas por una persona.
- Medir qué gana pandas en cada resumen, y dónde se va el tiempo de un comando.

---

## 1. Dónde vive cada pieza

En la semana 24 pusiste en `core/frames.py` todo lo que convierte la serie en tabla y la elige. Esta semana añades `core/summaries.py`, que trabaja **sobre** esas tablas:

| Archivo | Qué sabe hacer | Qué importa |
|---|---|---|
| `core/frames.py` | Pasar una `Series` a `DataFrame`, niveles, filtrar, ordenar, contar, escribir | pandas, `model` |
| `core/summaries.py` | Resumir por etiqueta, comparar dos resúmenes, poner tiempo, resumir por periodos | pandas |
| `cli.py` | Leer el archivo, llamar a las dos y escribir la tabla en español | pandas **solo** dentro de los comandos |

`summaries.py` no importa nada del Observatorio: recibe y devuelve `DataFrame`. Es más fácil de probar y de reutilizar: la API de la semana 20 podría usarlo sin pasar por la CLI.

Como `frames`, no se reexporta en `core/__init__.py`. Cualquier `from observatorio.core import ...` lo cargaría, y con él pandas, en todos los comandos. El test `test_importing_the_cli_does_not_load_pandas` de la semana 24 lo sigue vigilando.

La traducción al español vive en la CLI, en un solo diccionario, `NAMES`, que usa `frame_text` para las columnas **y** para los nombres de los índices. `core` habla inglés; la terminal, español.

---

## 2. Que mypy sepa qué devuelve

pandas no trae tipos; `pandas-stubs` sí (teoría 05 de la semana 24). Los *stubs* describen cada método, pero no siempre saben lo que tú sabes. Dos casos de esta semana:

**`agg` con nombre sobre una columna.** Las dos formas dan la misma tabla:

```python
frame.groupby("label")["value"].agg(count="count", mean="mean")
frame.groupby("label").agg(count=("value", "count"), mean=("value", "mean"))
```

Pero para los *stubs*, la primera devuelve una `Series`, y mypy protesta al devolverla como `DataFrame`:

```
error: Incompatible return value type (got "Series[Any]", expected "DataFrame")  [return-value]
```

La segunda, sobre la tabla y con tuplas, está tipada como `DataFrame`. Es la que usa `summary`. Cuando mypy y la ejecución no coinciden, busca otra forma de escribirlo antes que un `# type: ignore`.

**`rename_axis` con un diccionario.** Los *stubs* piden `dict[str | int, str]`, y un `dict[str, str]` no les vale (un diccionario no admite claves de otro tipo, aunque sean "más"):

```
error: Argument "index" to "rename_axis" of "DataFrame" has incompatible type "dict[str, str]"; expected "str | Sequence[str] | dict[str | int, str] | Callable[..., Any] | None"  [arg-type]
```

La solución es anotar el diccionario con el tipo que piden, y dejar un comentario de por qué:

```python
NAMES: dict[str | int, str] = {"label": "etiqueta", "count": "medidas", ...}
```

---

## 3. Probar resúmenes

`pd.testing.assert_frame_equal` compara valores, tipos, índice y columnas (semana 24). Con los resultados de esta semana, cuatro cosas más que vigilar:

- **El orden de las filas.** `groupby` ordena por defecto; con `sort=False`, no. `merge` con `outer` ordena siempre. Un test con la tabla esperada escrita a mano deja el orden escrito.
- **Los tipos de una tabla vacía.** Un `DataFrame` creado con listas vacías tiene columnas `float64`; el resumen de una serie vacía tiene `count` y `missing` `int64`. La función `summary_table` de los tests convierte los tipos para que la tabla esperada vacía coincida.
- **La frecuencia del índice.** Un índice de `date_range` o de `resample` lleva `freq` (`3h`); uno creado a mano con `pd.DatetimeIndex([...])`, no. `assert_frame_equal` lo compara: `Attribute "freq" are different`. Crea el esperado con `date_range`, o pasa `check_freq=False` si la frecuencia no importa.
- **El nombre de las columnas.** `pivot` deja `columns.name = "label"`. La tabla esperada necesita lo mismo: `rename_axis(columns="label")`.

Y una lección de Hypothesis. El test que compara `summary` con `Series.means` de la semana 09 falló así:

```
assert ['Norte', 'Sur'] == ['Sur', 'Norte']
Failing test case: measurements=[Measurement('Norte', None), Measurement('Sur', 0.0), Measurement('Norte', 0.0)]
```

¿Un error? No: `Series.means` ordena por el primer **valor** de cada etiqueta, y `summary`, por la primera **aparición**, tenga valor o no. Norte aparece primero, pero sin valor. Las medias son las mismas; el orden, no. El test compara diccionarios, sin orden, y deja un comentario. Cuando Hypothesis encuentra una diferencia, decide si es un error del código o del test, y escríbelo.

---

## 4. Tiempo en la frontera

Las firmas de `summaries.py` usan los tipos de Python, no los de pandas:

```python
def timed(frame: pd.DataFrame, start: datetime, every: timedelta) -> pd.DataFrame: ...
def evolution(frame: pd.DataFrame, period: timedelta) -> pd.DataFrame: ...
def duration(text: str) -> timedelta: ...
```

Quien llama no necesita saber nada de pandas para darle una fecha, y `date_range` y `resample` aceptan `datetime` y `timedelta` igual que textos. `duration` devuelve `to_pytimedelta()`: un `timedelta` de Python puro, que un test comprueba con `type(value) is timedelta`.

`duration` convierte lo que escribe una persona (`--cada 15min`) en una duración. Tres casos que rechazar, con el **mismo** mensaje:

- un texto que no es duración (`"abc"`, `"1M"`), que hace a `pd.Timedelta` lanzar `ValueError`;
- el texto vacío, que **no** lanza: da `NaT`;
- cero o negativo, que es una duración válida pero no sirve como intervalo: `date_range` con `freq` cero lanza `ValueError: range() arg 3 must not be zero`, y `resample` con un periodo cero, `ZeroDivisionError`.

```python
problem = ValueError(f"no es una duración mayor que cero: {text!r}")
try:
    value = pd.Timedelta(text)
except ValueError as error:
    raise problem from error
if pd.isna(value) or value <= pd.Timedelta(0):
    raise problem
```

Un mensaje propio y en español es mejor que tres de pandas en inglés, y la CLI lo convierte en `error: ...` con código 2, como cualquier otro dato de entrada que no vale.

Para `--inicio`, Typer ya sabe leer fechas: con el tipo `datetime`, acepta `2026-11-01`, `2026-11-01T08:00:00` y `2026-11-01 08:00:00`, y rechaza lo demás con su propio error de uso.

---

## 5. ¿Cuánto gana pandas esta vez?

En la máquina del bootcamp, con las 100 000 medidas de `generar_medidas.py`:

| Operación | Python | pandas |
|---|---|---|
| Media por etiqueta | 9,6 ms (`Series.means`) | 9,2 ms (`summary`, con cinco estadísticas) |
| Comparar dos resúmenes | 12,9 ms (dos `means` y un diccionario) | 1,3 ms (`compare`, ya resumidos) |
| Poner tiempo a la tabla | — | 0,1 ms (`timed`) |
| Media por etiqueta y día | — | 18,8 ms (`evolution`, 348 días) |

`summary` calcula cinco cosas en el tiempo que `Series.means` calcula una. Y `evolution` no tiene equivalente en lo que ya tenías: escribirlo con diccionarios llevaría un bucle por medida y otro por periodo, con cuidado de no olvidar los vacíos.

El comando entero tarda más de un segundo (`resumir` 1,25 s, `evolucion` 1,29 s), y casi todo es lo de siempre: arrancar Python, importar pandas y analizar 100 000 líneas con `Series.parse`. El resumen es la parte barata.

---

## 6. Cuándo no usar pandas

pandas paga un precio fijo: unos 0,3 s al importarse y más de 100 MB en la imagen Docker. Para una cuenta pequeña en un comando que se ejecuta mil veces al día, un diccionario puede ser mejor. Para resumir, cruzar o agrupar por tiempo tablas de miles de filas, pandas te ahorra código y errores: los NaN, los grupos vacíos, el orden y los tipos los decide él, de la misma forma cada vez.

La semana 26 trae dos alternativas para cuando pandas se queda corto en velocidad o en memoria: Polars y DuckDB.

---

## 7. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| `# type: ignore` porque mypy no entiende un `agg` | Esconde el problema y el siguiente | Escríbelo de la forma que los *stubs* tipan bien |
| Reexportar `summaries` en `core` | Todos los comandos cargarían pandas | Importa el módulo dentro de cada comando |
| Tabla esperada vacía hecha con listas | Sus columnas son `float64` | Convierte los tipos como el resultado real |
| Índice esperado con `pd.DatetimeIndex([...])` | No tiene `freq`, y el resultado sí | `date_range`, o `check_freq=False` |
| Dar por bueno un fallo de orden de Hypothesis sin pensarlo | Puede ser el test, no el código | Entiende la diferencia y escríbela |
| `pd.Timestamp` en las firmas de `core` | Quien llama tiene que importar pandas | `datetime` y `timedelta` de Python |
| Aceptar `--cada 0h` | `date_range` o `resample` fallan con un error poco claro | Rechaza las duraciones que no son mayores que cero |

---

## ✅ Qué debes saber al terminar

- [ ] Por qué `summaries.py` no importa nada del Observatorio, y por qué no se reexporta.
- [ ] Qué forma de `agg` tipa bien con `pandas-stubs`, y cómo anotar el diccionario de `rename_axis`.
- [ ] Qué vigilar al probar un resumen: orden, tipos de la tabla vacía, `freq` y nombres de columnas.
- [ ] Por qué un test con Hypothesis contra `Series.means` compara diccionarios.
- [ ] Qué tipos van en las firmas de `core`, y qué rechaza `duration`.
- [ ] Dónde se va el tiempo de `resumir` y `evolucion`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Series de tiempo](04-series-de-tiempo.md) | **05 · pandas II en un proyecto** | [Ejercicio 01 · groupby: dividir, calcular y juntar](../2-practicas/ejercicio-01-groupby-dividir-calcular-y-juntar/README.md) |
