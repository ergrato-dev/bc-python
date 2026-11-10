# Ejercicio 01 — matplotlib: figuras y ejes

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-matplotlib-figuras-ejes-y-artistas.md)

## Objetivo

Dibujar con matplotlib sabiendo qué objeto hace cada cosa:

- una `Figure`, unos `Axes` y una línea, y lo que guarda cada uno;
- qué recuerda `pyplot` y por qué en un programa conviene no usarlo;
- cuatro tipos de gráfico para cuatro preguntas distintas;
- títulos, ejes, una línea de referencia, una anotación y una leyenda que no tapa nada;
- el mismo gráfico en PNG con dos resoluciones, en SVG y en PDF.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-27-visualizacion_con_matplotlib_seaborn_y_plotly/2-practicas/ejercicio-01-matplotlib-figuras-y-ejes/starter
uv run python main.py
```

```
Ejercicio 01 · matplotlib
```

`readings` son treinta días de medidas, una por hora, de cinco estaciones: la temperatura sube de día y baja de noche, cada estación a su nivel, con ruido y un 5 % sin valor. Las genera NumPy con la semilla 27, así que salen siempre las mismas. `norte` son las del Norte, con el tiempo como índice. Cada ejecución borra la carpeta `salida/` y la vuelve a crear: ahí van los gráficos. **Ábrelos** después de cada paso, porque es la parte del ejercicio que la terminal no enseña.

## Pasos

### 1. Una figura, unos ejes, una línea

Descomenta el **PASO 1** y ejecuta:

```
                 time station  value
0 2026-11-01 00:00:00   Norte   15.6
1 2026-11-01 01:00:00   Norte   14.0
2 2026-11-01 02:00:00   Norte    NaN
medidas: 3600 · sin valor: 213
Figure(800x400)
Axes(0.125,0.11;0.775x0.77)
Line2D(_child0)
x: ['2026-11-01T00:00:00.000000' '2026-11-01T01:00:00.000000']
y: [15.6 14.   nan 10.4]
hijos de los ejes: 11
01-una-linea.png: 32.8 kB
```

- `Figure(figsize=(8, 4))` es el lienzo: 8 × 4 pulgadas, que a 100 puntos por pulgada son 800 × 400 píxeles.
- `add_subplot()` añade unos **ejes** (`Axes`): un gráfico con su eje x, su eje y y su zona de dibujo. Los números de `Axes(...)` dicen dónde está dentro de la figura, en fracciones de su ancho y su alto.
- `plot` devuelve una lista de líneas; `(line,) = ...` saca la única que hay. La línea **guarda los datos**: `get_xdata()` y `get_ydata()` devuelven lo que le diste, `NaN` incluido. Los tests del proyecto miran justo esto.
- Los ejes tienen 11 hijos: la línea, los dos ejes, el título, el fondo, los bordes... Todo lo que se ve en un gráfico es un **artista**.
- Abre `01-una-linea.png`: la línea se corta donde hay `NaN`. matplotlib no se inventa el dato que falta.

### 2. pyplot recuerda cada figura

Descomenta el **PASO 2** y ejecuta:

```
figuras abiertas en pyplot: [1, 2, 3]
el título fue a: la última figura · figura 3
después de close: []
¿y la del paso 1? no es de pyplot
```

- `matplotlib.use("Agg")` elige un *backend* que solo dibuja en archivos, sin abrir ventanas. Sin esa línea, en un ordenador con pantalla, `pyplot` podría intentar abrir una.
- `plt.figure()` crea una figura **y la guarda** en una lista global. `plt.plot` y `plt.title` no dicen en qué figura dibujan: usan "la actual", la última que creaste. Con tres figuras, es fácil escribir en la que no querías.
- Esas figuras viven hasta que llamas a `plt.close`. En un programa que dibuja mil gráficos en un bucle, sin `close`, la memoria crece sin parar, y matplotlib avisa cuando pasas de 20 abiertas.
- La `Figure` del paso 1 no está en esa lista: la creaste tú, y Python la borra cuando ya nadie la usa. Es lo que hace tu proyecto.

### 3. Cuatro gráficos, cuatro preguntas

Descomenta el **PASO 3** y ejecuta:

```
['¿Cómo cambia? Norte, tres días', '¿Cómo se reparten? Todas las medidas', '¿Cuál es mayor? Media por estación', '¿Qué relación hay? Valor y hora del día']
barras: 5 · puntos: 3600
medidas en el histograma: 3387
03-cuatro-preguntas.png: 110.5 kB
```

- `subplots(2, 2)` crea cuatro ejes en una rejilla y los devuelve en dos filas. `layout="constrained"` los separa para que los títulos no se pisen.
- Cada gráfico responde a una pregunta: una línea para lo que cambia con el tiempo, un histograma para cómo se reparten los valores, barras para comparar cantidades y puntos para la relación entre dos variables. La teoría 02 tiene la tabla completa.
- El diagrama de puntos recibe las 3600 medidas, pero no dibuja los 213 `NaN`. Al histograma le das los valores sin `NaN` (`dropna()`), y la suma de sus barras es 3387: 3600 − 213.
- Abre el PNG: el diagrama de puntos enseña lo que la línea solo insinuaba. El máximo llega hacia las 15 h, y el mínimo de madrugada.

### 4. Que se entienda sin explicarlo

Descomenta el **PASO 4** y ejecuta:

```
máximo: 2026-11-04 15:00:00 26.0
límites y: [7.9, 26.9]
leyenda: ['Norte', 'umbral 25']
04-con-sentido.png: 62.6 kB
```

- El título, los nombres de los ejes **con su unidad**, una línea de referencia (`axhline`) y una anotación en el máximo. Quien ve el gráfico no necesita que se lo expliques.
- `DayLocator` pone una marca por día, y `ConciseDateFormatter` escribe las fechas sin repetir el mes en cada una: `Nov`, `02`, `03`... y `2026-Nov` una sola vez, abajo.
- matplotlib elige los límites del eje y a partir de los datos, con un margen del 5 %. En una línea está bien que no empiece en cero (el ejercicio 02 lo compara con las barras).
- `figure.legend(loc="outside right upper")` pone la leyenda **fuera** de los ejes, y `constrained` les hace sitio. Dentro, tapaba justo los valores de la última noche.

### 5. PNG, SVG y PDF

Descomenta el **PASO 5** y ejecuta:

```
05-dpi-100.png: 62.6 kB
05-dpi-200.png: 142.2 kB
05-figura.svg: 54.8 kB
05-figura.pdf: 18.4 kB
píxeles a 200 dpi: 1800 x 800
elementos <text> en el SVG: 0
05-texto.svg: 36.1 kB
¿y ahora? 22
```

- `savefig` elige el formato por la extensión. El **PNG** es una imagen de píxeles: con `dpi=200` tiene el doble de ancho y de alto, cuatro veces más píxeles, y pesa más del doble.
- El **SVG** y el **PDF** son **vectoriales**: guardan líneas y textos, no píxeles, y se ven nítidos a cualquier tamaño. Úsalos para un informe o una web; el PNG, para un mensaje o una diapositiva.
- Por defecto, matplotlib dibuja cada letra del SVG como una forma: se ve igual en cualquier ordenador, pero no se puede buscar ni copiar el texto, y un lector de pantalla no lo lee. Con `svg.fonttype: "none"` el texto sigue siendo texto, y el archivo pesa un tercio menos.
- `rc_context` cambia la configuración **solo** dentro del `with`. Es lo que hace `save` en tu proyecto.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'matplotlib'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| Se abre una ventana, o sale un aviso de Tk o Qt en el paso 2 | Falta `matplotlib.use("Agg")` antes de `import matplotlib.pyplot` |
| `ValueError: not enough values to unpack` en el paso 3 | `subplots(2, 2)` devuelve dos filas de dos ejes: `(a, b), (c, d) = ...` |
| Las fechas del paso 4 se pisan | Falta `ConciseDateFormatter`, o lo pusiste antes del `DayLocator` |
| `AttributeError: 'NoneType' object has no attribute 'get_texts'` | La leyenda está en la figura, no en los ejes: `figure.legends[0]` |
| Tus tamaños de archivo no coinciden exactamente | Cambian un poco con la versión de matplotlib; con `matplotlib==3.11.2` deberían ser los del README |
| No ves los gráficos | Están en `starter/salida/`: ábrelos con el explorador de archivos o con `code salida/` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Gráficos en un proyecto](../../1-teoria/05-graficos-en-un-proyecto.md) | **Ejercicio 01 · matplotlib: figuras y ejes** | [Ejercicio 02 · Elegir el gráfico](../ejercicio-02-elegir-el-grafico/README.md) |
