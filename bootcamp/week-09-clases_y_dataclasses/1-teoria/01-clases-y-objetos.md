# 01 · Clases y objetos

⏱️ 50 min

## 🎯 Objetivos

- Explicar qué es una clase y qué es un objeto (una instancia).
- Escribir una clase con `__init__`, atributos y métodos, y explicar qué es `self`.
- Explicar dónde guarda Python los atributos y en qué orden los busca.
- Distinguir atributos de instancia y atributos de clase, y evitar la lista compartida.

---

## 1. Por qué clases

Hasta ahora tu Observatorio guarda una medida como una tupla, `("Norte", 12.5)`, y pasa la unidad y los umbrales a cada función por separado: `process_lines(lines, UNIT, LOW, HIGH)`. Funciona, pero:

- `record[1]` no dice qué es: tienes que recordar que la posición 1 es el valor.
- La unidad y los umbrales siempre viajan juntos y nadie comprueba que `LOW` sea menor que `HIGH`.
- Las funciones que trabajan con registros están repartidas por cuatro módulos.

Una **clase** junta en un solo sitio unos datos y las funciones que trabajan con ellos. Ya usas muchas: `str`, `list`, `dict`, `Path`, `Counter`. `"norte".upper()` es una función (`upper`) que trabaja con un dato (el texto `"norte"`). Esta semana escribes las tuyas.

## 2. Clase y objeto

```python
class Sensor:
    """Un sensor de una estación de medida."""


north = Sensor()
south = Sensor()
type(north)               # <class '__main__.Sensor'>
isinstance(north, Sensor) # True
north is south            # False
```

`class Sensor:` define un **tipo** nuevo. Llamar a la clase, `Sensor()`, crea un **objeto** de ese tipo, también llamado **instancia**. La clase es el plano; cada objeto, una casa construida con ese plano: todas iguales en forma, cada una con sus muebles. Los nombres de clase van en `CamelCase` (PEP 8); los de funciones y variables, en `snake_case`, como hasta ahora.

## 3. `__init__` y `self`

```python
class Sensor:
    def __init__(self, name: str, unit: str) -> None:
        self.name = name
        self.unit = unit
        self.readings: list[float] = []


north = Sensor("Norte", "µg/m³")
north.name       # 'Norte'
vars(north)      # {'name': 'Norte', 'unit': 'µg/m³', 'readings': []}
```

`Sensor("Norte", "µg/m³")` hace dos cosas: crea un objeto vacío y llama a `__init__` con ese objeto como primer argumento y después los tuyos. **`self` es el objeto que se está creando**. Cada `self.algo = valor` le pone un **atributo**. `__init__` no crea el objeto ni devuelve nada: lo deja preparado, con todos los atributos que va a tener, para que no haya sensores a medio hacer.

`self` es solo un nombre, pero todo el mundo usa ese: no lo cambies.

## 4. Métodos

```python
class Sensor:
    def __init__(self, name: str, unit: str) -> None:
        self.name = name
        self.unit = unit
        self.readings: list[float] = []

    def record(self, value: float) -> None:
        self.readings.append(value)

    def mean(self) -> float:
        if not self.readings:
            return 0.0
        return sum(self.readings) / len(self.readings)


north = Sensor("Norte", "µg/m³")
north.record(12.5)        # es lo mismo que Sensor.record(north, 12.5)
north.mean()              # 12.5
```

Un **método** es una función escrita dentro de la clase. Al escribir `north.record(12.5)`, Python busca `record` en la clase de `north` y lo llama pasando `north` como `self`. Por eso **todo método recibe `self` como primer parámetro**: es la forma de llegar a los atributos del objeto (`self.readings`) y a sus otros métodos (`self.mean()`). Si se te olvida, el error dice que le sobra un argumento: `takes 1 positional argument but 2 were given`.

Cada sensor tiene su propia lista `readings`: lo que añades a `north` no aparece en otro sensor.

## 5. Dónde viven los atributos

Cada objeto guarda sus atributos en un diccionario propio, su `__dict__`, que es lo que enseña `vars(objeto)`. Los métodos **no** están ahí: están una sola vez en la clase, que también tiene su `__dict__`, y los comparten todos los objetos.

Al leer `north.algo`, Python busca:

1. En el objeto (`vars(north)`).
2. Si no está, en la clase (`vars(Sensor)`).
3. Si tampoco, `AttributeError: 'Sensor' object has no attribute 'algo'`.

![La clase Sensor con su atributo de clase kind y sus métodos __init__, record y mean, y dos objetos, north y south, cada uno con su propio __dict__ (name, unit, readings). Al leer north.kind, Python mira primero en el objeto y después en la clase; north.kind = "agua" escribe en el objeto](../0-assets/01-objeto-y-clase.svg)

## 6. Atributos de clase

Un atributo escrito en la clase, fuera de los métodos, es un **atributo de clase**: hay uno solo, compartido por todos los objetos.

```python
class Sensor:
    kind = "aire"         # atributo de clase
    created = 0

    def __init__(self, name: str) -> None:
        self.name = name  # atributo de instancia
        Sensor.created += 1
```

Leer `north.kind` lo encuentra en la clase (paso 2 de la búsqueda). Pero **asignar** siempre escribe en el objeto: `north.kind = "agua"` crea un `kind` propio de `north`, que tapa el de la clase; los demás sensores siguen viendo `"aire"`. Por eso el contador se escribe `Sensor.created += 1`: `self.created += 1` leería el 0 de la clase y crearía un `created` en cada objeto, y el de la clase seguiría en 0.

Úsalos para constantes que tienen que ver con la clase. Para lo que es de cada objeto, `__init__`.

## 7. La lista compartida

```python
class SharedSensor:
    readings: list[float] = []      # ⚠️ una sola lista para todos

    def __init__(self, name: str) -> None:
        self.name = name

    def record(self, value: float) -> None:
        self.readings.append(value)


east, west = SharedSensor("Este"), SharedSensor("Oeste")
east.record(20.0)
west.readings                       # [20.0]
```

`self.readings.append(...)` no asigna nada: **lee** `readings`, que encuentra en la clase, y cambia esa lista. Todos los sensores escriben en la misma. Es el mismo problema que el valor por defecto mutable que encontró ruff en la semana 8 (`def f(items=[])`, la regla `B006`). El arreglo es el mismo: crear la lista en `__init__`, una por objeto. `@dataclass` te obliga a hacerlo bien (teoría 03).

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `TypeError: Sensor() takes no arguments` | La clase no tiene `__init__`, o está mal escrito (`__int__`, `_init_`) | `def __init__(self, ...)`, con dos guiones bajos a cada lado |
| `TypeError: Sensor.record() takes 1 positional argument but 2 were given` | Al método le falta `self` | `def record(self, value)` |
| `NameError: name 'readings' is not defined` dentro de un método | Escribiste `readings` en lugar de `self.readings` | Los atributos se leen siempre a través de `self` |
| `AttributeError: 'Sensor' object has no attribute 'unit'` | El atributo no se creó en `__init__`, o tiene otro nombre | Crea en `__init__` todos los atributos del objeto |
| Todos los objetos ven los mismos datos | Una lista o un diccionario como atributo de clase | Créalo en `__init__` con `self.` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué es una clase, qué es un objeto y cómo se crea uno.
- [ ] Qué hace `__init__` y qué es `self`.
- [ ] Por qué todo método recibe `self` y qué significa `north.record(12.5)`.
- [ ] Dónde guarda Python los atributos de un objeto y en qué orden los busca.
- [ ] La diferencia entre un atributo de clase y uno de instancia, y qué pasa al asignar.
- [ ] Por qué una lista como atributo de clase se comparte entre todos los objetos.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 09](../README.md) | **01 · Clases y objetos** | [02 · Propiedades y métodos especiales](02-propiedades-y-metodos-especiales.md) |
