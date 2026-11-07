# Semana 17 — asyncio: corrutinas, tareas y colas

> En la semana 16 esperabas cuatro cosas a la vez con cuatro hilos. ¿Y si fueran mil? Cada hilo cuesta memoria y trabajo al sistema operativo, y casi todo su tiempo lo pasa esperando. `asyncio` lleva miles de esperas en **un solo hilo**: cada tarea avisa con `await` cuando va a esperar, y el bucle de eventos aprovecha para atender a otra. Esta semana aprendes corrutinas, tareas, `TaskGroup`, plazos, cancelación y colas. Lo aplicas en `vigilar`, un comando que sigue varias estaciones a la vez y escribe cada medida en cuanto llega. Es la base de las semanas 18 (HTTP) y 20 (FastAPI).

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Escribir** corrutinas con `async def` y `await`, y **explicar** cómo reparte los turnos el bucle de eventos
- **Lanzar** tareas a la vez con `create_task`, `gather` y `TaskGroup`, y **capturar** sus errores con `except*`
- **Poner** plazos con `asyncio.timeout` y **cancelar** tareas sin perder la limpieza
- **Coordinar** tareas con `Semaphore`, `Lock`, `Queue` y `Event`, y **evitar** lo que bloquea el bucle
- **Recorrer** generadores asíncronos con `async for` y **escribir** gestores con `async with`
- **Probar** corrutinas con pytest sin plugins y sin depender del tiempo

---

## 📋 Prerrequisitos

- [Semana 16](../week-16-concurrencia_hilos_procesos_gil_y_free_threading/README.md): hilos, procesos, GIL y free-threading.
- El *pull request* `week-16` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-17-asyncio_corrutinas_tareas_y_colas/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 16 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Corrutinas y el bucle de eventos](1-teoria/01-corrutinas-y-el-bucle-de-eventos.md) | Concurrencia cooperativa, `async def` y `await`, el bucle de eventos, `asyncio.run`, el color de las funciones y cuándo no ayuda | 45 min |
| [02 · Tareas, gather y TaskGroup](1-teoria/02-tareas-gather-y-taskgroup.md) | `create_task`, `gather` y sus errores, `TaskGroup` y la concurrencia estructurada, `ExceptionGroup` y `except*`, tareas perdidas | 50 min |
| [03 · Tiempo límite y cancelación](1-teoria/03-tiempo-limite-y-cancelacion.md) | `timeout`, cómo llega una cancelación, limpiar sin tragársela, `as_completed`, `wait`, `shield` y Ctrl+C | 45 min |
| [04 · Coordinar tareas y no bloquear el bucle](1-teoria/04-coordinar-tareas-y-no-bloquear-el-bucle.md) | `Semaphore`, carreras sin hilos y `Lock`, `Queue` con contrapresión y `shutdown`, lo que bloquea, `to_thread` y el modo debug | 50 min |
| [05 · Iteradores, gestores y probar código asíncrono](1-teoria/05-iteradores-gestores-y-probar-codigo-asincrono.md) | Generadores asíncronos y `async for`, `async with`, tipos, tests con `asyncio.run`, probar sin tiempos y los plugins de pytest | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Corrutinas y el bucle](2-practicas/ejercicio-01-corrutinas-y-el-bucle/README.md) | Corrutinas, `await`, tareas, `gather`, turnos en un hilo, una llamada que bloquea y `to_thread` | 1 h 30 min |
| [02 · Tareas, errores y cancelación](2-practicas/ejercicio-02-tareas-errores-y-cancelacion/README.md) | `TaskGroup`, `except*`, `return_exceptions`, `timeout`, `cancel`, `as_completed` y una tarea perdida | 1 h 30 min |
| [03 · Coordinar tareas](2-practicas/ejercicio-03-coordinar-tareas/README.md) | `Semaphore`, una carrera sin hilos y su `Lock`, `Queue` con uno y varios consumidores, `Event` y `shutdown` | 1 h 30 min |
| [04 · Iteradores y gestores asíncronos](2-practicas/ejercicio-04-iteradores-y-gestores-asincronos/README.md) | `async for`, comprensiones, `aclose`, `async with`, `asynccontextmanager`, el modo debug y probar una corrutina | 1 h |

### Proyecto

Añades a tu Observatorio el módulo `core/live.py` y el comando `vigilar`:

- `replay`, un generador asíncrono que da las medidas de unas líneas con una pausa entre ellas;
- `watch_file`, que lee un archivo sin bloquear el bucle, avisa de cada medida y lo resume;
- `watch_files`, que vigila varios archivos a la vez con un `TaskGroup` y un `Semaphore`;
- `observatorio vigilar ARCHIVOS... [-i S] [-l N] [--tiempo SEGUNDOS]`, que escribe cada medida en cuanto llega y termina con la tabla de `lote`.

Por el camino, dos refactors: `FileReport.from_series` y `show_reports`, compartidos con la semana 16. Después mides, y haces una prueba de mutación. La versión sube a `0.17.0`. **Es el único entregable de la semana.**
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
| Ver las medidas sin esperar | `uv run observatorio vigilar -i 0 medidas.csv medidas.txt` |
| Probar el plazo | `uv run observatorio vigilar -i 1 --tiempo 2.5 medidas.csv` |
| Encontrar lo que bloquea el bucle | `PYTHONASYNCIODEBUG=1 uv run observatorio vigilar ...`: avisa de cada paso que tarda más de 0,1 s |
| Una consola donde `await` funciona | `uv run python -m asyncio`: puedes escribir `await asyncio.sleep(1)` directamente |
| Ver las tareas de un programa en marcha | `uv run python -m asyncio ps <PID>` (nuevo en 3.14), desde otra terminal |
| Saber si estás dentro de un bucle | `asyncio.get_running_loop()` lanza `RuntimeError` si no lo estás |
| Comprobar que un test asíncrono es estable | `for i in $(seq 20); do uv run pytest -q tests/test_live.py \| tail -1; done` |
| Ver los avisos de ruff sobre `asyncio` | `uv run ruff check --select ASYNC` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-17` de `python-<nombre>-<apellido>` con:
   - `core/live.py` con `replay`, `watch_file` y `watch_files`, exportados desde `core`, y `FileReport.from_series` en `batch.py`;
   - el comando `vigilar` con `--intervalo`, `--limite` y `--tiempo`, la constante `INTERVAL` y `show_reports` compartido con `lote`;
   - la versión `0.17.0` y al menos 6 tests propios en `tests/test_my_live.py`.

   Todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos.
2. ✅ `README.md` del repositorio con el comando `vigilar`
3. ✅ Pull request `week-17` → `main` con:
   - tests, `mypy`, `ruff` y la cobertura;
   - la tabla de tiempos, con tus cuentas;
   - la tabla de mutantes y el test que mata al superviviente;
   - por qué `asyncio.run` está en `cli.py` y por qué `watch_files` usa `TaskGroup`.

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
uv run observatorio vigilar -i 0.2 medidas.csv medidas.txt
docker compose run --build --rm app
```

Lo que debes ver:

- los tests terminan en `passed` sin `failed`, al menos 546;
- ruff dice `All checks passed!` y `N files already formatted`;
- `mypy` dice `Success: no issues found`;
- `coverage report` termina sin `Coverage failure`;
- `--version` escribe `observatorio 0.17.0`;
- `vigilar` escribe las medidas de los dos archivos intercaladas, una cada 0,2 s, y después la tabla y `archivos: 2 · con error: 0`.

En los ejercicios, cada paso descomentado da la salida que muestra su README, con los tiempos de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 16](../week-16-concurrencia_hilos_procesos_gil_y_free_threading/README.md) | **Semana 17** | [Semana 18](../week-18-http_con_httpx_reintentos_secretos_y_env/README.md) |

← [Volver al índice de semanas](../README.md)
