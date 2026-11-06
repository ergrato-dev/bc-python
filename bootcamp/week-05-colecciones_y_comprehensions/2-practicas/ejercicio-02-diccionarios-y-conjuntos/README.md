# Ejercicio 02 — Diccionarios y conjuntos

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-diccionarios.md) y [04](../../1-teoria/04-conjuntos.md)

## Objetivo

Guardar y buscar por clave, contar y agrupar con un diccionario, y quitar repetidos y comparar grupos con conjuntos. Son las dos operaciones del proyecto de esta semana. Ejercicio **guiado**: descomentas cada paso de `dicts_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-05-colecciones_y_comprehensions/2-practicas/ejercicio-02-diccionarios-y-conjuntos/starter
uv run python dicts_lab.py
```

```
Ejercicio 02 · Diccionarios y conjuntos
```

## Pasos

### 1. Leer por clave

Descomenta el **PASO 1** y ejecuta:

```
aire: µg/m³ | claves: 3
¿ruido? True | ¿luz? False
luz con get: None | con defecto: sin unidad
```

`in` pregunta por las **claves**, no por los valores: `"dB" in units` da `False`. Prueba `print(units["luz"])`: `KeyError: 'luz'`. Usa `[clave]` cuando la clave tiene que estar (si falta, es un error que quieres ver) y `.get` cuando puede faltar. Deshaz el cambio.

### 2. Añadir, cambiar, borrar y recorrer

Descomenta el **PASO 2**:

```
  aire  µg/m³
  agua  mg/l
  luz   lx
```

El diccionario recuerda el orden en que entró cada clave: `agua` cambió de valor pero conserva su sitio, y `luz` va al final. `.items()` da parejas `(clave, valor)` que el `for` desempaqueta, como las tuplas del ejercicio 01.

### 3. Contar

Descomenta el **PASO 3**:

```
Conteo: {'alto': 3, 'bajo': 2, 'medio': 1}
Más frecuente: alto
```

La primera vez que llega `"alto"`, `counts.get("alto", 0)` da `0` y se guarda `1`; las siguientes suma uno. `max` recorre las claves y las compara por su conteo gracias a `key`. Es `level_counts` del proyecto, salvo que allí las claves ya existen desde el principio.

### 4. Agrupar

Descomenta el **PASO 4**:

```
Grupos: {'Norte': [12.5, 48.9], 'Sur': [8.0, 9.5], 'Este': [30.0]}
  Norte: media 30.70 de 2
  Sur: media 8.75 de 2
  Este: media 30.00 de 1
```

`groups.setdefault(label, [])` devuelve la lista de esa etiqueta, y si no existía la crea vacía y la guarda. El `.append(value)` va sobre esa lista, que vive dentro del diccionario. Esto es un **agrupar por** (*group by*): lo que hace `values_by_label` en el proyecto y `groupby` en pandas en la semana 24.

### 5. Una tupla como clave

Descomenta el **PASO 5**:

```
Norte el martes: 14.0
```

Una pareja (lugar, día) identifica cada medida. Prueba `bad = {["Norte", "lunes"]: 12.5}`:

```
TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
```

Una clave no puede cambiar después de guardarse, porque el diccionario la busca por su valor. Una lista puede cambiar; una tupla, no. Deshaz el cambio.

### 6. Conjuntos

Descomenta el **PASO 6**:

```
Ambos días: ['Este', 'Sur']
Alguno: ['Este', 'Norte', 'Oeste', 'Sur']
Solo lunes: ['Norte']
Distintas: 3 | ¿Sur? True
Vacíos: <class 'dict'> <class 'set'>
```

`&` es la intersección (en los dos), `|` la unión (en alguno) y `-` la diferencia (en el primero y no en el segundo). `set(labels)` quita los repetidos. Prueba `print(monday)` y ejecuta dos o tres veces: el orden puede cambiar de una ejecución a otra, porque un conjunto no guarda orden. Por eso aquí se muestran con `sorted`. Deshaz el cambio. La última línea recuerda que `{}` es un diccionario vacío; el conjunto vacío se escribe `set()`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `KeyError: 'luz'` en el PASO 2 | Ejecutaste el `del` o la lectura antes de añadir: los pasos van en orden |
| `TypeError: unhashable type: 'list'` | Usaste una lista como clave o como elemento de un set: usa una tupla |
| `AttributeError: 'NoneType' object has no attribute 'append'` | Escribiste `groups.get(label).append(...)`: `get` no crea la lista; usa `setdefault` |
| Los conjuntos salen en otro orden | Es normal: compara el contenido o muéstralos con `sorted` |
| `TypeError: 'set' object is not subscriptable` | Un set no tiene posiciones: no admite `[0]`; conviértelo con `sorted` si necesitas orden |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Listas y tuplas](../ejercicio-01-listas-y-tuplas/README.md) | **Ejercicio 02 · Diccionarios y conjuntos** | [Ejercicio 03 · Comprehensions](../ejercicio-03-comprehensions/README.md) |
