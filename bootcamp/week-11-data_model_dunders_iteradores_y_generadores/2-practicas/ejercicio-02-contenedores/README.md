# Ejercicio 02 — Contenedores

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-operadores-y-contenedores.md)

## Objetivo

Construir clases que se comportan como contenedores: `len()`, `objeto[i]`, rebanadas, `in` y `for`. Verás que con `__getitem__` ya funciona un `for`, qué recibe `__getitem__` cuando le pides `[1:3]`, cómo cambia `in` con `__contains__` y cuánto te regala `collections.abc.Sequence`. Es lo que gana `Series` en tu proyecto. Ejercicio **guiado**: descomentas cada paso de `container_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-11-data_model_dunders_iteradores_y_generadores/2-practicas/ejercicio-02-contenedores/starter
uv run python container_lab.py
```

```
Ejercicio 02 · Contenedores
```

El paso 2 usa la clase del paso 1: descomenta en orden. Cada salida de abajo muestra solo las líneas nuevas del paso.

## Pasos

### 1. `__len__` y `__getitem__`

Descomenta el **PASO 1** y ejecuta:

```
    __getitem__(0)
    __getitem__(-1)
len: 3 · primera: 12.5 · última: 55.1
    __getitem__(3)
Error: list index out of range
```

`len(readings)` llama a `readings.__len__()` y `readings[0]`, a `readings.__getitem__(0)`. El `print` dentro de `__getitem__` te deja ver cada llamada. Los índices negativos funcionan porque `__getitem__` los pasa tal cual a la lista de dentro, y el `IndexError` del final también es el de la lista: **delegar** (semana 10) te da su comportamiento gratis.

### 2. Un `for` sin `__iter__`

Descomenta el **PASO 2** y ejecuta:

```
for:
    __getitem__(0)
  valor 12.5
    __getitem__(1)
  valor 8.0
    __getitem__(2)
  valor 55.1
    __getitem__(3)
    __getitem__(0)
    __getitem__(1)
    __getitem__(2)
¿55.1 in readings? True
¿Iterable? False · ¿Sized? True
```

`Readings` no tiene `__iter__` y aun así entra en un `for`. Es el protocolo **antiguo**: Python pide `[0]`, `[1]`, `[2]`... hasta que salta un `IndexError`, que para él significa "se acabó" (fíjate en el `__getitem__(3)` sin valor). `in` hace lo mismo: recorre hasta encontrar `55.1`. Pero `isinstance(readings, Iterable)` dice `False`, porque solo mira si existe `__iter__`, y mypy tampoco lo acepta (`"Readings" has no attribute "__iter__" (not iterable)`). Funciona por compatibilidad; en código nuevo, escribe `__iter__`.

### 3. Rebanadas (*slices*)

Descomenta el **PASO 3** y ejecuta:

```
    recibe 1
track[1]: 20.0
    recibe slice(1, 3, None)
track[1:3]: Track([20.0, 30.0])
    recibe slice(None, None, -1)
track[::-1]: Track([40.0, 30.0, 20.0, 10.0])
```

`track[1:3]` no llama a un método distinto: llama a `__getitem__` con un objeto `slice(inicio, fin, paso)`. `Track` mira qué ha recibido: con un `slice` devuelve un `Track` nuevo (como `lista[1:3]` devuelve otra lista); con un `int`, un valor. Tu `Series` del proyecto solo acepta `int`: no lo necesita.

### 4. `__iter__` y `__contains__` propios

Descomenta el **PASO 4** y ejecuta:

```
    __contains__('Norte')
    __contains__(12.5)
¿Norte in logbook? True · ¿12.5 in logbook? False
Valores: [12.5, 8.0] · suma: 20.5 · máximo: 12.5
¿Iterable? True
```

- Con `__contains__`, `in` deja de recorrer: llama a tu método, que aquí busca **etiquetas**. Por eso `12.5 in logbook` es `False` aunque `12.5` salga en el `for`. Se puede, pero confunde: piensa dos veces antes de que `in` y `for` hablen de cosas distintas.
- `__iter__` devuelve un iterador (teoría 03): aquí, el de los valores del diccionario. Con él, `list`, `sum` y `max` funcionan sin escribir nada más, e `isinstance(..., Iterable)` ya es `True`.

### 5. `Sequence` te da el resto

Descomenta el **PASO 5** y ejecuta:

```
¿'vie' in week? True · índice: 4 · cuántos 'lun': 1
Al revés: ['dom', 'sáb', 'vie']
Gratis de Sequence: ['__contains__', '__iter__', '__reversed__', 'count', 'index']
Error: Can't instantiate abstract class OnlyLength without an implementation for abstract method '__getitem__'
```

`collections.abc.Sequence` es una clase abstracta (semana 10) con dos métodos abstractos, `__len__` y `__getitem__`, y cinco métodos plantilla que se apoyan en ellos: `__contains__`, `__iter__`, `__reversed__`, `index` y `count`. `Week` escribe dos y recibe siete. `OnlyLength` olvida `__getitem__` y no se puede crear. El `# type: ignore[override]` es para mypy: el `__getitem__` de `Sequence` acepta también rebanadas y el de `Week` solo enteros.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'readings' is not defined` en el paso 2 | Descomenta antes el paso 1 |
| `TypeError: object of type 'Readings' has no len()` | Falta `__len__`, o tiene otro nombre |
| `TypeError: 'Readings' object is not subscriptable` | Falta `__getitem__` |
| El `for` del paso 2 no termina | `__getitem__` no lanza `IndexError` al pasarse del final: delega en la lista de dentro |
| `track[1:3]` devuelve una `list` y no un `Track` | Falta el `if isinstance(index, slice)` que envuelve el resultado en `Track(...)` |
| `TypeError: 'Logbook' object is not iterable` | Falta `__iter__`, o tiene otro nombre |
| `TypeError: iter() returned non-iterator of type 'list'` | `__iter__` devuelve una lista: debe devolver un iterador, `iter(...)` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Dunders](../ejercicio-01-dunders/README.md) | **Ejercicio 02 · Contenedores** | [Ejercicio 03 · Iteradores](../ejercicio-03-iteradores/README.md) |
