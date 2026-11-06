# Rúbrica de Evaluación — Semana 13: Typing estricto con mypy y Pydantic v2

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 12 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | `def mean(values): return sum(values) / len(values)` y la llamada `mean(["12,5", "8"])`. ¿Qué dice mypy sin `strict`? ¿Y con `strict`? ¿Por qué existe el modo sin `strict`? | 10 |
| 2 | ¿En qué se diferencian `Any` y `object`? ¿Cuál usarías para el resultado de `json.loads` y por qué? | 10 |
| 3 | `value = cast(float, json.loads('"12,5"'))`. ¿Qué vale `value` y de qué tipo es en ejecución? ¿Qué diferencia hay entre `cast` y validar con Pydantic? | 10 |
| 4 | `summary_data` devuelve un `Summary` (un `TypedDict`) y `write_json` pedía un `dict[str, object]`. ¿Por qué mypy rechaza la llamada si un `Summary` es un `dict` en ejecución? ¿Cómo lo arreglaste? | 10 |
| 5 | ¿Qué ganas al escribir `first` como genérica, con `[T]`, `Sequence[T]` y `-> T`, frente a `Sequence[object]` y `-> object`? ¿Y frente a `Any`? | 10 |
| 6 | ¿Qué hace Pydantic que mypy no puede hacer? Da un ejemplo con un archivo JSON de tu dominio. | 10 |
| 7 | En el modo normal, ¿qué da `MeasurementIn.model_validate({"label": "Norte", "value": True})` sin `Field(strict=True)`? ¿Por qué tu proyecto no pone `strict=True` en todo el modelo? | 10 |
| 8 | ¿Por qué `parse_text` es `mode="before"`? ¿Qué pasaría con `"12,5"` si fuera `mode="after"`? | 10 |
| 9 | Tu proyecto tiene un `MeasurementIn`, pero no un `ScaleIn`. ¿Por qué? ¿Qué hace `TypeAdapter(Scale)` con el `__post_init__` de `Scale`? | 10 |
| 10 | ¿Por qué `read_measurements` lanza `DataFileError` y no deja salir el `ValidationError`? ¿Qué guarda `raise ... from error` y cómo lo compruebas en un test? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Sin `strict`: `Success`, porque mypy no revisa una función sin anotar ni sus llamadas, y trata todo como `Any`. Con `strict`: `Function is missing a type annotation [no-untyped-def]` en el `def` y `Call to untyped function "mean" in typed context [no-untyped-call]` en la llamada. El error real (`TypeError: unsupported operand type(s) for +: 'int' and 'str'`) solo llega al ejecutar. El modo sin `strict` permite añadir mypy poco a poco a un proyecto que nunca se anotó.
2. Los dos aceptan cualquier valor. `Any` apaga la comprobación: cualquier operación vale y lo que sale también es `Any`, que se contagia. `object` no deja hacer nada que no tenga todo objeto, y obliga a comprobar el tipo con `isinstance` antes de usarlo. Para `json.loads`, `object` (o mejor, Pydantic), porque te obliga a mirar qué llegó. Con `Any`, una función que lo devuelve como `float` puede devolver un texto sin que mypy lo vea (`Returning Any from function declared to return "float"` solo lo detecta `strict`).
3. `value` es el texto `'12,5'`, un `str`. `cast` no convierte ni comprueba: devuelve el mismo objeto y solo cambia lo que mypy cree. `value + 1` fallará al ejecutar. Validar con Pydantic comprueba el dato al ejecutar, lo convierte si puede (`"12.5"` → `12.5`) y si no, lanza `ValidationError`.
4. mypy no mira lo que hace `write_json`, sino lo que **podría** hacer con un `dict[str, object]`: añadir o cambiar cualquier clave, y eso rompería un `Summary`. Por eso un `TypedDict` no es compatible con `dict[str, object]`. Como `write_json` solo lee, su parámetro pasa a ser `Mapping[str, object]`, que es de solo lectura y acepta un `Summary` y cualquier `dict`.
5. Con `[T]`, el tipo que sale es el que entra: `first(["Norte"])` es `str` para mypy, y `.upper()` se comprueba. Con `object` se pierde: habría que estrechar el resultado antes de usarlo. Con `Any` se pierde la comprobación entera: `first(["Norte"]) + 1` pasaría.
6. mypy revisa el código antes de ejecutarlo; no puede ver un archivo que llega mañana. Pydantic comprueba los datos al ejecutar, contra las anotaciones, y convierte o rechaza. Ejemplo: un `medidas.json` con `{"label": "Norte", "value": "doce"}`. mypy no dice nada; `read_measurements` lanza `datos no válidos en medidas.json: 0.value: Value error, could not convert string to float: 'doce'`.
7. `value=1.0`: en modo normal, Pydantic convierte un booleano en número, y un `true` enviado por error se colaría como una medida. `strict` va solo en `value` porque la regla es de ese campo: se pone donde se aplica, y el resto del modelo conserva las conversiones normales. Los textos `"12,5"` no se ven afectados, porque `parse_text` los convierte antes de la validación del tipo, y un entero sigue valiendo como `float` también en estricto.
8. Porque tiene que convertir el texto **antes** de que Pydantic lo valide como número. Con `mode="after"`, la validación del tipo fallaría primero con `Input should be a valid number, unable to parse string as a number` y el validador nunca se ejecutaría (o, con `strict`, cualquier texto fallaría).
9. Las reglas de `MeasurementIn` son del **formato** JSON: coma decimal, `"NA"`, espacios, claves de más, `true`. No son del dominio, y `Measurement` no tiene por qué saberlas. La regla de `Scale` (`low < high`) sí es del dominio, y ya vive en su `__post_init__` desde la semana 9. `TypeAdapter(Scale)` valida y convierte sus campos y ejecuta su `__post_init__`; el `ValueError` sale como un error de validación. Repetirla en un `ScaleIn` sería tener dos reglas que pueden separarse.
10. Para quien llama, un archivo que no existe, un JSON roto o una medida mal formada son lo mismo: el archivo no sirve. Un solo tipo de error, `DataFileError`, como desde la semana 7, deja que `main` lo trate en un solo `except` y no sabe de Pydantic. `raise ... from error` guarda el `ValidationError` original en `__cause__`: la traza muestra los dos. En un test: `with pytest.raises(DataFileError) as caught: ...` y `assert isinstance(caught.value.__cause__, ValidationError)`.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-13` muestra un commit por paso (dependencia, esqueleto, `Summary`, `strict`, campos, `parse_text`, plugin, `true`, lectores, versión, tests), sin cambiar los tests del bootcamp salvo el de `test_sources.py` del paso 7 | 8 |
| Reutiliza sin reescribir | `parse_text` usa `parse_value`; los lectores usan `read_lines`; `read_scale` usa `TypeAdapter(Scale)` sin repetir la regla; `git diff main -- src/observatorio` solo muestra `storage.py` y `core/__init__.py` ampliados y `schemas.py` nuevo; `__main__.py` y `model.py` sin cambios | 8 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff check`, `ruff format --check`, `mypy` y `--version`, en su máquina y en Docker | 6 |
| Rompe y explica | Quita `strict=True` de `value` y explica qué test falla; cambia `Mapping` por `dict` en `write_json` y explica el error de mypy; quita el plugin y explica el `unused-ignore` | 10 |
| Explica sus decisiones | Explica por qué el modelo no usa Pydantic, por qué no hay `ScaleIn` y por qué los `TypeAdapter` se crean a nivel de módulo | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 12

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Tipos estrictos | `strict = true` y el plugin de Pydantic en `[tool.mypy]`; `Summary` como `TypedDict` y `write_json` con `Mapping`; `mypy` sin avisos | 15 |
| Frontera con Pydantic | `MeasurementIn` con `extra="forbid"`, `frozen`, etiqueta no vacía, `parse_text` y `value` estricto; `read_measurements` y `read_scale` con `TypeAdapter` y errores como `DataFileError`; pasan sus tests de `test_schemas.py` y los de las semanas anteriores siguen en verde | 15 |
| API, dependencia y versión | Los cuatro nombres en `observatorio.core.__all__`; `pydantic==2.14.2` en las dependencias y en `uv.lock`; versión `0.13.0`; pasan `test_package.py` y `test_main.py`; el informe es idéntico al de la semana 12 | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_schemas.py` con datos del dominio, que importan solo de `observatorio.core` (y `pydantic` o `pytest`) (paso 15) | 20 |
| Calidad | `ruff check`, `ruff format --check` y `mypy` sin avisos; `docker compose run --build --rm app` en verde | 10 |
| Git y README | Rama `week-13` en `python-<nombre>-<apellido>`, README con `schemas.py` en el árbol del paquete | 10 |
| Pull request | Descripción con tests, `mypy`, `ruff`, los errores del paso 7 y las preguntas del paso 16 | 20 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 14 (próximamente) |
