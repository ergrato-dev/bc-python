# 02 · Rutas, parámetros y modelos

⏱️ 50 min

## 🎯 Objetivos

- Saber de dónde lee FastAPI cada parámetro: la ruta, la consulta o el cuerpo.
- Poner reglas a los parámetros con `Annotated`, `Path`, `Query` y `Field`.
- Recibir un cuerpo JSON con un modelo de Pydantic, y reutilizar los modelos de tu proyecto.
- Leer un 422: qué dice cada entrada de `detail`.
- Controlar lo que sale con el tipo de retorno, los códigos y las cabeceras.
- Hacer que las reglas de la API coincidan con las de la base, para no convertir un 422 en un 500.

---

## 1. Tres sitios de donde llegan los datos

```python
@app.post("/loads/{load_id}/notes")
def add_note(load_id: int, body: NoteIn, urgent: bool = False) -> NoteOut: ...
```

FastAPI mira cada parámetro de la función y decide de dónde sale, sin que se lo digas:

| El parámetro... | Sale de... | Ejemplo |
|---|---|---|
| tiene su nombre en la ruta (`{load_id}`) | la **ruta** | `/loads/7/notes` |
| es un modelo de Pydantic | el **cuerpo** JSON | `{"text": "revisar"}` |
| es un tipo sencillo (`int`, `str`, `bool`, `float`, `None`) | la **consulta** | `?urgent=true` |
| es de tipo `Request`, `Response` o una dependencia | FastAPI te lo da | teoría 03 |

Todo lo que llega en la ruta y en la consulta es **texto**. La anotación decide a qué se convierte: `"7"` pasa a ser `7`, y `"true"`, `"1"` o `"yes"` pasan a ser `True`. Si la conversión falla, la función no se llama.

Un parámetro de la consulta con valor por defecto es opcional; sin valor por defecto, es obligatorio. Con `int | None = None` puede faltar, y tu código distingue "no lo pidieron" de "pidieron el 0". Es lo que hace `?load=N` en `/stats`.

---

## 2. Reglas para los parámetros

Como en la semana 13, `Annotated` añade reglas al tipo:

```python
from typing import Annotated

from fastapi import Path, Query


@app.get("/loads/{load_id}/measurements")
def get_measurements(
    load_id: Annotated[int, Path(ge=1)],
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
) -> list[Measurement]: ...
```

`Path` y `Query` son a los parámetros lo que `Field` es a los campos de un modelo: `ge`, `le`, `min_length`, `max_length`, `pattern`. Y sus reglas también salen en `/docs`. En tu proyecto no hacen falta: un número de carga negativo no rompe nada, simplemente no existe y da 404.

---

## 3. El cuerpo: un modelo de Pydantic

```python
class LoadIn(BaseModel):
    """El cuerpo de POST /loads."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source: Annotated[str, Field(min_length=1, max_length=500)]
    measurements: Annotated[list[ReadingIn], Field(min_length=1)]
```

Un parámetro con este tipo es el cuerpo. FastAPI lee el JSON, lo valida con el modelo y te da un `LoadIn` construido; si no vale, responde 422. Dentro de la función ya no compruebas nada: si se ejecuta, el cuerpo cumple el contrato.

Tu proyecto **ya tiene** el modelo de una medida en JSON: `MeasurementIn`, de la semana 13, con sus reglas (etiqueta no vacía, `"12,5"` y `"NA"` como textos, `true` rechazado, claves de más prohibidas) y su `to_measurement()`. La API lo **reutiliza**: las medidas que llegan por HTTP siguen las mismas reglas que las de un archivo JSON. Solo le falta una, que en un archivo no importaba y en la base sí (sección 8):

```python
class ReadingIn(MeasurementIn):
    """Una medida en el cuerpo de POST /loads: como en los JSON, con el límite de la tabla."""

    label: Annotated[str, Field(min_length=1, max_length=100)]
```

Una subclase de un modelo de Pydantic hereda los campos, la configuración y los validadores; redefinir `label` solo cambia sus reglas. Escribir el modelo de nuevo copiaría reglas que algún día dejarían de coincidir.

---

## 4. El 422 por dentro

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "measurements", 1, "label"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": {"min_length": 1}
    }
  ]
}
```

`detail` es la lista de **todos** los problemas, no solo el primero, con:

- **`loc`**: dónde. Empieza por `path`, `query` o `body`, y sigue el camino dentro del JSON: el campo `label` de la segunda medida (la posición 1);
- **`msg`**: qué pasa, para una persona;
- **`type`**: lo mismo, para un programa;
- **`input`**: lo que llegó.

Es más útil que cualquier mensaje que escribieras tú, y es igual en todas las rutas. No lo cambies: quien llama a tu API sabrá leerlo. Y fíjate en que `input` **devuelve** lo que llegó: nunca valides con un modelo un secreto que no quieras ver en una respuesta.

---

## 5. Lo que sale: el tipo de retorno

```python
@app.get("/loads")
def get_loads(session: SessionDep) -> list[LoadInfo]:
    return list_loads(session)
```

El **tipo de retorno** es el contrato de la respuesta. FastAPI lo usa para tres cosas:

- **convertir** el resultado en JSON: modelos de Pydantic, *dataclasses* (`LoadInfo`, `LabelStats`, `Measurement`), listas y diccionarios; `None` sale como `null` y un `datetime` como texto ISO 8601 (`"2026-11-08T10:02:00Z"`);
- **validar** lo que sale: si devuelves algo que no cumple el tipo, es un error tuyo y responde 500;
- **filtrar**: si el tipo no tiene un campo, ese campo no sale, aunque el objeto lo tenga. Así un dato interno no se escapa porque alguien lo añadió a lo que guardas (ejercicio 02, paso 4).

Tu proyecto devuelve las *dataclasses* de `core` tal cual: ya son valores inmutables con los campos justos (semana 19, teoría 03, sección 9). No hacen falta modelos de salida nuevos que digan lo mismo.

Si la función devuelve algo distinto de lo que anuncias (un objeto del ORM y quieres un modelo), FastAPI tiene `response_model=` en el decorador. Con anotaciones exactas casi nunca hace falta, y mypy comprueba que devuelves lo que dices.

---

## 6. Códigos y cabeceras

```python
@router.post("/loads", status_code=status.HTTP_201_CREATED)
def post_load(body: LoadIn, session: SessionDep, response: Response) -> LoadInfo:
    ...
    response.headers["Location"] = f"/loads/{load.id}"
    return info


@router.delete("/loads/{load_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_load(load_id: int, session: SessionDep) -> None: ...
```

- `status_code=` en el decorador cambia el código de éxito. `status.HTTP_201_CREATED` es `201` con nombre: se lee mejor y no se escribe mal.
- Un parámetro de tipo `Response` es la respuesta que FastAPI enviará: le pones cabeceras, y tu valor de retorno sigue siendo el cuerpo.
- **`Location`** dice dónde está lo que acabas de crear. Quien llama lo sigue sin construir la URL.
- Un **204** no tiene cuerpo: la función devuelve `None` y se anota `-> None`. FastAPI se niega a arrancar si anuncias otra cosa.

---

## 7. Errores con `HTTPException`

```python
series = load_series(session, load_id)
if series is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"no existe la carga {load_id}")
```

`HTTPException` responde `{"detail": "..."}` con su código. Es una excepción: corta la función, y la puedes lanzar desde una función auxiliar. Tres reglas:

- **404** para lo que no existe; **422** lo pone FastAPI para lo que no vale; tú casi nunca lo escribes;
- el mensaje es para quien llama: di qué pasó con **sus** datos (`no existe la carga 999`), no cómo está hecho tu programa;
- **nunca** pongas en `detail` el texto de una excepción de la base de datos (`str(problem)`): puede llevar el usuario, el servidor o la consulta. Para esos errores, un manejador propio (teoría 03, sección 6).

---

## 8. El contrato de la API y el de la base

`readings.label` es `String(100)` en PostgreSQL. Si la API aceptara etiquetas de cualquier longitud, una de 101 caracteres pasaría la validación, llegaría a la base y PostgreSQL la rechazaría con un `DataError`. Nadie lo atrapa: **500**, con la traza en el registro del servidor. Quien llama no sabe qué hizo mal, y tú recibes una alarma por un error que no es tuyo.

La regla: **lo que la base rechazaría, la API lo rechaza antes**, con 422 y un `loc` que dice dónde. Por eso `ReadingIn` limita `label` a 100 y `LoadIn` limita `source` a 500, los mismos números que los modelos de `database.py`. Un test de la semana (`long label`) lo comprueba, y otro, que 100 caracteres sí valen.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| Un parámetro que querías en la consulta llega como cuerpo | Su tipo es un modelo | Los tipos sencillos van a la consulta; los modelos, al cuerpo |
| `422` con `loc: ["body"]` y `Field required` | Llegó sin cuerpo, o no era JSON | `json=` en el cliente, y `Content-Type: application/json` |
| Una clave mal escrita (`"sourse"`) se ignora sin aviso | El modelo no tiene `extra="forbid"` | Añádelo: quien llama se entera de su error |
| Sale un campo que no debía | La función devuelve un diccionario y el tipo de retorno es `dict` | Anota el tipo exacto de la respuesta |
| `500` con `DataError: value too long` | La API acepta más de lo que cabe en la columna | El mismo `max_length` en el modelo de entrada |
| `AssertionError: Status code 204 must not have a response body` | Una ruta 204 anuncia otro tipo de retorno | `-> None` |
| `detail` con el texto de una excepción de SQLAlchemy | `HTTPException(500, str(problem))` | Un mensaje fijo; el detalle, en el registro |

---

## ✅ Qué debes saber al terminar

- [ ] Cómo decide FastAPI si un parámetro viene de la ruta, de la consulta o del cuerpo.
- [ ] Cómo poner reglas con `Path`, `Query` y `Field`, y dónde se ven.
- [ ] Por qué `ReadingIn` hereda de `MeasurementIn`, y qué le añade.
- [ ] Leer un 422: `loc`, `msg`, `type` e `input`.
- [ ] Las tres cosas que hace el tipo de retorno: convertir, validar y filtrar.
- [ ] Cuándo 201 con `Location`, cuándo 204 sin cuerpo y cuándo 404.
- [ ] Por qué las reglas de la API deben coincidir con las de la base.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · De la CLI a la web: HTTP, ASGI y FastAPI](01-de-la-cli-a-la-web-http-asgi-y-fastapi.md) | **02 · Rutas, parámetros y modelos** | [03 · Dependencias, sesiones y ciclo de vida](03-dependencias-sesiones-y-ciclo-de-vida.md) |
