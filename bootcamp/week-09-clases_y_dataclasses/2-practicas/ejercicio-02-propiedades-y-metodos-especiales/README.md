# Ejercicio 02 — Propiedades y métodos especiales

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-propiedades-y-metodos-especiales.md)

## Objetivo

Dar a una clase una forma legible de imprimirse (`__repr__` y `__str__`) y de compararse (`__eq__`), calcular y validar atributos con `@property`, y crear objetos de otra forma con `@classmethod`. Todo esto lo escribes a mano para saber qué genera `@dataclass` en el ejercicio 03. Ejercicio **guiado**: descomentas cada paso de `properties_lab.py` y de `thermometer.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-09-clases_y_dataclasses/2-practicas/ejercicio-02-propiedades-y-metodos-especiales/starter
uv run python properties_lab.py
```

```
Ejercicio 02 · Propiedades y métodos especiales
```

`thermometer.py` define `Thermometer`, con un `__init__` que guarda `name` y `celsius`. `properties_lab.py` crea `kitchen = Thermometer("Cocina", 21.5)`.

## Pasos

### 1. `__repr__` y `__str__`

Descomenta solo el **PASO 1** de `properties_lab.py` y ejecuta:

```
<thermometer.Thermometer object at 0x7723183cc590>
<thermometer.Thermometer object at 0x7723183cc590>
[<thermometer.Thermometer object at 0x7723183cc590>, <thermometer.Thermometer object at 0x7723183bc550>]
En un f-string: <thermometer.Thermometer object at 0x7723183cc590> · con !r: <thermometer.Thermometer object at 0x7723183cc590>
```

Sin más información, Python escribe el módulo, la clase y la dirección en memoria del objeto (tus números serán otros). No dice nada útil. Descomenta el **PASO 1** de `thermometer.py` y ejecuta:

```
Cocina: 21.5 °C
Thermometer('Cocina', 21.5)
[Thermometer('Cocina', 21.5), Thermometer('Patio', 14.0)]
En un f-string: Cocina: 21.5 °C · con !r: Thermometer('Cocina', 21.5)
```

Los métodos con dos guiones bajos a cada lado son **métodos especiales**: no los llamas tú, los llama Python. `print()` y los f-strings usan `__str__`, el texto para quien lee el resultado. `repr()`, `!r` y las listas usan `__repr__`, el texto para quien programa: sin ambigüedad, a ser posible con la forma de crear el objeto (`'Cocina'` lleva comillas, así que se ve que es un texto). Si una clase solo tiene `__repr__`, `print()` usa ese.

### 2. `__eq__`

Descomenta el **PASO 2** de `properties_lab.py` y ejecuta:

```
¿Iguales? False
¿Igual a un texto? False
{<thermometer.Thermometer object at 0x7723183cc590>}
```

Como en el ejercicio 01, `==` compara la identidad. Descomenta el **PASO 2** de `thermometer.py` y ejecuta:

```
¿Iguales? True
¿Igual a un texto? False
Error: cannot use 'thermometer.Thermometer' as a set element (unhashable type: 'Thermometer')
```

`a == b` llama a `a.__eq__(b)`. Si `other` no es un termómetro, devolver `NotImplemented` (no `False`) le dice a Python "no sé compararme con eso": prueba entonces al revés y, si tampoco, responde `False`.

El precio: al definir `__eq__`, Python quita a la clase su `__hash__`, y un objeto sin *hash* no puede ir en un `set` ni ser clave de un diccionario. Es a propósito: dos objetos iguales deben tener el mismo *hash*, y si el termómetro cambia de temperatura, cambiaría su *hash* mientras está dentro del `set`. En el ejercicio 03, `frozen=True` resuelve las dos cosas.

### 3. Una propiedad calculada

Descomenta el **PASO 3** de `thermometer.py`, después el de `properties_lab.py`, y ejecuta. A la salida se añade:

```
En Fahrenheit: 70.7
Tras calentarse: 86.0
Error: property 'fahrenheit' of 'Thermometer' object has no setter
```

`@property` convierte un método en algo que se lee como un atributo: `kitchen.fahrenheit`, sin paréntesis. Se calcula cada vez a partir de `celsius`, así que nunca se queda desfasado: tras cambiar `celsius` a 30, vale 86. Como solo tiene la parte de lectura, asignarle un valor da `AttributeError`.

### 4. Una propiedad que valida

Descomenta el **PASO 4** de `thermometer.py`, después el de `properties_lab.py`, y ejecuta:

```
Atributos de kitchen: {'name': 'Cocina', '_celsius': 30.0}
Error: temperatura imposible: -300.0 °C (mínimo -273.15)
Error: temperatura imposible: -500.0 °C (mínimo -273.15)
Sigue igual: Cocina: 30.0 °C
```

Ahora `celsius` es una propiedad con *setter*: `kitchen.celsius = valor` llama al método marcado con `@celsius.setter`, que comprueba el valor antes de guardarlo en `self._celsius`. Fíjate en que `__init__` no ha cambiado: su `self.celsius = celsius` también pasa por el *setter*, así que tampoco se puede **crear** un termómetro imposible. El guion bajo de `_celsius` es una convención: "es interno, usa `celsius`". Python no lo impide.

Quien usaba `kitchen.celsius` no se ha enterado del cambio. Por eso en Python se empieza con atributos normales, sin `get_celsius()` ni `set_celsius()`, y se pasa a propiedad solo si un día hace falta validar o calcular.

### 5. Método de clase y método estático

Descomenta el **PASO 5** de `thermometer.py`, después el de `properties_lab.py`, y ejecuta:

```
Houston: 37.0 °C
212 °F son 100.0 °C
```

Un `@classmethod` recibe la **clase** en `cls` en lugar del objeto: sirve para crear objetos de otra manera, como `Thermometer.from_fahrenheit(...)`. Llama a `cls(...)` y no a `Thermometer(...)` para que funcione también con las clases hijas de la semana 10. Un `@staticmethod` no recibe ni objeto ni clase: es una función normal que vive en la clase porque tiene que ver con ella. En el proyecto, `Measurement.from_line` es un `@classmethod` como este.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Sigue saliendo `<thermometer.Thermometer object at 0x...>` | Falta descomentar el PASO 1 de `thermometer.py`, o el método está fuera de la clase (sin sangría) |
| `AttributeError: 'Thermometer' object has no attribute 'fahrenheit'` | Falta descomentar el PASO 3 de `thermometer.py` |
| `TypeError: 'float' object is not callable` | Escribiste `kitchen.fahrenheit()`: una propiedad se lee sin paréntesis |
| `RecursionError: maximum recursion depth exceeded` | En el *setter* escribiste `self.celsius = value` en lugar de `self._celsius = value`: el *setter* se llama a sí mismo |
| `AttributeError: property 'celsius' of 'Thermometer' object has no setter` | Descomentaste la parte de lectura del PASO 4 pero no el *setter*: falla ya al crear `kitchen` |
| `AttributeError: type object 'Thermometer' has no attribute 'from_fahrenheit'` | Falta descomentar el PASO 5 de `thermometer.py` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Clases y objetos](../ejercicio-01-clases-y-objetos/README.md) | **Ejercicio 02 · Propiedades y métodos especiales** | [Ejercicio 03 · `dataclasses`](../ejercicio-03-dataclasses/README.md) |
