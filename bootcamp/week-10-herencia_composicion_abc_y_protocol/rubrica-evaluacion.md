# Rúbrica de Evaluación — Semana 10: Herencia, composición, ABC y `Protocol`

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 9 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | `class AirSensor(Sensor): pass`. ¿Por qué `AirSensor("Centro", "µg/m³").record(18.5)` funciona? ¿Dónde busca Python `record` y en qué orden? | 10 |
| 2 | El `__init__` de `ForgetfulSensor` guarda `self.pollutant` y nada más. ¿Por qué `record` falla con `'ForgetfulSensor' object has no attribute 'readings'`? ¿Cómo se arregla? | 10 |
| 3 | `HeaderError` hereda de `DataFileError`. Si `except DataFileError` va antes que `except HeaderError`, ¿qué pasa con un `HeaderError`? ¿Por qué? | 10 |
| 4 | `ReadingList(list)` valida en `append`. Da dos formas de colar un negativo y explica por qué heredar de `list` no protege los datos. ¿Qué harías en su lugar? | 10 |
| 5 | ¿Qué dos problemas tiene una base con `raise NotImplementedError` que resuelve `@abstractmethod`? ¿Cuándo aparece cada error? | 10 |
| 6 | ¿Qué es un método plantilla? Pon un ejemplo con una base abstracta que tenga un método concreto y uno abstracto. | 10 |
| 7 | `LinesSource` cumple `Source` sin heredar de él. ¿Cómo lo sabe mypy? ¿Qué diferencia hay entre tipado estructural y nominal? | 10 |
| 8 | Con `@runtime_checkable`, `isinstance(WrongType(), Source)` da `True` aunque su `lines()` devuelve un `str`. ¿Por qué? ¿Quién detecta el error? | 10 |
| 9 | ¿Por qué `TextFile` y `CsvFile` no llevan `@dataclass` y aun así tienen `path`, `__repr__` y `__eq__`? ¿Por qué `TextFile(ruta) != CsvFile(ruta)`? | 10 |
| 10 | En tu proyecto, ¿por qué `Source` es un `Protocol`, `FileSource` una clase abstracta y `open_file` una función? ¿Por qué `LinesSource` no hereda de `FileSource`? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Porque `AirSensor` hereda de `Sensor` todos sus métodos, también el `__init__`. Python busca `record` primero en el objeto (su `__dict__` solo tiene `name`, `unit` y `readings`), después en `AirSensor` (no está), después en `Sensor` (lo encuentra y lo usa). Si no estuviera, seguiría con `object`. Ese orden es `AirSensor.__mro__`.
2. Porque su `__init__` sustituye por completo al de `Sensor`, y el de `Sensor` era el que creaba `self.readings`. `record` hace `self.readings.append(...)` y el atributo no existe. Se arregla empezando el `__init__` de la hija con `super().__init__(name, unit)`.
3. Entra por `except DataFileError` y el `except HeaderError` nunca se ejecuta. Python usa el primer `except` que encaja, y un `HeaderError` **es** un `DataFileError` (`isinstance` da `True`). Los `except` van del más concreto al más general.
4. `insert`, `extend`, `+=` o `lista[i] = valor` meten valores sin pasar por `append`; además, `lista + [1.0]` devuelve una `list` normal. Al heredar, la clase es una `list` en todo, con sus cuarenta y pico métodos, y habría que sustituirlos todos. En su lugar, composición: una clase que guarda una lista en `_values` y solo ofrece `add`, que valida, y `values`, que devuelve una copia.
5. La base se puede crear aunque no sirva para nada, y una subclase que olvida el método (o lo escribe mal) también se crea. Con `NotImplementedError`, los dos errores aparecen al **llamar** al método, quizá mucho después. Con `ABC` y `@abstractmethod`, aparecen al **crear** el objeto (`TypeError: Can't instantiate abstract class ...`), y mypy los ve antes de ejecutar.
6. Un método concreto de la base que fija los pasos y llama a métodos abstractos que rellena cada subclase. Por ejemplo, `FileExporter.export` escribe el archivo en UTF-8 y devuelve el número de filas, y llama a `render(rows)`, abstracto, que en `CsvExporter` devuelve el texto CSV y en `JsonExporter` el JSON. Lo común está escrito una vez.
7. mypy compara la estructura: `Source` pide un método `lines(self) -> list[str]`, y `LinesSource` lo tiene con esa firma. En el tipado estructural (`Protocol`), un tipo se cumple teniendo los métodos; en el nominal (herencia, ABC), hay que heredar de la clase. Por eso cualquier objeto de prueba con `lines()` vale como fuente.
8. Porque `isinstance` con un `Protocol` solo comprueba que el objeto tenga un atributo llamado `lines`; no mira parámetros ni tipo de retorno. El error lo detecta mypy, sin ejecutar: `incompatible type "WrongType"; expected "Source"`, con una nota que compara la firma esperada y la recibida.
9. Porque `FileSource` es una *dataclass* y las subclases heredan lo que generó `@dataclass`: el campo `path`, `__init__`, `__repr__` (que usa el nombre de la clase real) y `__eq__`. Ese `__eq__` comprueba primero que los dos objetos sean de la misma clase, así que un `TextFile` y un `CsvFile` con la misma ruta no son iguales: se leen distinto.
10. `Source` es lo único que necesita `main` (un método `lines()`), y como `Protocol` lo cumplen `LinesSource` y cualquier objeto de prueba sin heredar. `FileSource` es abstracta porque `TextFile` y `CsvFile` comparten código (la ruta, el `__init__`, la inmutabilidad) y nadie debe crear un `FileSource` a secas. `open_file` es una regla de una línea sobre la extensión: una clase "fábrica" no aportaría nada. `LinesSource` no tiene ruta: heredar de `FileSource` sería decir que es un archivo, y no lo es.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-10` muestra un commit por paso (esqueleto, `Protocol`, `LinesSource`, subclases, `open_file`, base abstracta, versión, `main`, tests), sin cambiar los tests del bootcamp | 8 |
| Reutiliza sin reescribir | `TextFile` y `CsvFile` llaman a `read_lines` y `read_csv`; `git diff main -- src/observatorio/core` solo muestra `sources.py` nuevo y `__init__.py` ampliado | 8 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff check`, `ruff format --check`, `mypy` y `--version`, en su máquina y en Docker | 6 |
| Rompe y explica | Renombra `LinesSource.lines` y explica el error de mypy sin ejecutar; crea `FileSource(ruta)` y explica el `TypeError`; quita `lines` de `TextFile` y explica por qué ya no se puede crear | 10 |
| Explica sus decisiones | Explica por qué `Source` es un `Protocol` y `FileSource` una ABC, por qué `LinesSource` no hereda y qué hace `monkeypatch` en `test_main_reads_files_through_open_file` | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 9

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Fuentes | `core/sources.py` con `Source`, `LinesSource`, `FileSource`, `TextFile`, `CsvFile` y `open_file`, como en la tabla del proyecto; pasan los 25 tests de `test_sources.py` y los de las semanas anteriores siguen en verde | 30 |
| API y versión | Los seis nombres en `observatorio.core.__all__`; versión `0.10.0`; pasan `test_package.py` y `test_main.py` | 10 |
| `main` usa las fuentes | `source: Source`, `open_file` para `-f` y `LinesSource` para argumentos y `stdin`, con un solo `try` alrededor de `source.lines()`; el informe es idéntico al de la semana 9 | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_sources.py` con datos del dominio, que importan solo de `observatorio.core` (paso 12) | 20 |
| Calidad | `ruff check`, `ruff format --check` y `mypy` sin avisos; `docker compose run --build --rm app` en verde | 10 |
| Git y README | Rama `week-10` en `python-<nombre>-<apellido>`, README con `sources.py` en el árbol del paquete | 10 |
| Pull request | Descripción con tests, `mypy`, `ruff`, los dos errores provocados y la decisión sobre `LinesSource` | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 11](../week-11-data_model_dunders_iteradores_y_generadores/README.md) |
