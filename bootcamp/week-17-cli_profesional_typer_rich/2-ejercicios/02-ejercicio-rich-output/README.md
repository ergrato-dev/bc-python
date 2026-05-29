# Ejercicio 02 — Rich Output

## Objetivos

- Reemplazar `print()` y `typer.secho()` con `rich.Console`
- Construir tablas y panels para datos de studio
- Mostrar progress bar durante una operación simulada
- Renderizar un resumen en Markdown

## Duración estimada

35 minutos

---

## Contexto

Studio BC necesita que sus herramientas CLI produzcan salidas visuales claras y consistentes — no texto plano. Migrarás una CLI existente para usar Rich en todos sus outputs.

---

## Pasos

### Paso 1 — `Console` y markup

Sustituye todos los `print()` del archivo por `console.print()` con markup:
- Éxitos en `[green bold]`
- Advertencias en `[yellow]`
- Errores en `[red bold]` hacia `err_console`

### Paso 2 — `Table` para assets

Implementa `show_assets_table(assets)` que muestre una tabla con columnas:
`Name`, `Type`, `Size`, `Status` (con íconos de color).

### Paso 3 — `Panel` para resúmenes

Implementa `show_summary_panel(stats)` que muestre un panel con borde `cyan`:
proyecto, total assets, ok, failed, tiempo.

### Paso 4 — `Progress` para operación larga

Implementa `run_with_progress(assets)` usando `track()` o `Progress`.
Simula 0.3s por asset con `time.sleep`.

### Paso 5 — `Markdown` para reporte

Implementa `show_markdown_report(assets)` que genere y renderice un Markdown
con tabla de assets y resumen final.

---

## Ejecutar

```bash
cd starter
uv run python main.py
```

## Criterios de éxito

- Sin ningún `print()` desnudo en el código final
- La tabla tiene colores en la columna Status
- El panel se ve enmarcado con título
- El progress muestra barra animada
