# Glosario — Semana 24

| Término | Definición |
|---|---|
| **Alineación por índice** | Al operar dos `Series` o `DataFrame`, pandas empareja las filas con la misma etiqueta, estén donde estén. Las etiquetas que solo están en un lado dan NaN |
| **`assign`** | Devuelve una tabla nueva con columnas añadidas o cambiadas, sin tocar la original |
| **Asignación encadenada** | Cambiar valores con dos selecciones seguidas, `df[máscara]["col"] = valor`. En pandas 3 nunca cambia la tabla original y avisa con `ChainedAssignmentError` |
| **`category`** | Tipo de pandas para columnas con pocos valores distintos que se repiten: guarda cada valor una vez y un código por fila. Lo devuelve `pd.cut` |
| ***Copy-on-write*** | La regla de pandas 3: toda tabla o columna que sale de otra se comporta como una copia, pero los datos solo se copian cuando una de las dos cambia |
| **`DataFrame`** | Una tabla: un índice para las filas y columnas con nombre, cada una una `Series` con su tipo |
| **`describe`** | Resumen de las columnas numéricas: cuántos valores, media, desviación (`ddof=1`), mínimo, cuartiles y máximo |
| **`dtypes`** | El tipo de cada columna de un `DataFrame`. Lo primero que se mira después de leer un archivo |
| **`equals`** | Dice si dos tablas tienen los mismos valores, tipos e índice, con NaN en el mismo sitio contando como iguales |
| **Estable (orden)** | Un algoritmo de ordenación que deja los empates en el orden en que estaban. En `sort_values`, `kind="stable"`; el de por defecto no lo es |
| **`iloc`** | Elegir filas y columnas por su **posición**, desde 0. Los cortes excluyen el final, como en Python |
| **Índice** | Las etiquetas de las filas de una `Series` o un `DataFrame`. No es una columna: no cuenta en `shape` |
| **`Int64`** | Tipo de pandas para enteros que admite datos que faltan, marcados con `pd.NA`. Con minúscula, `int64` es el de NumPy, que no los admite |
| **`isin`** | Máscara con `True` donde el valor está en una lista. Sustituye a encadenar varias comparaciones con `\|` |
| **`keep_default_na`** | Parámetro de `read_csv`. Con `False`, textos como `NA`, `null` o `None` dejan de ser datos que faltan en todas las columnas |
| **`loc`** | Elegir filas y columnas por su **etiqueta**. Los cortes incluyen el final |
| **Máscara** | Una `Series` de `bool` con el mismo índice que la tabla; `df[máscara]` se queda con las filas donde es `True` |
| **`na_values`** | Parámetro de `read_csv`: qué textos son un dato que falta. Con un dict, por columna |
| **`pandas-stubs`** | El paquete con los tipos de pandas para mypy. Va en las dependencias de desarrollo, con la versión de tu pandas |
| **`pd.cut`** | Reparte una columna de números en intervalos con nombre. `right=False` hace que cada intervalo incluya su borde izquierdo |
| **`pd.NA`** | El marcador de dato que falta de los tipos de pandas como `Int64`. NaN es el de `float64` |
| **`pd.testing`** | Funciones para comparar tablas en los tests: `assert_frame_equal` y `assert_series_equal` |
| **`query`** | Filtra filas con una condición escrita como texto: `df.query("valor > @limite")` |
| **`RangeIndex`** | El índice de enteros seguidos. No guarda los números, solo el inicio, el final y el paso |
| **`read_csv`** | Lee un CSV en un `DataFrame`. Rápido, pero no valida: una fila mala cambia el tipo de toda la columna |
| **`Series`** | Una columna: valores de un solo tipo, un índice con una etiqueta para cada uno y un nombre |
| **`set_index`** | Convierte una columna en el índice. `reset_index` hace lo contrario |
| **`skipna`** | Parámetro de los métodos de pandas, `True` por defecto: los NaN no cuentan en sumas, medias y desviaciones |
| **`sort_values`** | Ordena las filas por una o varias columnas. Los NaN van al final salvo que digas `na_position="first"` |
| **`str` (tipo)** | El tipo de texto de pandas 3. Hasta pandas 2, el texto se guardaba como `object` |
| **`.str`** | Los métodos de cadena aplicados a toda una `Series` de texto: `.str.strip()`, `.str.replace(...)`, `.str.startswith(...)` |
| **`to_csv`** | Escribe una tabla en un CSV. Con `index=False`, sin el índice como primera columna |
| **`to_numpy`** | El array de NumPy de una `Series`. Con *copy-on-write* puede ser de solo lectura |
| **`value_counts`** | Cuántas veces aparece cada valor, de más a menos. `normalize=True` da proporciones |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
