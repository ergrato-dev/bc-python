# 03 · Seleccionar: loc, iloc y máscaras

⏱️ 50 min

## 🎯 Objetivos

- Elegir filas y columnas por etiqueta con `.loc` y por posición con `.iloc`, sabiendo dónde acaba cada corte.
- Filtrar filas con máscaras, combinándolas con `&`, `|` y `~`, e `isin` y `between`.
- Prever qué hacen los NaN en un filtro.
- Escribir filtros legibles con `query`.
- Cambiar el índice con `set_index` y `reset_index`, y elegir por él.
- Cambiar los valores de una selección en un solo paso.

---

## 1. Tres formas de elegir filas

Todo lo de esta teoría usa esta tabla, la del ejercicio 03:

```python
READINGS = pd.DataFrame(
    {
        "estacion": ["Norte", "Sur", "Este", "Norte", "Sur", "Este", "Norte", "Sur"],
        "dia": [1, 1, 1, 2, 2, 2, 3, 3],
        "valor": [12.5, 8.0, 48.9, 15.0, np.nan, 52.3, 9.5, 30.1],
    },
    index=pd.RangeIndex(1, 9, name="posicion"),
)
```

El índice va de 1 a 8, como las líneas de un archivo, así que la **etiqueta** 1 está en la **posición** 0. Es a propósito: es el caso en que confundirlas da resultados equivocados sin error.

![La misma tabla con índice 10, 20, 30, 40: loc[20:30] elige las etiquetas 20 y 30, iloc[1:3] las posiciones 1 y 2, y una máscara True, False, True, False elige las filas 10 y 30](../0-assets/03-loc-iloc-y-mascaras.svg)

| Forma | Elige por | Ejemplo |
|---|---|---|
| `.loc[filas, columnas]` | Etiquetas | `READINGS.loc[2:4, ["estacion", "valor"]]` |
| `.iloc[filas, columnas]` | Posiciones | `READINGS.iloc[1:3, [0, 2]]` |
| `df[máscara]` | Una `Series` de `bool` | `READINGS[READINGS["valor"] > 20]` |

---

## 2. `.loc`: por etiqueta

```python
READINGS.loc[1, "valor"]                    # 12.5: la fila de etiqueta 1, la columna valor
READINGS.loc[2:4, ["estacion", "valor"]]    # filas 2, 3 y 4; dos columnas
READINGS.loc[[1, 7], "valor"]               # una lista de etiquetas
READINGS.loc[:, "valor"]                    # todas las filas: la columna, como READINGS["valor"]
```

```
         estacion  valor
posicion
2             Sur    8.0
3            Este   48.9
4           Norte   15.0
```

Con `.loc`, el corte `2:4` **incluye** el 4. Tiene sentido: con etiquetas no hay "siguiente" (¿qué va después de `"Norte"`?), así que pandas incluye las dos que nombras.

Una etiqueta que no existe da `KeyError`:

```python
READINGS.loc[0]    # KeyError: 0
```

---

## 3. `.iloc`: por posición

```python
READINGS.iloc[1, 2]          # 8.0: segunda fila, tercera columna
READINGS.iloc[1:3, [0, 2]]   # posiciones 1 y 2 (no la 3); columnas 0 y 2
READINGS.iloc[-1]            # la última fila
```

```
         estacion  valor
posicion
2             Sur    8.0
3            Este   48.9
```

Con `.iloc`, todo funciona como las listas de Python: empieza en 0 y el corte **excluye** el final. Las etiquetas que ves en la salida (2 y 3) son las de esas filas: la selección conserva el índice.

Para un solo valor hay versiones rápidas: `READINGS.at[1, "valor"]` (etiquetas) y `READINGS.iat[0, 2]` (posiciones).

---

## 4. Máscaras

Una comparación con una columna da una `Series` de `bool` con el mismo índice, y con ella se eligen filas, igual que con los arrays de la semana 23:

```python
high = READINGS["valor"] > 20
high.tolist()        # [False, False, True, False, False, True, False, True]
READINGS[high]       # las filas 3, 6 y 8
```

Para combinar condiciones, los operadores de bits, **cada condición entre paréntesis**:

```python
READINGS[READINGS["estacion"].isin(["Norte", "Sur"]) & (READINGS["valor"] > 10)]   # 1, 4 y 8
READINGS[READINGS["valor"].between(10, 30)]   # 1 y 4: los dos bordes incluidos
READINGS[(READINGS["valor"] < 9) | (READINGS["valor"] > 50)]
```

- `&` es "y", `|` es "o" y `~` es "no".
- `and` y `or` no sirven: Python pide un solo `bool` y la máscara tiene ocho. `ValueError: The truth value of a Series is ambiguous. Use a.empty, a.item(), a.any() or a.all().`
- Los paréntesis hacen falta porque `&` va antes que `>`: sin ellos, `a > 10 & b` se lee `a > (10 & b)`.
- `isin` compara con varios valores a la vez. Es más corto que encadenar `|`.

### NaN en un filtro

Cualquier comparación con NaN da `False`, así que una fila sin valor nunca pasa un filtro por valor. Pero `~` no es lo mismo que la comparación contraria:

```python
READINGS[~high].index.tolist()                      # [1, 2, 4, 5, 7]: la 5 (NaN) está
READINGS[READINGS["valor"] <= 20].index.tolist()    # [1, 2, 4, 7]: la 5 no
```

"No mayor que 20" incluye las que no tienen valor; "menor o igual que 20", no. Decide cuál quieres y, si dudas, quita los NaN antes con `dropna` o `notna()`.

---

## 5. `query`: el filtro como texto

Con varias condiciones, las máscaras se alargan. `query` acepta la condición como texto, con los nombres de las columnas:

```python
READINGS.query("dia == 2 and valor > 20")    # la fila 6
limit = 30
READINGS.query("valor > @limit")              # @ para una variable de Python: 3, 6 y 8
```

Dentro de `query` sí se escriben `and`, `or` y `not`. Es cómodo para explorar en una consola o un *notebook*. En código de un proyecto, las máscaras tienen una ventaja: mypy y ruff las leen, y un nombre de columna mal escrito en un texto solo falla al ejecutarse.

---

## 6. Otro índice

El índice no tiene por qué ser la posición. Si vas a elegir por estación, conviértela en índice:

```python
by_station = READINGS.set_index("estacion")
by_station.loc["Este"]
```

```
          dia  valor
estacion
Este        1   48.9
Este        2   52.3
```

El índice **no tiene por qué ser único**: `"Este"` aparece dos veces, y `.loc["Este"]` devuelve las dos filas, una tabla. Con un índice único habría devuelto una sola fila, como `Series`. `by_station.index.is_unique` te dice en qué caso estás.

```python
by_station.sort_index()       # ordenado por la etiqueta: Este, Este, Norte, Norte...
by_station.reset_index()      # el índice vuelve a ser una columna, y el índice, 0, 1, 2...
```

En tu proyecto, el índice es la **posición** de cada medida, desde 1: la primera medida del archivo es la 1. Así, al filtrar, cada fila sigue diciendo qué medida es, aunque el filtro quite las de alrededor.

---

## 7. Cambiar valores de una selección

Para cambiar algunas filas de una columna, **un solo** `.loc` con la máscara y la columna:

```python
readings.loc[readings["estacion"] == "Norte", "valor"] = 0.0
```

Lo que **no** funciona es encadenar dos selecciones:

```python
readings[readings["estacion"] == "Norte"]["valor"] = 0.0   # no cambia nada
```

```
ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment.
Such chained assignment never works to update the original DataFrame or Series, because the intermediate object on which we are setting values always behaves as a copy (due to Copy-on-Write).
```

La primera selección (`readings[...]`) crea una tabla intermedia, y el `["valor"] = 0.0` cambia **esa** tabla, que nadie guarda. pandas 3 lo detecta y te avisa. La teoría 04 explica por qué.

---

## 8. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| `.loc[0]` con un índice que empieza en 1 | `0` no es ninguna etiqueta: `KeyError` | `.iloc[0]` para la primera |
| Esperar que `.loc[2:4]` excluya el 4 | Con etiquetas, el final se incluye | `.iloc` si piensas en posiciones |
| `(a > 1) and (b < 2)` | `and` no sabe qué hacer con muchos `bool` | `&`, con paréntesis en cada condición |
| `a > 1 & b < 2` sin paréntesis | `&` se calcula antes que las comparaciones | `(a > 1) & (b < 2)` |
| Usar `~(x > 20)` como si fuera `x <= 20` | `~` incluye las filas con NaN | Elige la que quieres, o quita los NaN antes |
| `df[máscara]["col"] = valor` | Cambia una copia intermedia: no hace nada | `df.loc[máscara, "col"] = valor` |
| Un nombre de columna mal escrito en `query` | Solo falla al ejecutarse | Máscaras en el código del proyecto; `query` para explorar |

---

## ✅ Qué debes saber al terminar

- [ ] La diferencia entre `.loc` y `.iloc`, y dónde acaba un corte con cada uno.
- [ ] Filtrar con máscaras, `&`, `|`, `~`, `isin` y `between`, con los paréntesis en su sitio.
- [ ] Qué pasa con las filas sin valor al filtrar, y la diferencia entre `~(x > 20)` y `x <= 20`.
- [ ] Usar `query` con `@variable`, y cuándo prefieres una máscara.
- [ ] Qué hacen `set_index`, `reset_index` y `sort_index`, y qué devuelve `.loc` con un índice repetido.
- [ ] Cambiar valores con un solo `.loc`, y por qué falla la asignación encadenada.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · DataFrames: crear, leer y mirar](02-dataframes-crear-leer-y-mirar.md) | **03 · Seleccionar: loc, iloc y máscaras** | [04 · Ordenar, contar y copy-on-write](04-ordenar-contar-y-copy-on-write.md) |
