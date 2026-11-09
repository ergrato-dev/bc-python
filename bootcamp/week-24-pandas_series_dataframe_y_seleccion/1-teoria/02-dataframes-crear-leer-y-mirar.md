# 02 · DataFrames: crear, leer y mirar

⏱️ 50 min

## 🎯 Objetivos

- Explicar qué es un `DataFrame`: un índice compartido y columnas con nombre, cada una una `Series` de su tipo.
- Crear un `DataFrame` desde diccionarios, listas de registros o `Series`, con los tipos que quieres incluso vacío.
- Leer un CSV con `read_csv` eligiendo separador, decimal y datos que faltan, y reconocer sus trampas.
- Mirar una tabla antes de usarla: `head`, `info`, `describe` y los tipos.
- Añadir, renombrar y quitar columnas, y escribir la tabla otra vez a CSV.

---

## 1. Una tabla de Series

Un `DataFrame` es una tabla: un **índice** para las filas y varias **columnas** con nombre. Cada columna es una `Series` con su tipo, y todas comparten el índice.

![Un DataFrame con índice position de 1 a 4 y columnas label (str), value (float64) y level (str); frame["value"] es una Series; NaN en la fila 3](../0-assets/01-anatomia-de-un-dataframe.svg)

```python
table = pd.DataFrame(
    {"estacion": ["Norte", "Sur", "Este"], "valor": [12.5, 8.0, 48.9], "sensores": [3, 1, 2]}
)
print(table)
```

```
  estacion  valor  sensores
0    Norte   12.5         3
1      Sur    8.0         1
2     Este   48.9         2
```

```python
table.shape              # (3, 3): filas y columnas; el índice no cuenta
table.columns.tolist()   # ['estacion', 'valor', 'sensores']
table.dtypes             # estacion str, valor float64, sensores int64
table["valor"]           # una Series, con el mismo índice y name="valor"
```

Es la diferencia con un array de dos ejes de la semana 23: allí toda la tabla tenía **un** tipo; aquí cada columna tiene el suyo. Por dentro, pandas guarda cada columna (o cada grupo de columnas del mismo tipo) en su propio array.

---

## 2. Crear un DataFrame

Las tres formas más comunes:

```python
pd.DataFrame({"label": ["A", "B"], "value": [1.0, 2.0]})       # un dict de columnas
pd.DataFrame([{"label": "A", "value": 1.0}, {"label": "B"}])  # una lista de registros
pd.DataFrame({"label": labels_series, "value": values_series}) # Series: se alinean por índice
```

En la lista de registros, la clave que falta en el segundo (`value`) sale como NaN. Con `Series`, pandas alinea por el índice (teoría 01, sección 5): si los índices no coinciden, aparecen filas con NaN.

Dos parámetros útiles: `index=` para dar tu propio índice, y `columns=` para elegir el orden de las columnas.

Una trampa con las tablas **vacías**: sin valores, pandas no puede deducir el tipo y pone `float64` en todas.

```python
pd.DataFrame({"label": [], "value": []}).dtypes
# label float64, value float64
pd.DataFrame({"label": pd.Series([], dtype="str"), "value": pd.Series([], dtype="float64")}).dtypes
# label str, value float64
```

Si tu código recibe a veces una serie vacía, crea las columnas con su tipo, como `frame_of` en tu proyecto. Un test lo comprueba.

---

## 3. Leer un CSV

`pd.read_csv` lee un archivo (o una URL, o un texto) y devuelve un `DataFrame`. Sin parámetros supone un CSV "americano": comas entre campos, punto decimal, cabecera en la primera línea. Los CSV españoles suelen usar `;` y coma decimal, y hay que decírselo:

```
estacion;pais;dia;valor
Windhoek;NA;1;31,5
Madrid;ES;1;14,2
Oslo;NO;1;NA
...
```

```python
pd.read_csv(path).columns.tolist()          # ['estacion;pais;dia;valor']: una sola columna
pd.read_csv(path, sep=";")["valor"].dtype   # str: "31,5" no es un número para pandas
pd.read_csv(path, sep=";", decimal=",")["valor"].dtype   # float64
```

Y ahora la trampa. Windhoek está en Namibia, cuyo código de país es `NA`:

```python
stations = pd.read_csv(path, sep=";", decimal=",")
stations["pais"].unique().tolist()   # [nan, 'ES', 'PE', 'NO']
```

Namibia ha desaparecido. `read_csv` trata como dato que falta una lista de textos en **cualquier** columna: `""`, `"NA"`, `"N/A"`, `"NULL"`, `"null"`, `"None"`, `"nan"`, `"NaN"` y unos cuantos más. Para que solo `"NA"` en `valor` sea un dato que falta:

```python
stations = pd.read_csv(
    path, sep=";", decimal=",", keep_default_na=False, na_values={"valor": ["NA"]}
)
```

`keep_default_na=False` apaga la lista por defecto, y `na_values` con un dict dice qué texto falta **en qué columna**.

Otros parámetros que usarás:

| Parámetro | Para qué |
|---|---|
| `header=None, names=[...]` | El archivo no tiene cabecera: das tú los nombres |
| `comment="#"` | Ignora lo que va detrás de `#`, como las líneas de comentario de tu `medidas.txt` |
| `dtype={"codigo": "str"}` | No dejes que pandas adivine: un código postal `01001` no es el número 1001 |
| `usecols=[...]` | Lee solo esas columnas |
| `nrows=1000` | Lee solo las primeras filas, para mirar un archivo grande |

---

## 4. Una fila mala lo cambia todo

`read_csv` no se queja si un valor no es un número. Cambia el tipo de **toda** la columna:

```
estacion;pais;dia;valor
Madrid;ES;1;14,2
Lima;PE;1;19,8 C
Oslo;NO;1;2,7
```

```python
broken = pd.read_csv("rota.csv", sep=";", decimal=",")
broken["valor"].dtype     # str
broken["valor"].tolist()  # ['14,2', '19,8 C', '2,7']
```

Una sola fila con `"19,8 C"` y la columna entera es texto, sin aviso. Si después calculas `broken["valor"].mean()`, falla; si comparas con `> 10`, también; y si solo escribes la tabla, nadie se entera.

Para encontrar la culpable, convierte con `errors="coerce"`, que pone NaN donde no puede, y mira qué filas lo tienen:

```python
numbers = pd.to_numeric(broken["valor"].str.replace(",", "."), errors="coerce")
broken[numbers.isna()]    # la fila de Lima
```

Compáralo con tu Observatorio: si le llegara la línea `Lima;19,8 C`, `Series.parse` la apartaría y te diría en qué línea está. pandas es mucho más rápido leyendo (teoría 05), pero no valida por ti. Por eso, después de **cada** `read_csv`, lo primero es mirar los tipos.

---

## 5. Mirar una tabla antes de usarla

Cuatro llamadas que haces siempre con datos nuevos:

```python
stations.head(3)       # las 3 primeras filas (tail: las últimas)
stations.info()        # filas, columnas, tipos, cuántos valores no faltan, memoria
stations.describe()    # resumen de las columnas numéricas
stations.isna().sum()  # cuántos faltan en cada columna
```

```
<class 'pandas.DataFrame'>
RangeIndex: 8 entries, 0 to 7
Data columns (total 4 columns):
 #   Column    Non-Null Count  Dtype
---  ------    --------------  -----
 0   estacion  8 non-null      str
 1   pais      8 non-null      str
 2   dia       8 non-null      int64
 3   valor     7 non-null      float64
dtypes: float64(1), int64(1), str(2)
memory usage: 388.0 bytes
```

`info()` responde las dos preguntas más importantes: ¿cada columna tiene el tipo que espero? ¿Cuántos datos faltan? `describe()` da `count`, `mean`, `std` (con `ddof=1`), mínimo, cuartiles y máximo: lo mismo que tu `stats_of`, para todas las columnas numéricas de una vez.

---

## 6. Columnas: elegir, añadir, renombrar y quitar

```python
stations["valor"]                    # una columna: Series
stations[["estacion", "valor"]]      # varias, con una LISTA: DataFrame
stations["fahrenheit"] = stations["valor"] * 9 / 5 + 32   # nueva, sin bucle
```

La operación se hace sobre la columna entera, como con arrays, y el NaN se propaga: Oslo, sin valor, sale con NaN en `fahrenheit`.

`assign` hace lo mismo pero **devuelve una tabla nueva** y deja la original como estaba:

```python
hot = stations.assign(caliente=stations["valor"] > 25)
"caliente" in stations.columns       # False
```

Es la forma de añadir columnas dentro de una función sin cambiar lo que te pasan, como `with_levels` en tu proyecto.

```python
stations.rename(columns={"valor": "celsius"})   # otra tabla, con la columna renombrada
stations.drop(columns=["pais", "dia"])          # otra tabla, sin esas columnas
```

`rename` y `drop` también devuelven una tabla nueva. Muchos métodos aceptan `inplace=True` para cambiar la original; evítalo: casi nunca ahorra nada y hace más difícil seguir qué variable tiene qué.

---

## 7. Escribir un CSV

```python
stations.to_csv("salida.csv", sep=";", decimal=",", na_rep="NA", index=False)
```

- `sep` y `decimal`, los mismos que al leer.
- `na_rep="NA"`: cómo se escribe un dato que falta (por defecto, nada).
- `index=False`: sin él, pandas escribe el índice como una primera columna sin nombre.

Para comprobar que no se pierde nada, léelo con los mismos parámetros y compara con `equals`, que dice si dos tablas tienen los mismos valores, tipos e índice:

```python
again = pd.read_csv("salida.csv", sep=";", decimal=",", keep_default_na=False, na_values={"valor": ["NA"]})
again.equals(stations)   # True
```

---

## 8. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| `read_csv` con los valores por defecto en un CSV con `;` | Sale una sola columna con todo dentro | `sep=";"` y `decimal=","` |
| No mirar los tipos tras leer | Una fila mala convierte la columna a `str` sin avisar | `info()` o `dtypes` siempre, y `to_numeric(errors="coerce")` para encontrarla |
| Códigos como `NA`, `None` o `null` que desaparecen | Están en la lista de datos que faltan por defecto | `keep_default_na=False` y `na_values` por columna |
| `df["a", "b"]` para dos columnas | Busca una columna llamada `("a", "b")`: `KeyError` | `df[["a", "b"]]`, con una lista |
| Una tabla vacía con columnas `float64` | Sin valores, pandas no sabe el tipo | Crea las columnas con `pd.Series([], dtype=...)` |
| Escribir con `to_csv` sin `index=False` | Aparece una columna más al leerlo | `index=False`, salvo que el índice sea un dato |

---

## ✅ Qué debes saber al terminar

- [ ] Qué es un `DataFrame` y qué relación tiene con `Series`.
- [ ] Crear tablas desde diccionarios, registros y `Series`, con tipos incluso vacías.
- [ ] Leer un CSV con `sep`, `decimal`, `keep_default_na` y `na_values`, y qué hace una fila mala.
- [ ] Qué te dicen `head`, `info`, `describe` e `isna().sum()`.
- [ ] Añadir columnas con una operación o con `assign`, renombrar, quitar y escribir a CSV.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · Series: índice, tipos y alineación](01-series-indice-tipos-y-alineacion.md) | **02 · DataFrames: crear, leer y mirar** | [03 · Seleccionar: loc, iloc y máscaras](03-seleccionar-loc-iloc-y-mascaras.md) |
