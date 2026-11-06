# 04 · Validadores y serialización

⏱️ 50 min

## 🎯 Objetivos

- Añadir reglas propias a un campo con `field_validator`, antes y después del tipo.
- Comprobar varios campos a la vez con `model_validator`.
- Saber en qué orden valida Pydantic cada dato.
- Pasar un modelo a `dict` y a JSON, y leerlo de vuelta.
- Validar listas y dataclasses con `TypeAdapter`.

---

## 1. `field_validator`: reglas de un campo

`Field` cubre los límites comunes. Para lo demás, escribes una función:

```python
from pydantic import BaseModel, field_validator


class Reading(BaseModel):
    label: str
    value: float | None

    @field_validator("label")
    @classmethod
    def clean_label(cls, label: str) -> str:
        if any(char.isdigit() for char in label):
            raise ValueError("la etiqueta no lleva números")
        return label.strip().title()
```

```
Reading.model_validate({"label": "  zona norte ", "value": 12.5})  →  label='Zona Norte' value=12.5
Reading.model_validate({"label": "Norte2", "value": 12.5})         →  Value error, la etiqueta no lleva números
```

Tres reglas:

- **Lo que devuelve se guarda.** Sin `return`, el campo queda en `None`.
- **Un `ValueError` es un error de validación.** Pydantic añade el prefijo `Value error, ` y lo junta con los demás errores. Con un `assert`, igual, pero `python -O` quita los `assert`: usa `ValueError`.
- **`@classmethod` debajo.** El validador se ejecuta antes de que exista la instancia: recibe la clase, no `self`.

---

## 2. Antes o después del tipo

Por defecto, un `field_validator` es `mode="after"`: se ejecuta **después** de validar el tipo y recibe un `str` seguro. Con `mode="before"` se ejecuta **antes** y recibe el dato tal como llega, sea lo que sea: por eso se anota como `object`.

```python
    @field_validator("value", mode="before")
    @classmethod
    def parse_text(cls, value: object) -> object:
        if isinstance(value, str):
            return parse_value(value)
        return value
```

Es el validador de tu `MeasurementIn`. Un `"12,5"` fallaría al validarse como número, así que hay que convertirlo antes. Lo que no es texto sigue igual, para que Pydantic lo valide después como siempre.

![El orden de validación de un campo: el dato de entrada pasa por los validadores before, después por la validación del tipo y los límites de Field, después por los validadores after; cuando todos los campos están validados, el model_validator after recibe el modelo](../0-assets/02-orden-de-validacion.svg)

| Paso | Recibe | Para qué |
|---|---|---|
| `field_validator(mode="before")` | El dato crudo (`object`) | Convertir formatos: coma decimal, `"NA"`, fechas en texto |
| Tipo y `Field` | Lo que devuelve el `before` | La comprobación de siempre: tipo, conversión o `strict`, límites |
| `field_validator(mode="after")` | Un valor del tipo del campo | Reglas del dominio: normalizar, rechazar valores raros |
| `model_validator(mode="after")` | El modelo entero (`self`) | Reglas que comparan campos |

Si un paso falla, ese campo no sigue, y el `model_validator` no se ejecuta.

---

## 3. `model_validator`: reglas entre campos

Un `field_validator` ve un solo campo. Que `low` sea menor que `high` necesita los dos:

```python
from typing import Self

from pydantic import BaseModel, model_validator


class Thresholds(BaseModel):
    low: float
    high: float

    @model_validator(mode="after")
    def check_order(self) -> Self:
        if self.low >= self.high:
            raise ValueError(f"low ({self.low}) debe ser menor que high ({self.high})")
        return self
```

```
Thresholds(low=50, high=10)  →  () Value error, low (50.0) debe ser menor que high (10.0)
```

Recibe el modelo ya validado y **lo devuelve**. Sin `return self`, Pydantic avisa con un `UserWarning`. El error no pertenece a ningún campo: su `loc` es `()`.

Tu `Scale` ya hace esta comprobación en su `__post_init__`, desde la semana 9. En la sección 5 verás que no hace falta repetirla.

---

## 4. Serializar: de modelo a JSON y vuelta

| Método | De | A |
|---|---|---|
| `modelo.model_dump()` | Modelo | `dict` |
| `modelo.model_dump(exclude_none=True)` | Modelo | `dict` sin los campos `None` |
| `modelo.model_dump_json()` | Modelo | Texto JSON |
| `Modelo.model_validate(datos)` | `dict` | Modelo validado |
| `Modelo.model_validate_json(texto)` | Texto JSON | Modelo validado |
| `Modelo.model_json_schema()` | La clase | Un esquema JSON que la describe |

```python
text = Reading(label="Norte", value=12.5).model_dump_json()
print(text)                                # {"label":"Norte","value":12.5}
print(Reading.model_validate_json(text))   # label='Norte' value=12.5
```

`model_validate_json` lee y valida en un solo paso, sin `json.loads`. Es más rápido, y un JSON roto también es un `ValidationError`:

```
json_invalid · Invalid JSON: EOF while parsing an object at line 1 column 32
```

Así, un solo `except ValidationError` cubre "no es JSON" y "es JSON pero no encaja". `read_json`, de la semana 7, necesitaba dos comprobaciones para lo mismo.

`model_json_schema()` describe el modelo con el estándar JSON Schema. FastAPI lo usa para documentar sus APIs en la semana 20, y los LLM, para pedir respuestas con una forma fija en la semana 37.

---

## 5. `TypeAdapter`: validar cualquier tipo

`model_validate` es un método de un `BaseModel`. Un JSON con una **lista** de medidas no es un modelo, y tu `Scale` es una dataclass. `TypeAdapter` valida cualquier tipo:

```python
from pydantic import TypeAdapter

readings = TypeAdapter(list[Reading])
items = readings.validate_json('[{"label": "Norte", "value": 12.5}, {"label": "Sur", "value": null}]')
```

En una lista, el `loc` empieza por la posición: `(1, 'value')` es el campo `value` de la segunda medida.

Con una dataclass normal, Pydantic valida y convierte sus campos y **ejecuta su `__post_init__`**:

```python
scales = TypeAdapter(Scale)
scales.validate_json('{"unit": "ppm", "low": "10", "high": 50}')   # Scale(unit='ppm', low=10.0, high=50.0)
scales.validate_json('{"unit": "ppm", "low": 50, "high": 10}')     # Value error, umbrales imposibles: ...
```

Tu proyecto no necesita un `ScaleIn` que repita la regla: la regla vive en `Scale`, una sola vez. `MeasurementIn` sí existe, porque sus reglas son **de la entrada** y no del modelo. Que un valor llegue como `"12,5"`, que una etiqueta traiga espacios o que sobre una clave son cosas del formato JSON, y tu `Measurement` no tiene por qué saberlas.

> Crear un `TypeAdapter` es lo caro, porque construye el validador; usarlo es rápido. Créalo una vez, a nivel de módulo, como `_MEASUREMENTS` y `_SCALE` en `schemas.py`, y no dentro de una función que se llama mil veces.

---

## 🧯 Errores típicos

| Error | Causa | Solución |
|---|---|---|
| El campo sale `None` | El `field_validator` no tiene `return` | Devuelve el valor |
| ``UserWarning: A custom validator is returning a value other than `self`.`` | El `model_validator(mode="after")` no devuelve `self` | Termina con `return self` |
| `PydanticUserError: Decorators defined with incorrect fields` | `@field_validator("lable")`: ese campo no existe | Escribe bien el nombre del campo |
| `'12,5'`: `unable to parse string as a number` | El validador es `after`: el texto falla antes de llegar a él | `mode="before"` |
| `Input should be a valid array` | `TypeAdapter(list[...])` recibe un objeto `{...}` | El JSON debe ser una lista `[...]` |

---

## ✅ Qué debes saber al terminar

- [ ] La diferencia entre `mode="before"` y `mode="after"`, y qué recibe cada uno.
- [ ] El orden en que Pydantic aplica validadores, tipo y `model_validator`.
- [ ] Cuándo un error tiene `loc` vacío.
- [ ] Pasar un modelo a JSON y leerlo de vuelta, y por qué `model_validate_json` simplifica `read_json`.
- [ ] Para qué sirve `TypeAdapter` y por qué tu proyecto no tiene un `ScaleIn`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Modelos de Pydantic](03-modelos-pydantic.md) | **04 · Validadores y serialización** | [05 · Fronteras y diseño](05-fronteras-y-diseno.md) |
