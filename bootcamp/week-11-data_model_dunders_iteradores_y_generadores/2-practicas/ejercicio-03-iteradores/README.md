# Ejercicio 03 — Iteradores

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-iteradores.md)

## Objetivo

Recorrer una lista a mano con `iter()` y `next()`, escribir el `for` como un `while`, crear un iterador como clase y ver por qué se agota, y separar el **iterable** (lo que se puede recorrer muchas veces) del **iterador** (el cursor que avanza una sola vez). Terminas con los iteradores de la biblioteca estándar, que se gastan igual. Ejercicio **guiado**: descomentas cada paso de `iterator_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-11-data_model_dunders_iteradores_y_generadores/2-practicas/ejercicio-03-iteradores/starter
uv run python iterator_lab.py
```

```
Ejercicio 03 · Iteradores
```

Cada paso usa lo de los anteriores: descomenta en orden. Cada salida de abajo muestra solo las líneas nuevas del paso.

## Pasos

### 1. `iter()` y `next()` a mano

Descomenta el **PASO 1** y ejecuta:

```
Tipo: list_iterator
next: 12.5 8.0 55.1
StopIteration: no quedan valores
¿Con valor por defecto? fin
```

`iter(values)` no copia la lista: crea un **cursor** (`list_iterator`) que recuerda por dónde va. Cada `next()` da el siguiente valor y avanza. Cuando no queda nada, `next()` lanza `StopIteration`; con un segundo argumento, `next(cursor, "fin")`, devuelve ese valor en lugar de lanzar.

### 2. Lo que hace un `for` por dentro

Descomenta el **PASO 2** y ejecuta:

```
  a mano: 12.5
  a mano: 8.0
  a mano: 55.1
¿Una lista es su propio iterador? False
¿Un iterador lo es? True
```

Un `for` es exactamente ese `while`: pide un iterador con `iter()`, llama a `next()` en cada vuelta y termina al recibir `StopIteration`, que el `for` captura sin que lo veas. La lista y su iterador son objetos distintos; el iterador, en cambio, devuelve **a sí mismo** cuando le pides `iter()`. Por eso un `for` acepta las dos cosas.

### 3. Un iterador escrito como clase

Descomenta el **PASO 3** y ejecuta:

```
Cuenta atrás: [3, 2, 1]
Otra vez: []
```

Un iterador necesita dos métodos: `__iter__`, que devuelve `self`, y `__next__`, que da el siguiente valor o lanza `StopIteration`. `Countdown` guarda su estado en `self.current`. Al terminar la primera vuelta, `current` vale `0` y se queda así: la segunda `list(countdown)` no da nada. Un iterador se **agota** y no vuelve a empezar.

### 4. Iterable frente a iterador

Descomenta el **PASO 4** y ejecuta:

```
Primera: [3, 2, 1] · segunda: [3, 2, 1]
Parejas: [(3, 2), (3, 1), (2, 1)]
Parejas con un iterador: [(3, 2), (3, 1)]
```

`Launch` es un **iterable**: su `__iter__` crea una `Countdown` **nueva** cada vez, así que se recorre las veces que quieras, y dos bucles anidados no se estorban. Con un solo iterador, el bucle de dentro se come los valores del de fuera: con `a = 3`, el interior consume `2` y `1`, y el exterior ya no tiene más vueltas. Es el mismo reparto que hay entre una lista (iterable) y su `list_iterator`, y el que tendrá tu `Series`: cada `for` sobre ella empieza desde el principio.

### 5. Los iteradores de la biblioteca estándar

Descomenta el **PASO 5** y ejecuta:

```
zip es: zip · ¿iterador? True
Primera vuelta: [('Norte', 12.5), ('Sur', 8.0), ('Centro', 55.1)]
Segunda vuelta: []
map: 12 y luego [8, 55]
enumerate: (1, 'Norte') · queda: [(2, 'Sur'), (3, 'Centro')]
¿Un archivo es un iterador? True
Primera línea: Norte;12,5
Las demás: ['Sur;8', 'Centro;NA']
```

`zip`, `map` y `enumerate` no devuelven listas: devuelven iteradores que calculan cada elemento cuando se lo pides, y se agotan tras una vuelta. Un archivo abierto también es un iterador de líneas: después de `next(file)`, el `for` sigue desde la segunda. (`round(12.5)` da `12` porque Python redondea al par en los empates.) Si necesitas recorrer el resultado dos veces, guárdalo antes en una lista.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'values' is not defined` | Descomenta antes el paso 1 |
| `NameError: name 'Countdown' is not defined` en el paso 4 | Descomenta antes el paso 3 |
| `TypeError: iter() returned non-iterator of type 'Countdown'` | Falta `__next__` en `Countdown`, o tiene otro nombre |
| La cuenta atrás no termina nunca | `__next__` no lanza `StopIteration` al llegar a `0`, o no resta `1` |
| `FileNotFoundError: ... 'medidas.txt'` | Ejecuta desde la carpeta `starter`, donde está `medidas.txt` |
| La segunda vuelta de `zip` sale llena | Creaste el `zip` dos veces; con uno solo, la segunda vuelta está vacía |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Contenedores](../ejercicio-02-contenedores/README.md) | **Ejercicio 03 · Iteradores** | [Ejercicio 04 · Generadores](../ejercicio-04-generadores/README.md) |
