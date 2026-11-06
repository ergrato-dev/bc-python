# Rúbrica de Evaluación — Semana 16: Concurrencia: hilos, procesos, GIL y free-threading

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 15 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | Un programa tarda `real 4.1 s`, `user 0.2 s`, `sys 0.1 s`. ¿Está limitado por E/S o por CPU? ¿Qué herramienta probarías primero y por qué? | 10 |
| 2 | En el ejercicio 01, cuatro hilos que duermen 0,5 s tardan 0,5 s. En el ejercicio 02, cuatro hilos que cuentan primos tardan lo mismo que uno. ¿Por qué la diferencia? | 10 |
| 3 | `counter += 1` desde cuatro hilos da el resultado correcto en Python 3.14 y pierde sumas en 3.14t. ¿Era correcto el código con GIL? ¿Qué tres condiciones hacen posible una carrera? | 10 |
| 4 | ¿Por qué `report_files` no necesita ningún `Lock`, si varios hilos ejecutan `report_file` a la vez? | 10 |
| 5 | `pool.map(lambda path: report_file(path), paths)` funciona con hilos y falla con procesos. ¿Qué error da y por qué? | 10 |
| 6 | ¿Por qué el código que lanza procesos va dentro de `if __name__ == "__main__":`? ¿Qué nombre tiene tu archivo en el proceso hijo? | 10 |
| 7 | `report_files` usa `pool.map` y no `as_completed`. ¿Qué cambiaría en la tabla de `lote` con `as_completed`? ¿Cuándo elegirías `as_completed`? | 10 |
| 8 | `report_file` captura `DataFileError`, pero no `Exception`. ¿Qué pasa con cada uno dentro de `report_files`, y por qué esa diferencia es una decisión de diseño? | 10 |
| 9 | En el paso 11, `lote --procesos` es más lento que `lote -t 1`. ¿Por qué? ¿Con qué archivos ganarían los procesos? ¿Y los hilos? | 10 |
| 10 | `test_report_files_runs_the_tasks_at_the_same_time` usa una `Barrier(3)` y no mide ningún tiempo. ¿Cómo demuestra que las tareas corren a la vez? ¿Para qué sirve su `timeout=5`? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Por **E/S**: de 4,1 s reales, solo 0,3 s son de CPU (`user` + `sys`). El resto, el programa espera. Probaría primero **hilos** (`ThreadPoolExecutor`): mientras un hilo espera, suelta el GIL y otro avanza, así que las esperas se solapan. Los procesos no ayudarían más, y costarían más. Si fueran miles de esperas de red, `asyncio` (semana 17).
2. Un hilo que **duerme** (o espera E/S) suelta el GIL, y los otros avanzan: las cuatro esperas se solapan. Un hilo que **calcula** necesita el GIL para ejecutar código Python, y solo hay uno: los cuatro se turnan, cada 5 ms, en un solo núcleo. El trabajo total es el mismo, y se hace de uno en uno.
3. **No** era correcto: tenía una carrera que el GIL hacía **rara**. Con GIL, Python casi nunca cambia de hilo entre la lectura y la escritura de ese bucle; sin GIL, los hilos ejecutan de verdad a la vez y se pisan constantemente. Las tres condiciones: datos **compartidos**, al menos un hilo que los **modifica**, y una operación **no atómica** (leer, sumar, escribir).
4. Porque no se cumple ninguna de las tres condiciones. Cada tarea recibe su `Path` como argumento, trabaja con variables locales y **devuelve** un `FileReport` nuevo e inmutable (`frozen=True`). Ningún hilo escribe en nada que otro use. Quien junta los resultados es el hilo principal, a través de `map`.
5. `PicklingError: Can't pickle local object ...` (o `... it's not found as __main__.<lambda>`). Para enviar una tarea a otro proceso, Python convierte la función en bytes con `pickle`, y una función viaja **por su nombre** para que el hijo la busque en su copia del módulo. Una `lambda` no tiene un nombre que se pueda buscar. Un hilo comparte la memoria y recibe la `lambda` tal cual.
6. Porque el hijo **importa tu archivo** para encontrar las funciones de las tareas, y todo lo que está a nivel de módulo se vuelve a ejecutar. Si ahí estuviera el código que crea procesos, cada hijo crearía los suyos; Python lo detecta y para con un `RuntimeError`. En el hijo, tu archivo se llama `__mp_main__`, así que el bloque `if __name__ == "__main__":` no se ejecuta.
7. Con `as_completed`, las filas saldrían en el orden en que **terminan** los archivos, distinto en cada ejecución, y no en el orden de los argumentos. Para recuperarlo habría que guardar a qué archivo corresponde cada `Future` y reordenar. Elegiría `as_completed` para enseñar progreso, o para usar los primeros resultados sin esperar al más lento.
8. Un `DataFileError` es un error **esperado** (falta un archivo, la cabecera está mal): `report_file` lo convierte en un `FileReport` con `error`, el lote sigue, y `lote` lo informa con código 1. Cualquier otra excepción es un **bug**: `report_file` no la captura, `map` la relanza en el hilo principal, y el programa falla con su traza. Capturar `Exception` haría pasar un bug por "archivo con error", y nadie lo vería.
9. Porque resumir un archivo de siete líneas cuesta menos que arrancar procesos y enviarles cada ruta y cada `FileReport` con `pickle`. Además, el disco apenas hace esperar: el sistema operativo tiene los archivos en memoria. Los procesos ganarían con archivos **grandes** (mucho cálculo por tarea); los hilos, con archivos que hacen **esperar** (un disco de red, descargas HTTP).
10. La barrera solo se abre cuando **tres** tareas esperan en ella a la vez. Si `report_files` las ejecutara una detrás de otra, la primera esperaría a otras dos que nunca llegan. Cuando el test pasa, no depende de ningún tiempo. El `timeout=5` solo sirve si falla: en lugar de colgarse para siempre, lanza `BrokenBarrierError` a los 5 s y el test falla con un mensaje.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-16` muestra un commit por paso (tests, esqueleto, `report_file`, hilos, procesos, `lote`, opciones, versión, tests propios), sin cambiar los tests del bootcamp | 8 |
| `core/` sin interfaz | `batch.py` no importa nada de Typer ni de Rich; `cli.py` solo llama a `report_files` y dibuja el resultado | 6 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff check`, `ruff format --check`, `mypy`, `coverage report`, `lote` con hilos, con `--procesos` y con un archivo que falta, en su máquina, en Docker y con el Python sin GIL | 8 |
| Rompe y explica | Cambia `pool.map` por un bucle con `as_completed` y explica qué test falla y por qué; quita `max_workers=workers` y explica qué test falla y por qué la barrera sigue abriéndose; envía una `lambda` con `--procesos` y explica el `PicklingError` | 10 |
| Explica sus medidas | Explica sus tiempos del paso 11 y del paso 12, y qué mutante mata su test del paso 14 | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 15

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| `FileReport` y `report_file` | *Dataclass* `frozen` y `slots`; medidas, medidas con valor y media correctas; `DataFileError` convertido en `error`; exportados desde `core` | 15 |
| `report_files` | Hilos por defecto con `thread_name_prefix`, procesos con `processes=True`, `max_workers=workers`, orden de entrada con `map`, otras excepciones relanzadas; pasan los tests de `test_batch.py` | 20 |
| El comando `lote` | `files_table`, errores a stderr, la línea del total, código 1 si falla algún archivo, `--trabajadores` con `min=1`, `--procesos` y `WORKERS = 4` | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_batch.py` con archivos del dominio: `report_file` con éxito y con error, orden, procesos, `lote` con la tabla y con un archivo que falta; al menos uno mata un mutante que sobrevive a los tests del bootcamp | 20 |
| Calidad | `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos; suite en verde en Docker y con 3.14.10t; versión `0.16.0` | 10 |
| Git y README | Rama `week-16` en `python-<nombre>-<apellido>`; README con `lote`, `-t` y `--procesos` | 5 |
| Pull request | Descripción con tests, `mypy`, `ruff`, cobertura, las tablas de tiempos y de mutantes, y las dos preguntas del paso 15 | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 17 (próximamente) |
