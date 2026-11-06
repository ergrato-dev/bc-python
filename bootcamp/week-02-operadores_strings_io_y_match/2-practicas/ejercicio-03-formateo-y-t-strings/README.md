# Ejercicio 03 — Formateo y t-strings

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-formateo-f-strings-y-t-strings.md)

## Objetivo

Dar formato a números como los mostrarás en los informes del proyecto (decimales, miles, porcentaje, dinero, columnas) y ver por dentro una t-string de Python 3.14: qué guarda y cómo una función la convierte en HTML seguro. Ejercicio **guiado**: descomentas cada paso de `format_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-02-operadores_strings_io_y_match/2-practicas/ejercicio-03-formateo-y-t-strings/starter
uv run python format_lab.py
```

Salida esperada: `Ejercicio 03 · Formateo y t-strings`. En cada paso: predice, descomenta (`Ctrl+K Ctrl+U`), ejecuta y compara las **líneas nuevas**.

## Pasos

### 1. Decimales, miles y porcentaje

Descomenta el **PASO 1**:

```
Decimales: 3.14 2 4
Miles: 1,234,567.50 1_000_000
Porcentaje: 12.5% 78%
Precisión variable: 3.142
```

Mira `2.5` → `2` y `3.5` → `4`: con `.0f`, los empates se redondean al número **par** (es la regla IEEE, no un error). `7 / 9` es `0.777…`; `.0%` lo multiplica por 100 y lo redondea a `78%`.

### 2. Dinero en formato colombiano

Descomenta el **PASO 2**:

```
Dinero: $ 1.234.567,50 | $ 950,00
```

Sigue los tres `replace` sobre `"1,234,567.50"`: `,`→`_` da `"1_234_567.50"`; `.`→`,` da `"1_234_567,50"`; `_`→`.` da `"1.234.567,50"`. ¿Qué saldría si haces directamente `,`→`.` y luego `.`→`,`? Pruébalo en el REPL: todos los separadores acaban siendo comas.

### 3. Columnas con ancho y alineación

Descomenta el **PASO 3**:

```
Estación    |    PM2.5
Norte       |    12.50
Centro      |   131.04
Sur         |     7.00
```

`<12` ocupa 12 caracteres con el texto a la izquierda; `>9.2f`, 9 caracteres con el número a la derecha y 2 decimales. Las cifras quedan alineadas por las unidades. Cambia `"Sur"` por `"Estación Suroriental"` (20 caracteres) y ejecuta: la columna se desplaza, porque el ancho es un **mínimo** y el formato nunca recorta.

### 4. Depurar con `=`

Descomenta el **PASO 4**:

```
value=12.345 value * 2 = 24.69 value=12.3
```

### 5. Una t-string no es un `str`

Descomenta el **PASO 5**:

```
Tipo: Template
Partes fijas: ('Hola, ', '')
Valores: ('<b>Ana</b>',)
Con f-string: Hola, <b>Ana</b>
```

La f-string pegó las etiquetas `<b>` dentro del texto: si eso va a una página web, el navegador las interpreta. La t-string guardó el valor aparte, sin pegarlo. En el REPL, después de ejecutar el archivo con `uv run python -i format_lab.py`, prueba `greeting + "!"`: da `TypeError`, porque un `Template` no se usa como texto sin procesarlo.

### 6. Procesar la plantilla escapando HTML

Descomenta el **PASO 6**:

```
HTML: <p>Hola, &lt;b&gt;Ana&lt;/b&gt;: 12.3 µg/m³</p>
```

`to_html` recorre la plantilla. Usa un `for` (semana 3) y una lista (semana 5); lo que importa hoy es el `match`, que distingue dos tipos de piezas:

| Pieza | Qué hace `to_html` |
|---|---|
| `str` (parte fija, la escribiste tú) | La copia tal cual: `<p>` sigue siendo una etiqueta |
| `Interpolation` (un valor) | Le aplica su formato (`.1f`) y después `html.escape`, que cambia `<` por `&lt;` y `>` por `&gt;` |

El resultado: tus etiquetas `<p>` funcionan y las que traía el valor se muestran como texto. Es la idea de las t-strings: la plantilla separa lo que es tuyo de lo que viene de fuera.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `SyntaxError: invalid syntax` en la línea del `t"..."` | No estás en Python 3.14: ejecuta con `uv run` desde `starter/` |
| `ImportError: cannot import name 'Template'` | Igual: las t-strings existen desde Python 3.14 |
| `ValueError: Unknown format code 'f' for object of type 'str'` | Le diste formato numérico a un texto: el valor debe ser `int` o `float` |
| `NameError: name 'name' is not defined` en el paso 6 | El paso 6 usa `name` del paso 5: descomenta los dos |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Strings](../ejercicio-02-strings/README.md) | **Ejercicio 03 · Formateo y t-strings** | [Ejercicio 04 · Entrada, salida y `match`](../ejercicio-04-entrada-salida-y-match/README.md) |
