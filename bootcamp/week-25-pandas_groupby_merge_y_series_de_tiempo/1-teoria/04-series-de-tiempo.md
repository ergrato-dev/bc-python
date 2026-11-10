# 04 · Series de tiempo

⏱️ 50 min

## 🎯 Objetivos

- Trabajar con instantes (`Timestamp`), duraciones (`Timedelta`) y el dato de tiempo que falta (`NaT`).
- Convertir texto en fechas sin confundir el día con el mes, y encontrar las que no son fechas.
- Generar instantes a intervalos fijos con `date_range`, y distinguir una duración fija de un periodo de calendario.
- Usar un índice de tiempo para elegir por día, por intervalo y por hora.
- Agrupar por periodos con `resample`, y saber dónde empieza y acaba cada uno.
- Calcular medias móviles con `rolling` y cambios con `shift` y `diff`.
- Poner y cambiar la zona horaria de unas fechas.

---

## 1. Instantes, duraciones y NaT

Una medida de un sensor no es solo un valor: es un valor **en un instante**. pandas tiene tres piezas para el tiempo:

| Pieza | Qué es | Equivale en Python | Ejemplo |
|---|---|---|---|
| `Timestamp` | Un instante | `datetime` | `pd.Timestamp("2026-11-01 08:00")` |
| `Timedelta` | Una duración | `timedelta` | `pd.Timedelta("90min")` |
| `NaT` | Un instante que falta | `None` | lo que da una fecha que no se pudo leer |

Una columna de instantes tiene tipo `datetime64[us]`: cada valor es un entero de 64 bits que cuenta microsegundos (en pandas 3, la precisión por defecto). Una de duraciones, `timedelta64[us]`.

Se operan como en Python:

```python
pd.Timestamp("2026-11-01 08:00") - pd.Timestamp("2026-10-31 20:30")   # Timedelta('0 days 11:30:00')
pd.Timedelta("1h") * 3                                                 # 3 horas
pd.Timedelta("1D") / pd.Timedelta("1h")                                # 24.0
first + pd.Timedelta("90min")                                          # 90 minutos después
```

`Timestamp` es una subclase de `datetime`, y `Timedelta`, de `timedelta`: puedes pasarlos a cualquier función que espere los de Python, y compararlos con ellos. `to_pydatetime()` y `to_pytimedelta()` los convierten en los de Python puros, lo que conviene en la frontera de tu código (teoría 05).

---

## 2. De texto a fecha

Un CSV no tiene tipos: `read_csv` deja la fecha como texto. `pd.to_datetime` la convierte. Con fechas como `03/11/2026`, ¿es el 3 de noviembre o el 11 de marzo?

```python
pd.to_datetime("03/11/2026")                    # 2026-03-11: mes/día, al estilo de EE. UU.
pd.to_datetime("03/11/2026", dayfirst=True)     # 2026-11-03
```

Sin formato, pandas adivina, y adivina mes/día. Da siempre el **formato exacto**:

```python
pd.to_datetime(raw["fecha"], format="%d/%m/%Y %H:%M")
```

Los códigos son los de `strftime` de Python: `%d` día, `%m` mes, `%Y` año con cuatro cifras, `%H` hora de 0 a 23, `%M` minuto, `%S` segundo. Si una fila no encaja, la columna entera falla:

```
ValueError: time data "ayer" doesn't match format "%d/%m/%Y %H:%M"
```

`errors="coerce"` convierte esa fila en `NaT` y deja seguir. Después búscalas, como buscabas las celdas que no eran números en la semana 24:

```python
raw["time"] = pd.to_datetime(raw["fecha"], format="%d/%m/%Y %H:%M", errors="coerce")
raw.loc[raw["time"].isna(), "fecha"]        # ['ayer']
```

`read_csv` también lee fechas, con `parse_dates=["fecha"]` y `date_format="%d/%m/%Y %H:%M"`, pero con una trampa: si **una** fila no encaja, deja la columna entera como texto, sin error ni aviso. Con `lecturas.csv`, la columna sale `str` por culpa de `ayer`. Lee como texto y convierte con `to_datetime`: así el problema se ve.

Ya convertida, el accesor `.dt` da las partes de cada fecha: `.dt.hour`, `.dt.day_of_week` (0 es lunes), `.dt.day_name()` (en inglés), `.dt.date`, y `.dt.floor("h")`, que redondea hacia abajo a la hora.

---

## 3. date_range: duraciones y periodos de calendario

`date_range` genera instantes a intervalos fijos: el inicio, cuántos y cada cuánto.

```python
pd.date_range(datetime(2026, 11, 1, 8), periods=3, freq=timedelta(minutes=90), name="time")
# DatetimeIndex(['2026-11-01 08:00:00', '2026-11-01 09:30:00', '2026-11-01 11:00:00'], ..., freq='90min')
```

Es lo que hace `timed` en tu Observatorio: tus archivos no traen la hora de cada medida, así que `evolucion` supone que la primera es la de `--inicio` y que llega una cada `--cada`.

`freq` acepta una `timedelta` o un texto. Hay dos clases de textos, y se confunden:

| Texto | Qué es | ¿Duración fija? |
|---|---|---|
| `"15min"`, `"1h"`, `"1D"`, `"1W"` | Minutos, horas, días, semanas | Sí: un día son siempre 24 horas |
| `"ME"`, `"MS"`, `"YE"` | Fin de mes, inicio de mes, fin de año | No: un mes tiene 28, 30 o 31 días |

```python
pd.date_range("2026-01-31", periods=3, freq="ME")    # 31 de enero, 28 de febrero, 31 de marzo
```

Los periodos de calendario sirven en `date_range` y en `resample`, pero no son una `Timedelta`:

```
pd.Timedelta("1ME")   ValueError: invalid unit abbreviation: ME
pd.Timedelta("1M")    ValueError: Units 'M', 'Y' and 'y' do not represent unambiguous timedelta values and are not supported.
```

Por eso `summaries.duration`, que usa `pd.Timedelta`, solo acepta duraciones fijas. Las mayúsculas importan: `"1H"` y `"1d"` funcionan pero avisan de que dejarán de hacerlo (`Pandas4Warning`). Usa `h`, `min`, `D` y `W`.

---

## 4. Un índice de tiempo

Con los instantes en el índice, la tabla entiende el tiempo:

```python
timed = readings.set_index("time").sort_index()
type(timed.index)                                    # DatetimeIndex
timed.loc["2026-11-02"]                              # el día entero
timed.loc["2026-11-01 11:00":"2026-11-02 08:00"]     # incluye los dos extremos
timed.between_time("07:00", "12:00")                 # las mañanas, de cualquier día
```

- Con un texto parcial (`"2026-11-02"`, o `"2026-11"` para el mes), `loc` elige todo lo que cae dentro.
- Un corte con `loc` incluye los dos extremos, como siempre con etiquetas.
- Cortar necesita el índice **ordenado**. Sin `sort_index`: `KeyError: 'Value based partial slicing on non-monotonic DatetimeIndexes with non-existing keys is not allowed.'`

---

## 5. resample: groupby por periodos

`resample` agrupa las filas por periodos de tiempo, como `groupby` las agrupaba por estación:

```python
north.resample("6h").mean()
```

```
time
2026-11-01 06:00:00    13.25
2026-11-01 12:00:00      NaN
2026-11-01 18:00:00    20.00
2026-11-02 00:00:00      NaN
2026-11-02 06:00:00    48.90
2026-11-02 12:00:00    22.00
Freq: 6h, Name: value, dtype: float64
```

Tres cosas que no son obvias:

- **Dónde empieza cada periodo.** Por defecto, en la medianoche del primer día (`origin="start_day"`): 0:00, 6:00, 12:00, 18:00. La primera medida, de las 8:00, cae en el periodo de las 6:00. Con `origin="start"`, los periodos empiezan en la primera medida.
- **Qué fila es de qué periodo.** Cada periodo incluye su inicio y no su final (`closed="left"`), y se etiqueta con su inicio (`label="left"`). Una medida de las 12:00 en punto es del periodo de las 12:00.
- **Los periodos vacíos salen.** El de las 12:00 del día 1 no tiene ninguna medida, y aparece, con NaN. `groupby` solo saca los grupos que existen; `resample` saca todos los periodos entre la primera y la última medida. `count()` distingue un periodo vacío (0) de uno con valores.

Con varias columnas, `resample` las resume todas. Para resumir varias estaciones a la vez, cada una en su columna: `pivot` primero (teoría 03) y `resample` después. Es lo que hace `evolution` en tu proyecto:

![Una tabla larga con un instante, una etiqueta y un valor por fila pasa por pivot a una tabla ancha con una columna por etiqueta y NaN donde no hay medida; resample de 3 horas agrupa las filas en periodos que empiezan a las 6:00, 9:00 y 12:00, con la media de cada columna](../0-assets/03-pivot-y-resample.svg)

```python
frame.pivot(columns="label", values="value").resample(period).mean()
```

La otra forma, sin pasar a ancho, es un `groupby` con dos claves, la etiqueta y el periodo: `groupby(["label", pd.Grouper(freq="3h")])`. Da una fila por pareja que existe, en formato largo.

---

## 6. rolling, shift y diff

`resample` cambia el número de filas: una por periodo. Estas otras dan **una por fila**:

```python
north.rolling(2).mean()       # media de cada fila y la anterior
north.rolling("6h").mean()    # media de las filas de las 6 horas anteriores
north.shift(1)                # el valor de la fila anterior
north.diff()                  # cada valor menos el anterior
north.pct_change()            # el cambio en proporción
```

- `rolling(n)` es tu `moving_average` de la semana 06, con dos diferencias: devuelve una fila por fila (las primeras `n - 1` son NaN) y cualquier ventana con un NaN da NaN. `min_periods=1` calcula con lo que haya.
- `rolling("6h")` usa una ventana de **tiempo**: las filas de las 6 horas anteriores, sean cuantas sean. Con medidas que no llegan a intervalos fijos, es la que tiene sentido.
- `shift` y `diff` comparan con la fila anterior, no con el instante anterior: si falta una medida, comparan con la de antes.

Con `groupby`, todo esto se calcula dentro de cada grupo: `readings.groupby("station")["value"].diff()` compara cada medida con la anterior **de su estación**.

---

## 7. Zonas horarias

Las fechas de un CSV no suelen decir su zona horaria: son *naive*. pandas las trata como relojes sin zona, y no pasa nada mientras todas sean de la misma.

```python
local = timed.index.tz_localize("America/Bogota")    # dice cuál es: 08:00-05:00
local.tz_convert("UTC")                              # la pasa a otra: 13:00+00:00
```

- `tz_localize` **no cambia la hora**: dice en qué zona estaba. `tz_convert` la cambia a otra zona.
- Comparar o restar una fecha con zona y otra sin ella: `TypeError: Cannot compare tz-naive and tz-aware timestamps`.
- Donde cambia la hora, una hora local puede existir dos veces (al atrasar el reloj) o ninguna (al adelantarlo). Con zona, pandas las distingue; sin ella, no.

Regla práctica: **guarda en UTC**, convierte a la zona local solo para mostrar. La base de datos de zonas la trae `tzdata`, que pandas instala.

---

## 8. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| `to_datetime` sin `format` con fechas día/mes | Lee mes/día: el 3 de noviembre pasa a 11 de marzo | `format="%d/%m/%Y"` |
| `parse_dates` en `read_csv` y no mirar el tipo | Con una fila mala, la columna se queda como texto, sin aviso | Lee como texto y `to_datetime(..., errors="coerce")` |
| `pd.Timedelta("1M")` para un mes | Un mes no es una duración fija | `"ME"` o `"MS"` en `date_range` o `resample` |
| Esperar que los periodos empiecen en la primera medida | Empiezan a medianoche | `origin="start"` si lo necesitas |
| Creer que `resample` solo da periodos con datos | Saca todos, también los vacíos | `count()` para distinguirlos |
| `rolling(3)` con medidas irregulares | Mezcla tres filas, aunque estén separadas por días | `rolling("6h")` |
| Mezclar fechas con zona y sin zona | `TypeError` al comparar | Decide una vez; guarda en UTC |

---

## ✅ Qué debes saber al terminar

- [ ] Qué son `Timestamp`, `Timedelta` y `NaT`, y cómo pasar de los de pandas a los de Python.
- [ ] Convertir texto en fechas con `format` y `errors="coerce"`, y por qué no fiarte de `parse_dates`.
- [ ] La diferencia entre una duración fija (`"1D"`) y un periodo de calendario (`"ME"`).
- [ ] Elegir por día, por intervalo y por hora con un índice de tiempo.
- [ ] Dónde empiezan los periodos de `resample`, qué etiqueta llevan y qué pasa con los vacíos.
- [ ] Cuándo usar `rolling(n)` y cuándo `rolling("6h")`; qué hacen `shift` y `diff`.
- [ ] La diferencia entre `tz_localize` y `tz_convert`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Dar forma: pivot, melt y crosstab](03-dar-forma-pivot-melt-y-crosstab.md) | **04 · Series de tiempo** | [05 · pandas II en un proyecto](05-pandas-ii-en-un-proyecto.md) |
