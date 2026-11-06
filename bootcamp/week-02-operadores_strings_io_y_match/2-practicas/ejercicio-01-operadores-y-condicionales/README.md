# Ejercicio 01 — Operadores y condicionales

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-operadores-y-expresiones.md) y [02](../../1-teoria/02-condicionales-y-match.md)

## Objetivo

Ver en acción `//` y `%`, el cortocircuito de `and`/`or`, los rangos con `if`/`elif`, la expresión condicional y un `match` con alternativas. Ejercicio **guiado**: el código está en `ops_lab.py`, comentado por pasos; lo descomentas, ejecutas y comparas con la salida esperada. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-02-operadores_strings_io_y_match/2-practicas/ejercicio-01-operadores-y-condicionales/starter
uv run python ops_lab.py
```

Salida esperada: `Ejercicio 01 · Operadores y condicionales`.

En cada paso: **predice** primero la salida (mira el código y escríbela en un papel), descomenta el bloque (`Ctrl+K Ctrl+U` en VS Code), ejecuta `uv run python ops_lab.py` y compara. Las salidas de abajo son las **líneas nuevas** de cada paso.

## Pasos

### 1. `//` y `%` reparten minutos en horas

Descomenta el **PASO 1**:

```
135 minutos: 2 h 15 min
59 minutos: 0 h 59 min
-7 // 2 = -4 y -7 % 2 = 1
```

`135 // 60` es `2` (caben 2 horas) y `135 % 60` es `15` (sobran 15 minutos). La tercera línea es el caso que sorprende: `//` redondea **hacia abajo**, y hacia abajo de `-3.5` está `-4`. Comprueba en el REPL (`uv run python`) que se cumple `(-4) * 2 + 1 == -7`.

### 2. `and`, `or` y el orden de las condiciones

Descomenta el **PASO 2**:

```
Bisiestos: True False True False
```

Sigue `1900` a mano: `1900 % 4 == 0` es `True`, pero `1900 % 100 != 0` es `False`, así que el paréntesis da `False`; `1900 % 400 == 0` también es `False`. Resultado: `False`. Haz lo mismo con `2000`: el paréntesis da `False`, pero el `or` lo salva.

### 3. `or` para dar un valor por defecto

Descomenta el **PASO 3**:

```
Etiquetas: Norte | sin etiqueta
La trampa del or: 10 | sin dato
```

`"   ".strip()` es `""`, que es falso: `or` devuelve el valor por defecto. La segunda línea muestra el peligro: `0` y `0.0` también son falsos. Si en tu dominio una medida de `0.0` es real, `value or "sin dato"` la borra sin avisar. Por eso el proyecto usa `is None`.

### 4. `if` / `elif` / `else` por rangos

Descomenta el **PASO 4**:

```
Notas: insuficiente | aceptable | aceptable | sobresaliente
```

Mira los límites: `3.0` ya es "aceptable" (porque `3.0 < 3.0` es falso) y `4.0` ya es "sobresaliente". Ahora **cambia el orden**: pon la rama `score < 4.0` antes de `score < 3.0` y ejecuta. `grade(2.9)` sale "aceptable": el primer `if` verdadero gana. Deja el orden como estaba.

### 5. Expresión condicional

Descomenta el **PASO 5**:

```
Divisiones: 2.5 None
```

Sin el `None if b == 0 else`, `safe_ratio(10, 0)` daría `ZeroDivisionError: division by zero`. Pruébalo en el REPL con `10 / 0`.

### 6. `match` con literales y alternativas

Descomenta el **PASO 6**:

```
Días: laborable | fin de semana | inválido
```

Borra el `case _:` y su `return` y ejecuta: `day_type(9)` devuelve `None` porque ningún `case` encajó y la función terminó sin `return`. Vuelve a ponerlos.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `IndentationError: unexpected indent` | Al descomentar quedó un espacio de más al principio de la línea |
| `IndentationError: expected an indented block after 'if' statement` | Quitaste también la sangría del bloque: dentro de `def`, `if` y `case` van 4 espacios más |
| `NameError: name 'grade' is not defined` | Descomentaste el `print` pero no el `def` |
| `SyntaxError: expected ':'` | Borraste los `:` al final de `if`, `elif`, `else`, `match` o `case` |
| `Bisiestos:` no coincide | Revisa los paréntesis: `and` va antes que `or` aunque no los pongas, pero con ellos se lee mejor |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Entrada y salida](../../1-teoria/05-entrada-y-salida.md) | **Ejercicio 01 · Operadores y condicionales** | [Ejercicio 02 · Strings](../ejercicio-02-strings/README.md) |
