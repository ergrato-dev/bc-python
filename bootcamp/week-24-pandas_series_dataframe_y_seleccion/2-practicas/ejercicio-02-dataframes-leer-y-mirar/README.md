# Ejercicio 02 — DataFrames: leer y mirar

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-dataframes-crear-leer-y-mirar.md)

## Objetivo

Una tabla entera, de principio a fin:

- crear un `DataFrame` y ver su forma, sus columnas y sus tipos;
- leer un CSV con `;` y coma decimal, y no perder a Namibia;
- mirar la tabla con `head`, `info` y `describe`;
- añadir, renombrar y quitar columnas;
- encontrar la fila que estropea una columna entera;
- escribirla y leerla otra vez sin perder nada.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-24-pandas_series_dataframe_y_seleccion/2-practicas/ejercicio-02-dataframes-leer-y-mirar/starter
uv run python main.py
```

```
Ejercicio 02 · DataFrames: leer y mirar
```

En `starter/` hay dos CSV. Ábrelos antes de empezar: `estaciones.csv` (8 filas, cuatro estaciones en dos días) y `rota.csv` (3 filas, una con un error).

## Pasos

### 1. Una tabla desde un diccionario

Descomenta el **PASO 1** y ejecuta:

```
  estacion  valor  sensores
0    Norte   12.5         3
1      Sur    8.0         1
2     Este   48.9         2
forma: (3, 3) · columnas: ['estacion', 'valor', 'sensores']
estacion        str
valor       float64
sensores      int64
dtype: object
una columna es una Series: Series
```

Cada clave del diccionario es una columna, y cada columna tiene su tipo. `shape` no cuenta el índice. Al elegir una columna con `table["valor"]` obtienes una `Series` como las del ejercicio 01.

### 2. Leer un CSV, a la tercera

Descomenta el **PASO 2** y ejecuta:

```
sin sep: ['estacion;pais;dia;valor']
con sep: str
con decimal: float64
países que faltan: 2 · [nan, 'ES', 'PE', 'NO']
bien: ['NA', 'ES', 'PE', 'NO'] · valores que faltan: 1
```

1. Sin `sep`, `read_csv` separa por comas: una sola columna con todo dentro.
2. Con `sep=";"`, `valor` es texto: `"31,5"` no es un número con punto decimal.
3. Con `decimal=","`, `valor` es `float64`. Pero Windhoek tiene el país `NA` (Namibia), que está en la lista de textos que `read_csv` trata como dato que falta en **cualquier** columna: dos filas sin país.
4. Con `keep_default_na=False` se apaga esa lista, y con `na_values={"valor": ["NA"]}` solo `NA` en `valor` es un dato que falta: el de Oslo.

### 3. Mirar una tabla antes de usarla

Descomenta el **PASO 3** y ejecuta:

```
   estacion pais  dia  valor
0  Windhoek   NA    1   31.5
1    Madrid   ES    1   14.2
2      Lima   PE    1   19.8
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
            dia      valor
count  8.000000   7.000000
mean   1.500000  19.528571
std    0.534522  10.462905
min    1.000000   2.700000
25%    1.000000  14.650000
50%    1.500000  19.800000
75%    2.000000  25.950000
max    2.000000  33.000000
```

`info()` escribe por sí misma (no hace falta `print`) y responde: ¿qué tipo tiene cada columna? ¿Cuántos valores no faltan? `valor` tiene 7 de 8.

`describe()` resume las columnas numéricas. Fíjate en `dia`: su "media" de 1.5 no significa nada, es un número que en realidad es una etiqueta. pandas no lo sabe; tú sí. En la semana 25 lo convertirás en fecha.

### 4. Columnas nuevas, con otro nombre o fuera

Descomenta el **PASO 4** y ejecuta:

```
  estacion  valor
6     Lima   20.4
7     Oslo    2.7
[88.7, 57.6, 67.6, nan, 91.4, 59.2, 68.7, 36.9]
caliente: [True, False, False, False, True, False, False, False]
¿assign cambió stations? False
   estacion  celsius  fahrenheit
0  Windhoek     31.5       88.70
1    Madrid     14.2       57.56
```

- Dos columnas, con una **lista**: `stations[["estacion", "valor"]]`.
- `stations["fahrenheit"] = ...` crea una columna con una operación sobre la columna entera. Oslo, sin valor, sale con NaN.
- `assign` devuelve una tabla nueva: `stations` no tiene `caliente`.
- `rename` y `drop` también devuelven tablas nuevas, y se encadenan.

### 5. Una fila mala lo cambia todo

Descomenta el **PASO 5** y ejecuta:

```
tipo de valor: str · ['14,2', '19,8 C', '2,7']
convertidos: [14.2, nan, 2.7]
  estacion pais  dia   valor
1     Lima   PE    1  19,8 C
```

Una sola celda con `"19,8 C"` y la columna entera es texto, sin error ni aviso; ni siquiera se aplicó `decimal=","` en las otras. `pd.to_numeric(..., errors="coerce")` convierte lo que puede y pone NaN en lo demás, y la máscara `numbers.isna()` señala la fila culpable.

Tu Observatorio no tiene este problema: `Series.parse` valida cada línea y te dice cuál está mal.

### 6. Escribirla y leerla otra vez

Descomenta el **PASO 6** y ejecuta:

```
['estacion;pais;dia;valor', 'Windhoek;NA;1;31,5', 'Madrid;ES;1;14,2']
¿igual? True
```

`to_csv` con el mismo `sep` y `decimal` que al leer, `na_rep="NA"` para el dato que falta e `index=False` para no añadir una columna con el índice. Leído con los mismos parámetros, `equals` confirma que valores, tipos e índice son los mismos. El paso escribe `salida.csv` en `starter/`: bórralo cuando acabes.

Prueba a quitar `index=False` y mira la primera línea de `salida.csv`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `FileNotFoundError: ... 'estaciones.csv'` | Ejecuta desde `starter/`, donde están los CSV |
| `con decimal: str` | Has tocado `estaciones.csv`: alguna celda de `valor` ya no es un número |
| `países que faltan: 0` en el paso 2 | Ya has pasado `keep_default_na=False` en la primera lectura: el paso compara las dos |
| `NameError: name 'stations' is not defined` | Descomenta también el paso 2 |
| `¿igual? False` | Lees `salida.csv` sin `keep_default_na=False` (Namibia vuelve a faltar) o sin `na_values` |
| `KeyError: "['pais'] not found in axis"` | Has ejecutado el `drop` sobre una tabla que ya no tenía esa columna |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Series, índice y tipos](../ejercicio-01-series-indice-y-tipos/README.md) | **Ejercicio 02 · DataFrames: leer y mirar** | [Ejercicio 03 · Seleccionar con loc, iloc y máscaras](../ejercicio-03-seleccionar-con-loc-iloc-y-mascaras/README.md) |
