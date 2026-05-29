# Ejercicio 02 — gather, TaskGroup y timeout

## Objetivos

- Usar `asyncio.wait()` con `FIRST_COMPLETED` para tomar el primer resultado disponible
- Refactorizar `gather` a `TaskGroup` (Python 3.11+)
- Aplicar `asyncio.timeout()` para cancelar descargas lentas
- Usar `asyncio.as_completed()` para mostrar progreso en tiempo real

## Duración estimada

40 minutos

---

## Contexto

Studio BC lanza una descarga masiva de assets desde varios mirrors CDN. Necesita la versión más rápida de cada asset (múltiples servidores compiten), con timeout para no esperar indefinidamente, y progreso en tiempo real.

---

## Pasos

### Paso 1 — `asyncio.wait(FIRST_COMPLETED)`

Dado un asset disponible en 3 mirrors con delays distintos, descarga del **primero en responder** y cancela los demás.

### Paso 2 — Refactor a `TaskGroup`

Convierte la función `download_batch_gather` (usa `gather`) a `download_batch_taskgroup` (usa `TaskGroup`). Verifica que producen el mismo resultado.

### Paso 3 — Timeout global

Envuelve `download_batch_taskgroup` con `asyncio.timeout(5.0)`. Fuerza un asset con delay de 8s y maneja el `TimeoutError`.

### Paso 4 — Progreso con `as_completed`

Usa `asyncio.as_completed()` para imprimir cada asset en cuanto termine, en lugar de esperar a todos.

---

## Ejecutar

```bash
cd starter
uv run python main.py
```

## Criterios de éxito

- Paso 1: solo un mirror completa, los otros son cancelados
- Paso 2: mismo output, código más limpio con context manager
- Paso 3: `TimeoutError` capturado, assets anteriores ya procesados no se pierden
- Paso 4: los assets rápidos aparecen antes en consola
