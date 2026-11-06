# Ejercicio 04 — Entrada, salida y `match`

⏱️ 2 h · Teoría previa: [02](../../1-teoria/02-condicionales-y-match.md) y [05](../../1-teoria/05-entrada-y-salida.md)

## Objetivo

Construir paso a paso un programa de terminal completo: recibe una orden por argumento o por teclado, la interpreta con `match`, responde en stdout o stderr según toque y termina con el código de salida correcto. Es el mismo esqueleto que usa el proyecto de esta semana. Ejercicio **guiado**: descomentas cada paso de `cli.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-02-operadores_strings_io_y_match/2-practicas/ejercicio-04-entrada-salida-y-match/starter
uv run python cli.py
echo $?
```

No imprime nada y `echo $?` muestra `0`: todo el código está comentado y el programa terminó bien. `$?` guarda el código de salida del último comando; lo usarás en todo el ejercicio.

## Pasos

### 1. Los argumentos llegan en `sys.argv`

Descomenta el **PASO 1** y ejecuta con argumentos:

```bash
uv run python cli.py uno "dos tres"
```

```
argv: ['cli.py', 'uno', 'dos tres']
```

Las comillas agrupan: `"dos tres"` es un solo argumento. Prueba sin argumentos: la lista solo tiene `'cli.py'`.

### 2. Dos salidas distintas

Descomenta el **PASO 2** y ejecuta redirigiendo stdout a un archivo:

```bash
uv run python cli.py > salida.txt
cat salida.txt
```

En la pantalla solo aparece `esto va a stderr`; `salida.txt` tiene `argv: ['cli.py']` y `esto va a stdout`. `>` captura stdout y deja pasar stderr. Así un programa puede guardar resultados limpios y seguir avisando de los problemas. Borra el archivo: `rm salida.txt`.

### 3. La lógica, sin entrada ni salida

Descomenta el **PASO 3** y ejecuta `uv run python cli.py`. Las dos líneas nuevas:

```
Hola, Ana | 5 | EL AIRE
error: uso: sumar <entero> <entero> | error: comando desconocido: borrar | error: orden vacía
```

Relaciona cada respuesta con su `case`:

| Orden | `line.split()` | `case` que encaja |
|---|---|---|
| `"hola Ana"` | `['hola', 'Ana']` | `["hola", name]`: captura `name` |
| `"sumar 2 3"` | `['sumar', '2', '3']` | `["sumar", a, b]` y la guarda es verdadera |
| `"mayus el aire"` | `['mayus', 'el', 'aire']` | `["mayus", *words]`: `words` recibe `['el', 'aire']` |
| `"sumar dos 3"` | `['sumar', 'dos', '3']` | La guarda falla (`"dos"` no es decimal) y sigue: `["sumar", *_]` |
| `"borrar todo"` | `['borrar', 'todo']` | `[unknown, *_]` |
| `"  "` | `[]` | `[]` |

Ahora **quita la guarda** (`if a.isdecimal() and b.isdecimal()`) y ejecuta: `int("dos")` lanza `ValueError` y el programa se detiene. Vuelve a ponerla.

### 4. `main` habla con el exterior

Antes de seguir, **vuelve a comentar** las líneas `print(...)` de los pasos 1, 2 y 3 (deja los `def` descomentados), para ver solo lo que escribe `main`. Después descomenta el **PASO 4** y prueba cada caso:

```bash
uv run python cli.py "sumar 2 3"; echo "código: $?"
uv run python cli.py "sumar 2 x"; echo "código: $?"
uv run python cli.py sumar 2 3; echo "código: $?"
```

```
5
código: 0
error: uso: sumar <entero> <entero>
código: 1
uso: cli.py ["orden"]
código: 2
```

| Caso | Qué pasó | Código |
|---|---|---|
| `"sumar 2 3"` | Un argumento, orden válida, respuesta en stdout | `0` |
| `"sumar 2 x"` | Un argumento, respuesta de error en stderr | `1` |
| `sumar 2 3` sin comillas | Tres argumentos: `case _` en `main` | `2` |

Comprueba que el error va a stderr: `uv run python cli.py "sumar 2 x" 2>/dev/null; echo "código: $?"` solo muestra `código: 1`. `2>` redirige stderr, y `/dev/null` es un archivo que descarta todo.

### 5. Sin argumentos: teclado y tubería

```bash
uv run python cli.py
```

El programa muestra `orden> ` y espera. Escribe `hola Luis` y pulsa Enter: responde `Hola, Luis`. Ahora sin teclado, con una tubería:

```bash
echo "mayus por tubería" | uv run python cli.py
```

```
orden> POR TUBERÍA
```

`input()` leyó de la tubería. Por último, sin nada que leer:

```bash
uv run python cli.py < /dev/null
```

Termina con `EOFError: EOF when reading a line` y código `1`: `input()` no tenía de dónde leer. En la semana 7 aprenderás a capturar ese error.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'run_command' is not defined` | Descomentaste el paso 4 sin el `def run_command` del paso 3 |
| `echo $?` da `0` aunque viste un error | Falta `raise SystemExit(main(...))` al final, o tienes `print(main(...))` |
| Las líneas de stdout y stderr salen en otro orden | Son dos canales con su propio búfer: el orden entre ellos no está garantizado |
| `uso: cli.py ["orden"]` cuando escribiste una orden | Te faltaron las comillas: sin ellas, cada palabra es un argumento |
| El programa se queda esperando | Sin argumentos lee del teclado: escribe una orden y pulsa Enter, o `Ctrl+D` para cortar |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Formateo y t-strings](../ejercicio-03-formateo-y-t-strings/README.md) | **Ejercicio 04 · Entrada, salida y `match`** | [Proyecto · Observatorio, capa 1](../../3-proyecto/README.md) |
