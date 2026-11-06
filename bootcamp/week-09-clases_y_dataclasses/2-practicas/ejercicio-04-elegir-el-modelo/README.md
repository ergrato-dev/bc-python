# Ejercicio 04 — Elegir el modelo

⏱️ 1 h · Teoría previa: [05](../../1-teoria/05-elegir-el-modelo.md)

## Objetivo

Guardar la misma medida, `"Norte"` con `12.5`, de cinco formas (tupla, diccionario, `NamedTuple`, *dataclass* y *dataclass* con `slots`) y comparar qué permite y qué impide cada una. Al final, mypy te dice cuáles de los errores habría visto antes de ejecutar. Es la decisión que tomas en el proyecto al pasar de `Record = tuple[str, float | None]` a `Measurement`. Ejercicio **guiado**: descomentas cada paso de `model_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-09-clases_y_dataclasses/2-practicas/ejercicio-04-elegir-el-modelo/starter
uv run python model_lab.py
```

```
Ejercicio 04 · Elegir el modelo
```

## Pasos

### 1. Una tupla

Descomenta el **PASO 1** y ejecuta:

```
Tupla: ('Norte', 12.5) · valor: 12.5 · desempaquetada: Norte 12.5
Error: 'tuple' object does not support item assignment
```

Es lo que usa tu Observatorio desde la semana 5. Es corta, inmutable y se desempaqueta, pero `as_tuple[1]` no dice qué es el `1`: tienes que recordar que la posición 1 es el valor.

### 2. Un diccionario

Descomenta el **PASO 2** y ejecuta:

```
Diccionario: {'label': 'Norte', 'value': 13.0, 'unti': 'µg/m³'}
Error: no existe la clave 'valor'
```

Las claves tienen nombre, pero no hay ninguna forma fija: `as_dict["unti"]`, con una errata, crea una clave nueva sin avisar, y `as_dict["valor"]` falla solo cuando esa línea se ejecuta. Un diccionario va bien para datos que llegan de fuera con claves variables, como el JSON de la semana 7. Para el modelo de tu programa, no.

### 3. Una `NamedTuple`

Descomenta el **PASO 3** y ejecuta:

```
NamedTuple: NamedMeasurement(label='Norte', value=12.5) · valor: 12.5 · también: 12.5
Desempaquetada: Norte 12.5
¿Igual a la tupla? True
Error: can't set attribute
```

Una `NamedTuple` es una tupla con nombres: se lee `named.value`, se imprime con sus campos y sigue siendo inmutable. Pero **sigue siendo una tupla**: se indexa con `[1]`, se desempaqueta y es igual a `("Norte", 12.5)`. Es útil para cambiar una tupla por algo con nombres sin romper el código que la usaba. Su pega: una medida es igual a cualquier tupla con los mismos datos.

### 4. Una *dataclass*

Descomenta el **PASO 4** y ejecuta:

```
dataclass: Measurement(label='Norte', value=12.5) · valor: 12.5
¿Igual a la tupla? False
Error: cannot unpack non-iterable Measurement object
```

La *dataclass* es un tipo propio: solo es igual a otra `Measurement`, no se indexa ni se desempaqueta. Al principio parece que pierdes algo, pero ganas que nadie la confunda con una tupla cualquiera. Y puedes añadirle métodos, propiedades y validación, que es lo que hace el proyecto.

### 5. `slots`

Descomenta el **PASO 5** y ejecuta:

```
Sin slots: Loose(label='Norte', unit='µg/m³') · atributos: {'label': 'Norte', 'unit': 'µg/m³', 'unti': '°C'}
Error: 'Slotted' object has no attribute 'unti' and no __dict__ for setting new attributes
¿Tiene __dict__? True · False
```

Por defecto, un objeto guarda sus atributos en un diccionario, su `__dict__`, y como cualquier diccionario acepta claves nuevas: `loose.unti = "°C"`, con una errata, crea un atributo sin avisar. Con `slots=True`, la clase reserva sitio solo para sus campos y no tiene `__dict__`: la errata falla en el momento. Además, cada objeto ocupa menos memoria, cosa que se nota cuando tienes miles de medidas. En el proyecto, las tres clases del modelo llevan `slots=True`.

### 6. Lo que habría visto mypy

Ejecuta mypy sobre el archivo, sin añadirlo al proyecto (semana 8, `uv run --with`):

```bash
uv run --with mypy==2.4.1 mypy model_lab.py
```

```
model_lab.py:21: error: Unsupported target for indexed assignment ("tuple[str, float]")  [index]
model_lab.py:52: error: Property "value" defined in "NamedMeasurement" is read-only  [misc]
model_lab.py:70: error: "Measurement" object is not iterable  [misc]
model_lab.py:91: error: "Loose" has no attribute "unti"  [attr-defined]
model_lab.py:95: error: "Slotted" has no attribute "unti"  [attr-defined]
Found 5 errors in 1 file (checked 1 source file)
```

mypy encuentra sin ejecutar casi todos los errores que provocaste, y la errata `unti` también en `Loose`, que en ejecución pasó sin avisar. Los dos errores del diccionario, `"unti"` y `"valor"`, no aparecen: para mypy, cualquier texto es una clave válida de un `dict[str, ...]`. Cuanto más concreto es el tipo, más errores ves antes de ejecutar.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'NamedTuple' is not defined` | Borraste el `from typing import NamedTuple` de arriba |
| `TypeError: NamedMeasurement.__new__() missing 1 required positional argument: 'value'` | Falta un argumento al crearla: van en el orden de los campos |
| El paso 5 no da error con `Slotted` | Falta `slots=True` en el decorador de `Slotted` |
| mypy da más errores de los que salen aquí | Descomentaste algo distinto o añadiste líneas: compara los números de línea con los de tu archivo |
| mypy tarda la primera vez | Descarga mypy en un entorno temporal; la segunda vez va rápido |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · `dataclasses`](../ejercicio-03-dataclasses/README.md) | **Ejercicio 04 · Elegir el modelo** | [Proyecto](../../3-proyecto/README.md) |
