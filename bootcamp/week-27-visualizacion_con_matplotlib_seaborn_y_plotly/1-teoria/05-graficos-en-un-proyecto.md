# 05 · Gráficos en un proyecto

⏱️ 55 min

## 🎯 Objetivos

- Repartir el código de gráficos entre `core` y la CLI sin que la CLI cargue matplotlib al arrancar.
- Dibujar sin `pyplot`, para que el código funcione igual en la terminal, en un test, en la API y en Docker.
- Probar un gráfico mirando sus artistas, no sus píxeles.
- Guardar gráficos reproducibles: los mismos datos, el mismo archivo.
- Preparar la imagen Docker para matplotlib, y medir lo que cuesta.
- Decidir qué biblioteca de gráficos entra en el proyecto.

---

## 1. Dónde vive cada pieza

| Archivo | Qué sabe hacer | Qué importa |
|---|---|---|
| `core/summaries.py` | La tabla de `evolution`: una fila por periodo, una columna por etiqueta | pandas |
| `core/charts.py` | `evolution_figure` dibuja esa tabla; `save` la guarda | matplotlib (`Figure`), pandas |
| `cli.py` | `evolution_of` lee el archivo y calcula la tabla; `evolucion` la escribe, `graficar` la dibuja | matplotlib **solo** dentro de `graficar` |

`charts.py` sigue la regla de `frames`, `summaries` y `columnar`: no se reexporta en `core/__init__.py`. Importar `matplotlib.figure` cuesta unos 0,3 s. `test_importing_the_cli_does_not_load_matplotlib` lo vigila en otro proceso.

`evolucion` y `graficar` necesitan lo mismo: leer el archivo, comprobar `--cada` y `--periodo`, y calcular la tabla. En lugar de copiar esas líneas, salen a `evolution_of`, que devuelve la tabla, la serie y los errores. Es un cambio en código que ya funcionaba: los tests de `evolucion` de la semana 25 dicen si lo rompiste.

`charts.py` no sabe de archivos de medidas ni de periodos: recibe una tabla y un título. Así se prueba con una tabla escrita a mano, y la API podría usarlo mañana con otros datos.

---

## 2. Sin `pyplot`

```python
from matplotlib.figure import Figure

figure = Figure(figsize=(8, 4.5), layout="constrained")
axes = figure.add_subplot()
```

- **Sin estado global**: la figura es una variable más. Nada depende de "la figura actual", y dos llamadas seguidas no se pisan.
- **Sin fugas**: Python borra la figura cuando ya nadie la usa. Con `pyplot`, cada figura vive en su lista hasta `plt.close`; un servidor que dibuja un gráfico por petición acabaría sin memoria.
- **Sin ventanas**: `Figure.savefig` usa el *backend* del formato (Agg para PNG), sin mirar si hay pantalla. Funciona igual en tu terminal, en `pytest`, en GitHub Actions y en Docker.
- **Con hilos**: la documentación de matplotlib desaconseja `pyplot` en programas con varios hilos, como un servidor web; con una `Figure` por petición no hay nada compartido.

`test_charts_does_not_use_pyplot` comprueba en otro proceso que importar `charts` no carga `matplotlib.pyplot`.

---

## 3. Probar un gráfico

Comparar el PNG con una imagen "buena" guardada parece lo natural, pero es frágil: otra versión de matplotlib o de FreeType mueve un píxel el texto, y el test falla sin que nada importante haya cambiado. Existen herramientas para eso (`pytest-mpl`, con una tolerancia), pero hay algo más simple: **mirar los artistas**.

```python
norte, sur = evolution_figure(TABLE, "título").axes[0].get_lines()
np.testing.assert_array_equal(ys(norte), [12.5, NAN, 48.9])
assert norte.get_marker() == "o"
assert legend_of(figure) == ["Norte", "Sur"]
```

Lo que se comprueba es lo que importa: qué datos tiene cada línea, que el `NaN` sigue ahí y corta la línea, que cada punto tiene marcador, qué dice la leyenda, el título y los ejes. Es rápido (no se dibuja nada hasta `savefig`) y no depende de cómo se pinte cada píxel.

- `np.testing.assert_array_equal` considera iguales dos `NaN`; `==` no.
- Con Hypothesis, `test_evolution_figure_draws_the_whole_table` comprueba con cien series al azar que la figura tiene una línea por columna de la tabla, con sus mismos valores, y que la leyenda los nombra en orden. Las etiquetas incluyen `_oculta`, que empieza por `_`.
- Del archivo guardado basta con poco: que empiece como un PNG (`\x89PNG`), un SVG o un PDF, que el SVG tenga los textos, y que dos veces los mismos datos den los mismos bytes.

---

## 4. Los mismos datos, el mismo archivo

Si guardas un gráfico dos veces con los mismos datos y los archivos son distintos, `git` ve un cambio que no existe y un test no puede comparar dos ejecuciones. Con matplotlib 3.11:

| Formato | Sale igual dos veces | Por qué no, si no |
|---|---|---|
| PNG | Sí | — |
| SVG | No | Guarda la fecha (`<dc:date>`) y los identificadores internos llevan una parte al azar |
| PDF | No, si pasa un segundo entre las dos | Guarda la fecha de creación |

`save` arregla el SVG:

```python
with matplotlib.rc_context({"svg.hashsalt": "observatorio", "svg.fonttype": "none"}):
    figure.savefig(path, metadata={"Date": None})
```

- `metadata={"Date": None}` quita la fecha.
- `svg.hashsalt` fija la parte al azar de los identificadores.
- `svg.fonttype: "none"` deja el texto como texto: se busca, se copia, lo lee un lector de pantalla, y los tests pueden comprobar que el título está.
- `rc_context` solo cambia la configuración mientras guarda. `test_save_does_not_change_the_global_settings` lo vigila: `save` no puede cambiar los gráficos del resto del programa.

El PNG que dibuja `graficar` en tu máquina y en el contenedor Docker son iguales byte a byte: matplotlib trae su propia fuente (DejaVu Sans) y su propio FreeType, y no depende de lo que tenga instalado el sistema.

---

## 5. matplotlib en Docker

El usuario `app` de la imagen `runtime` no tiene carpeta personal. matplotlib guarda una caché de las fuentes del sistema en `~/.config/matplotlib`; si no puede, crea una carpeta temporal cada vez, y avisa en cada comando:

```
mkdir -p failed for path /home/app/.config/matplotlib: [Errno 13] Permission denied: '/home/app'
Matplotlib created a temporary cache directory at /tmp/matplotlib-fbi9ydo9 because there was an issue with the default path (/home/app/.config/matplotlib); it is highly recommended to set the MPLCONFIGDIR environment variable to a writable directory...
```

La solución es decirle dónde escribir:

```dockerfile
ENV PATH="/opt/venv/bin:$PATH" \
    MPLCONFIGDIR=/tmp/matplotlib
```

`test_runtime_gives_matplotlib_a_folder_it_can_write` lo comprueba. No hace falta instalar fuentes ni nada del sistema: matplotlib trae lo suyo, y sin pantalla usa Agg.

---

## 6. Lo que cuesta

```
week-26   850 MB
week-27   986 MB
```

136 MB más en la imagen `runtime`, por una dependencia que trae otras seis:

| Paquete | En disco | Para qué |
|---|---|---|
| `matplotlib` | 37 MB | Los gráficos, sus fuentes y sus estilos |
| `fontTools` | 29 MB | Leer y recortar fuentes para PDF y SVG |
| `pillow` (`PIL` y `pillow.libs`) | 22 MB | Leer y escribir imágenes: PNG, JPEG, WebP... |
| `kiwisolver` | 5,6 MB | Resolver las posiciones de `layout="constrained"` |
| `contourpy`, `pyparsing`, `cycler` | 2,7 MB | Curvas de nivel, el texto matemático, los ciclos de colores |

### ¿Y seaborn y plotly?

Tu proyecto solo usa matplotlib. Las otras dos se quedan en los ejercicios, por razones distintas:

| | Lo que daría al proyecto | Lo que costaría |
|---|---|---|
| seaborn | Nada que `graficar` necesite: la tabla ya está calculada, y dibujarla son cuatro líneas | 1 MB, pero una dependencia más que sigue a matplotlib con retraso (teoría 03, sección 7) |
| plotly | Un HTML interactivo | 39 MB; para PNG, Kaleido y un navegador Chrome dentro de la imagen |

Cada dependencia se paga en tamaño, en tiempo de arranque, en avisos de seguridad que vigilar y en versiones que actualizar. Entra cuando hace algo que el proyecto necesita y no puede hacer con lo que ya tiene.

---

## 7. Medir

Con las 100 000 medidas de `generar_medidas.py`, cada minuto, en periodos de un día:

| Comando | Tiempo | Archivo |
|---|---|---|
| `evolucion` | 1,0 s | — |
| `graficar ... grande.png` | 1,6 s | 166 kB |
| `graficar ... grande.svg` | 1,4 s | 62 kB |
| `graficar ... grande.pdf` | 1,4 s | 23 kB |

De esos 1,4 s, casi todo es lo de `evolucion`: leer el texto línea a línea. Importar matplotlib añade unos 0,3 s, y dibujar 5 líneas de 70 puntos, poco más. El PNG es el más grande y el más lento: 800 × 450 píxeles que comprimir, frente a cinco líneas y unos textos en el SVG.

Abre el gráfico: cinco líneas que se cruzan sin parar. Con datos al azar, no hay nada que ver; con los tuyos, quizá sí. Si se cruzan tanto, la teoría 02 tiene la respuesta: un panel por etiqueta.

---

## 8. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| `import matplotlib.pyplot as plt` en `core` | Estado global, figuras que no se liberan, ventanas | `from matplotlib.figure import Figure` |
| Importar `charts` al principio de `cli.py` | Todos los comandos cargan matplotlib | Dentro de `graficar` |
| Comparar PNG píxel a píxel en los tests | Falla por cambios que no importan | Mira los artistas |
| Cambiar `matplotlib.rcParams` en `save` | Cambia todos los gráficos del programa | `rc_context` |
| Un SVG distinto en cada ejecución | `git` ve cambios que no existen | `metadata={"Date": None}` y `svg.hashsalt` |
| Docker sin `MPLCONFIGDIR` | Un aviso en cada comando | `ENV MPLCONFIGDIR=/tmp/matplotlib` |
| Copiar en `graficar` el código de `evolucion` | Dos sitios que arreglar | `evolution_of` |
| Añadir seaborn o plotly "por si acaso" | Tamaño, arranque y avisos sin nada a cambio | Solo lo que el proyecto usa |

---

## ✅ Qué debes saber al terminar

- [ ] Por qué `charts.py` no usa `pyplot`, y cómo lo comprueba un test.
- [ ] Por qué existe `evolution_of`, y qué tests protegen ese cambio.
- [ ] Qué miran los tests de un gráfico, y por qué no comparan píxeles.
- [ ] Qué hace falta para que un SVG salga igual dos veces.
- [ ] Para qué sirve `MPLCONFIGDIR` en Docker.
- [ ] Cuánto crece la imagen, y por qué el proyecto no usa seaborn ni plotly.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · plotly: gráficos interactivos](04-plotly-graficos-interactivos.md) | **05 · Gráficos en un proyecto** | [Ejercicio 01 · matplotlib: figuras y ejes](../2-practicas/ejercicio-01-matplotlib-figuras-y-ejes/README.md) |
