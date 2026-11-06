# Ejercicio 01 — Herencia

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-herencia.md)

## Objetivo

Crear subclases de un `Sensor`: heredar sin escribir nada, sustituir un método, extenderlo con `super()`, leer la MRO, aprovechar el polimorfismo y montar una jerarquía de excepciones. Es la base de `TextFile` y `CsvFile` en el proyecto. Ejercicio **guiado**: descomentas cada paso de `inheritance_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-10-herencia_composicion_abc_y_protocol/2-practicas/ejercicio-01-herencia/starter
uv run python inheritance_lab.py
```

```
Ejercicio 01 · herencia
```

Arriba del archivo, sin comentar, está la clase `Sensor` que usan todos los pasos: nombre, unidad, una lista de lecturas, `record` y `describe`. Léela antes de seguir. Los pasos 2 a 5 usan clases de los pasos anteriores: descoméntalos en orden.

## Pasos

### 1. Una subclase vacía ya sabe hacer cosas

Descomenta el **PASO 1** y ejecuta:

```
Centro (µg/m³) · [18.5]
¿Es un AirSensor? True · ¿Es un Sensor? True
¿Un Sensor es un AirSensor? False
```

`AirSensor` solo tiene `pass` y sin embargo se crea con nombre y unidad, guarda lecturas y se describe: **hereda** el `__init__`, `record` y `describe` de `Sensor`. Un `AirSensor` **es un** `Sensor` (`isinstance` da `True`), pero no al revés: un `Sensor` cualquiera no es un sensor de aire.

### 2. Sustituir un método

Descomenta el **PASO 2** y ejecuta:

```
aire · Centro (µg/m³)
Norte (°C)
```

`LabeledSensor` define su propio `describe`, que **sustituye** al de la base (*override*). La base no cambia: un `Sensor` normal se sigue describiendo como antes. El método de la hija tiene el mismo nombre, los mismos parámetros y devuelve el mismo tipo; si devolviera un `int`, mypy avisaría.

### 3. Extender con `super()`

Descomenta el **PASO 3** y ejecuta:

```
Centro (µg/m³) · PM10 · [41.0]
Error: 'ForgetfulSensor' object has no attribute 'readings'
```

- `PollutantSensor` necesita un dato más, el contaminante. Su `__init__` llama primero a `super().__init__(name, unit)`, que ejecuta el de `Sensor` (nombre, unidad y la lista de lecturas), y después añade lo suyo.
- Su `describe` no repite el formato: toma el de la base con `super().describe()` y le añade el contaminante.
- `ForgetfulSensor` olvida `super().__init__`. Su `__init__` sustituye por completo al de la base, así que `readings` nunca se crea, y `record` falla al buscarla.

### 4. La MRO y el polimorfismo

Descomenta el **PASO 4** y ejecuta:

```
MRO: ['PollutantSensor', 'Sensor', 'object']
¿bool hereda de int? True · True + True = 2
  Sensor -> Norte (°C)
  LabeledSensor -> aire · Este (µg/m³)
  PollutantSensor -> Sur (ppb) · O3
```

`__mro__` es el orden en que Python busca un método: la propia clase, su base y, al final, `object`, del que heredan todas. Hasta `bool` es una subclase: hereda de `int`, por eso `True + True` da 2.

`report` recibe una lista de `Sensor` y llama a `describe()` sin preguntar de qué clase es cada uno: cada objeto responde con **su** versión. Eso es el **polimorfismo**, y es lo que hará `main` con las fuentes de tu proyecto: pedir `lines()` sin saber si vienen de un `.txt` o de un `.csv`.

### 5. Una jerarquía de excepciones

Descomenta el **PASO 5** y ejecuta:

```
MRO: ['HeaderError', 'DataFileError', 'Exception', 'BaseException', 'object']
Cabecera: cabecera inesperada: nombre;dato
Archivo: no existe medidas.csv
```

`HeaderError` es un `DataFileError`, que es un `Exception`. Python usa el **primer** `except` que encaja: el `HeaderError` entra por el primero; el `DataFileError` genérico no encaja en `except HeaderError` y entra por el segundo. Prueba a cambiar el orden de los dos `except`: los dos problemas acaban en "Archivo:", porque un `HeaderError` también **es** un `DataFileError`. Vuelve a dejarlos como estaban.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'LabeledSensor' is not defined` en el paso 4 | El paso 4 usa las clases de los pasos 2 y 3: descoméntalos antes |
| `TypeError: Sensor.__init__() takes 3 positional arguments but 4 were given` | Pasaste `pollutant` a `super().__init__`: la base solo recibe `name` y `unit` |
| `RecursionError` en el paso 3 | Escribiste `self.describe()` en lugar de `super().describe()` dentro de `describe` |
| `IndentationError` | Al descomentar, el cuerpo de cada clase y de cada `try` debe quedar con 4 espacios |
| En el paso 5 todo sale como "Archivo:" | El `except DataFileError` va antes que el `except HeaderError` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Diseñar jerarquías](../../1-teoria/05-disenar-jerarquias.md) | **Ejercicio 01 · Herencia** | [Ejercicio 02 · Composición](../ejercicio-02-composicion/README.md) |
