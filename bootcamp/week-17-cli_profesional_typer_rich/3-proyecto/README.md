# Proyecto Semana 17 — bc-studio-cli

## Descripción

Construir `bc-studio-cli`, la herramienta interna de Studio BC para gestionar proyectos y assets desde terminal. La CLI debe ser profesional: subcomandos organizados, salida rich consistente, variables de entorno, autocompletion y tests con CliRunner.

---

## Comandos requeridos

```
bc-studio-cli
├── assets
│   ├── list    [project-id] [--type video|audio|image]
│   ├── add     <project-id> <name> --type <type> [--size <size>]
│   └── remove  <project-id> <name>
├── projects
│   ├── list
│   ├── create  <project-id> --client <name> [--budget <float>]
│   └── status  <project-id>
└── report
    └── generate <project-id> [--format table|json|markdown]
```

---

## Estructura del proyecto

```
starter/
├── src/
│   ├── __init__.py
│   ├── main.py         — app raíz + callback global
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── assets.py   — assets_app
│   │   ├── projects.py — projects_app
│   │   └── report.py   — report_app
│   ├── models.py       — dataclasses: Config, Asset, Project
│   └── store.py        — estado en memoria (o JSON si completas el bonus)
├── tests/
│   ├── test_assets.py
│   ├── test_projects.py
│   └── test_report.py
└── pyproject.toml
```

---

## Requerimientos técnicos

### `src/models.py`

```python
@dataclass
class Config:
    verbose: bool
    api_url: str

@dataclass
class Asset:
    name: str
    type: Literal["video", "audio", "image"]
    project_id: str
    size: str = "—"

@dataclass
class Project:
    id: str
    client: str
    budget: float = 0.0
```

### Salida con Rich

- Listados: `Table` con columnas de color
- Resúmenes: `Panel` con borde y título
- Operaciones largas (report generate): `Progress` o `track()`
- Errores: `err_console.print(...)` + `raise typer.Exit(code=1)`

### Tests (mínimo 6)

- `test_assets_list_empty` — exit_code 0, output contiene "No assets"
- `test_assets_add_success` — exit_code 0, asset aparece en list
- `test_projects_create_invalid_id` — exit_code != 0
- `test_report_generate_table` — exit_code 0, output contiene nombres de columnas
- `test_verbose_flag` — output adicional aparece con `--verbose`
- `test_env_api_url` — URL custom aparece en config show

---

## Rúbrica (30 pts)

| Criterio | Puntos |
|----------|--------|
| 3 subcomandos funcionales con salida Rich | 10 |
| `--help` informativo en todos los comandos | 5 |
| `ctx.obj` con Config (verbose + api_url + envvar) | 5 |
| 6+ tests con CliRunner pasando | 7 |
| mypy --strict pasa sin errores | 3 |

## Bonus (+5 pts)

Persistir el store en `~/.bc-studio/store.json` con `json` + `pathlib`.

---

## Ejecutar

```bash
cd starter
uv run python -m src.main --help
uv run python -m src.main assets list
uv run python -m src.main projects create reel-2025 --client "Estudio Norte" --budget 5000
uv run python -m src.main report generate reel-2025 --format markdown

# Tests
uv run pytest tests/ -v
```
