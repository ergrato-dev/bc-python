# 03 · Modelos de Pydantic

⏱️ 50 min

## 🎯 Objetivos

- Entender qué problema resuelve Pydantic y en qué se diferencia de mypy.
- Crear modelos con `BaseModel` y validar datos con `model_validate`.
- Leer un `ValidationError`: cuántos errores, dónde y de qué tipo.
- Elegir entre el modo normal (*lax*) y el estricto.
- Limitar campos con `Field`, prohibir claves de más y congelar modelos.

---

## 1. mypy no ve los datos

mypy revisa **tu código** antes de ejecutarlo. No puede revisar un archivo JSON que llega mañana, una petición HTTP o una fila de una base de datos. Cuando haces `json.loads`, mypy solo sabe que es `Any` (teoría 01).

Pydantic hace la otra mitad del trabajo: comprueba **los datos** al ejecutar, contra las mismas anotaciones que lee mypy. Si encajan, te da un objeto con los tipos que prometen sus campos. Si no, lanza un error que dice qué falla y dónde.

| | mypy | Pydantic |
|---|---|---|
| Cuándo | Antes de ejecutar | Al ejecutar |
| Qué revisa | Tu código | Los datos que llegan |
| Si algo no encaja | Un error en la terminal | `ValidationError` |
| Convierte valores | No | Sí: `"12.5"` → `12.5` |

Instalarlo en tu proyecto es una dependencia más, fijada como todas:

```bash
uv add pydantic==2.14.2
```

Pydantic 2 tiene su núcleo escrito en Rust (`pydantic-core`), y por eso es rápido. Lo usan FastAPI (semana 20), las bibliotecas de los LLM y muchas herramientas de configuración.

---

## 2. Un modelo

```python
from pydantic import BaseModel


class Reading(BaseModel):
    label: str
    value: float | None
```

Se escribe como una dataclass: un campo por anotación. Hay dos formas de crearlo:

```python
Reading(label="Norte", value=12.5)                         # desde tu código
Reading.model_validate({"label": "Sur", "value": "8.0"})   # desde datos de fuera
```

```
label='Norte' value=12.5
label='Sur' value=8.0
```

Las dos validan. Usa el constructor para los objetos que crea tu programa, y `model_validate` para un `dict` que viene de fuera: así se ve dónde entra un dato sin comprobar. Para un texto JSON está `model_validate_json` (teoría 04).

---

## 3. Modo normal y modo estricto

En el modo normal (*lax*), Pydantic **convierte** lo que tiene una conversión sin ambigüedad:

| Dato | Campo `float \| None` en modo normal | En modo estricto |
|---|---|---|
| `12.5` | `12.5` | `12.5` |
| `8` | `8.0` | `8.0` |
| `"8.0"` | `8.0` | ❌ `Input should be a valid number` |
| `True` | `1.0` | ❌ `Input should be a valid number` |
| `None` | `None` | `None` |
| `"doce"` | ❌ `Input should be a valid number, unable to parse string as a number` | ❌ `Input should be a valid number` |

La conversión es cómoda con datos de un formulario o de un CSV, donde todo es texto. Pero `True` → `1.0` es una trampa: un sensor que manda `true` por error se cuela como una medida. El modo estricto se activa en todo el modelo o en un solo campo:

```python
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class StrictReading(BaseModel):
    model_config = ConfigDict(strict=True)   # todo el modelo
    label: str
    value: float | None


class MeasurementIn(BaseModel):
    label: str
    value: Annotated[float | None, Field(strict=True)]   # solo este campo
```

Tu `MeasurementIn` usa el segundo: es estricto en `value` y convierte `"12,5"` con su propio validador (teoría 04).

---

## 4. `ValidationError`

```python
try:
    Reading.model_validate({"label": 5, "value": "doce"})
except ValidationError as error:
    print(error)
```

```
2 validation errors for Reading
label
  Input should be a valid string [type=string_type, input_value=5, input_type=int]
    For further information visit https://errors.pydantic.dev/2.14/v/string_type
value
  Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='doce', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/float_parsing
```

Pydantic no se para en el primer error: revisa todos los campos y los da juntos. Para tratarlos en código, `error.errors()` devuelve una lista de diccionarios:

| Clave | Qué es | Ejemplo |
|---|---|---|
| `loc` | Dónde: una tupla con el campo, y la posición si está en una lista | `('label',)`, `(1, 'value')` |
| `type` | Un código estable, para los tests y para decidir qué hacer | `string_type`, `missing`, `extra_forbidden` |
| `msg` | El mensaje, en inglés | `Input should be a valid string` |
| `input` | El dato que falló | `5` |

`error.error_count()` dice cuántos hay. En tu proyecto, `_invalid` toma el primero y lo convierte en un `DataFileError` en español con su `loc`: `datos no válidos en medidas.json: 1.label: String should have at least 1 character`.

`ValidationError` es una subclase de `ValueError`. Un `except ValueError` lo atrapa, pero es mejor nombrarlo: dice qué esperas.

---

## 5. `Field`, `ConfigDict` y modelos anidados

`Annotated[tipo, Field(...)]` junta un tipo y sus límites:

```python
class Station(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: Annotated[str, Field(min_length=1, max_length=20)]
    altitude: Annotated[float, Field(ge=0)] = 0.0
    tags: list[str] = Field(default_factory=list)
    readings: list[Reading] = []
```

| Opción | Qué hace |
|---|---|
| `min_length`, `max_length` | Longitud de un texto o una lista |
| `gt`, `ge`, `lt`, `le` | Mayor, mayor o igual, menor, menor o igual |
| `pattern` | Una expresión regular que el texto debe cumplir |
| `strict` | Sin conversión en este campo |
| `default_factory` | Un valor por defecto nuevo en cada instancia |

`model_config = ConfigDict(...)` configura el modelo entero:

| Opción | Qué hace | Por qué en `MeasurementIn` |
|---|---|---|
| `extra="forbid"` | Una clave desconocida es un error (`Extra inputs are not permitted`) | Por defecto se **ignora** en silencio: `"valor"` en lugar de `"value"` daría `Field required` en `value`, sin decir por qué |
| `frozen=True` | No se pueden cambiar los campos (`Instance is frozen`) y el modelo se puede usar en un `set` | Como tu `Measurement` |
| `str_strip_whitespace=True` | Quita los espacios de los lados de cada texto antes de validarlo | `"   "` es una etiqueta vacía |

Un campo cuyo tipo es otro modelo (`list[Reading]`) valida cada elemento con ese modelo: un JSON anidado se convierte en objetos anidados de una vez.

> A diferencia de una dataclass, `readings: list[Reading] = []` es seguro: Pydantic copia el valor por defecto en cada instancia. Y `model_copy(update={...})` copia **sin validar**: para cambiar datos y comprobarlos, vuelve a pasar por `model_validate`.

Con el plugin de Pydantic para mypy (`plugins = ["pydantic.mypy"]`), mypy conoce lo que el `ConfigDict` cambia. Por ejemplo, avisa de que un campo de un modelo `frozen` es de solo lectura:

```
error: Property "name" defined in "Station" is read-only  [misc]
```

---

## 🧯 Errores típicos

| Error | Causa | Solución |
|---|---|---|
| `Field required [type=missing, ...]` | Falta un campo sin valor por defecto, o está mal escrito | Revisa el nombre; con `extra="forbid"` verás también la clave mal escrita |
| `Extra inputs are not permitted` | Una clave que el modelo no tiene, con `extra="forbid"` | Quítala del dato, o añade el campo si de verdad existe |
| `Input should be a valid number` con `"8.0"` | El campo o el modelo son estrictos | Es lo que pediste; si quieres aceptar textos, un validador `before` (teoría 04) |
| `Instance is frozen` | Asignas a un campo de un modelo `frozen` | Crea uno nuevo con `model_validate` |
| `ModuleNotFoundError: No module named 'pydantic'` | No está en las dependencias del proyecto | `uv add pydantic==2.14.2` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué comprueba mypy y qué comprueba Pydantic.
- [ ] Cuándo usar el constructor y cuándo `model_validate`.
- [ ] Qué convierte el modo normal y por qué `True` → `1.0` es un problema.
- [ ] Leer un `ValidationError` con `errors()`: `loc`, `type` y `msg`.
- [ ] Qué hacen `extra="forbid"`, `frozen=True` y `Field(min_length=1)`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Tipos avanzados](02-tipos-avanzados.md) | **03 · Modelos de Pydantic** | [04 · Validadores y serialización](04-validadores-y-serializacion.md) |
