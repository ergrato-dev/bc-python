# Semana 15 — Proyecto de fase: CLI con Typer y Rich

> Desde la semana 3, tu Observatorio lee sus opciones con un `match` sobre `sys.argv` que no ha dejado de crecer: `-h`, `-V`, `-f`, `-j`, `-v`. El orden importa, la ayuda es un texto que mantienes a mano y cada opción nueva multiplica los casos. Esta semana lo sustituyes por una CLI de verdad. **Typer** construye el analizador a partir de las firmas de tus funciones, y **Rich** dibuja el informe como una tabla con colores. `core/` no se toca: es la prueba de que la arquitectura de la fase 2 funciona. Y cierras la fase con una pregunta incómoda: tus tests tienen un 99 % de cobertura, pero ¿detectarían un bug? La respondes metiéndolos a propósito.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Construir** una CLI con Typer: argumentos y opciones con `Annotated`, varios comandos y un callback con opciones globales
- **Terminar** con el código de salida correcto: `typer.Exit`, `typer.BadParameter` y las excepciones de tu paquete
- **Escribir** en la terminal con Rich: tablas, estilos, dos consolas, y saber qué cambia sin terminal
- **Proteger** la salida de los datos del usuario que Rich interpretaría como marcas
- **Probar** una CLI con `CliRunner`, y **comprobar** con una prueba de mutación que los tests detectan bugs
- **Explicar** por qué cambiar la interfaz no obliga a tocar la lógica

---

## 📋 Prerrequisitos

- [Semana 14](../week-14-testing_profesional_fixtures_parametrize_mocks_hypothesis_cobertura_y_logging/README.md): testing profesional, cobertura y logging.
- El *pull request* `week-14` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-15-cli_con_typer_y_rich/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 4 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 14 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · De `argv` a Typer](1-teoria/01-de-argv-a-typer.md) | Las partes de una línea de comandos y sus convenciones, `argparse`, Click y Typer, la firma como especificación y `[project.scripts]` | 45 min |
| [02 · Argumentos y opciones](1-teoria/02-argumentos-y-opciones.md) | `Annotated`, argumento u opción, los tipos que convierte Typer, la ayuda, variables de entorno y qué valida cada uno | 50 min |
| [03 · Comandos, callback y salida](1-teoria/03-comandos-callback-y-salida.md) | Comandos y grupos, el callback, `--version` con `is_eager`, `Context`, códigos de salida, stdin y confirmaciones | 45 min |
| [04 · Rich](1-teoria/04-rich.md) | `Console`, tablas, dos consolas, terminal o tubería, `markup`, `highlight`, `soft_wrap` y Rich con `logging` | 50 min |
| [05 · Probar la CLI y cerrar la fase](1-teoria/05-probar-la-cli-y-cerrar-la-fase.md) | `CliRunner`, probar el color y otro proceso, la prueba de mutación y el repaso de la fase 2 | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Argumentos y opciones](2-practicas/ejercicio-01-argumentos-y-opciones/README.md) | Siete comandos: tipos, valores por defecto, `Annotated`, listas, `Path`, `Enum` y códigos de salida | 1 h 30 min |
| [02 · Comandos y contexto](2-practicas/ejercicio-02-comandos-y-contexto/README.md) | Uno o varios comandos, el callback, `ctx.obj`, `--version`, `add_typer`, stdin y `confirm` | 1 h |
| [03 · Rich](2-practicas/ejercicio-03-rich/README.md) | Estilos, los corchetes de tus datos, una tabla, un panel, stderr y terminal frente a tubería | 1 h 30 min |
| [04 · Probar la CLI](2-practicas/ejercicio-04-probar-la-cli/README.md) | `CliRunner` con stdout, stderr, códigos, stdin y archivos, y un bug que tus tests no ven | 1 h 30 min |

### Proyecto

Sustituyes el `main` de tu Observatorio por `cli.py`, una aplicación Typer con:

- el callback, con `--version` y `-v`;
- el comando `informe`: líneas, stdin, `-f`, `-j` y la nueva `-e` (la escala de un JSON), con una tabla de Rich;
- el comando `validar`, que comprueba un JSON de medidas con Pydantic.

`__main__.py` queda en tres líneas, `test_main.py` deja paso a `test_cli.py`, y `typer` y `rich` entran en las dependencias. La versión sube a `0.15.0`. Cierras con una prueba de mutación a mano sobre tus propios tests. **Es el único entregable de la semana.**
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
| Ver la ayuda de un comando | `uv run observatorio informe --help` |
| Llamar a la CLI sin el ejecutable | `uv run python -m observatorio informe -f medidas.csv` |
| Guardar el informe sin los errores | `uv run observatorio informe -f medidas.csv > informe.txt` |
| Ver el informe como lo ven los tests | `uv run observatorio informe -f medidas.csv \| cat`: sin colores y con 80 columnas |
| Forzar los colores en una tubería | `FORCE_COLOR=1 uv run observatorio informe -f medidas.csv \| less -R` |
| Ver qué excepción tumbó un comando en un test | `print(result.exception)` dentro del test, con `uv run pytest -s` |
| Probar si un test protege una línea | Cambia la línea, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>` |
| Instalar tu CLI para usarla en cualquier carpeta | `uv tool install .` (y `uv tool uninstall observatorio` para quitarla) |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-15` de `python-<nombre>-<apellido>` con:
   - `typer==0.27.3` y `rich==15.0.0` en `dependencies`, y `[project.scripts]` apuntando a `observatorio.cli:app`;
   - `cli.py` con el callback, `informe` y `validar`, y `__main__.py` reducido a llamar a `app`;
   - `tests/test_main.py` borrado y los tests nuevos del bootcamp en verde;
   - la versión `0.15.0` y al menos 6 tests propios en `tests/test_my_cli.py`.

   Todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos.
2. ✅ `README.md` del repositorio con los comandos nuevos
3. ✅ Pull request `week-15` → `main` con:
   - tests, `mypy`, `ruff` y la cobertura;
   - la tabla de mutantes del paso 14;
   - por qué `core/` no cambió y por qué la CLI usa `Console(markup=False)`.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
uv run ruff check && uv run ruff format --check
uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
uv run observatorio --version
uv run observatorio informe -f medidas.csv
docker compose run --build --rm app
```

Lo que debes ver:

- los tests terminan en `passed` sin `failed`, al menos 466;
- ruff dice `All checks passed!` y `N files already formatted`;
- `mypy` dice `Success: no issues found`;
- `coverage report` termina sin `Coverage failure`;
- `--version` escribe `observatorio 0.15.0`;
- `informe` dibuja la tabla de medidas y el resumen.

En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 14](../week-14-testing_profesional_fixtures_parametrize_mocks_hypothesis_cobertura_y_logging/README.md) | **Semana 15** | Semana 16 (próximamente) |

← [Volver al índice de semanas](../README.md)
