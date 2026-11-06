# Ejercicio 01 — Módulos e imports

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-modulos-e-imports.md)

## Objetivo

Ver qué hace de verdad un `import`: cuándo se ejecuta el archivo importado, qué nombres llegan a tu archivo, para qué sirve `__name__` y dónde busca Python los módulos. Es lo que pasa cada vez que tu Observatorio escribe `from observatorio.core.record import parse_value`. Ejercicio **guiado**: descomentas cada paso de `imports_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-08-proyectos_con_uv_modulos_paquetes_pyproject_ruff_y_lock/2-practicas/ejercicio-01-modulos-e-imports/starter
uv run python imports_lab.py
```

```
Ejercicio 01 · Módulos e imports
```

Abre también `units.py`: es el módulo que vas a importar. Fíjate en el `print` que hay fuera de las funciones.

## Pasos

### 1. `import` y el caché de módulos

Descomenta el **PASO 1** y ejecuta:

```
Ejercicio 01 · Módulos e imports
  [cargando units.py, __name__ = 'units']
10 millas: 16.09344 km
Constante: 1.609344
¿En el caché? True
```

`import units` busca `units.py`, lo **ejecuta** de arriba abajo (por eso sale el `print` de carga) y deja en tu archivo un nombre, `units`, con todo lo que el módulo definió. Llegas a sus funciones y constantes con un punto: `units.miles_to_km`.

El segundo `import units` no escribe nada. Python guarda cada módulo cargado en el diccionario `sys.modules`, y un `import` de algo que ya está ahí solo reutiliza el módulo: el archivo se ejecuta **una vez** por programa, aunque lo importen diez archivos.

### 2. `from ... import` y los alias

Descomenta el **PASO 2**:

```
Maratón: 42.2 km
25 °C: 77.0 °F
¿Mismo objeto? True
Nombres de units: ['KM_PER_MILE', 'celsius_to_fahrenheit', 'miles_to_km']
```

`from units import miles_to_km` trae el nombre suelto: escribes `miles_to_km(...)` sin `units.` delante. `as` le pone otro nombre en tu archivo, sin cambiar el del módulo. `¿Mismo objeto? True`: los dos caminos llegan a la **misma** función, no a una copia, y `units.py` no se cargó otra vez. La última línea lista los nombres públicos del módulo con `dir`.

Escribe debajo `print(KM_PER_MILE)` y ejecuta:

```
NameError: name 'KM_PER_MILE' is not defined
```

`from` solo trae los nombres que pides. `KM_PER_MILE` sigue disponible como `units.KM_PER_MILE`. Borra esa línea.

### 3. `__name__`

Descomenta el **PASO 3**:

```
Aquí __name__ vale: '__main__'
Y en units: 'units'
```

Cada módulo tiene una variable `__name__`. En el archivo que ejecutas vale `"__main__"`; en uno importado, su nombre. Ahora ejecuta el módulo directamente:

```bash
uv run python units.py
```

```
  [cargando units.py, __name__ = '__main__']
units.py ejecutado directamente: prueba rápida
  1 milla = 1.609 km
```

Esta vez `units.py` es el archivo principal, su `__name__` es `"__main__"` y el bloque `if __name__ == "__main__":` se ejecuta. Cuando lo importa `imports_lab.py`, ese bloque se salta. Así un módulo puede traer una prueba rápida sin que se ejecute al importarlo.

### 4. Dónde busca Python

Descomenta el **PASO 4**:

```
Primera carpeta: starter
Carpeta de trabajo: starter
units viene de: units.py
La biblioteca estándar: python3.14
```

`sys.path` es la lista de carpetas donde `import` busca, en orden. La primera es la carpeta **del script**, por eso encuentra `units.py`. Detrás vienen la biblioteca estándar y los paquetes instalados en el entorno.

Sube una carpeta y ejecuta desde allí:

```bash
cd ..
uv run python starter/imports_lab.py
cd starter
```

```
Primera carpeta: starter
Carpeta de trabajo: ejercicio-01-modulos-e-imports
units viene de: units.py
```

La carpeta de trabajo cambió, y `import units` sigue funcionando: los imports se buscan desde la carpeta del script, no desde la de trabajo. Las rutas de `open()` de la semana 7 sí dependen de la carpeta de trabajo. Son dos reglas distintas, y las dos aparecen en el mismo programa.

### 5. Un archivo que tapa la biblioteca estándar

Descomenta el **PASO 5**:

```
Mediana: 12.5
```

`statistics` es un módulo de la biblioteca estándar. Ahora crea un archivo vacío con el mismo nombre, junto a `imports_lab.py`, y ejecuta:

```bash
touch statistics.py
uv run python imports_lab.py
```

```
AttributeError: module 'statistics' has no attribute 'median' (consider renaming '.../starter/statistics.py' since it has the same name as the standard library module named 'statistics' and prevents importing that standard library module)
```

La carpeta del script va primero en `sys.path`, así que `import statistics` encontró **tu** archivo vacío antes que el de la biblioteca estándar. Python 3.14 lo detecta y propone renombrarlo. Pasa igual con un `csv.py`, `json.py` o `random.py` en tu proyecto: nunca llames a tus módulos como uno de la biblioteca estándar. Borra el archivo:

```bash
rm statistics.py
```

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'units'` | Ejecutas un `imports_lab.py` que no está junto a `units.py`, o escribiste mal el nombre |
| `NameError: name 'units' is not defined` en el paso 2 | Descomentaste el paso 2 sin el 1: el `import units` del paso 1 hace falta |
| `[cargando units.py ...]` sale dos veces | Ejecutaste `units.py` y además lo importaste: es lo que muestra el paso 3 |
| `AttributeError: module 'statistics' has no attribute 'median'` sin hacer el paso 5 | Hay un `statistics.py` en la carpeta: bórralo |
| No sale la línea `La biblioteca estándar` (Windows) | En Windows la carpeta se llama `Lib`, no `lib/python3.14`: no pasa nada |
| `IndentationError` al descomentar | Las líneas vacías dentro de un bloque comentado llevan `#`: quita también ese `#` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · ruff](../../1-teoria/05-ruff.md) | **Ejercicio 01 · Módulos e imports** | [Ejercicio 02 · Paquetes](../ejercicio-02-paquetes/README.md) |
