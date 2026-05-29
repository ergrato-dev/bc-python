# Ejercicio 02 — Expresiones Encadenadas

## Objetivos
- Usar `pl.when().then().otherwise()` para columnas condicionales
- Encadenar transformaciones de strings y fechas
- Combinar múltiples expresiones en un `with_columns()`

## Duración estimada
35 minutos

## Pasos

### Paso 1 — `pl.when()` para clasificación
Añade columna `shift_type`:
- `hours > 8` → "overtime"
- `hours >= 6` → "full"
- resto → "partial"

### Paso 2 — Transformaciones de strings
Añade `employee_upper` (mayúsculas) y `project_short` (primeras 4 letras del project_id).

### Paso 3 — Transformaciones de fechas
Añade `week_number`, `month` y `weekday_name` (lunes=0).

### Paso 4 — Pipeline completo
Combina todos los `with_columns()` anteriores en uno solo y añade
`billable_revenue = hours * 120 si billable else 0`.

## Ejecutar
```bash
cd starter
uv run python main.py
```
