# Ejercicio 01 — Definir funciones

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-definir-y-llamar-funciones.md)

## Objetivo

Ver con tus ojos cuándo se ejecuta una función, qué diferencia hay entre `print` y `return`, y cómo se pasan los argumentos: por posición, por nombre, con valor por defecto y solo por nombre. Ejercicio **guiado**: descomentas cada paso de `functions_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-04-funciones_scope_type_hints_y_pytest/2-practicas/ejercicio-01-definir-funciones/starter
uv run python functions_lab.py
```

```
Ejercicio 01 · Definir funciones
```

## Pasos

### 1. `def` define, la llamada ejecuta

Descomenta el **PASO 1** y ejecuta:

```
Definida: <function greet at 0x7f...>
  (dentro de greet)
Devolvió: Hola, Ana
```

El número `0x7f...` cambia en cada ejecución: es la dirección de la función en memoria. Fíjate en el orden: `(dentro de greet)` sale **después** de `Definida`, porque el `def` solo guardó la función; el cuerpo se ejecuta en la llamada `greet("Ana")`.

### 2. `print` no es `return`

Descomenta el **PASO 2**:

```
  el doble es 8
show_double devolvió: None | double devolvió: 8
double(double(3)) = 12
```

`show_double` muestra el resultado en la pantalla, pero a quien la llamó le entrega `None`: no hay nada que guardar ni que seguir usando. `double` lo devuelve, y por eso puede ir dentro de otra llamada: `double(double(3))` es `double(6)`.

### 3. Por posición y por nombre

Descomenta el **PASO 3**:

```
Norte: 12.5 µg/m³
Sur: 8.0 µg/m³
Centro: 40.2 µg/m³
```

Las tres llamadas dan lo mismo con argumentos colocados de forma distinta. Prueba `describe(label="Centro", 40.2, "µg/m³")`: `SyntaxError: positional argument follows keyword argument`. Los de posición siempre van primero. Deshaz el cambio.

### 4. Valores por defecto y solo por nombre

Descomenta el **PASO 4**:

```
$1,234.50
$1,234
€1,234.50
```

`decimals` vale `2` si no lo pasas. El `*` de la firma hace que `sign` solo se pueda pasar por nombre: prueba `money(1234.5, 2, "€")` y verás `TypeError: money() takes from 1 to 2 positional arguments but 3 were given`. Sirve para que una llamada se lea sola: `sign="€"` dice qué es, y un `"€"` suelto no. Deshaz el cambio.

### 5. Varios valores de vuelta

Descomenta el **PASO 5**:

```
135 min = 2 h 15 min | tupla completa: (2, 15)
```

`return a, b` devuelve una **tupla**, un valor con dos partes. `hours, minutes = ...` la desempaqueta. Las tuplas las verás a fondo en la semana 5.

### 6. Cláusulas de guarda

Descomenta el **PASO 6**:

```
Notas: fuera de rango | insuficiente | aprobado
```

Cada `return` termina la función: si la nota está fuera de rango, las líneas de abajo ya no se ejecutan. Así no hace falta anidar `if` dentro de `else`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'greet' is not defined` | Llamas a la función antes de su `def`, o el `def` sigue comentado |
| `TypeError: greet() missing 1 required positional argument: 'name'` | Llamaste `greet()` sin argumento |
| `TypeError: describe() got an unexpected keyword argument 'units'` | El nombre del argumento no coincide con el parámetro: es `unit` |
| Sale `None` donde esperabas un valor | A la función le falta `return` |
| `IndentationError` después de descomentar | Falta la sangría del cuerpo: 4 espacios más que el `def` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Tests con pytest](../../1-teoria/05-tests-con-pytest.md) | **Ejercicio 01 · Definir funciones** | [Ejercicio 02 · Scope y funciones como valores](../ejercicio-02-scope-y-funciones-como-valores/README.md) |
