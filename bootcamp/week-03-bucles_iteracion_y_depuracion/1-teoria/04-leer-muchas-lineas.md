# 04 · Leer muchas líneas

⏱️ 35 min

## 🎯 Objetivos

- Recorrer la entrada estándar línea a línea con `for line in sys.stdin`.
- Pasar un archivo a un programa con `<` y la salida de otro con `|`.
- Terminar la entrada desde el teclado con `Ctrl+D`.
- Numerar las líneas para que los errores digan dónde están.

---

## 1. `sys.stdin` es un iterable de líneas

En la semana 2, `input()` leía **una** línea. `sys.stdin` es la entrada estándar entera, y un `for` la recorre línea a línea hasta que se acaba:

```python
# eco.py
import sys

for line in sys.stdin:
    print("leí:", repr(line))
```

```bash
printf "Norte;12,5\nSur;8\n" | uv run python eco.py
```

```
leí: 'Norte;12,5\n'
leí: 'Sur;8\n'
```

Dos detalles:

| Detalle | Consecuencia |
|---|---|
| Cada línea trae su `\n` al final | Haz `line = line.strip()` antes de usarla |
| El bucle termina cuando la entrada se acaba (*EOF*, fin de archivo) | No hace falta centinela: el `for` sabe cuándo parar |

`sys.stdin.readlines()` lee todo de golpe y devuelve una lista de líneas. Es cómodo si necesitas recorrerlas varias veces; si no, el `for` directo es mejor: procesa cada línea en cuanto llega y no guarda el archivo entero en memoria.

## 2. De dónde vienen las líneas

El programa no sabe de dónde vienen: la terminal decide qué conecta a su stdin.

| Comando | stdin es |
|---|---|
| `uv run python eco.py` | El teclado: escribe líneas y termina con `Ctrl+D` |
| `uv run python eco.py < medidas.txt` | El archivo `medidas.txt` |
| `cat medidas.txt \| uv run python eco.py` | La salida de `cat` |
| `grep Norte medidas.txt \| uv run python eco.py` | Solo las líneas con `Norte` |

Desde el teclado, `Ctrl+D` al principio de una línea vacía le dice al programa "no hay más". En Windows (fuera de WSL), es `Ctrl+Z` y Enter. Con `Ctrl+C` lo interrumpes en lugar de terminarlo bien.

## 3. Numerar las líneas

Con `enumerate(sys.stdin, start=1)` cada línea viene con su número. Si saltas comentarios con `continue`, el número **sigue contando**, así que coincide con la línea del archivo:

```python
import sys

for number, line in enumerate(sys.stdin, start=1):
    line = line.strip()
    if line == "" or line.startswith("#"):
        continue
    if ";" not in line:
        print(f"error: línea {number}: {line!r}", file=sys.stderr)
        continue
    print(line)
```

Un mensaje como `error: línea 907: 'Sur 9,5'` permite abrir el archivo e ir directo al problema. Y como el bucle **sigue** después del error, una línea mala no tira las otras novecientas.

## 4. El orden de stdout y stderr

Cuando la salida va a un archivo o a una tubería, Python guarda stdout en un **búfer** y lo escribe en bloques; stderr se escribe al momento. Por eso, en la terminal, los errores pueden aparecer antes que filas que se imprimieron antes que ellos. Los datos no se pierden ni cambian; solo cambia el orden en que los ves. Si necesitas separarlos, redirige:

```bash
uv run python eco.py < medidas.txt > filas.txt 2> errores.txt
```

## 5. Lo mismo en Docker

Para pasar un archivo de tu máquina al programa dentro del contenedor, añade `-T` a `docker compose run`: le dice a Docker que no abra una terminal interactiva, sino que conecte la entrada del contenedor a lo que redirijas:

```bash
docker compose run --rm -T app observatorio < medidas.txt
```

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| El programa se queda esperando sin hacer nada | Lee del teclado porque no le pasaste un archivo | `< archivo`, o escribe las líneas y `Ctrl+D` |
| Las comparaciones fallan aunque el texto "se ve igual" | La línea trae `\n` al final | `line.strip()` |
| `bash: medidas.txt: No such file or directory` | Estás en otra carpeta | `ls`, y usa la ruta correcta |
| Los errores salen mezclados o antes que las filas | stdout tiene búfer y stderr no | Es normal; separa con `>` y `2>` |

## ✅ Qué debes saber al terminar

- [ ] Cómo recorrer `sys.stdin` y por qué hay que hacer `strip()`.
- [ ] Qué hacen `<` y `|`, y cómo terminar la entrada desde el teclado.
- [ ] Por qué numerar con `enumerate` y seguir después de una línea mala.
- [ ] Por qué stdout y stderr pueden salir en otro orden.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Patrones de bucle](03-patrones-de-bucle.md) | **04 · Leer muchas líneas** | [05 · Depuración](05-depuracion.md) |
