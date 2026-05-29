# Rúbrica de Evaluación — Semana 17: CLI Profesional con Typer y Rich

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica la diferencia entre `Argument` y `Option` en Typer, y cuándo usar cada uno | 8 |
| Describe qué componentes de Rich son síncronos vs cuáles requieren `Live` context | 7 |
| Distingue cuándo construir una TUI con Textual vs una CLI estándar con Typer | 8 |
| Explica por qué `CliRunner.invoke` es preferible a llamar la función directamente en tests | 7 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Implementa subcomandos con `app.add_typer()` y estado compartido via `ctx.obj` | 10 |
| Usa Rich `Table`, `Panel` y `Progress` correctamente en salida de CLI | 10 |
| Crea una TUI mínima funcional con Textual: al menos 2 widgets y 1 evento | 10 |
| Testea al menos 3 comandos con `CliRunner`: éxito, error, y output verification | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| `bc-studio-cli` tiene al menos 3 subcomandos funcionales (assets, projects, report) | 10 |
| Salida de los comandos usa Rich de forma consistente (no `print()` desnudo) | 8 |
| `--help` auto-generado es informativo: descriptions en todos los comandos y opciones | 7 |
| `mypy --strict` pasa sin errores | 5 |
