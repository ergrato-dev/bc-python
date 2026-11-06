# Ejercicio 01 — mypy estricto

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-mypy-estricto.md) y [02](../../1-teoria/02-tipos-avanzados.md)

## Objetivo

Ver qué añade `mypy --strict` a lo que ya hacías: funciones sin anotar, `Any` que se cuela desde `json.loads`, `None` que obliga a comprobar, `Literal` y `Final`, y por qué `cast` no convierte nada. Al final del ejercicio sabrás por qué tu proyecto activa `strict` y valida los JSON con Pydantic. Ejercicio **guiado**: descomentas cada paso de `strict_lab.py`, ejecutas el programa y mypy y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-13-typing_estricto_mypy_y_pydantic/2-practicas/ejercicio-01-mypy-estricto/starter
uv run python strict_lab.py
uvx --from mypy==2.4.1 mypy --strict strict_lab.py
```

```
Ejercicio 01 · mypy estricto
Success: no issues found in 1 source file
```

Después de cada paso, ejecuta las dos órdenes. Con lo que traen, mypy siempre dice `Success`: las líneas que darían error llevan un `# type: ignore[código]`, que quitas cuando el paso te lo pida y vuelves a poner después. Los pasos no dependen unos de otros, pero descomenta en orden. Cada salida de abajo muestra solo las líneas nuevas del paso.

## Pasos

### 1. Funciones sin anotar

Descomenta el **PASO 1** y ejecuta:

```
Sin anotar: 10.25 · anotada: 10.25
Sin anotar, el error llega al ejecutar: unsupported operand type(s) for +: 'int' and 'str'
```

Quita los tres `# type: ignore` del paso (líneas 17, 25 y 28) y ejecuta mypy **sin** `--strict`:

```bash
uvx --from mypy==2.4.1 mypy strict_lab.py
```

```
Success: no issues found in 1 source file
```

Sin anotaciones, mypy no revisa la función ni sus llamadas: la trata como si todo fuera `Any`. Por eso no avisa de que `mean_untyped(["12,5", "8"])` suma textos. Ahora con `--strict`:

```
strict_lab.py:17: error: Function is missing a type annotation  [no-untyped-def]
strict_lab.py:25: error: Call to untyped function "mean_untyped" in typed context  [no-untyped-call]
strict_lab.py:28: error: Call to untyped function "mean_untyped" in typed context  [no-untyped-call]
Found 3 errors in 1 file (checked 1 source file)
```

`strict` exige anotar cada función y no deja llamar a las que no lo están. Vuelve a poner los tres comentarios.

### 2. `Any` se cuela

Descomenta el **PASO 2** y ejecuta:

```
mypy cree que es float; en realidad es str
Comprobado: 50.0
Comprobado: limit debe ser un número, no '50'
```

`json.loads` devuelve `Any`: mypy no sabe qué hay dentro y deja pasar cualquier uso. `read_limit` promete un `float` y devuelve el texto `"50"`. Quita el `# type: ignore` de la línea 38 y ejecuta mypy:

```
strict_lab.py:38: error: Returning Any from function declared to return "float"  [no-any-return]
```

`read_limit_checked` lo hace bien: guarda el resultado como `object`, que obliga a comprobar el tipo con `isinstance` antes de usarlo. Funciona, pero con muchos campos se hace largo: es lo que Pydantic hará por ti en el ejercicio 03.

### 3. `None` obliga a comprobar

Descomenta el **PASO 3** y ejecuta:

```
Niveles: ['alto', 'sin dato', 'bajo']
```

Borra las líneas 66 y 67 (el `if value is None:` y su `return`) y ejecuta mypy:

```
strict_lab.py:66: error: Unsupported operand types for < ("int" and "None")  [operator]
strict_lab.py:66: note: Left operand is of type "float | None"
```

`value > 50` con un `None` lanzaría `TypeError` al ejecutar; mypy lo ve antes. El `if value is None: return` **estrecha** el tipo: debajo, `value` es `float`. `is_number` hace lo mismo con una función propia: devolver `TypeIs[float]` le dice a mypy que, cuando da `True`, el valor es `float`. Por eso el `"12,5"` de la lista se queda fuera. Vuelve a poner las dos líneas.

### 4. `Literal` y `Final`

Descomenta el **PASO 4** y ejecuta:

```
alto se pinta de rojo
Python no comprueba el Literal: KeyError 'altísimo'
Final tampoco se comprueba al ejecutar: HIGH vale 60.0
```

`Level` solo admite tres textos y `HIGH` es una constante. Python no comprueba ninguna de las dos cosas: las anotaciones no se ejecutan. Quita los `# type: ignore` de las líneas 94 y 97 y ejecuta mypy:

```
strict_lab.py:94: error: Argument 1 to "color" has incompatible type "Literal['altísimo']"; expected "Literal['bajo', 'medio', 'alto']"  [arg-type]
strict_lab.py:97: error: Cannot assign to final name "HIGH"  [misc]
```

Vuelve a ponerlos.

### 5. `cast` promete, no convierte

Descomenta el **PASO 5** y ejecuta:

```
Después de cast: '12,5' es str
Y falla al usarlo: can only concatenate str (not "int") to str
```

`cast(float, raw)` le dice a mypy "créeme, es un `float`" y devuelve el mismo objeto sin tocarlo. mypy no protesta y el programa falla igual. Úsalo solo cuando sepas algo que mypy no puede deducir. Si el dato viene de fuera, compruébalo (paso 2) o valídalo con Pydantic.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `error: unused "type: ignore" comment` | Ese `# type: ignore` ya no tapa nada: bórralo o vuelve a dejar la línea como estaba |
| mypy no dice nada aunque quitaste los `# type: ignore` | Ejecutaste mypy sin `--strict` |
| Los números de línea no coinciden | Descomentaste algo de más o borraste líneas en blanco: vuelve a descargar el archivo |
| `uvx: command not found` | Instala uv como en la semana 1 y abre una terminal nueva |
| `ImportError: cannot import name 'TypeIs'` | Tu Python es anterior a 3.13: comprueba que `uv run python --version` da 3.14.10 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Fronteras y diseño](../../1-teoria/05-fronteras-y-diseno.md) | **Ejercicio 01 · mypy estricto** | [Ejercicio 02 · Tipos avanzados](../ejercicio-02-tipos-avanzados/README.md) |
