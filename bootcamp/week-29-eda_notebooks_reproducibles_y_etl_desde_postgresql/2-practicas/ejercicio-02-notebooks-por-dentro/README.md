# Ejercicio 02 — Notebooks por dentro

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-notebooks-y-jupyterlab.md)

## Objetivo

Ver qué es de verdad un notebook, sin JupyterLab de por medio:

- un archivo JSON, que escribes y lees desde Python con `nbformat`;
- un kernel que lo ejecuta, con `nbclient`;
- el estado oculto, cuando el orden de ejecución no es el del archivo;
- una celda borrada que solo falla en un kernel nuevo;
- lo que pesan las salidas, y cómo se quitan.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-29-eda_notebooks_reproducibles_y_etl_desde_postgresql/2-practicas/ejercicio-02-notebooks-por-dentro/starter
uv run python main.py
```

```
Ejercicio 02 · Los notebooks por dentro
4 celdas, nbformat 4.5
```

`main.py` crea un notebook de cuatro celdas: un título en Markdown y tres celdas de código que calculan la media de tres medidas. El mismo de la teoría 02, sección 4. Los archivos van a `salida/`, que no va a Git.

## Pasos

### 1. Un notebook es un archivo JSON

Descomenta el **PASO 1** y ejecuta:

```
norte.ipynb: 912 bytes · claves ['cells', 'metadata', 'nbformat', 'nbformat_minor']
{'cell_type': 'code', 'execution_count': None, 'outputs': [], 'source': ['for value in values:\n', '    total = total + value']}
```

- `nbformat.write` lo guarda; `json.loads` lo lee como cualquier JSON. Ábrelo también con tu editor: `salida/norte.ipynb`.
- La celda guarda su código como **lista de líneas**, sin salidas (`[]`) y sin contador (`None`): todavía no se ha ejecutado.

### 2. Ejecutarlo con un kernel

Descomenta el **PASO 2** y ejecuta:

```
[1] []
[2] []
[3] ['stream', 'execute_result']
stream → 'media 13.17\n'
execute_result → '3'
con salidas: 2227 bytes
```

- `NotebookClient(...).execute()` arranca un kernel de IPython, le envía las celdas de código en orden y guarda lo que devuelve: es lo que hacen JupyterLab y `jupyter execute`.
- Las dos primeras celdas no muestran nada. La tercera tiene dos salidas: un `stream` (lo que imprime `print`) y un `execute_result` (el valor de su última línea, `len(values)`).
- El archivo pasa de 912 a 2 227 bytes: salidas, contadores, los datos del kernel en `metadata` y la hora de cada celda. Ábrelo y búscalos.

### 3. Estado oculto

Descomenta el **PASO 3** y ejecuta:

```
en desorden: media 26.33 · contadores [1, 3, 4]
de arriba abajo: media 13.17 · contadores [1, 2, 3]
```

- `setup_kernel()` abre un kernel y `execute_cell` le envía una celda: lo que haces tú en JupyterLab con `Shift + Enter`. La segunda celda va **dos veces**, y `total` suma dos veces.
- Los contadores lo delatan: `[1, 3, 4]`. Es la única pista, y casi nadie la mira.
- En un kernel nuevo y de arriba abajo, 13.17. Es lo que verá cualquier otra persona.

### 4. Una celda borrada

Descomenta el **PASO 4** y ejecuta:

```
kernel nuevo: NameError: name 'values' is not defined
```

- En tu sesión, borrar la celda que define `values` no rompe nada: la variable sigue en la memoria del kernel. En un kernel nuevo, la siguiente celda que la usa falla.
- `CellExecutionError` lleva el nombre (`ename`) y el mensaje (`evalue`) del error de la celda.

### 5. Quitar las salidas antes de Git

Descomenta el **PASO 5** y ejecuta:

```
grande.ipynb con salidas: 48855 bytes
grande.ipynb sin salidas: 2432 bytes
```

- Una celda que imprime 2 000 líneas multiplica el archivo por veinte. Un gráfico o una tabla grande hacen lo mismo.
- El bucle deja cada celda de código sin salidas y sin contador: lo que hace el gancho de tu proyecto con `nbconvert --clear-output` (teoría 05, sección 4). `nbformat.validate` comprueba que el resultado sigue siendo un notebook válido.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `[IPKernelApp] WARNING \| Kernel is running over TCP without encryption...` | Normal: el kernel y `nbclient` hablan por un puerto de tu propia máquina. Sale por stderr y no cambia nada |
| `ModuleNotFoundError: No module named 'nbclient'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `NoSuchKernel: No such kernel named python3` | Falta `ipykernel` en el entorno: no cambies las dependencias de `pyproject.toml` |
| `TimeoutError` o `DeadKernelError` | El kernel tardó más de 60 s en contestar: vuelve a ejecutar; si se repite, cierra otros notebooks abiertos |
| Los tamaños en bytes no coinciden exactamente | La hora de cada celda y la versión de Python van en el archivo; deben ser parecidos |
| El paso 3 da 13.17 en los dos casos | Ejecutas todas las celdas con `execute()` en lugar de `execute_cell` en el orden `[1, 2, 2, 3]` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · EDA con pandas](../ejercicio-01-eda-con-pandas/README.md) | **Ejercicio 02 · Notebooks por dentro** | [Ejercicio 03 · ETL desde PostgreSQL](../ejercicio-03-etl-desde-postgresql/README.md) |
