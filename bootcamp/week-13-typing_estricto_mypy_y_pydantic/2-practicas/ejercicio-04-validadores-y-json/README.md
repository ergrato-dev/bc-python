# Ejercicio 04 — Validadores y JSON

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-validadores-y-serializacion.md) y [05](../../1-teoria/05-fronteras-y-diseno.md)

## Objetivo

Escribir tus propias reglas con `field_validator` (después y antes del tipo) y `model_validator`, pasar un modelo a JSON y volver, y validar con `TypeAdapter` lo que no es un `BaseModel`: una lista de modelos o una dataclass. Es lo que hacen `MeasurementIn.parse_text`, `read_measurements` y `read_scale` en tu proyecto. Ejercicio **guiado**: descomentas cada paso de `validators_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-13-typing_estricto_mypy_y_pydantic/2-practicas/ejercicio-04-validadores-y-json/starter
uv run python validators_lab.py
uv run --with mypy==2.4.1 mypy --strict validators_lab.py
```

```
Ejercicio 04 · Validadores y JSON
Success: no issues found in 1 source file
```

Descomenta en orden: los pasos 4 y 5 usan los modelos de los pasos 2 y 3. Cada salida de abajo muestra solo las líneas nuevas del paso. Con todo descomentado, mypy sigue diciendo `Success`.

## Pasos

### 1. `field_validator` después del tipo

Descomenta el **PASO 1** y ejecuta:

```
Normalizada: label='Zona Norte' value=12.5
Rechazada: Value error, la etiqueta no lleva números
```

`@field_validator("label")` añade una regla al campo `label`. Por defecto se ejecuta **después** de validar el tipo (`mode="after"`), así que recibe un `str` seguro. Lo que devuelve es el valor que se guarda: aquí, sin espacios y con mayúsculas iniciales. Si lanza `ValueError`, Pydantic lo convierte en un error de validación con el prefijo `Value error, `. Va con `@classmethod` debajo porque se ejecuta antes de que exista la instancia.

### 2. `field_validator` antes del tipo

Descomenta el **PASO 2** y ejecuta:

```
'12,5': 12.5
'NA': None
8: 8.0
'doce': Input should be a valid number, unable to parse string as a number
```

Con `mode="before"`, el validador recibe el dato **tal como llega**, antes de comprobar el tipo: por eso se anota como `object`. Aquí cambia la coma por un punto y `"NA"` por `None`, y deja el resto como está. Después, Pydantic valida el tipo como siempre: `"12.5"` pasa a `12.5`, y `"doce"` falla con el error normal de un número.

Tu `MeasurementIn.parse_text` hace esto mismo con `parse_value`, la función de la semana 2.

### 3. `model_validator` compara campos

Descomenta el **PASO 3** y ejecuta:

```
Válidos: low=10.0 high=50.0
Imposibles: () Value error, low (50.0) debe ser menor que high (10.0)
```

Un `field_validator` ve un solo campo. Para comparar dos, `@model_validator(mode="after")` recibe el modelo ya validado (`self`) y lo devuelve: el tipo de vuelta es `Self`. El error no es de ningún campo, así que su `loc` es la tupla vacía `()`.

Tu `Scale` hace esta misma comprobación en su `__post_init__`. En el paso 5 verás que Pydantic la usa sin repetirla.

### 4. De modelo a JSON y vuelta

Descomenta el **PASO 4** y ejecuta:

```
model_dump: {'label': 'Sur', 'value': None}
Sin los None: {'label': 'Sur'}
model_dump_json: {"label":"Norte","value":12.5}
Y de vuelta: label='Norte' value=12.5
JSON roto: json_invalid · Invalid JSON: EOF while parsing an object at line 1 column 32
Esquema JSON: {"low": {"title": "Low", "type": "number"}, "high": {"title": "High", "type": "number"}}
```

- `model_dump()` da un `dict`, y `exclude_none=True` quita los campos con `None`.
- `model_dump_json()` da el texto JSON directamente, sin pasar por `json.dumps`.
- `model_validate_json(texto)` lee y valida en un solo paso. Un JSON roto también es un `ValidationError`, con el tipo `json_invalid`: un solo `except` cubre los dos fallos. Así lo hace `read_measurements`.
- `model_json_schema()` describe el modelo como un esquema JSON. FastAPI lo usa para documentar una API en la semana 20.

### 5. `TypeAdapter` para lo que no es un `BaseModel`

Descomenta el **PASO 5** y ejecuta:

```
Lista validada: [CommaReading(label='Norte', value=12.5), CommaReading(label='Sur', value=None)]
Falla la medida (1, 'value')
Una dataclass: Scale(unit='ppm', low=10.0, high=50.0)
Su __post_init__ también: Value error, umbrales imposibles
```

Un JSON con una lista no es un modelo, pero `TypeAdapter(list[CommaReading])` valida cualquier tipo: tiene `validate_python` y `validate_json`. El `loc` `(1, 'value')` es la posición en la lista y el campo, y `_invalid` lo convierte en `1.value` en el mensaje de tu proyecto.

`TypeAdapter(Scale)` valida una **dataclass** normal: comprueba y convierte sus campos (`"10"` pasa a `10.0`) y ejecuta su `__post_init__`. El `ValueError` sale como error de validación. Por eso tu proyecto no necesita un `ScaleIn`: la regla vive en el modelo y no se repite.

Crear un `TypeAdapter` cuesta tiempo, porque construye el validador; usarlo es rápido. En tu proyecto se crean una vez, al importar el módulo.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| La etiqueta sale `label=None` | El `field_validator` no tiene `return`: lo que devuelve es lo que se guarda |
| ``UserWarning: A custom validator is returning a value other than `self`.`` | El `model_validator(mode="after")` no termina con `return self` |
| `PydanticUserError: Decorators defined with incorrect fields` | El nombre que pasas a `@field_validator(...)` no es el de ningún campo: revisa cómo lo escribiste |
| `'12,5'` da `unable to parse string as a number` | Falta `mode="before"`: el validador se ejecuta después del tipo, y para entonces el texto ya ha fallado |
| `NameError: name 'CommaReading' is not defined` | Descomenta antes el paso 2 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Modelos de Pydantic](../ejercicio-03-modelos-pydantic/README.md) | **Ejercicio 04 · Validadores y JSON** | [Proyecto](../../3-proyecto/README.md) |
