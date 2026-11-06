# Ejercicio 03 — Tipos y conversiones

⏱️ 2 h 30 min · Teoría previa: [05](../../1-teoria/05-variables-y-tipos.md)

## Objetivo

Mirar de frente los detalles de los tipos: conversiones que fallan, `float` inexactos, `int` sin límite y la diferencia entre `None` y "vacío". Ejercicio **guiado**: el código está en `types_lab.py`, comentado por pasos; lo descomentas, ejecutas y comparas con la salida esperada. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-01-entorno_docker_uv_y_tipos/2-practicas/ejercicio-03-tipos-y-conversiones/starter
uv run python types_lab.py
```

Salida esperada: `Ejercicio 03 · Tipos y conversiones`. Para cada paso: **primero prueba en el REPL** (`uv run python`) lo que dice el README, después descomenta el bloque del paso en `types_lab.py` (`Ctrl+K Ctrl+U` en VS Code) y ejecuta el archivo.

## Pasos

### 1. Predice antes de ejecutar

Sin ejecutar nada, piensa qué da cada línea (anótalo en un papel). Después compruébalo en el REPL y cuenta tus aciertos:

```python
type(7 / 2)
int(3.99)
bool("False")
bool("")
0.1 * 3 == 0.3
True + True
```

Respuestas: `<class 'float'>`, `3`, `True`, `False`, `False`, `2`. Si fallaste alguna, la teoría 05 explica por qué.

### 2. El nombre de cada tipo

```python
>>> type(3.0)
<class 'float'>
>>> type(3.0).__name__
'float'
```

Descomenta el **PASO 2** y ejecuta. Línea nueva:

```
Tipos: int float str bool NoneType
```

### 3. De texto a `int`

Descomenta el **PASO 3** y ejecuta. Esta vez el programa **se detiene** con un error:

```
Entero: 42
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 10: '4.5'
```

`int(" 42 ")` funcionó (ignora los espacios), pero `int("4.5")` no: un texto con decimales no es un entero. Es el comportamiento correcto: quien llama a la función decide qué hacer con ese dato. Lee el traceback de abajo arriba (teoría 02) y localiza la línea que falló. Después **vuelve a comentar** solo la línea `print("Con decimales:", ...)` y ejecuta otra vez para seguir.

### 4. De texto a `float`, con coma decimal

```python
>>> float("3,5")
ValueError: could not convert string to float: '3,5'
>>> "3,5".replace(",", ".")
'3.5'
```

Descomenta el **PASO 4**. Los métodos se encadenan: `text.strip().replace(",", ".")` primero quita espacios y luego cambia la coma.

```
Decimal: 3.5 2.25
```

### 5. Comparar `float`

Descomenta el **PASO 5**:

```
0.1 + 0.2 == 0.3: False
isclose: True
Con 17 decimales: 0.30000000000000004
```

La tercera línea muestra el porqué: `0.1` y `0.2` no se pueden guardar exactos en binario, y su suma queda un poco por encima de `0.3`. Por eso los `float` se comparan con `math.isclose`, nunca con `==`.

### 6. `int` sin límite

Descomenta el **PASO 6**:

```
Cifras de 2**10: 4
Cifras de 2**1000: 302
```

En Python un `int` no tiene límite de tamaño: `2**1000` tiene 302 cifras y se calcula exacto. Pruébalo en el REPL: `2**1000`.

### 7. `None` no es `0` ni `""`

Descomenta el **PASO 7**:

```
Faltan: True False False False
Con not: True True True True
```

La segunda línea es la trampa: `not value` es `True` para `None`, `0`, `""` y `0.0`, así que **no** sirve para saber si falta el dato. Para eso, `value is None`. En el proyecto de la semana, un `0` medido y un dato faltante tienen que ser cosas distintas.

### 8. Las anotaciones no se verifican al ejecutar

Con el paso 3 descomentado, en el REPL:

```python
>>> from types_lab import to_int
>>> to_int(42)
42
```

(Al importar, se ejecutan también los `print` del archivo: es normal.) `to_int` dice recibir `text: str`, pero le pasaste un `int` y Python no protestó: las anotaciones no se comprueban al ejecutar. Las comprueba una herramienta aparte, **mypy**, que verás en la semana 13 ([teoría 05](../../1-teoria/05-variables-y-tipos.md), sección 5).

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'math' is not defined` en el REPL | Escribe `import math` antes de usarlo; en `types_lab.py` ya está importado |
| `NameError: name 'to_int' is not defined` | Descomentaste el `print` pero no el `def` |
| `IndentationError: unexpected indent` | Al descomentar quedó un espacio de más al principio de la línea |
| El programa se detiene en el paso 3 y no ves los siguientes | Es lo esperado: vuelve a comentar la línea `print("Con decimales:", ...)` |
| En el paso 8, `ModuleNotFoundError: No module named 'types_lab'` | Abre el REPL con `uv run python` desde `starter/` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Python en Docker](../ejercicio-02-python-en-docker/README.md) | **Ejercicio 03 · Tipos y conversiones** | [Proyecto · Observatorio, capa 0](../../3-proyecto/README.md) |
