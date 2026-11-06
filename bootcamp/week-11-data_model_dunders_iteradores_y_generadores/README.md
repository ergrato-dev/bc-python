# Semana 11 — Data model: dunders, iteradores y generadores

> Llevas diez semanas escribiendo `len(lista)`, `a + b` y `for x in algo` sin preguntarte qué hace Python por debajo. Esta semana lo descubres: cada operación llama a un método especial (*dunder*), y si lo escribes en tu clase, tu clase entra en el idioma de Python. Después abres el `for`: iterables, iteradores y generadores, funciones que se pausan y calculan cada valor cuando alguien lo pide. El proyecto le da a `Series` `len`, `for`, `[]` y `+`, y estrena tres generadores que procesan medidas de una en una, aunque no terminen nunca.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Explicar** el *data model* y **escribir** `__repr__`, `__str__`, `__eq__`, `__hash__` y `__lt__` sin romper los `set` ni los diccionarios
- **Sobrecargar** operadores con `__add__` y `__radd__`, **devolviendo** `NotImplemented` con los tipos que no conoces
- **Dar** a una clase `len()`, `if`, `[]`, rebanadas e `in` con los protocolos de contenedor
- **Distinguir** un iterable de un iterador, **recorrer** a mano con `iter()` y `next()` y **escribir** un iterador como clase
- **Escribir** funciones y expresiones generadoras, **usar** `yield from` y **prever** cuándo se ejecuta su código
- **Encadenar** generadores en tuberías perezosas con `itertools` y **probarlas**, también con entradas infinitas

---

## 📋 Prerrequisitos

- [Semana 10](../week-10-herencia_composicion_abc_y_protocol/README.md): herencia, composición, ABC y `Protocol`.
- El *pull request* `week-10` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-11-data_model_dunders_iteradores_y_generadores/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 10 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · El data model y los dunders](1-teoria/01-data-model-y-dunders.md) | Qué llama Python con su sintaxis, `__repr__` y `__str__`, `__eq__` y `__hash__`, `__lt__` con `total_ordering` y lo que genera `@dataclass` | 50 min |
| [02 · Operadores y contenedores](1-teoria/02-operadores-y-contenedores.md) | Operadores aritméticos, `NotImplemented`, `__radd__`, `__bool__` y `__len__`, `__getitem__` y rebanadas, `__contains__` y `collections.abc.Sequence` | 50 min |
| [03 · Iteradores](1-teoria/03-iteradores.md) | Iterable e iterador, `iter()`, `next()` y `StopIteration`, el `for` por dentro, un iterador como clase y por qué se agota | 45 min |
| [04 · Generadores](1-teoria/04-generadores.md) | `yield`, expresiones generadoras, memoria, `yield from`, cuándo se ejecuta el cuerpo y cómo se anota | 50 min |
| [05 · Pipelines perezosos](1-teoria/05-pipelines-perezosos.md) | Perezoso frente a ansioso, `itertools`, dónde termina la pereza, el diseño de la capa 10 y cómo probar generadores | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Dunders](2-practicas/ejercicio-01-dunders/README.md) | Una clase sin dunders, `__repr__` y `__str__`, el `__hash__` que desaparece, `total_ordering`, `__add__` y `__radd__` con `sum`, y `__bool__` | 1 h 30 min |
| [02 · Contenedores](2-practicas/ejercicio-02-contenedores/README.md) | `__len__` y `__getitem__`, un `for` sin `__iter__`, rebanadas, `__contains__` propio y lo que regala `Sequence` | 1 h 30 min |
| [03 · Iteradores](2-practicas/ejercicio-03-iteradores/README.md) | `iter()` y `next()` a mano, el `for` como `while`, una cuenta atrás como clase, iterable frente a iterador y los iteradores de la biblioteca estándar | 1 h 30 min |
| [04 · Generadores](2-practicas/ejercicio-04-generadores/README.md) | `yield` paso a paso, la memoria de una lista frente a un generador, generadores infinitos, una tubería y `yield from` | 1 h |

### Proyecto

El Observatorio gana dunders y generadores: `Measurement` se escribe como línea con `__str__`; `Series` tiene `len`, `for`, `in`, `[]` y `+`; y `core/streams.py` trae `iter_lines`, `iter_measurements` y `running_mean`, que procesan las medidas de una en una. `main` no cambia, la versión sube a `0.11.0` y el informe no cambia ni un carácter. **Es el único entregable de la semana.**
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
| Ver qué dunders tiene una clase | `[name for name in dir(Clase) if name.startswith("__")]` |
| Imprimir con `repr` dentro de un *f-string* | `f"{valor!r}"`: pone las comillas de los `str` |
| El primer elemento que cumple algo, o `None` | `next((x for x in datos if x > 50), None)` |
| Los `n` primeros de un generador | `list(itertools.islice(gen, n))` |
| Saber si algo es un iterador | `iter(x) is x` |
| Sumar objetos propios sin `__radd__` | `sum(objetos, ValorInicial(0))` |
| Ver los valores de un generador al depurar | `list(gen)`, sabiendo que lo gastas |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-11` de `python-<nombre>-<apellido>` con `Measurement.__str__`; `__len__`, `__iter__`, `__getitem__` y `__add__` en `Series`; `core/streams.py` (`iter_lines`, `iter_measurements` y `running_mean`), los tres nombres en la API pública, la versión `0.11.0` y al menos 6 tests propios en `tests/test_my_datamodel.py`, todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check` y `mypy` sin avisos
2. ✅ `README.md` del repositorio con `streams.py` en el árbol del paquete
3. ✅ Pull request `week-11` → `main` con tests, `mypy`, `ruff`, el `AttributeError` del `__add__` ingenuo y cuándo falla `iter_lines` con una ruta mala

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

Los tests terminan en `passed` sin `failed` (al menos 329), ruff dice `All checks passed!` y `N files already formatted`, `mypy` dice `Success: no issues found` y `--version` escribe `observatorio 0.11.0`. En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 10](../week-10-herencia_composicion_abc_y_protocol/README.md) | **Semana 11** | Semana 12 (próximamente) |

← [Volver al índice de semanas](../README.md)
