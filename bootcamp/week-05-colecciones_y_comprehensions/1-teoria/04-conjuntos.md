# 04 · Conjuntos

⏱️ 30 min

## 🎯 Objetivos

- Crear conjuntos y quitar repetidos con ellos.
- Usar las operaciones de unión, intersección y diferencia.
- Saber cuándo un conjunto es mejor que una lista.

---

## 1. Qué es un conjunto

Un conjunto (`set`) guarda elementos **sin repetir** y **sin orden**:

```python
labels = {"Norte", "Sur", "Norte"}
print(labels)            # {'Sur', 'Norte'}  (u otro orden)
len(labels)              # 2
"Sur" in labels          # True
set(["a", "b", "a"])     # {'a', 'b'}: quita los repetidos de una lista
empty = set()            # {} sería un diccionario vacío
```

Por dentro funciona como las claves de un diccionario, sin valores: cada elemento se guarda por su hash (teoría 03). De ahí sus tres propiedades:

| Propiedad | Consecuencia |
|---|---|
| Sin repetidos | Añadir un elemento que ya está no hace nada |
| Sin orden | No hay `labels[0]` (`TypeError: 'set' object is not subscriptable`); el orden al imprimir puede cambiar entre ejecuciones |
| Elementos hashables | Textos, números y tuplas sí; listas no |
| `in` casi instantáneo | Buscar en un set de un millón tarda lo mismo que en uno de diez |

El orden de un set de textos cambia de una ejecución a otra a propósito: Python mezcla los hashes de los textos al arrancar, por seguridad. Para mostrar un conjunto, ordénalo con `sorted`; para compararlo en un test, compáralo con otro set: `{"Norte", "Sur"} == {"Sur", "Norte"}` es `True`.

## 2. Cambiar un conjunto

| Método | Qué hace |
|---|---|
| `labels.add("Este")` | Añade uno |
| `labels.update(["Este", "Oeste"])` | Añade varios |
| `labels.discard("Este")` | Quita, y no falla si no estaba |
| `labels.remove("Este")` | Quita, y da `KeyError` si no estaba |

## 3. Operaciones

```python
monday = {"Norte", "Sur", "Este"}
tuesday = {"Sur", "Este", "Oeste"}
```

| Operación | Resultado | Pregunta que responde |
|---|---|---|
| `monday \| tuesday` | `{'Norte', 'Sur', 'Este', 'Oeste'}` | ¿Qué estaciones midieron algún día? |
| `monday & tuesday` | `{'Sur', 'Este'}` | ¿Cuáles midieron los dos días? |
| `monday - tuesday` | `{'Norte'}` | ¿Cuáles midieron el lunes y no el martes? |
| `monday ^ tuesday` | `{'Norte', 'Oeste'}` | ¿Cuáles midieron un solo día? |
| `{"Sur"} <= monday` | `True` | ¿Todas estas están en el lunes? |

Son las preguntas típicas al limpiar datos: qué categorías aparecen en un archivo y no en otro, qué etiquetas tienen un nombre mal escrito.

## 4. ¿Lista o conjunto?

| Necesitas | Usa |
|---|---|
| Guardar en orden, con repetidos | Lista |
| Saber cuántos **distintos** hay | `len(set(lista))` |
| Preguntar muchas veces "¿está?" | Set |
| Quitar repetidos **conservando el orden** | `list(dict.fromkeys(lista))`: las claves de un diccionario no se repiten y sí guardan el orden |
| Comparar dos grupos | Operaciones de set |

En el proyecto, `distinct_labels` devuelve un set y el informe muestra cuántas etiquetas distintas hay.

`frozenset` es la versión inmutable del set; se usa cuando necesitas un conjunto como clave de un diccionario. No la necesitarás estas semanas.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `{}` resulta ser un diccionario | Las llaves vacías son un diccionario | `set()` |
| `TypeError: 'set' object is not subscriptable` | Los sets no tienen posiciones | `sorted(s)[0]`, o usa una lista |
| Un test falla porque el orden cambia | Comparas `list(s)` con una lista | Compara sets, o `sorted(s)` |
| `TypeError: unhashable type: 'list'` | Metiste una lista en un set | Usa una tupla |
| `set("Norte")` da `{'N', 'o', 'r', 't', 'e'}` | `set` recorre el texto letra a letra | `{"Norte"}` |

## ✅ Qué debes saber al terminar

- [ ] Las tres propiedades de un set y de dónde salen.
- [ ] Qué responden `|`, `&` y `-`.
- [ ] Cómo crear un set vacío.
- [ ] Cuándo un set es mejor que una lista, y cómo quitar repetidos sin perder el orden.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Diccionarios](03-diccionarios.md) | **04 · Conjuntos** | [05 · Comprehensions](05-comprehensions.md) |
