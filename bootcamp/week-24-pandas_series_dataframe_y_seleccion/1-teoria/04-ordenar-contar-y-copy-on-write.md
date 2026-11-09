# 04 · Ordenar, contar y copy-on-write

⏱️ 45 min

## 🎯 Objetivos

- Ordenar por una o varias columnas, decidir dónde van los NaN y conservar el orden de los empates.
- Contar valores con `value_counts` y sacar los mayores con `nlargest`.
- Convertir números en categorías con `pd.cut`, sin bucle, con los bordes en su sitio.
- Explicar *copy-on-write*: por qué una selección se comporta como una copia, y por qué no cuesta memoria.
- Escribir funciones que reciben una tabla y devuelven otra sin cambiar la que les pasan.

---

## 1. Ordenar

```python
READINGS.sort_values("valor", ascending=False).index.tolist()
# [6, 3, 8, 4, 1, 7, 2, 5]: de mayor a menor; la 5 (NaN) al final
READINGS.sort_values("valor", na_position="first").index.tolist()
# [5, 2, 7, 1, 4, 8, 3, 6]: los NaN delante
READINGS.sort_values(["estacion", "valor"], ascending=[True, False]).index.tolist()
# [6, 3, 4, 1, 7, 8, 2, 5]: por estación A-Z y, dentro de cada una, de mayor a menor
```

Los NaN van al final por defecto, subas o bajes. `sort_index()` ordena por la etiqueta, y las dos devuelven una tabla **nueva**: el índice viaja con cada fila, así que la fila 6 sigue siendo la 6.

Para "los N mayores" hay un atajo que no ordena la tabla entera:

```python
READINGS.nlargest(2, "valor")    # las filas 6 y 3
READINGS.nsmallest(2, "valor")
```

### Los empates

Con valores repetidos, ¿en qué orden quedan? Depende del algoritmo. El de por defecto (`quicksort`) es rápido pero **no estable**: no garantiza que dos filas con el mismo valor conserven su orden. Con pocas filas parece que sí; con más, no:

```python
ties = pd.DataFrame({"valor": [1.0, 2.0, 1.0] * 20}, index=range(60))
ties.sort_values("valor").index[:6].tolist()                  # [0, 2, 3, 5, 6, 11]
ties.sort_values("valor", kind="stable").index[:6].tolist()   # [0, 2, 3, 5, 6, 8]
```

Con `quicksort`, la fila 11 se ha colado delante de la 8, aunque las dos valen 1.0. Si el orden de los empates importa (en tu proyecto, que dos medidas iguales salgan en el orden del archivo), pide `kind="stable"`. Un test con 100 filas lo vigila: con cuatro filas, el mutante que lo quita sobrevive.

---

## 2. Contar

`value_counts` cuenta cuántas veces aparece cada valor, de más a menos:

```python
labels = pd.Series(["Norte", "Sur", "Norte", "Este", None])
labels.value_counts()                 # Norte 2, Sur 1, Este 1
labels.value_counts(dropna=False)     # y nan 1
labels.value_counts(normalize=True)   # Norte 0.5, Sur 0.25, Este 0.25: proporciones
```

Los que faltan no se cuentan, salvo que pidas `dropna=False`. Con `normalize=True` da proporciones, que suman 1 sin contar los que faltan.

¿Y los empates? `Sur` y `Este` tienen 1 cada uno. En la práctica, `value_counts` los deja en el orden en que aparecen, como `Counter.most_common`, pero la documentación no lo promete. Tu `label_counts` lo da por bueno y un test con Hypothesis lo compara con `Series.most_common`: si una versión futura de pandas lo cambia, ese test te lo dirá.

Para contar por columnas de una tabla entera, `df["estacion"].value_counts()`. Contar por **grupos** con varias medidas a la vez (media, máximo...) es `groupby`, la semana que viene.

---

## 3. De números a categorías

Tu `Scale.level` decide el nivel de un valor con un `if` por medida. `pd.cut` lo hace con la columna entera:

```python
cut = pd.cut(
    frame["value"],
    bins=[-np.inf, 10, 50, np.inf],
    labels=["bajo", "medio", "alto"],
    right=False,
)
```

- `bins` son los bordes: tres intervalos, de −∞ a 10, de 10 a 50 y de 50 a ∞.
- `labels`, el nombre de cada intervalo.
- `right=False` hace que cada intervalo incluya su borde **izquierdo**: `[10, 50)`. Así, 10 ya es `"medio"` y 50 ya es `"alto"`, como en `classify`. Con el valor por defecto, `right=True`, el intervalo sería `(10, 50]`: 10 sería `"bajo"` y 50 `"medio"`.

```
valores:          [12.5,    8.0,    NaN,  50.0,    10.0]
right=True:       ['medio', 'bajo', nan, 'medio', 'bajo']
right=False:      ['medio', 'bajo', nan, 'alto',  'medio']
```

Un error de bordes como ese no da ningún error: da niveles equivocados en las medidas que caen justo en el borde. Por eso tu proyecto compara `with_levels` con `Scale.level` con Hypothesis, y prueba los cuatro bordes uno a uno.

El resultado de `cut` es de tipo `category`: un tipo de pandas para pocos valores distintos que se repiten. Guarda cada texto una sola vez y, en cada fila, un número pequeño. En el ejercicio 04, una columna de 100 000 etiquetas ocupa 5,36 MB como `str` y 0,10 MB como `category`.

Los NaN siguen siendo NaN. Para convertirlos en `"sin dato"`, pasa a texto y rellena:

```python
cut.astype("str").where(cut.notna(), "sin dato")
```

`where(condición, otro)` deja el valor donde la condición es `True` y pone `otro` donde es `False`. Su pareja, `mask`, hace lo contrario.

---

## 4. Copy-on-write

Hasta pandas 2, una selección **a veces** era una vista (como un corte de NumPy, teoría 02 de la semana 23) y a veces una copia, según cómo la hicieras. Cambiarla podía cambiar o no la tabla original, y pandas avisaba con un `SettingWithCopyWarning` que nadie entendía.

pandas 3 lo resuelve con una regla: **toda tabla o columna que obtienes de otra se comporta como una copia**. Si la cambias, la original no cambia. Nunca.

```python
readings = READINGS.copy()
north = readings[readings["estacion"] == "Norte"]
north["valor"] = 0.0
north["valor"].tolist()                                            # [0.0, 0.0, 0.0]
readings.loc[readings["estacion"] == "Norte", "valor"].tolist()    # [12.5, 15.0, 9.5]
```

¿Y no es muy caro copiar cada selección? No copia: el nombre lo dice, *copy-on-write*, copia **al escribir**. Mientras solo lees, la selección comparte los datos con la original; la copia se hace en el momento en que una de las dos cambia, y solo de lo que cambia.

Dos consecuencias que verás:

- La asignación encadenada, `df[máscara]["col"] = valor`, nunca funciona (teoría 03, sección 7): el primer `[]` da una tabla que se comporta como una copia.
- `to_numpy()` puede darte el array **compartido**, y para protegerlo pandas lo marca como de solo lectura: `arr[0] = 5` da `ValueError: assignment destination is read-only`. Si de verdad quieres cambiarlo, `to_numpy().copy()`.

---

## 5. Funciones que no cambian lo que reciben

Con *copy-on-write*, la forma natural de escribir funciones sobre tablas es la misma que con tus `Series` y tus *dataclasses* inmutables: recibir una tabla y **devolver otra**.

```python
def with_levels(frame: pd.DataFrame, scale: Scale) -> pd.DataFrame:
    """Una copia con la columna level."""
    ...
    return frame.assign(level=levels)
```

- `assign`, `sort_values`, `rename`, `drop`, `loc[...]` y `query` devuelven tablas nuevas.
- `frame["level"] = ...` dentro de la función **sí** cambiaría la tabla del que llama. Funciona, pero es una sorpresa para quien la usa; un test como `test_with_levels_does_not_change_the_frame` lo detecta.

Encadenadas, se leen de arriba abajo:

```python
chosen = by_value(select(with_levels(frame_of(series), SCALE), labels=["Norte"], low=10))
```

---

## 6. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| Esperar que los empates conserven su orden | `quicksort` no es estable | `kind="stable"` |
| `pd.cut` sin `right=False` para umbrales "desde" | El borde cae en el intervalo de abajo | `right=False`, y prueba los bordes |
| Comparar el resultado de `cut` con texto sin convertir | Es `category` y los NaN no son `"sin dato"` | `astype("str").where(...)` |
| `df[máscara]["col"] = valor` | Cambia una copia: no hace nada | `df.loc[máscara, "col"] = valor` |
| Escribir en el array de `to_numpy()` | Es de solo lectura: `ValueError` | `to_numpy().copy()` |
| `frame["nueva"] = ...` dentro de una función | Cambia la tabla del que llama | `return frame.assign(nueva=...)` |
| Fiarse de un orden que la documentación no promete | Puede cambiar en otra versión | Un test que lo compruebe |

---

## ✅ Qué debes saber al terminar

- [ ] Ordenar por una o varias columnas, colocar los NaN y conservar los empates con `kind="stable"`.
- [ ] Contar con `value_counts` (`dropna`, `normalize`) y elegir los mayores con `nlargest`.
- [ ] Categorizar con `pd.cut`: `bins`, `labels`, `right` y qué pasa en los bordes.
- [ ] Qué es *copy-on-write*, por qué no cuesta memoria y qué consecuencias tiene.
- [ ] Escribir funciones que devuelven una tabla nueva en lugar de cambiar la que reciben.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Seleccionar: loc, iloc y máscaras](03-seleccionar-loc-iloc-y-mascaras.md) | **04 · Ordenar, contar y copy-on-write** | [05 · pandas en un proyecto](05-pandas-en-un-proyecto.md) |
