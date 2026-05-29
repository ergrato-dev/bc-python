# ⚡ Semana 16: Concurrencia y AsyncIO

> **Fase 2 — Python Profesional** · _Junior → Mid-level_

---

## 🎯 Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- ✅ Explicar cómo funciona el event loop de asyncio y por qué no bloquea
- ✅ Escribir corutinas con `async def` / `await` y gestionarlas con Tasks
- ✅ Usar `asyncio.gather()` y `TaskGroup` para ejecutar múltiples corutinas concurrentemente
- ✅ Aplicar `ThreadPoolExecutor` y `ProcessPoolExecutor` del módulo `concurrent.futures`
- ✅ Elegir entre asyncio, threading y multiprocessing según el tipo de tarea
- ✅ Integrar código síncrono bloqueante dentro de un loop asyncio con `run_in_executor`

---

## 📚 Requisitos Previos

- ✅ Semana 15 completada (type system, dataclasses, Protocol)
- ✅ Funciones, closures y decoradores (semana 12)
- ✅ Manejo de excepciones (semana 11)
- ✅ Entidades Studio BC de la semana 15 (`Asset`, `Project`)

---

## 🗂️ Estructura de la Semana

```
week-16-concurrencia_y_asyncio/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/
│   ├── 01-event-loop.svg
│   ├── 02-concurrencia-vs-paralelismo.svg
│   └── 03-cuando-usar-que.svg
├── 1-teoria/
│   ├── 01-asyncio-fundamentos.md
│   ├── 02-async-patterns.md
│   ├── 03-concurrent-futures.md
│   ├── 04-threading-vs-asyncio.md
│   └── 05-asyncio-en-produccion.md
├── 2-ejercicios/
│   ├── 01-ejercicio-asyncio-basico/
│   ├── 02-ejercicio-gather-taskgroup/
│   ├── 03-ejercicio-concurrent-futures/
│   └── 04-ejercicio-pipeline-media/
├── 3-proyecto/
└── 4-recursos/ · 5-glosario/
```

---

## 📝 Contenidos

### 📚 Teoría

| # | Archivo | Tema | Diagrama |
|---|---------|------|----------|
| 1 | [01-asyncio-fundamentos.md](1-teoria/01-asyncio-fundamentos.md) | Event loop, corutinas, Tasks, Futures | `01-event-loop.svg` |
| 2 | [02-async-patterns.md](1-teoria/02-async-patterns.md) | gather, wait, as_completed, TaskGroup, timeout | — |
| 3 | [03-concurrent-futures.md](1-teoria/03-concurrent-futures.md) | ThreadPoolExecutor, ProcessPoolExecutor | `02-concurrencia-vs-paralelismo.svg` |
| 4 | [04-threading-vs-asyncio.md](1-teoria/04-threading-vs-asyncio.md) | Cuándo usar cada modelo | `03-cuando-usar-que.svg` |
| 5 | [05-asyncio-en-produccion.md](1-teoria/05-asyncio-en-produccion.md) | aiofiles, run_in_executor, semáforos | — |

### 💻 Ejercicios Guiados

| # | Ejercicio | Concepto |
|---|-----------|---------|
| 1 | [01-ejercicio-asyncio-basico](2-ejercicios/01-ejercicio-asyncio-basico/) | Corutinas, Tasks, `asyncio.run()` |
| 2 | [02-ejercicio-gather-taskgroup](2-ejercicios/02-ejercicio-gather-taskgroup/) | `gather`, `wait`, `as_completed`, `TaskGroup` |
| 3 | [03-ejercicio-concurrent-futures](2-ejercicios/03-ejercicio-concurrent-futures/) | `ThreadPoolExecutor`, `ProcessPoolExecutor` |
| 4 | [04-ejercicio-pipeline-media](2-ejercicios/04-ejercicio-pipeline-media/) | asyncio + executor para lotes de media |

### 🎯 Proyecto Semanal

[**Pipeline de Descarga y Procesamiento de Assets**](3-proyecto/README.md) — Sistema concurrente que descarga un lote de assets, los valida y los organiza en paralelo usando asyncio + ProcessPoolExecutor.

---

## ⏱️ Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría 01–02 (asyncio core + patterns) | 1.5h |
| 2 | Ejercicios 01–02 | 1.5h |
| 3 | Teoría 03–05 (futures, decisión, producción) | 1h |
| 4 | Ejercicios 03–04 | 1h |
| 5 | Proyecto semanal | 1h |

---

## 📌 Entregables

- [ ] Ejercicios 01–04 ejecutando sin errores
- [ ] Proyecto: pipeline que procesa mínimo 5 assets concurrentemente
- [ ] Sin llamadas bloqueantes (`time.sleep`, `requests.get`) dentro de corutinas

---

## 🔗 Navegación

← [Semana 15 — Python Moderno Avanzado](../week-15-python_moderno_avanzado/README.md) · [Semana 17 — CLI Profesional](../week-17-cli_profesional_typer_rich/README.md) →
