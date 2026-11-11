# Rúbrica de Evaluación — Semana 27: Visualización con matplotlib, seaborn y plotly

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 26 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué es una `Figure`, qué son unos `Axes` y qué es un artista? ¿Qué guarda una `Line2D`, y para qué le sirve eso a un test? | 10 |
| 2 | ¿Qué diferencia hay entre dibujar con `pyplot` y con `Figure`? Da dos razones por las que tu `charts.py` usa `Figure`. | 10 |
| 3 | Una tabla de evolución tiene `[12.5, NaN, 48.9]` para el Norte. ¿Qué dibuja `plot`? ¿Por qué no quitas el `NaN`, y por qué hace falta `marker="o"`? | 10 |
| 4 | Tus etiquetas son `Norte` y `_interna`. ¿Qué escribe `axes.legend()`, y qué escribe `axes.legend(lines, names)`? ¿Por qué? | 10 |
| 5 | Para cada pregunta, ¿qué gráfico usarías?: cómo cambia la media con el tiempo, qué estación tiene más medidas, cómo se reparten los valores de cinco estaciones, si el valor depende de la hora. | 10 |
| 6 | Las medias son 24 (Sur) y 15 (Oeste). En un gráfico de barras con el eje y desde 14, ¿cuántas veces más larga se ve la barra del Sur? ¿Qué regla rompe, y por qué una línea no la necesita? | 10 |
| 7 | ¿Qué es una tabla larga, y por qué la piden seaborn y plotly express? ¿Qué diferencia hay entre `sns.lineplot(..., ax=axes)` y `sns.relplot(...)`? | 10 |
| 8 | ¿Quién dibuja un gráfico de plotly, y dónde? ¿Qué cambia `include_plotlyjs="cdn"`, y qué hace falta para guardar un PNG? | 10 |
| 9 | ¿Por qué un SVG de matplotlib sale distinto cada vez que lo guardas, y qué hace `save` para evitarlo? ¿Por qué usa `rc_context` y no cambia `rcParams`? | 10 |
| 10 | ¿Por qué la imagen `runtime` necesita `MPLCONFIGDIR`? ¿Cuánto crece la imagen con matplotlib, y por qué el proyecto no añade también seaborn y plotly? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. La `Figure` es el lienzo, el archivo entero. Los `Axes` son un gráfico dentro de ella: la zona de dibujo, los ejes x e y, el título y la leyenda; una figura puede tener varios. Un artista es todo lo que se ve: líneas, barras, textos, marcas. Una `Line2D` guarda sus datos (`get_xdata()`, `get_ydata()`), su color, su marcador y su nombre. Un test puede comprobar qué se dibujó sin mirar píxeles, que cambian con la versión de matplotlib o de FreeType.
2. `pyplot` guarda una lista global de figuras y dibuja en "la actual"; cada figura vive hasta `plt.close`, y puede intentar abrir una ventana. Con `Figure`, la figura es una variable: dibujas en los ejes que dices, Python la borra cuando ya no la usas y no abre nada. Razones: no hay estado global que dos llamadas puedan pisar; no se acumulan figuras en memoria (un servidor que dibuja por petición); funciona igual en tests, Docker y CI sin pantalla; `pyplot` no es seguro con hilos.
3. Dibuja un punto en 12,5, nada en el segundo periodo y otro punto en 48,9, sin línea entre ellos: el `NaN` corta la línea. Si quitas el `NaN`, la línea une el primer y el tercer periodo como si hubiera dato en medio: el gráfico inventa un valor. Sin marcador, cada valor es un tramo de línea de longitud cero (no tiene vecino con el que unirse) y no se ve nada; `marker="o"` dibuja un punto en cada valor.
4. `axes.legend()` escribe solo `Norte`: matplotlib salta los artistas cuyo nombre empieza por `_`, porque usa ese prefijo para lo que no quiere en la leyenda (sus líneas sin nombre se llaman `_child0`...). Con `axes.legend(lines, names)`, los nombres van explícitos y escribe los dos.
5. Línea, con el tiempo en el eje x. Barras que empiezan en cero. Histogramas por estación (con `stat="density"` si los grupos tienen distinto tamaño) o cajas o violines, uno por estación. Puntos, con la hora en el eje x y el valor en el y (o un mapa de calor de día × hora).
6. Desde 14, la del Sur mide 10 y la del Oeste 1: diez veces (10,4 con las medias exactas del ejercicio 02), cuando la relación real es 1,6. Rompe la regla de que las barras empiezan en cero, porque una barra se lee por su longitud. Una línea o un punto se leen por su posición sobre la escala, no por su longitud: el eje puede empezar donde están los datos.
7. Una fila por observación y una columna por variable: `time`, `station`, `value`, en lugar de una columna por estación. seaborn y plotly express describen el gráfico con nombres de columna (`hue="station"`, `color="station"`), y necesitan que "estación" sea una columna. `lineplot` es una función de ejes: dibuja en los `Axes` que le das y los devuelve. `relplot` es de figura: crea su propia figura con `pyplot` (que hay que cerrar), no acepta `ax=`, devuelve un `FacetGrid` y puede hacer un panel por valor con `col=`.
8. plotly.js, una biblioteca de JavaScript, en el navegador. Python solo construye la figura, un diccionario de `data` y `layout` que viaja como JSON dentro de un HTML. Con `"cdn"`, el HTML no lleva los 4,8 MB de plotly.js dentro, sino un enlace a `cdn.plot.ly`: pesa unos kB, pero necesita internet al abrirse. Para un PNG hace falta Kaleido, que dibuja con un navegador Chrome.
9. matplotlib guarda en el SVG la fecha (`<dc:date>`) y genera los identificadores internos con una parte al azar. `save` pasa `metadata={"Date": None}` y fija `svg.hashsalt`. Lo hace dentro de `rc_context`, que cambia la configuración solo mientras guarda: `rcParams` es global, y cambiarlo cambiaría todos los gráficos del programa. Lo vigila `test_save_does_not_change_the_global_settings`.
10. El usuario `app` no tiene carpeta personal, y matplotlib necesita una carpeta donde escribir su caché de fuentes: sin ella, crea una temporal en cada ejecución y avisa en cada comando. La imagen pasa de 850 MB a 986 MB: matplotlib (37 MB), fontTools (29 MB), Pillow (22 MB), kiwisolver y otros. seaborn no aporta nada que `graficar` necesite (la tabla ya está calculada) y sigue a matplotlib con retraso; plotly son 39 MB más, y para escribir PNG necesitaría Kaleido y Chrome dentro de la imagen.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-27` muestra un commit por paso (tests, dependencia, módulo, `evolution_of`, comando, versión, Docker, tests propios), sin cambiar los tests del bootcamp, y cada commit pasó por los ganchos | 8 |
| Rojo a verde | Leyó `test_charts.py` antes de escribir; puede decir qué tests pasaron a verde con cada paso, y por qué los tests de `evolucion` siguieron en verde tras `evolution_of` | 8 |
| Ejecución en vivo | Ante el instructor: `graficar` con sus datos en PNG y en SVG, el SVG abierto en el navegador, dos `sha256sum` iguales, una extensión que falla con código 2, el comprobante de `sys.modules` y `pytest` en verde | 8 |
| Rompe y explica | Quita `marker="o"` y explica qué test falla y qué se deja de ver; quita `MPLCONFIGDIR` del `Dockerfile` y enseña el aviso | 8 |
| Explica sus decisiones | Explica por qué `Figure` y no `pyplot`, por qué los tests miran artistas y no píxeles, por qué `rc_context`, y por qué solo matplotlib en el proyecto, con los números de su imagen | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 26

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| La figura | `evolution_figure` con `Figure` y sin `pyplot`, una línea por columna con sus `NaN` y `marker="o"`, la leyenda con las líneas y los nombres, título y ejes; sin reexportar `charts` en `core/__init__.py` | 20 |
| El archivo | `save` con el formato por la extensión, `metadata={"Date": None}`, `svg.hashsalt` y `svg.fonttype` dentro de `rc_context`, sin atrapar errores | 15 |
| El comando | `evolution_of` compartida con `evolucion`; `graficar RUTA SALIDA` con las opciones de `evolucion`, el import dentro, `OSError` y `ValueError` con código 2, código 1 con líneas malas y la línea final | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_charts.py` con datos de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` en verde; CI en verde; `matplotlib` fijado; imágenes `week-27`; `MPLCONFIGDIR`; versión `0.27.0` | 10 |
| Git y README | Rama `week-27` en `python-<nombre>-<apellido>`; README con la sección "Gráficos" y una imagen | 5 |
| Pull request | Salidas, CI, un gráfico con sus datos, tabla de tiempos y respuesta sobre el gráfico grande, tamaño de la imagen y tabla de mutantes con las dos respuestas | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 28](../week-28-estadistica_aplicada_con_scipy_y_statsmodels/README.md) |
