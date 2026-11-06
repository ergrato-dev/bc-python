# Rúbrica de Evaluación — Semana 14: Testing profesional

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 13 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | `test_series_fixture_can_be_changed` añade una medida a `series` y `test_series_fixture_is_new_in_each_test` espera 3. ¿Por qué pasan los dos, en cualquier orden? ¿Qué pasaría con `@pytest.fixture(scope="module")`? | 10 |
| 2 | ¿Para qué sirve `conftest.py`? ¿Por qué `write_file` devuelve una función y no un archivo? | 10 |
| 3 | `test_parse_value_rejects_non_finite_values` tiene 5 casos con `parametrize`. ¿Qué ventaja tiene sobre un solo test con un bucle `for text in [...]`? | 10 |
| 4 | Tu proyecto tenía más de 300 tests en verde y el bug de `"Norte;abc"` desde la semana 2. ¿Por qué no lo encontró ninguno, y por qué Hypothesis sí? | 10 |
| 5 | Hypothesis da `Failing test case: ...(lines=['0;:'])`. ¿Es ese el primer ejemplo que falló? ¿Qué ha hecho Hypothesis con él y qué guarda en `.hypothesis/`? | 10 |
| 6 | `test_median_is_between_min_and_max` usa `st.floats(min_value=-1e6, max_value=1e6, ...)`. ¿Qué pasa con `st.floats()` sin límites? ¿Es un bug de `median`? ¿Y `"nan"` en un archivo de medidas, es un bug? | 10 |
| 7 | `weather.py` hace `from urllib.request import urlopen`. ¿Por qué `patch("urllib.request.urlopen")` no sirve en sus tests? ¿Qué hay que parchear? | 10 |
| 8 | ¿Por qué el `PermissionError` de `read_lines` se prueba con `mock.patch.object(Path, "open", ...)` y no con `chmod 000`? ¿Qué añade `autospec=True` al espiar `write_json`? | 10 |
| 9 | Tu proyecto tiene un 99 % de cobertura. ¿Significa que tiene pocos bugs? ¿Qué encuentra la cobertura de ramas que la de líneas no ve? | 10 |
| 10 | ¿Por qué `storage.py` crea un logger y escribe en DEBUG, pero nunca llama a `logging.basicConfig`? ¿Por qué `logger.debug("%d líneas", n)` y no una f-string? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Las fixtures son de `scope="function"` por defecto: pytest crea una `series` **nueva** para cada test. Lo que un test le hace no lo ve el siguiente, y el orden no importa. Con `scope="module"`, los dos tests del archivo compartirían la misma serie, y `test_series_fixture_is_new_in_each_test` fallaría con 4 si se ejecutara después del otro. Un objeto que se puede cambiar no se comparte entre tests.
2. `conftest.py` reúne las fixtures que usan varios archivos de tests. pytest lo carga antes que los tests de su carpeta, y sus fixtures valen en todos ellos sin importarlas. `write_file` es una **fábrica**: cada test necesita archivos distintos (nombre y contenido), y a veces varios. La fixture pone lo común (la carpeta `tmp_path`, UTF-8) y el test decide lo particular.
3. Con `parametrize` son 5 tests: cada caso pasa o falla por separado y sale en el informe con su id (`[nan]`, `[inf]`). Con un bucle es un solo test que se para en el primer fallo: no sabes cuántos casos fallan ni cuáles. Además, `-k inf` ejecuta solo un caso.
4. Todos los tests eran de **ejemplos**: probaban `"Norte;12,5"`, `"Sur;NA"` y líneas sin `;`, como `"malo"`. Nadie escribió una línea con `;` y un valor que no fuera un número. Hypothesis no depende de tu imaginación: genera cientos de listas de líneas, incluidas `"texto;texto"`, y comprueba la propiedad "`process_lines` nunca lanza una excepción".
5. No. El primero que falló era seguramente largo y lleno de caracteres raros. Hypothesis lo **encogió**: probó versiones más simples que siguieran fallando hasta llegar a la mínima, una línea con una etiqueta de un carácter y un valor que no es un número. En `.hypothesis/` guarda ese contraejemplo, y en la siguiente ejecución lo prueba primero: el fallo no desaparece por azar mientras lo arreglas.
6. Sin límites, Hypothesis genera números como `1e308`: `(1e308 + 1e308) / 2` da `inf`, que es mayor que el máximo, y la propiedad falla. No es un bug para el Observatorio: ningún sensor mide `1e308`, y la estrategia debe describir el dominio real. `"nan"` sí es un bug: es un texto que puede aparecer en un archivo de verdad, `float` lo acepta, `classify` lo pone en `alto` y estropea la mediana. Ahí cambia el código, no la estrategia.
7. `from ... import urlopen` crea en `weather` un nombre `urlopen` propio, que apunta a la función. `patch("urllib.request.urlopen")` cambia el nombre del módulo `urllib.request`, pero `weather.urlopen` sigue apuntando a la función real, y el test hace una petición de verdad. Se parchea donde se **usa** el nombre: `patch("weather.urlopen")`.
8. `chmod 000` no impide leer a `root`, que es como se ejecutan muchos contenedores y CI, y en Windows no funciona igual: el test pasaría en unos equipos y fallaría en otros. El mock hace que `Path.open` lance `PermissionError` en cualquier equipo. `autospec=True` da al doble la firma de `write_json`: si `main` la llamara con argumentos que la función real no acepta, el test fallaría con `TypeError`, en vez de pasar en verde.
9. No. La cobertura dice qué se **ejecutó**, no qué se **comprobó**: `parse_value` se ejecutaba en cientos de tests, pero ninguno con `"nan"`, y había tres bugs con casi el 100 %. Un test sin `assert` también cubre líneas. La cobertura de ramas mira los dos caminos de cada decisión: un `if` sin `else` en el que siempre se entró cuenta como 100 % de líneas, pero aparece como rama parcial (`34->36`).
10. El paquete escribe en sus loggers, y quien lo **usa** decide qué ver y dónde. Hoy es `main` con `-v`, y mañana puede ser un test (que no quiere nada en la terminal) o una API (semana 20). Si `storage.py` llamara a `basicConfig`, impondría su nivel y su formato a todo el programa. Con `%` y argumentos, `logging` solo compone el texto si el mensaje se va a ver. Con una f-string se compone siempre, aunque el nivel DEBUG esté apagado.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-14` muestra un commit por paso (dependencias, fixtures, `abc`, `nan`, registro, `-v`, permiso, coverage, versión, tests), sin cambiar los tests del bootcamp | 8 |
| Arregla en la raíz | `parse_line` usa `parse_record` en lugar de repetir la regla; `iter_lines` y `read_lines` tienen los mismos errores; `git diff main -- src` solo toca los archivos del árbol del paso "Qué construyes" | 8 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff check`, `ruff format --check`, `mypy`, `coverage report` y `observatorio -v -f ...`, en su máquina y en Docker | 6 |
| Rompe y explica | Quita el `try` de `parse_record` y explica el contraejemplo de Hypothesis; quita `math.isfinite` y explica qué test falla; cambia el `patch` de un test a un sitio equivocado y explica qué pasa | 10 |
| Explica sus decisiones | Explica por qué los `float` de las propiedades tienen límites, por qué el paquete no configura el registro y por qué el mínimo de cobertura es 95 % y no 100 % | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 13

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Los tres bugs | `parse_record` y `parse_line` rechazan valores que no son números; `parse_value` y `MeasurementIn` rechazan `nan` e `inf`; `read_lines` e `iter_lines` convierten `PermissionError` en `DataFileError`; pasan sus tests de `test_quality.py` y los de las semanas anteriores siguen en verde | 15 |
| Fixtures y registro | `tests/conftest.py` con `scale`, `lines`, `series` y `write_file`; loggers con `__name__` en `storage.py` y `groups.py`, en DEBUG; `-v` con `basicConfig` solo en `main` | 15 |
| Dependencias, cobertura y versión | `hypothesis==6.170.8` y `coverage==7.17.0` en `dev` y en `uv.lock`; `[tool.coverage]` con ramas y `fail_under = 95`; versión `0.14.0`; pasan `test_package.py` y `test_main.py` | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_quality.py` con datos del dominio, con al menos una propiedad, un `parametrize`, una fixture, un `caplog` y un mock, y el test de las líneas que el paso 12 dejó sin cubrir (paso 15) | 20 |
| Calidad | `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos; `docker compose run --build --rm app` en verde, sin `HypothesisWarning` | 10 |
| Git y README | Rama `week-14` en `python-<nombre>-<apellido>`; `.hypothesis/` y `.coverage` en el `.gitignore`; README con `-v` y el comando de cobertura | 10 |
| Pull request | Descripción con tests, `mypy`, `ruff`, la cobertura y las preguntas del paso 16 | 20 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 15 (próximamente) |
