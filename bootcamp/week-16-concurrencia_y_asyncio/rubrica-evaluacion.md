# 📋 Rúbrica de Evaluación — Semana 16: Concurrencia y AsyncIO

> **Puntaje total: 100 puntos** · Mínimo para aprobar: **70 puntos**

---

## 1. Conocimiento 🧠 — 30 puntos

### 1.1 Event loop y modelo de concurrencia (10 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica por qué asyncio es concurrente pero no paralelo | 4 |
| Describe qué ocurre cuando una corutina hace `await` | 3 |
| Diferencia entre una corutina, un Task y un Future | 3 |

### 1.2 Patrones async (10 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica la diferencia entre `gather` y `TaskGroup` en manejo de errores | 4 |
| Sabe cuándo usar `as_completed` en lugar de `gather` | 3 |
| Puede configurar un timeout con `asyncio.timeout()` | 3 |

### 1.3 concurrent.futures y decisión de modelo (10 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica cuándo usar `ThreadPoolExecutor` vs `ProcessPoolExecutor` | 4 |
| Describe el rol del GIL y por qué threads no aceleran código CPU-bound | 3 |
| Sabe cómo integrar código bloqueante en asyncio con `run_in_executor` | 3 |

---

## 2. Desempeño 💪 — 40 puntos

### 2.1 Ejercicios completados (20 pts)

| Ejercicio | Puntos | Criterio |
|-----------|--------|---------|
| 01-asyncio-basico | 5 | Corutinas con `async def`, tasks con `create_task` |
| 02-gather-taskgroup | 5 | `gather` y `TaskGroup` usados, cancelación manejada |
| 03-concurrent-futures | 5 | Executor correcto según tipo de tarea (I/O vs CPU) |
| 04-pipeline-media | 5 | Pipeline combina asyncio + executor sin código bloqueante en el loop |

### 2.2 Calidad del código (20 pts)

| Indicador | Puntos |
|-----------|--------|
| Sin `time.sleep()` ni código bloqueante dentro de corutinas | 6 |
| Manejo de excepciones en contexto async | 5 |
| Tipos anotados (incluye `Coroutine`, `Task`, `Awaitable`) | 5 |
| Recursos cerrados correctamente (`async with`, `executor.shutdown`) | 4 |

---

## 3. Producto 📦 — 30 puntos

### 3.1 Proyecto: Pipeline concurrente de assets (30 pts)

| Indicador | Puntos |
|-----------|--------|
| N assets descargados/simulados en paralelo con `gather` o `TaskGroup` | 8 |
| `asyncio.Semaphore` para limitar concurrencia máxima | 6 |
| Procesamiento CPU-bound delegado a `ProcessPoolExecutor` vía `run_in_executor` | 6 |
| Assets fallidos no abortan el pipeline completo | 6 |
| Reporte final con tiempo total, assets OK y assets fallidos | 4 |

---

## Criterios de Aprobación

- ✅ Mínimo **21/30** en Conocimiento
- ✅ Mínimo **28/40** en Desempeño
- ✅ Mínimo **21/30** en Producto
- ✅ El pipeline procesa al menos 5 assets concurrentemente
- ✅ Sin llamadas bloqueantes dentro del event loop
