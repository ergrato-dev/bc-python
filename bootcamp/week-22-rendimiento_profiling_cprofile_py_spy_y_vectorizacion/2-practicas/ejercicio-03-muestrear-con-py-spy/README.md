# Ejercicio 03 — Muestrear con py-spy

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-muestrear-con-py-spy.md)

## Objetivo

Medir un programa desde fuera, sin tocar su código, con py-spy:

- grabar un **gráfico de llamas** con `py-spy record` y leerlo en el navegador;
- comparar el modo normal con `--nonblocking`;
- ver por qué una espera no sale en el gráfico, y cómo verla con `--idle`;
- preguntarle a un programa que no termina **qué está haciendo**, con `py-spy dump`.

Ejercicio **guiado**: descomentas cada paso de `main.py` y ejecutas las órdenes de este README. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-22-rendimiento_profiling_cprofile_py_spy_y_vectorizacion/2-practicas/ejercicio-03-muestrear-con-py-spy/starter
uv run python main.py
uv run py-spy --version
```

```
Ejercicio 03 · py-spy
py-spy 0.4.2
```

py-spy es un programa escrito en Rust que se instala como un paquete de Python más (`py-spy==0.4.2` en `pyproject.toml`). No se importa: lee la memoria de otro proceso de Python unas 100 veces por segundo y anota qué función estaba ejecutando. Es un **perfilador por muestreo** (teoría 03).

## Pasos

### 1. Trabajo de CPU

Descomenta el **PASO 1** y ejecuta:

```
work: 897506.0 · 1.89 s
```

Ahora mídelo con py-spy. Todo lo que va después de `--` es la orden que py-spy arranca y observa:

```bash
uv run py-spy record -o perfil.svg -- python main.py
```

```
py-spy> Sampling process 100 times a second. Press Control-C to exit.
Ejercicio 03 · py-spy
work: 897506.0 · 1.82 s
py-spy> Stopped sampling because process exited
py-spy> Wrote flamegraph data to 'perfil.svg'. Samples: 186 Errors: 0
```

186 muestras en unos 2 segundos: una cada 10 ms. Abre `perfil.svg` en el navegador (en WSL, `explorer.exe perfil.svg`; en macOS, `open perfil.svg`; en Linux, `xdg-open perfil.svg`).

### 2. Leer el gráfico de llamas

Cada rectángulo es una función; el de **encima** es quien la llamó: py-spy dibuja el gráfico invertido, con la raíz (`all`, todas las muestras) arriba y las llamadas creciendo hacia abajo. El **ancho** es la parte de las muestras en que esa función estaba en la pila: cuanto más ancho, más tiempo. El eje horizontal **no** es el tiempo: las funciones van en orden alfabético, y el color no significa nada.

Pasa el ratón por encima de los rectángulos:

| Rectángulo | Muestras |
|---|---|
| `parse_values (main.py:17)` | 123 muestras, 72,8 % |
| `checksum (main.py:24)` | 36 muestras, 21,3 % |

py-spy también dice **qué línea**: `main.py:17` es la comprensión que parte cada línea y la convierte a `float`, y `main.py:24` la cuenta de `checksum`. Haz clic en un rectángulo para ampliarlo y usa `Ctrl+F` (o el botón *Search*) para resaltar una función.

Si optimizas, empieza por `parse_values`: aunque dejaras `checksum` en cero, el programa solo ganaría un 21 %.

### 3. Sin parar el programa

```bash
uv run py-spy record --nonblocking -o perfil.svg -- python main.py
```

```
py-spy> Wrote flamegraph data to 'perfil.svg'. Samples: 177 Errors: 0
```

Por defecto, py-spy **pausa** el programa un instante en cada muestra para leer una pila coherente. Con `--nonblocking` lee sin pausar: no frena nada, pero a veces lee una pila a medio cambiar y la cuenta en `Errors`.

En este programa la pausa no se nota (1,9 s en los dos modos). En el `informe` de la semana 21 con 50 000 medidas, que tiene pilas muy profundas, la pausa pasó el tiempo de 8 a 55 segundos en WSL2. Si con py-spy tu programa tarda mucho más que sin él, usa `--nonblocking`.

### 4. Una espera

Descomenta el **PASO 2** y graba otra vez:

```bash
uv run py-spy record -o perfil.svg -- python main.py
```

```
esperando: 2.00 s
py-spy> Wrote flamegraph data to 'perfil.svg'. Samples: 170 Errors: 0
```

El programa ha tardado 2 segundos más y las muestras **no** han subido: py-spy no cuenta por defecto las muestras en que el programa estaba **parado** (en `sleep`, esperando a la red o al disco). Sirve para buscar dónde se calcula; para ver dónde se espera:

```bash
uv run py-spy record --idle -o perfil.svg -- python main.py
```

```
py-spy> Wrote flamegraph data to 'perfil.svg'. Samples: 352 Errors: 0
```

Ahora aparece `<module> (main.py:52)`, el `time.sleep(2)`, con 163 muestras, el 46 %. Es la diferencia entre el tiempo de CPU y el de reloj del ejercicio 01.

### 5. Un programa que no termina

Descomenta el **PASO 3** y ejecuta en una terminal:

```bash
uv run python main.py
```

```
Ejercicio 03 · py-spy
work: 897506.0 · 1.75 s
esperando: 2.00 s
pid 766457: esperando a listo.txt
```

El programa se queda esperando, como uno que se ha colgado. Abre **otra** terminal en la misma carpeta y pregúntale qué hace, con su `pid`:

```bash
uv run py-spy dump --pid 766457
```

```
Permission Denied: Try running again with elevated permissions by going 'sudo env "PATH=$PATH" !!'
```

Antes, py-spy arrancaba el programa (`-- python main.py`) y por eso podía leer su memoria. Ahora el programa es de otro proceso, y Linux solo deja leer la memoria de un proceso ajeno a root. Con `sudo` y la ruta del py-spy de tu entorno:

```bash
sudo .venv/bin/py-spy dump --pid 766457
```

```
Process 766457: .venv/bin/python main.py
Python v3.14.10

Thread 766457 (idle)
    wait_for (main.py:63)
    <module> (main.py:67)
```

`dump` escribe la pila **de cada hilo** en ese momento, de dentro afuera: el programa está en la línea 63 de `wait_for` (el `time.sleep(0.1)` del bucle), llamada desde la línea 67. `(idle)` dice que estaba esperando, no calculando. Es lo primero que haces con un programa colgado en producción: sin pararlo ni reiniciarlo.

Para terminar, crea el archivo que espera, desde la segunda terminal:

```bash
touch listo.txt
```

La primera terminal escribe `listo` y termina. Borra `listo.txt` y `perfil.svg` al acabar.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `Permission Denied` con `record -- python main.py` | En macOS py-spy necesita `sudo` siempre: `sudo .venv/bin/py-spy record -o perfil.svg -- .venv/bin/python main.py` |
| `sudo: .venv/bin/py-spy: command not found` | Ejecuta antes `uv run python main.py` para que uv cree `.venv`, y lanza `sudo` desde la carpeta `starter` |
| `Error: No child process (os error 10)` al terminar | py-spy 0.4.2 lo escribe a veces en modo normal cuando el programa ya terminó; si dice `Wrote flamegraph data`, el gráfico está bien |
| `Errors:` con muchas muestras | Solo con `--nonblocking`: alguna pila se leyó a medias. Si son muchas, sube la duración o quita la opción |
| En Docker, `Permission denied (os error 13)` | El contenedor no deja leer otros procesos ni a root: hace falta `docker run --cap-add SYS_PTRACE` (teoría 03) |
| `perfil.svg` se ve vacío o sin interacción | Ábrelo en el navegador, no en un visor de imágenes: el gráfico usa JavaScript |
| El paso 5 no termina | Falta `listo.txt` en la carpeta desde la que ejecutaste `main.py`; o pulsa `Ctrl+C` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Perfilar con cProfile](../ejercicio-02-perfilar-con-cprofile/README.md) | **Ejercicio 03 · Muestrear con py-spy** | [Ejercicio 04 · Vectorizar con NumPy](../ejercicio-04-vectorizar-con-numpy/README.md) |
