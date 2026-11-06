# Rúbrica de Evaluación — Semana 15: CLI con Typer y Rich

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 14 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | Tu `main` de la semana 14 respondía a `-f medidas.csv -j resumen.json`, pero no a `-j resumen.json -f medidas.csv`. ¿Por qué? ¿Qué hace Typer distinto? | 10 |
| 2 | En `def umbrales(valor: float, bajo: float = 10.0)`, ¿cuál es un argumento y cuál una opción, y por qué? ¿Qué recibe la función si escribes `umbrales doce`? | 10 |
| 3 | ¿Qué parte de `Annotated[Path \| None, typer.Option("--archivo", "-f", help="...")]` lee mypy y qué parte lee Typer? ¿Por qué tu proyecto no usa `exists=True` en `--archivo`? | 10 |
| 4 | `observatorio informe -v -f medidas.csv` da `No such option: -v`. ¿Por qué, si `-v` existe? | 10 |
| 5 | ¿Qué hace `raise typer.Exit()` dentro de `show_version`, y por qué `observatorio --version` funciona sin escribir ningún comando? | 10 |
| 6 | El comando `informe` termina con códigos 0, 1 o 2. Di qué situación da cada uno y quién lo decide: Typer o tu código. ¿Por qué `return 1` no serviría? | 10 |
| 7 | Una estación se llama `Sala [b]`. ¿Qué escribe `Console().print(...)` y por qué no da ningún error? ¿Qué tiene que ver con una inyección SQL? | 10 |
| 8 | En tu terminal, el informe sale en color; con `observatorio informe -f medidas.csv \| cat`, en texto plano y con 80 columnas. ¿Quién decide eso? ¿Para qué sirve `soft_wrap=True`? | 10 |
| 9 | Tu proyecto tiene un 99 % de cobertura, y aun así un mutante que cambia la escala de la tabla sobrevivía. ¿Cómo es posible? ¿Qué cambió en el test que lo mata? | 10 |
| 10 | Esta semana cambiaste toda la forma de llamar al Observatorio. ¿Qué archivos de `core/` tocaste? ¿Por qué, y qué te dice eso de la arquitectura? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. El `match` compara la lista entera con patrones fijos, y solo había un `case` con `-f` primero y `-j` después. Cualquier otro orden caía en "opción desconocida". Typer construye un **analizador** que reconoce cada opción por su nombre, en cualquier posición, con `--archivo valor` o `--archivo=valor`. Además, convierte los tipos y escribe la ayuda.
2. `valor` no tiene valor por defecto: es un **argumento** obligatorio, por posición. `bajo` tiene `= 10.0`: es la **opción** `--bajo`, que vale `10.0` si no se escribe. Con `umbrales doce`, la función **no recibe nada**: Typer no puede convertir `"doce"` a `float`, escribe `Invalid value for 'valor': 'doce' is not a valid float.` en stderr y termina con código 2 sin llamarla.
3. mypy ve `Path | None`: el parámetro es eso, y nada más. Typer lee el `typer.Option(...)`: los nombres `--archivo` y `-f` y la ayuda. Sin `exists=True`, quien comprueba el archivo es `open_file` y `read_lines`, que dan un `DataFileError` con un mensaje en español ya probado. Validar en dos sitios daría dos mensajes distintos para el mismo error, y uno de ellos en inglés.
4. `-v` es una opción del **callback**, de la aplicación entera. Las opciones del callback van **antes** del nombre del comando: `observatorio -v informe -f medidas.csv`. Detrás de `informe`, Typer busca `-v` entre las opciones de `informe`, y no está.
5. `show_version` es el *callback* de la opción: Typer lo llama en cuanto lee `--version`. `typer.Exit()` termina el programa en ese momento con código 0, antes de buscar un comando. Por eso no hace falta escribir ninguno. `is_eager=True` hace que esa opción se procese antes que las demás.
6. `0`: todo bien, la función termina normalmente. `1`: hubo líneas inválidas; lo decide tu código con `raise typer.Exit(1)`. `2`: uso incorrecto. Lo decide Typer (opción desconocida, tipo incorrecto) o tu código (`typer.BadParameter` con líneas y `--archivo` a la vez; `DataFileError` convertido con `fail(..., 2)`). Typer ignora el valor que devuelve un comando: `return 1` terminaría con código 0.
7. Escribe `Sala `: Rich interpreta `[b]` como la marca de negrita, la quita del texto y pone en negrita lo que sigue. No hay error porque `[b]` es una marca válida. Un dato del usuario se ha interpretado como una **instrucción**, igual que en una inyección SQL un texto se ejecuta como parte de la consulta. La solución también es la misma: separar datos e instrucciones, con `escape` o con `Console(markup=False)`.
8. Rich: al escribir, comprueba si la salida va a una terminal. Si va, pone colores y usa el ancho de la ventana. Si no (una tubería, un archivo, `CliRunner`, Docker sin terminal), escribe texto plano y usa 80 columnas, porque no tiene ventana que medir. `soft_wrap=True` impide que corte las líneas de texto largas (un mensaje con una ruta larga) para que quepan en esas 80. Sin él, el mensaje sale partido y un test que lo busca entero falla.
9. La cobertura dice qué líneas se **ejecutaron**, y la de la tabla se ejecutaba en muchos tests. Pero ninguno **comprobaba** su resultado con otra escala: el test de `--escala` buscaba `"alto: 1"`, que sale en el **resumen**, y el resumen sí usaba la escala buena. El test pasaba por la razón equivocada. Ahora compara las filas de la tabla celda a celda (`table_rows`): con la escala fija, el nivel de la fila no coincide.
10. Ninguno. `core/` no sabe que existe una CLI. Recibe líneas y escalas y devuelve filas, errores y series. `cli.py` decide de dónde salen las líneas y cómo se enseña el resultado. Es la separación de la semana 3 (lógica pura y un `main` delgado) y de la semana 8 (el paquete `core/`). Por eso la API de la semana 20 podrá ser otro punto de entrada sobre el mismo `core/`.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-15` muestra un commit por paso (tests, dependencias, esqueleto, `informe`, stdin y archivos, `--json`, `--escala`, `validar`, `-v`, consolas, versión, tests propios), sin cambiar los tests del bootcamp | 8 |
| `core/` intacto | `git diff main -- src/observatorio/core` está vacío; `cli.py` solo llama a funciones de `core` que ya existían | 8 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff check`, `ruff format --check`, `mypy`, `coverage report`, `observatorio --help`, `informe` con líneas, con stdin y con `-f`, y `validar`, en su máquina y en Docker | 6 |
| Rompe y explica | Ejecuta en vivo uno de los mutantes del paso 14 y explica qué test lo mata; quita `markup=False` y explica el fallo de `Sala [b]`; mueve `-v` detrás del comando y explica el error | 10 |
| Explica sus decisiones | Explica por qué `-v` va en el callback, por qué `fail` devuelve la excepción en lugar de lanzarla, y qué mutante mata su test del paso 15 | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 14

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| La aplicación | `cli.py` con `app`, el callback con `--version` y `-v`, sus constantes de dominio, `[project.scripts]` en `observatorio.cli:app` y `__main__.py` reducido a llamar a `app` | 15 |
| `informe` | Líneas, stdin, `-f`, `-j` y `-e`; la tabla de Rich con el color del nivel; el resumen; los códigos 0, 1 y 2; pasan `test_cli.py` y los tests modificados | 15 |
| `validar`, dependencias y versión | `validar` con `read_measurements`; `typer==0.27.3` y `rich==15.0.0` en `dependencies` y en `uv.lock`; versión `0.15.0`; `test_main.py` borrado | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_cli.py` con `CliRunner` y datos del dominio: éxito, errores, archivo que falta, stdin, `--json` y `validar`; al menos uno mata un mutante que sobrevive a los tests del bootcamp | 20 |
| Calidad | `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos; `docker compose run --build --rm app` en verde | 10 |
| Git y README | Rama `week-15` en `python-<nombre>-<apellido>`; README con `informe`, `validar`, `--escala` y `--help` | 10 |
| Pull request | Descripción con tests, `mypy`, `ruff`, la cobertura, la tabla de mutantes y las preguntas del paso 16 | 20 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 16 (próximamente) |
