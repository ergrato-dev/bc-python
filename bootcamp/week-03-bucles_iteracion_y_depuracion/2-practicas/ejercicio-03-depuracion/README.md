# Ejercicio 03 — Depuración: traceback, `print`, `pdb` y VS Code

⏱️ 2 h · Teoría previa: [05](../../1-teoria/05-depuracion.md)

## Objetivo

Encontrar cuatro errores con cuatro herramientas distintas: leer un traceback, imprimir el estado con `f"{x=}"`, detener el programa con `breakpoint()` y moverte por él en `pdb`, y usar el depurador gráfico de VS Code. Cada paso de `debug_lab.py` trae un error **a propósito**. Ejercicio **guiado**: no se entrega.

## Antes de empezar

```bash
cd bootcamp/week-03-bucles_iteracion_y_depuracion/2-practicas/ejercicio-03-depuracion/starter
uv run python debug_lab.py
```

```
Ejercicio 03 · Depuración
```

## Pasos

### 1. Leer el traceback

Descomenta el **PASO 1** y ejecuta:

```
Promedio de [4.0, 6.0]: 5.0
Traceback (most recent call last):
  File ".../debug_lab.py", line 19, in <module>
    print("Promedio de []:", average([]))
                             ~~~~~~~^^^^
  File ".../debug_lab.py", line 15, in average
    return sum(values) / len(values)
           ~~~~~~~~~~~~^~~~~~~~~~~~~
ZeroDivisionError: division by zero
```

Léelo **de abajo arriba**:

| Línea | Qué te dice |
|---|---|
| `ZeroDivisionError: division by zero` | Qué pasó: una división entre cero |
| `line 15, in average` y los `^` | Dónde: en la división de `average` |
| `line 19, in <module>` | Quién la llamó: la línea 19, con una lista vacía |

El error no está en la división, sino en llamar a `average` con `[]`. Vuelve a **comentar** la línea 19 (la del `print` con `[]`) para que el programa siga a los pasos siguientes.

### 2. `print` con `=`

Descomenta el **PASO 2**:

```
    value=60.0 count=1
    value=20.0 count=0
    value=70.0 count=1
    value=80.0 count=1
Altos en [60, 20, 70, 80]: 1
```

Deberían ser 3. El `print` muestra que `count` nunca pasa de 1: vuelve a `0` en cada vuelta, porque `count = 0` está **dentro** del `for`. Arréglalo: mueve `count = 0` una línea arriba, antes del `for`, con la sangría de la función. Ejecuta:

```
    value=60.0 count=1
    value=20.0 count=1
    value=70.0 count=2
    value=80.0 count=3
Altos en [60, 20, 70, 80]: 3
```

Ahora borra el `print` de depuración: ya cumplió su función.

### 3. `breakpoint()` y `pdb`

Descomenta el **PASO 3** y ejecuta. El programa se detiene y aparece el *prompt* de `pdb`:

```
> .../debug_lab.py(46)longest_run()
-> breakpoint()
(Pdb)
```

La flecha `->` marca la línea que está **a punto** de ejecutarse. Escribe cada comando y pulsa Enter:

| Escribes | Ves | Qué hace |
|---|---|---|
| `l` | El código alrededor, con `->` en la línea 46 | *list*: dónde estás |
| `p item, current, best` | `('alto', 0, 0)` | *print*: el valor de esas variables |
| `c` | Se detiene otra vez en la 46 | *continue*: sigue hasta el próximo `breakpoint()` |
| `p item, current, best` | `('medio', 1, 0)` | La racha de 1 se guardará en `best` |
| `c`, `c` y `c` | Tres paradas más | Avanza hasta la última vuelta |
| `p item, current, best` | `('alto', 2, 1)` | Última vuelta: la racha va por 2 |
| `n` cuatro veces | `if item == level:`, `current += 1`, `for item in levels:`, `return best` | *next*: una línea cada vez |
| `p best, current` | `(1, 3)` | ¡La racha de 3 está en `current` y nunca pasó a `best`! |
| `c` | `Racha de alto: 1` | El programa termina |

El error: `best` solo se actualiza cuando la racha **se corta**, y la última racha no se corta nunca. Arréglalo cambiando `return best` por `return max(best, current)`. Después **borra la línea `breakpoint()`** y ejecuta:

```
Racha de alto: 3
```

Dos comandos más que te servirán: `q` sale de `pdb` y termina el programa, y `h` muestra la ayuda. Para ignorar todos los `breakpoint()` sin borrarlos: `PYTHONBREAKPOINT=0 uv run python debug_lab.py`.

### 4. El depurador de VS Code

Descomenta el **PASO 4** y ejecuta en la terminal:

```
Total: 4161.0
```

Debería ser `63.75` (12.5 + 8 + 40.25 + 3). Esta vez lo investigas en VS Code:

1. Abre la carpeta `starter` en VS Code (`code .`) y abre `debug_lab.py`. Si VS Code te pide instalar la extensión **Python** de Microsoft, instálala: incluye el depurador.
2. Elige el intérprete del ejercicio: `Ctrl+Shift+P` → **Python: Select Interpreter** → el que está en `.venv`. Si no aparece, ejecuta antes `uv sync` en la terminal.
3. Haz clic a la izquierda del número de la línea `total += value`: aparece un punto rojo, un **punto de parada**.
4. Pulsa `F5` y elige **Python Debugger: Python File**. El programa se detiene en el punto rojo.
5. En el panel **Variables** (a la izquierda) mira `text` y `value`: `'12,5'` y `125.0`. Ahí está el error: `replace(",", "")` borró la coma en lugar de cambiarla por un punto.
6. Pulsa `F5` (continuar) para ir a la siguiente vuelta y mira `value` en cada una.
7. Para la ejecución con `Shift+F5`.

Prueba también un punto de parada **condicional**: clic derecho sobre el punto rojo → **Edit Breakpoint** → escribe `index == 2` y Enter. Con `F5` el programa solo se detiene en la vuelta de `Centro`.

Arregla `parse_reading` con `text.replace(",", ".")` y ejecuta:

```
Total: 63.75
```

| Tecla en VS Code | Comando de `pdb` equivalente | Qué hace |
|---|---|---|
| `F5` | `c` | Continuar hasta el próximo punto de parada |
| `F10` | `n` | Siguiente línea, sin entrar en las funciones |
| `F11` | `s` | Entrar en la función de esta línea |
| `Shift+F11` | `r` | Terminar la función actual y volver a quien la llamó |
| `Shift+F5` | `q` | Parar |

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| El programa termina en el traceback del paso 1 y no ves los demás | Vuelve a comentar la línea 19 |
| La terminal muestra `(Pdb)` y no responde como esperas | Estás dentro de `pdb`: `c` para seguir, `q` para salir |
| Sale `(Pdb)` cuando ya no lo quieres | Quedó un `breakpoint()`: bórralo o usa `PYTHONBREAKPOINT=0` |
| `*** NameError: name 'best' is not defined` en `pdb` | Pediste una variable antes de crearla o fuera de la función |
| VS Code no se detiene en el punto rojo | Ejecutaste con el botón de *Run* en vez de `F5`, o el punto está en una línea comentada |
| `ModuleNotFoundError` o un Python distinto en VS Code | Elige el intérprete de `.venv` (paso 4.2) |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · `while`, `break` y `continue`](../ejercicio-02-while-break-y-continue/README.md) | **Ejercicio 03 · Depuración** | [Ejercicio 04 · Muchas líneas](../ejercicio-04-muchas-lineas/README.md) |
