# Ejercicio 04 — TUI con Textual

## Objetivos

- Construir una TUI mínima con Textual
- Usar `DataTable`, `Input`, `Button` y `Label`
- Manejar eventos de botón e input
- Añadir keyboard bindings con `BINDINGS`

## Duración estimada

45 minutos

---

## Contexto

Studio BC quiere una TUI para visualizar y filtrar assets de un proyecto sin salir de la terminal. La aplicación debe mostrar una tabla de assets y permitir filtrarlos por nombre.

---

## Pasos

### Paso 1 — Layout básico

Implementa `compose()` con:
- `Header(show_clock=True)`
- Un `Input` para filtrar
- Un `DataTable` para los assets
- `Footer()` con los bindings visibles

### Paso 2 — Poblar la DataTable

En `on_mount()`, añade las columnas y filas de `ASSETS` a la tabla.

### Paso 3 — Filtrar en tiempo real

Implementa `on_input_changed()`: cuando el usuario escribe en el Input, filtra `ASSETS` y recarga la tabla (clear + add_rows).

### Paso 4 — Bindings de teclado

Añade:
- `("q", "quit", "Quit")`
- `("r", "reload", "Reload")` — recarga todos los assets sin filtro
- `("d", "delete_selected", "Delete")` — elimina la fila seleccionada (requiere `table.move_cursor()`)

---

## Ejecutar

```bash
cd starter
uv run python main.py
```

## Criterios de éxito

- La tabla se muestra al arrancar con todos los assets
- Escribir en el Input filtra la tabla en tiempo real
- `q` cierra la app
- `r` recarga todos los assets (borra el filtro)
