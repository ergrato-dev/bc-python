# Ejercicio 01 — DataFrames Básico

## Objetivos
- Crear un DataFrame desde dict y desde CSV
- Usar `select()`, `filter()` y `sort()`
- Verificar schema, shape y head

## Duración estimada
30 minutos

## Pasos

### Paso 1 — Cargar y explorar
Lee `timesheets.csv` con `pl.read_csv(try_parse_dates=True)`.
Imprime: `schema`, `shape`, `head(3)` y `describe()`.

### Paso 2 — Selección
Selecciona solo `project_id`, `employee` y `hours`. Añade una columna calculada `revenue_usd` (hours × 120).

### Paso 3 — Filtrado
Filtra las filas donde `hours > 6` Y `billable == True`. ¿Cuántas filas quedan?

### Paso 4 — Sort y unique
Ordena por `hours` descendente. Luego obtén los valores únicos de `employee`.

## Ejecutar
```bash
cd starter
uv run python main.py
```
