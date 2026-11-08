# Ejercicio 02 — Cuerpos y respuestas con Pydantic

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-rutas-parametros-y-modelos.md)

## Objetivo

Recibir datos en el **cuerpo** de un `POST` y decidir qué sale en la respuesta, con los modelos de Pydantic de la semana 13:

- un **modelo de entrada** como parámetro: el cuerpo JSON, validado;
- el **422** y su lista de problemas, para cada cosa que puede llegar mal;
- **reglas** en el modelo: longitudes, rangos, espacios y claves de más;
- un **modelo de respuesta** que filtra lo que no debe salir;
- los **códigos** 201 y 204, y la cabecera `Location`;
- fechas y *dataclasses* como respuesta.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-20-fastapi_lo_justo_para_servir_tu_proyecto/2-practicas/ejercicio-02-cuerpos-y-respuestas-con-pydantic/starter
uv run python main.py
```

```
Ejercicio 02 · Cuerpos y respuestas con Pydantic
```

## Pasos

### 1. Un cuerpo con un modelo

Descomenta el **PASO 1** y ejecuta:

```
--- Paso 1: POST /readings ---
  la función recibe: ReadingIn(label='Norte', value=12.5)
estado: 201 · cuerpo: {'id': 1, 'label': 'Norte', 'value': 12.5, 'author': 'ana@example.com'}
  la función recibe: ReadingIn(label='Sur', value=30.0)
estado: 201 · cuerpo: {'id': 2, 'label': 'Sur', 'value': 30.0, 'author': 'ana@example.com'}
```

Un parámetro cuyo tipo es un modelo de Pydantic es el **cuerpo** de la petición. FastAPI lee el JSON, lo valida con `ReadingIn` y te da un objeto ya construido: la función no ve el JSON. `"30"` llega como `30.0`: en modo normal, Pydantic convierte un texto que es un número.

`status_code=201` es el código de "creado". Y fíjate en el cuerpo: **sale el correo** del autor, porque la función devuelve el diccionario entero. Lo arreglas en el paso 4.

### 2. Lo que no es válido: 422

Descomenta el **PASO 2** y ejecuta:

```
--- Paso 2: cuerpos no válidos ---
{'label': 'Norte'}                     -> 422
    ['body', 'value']: Field required
{'label': 'Norte', 'value': 'mucho'}   -> 422
    ['body', 'value']: Input should be a valid number, unable to parse string as a number
{'label': ['Norte'], 'value': 1}       -> 422
    ['body', 'label']: Input should be a valid string
'Norte;12,5'                           -> 422
    ['body']: Input should be a valid dictionary or object to extract fields from
guardadas: 2 (ninguna de las no válidas)
```

Si el cuerpo no cumple el modelo, la función **no se ejecuta**: FastAPI responde 422 con un problema por campo. `loc` empieza por `body` y sigue por el campo. `value: float | None` no tiene valor por defecto: puede ser `null`, pero no puede faltar. Por eso `SAVED` sigue con 2.

### 3. Reglas en el modelo

Descomenta el **PASO 3** y ejecuta:

```
--- Paso 3: reglas ---
{'label': '  Norte  ', 'value': 12.5}          -> 201 {'label': 'Norte', 'value': 12.5}
{'label': '', 'value': 12.5}                   -> 422 String should have at least 1 character
{'label': 'Norte', 'value': 200}               -> 422 Input should be less than or equal to 150
{'label': 'Norte', 'value': 1, 'unit': '°C'}   -> 422 Extra inputs are not permitted
```

Con `Field` el tipo dice algo más: longitud mínima y máxima, valores entre `-50` y `150`. `str_strip_whitespace` quita los espacios antes de validar, así que `"  Norte  "` llega limpio. Y `extra="forbid"` rechaza `unit`: sin él, Pydantic **ignoraría** la clave en silencio, y quien llama creería que se guardó. Son las reglas de `MeasurementIn` en tu proyecto (semana 13).

La ruta devuelve el modelo mismo: un modelo de Pydantic también vale como respuesta.

### 4. Lo que sale: el modelo de respuesta

Descomenta el **PASO 4** y ejecuta:

```
--- Paso 4: GET /readings ---
guardado: {'id': 1, 'label': 'Norte', 'value': 12.5, 'author': 'ana@example.com'}
respuesta: [{'id': 1, 'label': 'Norte', 'value': 12.5}, {'id': 2, 'label': 'Sur', 'value': 30.0}]
limit=0 -> 422
```

El **tipo de retorno** de la función es el contrato de la respuesta: `list[ReadingOut]`. Lo que guardas lleva `author`, pero `ReadingOut` no lo tiene, y no sale. Así no se escapa un dato porque alguien añadió un campo a lo guardado. Y `/openapi.json` describe la respuesta con ese modelo.

`Query(ge=1, le=100)` pone reglas a un parámetro de la consulta, como `Field` a un campo.

### 5. Códigos y cabeceras

Descomenta el **PASO 5** y ejecuta:

```
--- Paso 5: códigos y cabeceras ---
POST /places      -> 201 /readings/3
DELETE /readings/1 -> 204 b''
DELETE /readings/1 -> 404 {'detail': 'no existe la medida 1'}
```

Un parámetro de tipo `Response` te da la respuesta antes de enviarla: le pones la cabecera **`Location`**, que dice dónde está lo que acabas de crear. **204** es "hecho, y no hay nada que contar": la respuesta no lleva cuerpo, ni siquiera `null`. La segunda vez que borras, la medida ya no existe: 404.

### 6. Fechas y *dataclasses*

Descomenta el **PASO 6** y ejecuta:

```
--- Paso 6: GET /summary ---
{"readings":2,"mean":30.0,"at":"2026-11-08T10:30:00Z"}
```

JSON no tiene fechas: FastAPI escribe el `datetime` como texto **ISO 8601**, con la zona horaria (`Z` es UTC). Del otro lado, `datetime.fromisoformat` lo vuelve a convertir. Y una *dataclass* vale como respuesta igual que un modelo: tu proyecto devolverá así `LoadInfo` y `LabelStats`, sin escribir modelos nuevos.

`readings` es 2 y no 3: el paso 5 añadió una y borró otra. Y `mean` es 30.0 porque `Este` no tiene valor.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `422` con `loc: ['body']` | El cuerpo no es un objeto JSON: usa `json={...}`, no `content=` ni `data=` |
| `422` con `Field required` en un campo que puede ser `null` | Sin valor por defecto, el campo tiene que estar, aunque sea `null` |
| El correo sigue saliendo en el paso 4 | La función devuelve diccionarios: el tipo de retorno tiene que ser `list[ReadingOut]` |
| `AssertionError: Status code 204 must not have a response body` al arrancar | La ruta de un 204 anuncia un tipo de retorno: tiene que ser `-> None` |
| `KeyError: 'location'` | Falta el parámetro `response: Response`, o la línea que pone la cabecera |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Tu primera API](../ejercicio-01-primera-api/README.md) | **Ejercicio 02 · Cuerpos y respuestas con Pydantic** | [Ejercicio 03 · Dependencias y ciclo de vida](../ejercicio-03-dependencias-y-ciclo-de-vida/README.md) |
