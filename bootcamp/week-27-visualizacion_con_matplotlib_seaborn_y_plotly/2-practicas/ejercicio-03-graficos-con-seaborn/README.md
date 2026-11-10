# Ejercicio 03 — Gráficos con seaborn

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-seaborn-graficos-estadisticos.md)

## Objetivo

Dejar que seaborn agrupe, calcule y coloree por ti, sin perder de vista que debajo sigue matplotlib:

- datos anchos y datos largos, y por qué seaborn quiere los largos;
- una línea por estación con su intervalo de confianza, en unos ejes tuyos;
- distribuciones por grupo: histogramas y violines;
- paneles con una sola llamada, y la figura de `pyplot` que crean;
- temas y paletas, con y sin estado global.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-27-visualizacion_con_matplotlib_seaborn_y_plotly/2-practicas/ejercicio-03-graficos-con-seaborn/starter
uv run python main.py
```

```
Ejercicio 03 · seaborn
```

Son las mismas medidas de los ejercicios 01 y 02, con una columna más, `hour`, la hora del día de cada medida. Los gráficos van a `salida/`.

## Pasos

### 1. Datos anchos y datos largos

Descomenta el **PASO 1** y ejecuta:

```
ancha: (720, 5) ['Centro', 'Este', 'Norte', 'Oeste', 'Sur']
larga: (3600, 3) ['time', 'station', 'value']
                 time station  value
0 2026-11-01 00:00:00  Centro   14.6
1 2026-11-01 01:00:00  Centro   15.3
2 2026-11-01 02:00:00  Centro    NaN
¿las mismas medidas? True
```

- **Ancha**: una fila por momento y una columna por estación, como la tabla de `evolucion` de tu proyecto. Cómoda para leer y para `pivot`.
- **Larga**: una fila por medida, con columnas para lo que la describe (`time`, `station`) y una para el valor. `melt` pasa de ancha a larga; `pivot`, al revés.
- seaborn pide la tabla **larga** y nombres de columna: `x="hour"`, `y="value"`, `hue="station"`. Con eso decide qué agrupar y de qué color pintar cada grupo, sin bucles.
- Las dos tablas tienen las mismas medidas con valor: `count` no cuenta los `NaN`.

### 2. Una línea por grupo, con su incertidumbre

Descomenta el **PASO 2** y ejecuta:

```
¿devuelve los mismos ejes? True
líneas: 10 · con datos: 5
nombres: ['_child0', '_child2', '_child4', '_child6', '_child8', 'Norte', 'Sur', 'Este', 'Oeste', 'Centro']
bandas: 5
Norte a las 15, en el gráfico: 24.09
Norte a las 15, con pandas:    24.09
leyenda: ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
```

- `sns.lineplot(..., ax=axes)` dibuja en **tus** ejes y te los devuelve: es una función de ejes (*axes-level*). La figura sigue siendo tu `Figure`, sin `pyplot`.
- Con 30 medidas de cada estación a cada hora, seaborn dibuja la **media**: el valor del Norte a las 15 es el mismo que da `groupby("hour").mean()`.
- La banda alrededor de cada línea es el **intervalo de confianza del 95 %** de esa media (`errorbar=("ci", 95)`). seaborn lo calcula remuestreando los datos al azar (*bootstrap*); `seed=27` hace que salga siempre igual.
- Hay 10 líneas y solo 5 tienen datos. Las otras 5 están vacías y llevan el nombre de cada estación: seaborn las crea para la **leyenda**. Las de datos se llaman `_child0`, `_child2`...: matplotlib deja fuera de la leyenda todo lo que empieza por `_`. Es el mismo detalle que vigila `test_evolution_figure_legend_keeps_labels_that_start_with_underscore` en tu proyecto.

### 3. Distribuciones por grupo

Descomenta el **PASO 3** y ejecuta:

```
pasos del histograma: 5
violines: 5
NaN que seaborn dejó fuera: 213
```

- `histplot` con `hue` dibuja un histograma por estación, superpuestos. `element="step"` dibuja solo el contorno, para que se vean todos; `stat="density"` hace que el área de cada uno sume 1, y se comparan aunque un grupo tenga más medidas que otro.
- `violinplot` es una caja del ejercicio 02 con la forma de la distribución a cada lado. `inner="quart"` dibuja dentro la mediana y los cuartiles.
- seaborn deja fuera los `NaN` sin avisar. Aquí son 213 de 3600; si fueran la mitad, el gráfico seguiría saliendo igual de bonito. Cuenta lo que falta antes de dibujar.

### 4. Paneles con una sola llamada

Descomenta el **PASO 4** y ejecuta:

```
FacetGrid · Figure · paneles: 5
títulos: ['station = Norte', 'station = Sur', 'station = Este', 'station = Oeste', 'station = Centro']
figuras abiertas en pyplot: [1]
después de close: []
```

- `relplot` con `col="station"` hace los *small multiples* del ejercicio 02 en una llamada: un panel por estación, con los ejes compartidos. `col_wrap=3` pasa a la fila siguiente cada tres paneles.
- Es una función **de figura** (*figure-level*): no recibe `ax=`, crea su propia figura y devuelve un `FacetGrid`, que la guarda en `grid.figure`.
- Esa figura la crea con `pyplot`, y queda en su lista hasta que la cierras. En un programa que dibuja muchas, `plt.close(grid.figure)` después de guardar.
- `autofmt_xdate` inclina las fechas para que no se pisen.

### 5. Temas y paletas

Descomenta el **PASO 5** y ejecuta:

```
fondo antes: white
fondo dentro del with: #EAEAF2
fondo después: white
colorblind: ['#0173b2', '#de8f05', '#029e73', '#d55e00', '#cc78bc']
fondo tras set_theme: #EAEAF2
```

- `sns.axes_style("darkgrid")` dentro de un `with` cambia el fondo y la rejilla solo para lo que dibujas dentro. Al salir, todo vuelve a ser como antes.
- `sns.set_theme()` cambia la configuración **global** de matplotlib: desde ese momento, todos los gráficos del programa, también los que no son de seaborn, salen con el fondo gris. En un script de análisis es cómodo; en una biblioteca o en tu proyecto, cambiaría los gráficos de otros.
- `palette="colorblind"` usa cinco colores que se distinguen con los tipos de daltonismo más comunes. Con `hue="station"` y `x="station"`, cada barra tiene su color.
- `barplot` dibuja la media de cada grupo y su intervalo de confianza en una línea negra encima. Las barras empiezan en cero, como en el ejercicio 02.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'seaborn'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| ``ValueError: Could not interpret value `hour` for `x` `` | Le pasaste la tabla ancha, que no tiene las columnas `hour` ni `station`: seaborn necesita la larga, con una columna por variable |
| Las bandas del paso 2 cambian un poco en cada ejecución | Falta `seed=27`: el *bootstrap* es aleatorio |
| `UserWarning: relplot is a figure-level function and does not accept the ax parameter` | Las funciones de figura no dibujan en tus ejes: usa `lineplot` con `ax=`, o deja que `relplot` cree la figura |
| `figuras abiertas` sale `[]` en el paso 4 | Ya cerraste la figura antes, o no ejecutaste `relplot`: debe ser `[1]` antes de `close` |
| `MatplotlibDeprecationWarning: vert: bool was deprecated` | Usaste `sns.boxplot`: seaborn 0.13.2 (enero de 2024) llama a una opción de matplotlib que la 3.11 marca como obsoleta. No es un error tuyo; la teoría 03 lo explica |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Elegir el gráfico](../ejercicio-02-elegir-el-grafico/README.md) | **Ejercicio 03 · Gráficos con seaborn** | [Ejercicio 04 · plotly, y tres bibliotecas](../ejercicio-04-plotly-y-tres-bibliotecas/README.md) |
