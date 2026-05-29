# Ejercicio 04 — Pipeline de Media con Semáforos

## Objetivos

- Construir un pipeline async completo con múltiples etapas
- Limitar la concurrencia con `asyncio.Semaphore`
- Rastrear el estado de cada tarea con un dataclass
- Implementar retry con backoff exponencial

## Duración estimada

50 minutos

---

## Contexto

Studio BC necesita un pipeline que procese un lote de assets de video: descarga, transcodificación simulada, y subida a almacenamiento. El sistema debe procesar máximo 3 assets a la vez para no saturar la red, y reintentar automáticamente si una etapa falla.

---

## Pasos

### Paso 1 — Dataclass de estado

Completa el dataclass `AssetJob` con los campos: `name`, `url`, `status` (Literal), `error`, `retries`. Añade un método `mark_failed(reason)`.

### Paso 2 — Etapas del pipeline

Implementa las 3 etapas async:
- `download_stage(job)` — simula descarga (1.5s), puede fallar aleatoriamente
- `transcode_stage(job)` — simula transcodificación (1.0s)
- `upload_stage(job)` — simula subida (0.8s), puede fallar aleatoriamente

### Paso 3 — Semáforo de concurrencia

Implementa `process_job(sem, job)` que adquiere el semáforo y ejecuta las 3 etapas en secuencia. Maneja errores por etapa.

### Paso 4 — Retry con backoff

Añade `process_job_with_retry(sem, job, max_retries=2)`. Si una etapa falla, espera `1 * 2^attempt` segundos y reintenta el job completo (reseteando el estado).

---

## Ejecutar

```bash
cd starter
uv run python main.py
```

## Criterios de éxito

- El semáforo limita a `MAX_CONCURRENT` jobs activos simultáneamente
- Los jobs fallidos se reintentan hasta `max_retries` veces
- El resumen final muestra done/failed/retried correctamente
- El tiempo total es menor que la suma de todos los tiempos individuales
