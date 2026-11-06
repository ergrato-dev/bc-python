# Ejercicio 04 — Muchas líneas

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-patrones-de-bucle.md) y [04](../../1-teoria/04-leer-muchas-lineas.md)

## Objetivo

Leer un archivo entero por la entrada estándar, saltar comentarios y líneas vacías, acumular un resumen y avisar de las líneas inválidas con su número sin detener el resto. Es lo que hace el proyecto de esta semana, escrito todo seguido. Ejercicio **guiado**: descomentas cada paso de `lines_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-03-bucles_iteracion_y_depuracion/2-practicas/ejercicio-04-muchas-lineas/starter
cat lecturas.txt
uv run python lines_lab.py < lecturas.txt
```

`cat` muestra las 8 líneas del archivo: un comentario, una vacía, un dato que falta (`NA`) y una línea sin `;`. El programa solo imprime su título. `< lecturas.txt` conecta el archivo a la entrada estándar del programa: es como si lo escribieras con el teclado.

## Pasos

### 1. Leer todo stdin

Descomenta el **PASO 1** y ejecuta con `< lecturas.txt`:

```
Líneas leídas: 8
   '# estación;valor en µg/m³\n'
   'Norte;12,5\n'
   'Sur;8\n'
```

Cada línea conserva su salto `\n` al final: por eso, en los pasos siguientes, lo primero es `strip()`. Ahora ejecuta **sin** `< lecturas.txt`: el programa espera que escribas. Escribe dos líneas y pulsa `Ctrl+D` (en Windows, `Ctrl+Z` y Enter) para decirle que la entrada terminó.

### 2. Limpiar, numerar y saltar

Descomenta el **PASO 2**:

```
  línea 2: Norte;12,5
  línea 3: Sur;8
  línea 5: Centro;NA
  línea 6: Oriente;55,1
  línea 7: Occidente 61
  línea 8: Norte;48,9
Saltadas: 2
```

Faltan la 1 (comentario) y la 4 (vacía): `continue` las salta. Pero `enumerate` las sigue contando, y por eso los números coinciden con los del archivo. Así, cuando avises de un error, la persona podrá ir directo a esa línea.

### 3. Total, cantidad y máximo

Descomenta el **PASO 3**:

```
Medidas: 4 | sin dato: 1 | promedio: 31.12
Máximo: Oriente con 55.1
```

Cinco variables acumulan a la vez, todas creadas **antes** del bucle. `Centro;NA` cuenta como "sin dato" y no entra en el promedio; `Occidente 61` no tiene `;` y se salta. Comprueba el promedio a mano: (12.5 + 8 + 55.1 + 48.9) / 4 = 31.125.

### 4. Avisar sin detenerse

Descomenta el **PASO 4** y ejecuta:

```
error: línea 7: 'Occidente 61'
...
Líneas inválidas: 1
```

El aviso puede salir arriba del todo, antes que el resto: stderr se escribe al momento y stdout se guarda en un búfer hasta el final. Para verlos por separado:

```bash
uv run python lines_lab.py < lecturas.txt > resumen.txt; echo "código: $?"
cat resumen.txt
rm resumen.txt
```

En la pantalla solo queda `error: línea 7: 'Occidente 61'` y `código: 1`; el resumen limpio está en `resumen.txt`. Corrige la línea 7 de `lecturas.txt` (`Occidente;61`) y repite: código `0`, y el máximo pasa a ser `Occidente con 61.0`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| El programa se queda esperando | Faltó `< lecturas.txt`: escríbelo, o termina la entrada con `Ctrl+D` |
| `Líneas leídas: 0` | El archivo está vacío o escribiste `<` hacia otro archivo: revisa con `cat lecturas.txt` |
| `NameError: name 'lines' is not defined` | Descomentaste un paso sin el paso 1 |
| `ZeroDivisionError` en el promedio | Ninguna línea tenía una medida válida (por ejemplo, con un archivo vacío) |
| `ValueError: could not convert string to float` | Una medida no es un número: `float` no entiende `"abc"`. En la semana 7 lo capturarás |
| `bash: lecturas.txt: No such file or directory` | No estás en la carpeta `starter` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Depuración](../ejercicio-03-depuracion/README.md) | **Ejercicio 04 · Muchas líneas** | [Proyecto · Observatorio, capa 2](../../3-proyecto/README.md) |
