# 03 · Comandos, callback y salida

⏱️ 45 min

## 🎯 Objetivos

- Organizar una CLI en comandos y grupos de comandos.
- Usar el callback para las opciones de toda la aplicación: `--version` y `-v`.
- Pasar datos del callback a los comandos con `typer.Context`.
- Terminar con el código correcto: `typer.Exit`, `typer.BadParameter` y las excepciones de tu paquete.
- Leer de stdin cuando no hay argumentos.

---

## 1. Comandos

Cada `@app.command()` registra una función como comando, con el nombre de la función:

```python
@app.command()
def informe(...) -> None:
    """Clasifica las medidas y escribe la tabla y el resumen."""


@app.command()
def validar(ruta: Path) -> None:
    """Comprueba un JSON de medidas con Pydantic sin escribir el informe."""
```

```
$ observatorio informe -f medidas.csv
$ observatorio validar medidas.json
```

Cada comando tiene su propia ayuda (`observatorio validar --help`) y sus propias opciones. Un comando es la unidad que haría `git commit` o `docker build`: un verbo o un sustantivo corto, en minúsculas.

Para cambiar el nombre: `@app.command("ver")`. Para agrupar comandos bajo otro, se monta una segunda aplicación:

```python
escala = typer.Typer(help="Consulta y comprueba la escala.")
app.add_typer(escala, name="escala")   # observatorio escala ver, observatorio escala comprobar
```

Tu proyecto tiene dos comandos y no necesita grupos. Si llegara a tener una docena, sí.

**Un comando o varios.** Si la aplicación tiene **un solo** comando y ningún callback, Typer lo ejecuta directamente, sin escribir su nombre. Al añadir el segundo, hay que escribirlo, y cambia la forma de llamar al primero. Un callback desde el principio evita la sorpresa.

## 2. El callback

`@app.callback()` registra la función del **grupo**. Typer la ejecuta antes que el comando, con las opciones que van **delante** del nombre del comando:

```python
@app.callback()
def main(
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Muestra el registro DEBUG en stderr.")
    ] = False,
    version: Annotated[
        bool,
        typer.Option("--version", "-V", callback=show_version, is_eager=True,
                     help="Muestra la versión y termina."),
    ] = False,
) -> None:
    """Observatorio de datos de mi dominio."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(name)s: %(message)s")
```

```
observatorio  -v  informe  -f medidas.csv
              ▲   ▲        ▲
              │   │        └─ opción de informe
              │   └─ comando
              └─ opción del callback: vale para todos los comandos
```

Son las opciones **globales**: `-v` sirve igual para `informe` que para `validar`. El *docstring* del callback es la descripción de la aplicación en `observatorio --help`.

El registro sigue la regla de la semana 14: solo el programa configura `logging`. Antes lo hacía tu `main`, y ahora lo hace el callback, que es el principio del programa.

## 3. `--version`, con `is_eager`

```python
def show_version(value: bool) -> None:
    if value:
        out.print(f"observatorio {__version__}")
        raise typer.Exit()
```

`callback=show_version` en la opción llama a esa función en cuanto Typer lee `--version`. Ojo: es otro *callback*, el de una opción, no el de la aplicación. `raise typer.Exit()` termina con código 0 **en ese momento**: ni el callback de la aplicación ni ningún comando se ejecutan. Por eso `observatorio --version` funciona sin comando.

`is_eager=True` hace que Typer procese esa opción antes que las demás. Si otra opción tuviera un valor imposible de convertir, `--version` respondería igual en lugar de dar el error. Hoy tu callback no tiene opciones que puedan fallar, así que no cambia nada visible. Se pone porque es la convención y porque protege el `--version` del futuro.

## 4. `typer.Context`

Si el callback prepara algo que los comandos necesitan, se lo pasa por el **contexto**:

```python
@app.callback()
def main(ctx: typer.Context, unidad: str = "µg/m³") -> None:
    ctx.obj = {"unidad": unidad}


@app.command()
def maximo(ctx: typer.Context) -> None:
    print(ctx.obj["unidad"])
```

Typer rellena los parámetros de tipo `typer.Context` y no los enseña en la ayuda. `ctx.obj` es libre: lo que el callback guarda, el comando lo lee. Tu proyecto no lo necesita, porque `-v` solo configura el registro y la escala va por comando. Lo verás en el ejercicio 02.

## 5. Códigos de salida

| Situación | Cómo | Código |
|---|---|---|
| Todo bien | La función termina sin más | `0` |
| `--help`, `--version` | `raise typer.Exit()` | `0` |
| Datos con errores: líneas inválidas | `raise typer.Exit(1)` | `1` |
| Llamada mal hecha, la detecta Typer: opción desconocida, tipo incorrecto | Lo hace Typer | `2` |
| Llamada mal hecha, la detectas tú: líneas **y** `--archivo` a la vez | `raise typer.BadParameter("usa líneas o --archivo, no los dos", param_hint="LINEAS")` | `2` |
| Archivo que no existe o no se puede leer | Tu `DataFileError`, convertido en un mensaje y `typer.Exit(2)` | `2` |

Son los códigos de tu `main` desde la semana 3. Lo nuevo es **cómo** se termina. Un comando de Typer no devuelve el código: lanza una excepción que Typer convierte en código. `typer.Exit(código)` termina en silencio, y `typer.BadParameter` escribe el mensaje con `Usage:` delante, como los errores de Typer.

Tu `DataFileError` no es de Typer. Si escapara del comando, Typer enseñaría una traza (con Rich, en un recuadro grande) y terminaría con código 1. El comando la captura y la convierte:

```python
def fail(message: str, code: int) -> typer.Exit:
    """Escribe "error: <mensaje>" en stderr y devuelve la salida con ese código."""
    err.print(f"error: {message}")
    return typer.Exit(code)


try:
    lines = source.lines()
except DataFileError as problem:
    raise fail(str(problem), 2) from problem
```

`fail` **devuelve** la excepción y el comando la lanza con `raise`. Así mypy y quien lee saben que ahí termina la función, igual que con un `raise` normal.

## 6. stdin

`informe` lee de tres sitios, en este orden:

```python
source: Source
if archivo is not None:
    source = open_file(archivo)
elif lineas:
    source = LinesSource(lineas)
else:
    source = LinesSource(list(sys.stdin))
```

Es el `Source` de la semana 10: el comando decide **de dónde** salen las líneas, y el resto no lo sabe. `observatorio informe < medidas.txt` y `cat medidas.txt | observatorio informe` llegan por la última rama. Si lo ejecutas sin nada, espera a que escribas: termina con `Ctrl+D`.

## 7. Confirmaciones

Para algo que no tiene vuelta atrás, una CLI pregunta:

```python
if not si:
    typer.confirm("¿Borrar los datos?", abort=True)
```

`typer.confirm` lee la respuesta de stdin. Si es "no", `abort=True` termina con `Aborted.` y código 1. Ofrece siempre una opción para saltarse la pregunta (`--si`, `--yes`), porque un *script* o el CI no tienen a nadie que conteste. Tu Observatorio no borra nada, así que no pregunta.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `No such option: -v` tras el comando | `-v` es del callback: va **antes** del comando | `observatorio -v informe ...` |
| `observatorio --version` pide un comando | Falta `raise typer.Exit()` en `show_version`, o el `callback=` de la opción | Termina dentro del callback de la opción |
| Una traza grande con `DataFileError` | La excepción escapó del comando | `try` / `except DataFileError` y `raise fail(...)` |
| `return 1` en un comando no cambia el código | Typer ignora lo que devuelve un comando | `raise typer.Exit(1)` |
| `Missing command.` | Escribiste solo `observatorio -v` | Falta el comando: `observatorio -v informe` |
| El comando espera para siempre | Lee stdin y nadie escribe | Pasa líneas, `-f` o una tubería |

---

## ✅ Qué debes saber al terminar

- [ ] Cómo se registran los comandos y cuándo hacen falta grupos con `add_typer`.
- [ ] Qué hace el callback y por qué sus opciones van antes del comando.
- [ ] Por qué `--version` necesita un callback propio con `typer.Exit()`.
- [ ] Para qué sirven `typer.Context` y `ctx.obj`.
- [ ] Qué código da cada situación y cómo se termina con él en Typer.
- [ ] Por qué el comando convierte `DataFileError` en un mensaje y un código.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Argumentos y opciones](02-argumentos-y-opciones.md) | **03 · Comandos, callback y salida** | [04 · Rich](04-rich.md) |
