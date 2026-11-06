# Ejercicio 03 — Type hints y `mypy`

⏱️ 1 h · Teoría previa: [04](../../1-teoria/04-type-hints.md)

## Objetivo

Comprobar que Python ejecuta sin quejarse un código con los tipos equivocados, y que `mypy` encuentra esos errores **sin ejecutarlo**. Arreglarás los tres errores que trae el código. Ejercicio **guiado**: no se entrega.

## Antes de empezar

```bash
cd bootcamp/week-04-funciones_scope_type_hints_y_pytest/2-practicas/ejercicio-03-type-hints/starter
uv run python hints_lab.py
uv run --with mypy==2.4.1 mypy hints_lab.py
```

```
Ejercicio 03 · Type hints
Success: no issues found in 1 source file
```

`uv run --with mypy==2.4.1` usa `mypy` solo para este comando, sin añadirlo al proyecto. La primera vez lo descarga y tarda unos segundos. En la semana 13 lo añadirás al proyecto y lo usarás en modo estricto.

## Pasos

### 1. Las anotaciones no se comprueban al ejecutar

Descomenta el **PASO 1** y ejecuta con `python`:

```
double(21) = 42
double('ab') = abab
Anotaciones: {'n': <class 'int'>, 'return': <class 'int'>}
```

`double` dice que recibe un `int`, le pasaste un `str` y Python lo ejecutó igualmente: `"ab" * 2` es `"abab"`. Las anotaciones solo se guardan en `__annotations__`. Ahora revisa con `mypy`:

```
hints_lab.py:20: error: Argument 1 to "double" has incompatible type "str"; expected "int"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

`mypy` lee el código sin ejecutarlo y compara cada llamada con las anotaciones. Arréglalo: comenta la línea 20 (`double("ab")`) y repite: `Success`.

### 2. `float | None`

Descomenta el **PASO 2**. Con `python` funciona:

```
double_reading('12,5') = 25.0
```

Con `mypy`:

```
hints_lab.py:36: error: Unsupported operand types for * ("None" and "int")  [operator]
hints_lab.py:36: note: Left operand is of type "float | None"
```

`parse_value` puede devolver `None`, y `None * 2` es un `TypeError`. Con `"12,5"` no pasa, pero con `"NA"` sí. `mypy` lo ve sin que tengas que probar ese caso. Arréglalo comprobando el `None` antes de usar el valor, y di en la firma que el resultado también puede faltar:

```python
def double_reading(text: str) -> float | None:
    value = parse_value(text)
    if value is None:
        return None
    return value * 2
```

Después de `if value is None: return None`, `mypy` sabe que `value` ya es un `float`. Añade al `print` un caso con `"NA"`, ejecuta (sale `None`) y repite `mypy`: `Success`.

### 3. Tipos de lo que se devuelve

Descomenta el **PASO 3**. Con `python`:

```
Promedio: 25.2
Mejor estación: ('Centro', 55.1)
```

Con `mypy`:

```
hints_lab.py:50: error: Incompatible return value type (got "str", expected "float")  [return-value]
```

`average` promete un `float` y devuelve un texto formateado: se ve bien al imprimir, pero quien quiera sumar ese promedio recibirá un `str`. Arréglalo: que `average` devuelva `total / len(values)` y que el formato lo haga el `print`, con `f"Promedio: {average([12.5, 8.0, 55.1]):.1f}"`. Ejecuta las dos órdenes: misma salida y `Success: no issues found in 1 source file`.

`best_station` no da error: `tuple[str, float]` coincide con lo que devuelve.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `error: Failed to spawn: mypy` | Escribe `uv run --with mypy==2.4.1 mypy`, con `mypy` dos veces: la primera es el paquete y la segunda el comando |
| Los números de línea no coinciden con los del README | Añadiste o borraste líneas; busca el error por el texto, no por el número |
| `mypy` sigue diciendo `float \| None` después de arreglarlo | El `if value is None` no tiene `return` dentro, o usas `parse_value(text)` otra vez en lugar de `value` |
| `TypeError: unsupported format string passed to str.__format__` | Aplicaste `:.1f` a un texto: `average` todavía devuelve `str` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Scope y funciones como valores](../ejercicio-02-scope-y-funciones-como-valores/README.md) | **Ejercicio 03 · Type hints** | [Ejercicio 04 · pytest desde cero](../ejercicio-04-pytest-desde-cero/README.md) |
