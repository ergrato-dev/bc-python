# Semana 17: CLI Profesional con Typer y Rich

> **Fase 2 — Python Profesional** · _Junior → Mid-level_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Construir CLIs con subcomandos, opciones tipadas y autocompletion usando **Typer**
- Crear salidas de terminal ricas: tablas, progress bars, panels y markdown con **Rich**
- Implementar TUIs interactivas con **Textual** (widgets, layouts, eventos)
- Elegir entre Click y Typer según el proyecto y migrar código existente
- Testear CLIs con `typer.testing.CliRunner` de forma reproducible

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [Typer — Fundamentos](1-teoria/01-typer-fundamentos.md) | Comandos, opciones, argumentos, callbacks, autocompletion |
| 02 | [Rich — Output](1-teoria/02-rich-output.md) | Console, tables, panels, syntax highlighting, Markdown |
| 03 | [Rich — Live y Layout](1-teoria/03-rich-live-layout.md) | Progress bars, Live display, Layout, Columns |
| 04 | [Textual — TUIs](1-teoria/04-textual-tui.md) | App, Widgets, layouts, eventos, CSS reactivo |
| 05 | [Testing CLIs](1-teoria/05-testing-clis.md) | CliRunner, fixtures, testing subcomandos y errores |

---

## Estructura de la Semana

```
week-17-cli_profesional_typer_rich/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-ejercicio-typer-basico/
│   ├── 02-ejercicio-rich-output/
│   ├── 03-ejercicio-subcomandos/
│   └── 04-ejercicio-tui-textual/
├── 3-proyecto/
│   ├── README.md           # Studio BC Asset CLI
│   ├── starter/
│   └── solution/           # Solo instructores
├── 4-recursos/
│   ├── ebooks-free/
│   ├── videografia/
│   └── webgrafia/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: Typer fundamentos + Rich output | 1.5h |
| 2 | Teoría: Rich Live + Textual + Testing CLIs | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Entregables

- [ ] Ejercicio 01: CLI básica con Typer (comandos y opciones tipadas)
- [ ] Ejercicio 02: Salida rich con tablas, panels y markdown
- [ ] Ejercicio 03: CLI con subcomandos y estado compartido
- [ ] Ejercicio 04: TUI básica con Textual
- [ ] Proyecto: `bc-studio-cli` — herramienta interna de Studio BC

---

## Navegación

← [Semana 16](../week-16-concurrencia_y_asyncio/README.md) · [Semana 18](../week-18-gestion_datos_polars/README.md) →
