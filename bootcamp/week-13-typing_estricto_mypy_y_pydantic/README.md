# Semana 13 — Typing estricto con mypy y Pydantic v2

> Llevas doce semanas anotando tipos y ejecutando mypy, pero mypy aún deja pasar funciones sin anotar y los `Any` que salen de `json.loads`. Y nada comprueba lo que trae un archivo cuando el programa ya está en marcha. Esta semana cierras las dos puertas. Con `mypy --strict`, mypy revisa cada línea de tu código antes de ejecutarlo. Con **Pydantic**, los datos que llegan de fuera se validan y se convierten al entrar, contra las mismas anotaciones. El proyecto activa `strict`, da un tipo exacto al resumen JSON y abre una frontera que convierte un JSON en tus `Series` y `Scale` de siempre.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Activar** `mypy --strict` en un proyecto y **corregir** lo que encuentra: funciones sin anotar, `Any` que se cuela, reexportaciones implícitas
- **Distinguir** `Any` de `object`, **estrechar** tipos con `is None`, `isinstance` y `TypeIs`, y **explicar** por qué `cast` no es una validación
- **Usar** `TypedDict`, `Mapping` y `Sequence`, genéricos con `[T]`, `NewType`, `Literal` y `assert_never`
- **Crear** modelos de Pydantic con `Field` y `ConfigDict`, y **leer** un `ValidationError`
- **Escribir** validadores con `field_validator` y `model_validator`, y **validar** JSON con `model_validate_json` y `TypeAdapter`
- **Decidir** dónde validar (la frontera) y qué modelar con una dataclass, un `TypedDict` o un modelo de Pydantic

---

## 📋 Prerrequisitos

- [Semana 12](../week-12-closures_decoradores_y_functools/README.md): closures, decoradores y `functools`.
- El *pull request* `week-12` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-13-typing_estricto_mypy_y_pydantic/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 12 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · mypy estricto](1-teoria/01-mypy-estricto.md) | Qué deja pasar mypy, qué añade `strict`, `Any` frente a `object`, estrechar tipos, `cast` y `# type: ignore` | 45 min |
| [02 · Tipos avanzados](1-teoria/02-tipos-avanzados.md) | `TypedDict`, `Mapping` y `Sequence`, genéricos con `[T]`, alias y `NewType`, `Literal`, `Final` y `assert_never` | 50 min |
| [03 · Modelos de Pydantic](1-teoria/03-modelos-pydantic.md) | `BaseModel`, `model_validate`, modo normal y estricto, `ValidationError`, `Field`, `ConfigDict` y modelos anidados | 50 min |
| [04 · Validadores y serialización](1-teoria/04-validadores-y-serializacion.md) | `field_validator` antes y después del tipo, `model_validator`, el orden de validación, JSON de ida y vuelta y `TypeAdapter` | 50 min |
| [05 · Fronteras y diseño](1-teoria/05-fronteras-y-diseno.md) | Validar en la frontera, dataclass, `TypedDict` o Pydantic, el diseño de la capa 12, errores de la frontera y cómo probarla | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · mypy estricto](2-practicas/ejercicio-01-mypy-estricto/README.md) | Funciones sin anotar, `Any` de `json.loads`, `None` y `TypeIs`, `Literal` y `Final`, y `cast` | 1 h 30 min |
| [02 · Tipos avanzados](2-practicas/ejercicio-02-tipos-avanzados/README.md) | `TypedDict`, `dict` frente a `Mapping`, genéricos, `type` y `NewType`, y un `match` con `assert_never` | 1 h |
| [03 · Modelos de Pydantic](2-practicas/ejercicio-03-modelos-pydantic/README.md) | Validar y convertir, leer un `ValidationError`, el modo estricto, `Field` y `extra="forbid"`, modelos anidados y `frozen` | 1 h 30 min |
| [04 · Validadores y JSON](2-practicas/ejercicio-04-validadores-y-json/README.md) | `field_validator` después y antes del tipo, `model_validator`, JSON de ida y vuelta y `TypeAdapter` con una lista y una dataclass | 1 h 30 min |

### Proyecto

El Observatorio activa `mypy --strict` con el plugin de Pydantic y añade:

- `Summary`, un `TypedDict` para el resumen JSON;
- `write_json` con un `Mapping`;
- `core/schemas.py`: `MeasurementIn` valida cada medida de un JSON, y `read_measurements` y `read_scale` convierten un archivo en una `Series` o una `Scale`.

`main` no cambia, la versión sube a `0.13.0` y el proyecto gana su primera dependencia, `pydantic==2.14.2`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Preguntar a mypy qué tipo deduce | `reveal_type(expresión)`; bórralo después |
| Ver qué activa `--strict` | `uvx --from mypy==2.4.1 mypy --help` y busca `--strict` |
| Ignorar un solo error de mypy | `# type: ignore[código]`, con el código que da el error, nunca a secas |
| Ver todos los errores de un dato en Pydantic | `error.errors()`: una lista con `loc`, `type`, `msg` e `input` de cada uno |
| Ver el esquema de un modelo | `print(json.dumps(Modelo.model_json_schema(), indent=2))` |
| Ver qué instaló `uv add` | `uv tree --depth 1` |
| mypy con Pydantic en un ejercicio | `uv run --with mypy==2.4.1 mypy --strict archivo.py`, no `uvx`: así ve el entorno |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-13` de `python-<nombre>-<apellido>` con `pydantic==2.14.2`, `strict` y el plugin de mypy, `Summary` y `write_json` con `Mapping`, `core/schemas.py` (`MeasurementIn`, `read_measurements` y `read_scale`), los cuatro nombres en la API pública, la versión `0.13.0` y al menos 6 tests propios en `tests/test_my_schemas.py`. Todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check` y `mypy` sin avisos
2. ✅ `README.md` del repositorio con `schemas.py` en el árbol del paquete
3. ✅ Pull request `week-13` → `main` con tests, `mypy`, `ruff`, los errores que dio `strict` y por qué `write_json` pide un `Mapping`

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
uv run ruff check && uv run ruff format --check
uv run mypy
uv run observatorio --version
docker compose run --build --rm app
```

Los tests terminan en `passed` sin `failed` (al menos 401), ruff dice `All checks passed!` y `N files already formatted`, `mypy` dice `Success: no issues found` y `--version` escribe `observatorio 0.13.0`. En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 12](../week-12-closures_decoradores_y_functools/README.md) | **Semana 13** | [Semana 14](../week-14-testing_profesional_fixtures_parametrize_mocks_hypothesis_cobertura_y_logging/README.md) |

← [Volver al índice de semanas](../README.md)
