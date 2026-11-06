# Semana 16 — Concurrencia: hilos, procesos, GIL y free-threading

> Empieza la fase 3, Python profesional. Tu Observatorio ya tiene una CLI de verdad, pero lee los archivos de uno en uno: mientras espera al disco, no hace nada más. Esta semana aprendes a hacer varias cosas a la vez. Hilos para las esperas y procesos para el cálculo, el GIL que explica por qué, y el Python 3.14 sin GIL, que cambia las reglas. Lo aplicas en un comando nuevo, `lote`, que resume muchos archivos a la vez. Y lo mides, porque la concurrencia no siempre acelera: a veces solo complica.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Distinguir** concurrencia de paralelismo, y **medir** si un programa espera o calcula
- **Usar** hilos con `threading`: `start`, `join`, `Lock`, `Queue`, y **reconocer** una condición de carrera
- **Explicar** el GIL, y **elegir** entre hilos y procesos según el trabajo
- **Repartir** tareas con `concurrent.futures`: `map`, `submit`, `as_completed`, errores, esperas y cancelación
- **Ejecutar** tu código con el Python 3.14 *free-threaded* y **saber** qué cambia sin GIL
- **Probar** código concurrente sin depender de la suerte, y **medir** antes de decidir

---

## 📋 Prerrequisitos

- [Semana 15](../week-15-cli_con_typer_y_rich/README.md): CLI con Typer y Rich, y el cierre de la fase 2.
- El *pull request* `week-15` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-16-concurrencia_hilos_procesos_gil_y_free_threading/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 15 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Concurrencia y paralelismo](1-teoria/01-concurrencia-y-paralelismo.md) | Concurrencia y paralelismo, E/S frente a CPU, hilos y procesos, las herramientas de Python y la ley de Amdahl | 45 min |
| [02 · Hilos, carreras y locks](1-teoria/02-hilos-carreras-y-locks.md) | `threading.Thread`, condiciones de carrera, `Lock`, interbloqueos, `Queue`, `Event`, `Barrier` y tareas que no comparten nada | 50 min |
| [03 · El GIL, procesos y free-threading](1-teoria/03-el-gil-procesos-y-free-threading.md) | Qué es el GIL, procesos con `pickle` y el guardián `__main__`, métodos de arranque, Python 3.14t y subintérpretes | 50 min |
| [04 · concurrent.futures](1-teoria/04-concurrent-futures.md) | `Executor`, `submit` y `Future`, `map`, `as_completed`, errores, *timeouts*, cancelación y cuántos trabajadores | 50 min |
| [05 · Probar y medir código concurrente](1-teoria/05-probar-y-medir-codigo-concurrente.md) | Medir bien, tests frágiles, probar orden y simultaneidad sin tiempos, `monkeypatch` y procesos, y un adelanto de `asyncio` | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Hilos](2-practicas/ejercicio-01-hilos/README.md) | Esperas en paralelo, `start` y `join`, resultados por hilo, una carrera, su `Lock` y una `Queue` | 1 h 30 min |
| [02 · Procesos](2-practicas/ejercicio-02-procesos/README.md) | CPU con hilos y con procesos, el guardián `__main__`, `pickle`, memoria separada, `chunksize` y el método de arranque | 1 h 30 min |
| [03 · El GIL y free-threading](2-practicas/ejercicio-03-gil-y-free-threading/README.md) | El mismo programa con Python 3.14 y 3.14t: hilos que calculan, una carrera escondida y subintérpretes | 1 h |
| [04 · concurrent.futures](2-practicas/ejercicio-04-concurrent-futures/README.md) | `submit`, `map` frente a `as_completed`, errores, `timeout`, `wait`, cancelar y avisos | 1 h 30 min |

### Proyecto

Añades a tu Observatorio el módulo `core/batch.py` y el comando `lote`:

- `FileReport`, un resumen inmutable de un archivo: medidas, medidas con valor, media o error;
- `report_file`, que resume un archivo y convierte un `DataFileError` en un resultado;
- `report_files`, que reparte los archivos entre hilos o procesos y devuelve los resúmenes en orden;
- `observatorio lote ARCHIVOS... [-t N] [--procesos]`, con una tabla de Rich.

Después mides hilos frente a procesos, ejecutas la suite con el Python sin GIL y haces una prueba de mutación. La versión sube a `0.16.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Saber si tu programa espera o calcula | `time uv run observatorio lote ...`: si `user` + `sys` es mucho menor que `real`, espera |
| Ejecutar con el Python sin GIL sin tocar tu entorno | `UV_PROJECT_ENVIRONMENT=.venv-ft uv run --python 3.14.10t pytest` |
| Saber si el GIL está activo | `uv run python -c "import sys; print(sys._is_gil_enabled())"` |
| Encender el GIL en el Python sin GIL | `PYTHON_GIL=1 uv run --python 3.14.10t ...` |
| Medir una función pequeña | `uv run python -m timeit -s "from observatorio.core import parse_value" "parse_value('12,5')"` |
| Comprobar que un test concurrente es estable | `for i in $(seq 20); do uv run pytest -q tests/test_batch.py \| tail -1; done` |
| Ver los hilos en el registro | Añade `%(threadName)s` al `format` de `logging.basicConfig` |
| Saber cuántos núcleos tienes | `uv run python -c "import os; print(os.process_cpu_count())"` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-16` de `python-<nombre>-<apellido>` con:
   - `core/batch.py` con `FileReport`, `report_file` y `report_files`, exportados desde `core`;
   - el comando `lote` con `--trabajadores` y `--procesos`, y la constante `WORKERS`;
   - la versión `0.16.0` y al menos 6 tests propios en `tests/test_my_batch.py`.

   Todo en verde en tu máquina, en Docker y con el Python sin GIL, con `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos.
2. ✅ `README.md` del repositorio con el comando `lote`
3. ✅ Pull request `week-16` → `main` con:
   - tests, `mypy`, `ruff` y la cobertura;
   - las medidas de hilos, procesos y sin GIL, con tu explicación;
   - la tabla de mutantes;
   - por qué `report_files` no necesita ningún `Lock`.

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
uv run observatorio lote medidas.csv medidas.txt
UV_PROJECT_ENVIRONMENT=.venv-ft uv run --python 3.14.10t pytest -q
docker compose run --build --rm app
```

Lo que debes ver:

- los tests terminan en `passed` sin `failed`, al menos 503;
- ruff dice `All checks passed!` y `N files already formatted`;
- `mypy` dice `Success: no issues found`;
- `coverage report` termina sin `Coverage failure`;
- `--version` escribe `observatorio 0.16.0`;
- `lote` dibuja una fila por archivo y `archivos: 2 · con error: 0`;
- la suite también pasa con el Python sin GIL.

En los ejercicios, cada paso descomentado da la salida que muestra su README, con los tiempos de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 15](../week-15-cli_con_typer_y_rich/README.md) | **Semana 16** | [Semana 17](../week-17-asyncio_corrutinas_tareas_y_colas/README.md) |

← [Volver al índice de semanas](../README.md)
