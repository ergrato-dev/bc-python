# Ejercicio 01 — Archivos y rutas

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-pathlib-y-archivos.md)

## Objetivo

Manejar rutas con `pathlib`, entender desde dónde se resuelve una ruta relativa, y escribir y leer archivos de texto con `with` y `encoding="utf-8"`. El paso 3 es la base de `read_lines` del proyecto. Ejercicio **guiado**: descomentas cada paso de `files_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-07-pathlib_json_csv_excepciones_y_context_managers/2-practicas/ejercicio-01-archivos-y-rutas/starter
uv run python files_lab.py
```

```
Ejercicio 01 · Archivos y rutas
```

Aparece una carpeta `salida/` junto a `files_lab.py`: todo lo que escribe el ejercicio va ahí, y está en el `.gitignore`. Puedes borrarla cuando quieras; se vuelve a crear.

## Pasos

### 1. Las piezas de una ruta

Descomenta el **PASO 1** y ejecuta:

```
parent: /home/ana/proyectos/observatorio
name: medidas.csv | stem: medidas | suffix: .csv
Unida con /: datos/2026/medidas.csv
Otra extensión: medidas.json
¿Existe? False
```

Ningún archivo `/home/ana/...` existe en tu máquina, y aun así `parent`, `name`, `stem`, `suffix`, `/` y `with_suffix` funcionan: solo trabajan con el texto de la ruta. `exists()` es la única que pregunta al disco. En Windows, `Path` escribe las rutas con `\`, y el código no cambia.

### 2. Relativa o absoluta

Descomenta el **PASO 2**:

```
Carpeta de trabajo: starter
Carpeta de este .py: starter
¿Absoluta? False -> True
```

Ahora sube una carpeta y lánzalo desde allí:

```bash
cd ..
uv run --project starter python starter/files_lab.py
```

```
Carpeta de trabajo: ejercicio-01-archivos-y-rutas
Carpeta de este .py: starter
```

La carpeta de trabajo cambió y la del `.py` no. Una ruta relativa como `Path("salida") / "notas.txt"` se resuelve desde la **carpeta de trabajo**, y ahora apuntaría a otro sitio. Por eso este ejercicio construye `OUT` desde `Path(__file__).parent`, la carpeta del propio `.py`. Vuelve con `cd starter`.

### 3. Escribir y leer con `with`

Descomenta el **PASO 3**:

```
¿Cerrado tras el with? True
read().splitlines(): ['Norte;12,5', 'Peñalara;3,5']
readlines(): ['Norte;12,5\n', 'Peñalara;3,5\n']
read_text: 'Norte;12,5\nPeñalara;3,5\n'
```

Al salir del `with`, el archivo está cerrado aunque la variable `file` siga existiendo. `write` no añade el salto de línea: el `\n` lo pones tú. Compara las dos formas de leer: `read().splitlines()` da las líneas limpias y `readlines()` les deja el `\n`, que estorba al comparar. `read_text` lee todo de una vez.

Ahora quita `encoding="utf-8"` de la línea que lee con `read().splitlines()` y ejecuta. En Linux y macOS no cambia nada, porque su codificación por defecto ya es UTF-8. En Windows puedes ver `PeÃ±alara` o un `UnicodeDecodeError`. Por eso se escribe siempre. Vuelve a ponerlo.

### 4. Los modos `"a"` y `"w"`

Descomenta el **PASO 4**:

```
Tras tres 'a': ['10', '20', '30']
Tras un 'w': ['40']
```

`"a"` añade al final: cada vuelta abre, escribe una línea y cierra, y las anteriores siguen ahí. `"w"` vacía el archivo **al abrirlo**, antes de escribir nada. Prueba el modo `"x"`: cambia el último `"w"` por `"x"` y ejecuta.

```
FileExistsError: [Errno 17] File exists: '.../salida/registro.txt'
```

`"x"` solo crea archivos nuevos. Sirve cuando pisar uno existente sería un error. Vuelve a `"w"`.

### 5. Carpetas y `glob`

Descomenta el **PASO 5**:

```
Archivos .txt: ['medidas-01.txt', 'medidas-02.txt', 'medidas-03.txt']
Tamaño del primero: 9 bytes
Relativa a salida: diarias/2026/medidas-01.txt
```

`mkdir(parents=True, exist_ok=True)` crea `diarias/` y `2026/` de una vez, sin error si ya existen. `glob("*.txt")` encuentra solo los `.txt`, y `leeme.md` queda fuera. `glob` no promete ningún orden: el `sorted` lo fija. `stat().st_size` da el tamaño en bytes: `Norte;01` y el salto de línea son 9. `relative_to` quita el principio común de dos rutas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `FileNotFoundError` al escribir | La carpeta no existe: `mkdir(parents=True, exist_ok=True)` antes |
| Las líneas salen con `\n` al final | Usaste `readlines()`: `read().splitlines()` |
| `ValueError: I/O operation on closed file.` | Usaste `file` fuera del `with`: mételo dentro |
| `FileExistsError` | Abriste en `"x"` un archivo que ya existe: es justo lo que hace `"x"` |
| `Tamaño del primero` da 10 bytes | En Windows, el modo texto escribe cada `\n` como `\r\n`: no pasa nada |
| `Carpeta de trabajo` no es `starter` | Lo lanzaste desde otra carpeta: es lo que enseña el paso 2 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · JSON](../../1-teoria/05-json.md) | **Ejercicio 01 · Archivos y rutas** | [Ejercicio 02 · Excepciones](../ejercicio-02-excepciones/README.md) |
