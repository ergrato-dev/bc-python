# Semana 07 — `pathlib`, JSON, CSV, excepciones y context managers

> Un programa que solo lee de la terminal lo olvida todo al cerrarse. Esta semana tu código abre archivos, los lee, guarda resultados y, sobre todo, falla bien: un archivo que no existe, una tilde mal codificada o un JSON roto dejan de ser un *traceback* y pasan a ser un mensaje claro. El Observatorio lee sus medidas de un CSV como el que exporta cualquier hoja de cálculo y guarda un resumen en JSON que otro programa puede leer.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Construir** y **desmontar** rutas con `pathlib.Path` y **explicar** desde dónde se resuelve una ruta relativa
- **Leer** y **escribir** archivos de texto con `with`, el modo correcto y `encoding="utf-8"`
- **Capturar** excepciones con `try`, `except`, `else` y `finally`, y **decidir** qué capturar y dónde
- **Lanzar** excepciones propias y **traducir** errores de bajo nivel con `raise ... from`
- **Escribir** context managers con `@contextmanager` y **usar** `suppress`
- **Leer** y **escribir** CSV con el módulo `csv` y JSON con el módulo `json`, **validando** cabecera y forma

---

## 📋 Prerrequisitos

- [Semana 06](../week-06-algoritmos_big_o_collections_e_itertools/README.md): Big-O, `collections` e `itertools`.
- El *pull request* `week-06` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-07-pathlib_json_csv_excepciones_y_context_managers/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 6 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · `pathlib` y archivos](1-teoria/01-pathlib-y-archivos.md) | Rutas como objetos, relativas y absolutas, `with`, formas de leer, `encoding`, modos de apertura | 50 min |
| [02 · Excepciones](1-teoria/02-excepciones.md) | *Tracebacks*, `try`/`except`/`else`/`finally`, `raise`, `raise ... from`, excepciones propias, qué capturar y dónde | 55 min |
| [03 · Context managers](1-teoria/03-context-managers.md) | Qué hace `with`, varios recursos a la vez, `@contextmanager`, `suppress` | 40 min |
| [04 · CSV](1-teoria/04-csv.md) | El formato y el `;` en español, `csv.reader`, la cabecera, `DictReader`, `csv.writer` | 45 min |
| [05 · JSON](1-teoria/05-json.md) | Tipos de JSON y de Python, `dumps`/`loads`, `dump`/`load`, `JSONDecodeError`, CSV o JSON | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Archivos y rutas](2-practicas/ejercicio-01-archivos-y-rutas/README.md) | Piezas de una ruta, carpeta de trabajo, escribir y leer con `with`, modos, `glob` | 1 h 30 min |
| [02 · Excepciones](2-practicas/ejercicio-02-excepciones/README.md) | `try`/`except`, `else` y `finally`, una excepción que sube, `raise ... from`, familias | 1 h 30 min |
| [03 · CSV y JSON](2-practicas/ejercicio-03-csv-y-json/README.md) | `csv.writer` y `csv.reader`, `DictReader`, ida y vuelta por JSON, `JSONDecodeError` | 1 h 30 min |
| [04 · Context managers](2-practicas/ejercicio-04-context-managers/README.md) | `with` ante un error, `@contextmanager`, un cronómetro, dos archivos y `suppress` | 1 h |

### Proyecto

El Observatorio lee sus medidas de un archivo de texto o CSV con `-f` y guarda un resumen en JSON con `-j`. Todos los fallos de archivo salen como una excepción propia, `DataFileError`, que `main` convierte en un mensaje y el código de salida 2. **Es el único entregable de la semana.**
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
| Leer un archivo pequeño en una línea | `path.read_text(encoding="utf-8").splitlines()` |
| Ver desde dónde se resuelven tus rutas | `python -c "from pathlib import Path; print(Path.cwd())"` |
| Revisar o embellecer un JSON desde la terminal | `uv run python -m json.tool resumen.json` |
| Ver un CSV como tabla en la terminal | `column -s ';' -t < medidas.csv` (Linux y macOS) |
| Saber qué excepción capturar | Provoca el error en el REPL y copia el tipo de la última línea del *traceback* |
| Encontrar la familia de una excepción | `FileNotFoundError.__mro__` |
| Borrar sin error si no existe | `path.unlink(missing_ok=True)` |
| Un test que escribe archivos | Pide `tmp_path` como argumento: pytest te da una carpeta temporal |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-07` de `python-<nombre>-<apellido>` con `storage.py`, tu `main` ampliado con `-f` y `-j`, tu `medidas.csv` con al menos 12 filas y al menos 6 tests propios, todo en verde en tu máquina y en Docker, y `mypy` sin errores
2. ✅ `README.md` del repositorio con los comandos nuevos, un `resumen.json` de ejemplo y la tabla de errores que reconoce tu programa
3. ✅ Pull request `week-07` → `main` con tests, `mypy`, `resumen.json` y dos casos de error explicados

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
uv run --with mypy==2.4.1 mypy src tests
uv run observatorio -f medidas.csv -j resumen.json; echo "código: $?"
uv run observatorio -f no-existe.csv; echo "código: $?"
docker compose run --build --rm app
```

Los tests terminan en `passed` sin `failed`, `mypy` dice `Success: no issues found` y el informe termina con `resumen guardado en resumen.json`. El archivo que no existe da `error: no existe el archivo no-existe.csv` y `código: 2`, sin *traceback*. En los ejercicios, cada paso descomentado da la salida que muestra su README (en los tiempos, la misma proporción entre filas).

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 06](../week-06-algoritmos_big_o_collections_e_itertools/README.md) | **Semana 07** | Semana 08 (próximamente) |

← [Volver al índice de semanas](../README.md)
