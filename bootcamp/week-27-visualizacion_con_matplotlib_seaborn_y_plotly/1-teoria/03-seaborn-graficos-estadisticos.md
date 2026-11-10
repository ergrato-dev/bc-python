# 03 · seaborn: gráficos estadísticos

⏱️ 45 min

## 🎯 Objetivos

- Explicar qué añade seaborn a matplotlib, y qué sigue siendo de matplotlib.
- Preparar los datos en formato largo y describir el gráfico con nombres de columna.
- Distinguir las funciones de ejes de las de figura.
- Leer lo que seaborn calcula por ti: medias, intervalos de confianza, densidades.
- Cambiar el tema y la paleta sin cambiar los gráficos de todo el programa.

---

## 1. Una capa sobre matplotlib

Para dibujar cinco estaciones con matplotlib escribes un bucle: filtrar cada estación, llamar a `plot`, darle un nombre, y al final la leyenda. Para la media de cada hora con su incertidumbre, además, agrupas y calculas tú.

seaborn hace las dos cosas a partir de una **descripción**:

```python
import seaborn as sns

sns.lineplot(data=readings, x="hour", y="value", hue="station", ax=axes)
```

"De la tabla `readings`, pon `hour` en el eje x, `value` en el y, y un color por cada `station`". seaborn agrupa, calcula la media de cada hora, dibuja una línea por estación con su banda de confianza, elige los colores y pone la leyenda.

Debajo, todo es matplotlib: `lineplot` dibuja en unos `Axes`, crea `Line2D` y te devuelve los mismos `Axes`. Puedes seguir con `axes.set(...)`, guardar con `figure.savefig` e inspeccionar los artistas como en la teoría 01.

---

## 2. Datos largos

seaborn quiere una tabla **larga** (*tidy*): una fila por observación y una columna por variable.

```
ancha                                    larga
time    Norte  Sur   Este                time    station  value
08:00   12.5   8.0   30.0                08:00   Norte    12.5
09:00   48.9   9.5   NaN                 08:00   Sur       8.0
                                         08:00   Este     30.0
                                         09:00   Norte    48.9
                                         ...
```

- La **ancha** es la que sale de `pivot`, la de tu `evolucion`: cómoda para leerla y para matplotlib, una columna por línea.
- La **larga** es la de tus medidas: cada fila dice qué se midió (`station`), cuándo (`time`) y cuánto (`value`). seaborn y plotly express la necesitan para poder decir `hue="station"`.
- `frame.melt(id_vars="time", var_name="station", value_name="value")` pasa de ancha a larga; `pivot`, al revés.

---

## 3. Qué pintar y cómo

| Argumento | Qué decide |
|---|---|
| `x`, `y` | Las columnas de cada eje |
| `hue` | Un color por valor de esa columna |
| `style`, `size` | Un tipo de línea o marcador, un tamaño, por valor |
| `col`, `row` | Un panel por valor (solo en las funciones de figura) |
| `palette` | Los colores: `"colorblind"`, `"viridis"`, una lista... |
| `errorbar` | La incertidumbre: `("ci", 95)`, `"sd"`, `None` |

### Lo que calcula

Cuando hay varias filas con el mismo `x` (30 medidas del Norte a las 15 h), `lineplot` y `barplot` dibujan su **media** y una banda o una barra de error:

- `errorbar=("ci", 95)`: el **intervalo de confianza del 95 %** de la media. seaborn lo calcula con *bootstrap*: remuestrea los datos mil veces al azar y mira cuánto varía la media. Como es al azar, cambia un poco en cada ejecución salvo que fijes `seed=`.
- `errorbar="sd"`: la desviación típica, cuánto varían los datos (no la media).
- `errorbar=None`: solo la media.

Son cosas distintas: con muchos datos, el intervalo de la media es estrecho aunque los datos varíen mucho. Dilo en el gráfico, porque quien lo lee no sabe qué banda es. La semana 28 explica qué significa de verdad un intervalo de confianza.

seaborn deja fuera los `NaN` sin avisar, como `hist`.

---

## 4. Funciones de ejes y de figura

| Tipo | Ejemplos | Dibuja en | Devuelve |
|---|---|---|---|
| De ejes (*axes-level*) | `lineplot`, `scatterplot`, `histplot`, `boxplot`, `violinplot`, `barplot`, `heatmap` | Los `Axes` que le pasas con `ax=` | Esos `Axes` |
| De figura (*figure-level*) | `relplot`, `displot`, `catplot` | Una figura nueva que crea ella | Un `FacetGrid` |

Las de figura existen para los paneles: `relplot(..., col="station", col_wrap=3)` hace un panel por estación, con los ejes compartidos, en una línea. El `FacetGrid` guarda la figura en `grid.figure` y los ejes en `grid.axes`.

Pero crean esa figura con `pyplot`: queda en su lista global hasta que la cierras con `plt.close(grid.figure)`, y no aceptan `ax=` (si se lo pasas, avisan y lo ignoran). En un programa, usa las de ejes con tu `Figure`; las de figura, para explorar.

Cada función de figura agrupa varias de ejes con `kind=`:

| Figura | `kind=` | Equivale a |
|---|---|---|
| `relplot` | `"scatter"`, `"line"` | `scatterplot`, `lineplot` |
| `displot` | `"hist"`, `"kde"`, `"ecdf"` | `histplot`, `kdeplot`, `ecdfplot` |
| `catplot` | `"strip"`, `"box"`, `"violin"`, `"bar"`... | `stripplot`, `boxplot`, `violinplot`, `barplot` |

---

## 5. Distribuciones

| Función | Dibuja |
|---|---|
| `histplot(x="value", hue="station")` | Histogramas, uno por grupo. `stat="density"` para comparar grupos de distinto tamaño; `element="step"` para que no se tapen |
| `kdeplot` | Una curva suave estimada a partir de los datos. Bonita, pero inventa forma donde hay pocos datos |
| `boxplot` | Cajas: mediana, cuartiles, bigotes y valores sueltos |
| `violinplot(inner="quart")` | Una caja con la forma de la distribución a los lados |
| `ecdfplot` | Qué fracción de los datos queda por debajo de cada valor. Sin parámetros que elegir |

---

## 6. Temas, paletas y estado global

| Llamada | Alcance |
|---|---|
| `sns.set_theme()` | **Global**: cambia `matplotlib.rcParams`, y todos los gráficos del programa, también los que no son de seaborn |
| `with sns.axes_style("whitegrid"):` | Solo lo que dibujas dentro del `with` |
| `with sns.plotting_context("talk"):` | Igual, para los tamaños de letra: `paper`, `notebook`, `talk`, `poster` |
| `palette="colorblind"` en una llamada | Solo ese gráfico |

`import seaborn` ya no cambia nada desde la versión 0.8; `set_theme` sí. En un *notebook* es cómodo; en una biblioteca o en tu proyecto cambiaría los gráficos de otras partes del programa. Usa los `with`, o pasa `palette` en cada llamada.

---

## 7. Un proyecto con poca actividad

La última versión de seaborn es la 0.13.2, de enero de 2024. Funciona con pandas 3 y matplotlib 3.11, pero algunas funciones usan opciones que matplotlib ya marca como obsoletas: `sns.boxplot` escribe `MatplotlibDeprecationWarning: vert: bool was deprecated in Matplotlib 3.11 and will be removed in 3.13`. No es un error tuyo, y hoy no rompe nada; dentro de dos versiones de matplotlib, puede.

Es lo que miras antes de añadir una dependencia a un proyecto (semana 8): cuándo salió la última versión, si alguien la mantiene y qué pasa si deja de funcionar. Para explorar, seaborn sigue siendo muy útil. En tu proyecto, matplotlib basta, y no depende de que seaborn publique una versión nueva.

---

## 8. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| Pasar la tabla ancha con `hue=` | seaborn no encuentra la columna | `melt` a formato largo |
| `relplot(..., ax=axes)` | Las funciones de figura crean su figura | `lineplot(..., ax=axes)` |
| No cerrar la figura de `relplot` en un bucle | Se acumula en `pyplot` | `plt.close(grid.figure)` |
| `sns.set_theme()` en código que importa otra gente | Cambia todos sus gráficos | `with sns.axes_style(...)` |
| Dejar la banda sin explicar | No se sabe si es la confianza o la dispersión | Dilo en el título, o `errorbar="sd"` si quieres la dispersión |
| Confiar en `kdeplot` con pocos datos | La curva se inventa la forma | `histplot` o `ecdfplot` |
| Bandas que cambian en cada ejecución | El *bootstrap* es aleatorio | `seed=` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué hace seaborn por ti, y que debajo los artistas son de matplotlib.
- [ ] Qué es una tabla larga, y cómo pasar de ancha a larga.
- [ ] Qué dibuja `lineplot` cuando hay varias filas por cada `x`, y qué es su banda.
- [ ] Qué diferencia hay entre una función de ejes y una de figura.
- [ ] Qué cambia `set_theme`, y cómo cambiar el tema solo para un gráfico.
- [ ] Qué mirar en una dependencia antes de añadirla.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Elegir el gráfico y contarlo bien](02-elegir-el-grafico-y-contarlo-bien.md) | **03 · seaborn: gráficos estadísticos** | [04 · plotly: gráficos interactivos](04-plotly-graficos-interactivos.md) |
