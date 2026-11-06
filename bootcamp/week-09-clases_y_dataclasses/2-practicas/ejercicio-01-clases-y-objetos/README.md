# Ejercicio 01 — Clases y objetos

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-clases-y-objetos.md)

## Objetivo

Crear una clase y sus objetos, escribir `__init__` y métodos con `self`, ver dónde guarda Python los atributos y distinguir los atributos de cada objeto de los de la clase. Terminas con el error más común de las clases: una lista que comparten todos los objetos sin querer. Ejercicio **guiado**: descomentas cada paso de `objects_lab.py` y de `sensor.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-09-clases_y_dataclasses/2-practicas/ejercicio-01-clases-y-objetos/starter
uv run python objects_lab.py
```

```
Ejercicio 01 · Clases y objetos
```

Hay dos archivos: `sensor.py` define las clases `Sensor` y `SharedSensor`, y `objects_lab.py` las usa. Los pasos te dicen en qué orden descomentar cada uno.

## Pasos

### 1. Una clase vacía y sus objetos

Descomenta el **PASO 1** de `objects_lab.py` y ejecuta:

```
Tipo de north: Station
¿north es una Station? True
¿north y south son el mismo objeto? False
Atributos de north: {'city': 'Lima'}
Atributos de south: {}
```

`class Station:` crea un tipo nuevo, igual que `int` o `str` son tipos. Cada llamada `Station()` crea un **objeto** (una **instancia**) distinto de ese tipo: `north` y `south` son dos objetos, no el mismo. `north.city = "Lima"` le pone un atributo solo a `north`, y `vars()` enseña dónde lo guarda: en un diccionario de cada objeto, su `__dict__`. El de `south` sigue vacío.

### 2. `__init__` y `self`

Descomenta solo el **PASO 2** de `objects_lab.py` y ejecuta:

```
TypeError: Sensor() takes no arguments
```

`Sensor` todavía no dice qué hacer con `"Norte"` y `"µg/m³"`. Descomenta también el **PASO 2** de `sensor.py` y ejecuta:

```
  [creado el sensor Norte]
  [creado el sensor Sur]
Nombre de north: Norte
Atributos de south: {'name': 'Sur', 'unit': 'µg/m³', 'readings': []}
  [creado el sensor Este]
  [creado el sensor Este]
¿Iguales? False
```

`Sensor("Norte", "µg/m³")` crea un objeto vacío y llama a `__init__` con ese objeto como primer argumento, `self`, y después `"Norte"` y `"µg/m³"`. Cada `self.algo = ...` guarda un atributo en el objeto que se está creando. Así todos los sensores nacen con los mismos atributos, cada uno con sus valores.

La última línea sorprende: dos sensores con los mismos datos **no** son iguales. Si la clase no dice cómo comparar, `==` compara la identidad, como `is`: son dos objetos distintos. Lo arreglarás en el ejercicio 02, y `@dataclass` lo hace solo en el 03.

### 3. Métodos

Descomenta el **PASO 3** de `sensor.py`, después el de `objects_lab.py`, y ejecuta. A la salida anterior se añade:

```
Norte: 2 lecturas, media 30.7 µg/m³
Sur: 2 lecturas, media 8.5 µg/m³
Lo mismo, llamado desde la clase: 30.7
```

Un **método** es una función escrita dentro de la clase. `north.record(12.5)` es lo mismo que `Sensor.record(north, 12.5)`: Python pasa el objeto de la izquierda del punto como `self`, y la última línea lo hace a mano. Por eso cada método recibe `self` y lo usa para llegar a los atributos del objeto (`self.readings`) y a sus otros métodos (`self.mean()`). Cada sensor tiene su propia lista: las lecturas de `north` no se mezclan con las de `south`.

### 4. Atributos de clase

Descomenta los **dos** bloques del **PASO 4** de `sensor.py`: el de arriba, dentro de la clase, y la línea `Sensor.created += 1`, que queda dentro de `__init__`. Después, el de `objects_lab.py`. Ejecuta:

```
Sensores creados: 4
Clase de medida de north: aire · de south: aire
Tras cambiar north.kind: agua · aire · aire
¿kind está en vars(north)? True · ¿y en vars(south)? False
```

`kind` y `created` están escritos en la clase, fuera de los métodos: son **atributos de clase**, uno solo para todos los sensores. Cuentan 4 porque los dos sensores `"Este"` del paso 2 también se crearon. Al leer `south.kind`, Python busca primero en el objeto; si no está, en la clase. Pero `north.kind = "agua"` **escribe** en el objeto: `north` gana su propio `kind`, que tapa el de la clase, y `south` y `Sensor` siguen con `"aire"`. Por eso el contador se escribe `Sensor.created += 1` y no `self.created += 1`: así cambia el de la clase.

### 5. Una lista compartida sin querer

Descomenta el **PASO 5** de `sensor.py`, después el de `objects_lab.py`, y ejecuta:

```
Lecturas de west: [20.0]
¿La misma lista? True
```

`west` tiene una lectura que nunca le diste. En `SharedSensor`, `readings = []` está en la clase, así que hay **una** lista para todos. `east.readings.append(...)` no escribe un atributo nuevo en `east`: lee `readings`, que encuentra en la clase, y cambia esa lista. Con números o textos no pasa, porque no se pueden cambiar por dentro; con listas y diccionarios, sí. Lo que es de cada objeto se crea en `__init__` (`self.readings = []`), como en `Sensor`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: Sensor() takes no arguments` | Falta descomentar el PASO 2 de `sensor.py`: es lo que muestra el paso 2 |
| `AttributeError: 'Sensor' object has no attribute 'record'` | Falta descomentar el PASO 3 de `sensor.py` |
| `TypeError: Sensor.record() takes 1 positional argument but 2 were given` | A un método le falta `self` como primer parámetro |
| `IndentationError` en `sensor.py` | Al descomentar quitaste espacios: los métodos van con 4 espacios y su cuerpo con 8 |
| `AttributeError: type object 'Sensor' has no attribute 'created'` | Descomentaste la línea de `__init__` del PASO 4 pero no el bloque de arriba |
| `Sensores creados` no es 4 | Has creado más o menos sensores en los pasos 2 y 3: está bien, cuenta los tuyos |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Elegir el modelo](../../1-teoria/05-elegir-el-modelo.md) | **Ejercicio 01 · Clases y objetos** | [Ejercicio 02 · Propiedades y métodos especiales](../ejercicio-02-propiedades-y-metodos-especiales/README.md) |
