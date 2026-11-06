# 02 · Tuplas y desempaquetado

⏱️ 35 min

## 🎯 Objetivos

- Crear tuplas y explicar en qué se diferencian de las listas.
- Desempaquetar una tupla, también con `*` y en un `for`.
- Usar una tupla como registro y anotar su tipo.

---

## 1. Qué es una tupla

Una tupla es una secuencia **inmutable**: se crea con sus elementos y ya no cambia.

```python
station = ("Norte", 12.5, "µg/m³")
station[0]          # 'Norte'
len(station)        # 3
station[1] = 13.0   # TypeError: 'tuple' object does not support item assignment
```

Se lee como una lista (índices, trozos, `in`, `for`, `len`), pero no tiene `append`, `remove` ni `sort`.

| Escribes | Obtienes |
|---|---|
| `(1, 2)` o `1, 2` | Una tupla de dos: la coma hace la tupla, no los paréntesis |
| `(1,)` | Una tupla de uno; la coma es obligatoria |
| `(1)` | El número `1`, entre paréntesis |
| `()` | La tupla vacía |

En la semana 4 ya las usaste sin nombrarlas: `return hours, minutes` devuelve una tupla.

## 2. Lista o tupla

| | Lista | Tupla |
|---|---|---|
| Cambia después de crearse | Sí | No |
| Uso típico | Muchos elementos del **mismo** tipo, cuántos no se sabe: las lecturas de un archivo | Pocas partes de tipos **distintos**, siempre las mismas: un registro (etiqueta, valor) |
| Anotación | `list[float]`: cualquier longitud | `tuple[str, float]`: exactamente dos partes, en ese orden |
| Clave de diccionario o elemento de un set | No | Sí, si lo de dentro tampoco cambia (teoría 03) |

En el proyecto, un registro es `("Norte", 12.5)` y un archivo es una **lista de tuplas**. Para no repetir la anotación, el proyecto le pone nombre:

```python
Record = tuple[str, float | None]

def records_of(lines: Iterable[str]) -> list[Record]: ...
```

`Record` es un **alias de tipo**: otro nombre para la misma anotación.

## 3. Desempaquetar

Repartir las partes de una secuencia en varios nombres:

```python
label, value, unit = station
low, high = 10.0, 50.0
low, high = high, low          # intercambio: primero se crea la tupla (high, low)
```

Tiene que haber tantos nombres como partes; si no, `ValueError: too many values to unpack` (o `not enough`). Con `*`, un nombre recoge lo que sobra, en una lista:

```python
first, *rest = [3, 1, 4, 1, 5]      # first = 3, rest = [1, 4, 1, 5]
*_, last = [3, 1, 4, 1, 5]          # last = 5
```

`_` es el nombre que se usa, por convención, para lo que no te interesa.

**En un `for`.** Si cada elemento es una tupla, el `for` la desempaqueta en cada vuelta. Es lo que hacías con `enumerate` y `zip` en la semana 3: dan tuplas.

```python
records = [("Norte", 12.5), ("Sur", 8.0)]
for label, value in records:
    print(label, value)
```

**En un `match`.** El `case [label, text]` de la semana 2 era otra forma de desempaquetar, con comprobación de longitud incluida.

## 4. Las tuplas también se comparan

Dos tuplas se comparan elemento a elemento, de izquierda a derecha, como las palabras en un diccionario:

```python
("Norte", 12.5) < ("Sur", 1.0)     # True: "Norte" < "Sur", ya no mira el resto
(5, "Sur") < (5, "Este")           # False: empatan en 5; "Sur" > "Este"
```

Por eso `sorted(records)` ordena por la etiqueta, y por eso un `key` que devuelve una tupla ordena por varios criterios (teoría 01).

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `TypeError: 'tuple' object does not support item assignment` | Intentas cambiar una tupla | Crea otra: `(label, new_value)` |
| `ValueError: too many values to unpack (expected 2, got 3)` | Más partes que nombres | Ajusta los nombres o usa `*rest` |
| `x = (5)` no es una tupla | Sin coma no hay tupla | `x = (5,)` |
| `TypeError: '<' not supported between instances of 'float' and 'NoneType'` al ordenar tuplas | Empatan en la primera parte y la segunda tiene `None` | Usa `key` para decidir por qué se ordena |

## ✅ Qué debes saber al terminar

- [ ] Qué diferencia una tupla de una lista y cuándo usar cada una.
- [ ] Cómo se escribe una tupla de un elemento.
- [ ] Cómo desempaquetar con y sin `*`, también en un `for`.
- [ ] Cómo se comparan dos tuplas.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · Listas](01-listas.md) | **02 · Tuplas y desempaquetado** | [03 · Diccionarios](03-diccionarios.md) |
