# Ejercicio 03 — Tipos y conversiones

⏱️ 2 h 30 min · Teoría previa: [05](../../1-teoria/05-variables-y-tipos.md)

## Objetivo

Implementar seis funciones pequeñas que te obligan a mirar de frente los detalles de los tipos: conversiones que fallan, `float` inexactos, `int` sin límite y la diferencia entre `None` y "vacío".

## Antes de empezar

```bash
cd bootcamp/week-01-entorno_docker_uv_y_tipos/2-practicas/ejercicio-03-tipos-y-conversiones/starter
uv run pytest
```

Salida esperada: `17 failed, 1 passed`. Hay 18 tests aunque el archivo tiene menos funciones de test: `@pytest.mark.parametrize` ejecuta la misma prueba con varios valores, y pytest cuenta cada valor como un test. El que ya pasa (`test_float_sum_is_not_exact_with_double_equals`) documenta cómo se comportan los `float`: no lo cambies.

Para cada paso: **primero prueba en el REPL** (`uv run python`), después escribe la función en `types_lab.py` y ejecuta solo sus tests con `-k`.

## Pasos

### 1. Predice antes de ejecutar

Sin ejecutar nada, escribe en `NOTAS.md` qué crees que da cada línea. Después compruébalo en el REPL y marca tus aciertos:

```python
type(7 / 2)
int(3.99)
bool("False")
bool("")
0.1 * 3 == 0.3
True + True
```

### 2. `type_name`

En el REPL:

```python
>>> type(3.0)
<class 'float'>
>>> type(3.0).__name__
'float'
>>> type(None).__name__
'NoneType'
```

`__name__` da el nombre del tipo como texto. Implementa `type_name` con `return type(value).__name__`.

```bash
uv run pytest -k type_name
```

Esperado: `5 passed, 13 deselected` (un test por cada valor del `parametrize`).

### 3. `to_int`

```python
>>> int(" 42 ")
42
>>> int("4.5")
ValueError: invalid literal for int() with base 10: '4.5'
```

`int()` ya ignora los espacios. Implementa `to_int` con `return int(text)`. El test `test_to_int_rejects_decimal_text` **espera** el `ValueError`: no lo evites, es el comportamiento correcto. Si llega un texto con decimales, el que llama a la función decide qué hacer.

```bash
uv run pytest -k to_int
```

Esperado: `2 passed`.

### 4. `to_float`

Tiene que aceptar `"3.5"` y `"3,5"`. En el REPL:

```python
>>> float("3,5")
ValueError: could not convert string to float: '3,5'
>>> "3,5".replace(",", ".")
'3.5'
```

Implementa `to_float`: quita espacios con `strip()`, cambia la coma por punto con `replace` y convierte con `float`. Puedes encadenar los métodos: `text.strip().replace(",", ".")`.

```bash
uv run pytest -k to_float
```

Esperado: `2 passed`.

### 5. `floats_are_equal`

```python
>>> import math
>>> 0.1 + 0.2 == 0.3
False
>>> math.isclose(0.1 + 0.2, 0.3)
True
>>> math.isclose(0.3, 0.31)
False
```

El archivo ya importa `math`. Implementa `floats_are_equal` con `return math.isclose(a, b)`.

```bash
uv run pytest -k floats_are_equal
```

Esperado: `2 passed`. En `NOTAS.md`, explica con tus palabras por qué `0.1 + 0.2 == 0.3` es `False`.

### 6. `digits_of_power_of_two`

`2**exponent` es la potencia (`**` significa "elevado a"). Para contar cifras, convierte el número en texto y mide su longitud con `len`:

```python
>>> 2**10
1024
>>> str(2**10)
'1024'
>>> len(str(2**10))
4
>>> len(str(2**100))
31
```

Implementa `digits_of_power_of_two` con `return len(str(2**exponent))`. Prueba después `2**1000` en el REPL: en Python un `int` no tiene límite de tamaño.

```bash
uv run pytest -k digits
```

Esperado: `1 passed`.

### 7. `is_missing`

`None` es "no hay dato"; `0`, `""`, `0.0` y `False` sí son datos. En el REPL:

```python
>>> None is None
True
>>> 0 is None
False
>>> not 0
True
```

La última línea es la trampa: `not value` es `True` para `0` y `""`, así que **no** sirve para saber si falta el dato. Implementa `is_missing` con `return value is None`.

```bash
uv run pytest
```

Esperado: `18 passed`. Ejecuta también el programa:

```bash
uv run python types_lab.py
```

```
int float str bool NoneType
42 3.5
False True
31
True False
3.141592653589793
```

### 8. Comprueba que las anotaciones no se verifican al ejecutar

En el REPL:

```python
>>> from types_lab import to_int
>>> to_int(42)
42
```

`to_int` dice recibir `text: str`, pero le pasaste un `int` y Python no protestó por el tipo: ejecutó la función. (Si en el paso 3 usaste `int(text.strip())`, verás `AttributeError: 'int' object has no attribute 'strip'`: el error llega igual, pero tarde, dentro de la función.) Responde en `NOTAS.md`: ¿quién detectaría este error, y en qué semana del bootcamp lo verás? (Pista: [teoría 05](../../1-teoria/05-variables-y-tipos.md), sección 5.)

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'math' is not defined` en el REPL | Escribe `import math` antes de usarlo; en `types_lab.py` ya está importado |
| `test_to_int_rejects_decimal_text` falla con `DID NOT RAISE` | Tu `to_int` está convirtiendo de más (por ejemplo, con `float` primero). Usa solo `int(text)` |
| `test_empty_values_are_not_missing[0]` falla | Usaste `not value` o `value == None`; usa `value is None` |
| `-k` no selecciona ningún test (`18 deselected`) | Revisa que el texto de `-k` aparece en el nombre del test |

## Entrega

`uv run pytest` con 18 de 18 en verde, y `NOTAS.md` con las predicciones del paso 1 y las respuestas de los pasos 5 y 8.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Python en Docker](../ejercicio-02-python-en-docker/README.md) | **Ejercicio 03 · Tipos y conversiones** | [Proyecto · Observatorio, capa 0](../../3-proyecto/README.md) |
