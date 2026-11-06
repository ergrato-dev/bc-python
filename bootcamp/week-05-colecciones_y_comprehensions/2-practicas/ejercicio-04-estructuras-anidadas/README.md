# Ejercicio 04 — Estructuras anidadas

⏱️ 1 h · Teoría previa: [01](../../1-teoria/01-listas.md), [03](../../1-teoria/03-diccionarios.md) y [04](../../1-teoria/04-conjuntos.md)

## Objetivo

Caer a propósito en las tres trampas de la mutabilidad (repetir una lista con `*`, copiar solo por fuera y cambiar una lista mientras la recorres), leer datos anidados como los de un JSON y medir por qué conviene un `set` para buscar. Ejercicio **guiado**: descomentas cada paso de `nested_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-05-colecciones_y_comprehensions/2-practicas/ejercicio-04-estructuras-anidadas/starter
uv run python nested_lab.py
```

```
Ejercicio 04 · Estructuras anidadas
```

## Pasos

### 1. La trampa de `[[0] * 3] * 3`

Descomenta el **PASO 1** y ejecuta:

```
Con *:             [[9, 0, 0], [9, 0, 0], [9, 0, 0]]
Con comprehension: [[9, 0, 0], [0, 0, 0], [0, 0, 0]]
```

Cambiaste una casilla y con `*` cambiaron tres. El `* 3` de fuera no copia la lista interior: pone tres referencias a la misma (el diagrama de la teoría 01). La comprehension ejecuta `[0] * 3` en cada vuelta y crea tres listas distintas.

### 2. Copia superficial y profunda

Descomenta el **PASO 2**:

```
original: {'Norte': [12.5, 48.9, 99.0], 'Sur': [8.0]}
copy():   {'Norte': [12.5, 48.9, 99.0], 'Sur': [8.0]}
deepcopy: {'Norte': [12.5, 48.9], 'Sur': [8.0]}
```

`.copy()` creó un diccionario nuevo, pero sus valores son las **mismas** listas: el `99.0` aparece también en la copia. `copy.deepcopy` copia también lo de dentro, a todos los niveles. Prueba `shallow["Este"] = [1.0]` y vuelve a imprimir `stations`: no tiene `Este`, porque el diccionario de fuera sí es otro. Deshaz el cambio.

### 3. No cambies una lista mientras la recorres

Descomenta el **PASO 3**:

```
Quitando dentro del for: [5, 70, 8]
Con comprehension:       [5, 8]
```

El `70` sobrevivió. El `for` avanza por posiciones: al quitar el `60` (posición 1), el `70` pasa a la posición 1, y la vuelta siguiente mira la posición 2, el `8`. Haz la tabla de traza de la semana 3 con la posición y la lista en cada vuelta si no lo ves. Arreglo: construir una lista nueva con los que se quedan.

### 4. Datos anidados

Descomenta el **PASO 4**:

```
  Norte   máximo 48.9 µg/m³
  Sur     máximo 9.5 µg/m³
  Centro  máximo sin dato
Segunda lectura del Norte: 48.9
```

Una lista de diccionarios es la forma que tiene un JSON (semana 7) y una fila de una API (semana 18). `measurements[0]["values"][1]` se lee de izquierda a derecha: el primer elemento de la lista, su clave `"values"` y la posición 1 de esa lista. El `if values else` evita `max([])`, que daría `ValueError: max() iterable argument is empty`.

### 5. Buscar en una lista o en un set

Descomenta el **PASO 5**:

```
list: 288.5 ms | set: 0.019 ms | ¿encontrada? True
El set fue unas 15,031 veces más rápido
```

Tus números serán otros, porque dependen de la máquina, pero la diferencia será de miles de veces. Para responder `in`, la lista compara elemento a elemento hasta encontrarlo (aquí, 200 000 comparaciones); el set calcula dónde debería estar y va directo. Prueba a buscar `"estación-0"`: la lista lo encuentra al primer intento y la diferencia casi desaparece. En la semana 6 le pondrás nombre: O(n) frente a O(1). Deshaz el cambio.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'copy' is not defined` | Borraste el `import copy` de arriba del archivo: vuelve a ponerlo |
| El PASO 5 tarda varios segundos | Tu máquina es más lenta: baja `200_000` a `20_000` |
| `ZeroDivisionError` en el PASO 5 | El set fue tan rápido que el tiempo dio 0: sube las vueltas de `200` a `2000` |
| `KeyError: 'value'` en el PASO 4 | La clave se llama `"values"`, en plural |
| El PASO 3 da `[5, 8]` en los dos casos | Cambiaste los datos: deben ser `[5, 60, 70, 8, 90]`, con dos valores altos seguidos |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Comprehensions](../ejercicio-03-comprehensions/README.md) | **Ejercicio 04 · Estructuras anidadas** | [Proyecto · Observatorio, capa 4](../../3-proyecto/README.md) |
