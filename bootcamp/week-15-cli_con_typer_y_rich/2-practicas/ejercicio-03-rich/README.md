# Ejercicio 03 — Rich

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-rich.md)

## Objetivo

Escribir en la terminal con Rich:

- estilos con marcas entre corchetes: `[bold]`, `[green]`;
- el peligro de esas marcas cuando el texto viene de tus datos;
- una tabla con columnas alineadas y colores por nivel;
- un panel y una regla;
- una segunda consola para stderr;
- qué cambia cuando la salida no va a una terminal.

Tu proyecto escribe su informe como una tabla de Rich, con dos consolas y sin marcas. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-15-cli_con_typer_y_rich/2-practicas/ejercicio-03-rich/starter
uv run python main.py
```

```
Ejercicio 03 · Rich
```

En tu terminal, el `03` sale en otro color: Rich **resalta** por su cuenta los números, las rutas y los valores como `True` o `None`. Cada paso añade salida debajo de la anterior. Los colores de este README no se ven: compáralos en tu terminal.

## Pasos

### 1. Estilos

Descomenta el **PASO 1** y ejecuta:

```
Norte: 12.5 µg/m³ → medio
Oriente: 55.1 µg/m³ → alto
Estilo para todo el texto
```

`Norte` sale en negrita, `medio` en verde, la línea de `Oriente` en rojo y negrita, y la última en cursiva y cian. `[bold]...[/bold]` abre y cierra un estilo, y `[/]` cierra el último abierto. `style=` aplica uno a todo el texto. Los estilos se combinan: `"bold red"`, `"italic cyan"`, `"white on red"`.

### 2. Los corchetes de tus datos

Descomenta el **PASO 2** y ejecuta:

```
con marcas: Sala 
con escape: Sala [b]
sin marcas: Sala [b]
```

La etiqueta es `"Sala [b]"`. Con marcas activadas, Rich toma `[b]` por "negrita" (`b` es la abreviatura de `bold`): lo **borra** y pone en negrita lo que sigue. No da ningún error. Un dato que el usuario escribió acaba de cambiar tu salida.

Dos soluciones:

- `escape(texto)` protege los corchetes de ese texto, y sigues pudiendo usar marcas en el resto;
- `markup=False` en `print` (o en la `Console`) desactiva las marcas del todo.

Tu proyecto escribe datos del usuario en todas partes, así que usa `Console(markup=False)`.

### 3. Una tabla

Descomenta el **PASO 3** y ejecuta:

```
          Medidas
┏━━━━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃ Etiqueta ┃ Valor ┃ Nivel ┃
┡━━━━━━━━━━╇━━━━━━━╇━━━━━━━┩
│ Norte    │  12.5 │ medio │
│ Sur      │   8.0 │ bajo  │
│ Oriente  │  55.1 │ alto  │
│ Sala [b] │  30.0 │ medio │
└──────────┴───────┴───────┘
```

`Table` calcula el ancho de cada columna con su contenido más largo. `justify="right"` alinea los números a la derecha, para que las cifras queden unas bajo otras. Cada celda es texto con marcas, así que el nivel lleva su color con `[green]medio[/]` y la etiqueta pasa por `escape`. Sin `escape`, la fila de `Sala [b]` volvería a perder sus corchetes.

### 4. Un panel y una regla

Descomenta el **PASO 4** y ejecuta:

```
─────────────────────────────────── Resumen ────────────────────────────────────
╭──────────────────────────────── Observatorio ────────────────────────────────╮
│ registros: 4                                                                 │
│ media: 26.4                                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

`console.rule` dibuja una línea con un título, y `Panel` enmarca un texto. Los dos ocupan **todo el ancho** de la terminal: estrecha la ventana, vuelve a ejecutar y mira cómo cambian.

### 5. Los errores, a stderr

Descomenta el **PASO 5** y ejecuta dos veces:

```bash
uv run python main.py
uv run python main.py 2> /dev/null
```

La primera vez, la última línea es `error: línea 7: 'Sur 9,5'`, con `error:` en rojo. La segunda no aparece: `errors = Console(stderr=True)` escribe en stderr, y `2> /dev/null` lo tira. Lo mismo que `print(..., file=sys.stderr)` desde la semana 3, pero con estilos.

### 6. ¿Hay una terminal?

Descomenta el **PASO 6** y ejecuta dos veces:

```bash
uv run python main.py
uv run python main.py | cat
```

La primera vez, la última línea es `terminal: True · ancho: ...`, con el ancho de tu ventana. La segunda:

```
terminal: False · ancho: 80
```

Con `| cat`, la salida va a otro programa, no a una terminal. Rich lo detecta y cambia de comportamiento:

- **sin colores ni estilos**: ningún código de escape ensucia el texto que lee el otro programa, ni un archivo con `> informe.txt`;
- **ancho de 80**: no puede preguntar el ancho a una ventana que no existe. Las líneas más largas se cortan, salvo con `soft_wrap=True`.

Lo mismo pasa en los tests con `CliRunner` y en Docker sin `-t`. Dos variables de entorno cambian esta decisión: `NO_COLOR=1` quita los colores aunque haya terminal, y `FORCE_COLOR=1` los pone aunque no la haya. Prueba `FORCE_COLOR=1 uv run python main.py | cat` y verás los colores pasar por la tubería.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `MarkupError: closing tag '[/bold]' ... doesn't match any open tag` | Cierras un estilo que no abriste, o que ya cerraste: revisa que cada `[x]` tenga su `[/x]` |
| Desaparece texto entre corchetes | Rich lo tomó por una marca: `escape(texto)` o `markup=False` |
| No ves ningún color | Tu salida no va a una terminal (rediriges, o es la consola de un editor), o tienes `NO_COLOR` definida. Prueba en una terminal normal |
| Salen códigos como `^[[1m` en un archivo | Algo forzó los colores, por ejemplo `FORCE_COLOR`: quítala al redirigir |
| La tabla sale rota, con `?` o con cuadros vacíos | Tu terminal no muestra bien Unicode: en Windows usa Windows Terminal |
| Las líneas de error salen antes que la tabla | Rediriges la salida: stdout se acumula en un búfer y stderr se escribe al momento |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Comandos y contexto](../ejercicio-02-comandos-y-contexto/README.md) | **Ejercicio 03 · Rich** | [Ejercicio 04 · Probar la CLI](../ejercicio-04-probar-la-cli/README.md) |
