# Ejercicio 03 — Salida estructurada

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-salida-estructurada.md)

## Objetivo

Que Claude responda con datos que tu programa puede leer **siempre**:

- pedir JSON en el prompt, y por qué no basta;
- un esquema JSON en `output_config`;
- el mismo esquema con Pydantic y `messages.parse`;
- extraer varios campos de una nota larga;
- lo que el esquema no garantiza;
- mirar `stop_reason` antes de leer.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-37-llms_por_api_prompting_salida_estructurada_y_tool_use/2-practicas/ejercicio-03-salida-estructurada/starter
uv run python main.py
```

```
Ejercicio 03 · Salida estructurada
```

Las respuestas salen de `respuestas.json` (de ejemplo, como en los ejercicios anteriores); con tu clave, `CLAUDE_REAL=1`. `NOTES` son cuatro notas del ejercicio 02, y `SYSTEM` es el prompt con contexto de su paso 3.

## Pasos

### 1. Pedir JSON en el prompt

Descomenta el **PASO 1** y ejecuta:

```
{'tipo': 'averia', 'urgente': True, 'resumen': 'Sensor de Norte sin lecturas; limpiarlo no sirvió'}
no es JSON (Expecting value): '```json\n{"tipo": "limpieza", "urgente": false, "resumen": "Filtro sucio cambiado en Centro"}\n```'
{'tipo': 'calibracion', 'urgente': False, 'resumen': 'Deriva corregida en el cero de Centro'}
{'tipo': 'averia', 'urgente': True, 'resumen': 'Placa quemada en Sur, repuesto pedido'}
```

Tres de cuatro se leen. La segunda trae el JSON dentro de un bloque de código de Markdown, y `json.loads` falla. Pedirlo en el prompt funciona casi siempre, y "casi siempre" en un programa que lee mil notas son unas cuantas excepciones. También podría faltar un campo, o llegar `"urgente": "sí"`.

### 2. Un esquema JSON en `output_config`

Descomenta el **PASO 2** y ejecuta:

```
{'tipo': 'averia', 'urgente': True, 'resumen': 'Sensor de Norte sin lecturas; limpiarlo no sirvió'}
{'tipo': 'limpieza', 'urgente': False, 'resumen': 'Filtro sucio cambiado en Centro'}
{'tipo': 'calibracion', 'urgente': False, 'resumen': 'Deriva corregida en el cero de Centro'}
{'tipo': 'averia', 'urgente': True, 'resumen': 'Placa quemada en Sur, repuesto pedido'}
```

`output_config={"format": {"type": "json_schema", "schema": SCHEMA}}` **obliga** a que la respuesta sea un JSON con esa forma: la API solo deja escribir tokens que cumplan el esquema (*constrained decoding*). Fíjate en el esquema:

- `enum` en `tipo`: solo uno de los tres valores;
- `required` con los tres campos, y `additionalProperties: false`: ni falta ni sobra ninguno;
- `"type": "boolean"` en `urgente`: `true` o `false`, nunca "sí".

Ya no hace falta pedir el JSON en el prompt.

### 3. El esquema con Pydantic

Descomenta el **PASO 3** y ejecuta:

```
Reading(tipo='averia', urgente=True, resumen='Placa quemada en Sur, repuesto pedido')
AVERIA · urgente: sí · Placa quemada en Sur, repuesto pedido
```

El mismo esquema, escrito como una clase de Pydantic (semana 13): `Literal[...]` es el `enum`. `client.messages.parse(..., output_format=Reading)` genera el esquema, lo envía y valida la respuesta: `response.parsed_output` es un objeto `Reading`, con sus tipos. Tu editor y mypy saben que `reading.urgente` es un `bool`.

### 4. Extraer más de una nota larga

Descomenta el **PASO 4** y ejecuta:

```
{'tipo': 'averia', 'equipo': 'analizador de ozono', 'acciones': ['reiniciar el equipo', 'revisar el cableado'], 'urgencia': 'alta', 'repuesto': True}
{'tipo': 'limpieza', 'equipo': None, 'acciones': ['revisión de rutina'], 'urgencia': 'baja', 'repuesto': False}
```

`Maintenance` tiene una lista (`acciones`), un campo que puede faltar (`equipo: str | None`) y descripciones en `Field(description=...)`: las descripciones van en el esquema y Claude las lee, son parte del prompt.

- De la nota larga saca el equipo, dos acciones, urgencia alta y que hace falta un repuesto: lo que antes era texto ahora se puede filtrar y contar.
- La nota corta no dice qué equipo: `None`. Bien.
- Pero dice "todo normal" y el esquema **obliga** a elegir un tipo: `limpieza`, un tipo que la nota no dice. Un esquema garantiza la forma, no la verdad. Si una nota puede no tener tipo, el esquema necesita esa opción (como `desconocido` en el ejercicio 02).

### 5. Lo que el esquema no garantiza

Descomenta el **PASO 5** y ejecuta:

```
{'type': 'string', 'title': 'Resumen', 'description': '{maxLength: 40}'}
ValidationError en ('resumen',): String should have at most 40 characters
```

La API no admite todas las reglas de JSON Schema: `maxLength`, `minimum` o `pattern`, por ejemplo, no. `anthropic.transform_schema` (lo usa `parse` por dentro) las pasa a la descripción: Claude las lee como una petición, no como una obligación. Aquí el resumen tiene 76 caracteres, y la validación de Pydantic, en tu lado, lo rechaza con un `ValidationError`. Las reglas que importan se comprueban en tu código.

### 6. Mirar `stop_reason` antes de leer

Descomenta el **PASO 6** y ejecuta:

```
stop_reason: max_tokens
respuesta cortada, no se lee: '{"tipo": "averia", "equipo": "analizador de ozono", "acciones": ["reiniciar el'
```

Con `max_tokens=30`, el JSON se corta a la mitad. El esquema no lo evita: obliga a la forma mientras escribe, pero no puede escribir más allá del límite. Por eso se mira `stop_reason` **antes** de leer, y aquí se usa `messages.create` con `transform_schema` en lugar de `parse`: con una respuesta cortada, `parse` lanza un error y pierdes la respuesta y sus tokens. Es lo que hace `llm.read` en el proyecto.

Para terminar, escribe al final de `main.py` una clase de Pydantic para las notas de **tu** dominio: qué campos sacarías, cuáles pueden faltar, y qué valores admite cada uno.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `LookupError: respuestas.json no tiene esta petición` | Cambiaste un esquema, una nota o un prompt: vuelve al código del paso, o pruébalo con tu clave y `CLAUDE_REAL=1` |
| `BadRequestError: 400 ... output_config.format.schema` | El esquema usa algo que la API no admite: pásalo por `anthropic.transform_schema` |
| `ValidationError` en el paso 3 o 4 con tu clave | La respuesta no cumple una regla de Pydantic que la API no puede imponer: mírala con `response.content[0].text` |
| `AttributeError: 'NoneType' object has no attribute 'tipo'` | `parsed_output` es `None` cuando la respuesta no terminó: mira `response.stop_reason` |
| `NameError: name 'LONG' is not defined` | Descomenta los pasos en orden: el 5 y el 6 usan la nota del 4 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Prompting](../ejercicio-02-prompting/README.md) | **Ejercicio 03 · Salida estructurada** | [Ejercicio 04 · Tool use](../ejercicio-04-tool-use/README.md) |
