# Ejercicio 03 — Modelos de Pydantic

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-modelos-pydantic.md)

## Objetivo

Crear modelos con `BaseModel` y ver qué convierte Pydantic y qué rechaza. Lees un `ValidationError` campo a campo, activas el modo estricto, añades restricciones con `Field`, prohíbes claves de más y anidas modelos. Es lo que hace `MeasurementIn` en tu proyecto. Ejercicio **guiado**: descomentas cada paso de `models_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

Este ejercicio tiene una dependencia, `pydantic==2.14.2`, ya fijada en su `pyproject.toml` y en su `uv.lock`. `uv run` la instala la primera vez:

```bash
cd bootcamp/week-13-typing_estricto_mypy_y_pydantic/2-practicas/ejercicio-03-modelos-pydantic/starter
uv run python models_lab.py
uv run --with mypy==2.4.1 mypy --strict models_lab.py
```

```
Ejercicio 03 · Modelos de Pydantic
Success: no issues found in 1 source file
```

mypy se ejecuta ahora con `uv run --with` y no con `uvx`: así ve el Pydantic del entorno del ejercicio y el plugin que activa el `pyproject.toml`. Descomenta en orden: cada paso usa los modelos de los anteriores. Cada salida de abajo muestra solo las líneas nuevas del paso.

## Pasos

### 1. Un modelo valida y convierte

Descomenta el **PASO 1** y ejecuta:

```
Con el constructor: label='Norte' value=12.5
repr: Reading(label='Norte', value=12.5)
Un texto con un número: label='Sur' value=8.0
Un entero: label='Sur' value=8.0
Un booleano: label='Sur' value=1.0
```

`Reading` se escribe como una dataclass: un campo por anotación. La diferencia está en lo que pasa al crearlo. Pydantic **valida** cada campo y, en su modo normal (*lax*), **convierte** lo que tiene una conversión clara: `"8.0"` y `8` pasan a `8.0`.

Fíjate en la última línea: `True` también se convierte, en `1.0`. Es la trampa que tu proyecto cierra con `strict=True` en el campo `value`.

El constructor, `Reading(label=..., value=...)`, es para los datos que crea tu código. Para los de fuera (un `dict` de `json.loads`, una petición HTTP), usa `Reading.model_validate(datos)`: se lee claro dónde entra un dato sin comprobar. Con el plugin de Pydantic, mypy avisa si al constructor le falta un campo (`Missing named argument "value" for "Reading"`), pero no de sus tipos: Pydantic los convierte al ejecutar.

### 2. `ValidationError` dice qué falla y dónde

Descomenta el **PASO 2** y ejecuta:

```
Errores: 2
2 validation errors for Reading
label
  Input should be a valid string [type=string_type, input_value=5, input_type=int]
    For further information visit https://errors.pydantic.dev/2.14/v/string_type
value
  Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='doce', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/float_parsing
   ('label',) string_type · Input should be a valid string
   ('value',) float_parsing · Input should be a valid number, unable to parse string as a number
```

Pydantic no se para en el primer error: revisa todos los campos y te los da juntos. Un `ValidationError` es una excepción, y además trae los datos de cada fallo. `error.errors()` es una lista de diccionarios con:

- `loc`: dónde está el fallo, una tupla con el nombre del campo;
- `type`: un código estable, útil en los tests;
- `msg`: el mensaje, en inglés.

`_invalid` en tu proyecto usa el primero de ellos para el mensaje de `DataFileError`.

### 3. Modo estricto

Descomenta el **PASO 3** y ejecuta:

```
Un entero sigue valiendo: label='N' value=3.0
'8.0' en estricto: Input should be a valid number
True en estricto: Input should be a valid number
```

`ConfigDict(strict=True)` desactiva las conversiones para todo el modelo. Solo queda la que no pierde nada, de entero a `float`. `strict` también puede ir en un campo solo: `Annotated[float | None, Field(strict=True)]`, que es lo que usa tu `MeasurementIn` para rechazar `true` y aceptar `"12,5"` con su propio validador (ejercicio 04).

### 4. Restricciones con `Field` y claves de más

Descomenta el **PASO 4** y ejecuta:

```
Con los valores por defecto: name='Norte' altitude=0.0 tags=[] readings=[]
3 validation errors for Station
name
  String should have at least 1 character [type=string_too_short, input_value='', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/string_too_short
altitude
  Input should be greater than or equal to 0 [type=greater_than_equal, input_value=-5, input_type=int]
    For further information visit https://errors.pydantic.dev/2.14/v/greater_than_equal
zone
  Extra inputs are not permitted [type=extra_forbidden, input_value='centro', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/extra_forbidden
```

`Annotated[str, Field(min_length=1, max_length=20)]` junta el tipo y sus límites; `ge=0` es *greater or equal*, mayor o igual que 0. Hay más: `gt`, `lt`, `le` y `pattern`. Con `extra="forbid"`, una clave que el modelo no conoce es un error. Sin él, Pydantic la **ignora** en silencio, y un `"valor"` mal escrito por `"value"` acabaría como un campo que falta.

A diferencia de una dataclass, `readings: list[Reading] = []` es seguro: Pydantic copia el valor por defecto en cada instancia. `Field(default_factory=list)` hace lo mismo y es más explícito.

### 5. Modelos anidados, `frozen` y `model_copy`

Descomenta el **PASO 5** y ejecuta:

```
Anidado: [Reading(label='N1', value=12.5), Reading(label='N2', value=None)]
Cada medida es un Reading: Reading
frozen: Instance is frozen
model_copy no valida: -100
model_validate sí: 2600.0
```

Un campo `list[Reading]` valida cada diccionario de la lista como un `Reading`. Con `frozen=True`, cambiar un campo lanza `ValidationError`. Quita el `# type: ignore` de la línea 88 y ejecuta mypy:

```
models_lab.py:88: error: Property "name" defined in "Station" is read-only  [misc]
```

Lo sabe gracias al plugin de Pydantic; sin él, mypy no avisa. Vuelve a ponerlo.

`model_copy(update=...)` crea una copia **sin validar**: la altitud `-100` se ha colado. Para cambiar datos y validarlos, vuelve a pasar por `model_validate`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'pydantic'` | Ejecutas `python` en lugar de `uv run python`, o estás fuera de `starter/` |
| mypy dice `Error importing plugin "pydantic.mypy": No module named 'pydantic'` | Usaste `uvx`: con `uvx`, mypy no ve el entorno del ejercicio. Usa `uv run --with mypy==2.4.1 mypy ...` |
| `NameError: name 'Reading' is not defined` | Descomenta antes el paso 1 |
| Ves `URL` y `For further information` en cada error | Es normal: `str(error)` los incluye. `error.errors()` da solo los datos |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Tipos avanzados](../ejercicio-02-tipos-avanzados/README.md) | **Ejercicio 03 · Modelos de Pydantic** | [Ejercicio 04 · Validadores y JSON](../ejercicio-04-validadores-y-json/README.md) |
