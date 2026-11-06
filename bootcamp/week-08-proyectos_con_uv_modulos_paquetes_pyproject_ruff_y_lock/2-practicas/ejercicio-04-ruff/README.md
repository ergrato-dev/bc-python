# Ejercicio 04 — ruff

⏱️ 1 h · Teoría previa: [05](../../1-teoria/05-ruff.md)

## Objetivo

Pasar ruff por un archivo que funciona pero tiene un bug escondido, leer sus avisos, arreglar unos solos y otros a mano, formatear el código y activar más reglas en `pyproject.toml`. Es lo que harás con el Observatorio en los pasos 8 y 9 del proyecto. Ejercicio **guiado**: ejecutas los comandos, descomentas el paso 5 de `pyproject.toml` y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-08-proyectos_con_uv_modulos_paquetes_pyproject_ruff_y_lock/2-practicas/ejercicio-04-ruff/starter
uv run python messy.py
```

```
Ejercicio 04 · ruff
primera lectura: [8.0]
segunda lectura: [8.0, 12.5]
sin dato | valor: 30.7
media: 17.1
```

ruff ya está en el grupo `dev` de `pyproject.toml`, fijado a `0.17.3`: el primer `uv run` lo instaló. Abre `messy.py` y fíjate en la segunda línea de la salida: `add_reading(12.5)` debería devolver `[12.5]`, y devuelve también la lectura de la llamada anterior.

## Pasos

### 1. El primer `ruff check`

```bash
uv run ruff check
```

Por cada problema, ruff enseña el código de la regla, el mensaje, la línea marcada y, si sabe arreglarlo, el arreglo. Para ver la lista entera de un vistazo, una línea por aviso:

```bash
uv run ruff check --output-format concise
```

```
messy.py:7:1: I001 [*] Import block is un-sorted or un-formatted
messy.py:7:8: F401 [*] `os` imported but unused
messy.py:8:8: F401 [*] `sys` imported but unused
messy.py:8:13: F401 [*] `json` imported but unused
messy.py:9:1: UP035 `typing.List` is deprecated, use `list` instead
messy.py:12:55: B006 Do not use mutable data structures for argument defaults
messy.py:17:21: UP045 [*] Use `X | None` for type annotations
messy.py:20:5: F841 Local variable `doubled` is assigned to but never used
messy.py:21:12: UP031 Use format specifiers instead of percent format
messy.py:24:18: UP006 [*] Use `list` instead of `List` for type annotation
messy.py:31:7: F541 [*] f-string without any placeholders
Found 11 errors.
[*] 7 fixable with `--fix` (3 unsafe fixes available with `--fix --unsafe-fixes`).
```

Cada línea es `archivo:línea:columna: CÓDIGO mensaje`. La letra del código dice de qué familia es la regla: `F` (Pyflakes) son errores seguros, como imports o variables sin usar; `I`, el orden de los imports; `UP` (pyupgrade), sintaxis antigua que tiene una forma moderna; `B` (bugbear), trampas que suelen ser bugs.

### 2. Lee una regla

`B006` no lleva `[*]`, y es el bug de la segunda lectura. Pregúntale a ruff:

```bash
uv run ruff rule B006
```

```
# mutable-argument-default (B006)

Derived from the **flake8-bugbear** linter.

Fix is sometimes available.

## What it does
Checks for uses of mutable objects as function argument defaults.

## Why is this bad?
Function defaults are evaluated once, when the function is defined.
...
```

El `[]` de `readings: list[float] = []` se crea **una vez**, al definir la función, y todas las llamadas que no pasan `readings` comparten esa misma lista. Cada llamada añade a la lista de la anterior. Los tests de una sola llamada no lo ven nunca.

### 3. Arreglos automáticos y a mano

```bash
uv run ruff check --fix --output-format concise
```

```
messy.py:9:55: B006 Do not use mutable data structures for argument defaults
messy.py:17:5: F841 Local variable `doubled` is assigned to but never used
messy.py:18:12: UP031 Use format specifiers instead of percent format
Found 11 errors (8 fixed, 3 remaining).
3 unsafe fixes available with `--fix --unsafe-fixes`.
```

`--fix` aplicó los arreglos **seguros**, los que no cambian lo que hace el programa: ordenó y separó los imports, quitó los que sobraban, cambió `List` por `list` y `Optional[float]` por `float | None`. Mira el resultado con `git diff messy.py`. Los tres que quedan tienen arreglo, pero **inseguro**: podría cambiar el comportamiento, y ruff quiere que decidas tú. Arréglalos a mano:

1. `B006`: el valor por defecto pasa a ser `None`, y la lista se crea dentro, en cada llamada:

   ```python
   def add_reading(value: float, readings: list[float] | None = None) -> list[float]:
       if readings is None:
           readings = []
       readings.append(value)
       return readings
   ```

2. `F841`: borra la línea de `doubled`, que nadie usa.
3. `UP031`: `"valor: %s" % value` pasa a ser `f"valor: {value}"`.

```bash
uv run ruff check
uv run python messy.py
```

```
All checks passed!
Ejercicio 04 · ruff
primera lectura: [8.0]
segunda lectura: [12.5]
sin dato | valor: 30.7
media: 17.1
```

La segunda lectura ya sale bien: ruff encontró un bug que los ojos y la ejecución normal pasaban por alto.

### 4. Formatear

```bash
uv run ruff format --diff
```

```
--- messy.py
+++ messy.py
@@ -15,7 +15,7 @@
 
 def describe(value: float | None) -> str:
     if value == None:
-        return 'sin dato'
+        return "sin dato"
     return f"valor: {value}"
 
 
@@ -23,7 +23,7 @@
     total = 0
     for i in range(len(values)):
         total += values[i]
-    return total/len(values)
+    return total / len(values)
 
 
 print("Ejercicio 04 · ruff")

1 file would be reformatted
```

El *linter* (`ruff check`) busca errores; el *formatter* (`ruff format`) solo cambia la forma: comillas dobles, espacios alrededor de los operadores, saltos de línea. `--diff` enseña los cambios sin hacerlos. Aplícalos:

```bash
uv run ruff format
uv run python messy.py
```

```
1 file reformatted
```

La salida del programa es la misma: el formato nunca cambia lo que hace el código.

### 5. Más reglas, en `pyproject.toml`

Fíjate en que nadie se quejó de `if value == None:`. Las reglas de ruff que vienen activas por defecto evitan las de puro estilo. Descomenta el **PASO 5** de `pyproject.toml` y vuelve a revisar:

```bash
uv run ruff check --output-format concise
```

```
messy.py:17:17: E711 Comparison to `None` should be `cond is None`
Found 1 error.
1 unsafe fix available with `--fix --unsafe-fixes`.
```

`extend-select` añade reglas a las que ya había; `select` las sustituye todas. La familia `E` (pycodestyle) es el estilo de PEP 8. Con `None`, se compara con `is`: hay un único `None`, y `==` puede dar resultados raros con objetos que redefinen la igualdad. Cambia `==` por `is` y comprueba que queda `All checks passed!`.

La configuración vive en el proyecto, no en tu editor: cualquiera que clone el repositorio revisa con las mismas reglas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `error: Failed to spawn: ruff` | Ejecutas desde otra carpeta y uv no encuentra el `pyproject.toml` de `starter/`: `cd` a `starter/` |
| Tus números de línea no coinciden con los del paso 3 | Ya arreglaste algo a mano antes de `--fix`: no pasa nada, lo importante son los códigos |
| `--fix` no arregla `B006` | Es inseguro a propósito: arréglalo a mano, como en el paso 3 |
| `segunda lectura: [8.0, 12.5]` después del paso 3 | Dejaste `= []` como valor por defecto: tiene que ser `= None` |
| No sale `E711` en el paso 5 | Quedó un `#` delante de `[tool.ruff.lint]`: sin esa línea, `extend-select` cae dentro de la tabla de arriba, `[dependency-groups]`, y ruff no lo ve |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · `pyproject.toml` y dependencias](../ejercicio-03-pyproject-y-dependencias/README.md) | **Ejercicio 04 · ruff** | [Proyecto · Observatorio, capa 7](../../3-proyecto/README.md) |
