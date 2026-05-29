# Glosario — Semana 17: CLI Profesional con Typer y Rich

| Término | Definición |
|---------|-----------|
| `typer.Argument` | Parámetro posicional de CLI. Requerido por defecto. Se pasa sin nombre en la línea de comandos: `cmd valor`. |
| `typer.Option` | Parámetro con nombre (flag). Tiene valor por defecto. Se pasa como `--flag valor` o `-f valor`. |
| `app.add_typer()` | Registra una sub-app como grupo de comandos. Permite organizar comandos en namespaces: `cmd grupo subcmd`. |
| `@app.callback()` | Decorador para la función que se ejecuta antes de cualquier subcomando. Ideal para configuración global. |
| autocompletion | Completado automático de valores en shell. Typer genera scripts de completado con `--install-completion`. |
| `typer.BadParameter` | Excepción que Typer convierte en mensaje de error de validación. Lanzar en callbacks de validación. |
| `typer.Exit` | Excepción para terminar la CLI con un código de salida específico. `raise typer.Exit(code=1)` para error. |
| `ctx.obj` | Objeto arbitrario almacenado en el contexto de Click/Typer. Ideal para pasar configuración global a subcomandos. |
| `CliRunner` | Clase de `typer.testing` que invoca comandos sin necesitar un proceso real. Captura stdout, stderr y exit_code. |
| `Console` | Clase principal de Rich. Reemplaza `print()` con soporte de markup, estilos y renderables complejos. |
| markup (Rich) | Sintaxis similar a BBCode para estilos en Rich: `[bold red]texto[/bold red]`, `[cyan]valor[/cyan]`. |
| `Table` | Renderable de Rich para datos tabulares con columnas con estilos, alineación y opciones de borde. |
| `Panel` | Renderable de Rich que enmarca contenido con un borde y título opcional. |
| `Progress` | Clase de Rich para barras de progreso. Soporta múltiples tareas y columnas personalizables. |
| `track()` | Shortcut de Rich para iterar un iterable mostrando barra de progreso automáticamente. |
| `Live` | Context manager de Rich que actualiza un renderable en el mismo espacio de terminal sin scroll. |
| `Layout` | Divide la terminal en secciones nombradas. Cada sección puede contener un renderable diferente. |
| `Textual App` | Clase base de aplicaciones TUI interactivas. Gestiona el ciclo de vida, eventos y re-render reactivo. |
| `compose()` | Método de Textual App que define el árbol de widgets de la interfaz. Equivalente a `render()` en React. |
| `on_mount()` | Evento de Textual que se dispara cuando los widgets ya están montados. Ideal para cargar datos iniciales. |
| `reactive` | Descriptor de Textual que notifica a `watch_<nombre>()` automáticamente cuando el valor cambia. |
| `BINDINGS` | Lista de tuplas `(key, action, description)` en Textual que vincula teclas a métodos `action_*`. |
| `query_one()` | Método de Textual para seleccionar un único widget por ID, clase CSS o tipo. |
| exit code | Entero que un proceso retorna al sistema operativo. 0 = éxito, != 0 = error. CLIs deben usarlo correctamente. |
