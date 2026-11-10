# Ejercicio 04 — Series de tiempo

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-series-de-tiempo.md)

## Objetivo

Medidas con fecha y hora, como llegan de un sensor de verdad:

- leer fechas en formato día/mes/año sin que pandas las confunda, y apartar las que no son fechas;
- trabajar con instantes (`Timestamp`) y duraciones (`Timedelta`);
- usar la fecha como índice y elegir por día o por intervalo con un texto;
- agrupar por periodos con `resample`, y saber dónde empieza cada periodo;
- medias móviles con `rolling`, y comparar con la medida anterior con `shift` y `diff`;
- poner zona horaria a las fechas, y ver el cambio de hora.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-25-pandas_groupby_merge_y_series_de_tiempo/2-practicas/ejercicio-04-series-de-tiempo/starter
cat lecturas.csv
uv run python main.py
```

```
Ejercicio 04 · Series de tiempo
```

`lecturas.csv` tiene once lecturas de Norte y Sur del 1 y el 2 de noviembre de 2026, con la fecha como `01/11/2026 08:00` (día/mes/año). No llegan a intervalos fijos, la de las 2:00 del día 2 no tiene valor (`NA`) y la última dice `ayer` en lugar de una fecha.

## Pasos

### 1. De texto a fecha

Descomenta el **PASO 1** y ejecuta:

```
tipo leído: str · 01/11/2026 08:00
sin formato: 2026-03-11 00:00:00 · dayfirst: 2026-11-03 00:00:00
ValueError: time data "ayer" doesn't match format "%d/%m/%Y %H:%M"
tipo: datetime64[us] · sin fecha: ['ayer']
```

- `read_csv` deja las fechas como texto: no sabe que lo son.
- Sin formato, `pd.to_datetime("03/11/2026")` lee **mes/día**, al estilo de Estados Unidos: el 11 de marzo. `dayfirst=True` lo arregla, pero lo seguro es dar el formato exacto.
- Con `format`, una sola fila que no encaja (`ayer`) hace fallar toda la columna. `errors="coerce"` la convierte en `NaT` ("not a time", el NaN de las fechas) y puedes buscarla.
- El tipo es `datetime64[us]`: un instante con precisión de microsegundos, el valor por defecto de pandas 3.

Las filas sin fecha se quitan con `dropna(subset=["time"])`, y las columnas pasan a inglés, como en tu Observatorio.

### 2. Instantes y duraciones

Descomenta el **PASO 2** y ejecuta:

```
Timestamp 2026-11-01 08:00:00 · hora: 8 · día: Sunday
huecos: 0 days 01:30:00 · el mayor: 0 days 06:00:00 · tipo: timedelta64[us]
más 90 min: 2026-11-01 09:30:00 · ¿igual? True
['01 00:00', '01 06:00', '01 12:00', '01 18:00']
```

- Cada fecha es un `Timestamp`, el `datetime` de pandas, con atributos como `hour` y métodos como `day_name()` (en inglés).
- Restar dos instantes da una duración, un `Timedelta`. `diff()` resta cada fila a la anterior: el hueco más largo entre lecturas es de 6 horas.
- `pd.Timedelta("90min")` lee una duración escrita como texto. Es lo que hace `summaries.duration` en el proyecto.
- `date_range` genera instantes a intervalos fijos: el principio, cuántos y cada cuánto (`freq`).

### 3. Un índice de tiempo

Descomenta el **PASO 3** y ejecuta:

```
DatetimeIndex · ¿ordenado? True
el día 2: [nan, 7.5, 48.9, 22.0, 10.0]
de 11:00 a 08:00: ['Norte', 'Sur', 'Norte', 'Norte', 'Sur', 'Norte']
por la mañana: [12.5, 8.0, 14.0, 7.5, 48.9]
```

- Con la fecha en el índice (`set_index`), el índice es un `DatetimeIndex`. Ordénalo con `sort_index`: elegir por intervalo lo necesita.
- `loc["2026-11-02"]` elige el día entero con un texto, sin escribir horas.
- Un corte con dos textos incluye **los dos extremos**, como todo corte con `loc`.
- `between_time` elige por hora del día, sea el día que sea.

### 4. resample, medias por periodo

Descomenta el **PASO 4** y ejecuta:

```
time
2026-11-01 06:00:00    13.25
2026-11-01 12:00:00      NaN
2026-11-01 18:00:00    20.00
2026-11-02 00:00:00      NaN
2026-11-02 06:00:00    48.90
2026-11-02 12:00:00    22.00
Freq: 6h, Name: value, dtype: float64
cuántas: [2, 0, 1, 0, 1, 1]
desde la primera: ['01 08:00', '01 14:00', '01 20:00', '02 02:00', '02 08:00']
station     Norte         Sur      
             mean   max  mean   max
time                               
2026-11-01  15.50  20.0  8.75   9.5
2026-11-02  35.45  48.9  8.75  10.0
```

- `resample("6h")` es un `groupby` por periodos de 6 horas. Los periodos empiezan a medianoche (0:00, 6:00, 12:00, 18:00), **no** en la primera medida: la de las 8:00 cae en el de las 6:00.
- Salen **todos** los periodos, también los vacíos: el de las 12:00 del día 1 no tiene ninguna, y el de las 0:00 del día 2 tiene una sin valor. Los dos dan NaN; `count` los distingue (0 en los dos, porque el NA no cuenta).
- `origin="start"` empieza a contar en la primera medida.
- Para varias estaciones a la vez, `pivot` (ejercicio 03) y después `resample`, con varias funciones: dos niveles de columnas.

### 5. rolling, shift y diff

Descomenta el **PASO 5** y ejecuta:

```
rolling(2):   [nan, 13.25, 17.0, nan, nan, 35.45]
rolling("6h"): [12.5, 13.25, 20.0, nan, 48.9, 35.45]
shift(1):     [nan, 12.5, 14.0, 20.0, nan, 48.9]
diff():       [nan, 1.5, 6.0, nan, nan, -26.9]
cada 12 h:    [12.5, 20.0, 48.9]
```

- `rolling(2)` es una media móvil de **dos filas**, la de la semana 06: la primera no tiene anterior y da NaN, y cualquier ventana con el NA da NaN.
- `rolling("6h")` usa una ventana de **6 horas** hacia atrás, tengan las filas que tengan. Con medidas a intervalos irregulares, es la que tiene sentido: la de las 20:00 no se mezcla con la de las 11:00.
- `shift(1)` baja cada valor una fila; `diff()` resta el anterior: cuánto cambió desde la última lectura.
- `asfreq("12h")` se queda con la lectura que cae justo cada 12 horas desde la primera.

### 6. Zonas horarias

Descomenta el **PASO 6** y ejecuta:

```
Bogotá: 2026-11-01 08:00:00-05:00 · UTC: 2026-11-01 13:00:00+00:00
Madrid, cambio de hora: ['01:00 CEST', '02:00 CEST', '02:00 CET']
TypeError: Cannot compare tz-naive and tz-aware timestamps
```

- Las fechas del CSV no dicen su zona horaria (*naive*). `tz_localize` dice cuál es; `tz_convert` la pasa a otra. Las 8:00 de Bogotá son las 13:00 en UTC.
- En Madrid, el 25 de octubre de 2026 a las 3:00 se atrasa el reloj: las 2:00 existen dos veces. Con zona horaria, pandas las distingue (CEST y CET); sin ella, se confundirían.
- Comparar una fecha con zona y otra sin ella lanza `TypeError`. Decide una vez si trabajas con zona o sin ella; para guardar, UTC.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `FileNotFoundError: ... 'lecturas.csv'` | Ejecuta desde `starter/`, donde está el CSV |
| El 3 de noviembre sale como 11 de marzo | Falta `format="%d/%m/%Y %H:%M"` o `dayfirst=True` |
| `ValueError: time data "ayer" doesn't match format` fuera del `try` | Falta `errors="coerce"` |
| `KeyError: 'Value based partial slicing on non-monotonic DatetimeIndexes...'` | El índice no está ordenado: `sort_index()` antes de cortar |
| `TypeError: Only valid with DatetimeIndex, TimedeltaIndex or PeriodIndex, but got an instance of 'RangeIndex'` | `resample` necesita el índice de tiempo: falta el `set_index("time")` del paso 3 |
| `ZoneInfoNotFoundError: 'No time zone found with key america/bogota'` | Escribe el nombre exacto, con mayúsculas y sin tildes: `America/Bogota`. La base de datos de zonas la trae `tzdata`, que pandas instala |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Dar forma con pivot y melt](../ejercicio-03-dar-forma-con-pivot-y-melt/README.md) | **Ejercicio 04 · Series de tiempo** | [Proyecto · Resumir medidas por grupos y por periodos](../../3-proyecto/README.md) |
