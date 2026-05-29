# Ejercicio 01 — Typer Básico

## Objetivos

- Crear un app Typer con comandos y opciones tipadas
- Diferenciar `Argument` vs `Option` en la práctica
- Añadir validación con callbacks
- Verificar que `--help` se genera automáticamente

## Duración estimada

30 minutos

---

## Contexto

Studio BC quiere un script para gestionar una lista de proyectos en memoria. Cada proyecto tiene un ID, un cliente y un presupuesto.

---

## Pasos

### Paso 1 — Comando `create`

Implementa `create(project_id, client, budget)`:
- `project_id`: `Argument` requerido
- `client`: `Option` requerido (sin default)
- `budget`: `Option` con default `0.0`, mínimo `0.0`
- Valida que `project_id` sea alfanumérico con guiones (usa callback)
- Imprime: `Created: {project_id} for {client} (${budget:.2f})`

### Paso 2 — Comando `list`

Imprime los proyectos creados. Usa una variable global `PROJECTS: list[dict]`.
Añade `--count / --no-count` para mostrar el total al final.

### Paso 3 — Comando `delete`

Usa `typer.confirm()` antes de eliminar. Si el usuario cancela, imprime `Cancelled.` y retorna.

### Paso 4 — Verificación de --help

Ejecuta `uv run python main.py --help`, `uv run python main.py create --help` y verifica que los descriptions son claros.

---

## Ejecutar

```bash
cd starter
uv run python main.py create reel-2025 --client "Estudio Norte" --budget 5000
uv run python main.py list
uv run python main.py delete reel-2025
```

## Criterios de éxito

- `--help` muestra descriptions en todos los comandos y opciones
- Budget negativo es rechazado con error claro
- project_id inválido (con espacios) es rechazado
- `confirm()` funciona: "y" elimina, "n" cancela
