# Ejercicio 04 — Reproducible o no

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-reproducibilidad.md)

## Objetivo

Romper a propósito cada ingrediente de la reproducibilidad, y arreglarlo:

- el azar, sin semilla y con ella;
- la hora de la ejecución;
- una ruta que solo existe en una máquina;
- unos datos que cambian por debajo, y la huella que lo detecta;
- las versiones que usa el kernel.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-29-eda_notebooks_reproducibles_y_etl_desde_postgresql/2-practicas/ejercicio-04-reproducible-o-no/starter
uv run python main.py
```

```
Ejercicio 04 · Reproducible o no
1 + 1 en un kernel nuevo: 2
```

`run` crea un notebook con las celdas que le pasas, lo ejecuta en un **kernel nuevo** (con `nbclient`, como en el ejercicio 02) y devuelve lo que muestra cada celda. `twice` lo ejecuta dos veces, en dos kernels distintos, y compara: es lo que haría otra persona con tu notebook. Cada ejecución arranca un kernel, así que cada paso tarda un par de segundos.

## Pasos

### 1. Números al azar

Descomenta el **PASO 1** y ejecuta:

```
sin semilla: 16.474 | 16.485 → DISTINTO
con semilla: 18.824 | 18.824 → igual
```

Tus dos números sin semilla serán otros, y cambian en cada ejecución: esa es la idea.

- `default_rng()` sin argumento toma su semilla del sistema operativo: cada kernel, otra.
- `default_rng(29)` empieza siempre en el mismo punto de la secuencia: 18.824 en cualquier máquina con la misma versión de numpy.

### 2. La hora de la ejecución

Descomenta el **PASO 2** y ejecuta:

```
ahora: '20:52:00.015836' | '20:52:00.629751' → DISTINTO
fijada: datetime.date(2026, 11, 10) | datetime.date(2026, 11, 10) → igual
```

- `datetime.now()` es otra fuente de azar: aquí cambia en microsegundos; en un análisis de "los últimos 30 días", cambia cada día.
- Una fecha escrita como constante (`TODAY`) da lo mismo siempre. Escribe al lado de dónde sale: la fecha de la instantánea.

### 3. Rutas que solo existen en tu máquina

Descomenta el **PASO 3** y ejecuta:

```
ruta absoluta: FileNotFoundError
ruta relativa: 'Norte,12.5'
```

- `/home/ana/proyecto/notebooks/medidas.csv` solo existe en la máquina de Ana.
- `run` ejecuta el notebook en `salida/` (`resources={"metadata": {"path": ...}}`), igual que JupyterLab ejecuta cada notebook en su carpeta. `medidas.csv`, relativa, funciona en cualquier máquina que tenga la carpeta.

### 4. Los datos cambian por debajo

Descomenta el **PASO 4** y ejecuta:

```
los mismos datos: 'huella correcta'
un valor cambiado: AssertionError: otros datos
```

- La celda calcula la huella SHA-256 de `medidas.csv` y la compara con `EXPECTED`, la que tenía el archivo al escribir el análisis: lo mismo que la primera celda del notebook de tu proyecto.
- Cambias un solo valor, de 8.0 a 8.1, y el notebook se para en esa celda en lugar de calcular sobre otros datos.

### 5. Las versiones

Descomenta el **PASO 5** y ejecuta:

```
Python 3.14 · numpy 2.5.4
¿la de pyproject.toml? True
```

- El kernel corre con el Python y los paquetes del entorno de `uv`: los que fija `uv.lock`. `importlib.metadata.version` lee la versión instalada de verdad, no la que crees tener.
- En Colab, esta celda daría otra versión de Python y otra de numpy, hasta que la primera celda instalara las fijadas (teoría 03, sección 5).

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `[IPKernelApp] WARNING \| Kernel is running over TCP without encryption...` | Normal: el kernel escucha en tu propia máquina. Sale por stderr y no cambia nada |
| `ModuleNotFoundError: No module named 'nbclient'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `con semilla` da `DISTINTO` | Quitaste el `29` de `default_rng(29)` |
| El paso 3 no da `FileNotFoundError` | Tienes de verdad un archivo en esa ruta: cámbiala por otra que no exista |
| El paso 4 dice `huella correcta` dos veces | Cambiaste el archivo antes de calcular `EXPECTED`, o no lo cambiaste |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · ETL desde PostgreSQL](../ejercicio-03-etl-desde-postgresql/README.md) | **Ejercicio 04 · Reproducible o no** | [Proyecto · Extraer y explorar](../../3-proyecto/README.md) |
