# 02 · Argumentos y opciones

⏱️ 50 min

## 🎯 Objetivos

- Declarar argumentos y opciones con `Annotated`, `typer.Argument` y `typer.Option`.
- Elegir entre argumento y opción.
- Usar los tipos que Typer sabe convertir: números, `bool`, `Path`, listas y `Enum`.
- Escribir una ayuda útil: textos, nombres cortos y `metavar`.
- Saber qué valida Typer y qué sigue validando tu paquete.

---

## 1. `Annotated`

En la teoría anterior, Typer sacaba todo de la firma: el nombre, el tipo y el valor por defecto. Para añadir más (una ayuda, un nombre corto, una comprobación) se usa `Annotated`, el mismo que usaste en la semana 13 con Pydantic:

```python
from typing import Annotated

import typer


@app.command()
def informe(
    archivo: Annotated[
        Path | None, typer.Option("--archivo", "-f", help="Lee las líneas de un .txt o un .csv.")
    ] = None,
) -> None: ...
```

`Annotated[T, extra]` sigue siendo `T` para mypy y para ti. El `extra` lo lee Typer. El valor por defecto va detrás del `=`, como en cualquier función.

| Declaración | Es |
|---|---|
| `x: T` | Argumento obligatorio |
| `x: T = valor` | Opción `--x`, que vale `valor` si no se escribe |
| `x: Annotated[T, typer.Argument(...)]` | Argumento, con la configuración de `Argument` |
| `x: Annotated[T, typer.Argument(...)] = valor` | Argumento **opcional** |
| `x: Annotated[T, typer.Option(...)] = valor` | Opción, con la configuración de `Option` |
| `x: Annotated[T, typer.Option(...)]`, sin valor | Opción **obligatoria**: `Missing option '--x'` |

## 2. ¿Argumento u opción?

| Usa un argumento | Usa una opción |
|---|---|
| El dato principal, sin el que el comando no tiene sentido | Lo que cambia **cómo** se hace |
| Se entiende sin nombre: `cp origen destino` | Necesita nombre para entenderse: `--json resumen.json` |
| Puede haber muchos: `informe "Norte;1" "Sur;2"` | Tiene un valor por defecto razonable |

Una opción obligatoria suele ser una señal de que querías un argumento. En tu proyecto, las líneas son argumentos de `informe`, y el archivo, el JSON y la escala son opciones.

## 3. Los tipos

| Anotación | Desde la terminal | Tu función recibe |
|---|---|---|
| `str` | `Norte` | `"Norte"` |
| `int`, `float` | `12.5` | `12.5`; `doce` da un error con código 2 |
| `bool` (opción) | `--verbose` | `True` si aparece, `False` si no |
| `Path` | `medidas.csv` | `Path("medidas.csv")` |
| `list[str]` (argumento) | `a b c` | `["a", "b", "c"]` |
| `list[str]` (opción) | `-e a -e b` | `["a", "b"]`: la opción se repite |
| `X \| None = None` | Nada | `None`: "no lo escribieron" |
| Un `StrEnum` | `medio` | `Nivel.MEDIO`; otro valor da un error con la lista de los válidos |

**Booleanos.** Una opción `bool` con valor por defecto `False` es un *flag*: `-v`. Para que también se pueda apagar de forma explícita, se declaran los dos nombres separados por una barra:

```python
color: Annotated[bool, typer.Option("--color/--sin-color")] = True
```

**Listas opcionales.** `lineas: Annotated[list[str] | None, typer.Argument()] = None` acepta cero o más argumentos. Sin ninguno, llega `None`, no una lista vacía. Tu `informe` lo usa así: sin líneas, lee stdin.

**`Path` con comprobaciones.** `typer.Argument(exists=True, dir_okay=False)` comprueba que el archivo existe y no es una carpeta antes de llamar a tu función. Tu proyecto **no** lo usa: `open_file` y `read_lines` ya dan un `DataFileError` con un mensaje en español, y los tests del paquete lo comprueban. Validar el archivo en dos sitios daría dos mensajes distintos para el mismo error.

## 4. La ayuda

Typer genera `--help` con lo que declaras. Que sea útil depende de ti:

```python
@app.command()
def informe(
    lineas: Annotated[
        list[str] | None,
        typer.Argument(metavar="LINEAS", help='Líneas "etiqueta;valor". Sin líneas ni --archivo, lee stdin.'),
    ] = None,
    ...
) -> None:
    """Clasifica las medidas y escribe la tabla y el resumen."""
```

```
 Usage: observatorio informe [OPTIONS] [LINEAS]

 Clasifica las medidas y escribe la tabla y el resumen.

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│   LINEAS      <str>  Líneas "etiqueta;valor". Sin líneas ni --archivo, lee   │
│                      stdin.                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --archivo  -f      <path>  Lee las líneas de un .txt o un .csv.              │
│ --json     -j      <path>  Guarda el resumen en este JSON.                   │
│ --escala   -e      <path>  Lee la unidad y los umbrales de un JSON.          │
│ --help                     Show this message and exit.                       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

| Qué | Dónde se escribe |
|---|---|
| Descripción del comando | El *docstring* de la función: su primera línea sale en la lista de comandos |
| Ayuda de cada parámetro | `help="..."` |
| Nombres de una opción | `typer.Option("--archivo", "-f")`: largo y corto |
| Nombre del argumento en `Usage` | `metavar="LINEAS"`; sin él, `[lineas]...`, con el nombre del parámetro |
| Ocultar una opción interna | `hidden=True` |

**Nombres.** Sin nombres explícitos, Typer usa el del parámetro con guiones: `json_path` sería `--json-path`. Por eso tu proyecto escribe `typer.Option("--json", "-j")`. Además, el parámetro no se llama `json`: taparía el módulo `json` dentro de la función si algún día lo importas.

Las opciones cortas son una letra y deben ser fáciles de recordar: `-f` de *file*, `-j` de *json*, `-v` de *verbose*. Mantén las de tu `main` de siempre. Quien ya escribía `observatorio -f medidas.csv` solo tiene que añadir `informe`.

## 5. Variables de entorno

Una opción puede leer su valor de una variable de entorno si no se escribe:

```python
escala: Annotated[Path | None, typer.Option("--escala", "-e", envvar="OBSERVATORIO_ESCALA")] = None
```

El orden es: lo que escribes en la línea de comandos, si no la variable, y si no el valor por defecto. Es la forma habitual de configurar una CLI en Docker o en el CI. En la semana 18 verás `.env` y secretos.

## 6. Qué valida cada uno

```
argv ──► Typer: ¿existe la opción? ¿falta un argumento? ¿"12.5" es un float?
              │ si no: mensaje, código 2, tu función no se ejecuta
              ▼
         tu comando ──► tu paquete: ¿el archivo existe? ¿la línea es "etiqueta;valor"?
                                    ¿los umbrales son posibles? (DataFileError, código 2)
```

Typer valida la **forma** de la llamada: nombres, número de argumentos y tipos. Tu paquete valida el **contenido**: archivos, líneas y escalas. Ese reparto mantiene `core/` sin saber nada de Typer, igual que no sabía nada de `sys.argv`.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| Un parámetro que querías opción sale como argumento obligatorio | Le falta el valor por defecto | `= None` o un valor razonable |
| `No such option: --json-path` cuando escribías `--json` | El nombre sale del parámetro: `json_path` es `--json-path` | Da los nombres: `typer.Option("--json", "-j")` |
| La lista llega como `None` y `len(lineas)` falla | Argumento opcional sin nada escrito | `if lineas:` antes de usarla, o `lineas or []` |
| `--verbose False` da `Got unexpected extra argument` | Un *flag* no lleva valor | `--verbose` para activarlo; para un par `--x/--no-x`, decláralo así |
| `-5` da `No such option` | Empieza por `-` y parece una opción | `--` antes: `comprobar -- -5` |
| mypy: `Incompatible default for argument` | Valor por defecto `None` con un tipo que no admite `None` | `Path \| None = None` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué hace `Annotated` y qué parte lee mypy y qué parte lee Typer.
- [ ] La diferencia entre argumento y opción, y cuándo usar cada uno.
- [ ] Cómo se declaran un *flag*, una lista, un `Path` y un `Enum`.
- [ ] Dónde se escribe cada parte de la ayuda.
- [ ] Qué valida Typer y qué sigue validando tu paquete.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · De `argv` a Typer](01-de-argv-a-typer.md) | **02 · Argumentos y opciones** | [03 · Comandos, callback y salida](03-comandos-callback-y-salida.md) |
