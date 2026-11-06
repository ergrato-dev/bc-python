# Rúbrica de Evaluación — Semana 17: asyncio: corrutinas, tareas y colas

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 16 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | Escribes `watch_file(path)` dentro de `watch_files`, sin `await`. ¿Qué pasa al ejecutar? ¿Qué devuelve esa llamada? | 10 |
| 2 | Cuatro tareas que esperan con `asyncio.sleep(0.5)` tardan 0,5 s; si esperan con `time.sleep(0.5)`, 2 s. Las dos versiones son `async def`. ¿Por qué la diferencia? | 10 |
| 3 | En el ejercicio 03, cien tareas suman uno a un contador y el resultado es 1, en un solo hilo. ¿Cómo es posible una carrera sin hilos? ¿Por qué `active += 1` en `watch_files` no necesita `Lock`? | 10 |
| 4 | `watch_files` usa `TaskGroup` y no `gather`. ¿Qué pasaría con cada uno si `watch_file` tuviera un bug y lanzara un `ValueError` en el segundo archivo? | 10 |
| 5 | Un archivo que falta no cancela las demás tareas de `watch_files`. ¿Por qué no, si `TaskGroup` cancela al resto cuando una falla? | 10 |
| 6 | ¿Qué hace `asyncio.timeout(tiempo)` cuando se agota el plazo de `vigilar --tiempo`? ¿Por qué el `except` de la CLI captura `TimeoutError` y no `CancelledError`? ¿Qué pasa si `tiempo` es `None`? | 10 |
| 7 | Una tarea captura `CancelledError` para cerrar una conexión y no la relanza. ¿Qué problemas causa? ¿Cómo deberías escribirlo? | 10 |
| 8 | `watch_file` lee el archivo con `await asyncio.to_thread(open_file(path).lines)`. ¿Por qué en otro hilo, si el resto es `asyncio`? ¿Qué falla si escribes `.lines()` con paréntesis? | 10 |
| 9 | `asyncio.run` está en `cli.py` y no en `core/live.py`. ¿Por qué? ¿Qué cambiará en la semana 20? | 10 |
| 10 | `test_replay_lets_other_tasks_run` espera `['A1', 'B1', 'A2', 'B2', 'A3', 'B3']` y no mide ningún tiempo. ¿Qué bug detecta, y por qué el resultado sale siempre en ese orden? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. La llamada **no** ejecuta nada: devuelve un objeto **corrutina**. Si nadie la espera, Python avisa con `RuntimeWarning: coroutine 'watch_file' was never awaited`, y el archivo no se lee. Con `TaskGroup`, `create_task` necesita esa corrutina, y es el grupo quien la espera; sin grupo y sin `await`, se pierde.
2. `asyncio.sleep` **cede el turno**: la tarea le dice al bucle "despiértame en 0,5 s", y el bucle pasa a la siguiente. Las cuatro esperas se solapan. `time.sleep` es una función normal que para el **hilo**, y el bucle vive en ese hilo: nadie puede avanzar hasta que termine. `async def` no hace asíncrono lo que hay dentro; solo los `await` de algo que de verdad espera.
3. Una tarea pierde el turno en cada `await`. `add` lee el valor, hace `await` y escribe: en el `await` entran las demás, leen el mismo 0 y todas escriben 1. Se cumplen las tres condiciones: datos compartidos, alguien que los modifica y una operación no atómica, que aquí significa "con un `await` en medio". `active += 1` y `peak = max(...)` no tienen ningún `await` entre medias: ninguna otra tarea puede ejecutarse ahí.
4. Con `TaskGroup`, el grupo **cancela** a las demás tareas, espera a que terminen y lanza un `ExceptionGroup` con el `ValueError`: el bug sale enseguida y nada queda corriendo. Con `gather` sin `return_exceptions`, el `ValueError` llega a quien espera, pero las demás tareas **siguen corriendo** sin que nadie las espere, escribiendo medidas en la terminal. Con `return_exceptions=True`, el error sería un resultado más en la lista, y el bug pasaría por un archivo.
5. Porque `watch_file` no deja escapar el `DataFileError`: lo captura y devuelve un `FileReport` con `error`. Para el grupo, esa tarea terminó **bien**. Es la misma decisión que `report_file` en la semana 16: un archivo que falta es un resultado esperado; una excepción que llega al grupo es un bug.
6. **Cancela** la tarea que espera dentro del bloque: a `watch_files`, y su `TaskGroup` cancela a cada tarea con una `CancelledError` en su `asyncio.sleep`. Al salir del bloque, `timeout` convierte esa cancelación en un `TimeoutError`, y eso es lo que sale de `asyncio.run`. Con `None`, `timeout` no pone límite: por eso la misma línea sirve con y sin `--tiempo`.
7. La tarea sigue como si nada: quien la canceló cree que paró, y no. `timeout` no puede convertir la cancelación en `TimeoutError` y la espera se alarga; un `TaskGroup` se queda esperando a una tarea que debía haber terminado. Hay que limpiar en un `finally`, o en el `except asyncio.CancelledError:` y después `raise`.
8. Leer un archivo es una llamada **que bloquea**: mientras el disco responde, el hilo se para, y con él el bucle y todas las estaciones. `to_thread` la ejecuta en un hilo aparte y te da algo que esperar con `await`; el bucle sigue libre. Con `.lines()`, el archivo se lee **antes**, en el bucle, bloqueándolo, y `to_thread` recibe una lista: el hilo intenta llamarla y falla con `TypeError: 'list' object is not callable`.
9. Porque `core` no debe decidir cuándo empieza ni cuánto dura el bucle: solo ofrece corrutinas. `asyncio.run` crea un bucle nuevo, y no se puede llamar dentro de otro bucle. En la semana 20, FastAPI ya tendrá su bucle en marcha y llamará a `watch_files` con `await`. Si `core` tuviera un `asyncio.run`, fallaría con `RuntimeError: asyncio.run() cannot be called from a running event loop`.
10. Detecta que `replay` **no cede el turno**: con `time.sleep`, o sin ninguna espera, la tarea A daría sus tres medidas antes de que B empezara (`A1, A2, A3, B1...`). Sale siempre en el mismo orden porque el bucle reparte los turnos de forma fija: las tareas listas se ejecutan en el orden en que quedaron listas, y `asyncio.sleep(0)` pone a cada una al final de la fila. No hay un sistema operativo interrumpiendo cuando quiere.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-17` muestra un commit por paso (tests, esqueleto, `from_series`, `replay`, `watch_file`, `watch_files`, `vigilar`, opciones, versión, tests propios), sin cambiar los tests del bootcamp | 8 |
| Refactors sin cambiar el comportamiento | `FileReport.from_series` y `show_reports` en commits propios, con los tests de la semana 16 en verde antes y después | 6 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff check`, `ruff format --check`, `mypy`, `coverage report`, `vigilar` con varios archivos, con uno que falta, con `--tiempo` y con Ctrl+C, en su máquina y en Docker | 8 |
| Rompe y explica | Cambia `asyncio.sleep` por `time.sleep` y explica qué test falla; saca el `await` del bloque del semáforo y explica el `assert 6 == 1`; quita el `to_thread` y explica qué test lo nota y por qué la salida no cambia | 10 |
| Explica sus medidas | Explica sus tiempos del paso 12 con las cuentas, y qué mutante sobrevivió y cómo lo mata su test | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 16

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| `replay` y `watch_file` | `replay` es un generador asíncrono con `iter_measurements` y `asyncio.sleep` antes de cada medida; `watch_file` lee con `to_thread`, convierte `DataFileError` en `error`, avisa con `on_reading` y resume con `FileReport.from_series` | 20 |
| `watch_files` | `TaskGroup`, `Semaphore(limit)`, resultados en el orden de entrada, otros errores en un `ExceptionGroup`; sin `asyncio.run`, Typer ni Rich en `live.py`; pasan los tests de `test_live.py` | 15 |
| El comando `vigilar` | `show_reading` con el nivel y su color, `show_reports` compartido con `lote`, `--intervalo` con `min=0`, `--limite` con `min=1`, `--tiempo` con `asyncio.timeout` y código 1, `INTERVAL = 0.5` | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_live.py` con datos del dominio: `replay`, `watch_file` con éxito y con error, orden de `watch_files`, `vigilar` con `CliRunner`; al menos uno mata el mutante que sobrevive a los tests del bootcamp | 20 |
| Calidad | `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos; `live.py` al 100 %; `docker compose run --build --rm app` en verde; versión `0.17.0` | 10 |
| Git y README | Rama `week-17` en `python-<nombre>-<apellido>`; README con `vigilar`, `-i`, `-l` y `--tiempo` | 5 |
| Pull request | Descripción con tests, `mypy`, `ruff`, cobertura, las tablas de tiempos y de mutantes, y las dos preguntas del paso 15 | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 18 (próximamente) |
