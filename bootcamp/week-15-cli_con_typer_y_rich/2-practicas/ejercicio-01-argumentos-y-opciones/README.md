# Ejercicio 01 — Argumentos y opciones

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-de-argv-a-typer.md) y [02](../../1-teoria/02-argumentos-y-opciones.md)

## Objetivo

Construir comandos con Typer a partir de las firmas de las funciones:

- un argumento con tipo, que Typer convierte y valida;
- opciones con valor por defecto;
- `Annotated` con ayuda, un nombre corto y una opción booleana;
- una lista de argumentos;
- un archivo que debe existir;
- un valor elegido de una lista fija, con un `Enum`;
- los códigos de salida 0, 1 y 2.

Tu proyecto cambia su `match` sobre `argv` por una aplicación Typer. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-15-cli_con_typer_y_rich/2-practicas/ejercicio-01-argumentos-y-opciones/starter
uv run python main.py
```

```
 Usage: main.py [OPTIONS] COMMAND [ARGS]...

 Ejercicio 01 · Argumentos y opciones.

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

`uv` instala `typer` (y con él, `rich`) la primera vez. Sin argumentos, la aplicación enseña su ayuda: lo pide `no_args_is_help=True`. Todavía no hay comandos. Los recuadros los dibuja Rich, y su ancho depende de tu terminal.

Los textos que escribe Typer por su cuenta (`Usage`, `Show this message and exit.`, los errores) están en inglés. Los que escribes tú (la ayuda de cada comando y de cada opción) salen en español.

## Pasos

### 1. Un argumento con tipo

Descomenta el **PASO 1** y ejecuta:

```bash
uv run python main.py clasificar 12.5
uv run python main.py clasificar abc
uv run python main.py clasificar
```

```
12.5 → medio
```

```
Usage: main.py clasificar [OPTIONS] {valor}
Try 'main.py clasificar --help' for help.
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Invalid value for 'valor': 'abc' is not a valid float.                       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

```
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Missing argument 'valor'.                                                    │
╰──────────────────────────────────────────────────────────────────────────────╯
```

`def clasificar(valor: float)` basta: un parámetro sin valor por defecto es un **argumento** obligatorio, y su anotación `float` dice cómo convertir el texto. Typer convierte `"12.5"` antes de llamar a tu función, y si no puede, escribe el error en stderr y termina con código `2`, sin llamarla. Compruébalo con `echo $?` justo después.

### 2. Opciones con valor por defecto

Descomenta el **PASO 2** y ejecuta:

```bash
uv run python main.py umbrales 12.5 --bajo 15
uv run python main.py umbrales 12.5 --alto
```

```
12.5 entre 15.0 y 50.0 → bajo
```

```
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Option '--alto' requires an argument.                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

Un parámetro **con** valor por defecto es una **opción**: `bajo: float = 10.0` se convierte en `--bajo`, y si no la escribes vale `10.0`. Las opciones van por nombre y en cualquier orden: `--alto 60 12.5 --bajo 5` también vale.

### 3. `Annotated`, ayuda y una opción booleana

Descomenta el **PASO 3** y ejecuta:

```bash
uv run python main.py etiquetar "  Norte " -m
uv run python main.py etiquetar --help
```

```
NORTE
```

```
 Usage: main.py etiquetar [OPTIONS] {etiqueta}

 Escribe una etiqueta limpia.

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    etiqueta      <str>  El nombre de la estación. [required]               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --mayusculas  -m        Escribe la etiqueta en mayúsculas.                   │
│ --help                  Show this message and exit.                          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

`Annotated[str, typer.Argument(help=...)]` añade información al tipo sin cambiarlo: para mypy, `etiqueta` sigue siendo un `str`. La ayuda del comando es el *docstring* de la función. Una opción `bool` no lleva valor: `-m` la pone a `True`. Los nombres `"--mayusculas", "-m"` sustituyen al que Typer sacaría del parámetro.

### 4. Una lista de argumentos

Descomenta el **PASO 4** y ejecuta:

```bash
uv run python main.py media 12.5 8 61
uv run python main.py media
```

```
media de 3: 27.17
```

```
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Missing argument 'valores'.                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

`list[float]` recoge todos los argumentos que quedan y convierte cada uno. Sin valor por defecto, hace falta al menos uno. Así, tu función nunca recibe una lista vacía y la división nunca falla.

### 5. Un archivo que debe existir

Descomenta el **PASO 5** y ejecuta:

```bash
uv run python main.py contar medidas.txt
uv run python main.py contar nada.txt
uv run python main.py contar .
```

```
medidas.txt: 3 líneas
```

```
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Invalid value for 'ruta': File 'nada.txt' does not exist.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
```

```
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Invalid value for 'ruta': File '.' is a directory.                           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

Con la anotación `Path`, Typer entrega un `Path`, no un `str`. `exists=True` y `dir_okay=False` comprueban el archivo antes de llamar a tu función. Es cómodo, pero el mensaje está en inglés y no es tu `DataFileError`: en el proyecto, quien comprueba los archivos sigue siendo tu paquete.

### 6. Valores fijos con un `Enum`

Descomenta el **PASO 6** y ejecuta:

```bash
uv run python main.py umbral
uv run python main.py umbral --nivel medio
uv run python main.py umbral --nivel muy-alto
```

```
alto: más de 50
medio: de 10 a 50
```

```
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Invalid value for '--nivel': 'muy-alto' is not one of 'bajo', 'medio',       │
│ 'alto'.                                                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

Un `StrEnum` como anotación limita los valores posibles. La ayuda los enumera y Typer rechaza los demás. Tu función recibe un `Nivel`, no un texto.

### 7. Códigos de salida

Descomenta el **PASO 7** y ejecuta cada línea seguida de `echo $?`:

```bash
uv run python main.py comprobar 30; echo $?
uv run python main.py comprobar 70; echo $?
uv run python main.py comprobar -- -5; echo $?
```

```
30.0 está dentro del rango
0
70.0 está fuera del rango
1
```

```
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Invalid value for VALOR: no puede ser negativo                               │
╰──────────────────────────────────────────────────────────────────────────────╯
2
```

| Código | Quién | Significa |
|---|---|---|
| `0` | Tu función termina normalmente | Todo bien |
| `1` | `raise typer.Exit(code=1)` | El programa funcionó, pero el resultado es "no" (como `grep` cuando no encuentra nada) |
| `2` | Typer, o tu `raise typer.BadParameter(...)` | Lo has llamado mal: argumento que falta, tipo incorrecto, opción desconocida |

El `--` dice "lo que sigue ya no son opciones": sin él, `-5` parece una opción llamada `-5`.

Al terminar, `uv run python main.py --help` enumera los siete comandos.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `No such command 'clasificar'` | El `@app.command()` de ese paso sigue comentado: descomenta el bloque entero |
| `Got unexpected extra argument(s)` | Sobra un argumento, o escribiste una opción sin `--` (`bajo 15` en lugar de `--bajo 15`) |
| `No such option: --mayúsculas (Possible options: --mayusculas)` | El nombre de la opción sale del parámetro, que no lleva tilde: `--mayusculas` |
| La ayuda no enseña tu texto | La ayuda del comando es el *docstring*, la primera cadena de la función, no un comentario `#` |
| `-5` da `No such option` | Escribe `--` antes de un número negativo: `comprobar -- -5` |
| Los recuadros salen cortados o con caracteres raros | Tu terminal no muestra bien Unicode: en Windows usa Windows Terminal. La ayuda funciona igual |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Probar la CLI y cerrar la fase](../../1-teoria/05-probar-la-cli-y-cerrar-la-fase.md) | **Ejercicio 01 · Argumentos y opciones** | [Ejercicio 02 · Comandos y contexto](../ejercicio-02-comandos-y-contexto/README.md) |
