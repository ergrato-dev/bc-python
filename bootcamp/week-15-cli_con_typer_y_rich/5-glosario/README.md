# Glosario — Semana 15

| Término | Definición |
|---|---|
| **`add_typer`** | `app.add_typer(otra, name="escala")`: cuelga una aplicación Typer de otra, para tener comandos agrupados como `observatorio escala ver` |
| **`Annotated`** | `Annotated[T, extra]`: el tipo `T` con información añadida. mypy ve `T`; Typer lee el `extra` (`typer.Argument(...)`, `typer.Option(...)`) |
| **Argumento** | Dato de una línea de comandos que se reconoce por su **posición**, sin nombre: `"Norte;12,5"` en `observatorio informe "Norte;12,5"` |
| **`argv`** | La lista de textos con la que se llamó al programa: `sys.argv`. Typer la lee y la analiza por ti |
| **`BadParameter`** | `raise typer.BadParameter("mensaje")`: error de uso que detectas tú. Typer escribe el mensaje con `Usage:` y termina con código 2 |
| **Callback (de la aplicación)** | Función con `@app.callback()` que Typer ejecuta antes de cada comando, con las opciones globales. Su *docstring* describe la aplicación |
| **Callback (de una opción)** | Función que Typer llama al leer una opción: `typer.Option(callback=show_version)`. Es lo que hace funcionar `--version` |
| **CLI** | *Command line interface*: un programa que se usa escribiendo comandos en la terminal |
| **Click** | La biblioteca de CLI sobre la que está construido Typer. En Typer 0.27 va incluida dentro, sin ser una dependencia aparte |
| **`CliRunner`** | Clase de `typer.testing` que ejecuta una aplicación dentro de un test y devuelve un `Result` con `exit_code`, `stdout`, `stderr` y `exception` |
| **Código de salida** | Número con el que termina un programa: 0 bien, 1 resultado "no" o datos con errores, 2 uso incorrecto. Lo lee la shell con `$?` |
| **Comando** | Lo que quieres hacer en un programa que hace varias cosas: `informe`, `validar`. En Typer, una función con `@app.command()` |
| **`Console`** | El objeto de Rich que escribe en la terminal: `Console()` en stdout, `Console(stderr=True)` en stderr |
| **`Context`** | `typer.Context`: parámetro especial que Typer rellena. `ctx.obj` lleva datos del callback a los comandos |
| ***Eager*** | `is_eager=True`: una opción que Typer procesa antes que las demás, como `--version` |
| **`escape`** | `rich.markup.escape(texto)`: protege los corchetes de un texto para que Rich no los tome por marcas |
| **`exit_code`** | En un `Result` de `CliRunner`, el código con el que terminó el comando |
| **`FORCE_COLOR`** | Variable de entorno que pide colores aunque la salida no vaya a una terminal |
| ***Flag*** | Opción booleana, sin valor: `-v`. Con `"--color/--sin-color"` se declara también la forma de apagarla |
| **Marcas (*markup*)** | La sintaxis de estilos de Rich entre corchetes: `[bold red]alto[/]`. Peligrosa con datos del usuario: `Console(markup=False)` la desactiva |
| **`metavar`** | El nombre con el que un argumento aparece en `Usage:`: `metavar="LINEAS"` |
| **Mutante** | Copia del código con un cambio pequeño hecho a propósito, como `>` por `>=`. Si ningún test falla, el mutante **sobrevive** y falta un test |
| **`no_args_is_help`** | Opción de `typer.Typer(...)`: sin argumentos, la aplicación enseña su ayuda en vez de quejarse |
| **`NO_COLOR`** | Variable de entorno que pide que no haya colores, aunque la salida vaya a una terminal |
| **Opción** | Dato de una línea de comandos con nombre: `-f medidas.csv` o `--archivo medidas.csv`. Opcional y en cualquier orden |
| **Opción global** | Opción del callback, que vale para todos los comandos y se escribe antes de ellos: `observatorio -v informe` |
| **`prog_name`** | `app(prog_name="observatorio")`: el nombre del programa en la ayuda, para que `python -m observatorio` no diga `python -m` |
| **`[project.scripts]`** | Tabla de `pyproject.toml` que crea un comando de la terminal: `observatorio = "observatorio.cli:app"` |
| **Prueba de mutación** | Meter bugs a propósito (mutantes) para comprobar si los tests los detectan. Dice qué se comprobó, no solo qué se ejecutó |
| **Rich** | Biblioteca para escribir en la terminal con estilos, tablas, paneles y colores. Typer la usa para su ayuda y sus errores |
| **`soft_wrap`** | Opción de `Console`: con `True`, Rich no corta las líneas largas al ancho de la terminal (80 sin terminal) |
| **stdin** | La entrada estándar. `observatorio informe < medidas.txt` le pasa un archivo; en un test, `invoke(..., input="...")` |
| **`Table`** | Tabla de Rich: `add_column` y `add_row`, con el ancho de cada columna calculado y alineación por columna |
| **`Text`** | Texto de Rich con su propio estilo: `Text("alto", style="bold red")`. Funciona aunque las marcas estén desactivadas |
| **Typer** | Biblioteca que construye una CLI a partir de las firmas de las funciones y sus anotaciones de tipo |
| **`typer.Exit`** | `raise typer.Exit(código)`: termina el comando con ese código, sin mensaje. Un comando de Typer no devuelve su código con `return` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
