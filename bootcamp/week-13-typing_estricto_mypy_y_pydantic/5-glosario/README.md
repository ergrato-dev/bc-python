# Glosario — Semana 13

| Término | Definición |
|---|---|
| **`Any`** | Tipo que apaga la comprobación de mypy: todo lo que hagas con él vale, y lo que sale de él también es `Any`. Es lo que devuelve `json.loads` |
| **`assert_never`** | Función de `typing` que solo acepta el tipo `Never`. En el `case _` de un `match`, hace que mypy avise si falta algún caso |
| **`BaseModel`** | Clase base de los modelos de Pydantic: cada campo anotado se valida al crear el objeto |
| **`cast`** | Función de `typing` que cambia lo que mypy cree de un valor sin tocarlo. No convierte ni comprueba nada |
| **`ConfigDict`** | Configuración de un modelo de Pydantic: `extra="forbid"`, `frozen=True`, `strict=True`, `str_strip_whitespace=True`... |
| **`Field`** | Función de Pydantic que añade límites y opciones a un campo: `Field(min_length=1)`, `Field(ge=0)`, `Field(strict=True)` |
| **`field_validator`** | Decorador de Pydantic para una regla propia de un campo. Con `mode="before"` recibe el dato crudo; con `mode="after"`, ya validado |
| **`Final`** | Anotación que marca una constante: mypy avisa si se vuelve a asignar |
| **Frontera** | El punto por el que los datos de fuera (archivos, APIs, terminal) entran al programa. Se validan allí, una vez |
| **Genérico** | Función o clase con una variable de tipo, como `first[T]`, que recibe un `Sequence[T]` y devuelve un `T`: lo que entra decide lo que sale |
| **Invariante** | Un tipo como `list[float]` que solo acepta exactamente ese tipo, no `list[int]` ni `list[float \| None]`, porque se puede cambiar |
| **Lax (modo normal)** | Modo por defecto de Pydantic: convierte lo que tiene una conversión clara, como `"8.0"` → `8.0` o `true` → `1.0` |
| **`Literal`** | Tipo limitado a unos valores concretos: `Literal["bajo", "medio", "alto"]` |
| **`Mapping` / `Sequence`** | Tipos de solo lectura de `collections.abc`. Se piden en lugar de `dict` y `list` cuando una función no cambia lo que recibe |
| **`model_dump` / `model_dump_json`** | Pasan un modelo de Pydantic a `dict` o a texto JSON |
| **`model_validate` / `model_validate_json`** | Crean un modelo validado desde un `dict` o desde un texto JSON. Son la puerta para los datos de fuera |
| **`model_validator`** | Decorador de Pydantic para reglas que comparan campos. Con `mode="after"` recibe el modelo (`self`) y lo devuelve |
| **Narrowing (estrechar)** | Lo que hace mypy después de `if x is None`, `isinstance` o un `case`: debajo, sabe un tipo más concreto |
| **`NewType`** | Crea un tipo distinto para mypy que en ejecución es el original: `Celsius = NewType("Celsius", float)` |
| ***Parse, don't validate*** | Convertir los datos en la frontera en un tipo que ya no puede estar mal, en vez de comprobarlos en cada función |
| **Plugin de mypy** | Módulo que enseña a mypy cómo funciona una biblioteca. `pydantic.mypy` le explica los modelos de Pydantic |
| **`reveal_type`** | Pregunta el tipo de una expresión: mypy lo escribe como una nota y Python lo escribe en stderr al ejecutar |
| **Strict (mypy)** | `strict = true`: activa todas las comprobaciones opcionales de mypy, como exigir anotaciones o rechazar los `Any` que se devuelven |
| **Strict (Pydantic)** | Modo sin conversiones: el dato debe ser ya del tipo del campo. Solo se permite de entero a `float` |
| **`type` (alias)** | `type Record = tuple[str, float \| None]`: otro nombre para un tipo, que vale donde vale el original |
| **`# type: ignore[código]`** | Comentario que tapa un error de mypy en una línea. Con código, solo ese error; con `strict`, mypy avisa si sobra |
| **`TypeAdapter`** | Validador de Pydantic para cualquier tipo que no sea un `BaseModel`: `list[MeasurementIn]`, una dataclass, un `int` |
| **`TypedDict`** | Describe un `dict` con claves fijas y el tipo de cada una. En ejecución es un `dict` normal |
| **`TypeIs`** | Tipo de vuelta de una función que comprueba un tipo: si devuelve `True`, mypy estrecha el argumento |
| **`ValidationError`** | Excepción de Pydantic con todos los fallos de una validación; `errors()` da `loc`, `type` y `msg` de cada uno |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
