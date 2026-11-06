# Ejercicio 02 — Comandos y contexto

⏱️ 1 h · Teoría previa: [03](../../1-teoria/03-comandos-callback-y-salida.md)

## Objetivo

Organizar una CLI con varios comandos:

- qué cambia entre una aplicación con un comando y otra con dos;
- el **callback**: opciones de toda la aplicación, que se escriben antes del comando;
- `typer.Context` para pasar datos del callback a los comandos;
- `--version` con `is_eager`;
- un grupo de comandos dentro de otro, con `add_typer`;
- argumentos o stdin;
- pedir confirmación antes de algo que no tiene vuelta atrás.

Tu proyecto tiene un callback con `--version` y `-v`, y dos comandos: `informe` y `validar`. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-15-cli_con_typer_y_rich/2-practicas/ejercicio-02-comandos-y-contexto/starter
uv run python main.py
```

```
RuntimeError: Could not get a command for this Typer instance
```

Antes de esa línea sale una traza dentro de un recuadro. Es lo esperado: una aplicación Typer sin comandos no tiene nada que ejecutar.

## Pasos

### 1. Un solo comando

Descomenta el **PASO 1** y ejecuta:

```bash
uv run python main.py
uv run python main.py listar
```

```
Norte: 12.5
Sur: 8.0
Oriente: 55.1
```

```
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Got unexpected extra argument(s) (listar)                                    │
╰──────────────────────────────────────────────────────────────────────────────╯
```

Con **un** comando, Typer lo ejecuta directamente: `main.py` **es** `listar`, y la palabra `listar` sobra. Es lo que hacía `typer.run(función)`.

### 2. Un segundo comando

Descomenta el **PASO 2** y ejecuta:

```bash
uv run python main.py
uv run python main.py listar
```

```
 Usage: main.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ listar  Escribe cada estación con su valor.                                  │
│ media   Escribe la media de todas las estaciones.                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

```
Norte: 12.5
Sur: 8.0
Oriente: 55.1
```

Con dos comandos, la aplicación pasa a ser un **grupo**: el primer argumento elige el comando. Sin argumentos, `no_args_is_help=True` enseña la ayuda (y termina con código `2`, porque faltaba el comando).

Si tu aplicación tendrá varios comandos, decláralos desde el principio con un callback (paso 3). Si no, añadir el segundo comando cambia cómo se llama al primero.

### 3. El callback

Descomenta el **PASO 3** y ejecuta:

```bash
uv run python main.py --help
uv run python main.py maximo
uv run python main.py --unidad ppm maximo
uv run python main.py maximo --unidad ppm
```

```
 Ejercicio 02 · Comandos, callback y contexto.

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --unidad         <str>  La unidad de las medidas. [default: µg/m³]           │
│ --version                                                                    │
│ --help                  Show this message and exit.                          │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ listar  Escribe cada estación con su valor.                                  │
│ media   Escribe la media de todas las estaciones.                            │
│ maximo  Escribe la estación con el valor más alto, en la unidad del          │
│         callback.                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

```
[callback] unidad=µg/m³
máximo: Oriente 55.1 µg/m³
[callback] unidad=ppm
máximo: Oriente 55.1 ppm
```

```
[callback] unidad=µg/m³
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ No such option: --unidad                                                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

`@app.callback()` es la función del grupo. Typer la ejecuta **antes** de cada comando, con las opciones escritas **antes** del nombre del comando. Su *docstring* es la descripción de la aplicación. `--unidad` es del grupo, no de `maximo`: escrita detrás del comando, no existe.

Para pasar datos al comando, el callback los guarda en `ctx.obj`. `ctx: typer.Context` es un parámetro especial: Typer lo rellena y no aparece en la ayuda. `maximo` lee `ctx.obj["unidad"]`.

Ahora `--version`:

```bash
uv run python main.py --version
uv run python main.py --version maximo
```

```
ejercicio-02 0.2.0
ejercicio-02 0.2.0
```

`callback=mostrar_version` llama a esa función en cuanto Typer lee la opción, y `typer.Exit()` termina ahí: ni el callback principal ni `maximo` llegan a ejecutarse. `is_eager=True` la procesa antes que las demás opciones. Si otra opción trajera un valor imposible de convertir (`--n abc` en una opción `int`), `--version` respondería igual; sin `is_eager`, ganaría el error.

### 4. Un grupo dentro del grupo

Descomenta el **PASO 4** y ejecuta:

```bash
uv run python main.py escala ver
uv run python main.py escala comprobar 10 50
uv run python main.py escala comprobar 50 10; echo $?
```

```
[callback] unidad=µg/m³
bajo < 10 ≤ medio ≤ 50 < alto
[callback] unidad=µg/m³
umbrales correctos
[callback] unidad=µg/m³
umbrales imposibles: 50.0 ≥ 10.0
1
```

`escala` es otra aplicación Typer, colgada de la principal con `app.add_typer(escala, name="escala")`. Así funcionan `git remote add` o `docker compose up`: un comando que agrupa otros. `@escala.command("ver")` da al comando un nombre distinto del de la función, `escala_ver`, que no puede llamarse `ver` a secas sin chocar con otros.

### 5. Argumentos o stdin

Descomenta el **PASO 5** y ejecuta:

```bash
uv run python main.py leer a b c
printf "Norte;1\n\nSur;2\n" | uv run python main.py leer
```

```
[callback] unidad=µg/m³
3 líneas de argumentos
[callback] unidad=µg/m³
2 líneas de stdin
```

`list[str] | None = None` hace los argumentos opcionales. Sin ellos, el comando lee `sys.stdin`, como el `informe` de tu proyecto. Si lo ejecutas sin argumentos y sin tubería, espera a que escribas: termina con `Ctrl+D` (en Windows, `Ctrl+Z` e `Intro`).

### 6. Pedir confirmación

Descomenta el **PASO 6** y ejecuta. Contesta `n` la primera vez e `y` la segunda:

```bash
uv run python main.py borrar Sur
uv run python main.py borrar Sur
uv run python main.py borrar Sur --si
```

```
[callback] unidad=µg/m³
¿Borrar Sur? [y/N]: n
Aborted.
[callback] unidad=µg/m³
¿Borrar Sur? [y/N]: y
borrada: Sur; quedan 2
[callback] unidad=µg/m³
borrada: Sur; quedan 2
```

`typer.confirm(..., abort=True)` pregunta y, si la respuesta es "no", termina con `Aborted.` y código `1`. La `N` mayúscula indica la respuesta por defecto (pulsar `Intro`). `--si` se salta la pregunta: un *script* o el CI no tienen a nadie que conteste.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `Got unexpected extra argument(s) (listar)` en el paso 1 | Es lo esperado: con un solo comando, no se escribe su nombre |
| `No such option: --unidad` | Las opciones del callback van **antes** del comando: `main.py --unidad ppm maximo` |
| `TypeError: 'NoneType' object is not subscriptable` en `maximo` | `ctx.obj` es `None`: el callback no lo rellenó. ¿Descomentaste `ctx.obj = {...}`? |
| `leer` se queda esperando | Lee stdin y no le llega nada: escribe líneas y termina con `Ctrl+D`, o pásale argumentos |
| `Aborted.` sin dejarte contestar | stdin no es una terminal (una tubería vacía): `typer.confirm` lee de stdin. Usa `--si` |
| La línea de error sale antes que `[callback]` | Rediriges la salida: stdout se acumula en un búfer y stderr se escribe al momento. En la terminal salen en orden |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Argumentos y opciones](../ejercicio-01-argumentos-y-opciones/README.md) | **Ejercicio 02 · Comandos y contexto** | [Ejercicio 03 · Rich](../ejercicio-03-rich/README.md) |
