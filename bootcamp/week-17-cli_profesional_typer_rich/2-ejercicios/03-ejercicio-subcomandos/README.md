# Ejercicio 03 — Subcomandos y Estado Compartido

## Objetivos

- Estructurar una CLI con múltiples sub-apps usando `app.add_typer()`
- Pasar configuración global entre subcomandos con `ctx.obj`
- Leer variables de entorno con `envvar=`
- Integrar Rich en salidas de todos los subcomandos de forma consistente

## Duración estimada

45 minutos

---

## Contexto

Studio BC necesita `bc-studio-cli` con tres grupos de comandos:
- `assets`: list, add, remove
- `projects`: list, create
- `config`: show

Todos los comandos deben respetar `--verbose` global y la URL de API leída desde `BC_API_URL`.

---

## Pasos

### Paso 1 — Estructura de sub-apps

Crea `assets_app`, `projects_app` y `config_app` como `typer.Typer()` y agrégalos al `app` raíz con `add_typer()`.

### Paso 2 — Callback global con `ctx.obj`

Implementa `@app.callback()` que:
- Acepta `--verbose / --no-verbose` y `--api-url` (o `BC_API_URL` env var)
- Almacena un dataclass `Config` en `ctx.obj`

### Paso 3 — Comandos con acceso al contexto

Cada comando recibe `ctx: typer.Context` y accede a `ctx.obj` para leer `Config`.
Si `verbose=True`, imprime detalles adicionales.

### Paso 4 — Rich consistente

Usa `console.print()` en todos los comandos. Errores a `err_console`.
Tablas para listados, panels para resúmenes.

---

## Ejecutar

```bash
cd starter
uv run python main.py --help
uv run python main.py assets list
uv run python main.py --verbose projects create reel-2025
BC_API_URL=https://staging.studio.bc uv run python main.py config show
```

## Criterios de éxito

- `bc-studio-cli --help` muestra los 3 grupos de comandos
- `--verbose` activa output adicional en todos los subcomandos
- `BC_API_URL` se lee desde el entorno correctamente
- Salida usa Rich en todos los comandos (no print desnudo)
