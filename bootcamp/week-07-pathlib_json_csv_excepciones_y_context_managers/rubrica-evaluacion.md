# Rúbrica de Evaluación — Semana 07: `pathlib`, JSON, CSV, excepciones y context managers

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 6 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | Con `path = Path("datos/2026/medidas.csv")`, ¿qué dan `path.parent`, `path.name`, `path.stem`, `path.suffix` y `path.with_suffix(".json")`? ¿Cuál de ellas necesita que el archivo exista? | 10 |
| 2 | `uv run observatorio -f medidas.csv` funciona en la raíz del proyecto y da "no existe el archivo" después de `cd src`. ¿Por qué? | 10 |
| 3 | ¿Por qué se abre un archivo con `with`? ¿Qué pasa con el archivo si salta una excepción dentro del bloque? | 10 |
| 4 | ¿Qué diferencia hay entre los modos `"w"`, `"a"` y `"x"`? ¿Por qué hay que escribir siempre `encoding="utf-8"`? | 10 |
| 5 | En un `try` con `except`, `else` y `finally`, ¿qué bloques se ejecutan si no hay error, si hay un error que el `except` captura y si hay uno que no captura? | 10 |
| 6 | ¿Qué hace `raise DataFileError(...) from error`? ¿Qué pierdes si quitas el `from error`? | 10 |
| 7 | ¿Por qué `except OSError` captura un `FileNotFoundError`? ¿Por qué no se escribe `except:` a secas? | 10 |
| 8 | ¿Por qué el CSV del Observatorio se separa con `;`? ¿Qué ventaja tiene `csv.reader` frente a `line.split(";")`? | 10 |
| 9 | ¿Qué devuelve `json.loads(json.dumps({"rango": (1, 2), 3: None}))`? ¿Por qué no es igual al original? | 10 |
| 10 | Escribe un context manager `timer(name)` con `@contextmanager` que escriba lo que tarda el bloque. ¿Por qué el `yield` va dentro de un `try` con `finally`? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. `Path('datos/2026')`, `'medidas.csv'`, `'medidas'`, `'.csv'` y `Path('datos/2026/medidas.json')`. Ninguna: las cinco trabajan con el texto de la ruta. Las que miran el disco son otras, como `exists()`, `is_file()` u `open()`.
2. `medidas.csv` es una ruta relativa, y se resuelve desde la carpeta de trabajo, no desde la del programa. Después de `cd src` apunta a `src/medidas.csv`, que no existe. Se arregla lanzando el programa desde la raíz o pasando la ruta correcta (`-f ../medidas.csv`).
3. Para que el archivo se cierre siempre, sin depender de llamar a `close()`. Si salta una excepción, `with` cierra el archivo al salir del bloque, y después la excepción sigue subiendo: equivale a un `try` con `finally: file.close()`.
4. `"w"` vacía el archivo al abrirlo, o lo crea; `"a"` escribe detrás de lo que había, o lo crea; `"x"` solo crea, y da `FileExistsError` si ya existe. Sin `encoding`, Python usa la codificación del sistema, que en Windows no siempre es UTF-8: el mismo archivo se leería bien en una máquina y con errores o `UnicodeDecodeError` en otra.
5. Sin error: `try`, `else` y `finally`. Con un error capturado: el `try` hasta la línea que falla, el `except` y `finally`. Con uno no capturado: el `try` hasta la línea que falla y `finally`, y después el error sigue subiendo.
6. Lanza una `DataFileError` con un mensaje propio y guarda la excepción original en su `__cause__`. Sin `from error`, el *traceback* dice "During handling of the above exception, another exception occurred", como si hubiera habido un segundo error por accidente, y el test de la causa falla.
7. Porque las excepciones forman una jerarquía y `FileNotFoundError` es una subclase de `OSError`: un `except` captura su tipo y todos los que heredan de él. `except:` a secas captura todo, también Ctrl+C (`KeyboardInterrupt`) y los errores de programación, y los esconde.
8. Porque en español la coma es el separador decimal (`12,5`), y Excel y LibreOffice en español exportan con `;`. `csv.reader` entiende las comillas: `"Sur; centro";8` da dos campos, y `split` daría tres con las comillas dentro.
9. `{'rango': [1, 2], '3': None}`. JSON no tiene tuplas, así que la tupla vuelve como lista, y las claves de un objeto JSON siempre son textos, así que `3` vuelve como `'3'`.
10. Por ejemplo:

    ```python
    @contextmanager
    def timer(name: str) -> Iterator[None]:
        start = time.perf_counter()
        try:
            yield
        finally:
            print(f"{name}: {time.perf_counter() - start:.3f} s")
    ```

    El cuerpo del `with` corre en el `yield`. Si lanza una excepción, esta aparece en el `yield`: sin `finally`, la línea de después no se ejecutaría y el tiempo no se escribiría.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Rojo, verde | El historial de `week-07` muestra los tests en rojo y un commit por función en verde, sin cambiar los tests | 8 |
| Commits con sentido | Commits pequeños, con Conventional Commits (`feat`, `test`, `chore`), sin `.venv/`, `__pycache__/` ni `resumen.json` | 6 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `mypy`, `-f medidas.csv -j resumen.json` y el informe en Docker | 8 |
| Rompe y explica | Provoca en vivo dos errores del paso 10 y explica qué excepción de Python saltó, dónde se tradujo y por qué el código de salida es 2 | 10 |
| Explica sus decisiones | Explica por qué `read_csv` reutiliza `read_lines`, por qué `main` captura solo `DataFileError` y qué pasaría con `except Exception` | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 6

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Funciones | Las seis funciones de `storage.py` y `main` pasan los 48 tests de `test_storage.py` y `test_main.py`, y los de las semanas anteriores siguen en verde | 30 |
| Errores bien tratados | Cada fallo de archivo sale como `DataFileError` con `raise ... from`; `main` la captura en un solo sitio y nunca muestra un *traceback* | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_storage.py` con datos del dominio y `tmp_path` (paso 11) | 20 |
| Tipos | `mypy src tests` sin errores | 10 |
| Datos y Docker | `medidas.csv` con cabecera y al menos 12 filas; `docker compose run --build --rm app` en verde | 10 |
| Git y README | Rama `week-07` en `python-<nombre>-<apellido>`, `resumen.json` en `.gitignore`, README con los comandos nuevos, un resumen de ejemplo y la tabla de errores | 10 |
| Pull request | Descripción con tests, `mypy`, `resumen.json` y dos casos de error explicados | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 08 (próximamente) |
