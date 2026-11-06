# Semana 10 — Herencia, composición, ABC y `Protocol`

> La semana pasada creaste tus propios tipos. Esta aprendes a relacionarlos: una clase que **es** otra con algo más (herencia), una que **tiene** otras dentro (composición), una base que obliga a sus hijas a escribir un método (clase abstracta) y un tipo que se cumple solo con tener los métodos adecuados (`Protocol`). El proyecto deja de decidir con un `if` de dónde salen las líneas: cada origen (argumentos, `stdin`, un `.txt`, un `.csv`) pasa a ser una fuente con un método `lines()`, y el informe no cambia ni un carácter.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Crear** subclases, **sustituir** métodos heredados y **extenderlos** con `super()`, y **explicar** la MRO
- **Distinguir** "es un" de "tiene un" y **preferir** la composición cuando la herencia no encaja en todo
- **Declarar** clases abstractas con `ABC` y `@abstractmethod`, y **escribir** métodos plantilla
- **Declarar** un `Protocol` y **dejar** que mypy compruebe quién lo cumple, sabiendo qué comprueba y qué no `@runtime_checkable`
- **Heredar** de *dataclasses* respetando el orden de los campos, `frozen` y `slots`
- **Diseñar** una jerarquía plana que combina un `Protocol`, una base abstracta y una función, y **probarla**

---

## 📋 Prerrequisitos

- [Semana 09](../week-09-clases_y_dataclasses/README.md): clases, propiedades y `dataclasses`.
- El *pull request* `week-09` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-10-herencia_composicion_abc_y_protocol/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 9 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Herencia](1-teoria/01-herencia.md) | Subclases, *override*, `super()`, la MRO, `isinstance` e `issubclass`, polimorfismo y jerarquías de excepciones | 50 min |
| [02 · Composición](1-teoria/02-composicion.md) | "Es un" o "tiene un", la trampa de heredar de `list`, delegar, cambiar una pieza y la prueba de "B es un A en todo" | 45 min |
| [03 · Clases abstractas](1-teoria/03-clases-abstractas.md) | `ABC` y `@abstractmethod` frente a `NotImplementedError`, el método plantilla, propiedades abstractas, bases que son *dataclasses* y `collections.abc` | 50 min |
| [04 · `Protocol`](1-teoria/04-protocol.md) | *Duck typing*, tipado estructural con `Protocol`, `@runtime_checkable` y sus límites, y cuándo un `Protocol` y cuándo una ABC | 45 min |
| [05 · Diseñar jerarquías](1-teoria/05-disenar-jerarquias.md) | Herencia de *dataclasses*, varias bases y *mixins*, jerarquías planas, el diseño de las fuentes del proyecto y cómo probar una jerarquía | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Herencia](2-practicas/ejercicio-01-herencia/README.md) | Una subclase vacía, un *override*, `super()` y el error de olvidarlo, la MRO, el polimorfismo y una jerarquía de excepciones | 1 h 30 min |
| [02 · Composición](2-practicas/ejercicio-02-composicion/README.md) | Una lista sin negativos heredando de `list` y teniendo una lista; cambiar la pieza por un `deque`; un objeto hecho de piezas | 1 h 30 min |
| [03 · Clases abstractas](2-practicas/ejercicio-03-clases-abstractas/README.md) | De `NotImplementedError` a `ABC`, el método plantilla, una propiedad abstracta y una base abstracta que es una *dataclass* | 1 h 30 min |
| [04 · `Protocol`](2-practicas/ejercicio-04-protocol/README.md) | *Duck typing*, un `Protocol`, lo que deja pasar `@runtime_checkable` y lo que encuentra mypy | 1 h |

### Proyecto

El Observatorio gana `core/sources.py`: el `Protocol` `Source` (algo con `lines()`), `LinesSource` para argumentos y `stdin`, la base abstracta `FileSource` con sus hijas `TextFile` y `CsvFile`, y la función `open_file`, que elige la clase por la extensión. `main` solo pide `source.lines()` y la versión sube a `0.10.0`. El informe no cambia ni un carácter. **Es el único entregable de la semana.**
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
| Ver en qué orden busca Python un método | `[cls.__name__ for cls in Clase.__mro__]` |
| Saber qué métodos le faltan a una clase abstracta | `Clase.__abstractmethods__` |
| ¿Hereda de...? | `issubclass(Hija, Base)`; para un objeto, `isinstance(objeto, Base)` |
| La clase exacta de un objeto, sin subclases | `type(objeto) is Clase` (casi siempre quieres `isinstance`) |
| Llamar al método de la base desde la hija | `super().metodo(...)` |
| Comprobar un `Protocol` sin ejecutar | `uv run mypy` |
| Un objeto de prueba que cumple un `Protocol` | Una clase de tres líneas dentro del test, con el método que pide |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-10` de `python-<nombre>-<apellido>` con `core/sources.py` (`Source`, `LinesSource`, `FileSource`, `TextFile`, `CsvFile` y `open_file`), los seis nombres en la API pública, `main` leyendo a través de las fuentes, la versión `0.10.0` y al menos 6 tests propios en `tests/test_my_sources.py`, todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check` y `mypy` sin avisos
2. ✅ `README.md` del repositorio con `sources.py` en el árbol del paquete
3. ✅ Pull request `week-10` → `main` con tests, `mypy`, `ruff`, el error de mypy al romper el `Protocol`, el `TypeError` de la base abstracta y por qué `LinesSource` no hereda de nada

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

Los tests terminan en `passed` sin `failed` (al menos 298), ruff dice `All checks passed!` y `N files already formatted`, `mypy` dice `Success: no issues found` y `--version` escribe `observatorio 0.10.0`. En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 09](../week-09-clases_y_dataclasses/README.md) | **Semana 10** | Semana 11 (próximamente) |

← [Volver al índice de semanas](../README.md)
