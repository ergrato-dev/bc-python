# Ejercicio 04 — I/O de Datos

## Objetivos
- Leer CSV con opciones avanzadas (null_values, schema)
- Escribir y leer Parquet
- Exportar a JSON
- Usar `scan_csv` en lugar de `read_csv` y medir la diferencia

## Duración estimada
30 minutos

## Pasos

### Paso 1 — Leer CSV con opciones
Lee `timesheets.csv` con: `null_values=[""]`, `try_parse_dates=True` y schema explícito para hours como Float32.

### Paso 2 — Escribir y leer Parquet
Escribe el DataFrame a `output/timesheets.parquet` con `compression="zstd"`.
Léelo de nuevo y verifica que el schema se preservó.

### Paso 3 — Exportar a JSON
Escribe el resumen (group_by project_id) a `output/summary.json`.
Léelo de nuevo con `pl.read_json()`.

### Paso 4 — scan_csv vs read_csv
Implementa la misma transformación con `scan_csv` + `collect()`.
Compara con `read_csv`. ¿El resultado es idéntico?

## Ejecutar
```bash
cd starter
uv run python main.py
```
