# Ejercicio 02 — Composición

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-composicion.md)

## Objetivo

Comparar dos formas de escribir una lista de lecturas sin negativos: heredando de `list` y guardando una lista dentro. Después, cambiar la pieza interna sin tocar a quien la usa y montar un objeto con piezas intercambiables. Es lo que hace `Series` en tu proyecto (tiene una lista de medidas) y lo que hace `LinesSource` (tiene unas líneas). Ejercicio **guiado**: descomentas cada paso de `composition_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-10-herencia_composicion_abc_y_protocol/2-practicas/ejercicio-02-composicion/starter
uv run python composition_lab.py
```

```
Ejercicio 02 · composición
```

Los pasos 3 y 4 usan la clase `Readings` del paso 2: descomenta en orden.

## Pasos

### 1. Heredar de `list`

Descomenta el **PASO 1** y ejecuta:

```
Error: lectura negativa: -3.0
Se colaron: [-5.0, 12.5, -1.0, -2.0]
Al sumar: list
```

`ReadingList` hereda de `list` y valida en `append`. El `-3.0` se rechaza, pero tres negativos entran por otras puertas: `insert`, `extend` y `+=` son métodos de `list` que no pasan por tu `append`. Y `inherited + [1.0]` devuelve una `list` normal, que ya no valida nada. Al heredar, `ReadingList` **es una** `list` en todo, también en los cuarenta y pico métodos en los que no pensaste.

### 2. Tener una lista

Descomenta el **PASO 2** y ejecuta:

```
Error: lectura negativa: -3.0
Error: 'Readings' object has no attribute 'insert'
Valores: [12.5, 48.9] · media: 30.7
```

`Readings` no hereda de nada: **tiene** una lista en `_values` y solo ofrece tres métodos, `add`, `values` y `mean`. `add` valida y le pasa el valor a la lista (**delega**). `insert` no existe, así que no hay otra puerta. Y `values()` devuelve una **copia**: el `copy.append(-1.0)` de la penúltima línea cambia la copia, no las lecturas. Es la misma idea que `LinesSource.lines()` en tu proyecto.

### 3. Cambiar la pieza de dentro

Descomenta el **PASO 3** y ejecuta:

```
Readings -> [10.0, 20.0, 30.0, 40.0] · media: 25.0
RecentReadings -> [20.0, 30.0, 40.0] · media: 30.0
```

`RecentReadings` es `Readings` con una sola línea distinta: guarda las lecturas en un `deque(maxlen=3)` (semana 6) en lugar de una lista, así que solo recuerda las tres últimas. Los métodos `add`, `values` y `mean` no cambian, y el bucle `for kind in [...]` usa las dos clases igual. Quien usa la clase no se entera de qué hay dentro. Con `ReadingList` esto no sería posible: alguien podría estar usando `insert` o `sort`, y un `deque` no tiene `sort`.

### 4. Un objeto hecho de piezas

Descomenta el **PASO 4** y ejecuta:

```
Centro: 40.0 µg/m³ -> alto
Puente: 4.5 mg/L -> medio
Centro: 40.0 µg/m³ -> medio
Lecturas del aire: [40.0, 40.0]
```

`Monitor` **tiene** una escala y unas lecturas, y las usa: `check` guarda el valor en las lecturas y le pide el nivel a la escala.

- Cada monitor recibe sus piezas al crearse: el del aire, una escala en µg/m³ y unas `Readings` nuevas (`default_factory`); el del río, otra escala y unas `RecentReadings`.
- Las piezas se pueden cambiar en vivo: con `air.scale = Scale(...)`, el mismo 40.0 pasa de "alto" a "medio".
- Ni una sola subclase: en lugar de `AirMonitor`, `RiverMonitor` o `MonitorWithRecentReadings`, combinas objetos.

Un detalle: el campo dice `readings: Readings`, y al río le pasas unas `RecentReadings`, que no heredan de `Readings`. En ejecución funciona porque tienen los mismos métodos (*duck typing*), pero mypy se quejaría. En el ejercicio 04, un `Protocol` lo arregla.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'Readings' is not defined` | Los pasos 3 y 4 usan `Readings`: descomenta antes el paso 2 |
| `ZeroDivisionError: division by zero` | `mean()` con cero lecturas: añade alguna antes de pedir la media |
| Dos monitores comparten las lecturas | Escribiste `readings: Readings = Readings()`: es **un** objeto para todos, y `@dataclass` solo detecta los valores sin *hash*, como `list`, `dict` o `set`. Usa `field(default_factory=Readings)` |
| `FrozenInstanceError` en el paso 4 | Intentaste cambiar un campo de la escala; `air.scale = ...` cambia el monitor, que no es `frozen` |
| `IndentationError` | Al descomentar, el cuerpo de cada clase y de cada método debe quedar con su sangría |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Herencia](../ejercicio-01-herencia/README.md) | **Ejercicio 02 · Composición** | [Ejercicio 03 · Clases abstractas](../ejercicio-03-clases-abstractas/README.md) |
