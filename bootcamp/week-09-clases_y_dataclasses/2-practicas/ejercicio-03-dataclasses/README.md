# Ejercicio 03 — `dataclasses`

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-dataclasses.md) y [04](../../1-teoria/04-dataclasses-inmutables-y-con-slots.md)

## Objetivo

Declarar clases de datos con `@dataclass`: campos con valores por defecto, listas con `field(default_factory=...)`, validación en `__post_init__` y objetos inmutables y ordenables con `frozen=True` y `order=True`. Es lo que usa el modelo del proyecto (`Scale`, `Measurement`, `Series`). Ejercicio **guiado**: descomentas cada paso de `dataclasses_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-09-clases_y_dataclasses/2-practicas/ejercicio-03-dataclasses/starter
uv run python dataclasses_lab.py
```

```
Ejercicio 03 · dataclasses
```

Cada paso define sus propias clases, así que puedes descomentarlos de uno en uno, en orden.

## Pasos

### 1. `@dataclass` escribe los métodos por ti

Descomenta el **PASO 1** y ejecuta:

```
Station(name='Norte', city='Lima', altitude=154)
¿Iguales? True
Campos: ['name', 'city', 'altitude']
Tras cambiarla: 160
```

En la clase solo hay tres líneas, `nombre: tipo`, y sin embargo `Station("Norte", "Lima", 154)` funciona, se imprime con sus datos y `==` compara los campos. `@dataclass` lee los campos declarados y **genera** `__init__`, `__repr__` y `__eq__`, los tres métodos que escribiste a mano en el ejercicio 02. `fields()` devuelve los campos en orden de declaración, que es también el orden de los argumentos del `__init__`. El objeto se puede cambiar como cualquier otro.

Los tipos son obligatorios para que la línea sea un campo, pero Python no los comprueba al crear el objeto: `Station("Norte", "Lima", "alta")` no falla. Para eso está mypy, y en la semana 13, Pydantic.

### 2. Valores por defecto

Descomenta el **PASO 2** y ejecuta:

```
Sensor(name='PM2.5', unit='µg/m³', active=True)
Sensor(name='Temperatura', unit='°C', active=False)
Error: non-default argument 'name' follows default argument 'unit'
```

Un campo con `= valor` tiene valor por defecto, igual que un parámetro de función. Y con la misma regla: como el `__init__` generado sigue el orden de los campos, los campos sin valor por defecto van **antes** que los que lo tienen. `Broken` rompe la regla y `@dataclass` falla al crear la clase, no al usarla.

### 3. Una lista por defecto

Descomenta el **PASO 3** y ejecuta:

```
Error: mutable default <class 'list'> for field stops is not allowed: use default_factory
Route(name='Mañana', stops=['Norte'])
Route(name='Tarde', stops=[])
```

Es la trampa del paso 5 del ejercicio 01: `= []` crearía **una** lista para todos los objetos. `@dataclass` lo detecta y no te deja. `field(default_factory=list)` dice "llama a `list()` cada vez que se cree un objeto sin este argumento": cada ruta tiene su propia lista, y lo que añades a `morning` no aparece en `evening`. Vale cualquier función sin argumentos: `dict`, `set` o una tuya.

### 4. `__post_init__`

Descomenta el **PASO 4** y ejecuta:

```
Reading(label='Norte', value=48.9, level='normal')
Reading(label='Centro', value=61.2, level='alto')
Error: lectura negativa en Sur: -3.0
```

El `__init__` lo genera `@dataclass`, así que tu código va en `__post_init__`, que se ejecuta justo después. Sirve para dos cosas: **validar** (una lectura negativa no llega a existir) y **calcular** campos a partir de otros. `field(init=False)` saca `level` del `__init__`: no se pasa al crear la lectura, la calcula `__post_init__`, pero sigue siendo un campo y sale en el `repr`. En el proyecto, `Scale.__post_init__` rechaza unos umbrales imposibles.

### 5. `frozen`, `order`, `replace` y `asdict`

Descomenta el **PASO 5** y ejecuta:

```
Error: cannot assign to field 'minor'
Siguiente: Version(major=0, minor=9, patch=0) · la de antes sigue: Version(major=0, minor=8, patch=0)
Ordenadas: [Version(major=0, minor=9, patch=0), Version(major=0, minor=10, patch=0), Version(major=1, minor=0, patch=0)]
En un set: {Version(major=0, minor=8, patch=0)}
Como JSON: {"major": 0, "minor": 9, "patch": 0}
```

- `frozen=True` hace el objeto **inmutable**: asignar a un campo lanza `FrozenInstanceError`. Para "cambiar" una versión, `replace()` crea otra con el campo nuevo, y la original sigue igual.
- Como ya no puede cambiar, `@dataclass` le da un `__hash__`: dos versiones iguales tienen el mismo *hash*, y el `set` se queda con una. Es lo que perdió el termómetro del ejercicio 02 al definir `__eq__`.
- `order=True` genera `<`, `<=`, `>` y `>=`, que comparan los campos en orden, como tuplas: 0.10.0 va detrás de 0.9.0, cosa que no pasaría comparando los textos `"0.10.0"` y `"0.9.0"`.
- `asdict()` convierte el objeto en un diccionario, listo para `json.dumps` o el `write_json` de tu proyecto.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: Station.__init__() missing 1 required positional argument: 'altitude'` | Faltan argumentos al crear el objeto: van en el orden de los campos |
| `NameError: name 'field' is not defined` | Borraste algún nombre del `from dataclasses import ...` de arriba |
| `IndentationError` | Al descomentar, el `@dataclass` y la clase del `try` deben quedar con 4 espacios dentro del `try` |
| Un campo no sale en el `repr` ni en el `__init__` | Le falta el tipo: `name = "x"` es un atributo de clase; `name: str = "x"` es un campo |
| `AttributeError: 'Reading' object has no attribute 'level'` | `__post_init__` no asignó `self.level`, o el nombre del método está mal escrito: `__post_init__`, con dos guiones bajos a cada lado |
| `TypeError: '<' not supported between instances of 'Version' and 'Version'` | Falta `order=True` en el decorador |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Propiedades y métodos especiales](../ejercicio-02-propiedades-y-metodos-especiales/README.md) | **Ejercicio 03 · `dataclasses`** | [Ejercicio 04 · Elegir el modelo](../ejercicio-04-elegir-el-modelo/README.md) |
