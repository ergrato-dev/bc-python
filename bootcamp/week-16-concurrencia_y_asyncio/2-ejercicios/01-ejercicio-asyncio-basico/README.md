# Ejercicio 01 — AsyncIO Básico

## Objetivos

- Escribir corutinas con `async def` y `await`
- Crear Tasks con `asyncio.create_task()`
- Medir la diferencia de tiempo entre ejecución secuencial y concurrente

## Duración estimada

30 minutos

---

## Contexto

Studio BC necesita un sistema que verifique el estado de varios assets de un proyecto antes de iniciar la edición. Cada verificación hace una llamada de red simulada que tarda entre 1 y 3 segundos.

---

## Pasos

### Paso 1 — Versión secuencial (punto de partida)

Ejecuta el código marcado como `# PASO 1` y observa el tiempo total.

### Paso 2 — Versión con `await` concurrente

Convierte `check_asset` en una corutina async. Usa `asyncio.create_task()` para las 4 llamadas y mide de nuevo el tiempo.

### Paso 3 — Versión con `asyncio.gather()`

Reescribe usando `asyncio.gather(*tasks)`. Compara con el paso 2.

### Paso 4 — Manejo de errores

Agrega `return_exceptions=True` y fuerza que `check_asset("audio_02.wav")` lance un `ValueError`. Muestra los errores sin que el programa se detenga.

---

## Ejecutar

```bash
cd starter
uv run python main.py
```

## Criterios de éxito

- Paso 1: tiempo ≈ suma de todos los delays
- Paso 2 y 3: tiempo ≈ delay máximo
- Paso 4: el error aparece en resultados sin detener los demás tasks
