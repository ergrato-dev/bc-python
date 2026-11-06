# Semana 09 — Clases y `dataclasses`

> Empieza la fase 2. Hasta ahora tu Observatorio guardaba cada medida en una tupla y pasaba la unidad y los umbrales sueltos de función en función. Esta semana aprendes a crear tus propios tipos: clases con atributos y métodos, propiedades, constructores alternativos y, sobre todo, `dataclasses`, que escriben por ti el código repetitivo. El proyecto gana un modelo de tres clases, `Scale`, `Measurement` y `Series`, que reutiliza todas las funciones de la fase 1 sin cambiar ni un carácter del informe.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Escribir** clases con `__init__`, atributos y métodos, y **explicar** qué es `self` y dónde busca Python un atributo
- **Distinguir** atributos de clase y de instancia, y **evitar** la lista compartida entre objetos
- **Implementar** `__repr__`, `__str__` y `__eq__`, propiedades con `@property` y constructores alternativos con `@classmethod`
- **Declarar** clases de datos con `@dataclass`, `field(default_factory=...)` y `__post_init__`
- **Elegir** las opciones `frozen`, `order` y `slots` según la clase sea un valor o acumule datos
- **Elegir** entre tupla, `NamedTuple`, diccionario, `TypedDict` y *dataclass*, y **diseñar** clases que reutilizan funciones existentes

---

## 📋 Prerrequisitos

- [Semana 08](../week-08-proyectos_con_uv_modulos_paquetes_pyproject_ruff_y_lock/README.md): módulos, paquetes, `pyproject.toml`, ruff y lock.
- El *pull request* `week-08` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-09-clases_y_dataclasses/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 8 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Clases y objetos](1-teoria/01-clases-y-objetos.md) | Clase e instancia, `__init__` y `self`, métodos, `__dict__` y la búsqueda de atributos, atributos de clase, la lista compartida | 50 min |
| [02 · Propiedades y métodos especiales](1-teoria/02-propiedades-y-metodos-especiales.md) | `__repr__`, `__str__`, `__eq__` y el *hash*, `@property` y *setters*, el guion bajo, `@classmethod` y `@staticmethod` | 45 min |
| [03 · `dataclasses`](1-teoria/03-dataclasses.md) | `@dataclass`, campos y valores por defecto, `field(default_factory=...)`, `__post_init__`, `fields` y `asdict` | 50 min |
| [04 · *Dataclasses* inmutables y con `slots`](1-teoria/04-dataclasses-inmutables-y-con-slots.md) | `frozen` y `replace`, `order`, `slots`, `kw_only`, `ClassVar` y `match` | 45 min |
| [05 · Elegir el modelo](1-teoria/05-elegir-el-modelo.md) | Tupla, `NamedTuple`, diccionario, `TypedDict`, *dataclass* y clase normal; clases que reutilizan funciones; cuándo sobra una clase; probar clases | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Clases y objetos](2-practicas/ejercicio-01-clases-y-objetos/README.md) | Una clase vacía, `__init__` y `self`, métodos, atributos de clase y una lista compartida sin querer | 1 h 30 min |
| [02 · Propiedades y métodos especiales](2-practicas/ejercicio-02-propiedades-y-metodos-especiales/README.md) | `__repr__` y `__str__`, `__eq__` y el *hash*, una propiedad calculada y otra que valida, `@classmethod` y `@staticmethod` | 1 h 30 min |
| [03 · `dataclasses`](2-practicas/ejercicio-03-dataclasses/README.md) | Lo que genera `@dataclass`, valores por defecto, `default_factory`, `__post_init__`, `frozen`, `order`, `replace` y `asdict` | 1 h 30 min |
| [04 · Elegir el modelo](2-practicas/ejercicio-04-elegir-el-modelo/README.md) | La misma medida como tupla, diccionario, `NamedTuple`, *dataclass* y *dataclass* con `slots`, y lo que ve mypy | 1 h |

### Proyecto

El Observatorio gana un modelo en `core/model.py`: `Scale` (unidad y umbrales, que se validan al crearse), `Measurement` (una medida, con `from_line`) y `Series` (las medidas de una entrada, con los análisis como métodos). Los métodos llaman a las funciones de la fase 1, `main` usa `SCALE` y una `Series`, y la versión sube a `0.9.0`. El informe no cambia ni un carácter. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Ver los atributos de un objeto | `vars(objeto)` (no funciona con `slots`) |
| Ver los campos de una *dataclass* | `[f.name for f in dataclasses.fields(Clase)]` |
| Una *dataclass* como diccionario, para JSON | `dataclasses.asdict(objeto)` |
| "Cambiar" un objeto `frozen` | `dataclasses.replace(objeto, campo=valor)` |
| Una lista o un diccionario por defecto | `field(default_factory=list)` |
| Saber de qué clase es un objeto | `type(objeto).__name__` o `isinstance(objeto, Clase)` |
| Probar una clase en el REPL | `uv run python -i -c "from observatorio.core import *"` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-09` de `python-<nombre>-<apellido>` con `core/model.py` (`Scale`, `Measurement` y `Series`), las tres clases en la API pública, `main` usando `SCALE` y `Series`, la versión `0.9.0` y al menos 6 tests propios en `tests/test_my_model.py`, todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check` y `mypy` sin avisos
2. ✅ `README.md` del repositorio con `model.py` en el árbol del paquete
3. ✅ Pull request `week-09` → `main` con tests, `mypy`, `ruff`, tu escala con el error de los umbrales al revés y por qué `Measurement` es `frozen`

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

Los tests terminan en `passed` sin `failed` (al menos 267), ruff dice `All checks passed!` y `N files already formatted`, `mypy` dice `Success: no issues found` y `--version` escribe `observatorio 0.9.0`. En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 08](../week-08-proyectos_con_uv_modulos_paquetes_pyproject_ruff_y_lock/README.md) | **Semana 09** | [Semana 10](../week-10-herencia_composicion_abc_y_protocol/README.md) |

← [Volver al índice de semanas](../README.md)
