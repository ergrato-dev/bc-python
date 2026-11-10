# Glosario — Semana 25

| Término | Definición |
|---|---|
| **Agregación con nombre** | `groupby(...).agg(nombre=("columna", "función"))`: cada columna del resultado dice su nombre, de qué columna sale y qué función usa |
| **`agg`** | Calcula una o varias funciones por grupo y da **una fila por grupo** |
| **`as_index=False`** | En `groupby`, deja las claves como columnas normales en lugar de en el índice |
| **`concat`** | Pone tablas una debajo de otra (o lado a lado, con `axis=1`). Conserva los índices salvo con `ignore_index=True` |
| **`count` y `size`** | Por grupo, `count` cuenta los valores (sin NaN) y `size` las filas. La resta son los datos que faltan |
| **`crosstab`** | Tabla que cuenta cuántas filas hay de cada combinación de dos columnas |
| **`date_range`** | Genera instantes a intervalos fijos: el inicio, cuántos (`periods`) y cada cuánto (`freq`) |
| **`DatetimeIndex`** | Un índice de instantes. Permite elegir por día o intervalo con un texto, `resample` y `rolling` por tiempo |
| **`diff`** | Cada valor menos el de la fila anterior |
| **`dropna=False`** | En `groupby`, crea un grupo para las filas cuya clave es NaN, que si no se quitan sin aviso |
| **`.dt`** | Las partes de una columna de fechas: `.dt.hour`, `.dt.day_of_week`, `.dt.day_name()`, `.dt.floor("h")` |
| **`filter`** | En `groupby`, se queda con los grupos que cumplen una condición, con todas sus filas |
| **Formato ancho** | Una columna por categoría y una celda por medida. Para leer y comparar |
| **Formato largo** | Una fila por medida y una columna por variable. Para guardar, agrupar y cruzar |
| **`freq`** | Cada cuánto, en `date_range` y `resample`: una duración (`"15min"`, `"1h"`, `"1D"`) o un periodo de calendario (`"ME"`, `"MS"`) |
| **`groupby`** | Divide la tabla en grupos por el valor de una o varias columnas, calcula en cada grupo y junta los resultados |
| **`how`** | En `merge`, qué filas salen: `inner` (las de las dos, por defecto), `left`, `right` u `outer` (todas) |
| **`indicator`** | En `merge`, añade la columna `_merge` con `both`, `left_only` o `right_only` |
| **`join`** | Cruza dos tablas por el índice; por defecto, `how="left"` |
| **`melt`** | De formato ancho a largo: cada celda pasa a ser una fila |
| **`merge`** | Cruza dos tablas por una o varias columnas clave (o por el nombre de un índice) |
| **`MergeError`** | El error de `merge` cuando las claves no cumplen la relación de `validate` |
| **`MultiIndex`** | Un índice de varios niveles, como el de `groupby` con dos claves. Se elige con una tupla |
| **NaT** | *Not a time*: el instante que falta, el NaN de las fechas |
| **`origin`** | En `resample`, desde dónde se cuentan los periodos: la medianoche del primer día (`"start_day"`, por defecto) o la primera medida (`"start"`) |
| **`pivot`** | De formato largo a ancho: una columna para el índice, otra para las columnas y otra para las celdas. Falla con parejas repetidas |
| **`pivot_table`** | Como `pivot`, pero junta los valores repetidos con un `aggfunc` |
| **`resample`** | `groupby` por periodos de tiempo. Saca todos los periodos, también los vacíos |
| **`rolling`** | Ventana móvil: `rolling(3)` por filas, `rolling("6h")` por tiempo |
| ***Series* de tiempo** | Medidas ordenadas en el tiempo, con un instante por medida |
| **`shift`** | Mueve los valores una o varias filas: `shift(1)` da el valor anterior |
| ***Split-apply-combine*** | Dividir, calcular y juntar: el patrón que implementa `groupby` |
| **`stack` y `unstack`** | Pasan un nivel de las columnas al índice (`stack`) o del índice a las columnas (`unstack`) |
| **`suffixes`** | En `merge`, cómo se llaman las columnas que tienen el mismo nombre en las dos tablas |
| **`Timedelta`** | Una duración, el `timedelta` de pandas. Solo admite duraciones fijas: un mes no lo es |
| **`Timestamp`** | Un instante, el `datetime` de pandas |
| **`to_datetime`** | Convierte texto en fechas. Con `format` exacto y `errors="coerce"` para encontrar las que no lo son |
| **`transform`** | Calcula por grupo y devuelve **una fila por fila**, con el índice de la tabla original |
| **`tz_convert`** | Pasa unas fechas con zona horaria a otra zona |
| **`tz_localize`** | Dice en qué zona horaria están unas fechas sin zona, sin cambiar la hora |
| **`validate`** | En `merge`, la relación que esperas entre las claves (`one_to_one`, `many_to_one`...). Si no se cumple, `MergeError` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
