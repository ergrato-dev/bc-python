# Ejercicio 01 — Dunders

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-data-model-y-dunders.md) y [02](../../1-teoria/02-operadores-y-contenedores.md)

## Objetivo

Ver qué hace Python con una clase que no tiene ningún dunder y dárselos uno a uno: `__repr__` y `__str__` para imprimirla, `__eq__` y `__hash__` para compararla y meterla en un `set`, `__lt__` con `total_ordering` para ordenarla, `__add__` y `__radd__` para sumarla, y `__bool__` y `__len__` para usarla en un `if`. Son los métodos que gana `Measurement` y `Series` en tu proyecto. Ejercicio **guiado**: descomentas cada paso de `dunder_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-11-data_model_dunders_iteradores_y_generadores/2-practicas/ejercicio-01-dunders/starter
uv run python dunder_lab.py
```

```
Ejercicio 01 · Dunders
```

El paso 6 usa la clase del paso 1: descomenta en orden. Cada salida de abajo muestra solo las líneas nuevas del paso.

## Pasos

### 1. Una clase sin dunders

Descomenta el **PASO 1** y ejecuta:

```
¿Se imprime bien? True
¿Iguales? False
¿Tiene __eq__ propio? False
```

`print(plain)` daría algo como `<__main__.PlainReading object at 0x7f3a2c1b9e50>`: el `__repr__` que hereda de `object`, con una dirección de memoria que cambia en cada ejecución (por eso el paso solo comprueba que aparezca `object at 0x`). Y dos lecturas con los mismos datos **no** son iguales: el `__eq__` de `object` compara identidad, como `is`. Es lo que la semana 9 te ahorraba `@dataclass`; hoy lo escribes a mano para ver qué hay debajo.

### 2. `__repr__` y `__str__`

Descomenta el **PASO 2** y ejecuta:

```
Norte: 12.5 µg/m³
En un f-string: Norte: 12.5 µg/m³
repr: Reading('Norte', 12.5)
En una lista: [Reading('Norte', 12.5), Reading('Sur', 8.0)]
Con !r: Reading('Norte', 12.5)
```

`print` y los *f-strings* usan `__str__`: el texto para quien lee el informe. `repr()`, la consola y **los elementos de una lista** usan `__repr__`: el texto para quien programa, que dice qué objeto es. Fíjate en el `!r` dentro del `__repr__`: pone las comillas de `'Norte'`, así se ve que es un `str`. Si solo escribes `__repr__`, `print` lo usa también; si solo escribes `__str__`, la lista seguiría enseñando `<... object at 0x...>`.

### 3. `__eq__` y `__hash__`

Descomenta el **PASO 3** y ejecuta:

```
¿Iguales? True · ¿Igual a un str? False
__hash__ de Station: None
Error: cannot use 'Station' as a set element (unhashable type: 'Station')
En un set: 2 estaciones distintas
```

- Con `__eq__`, dos estaciones con el mismo código son iguales. Con un `str` devuelve `NotImplemented`: Python prueba entonces la comparación al revés y, si tampoco sirve, da `False`.
- Al definir `__eq__`, Python **borra** el `__hash__` heredado (`None`): dos objetos iguales deben tener el mismo *hash*, y el de `object` no lo garantiza. Sin `__hash__`, no entra en un `set` ni sirve de clave de un diccionario.
- `HashableStation` lo devuelve calculado con el mismo dato que compara `__eq__`, y el `set` ya ve dos estaciones iguales como una sola.

### 4. Ordenar con `__lt__` y `total_ordering`

Descomenta el **PASO 4** y ejecuta:

```
Ordenados: [Level('bajo'), Level('medio'), Level('alto')]
¿alto >= medio? True · máximo: Level('alto')
Métodos que añadió total_ordering: ['__ge__', '__gt__', '__le__']
```

`sorted`, `max` y `min` solo necesitan `<`, que es `__lt__`. El orden no es alfabético (sería `alto`, `bajo`, `medio`): es la posición en `NAMES`. `>=` no lo escribiste: `@total_ordering` deduce `__le__`, `__gt__` y `__ge__` a partir de `__eq__` y `__lt__`.

### 5. Operadores aritméticos y `NotImplemented`

Descomenta el **PASO 5** y ejecuta:

```
Suma: Distance(3.5) · Por 3: Distance(4.5)
Error: unsupported operand type(s) for +: 'Distance' and 'int'
Error con sum: unsupported operand type(s) for +: 'int' and 'Distance'
Con __radd__: Distance(4.0)
```

- `a + b` llama a `a.__add__(b)`; `a * 3`, a `a.__mul__(3)`. Devuelven un objeto **nuevo**: no cambian `a`.
- `Distance(1.5) + 1` devuelve `NotImplemented`, Python prueba `(1).__radd__(...)`, que tampoco sabe, y lanza el `TypeError`. Devolver `NotImplemented` (no lanzarlo) es lo que permite ese segundo intento.
- `sum` empieza en `0`: lo primero que hace es `0 + Distance(1.5)`. El `int` no sabe sumar distancias, así que Python busca `Distance.__radd__`, la suma **por la derecha**. `SummableDistance` la tiene y, cuando el otro operando es `0`, devuelve la distancia tal cual.

### 6. `__bool__` y `__len__` en un `if`

Descomenta el **PASO 6** y ejecuta:

```
  Inbox con 0: vacía
  Inbox con 1: hay avisos
¿Alarma con 55 sobre 50? True · ¿Con 12? False
¿Un objeto sin __bool__ ni __len__? True
```

Un `if objeto` pregunta primero por `__bool__` y, si no existe, por `__len__`: con `0` es falso. `Inbox` solo tiene `__len__` y ya funciona en un `if`, como una lista. `Alarm` decide con `__bool__` qué significa "verdadero". Un objeto sin ninguno de los dos siempre es verdadero, aunque su valor sea `0.0`. Tu `Series` vacía será falsa gracias a `__len__`, sin escribir `__bool__`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'PlainReading' is not defined` en el paso 6 | Descomenta antes el paso 1 |
| `print(reading)` sigue mostrando `object at 0x...` | El método se llama `__repr__` o `__str__`, con dos guiones bajos a cada lado, y va dentro de la clase |
| `RecursionError` en `__repr__` | Escribiste `{self!r}` dentro de `__repr__`: se llama a sí mismo. Usa los atributos, `{self.label!r}` |
| `ValueError: must define at least one ordering operation: < > <= >=` | `@total_ordering` no encuentra `__lt__`: falta o tiene otro nombre |
| `TypeError: Level.__lt__() takes 1 positional argument but 2 were given` | `__lt__` necesita dos parámetros: `self` y `other` |
| El `set` del paso 3 tiene 3 estaciones | `__hash__` no usa el mismo dato que `__eq__` |
| `sum` sigue fallando con `__radd__` | `__radd__` debe devolver `self` cuando `other == 0` y `NotImplemented` en el resto |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Pipelines perezosos](../../1-teoria/05-pipelines-perezosos.md) | **Ejercicio 01 · Dunders** | [Ejercicio 02 · Contenedores](../ejercicio-02-contenedores/README.md) |
