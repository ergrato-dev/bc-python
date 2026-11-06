# 01 · Operadores y expresiones

⏱️ 45 min

## 🎯 Objetivos

- Calcular con los operadores aritméticos, incluidos `//`, `%` y `**`, y predecir su resultado con negativos.
- Comparar valores y encadenar comparaciones.
- Combinar condiciones con `and`, `or` y `not`, y explicar el cortocircuito.
- Leer una expresión larga aplicando la precedencia de operadores.

---

## 1. Expresión y sentencia

Una **expresión** es cualquier trozo de código que produce un valor: `2 + 3`, `value > 0`, `name.strip()`. Una **sentencia** es una orden completa: `x = 2 + 3` (asignación), `if`, `return`. El REPL muestra el valor de las expresiones que escribes; las sentencias no muestran nada.

```python
>>> 2 + 3
5
>>> x = 2 + 3
>>> x
5
```

Esta semana todo gira en torno a expresiones: cómo se calculan, cómo se comparan y cómo se combinan.

## 2. Operadores aritméticos

| Operador | Qué hace | Ejemplo | Resultado |
|---|---|---|---|
| `+` | Suma | `10 + 4` | `14` |
| `-` | Resta | `10 - 4` | `6` |
| `*` | Multiplicación | `10 * 4` | `40` |
| `/` | División, **siempre** da `float` | `10 / 4` | `2.5` |
| `//` | División entera (redondea hacia abajo) | `10 // 4` | `2` |
| `%` | Módulo: el resto de la división entera | `10 % 4` | `2` |
| `**` | Potencia | `2 ** 10` | `1024` |

`/` siempre devuelve `float`, aunque la división sea exacta: `8 / 2` da `4.0`. Si necesitas un entero, usa `//`.

### Paso a paso: `//` y `%` juntos

`//` y `%` responden a la misma pregunta desde dos lados: "¿cuántas veces cabe, y cuánto sobra?". Con 135 minutos:

```python
>>> total = 135
>>> total // 60
2
>>> total % 60
15
>>> divmod(total, 60)
(2, 15)
```

2 horas y 15 minutos. `divmod` devuelve las dos cosas a la vez (el resultado entre paréntesis es una **tupla**, la verás en la semana 5).

Usos típicos de `%`:

| Pregunta | Expresión |
|---|---|
| ¿`n` es par? | `n % 2 == 0` |
| ¿`year` es múltiplo de 4? | `year % 4 == 0` |
| Último dígito de `n` | `n % 10` |

### Negativos: `//` redondea hacia abajo, no hacia el cero

```python
>>> 7 // 2
3
>>> -7 // 2
-4
>>> -7 % 2
1
```

`-7 / 2` es `-3.5`; "hacia abajo" en la recta numérica es `-4`, no `-3`. Python mantiene siempre la regla `(a // b) * b + (a % b) == a`: `(-4) * 2 + 1 == -7`. Si en otro lenguaje viste que `-7 / 2` da `-3`, aquí no.

### Asignación aumentada

`x += 5` es la forma corta de `x = x + 5`. Existe para todos los operadores: `-=`, `*=`, `/=`, `//=`, `%=`, `**=`.

```python
>>> count = 0
>>> count += 1
>>> count += 1
>>> count
2
```

## 3. Comparaciones

| Operador | Significa |
|---|---|
| `==` | Igual valor |
| `!=` | Distinto valor |
| `<`, `<=`, `>`, `>=` | Menor, menor o igual, mayor, mayor o igual |
| `is`, `is not` | El **mismo objeto** (solo para `None`, teoría 05 de la semana 1) |
| `in`, `not in` | Está contenido en (`"a" in "casa"`) |

Toda comparación da un `bool`. Y se pueden **encadenar** como en matemáticas:

```python
>>> value = 12.5
>>> 0 <= value <= 500
True
```

`0 <= value <= 500` significa `0 <= value and value <= 500`, pero `value` se evalúa una sola vez.

Detalles que causan errores:

```python
>>> 10 == 10.0
True
>>> "10" == 10
False
>>> "a" < "B"
False
```

- Un `int` y un `float` con el mismo valor son iguales.
- Un `str` nunca es igual a un número: `"10"` es texto. Convierte primero (`int("10") == 10`).
- Los textos se comparan carácter a carácter por su código Unicode, y en Unicode todas las mayúsculas van antes que las minúsculas. Para ordenar palabras sin que importen las mayúsculas, compáralas en minúsculas (teoría 03).

## 4. Operadores lógicos y cortocircuito

| Operador | Da `True` cuando |
|---|---|
| `a and b` | `a` y `b` son verdaderos |
| `a or b` | Al menos uno es verdadero |
| `not a` | `a` es falso |

```python
>>> year = 2024
>>> year % 4 == 0 and year % 100 != 0
True
```

### Cortocircuito: Python deja de evaluar en cuanto sabe la respuesta

- En `a and b`, si `a` es falso, el resultado ya es falso: **`b` no se ejecuta**.
- En `a or b`, si `a` es verdadero, el resultado ya es verdadero: **`b` no se ejecuta**.

Por eso el orden importa. En el proyecto de la semana 1 lo usaste:

```python
>>> value = None
>>> value is not None and value > 0
False
>>> value > 0 and value is not None
TypeError: '>' not supported between instances of 'NoneType' and 'int'
```

En la primera línea, `value is not None` es `False` y Python no llega a `value > 0`. En la segunda, compara `None > 0` y falla. **Pon primero la condición que protege a la otra.**

### `and` y `or` devuelven uno de los operandos, no siempre un `bool`

Cada valor de Python es "verdadero" o "falso" cuando se usa como condición (*truthiness*). Son **falsos**: `False`, `None`, `0`, `0.0` y `""` (texto vacío). Todo lo demás es verdadero, incluido `"0"` y `" "`.

`a or b` devuelve `a` si `a` es verdadero; si no, devuelve `b`. Eso sirve para dar un valor por defecto:

```python
>>> label = ""
>>> label or "sin etiqueta"
'sin etiqueta'
>>> label = "Norte"
>>> label or "sin etiqueta"
'Norte'
```

Cuidado: `0 or 10` da `10`. Si `0` es un dato válido en tu dominio, `or` lo cambia por el valor por defecto sin avisar. Para "falta el dato" usa `is None` (semana 1).

## 5. Precedencia: qué se calcula primero

De mayor a menor (lo de arriba se calcula antes):

| Nivel | Operadores |
|---|---|
| 1 | `( )` |
| 2 | `**` |
| 3 | `-x` (signo) |
| 4 | `*`, `/`, `//`, `%` |
| 5 | `+`, `-` |
| 6 | Comparaciones: `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `in` |
| 7 | `not` |
| 8 | `and` |
| 9 | `or` |

```python
>>> 2 + 3 * 4 ** 2
50
>>> (2 + 3) * 4
20
>>> 2 ** 3 ** 2
512
>>> -2 ** 2
-4
```

- `4 ** 2` primero (16), después `3 * 16` (48), después `2 + 48`.
- `**` se agrupa de derecha a izquierda: `2 ** (3 ** 2)` es `2 ** 9`.
- `-2 ** 2` es `-(2 ** 2)`. Si quieres el cuadrado de `-2`, escribe `(-2) ** 2`.

Regla práctica: **si dudas, pon paréntesis**. No cuestan nada y el siguiente que lea el código no tendrá que consultar esta tabla.

## 6. Errores frecuentes

| Síntoma | Causa | Arreglo |
|---|---|---|
| `8 / 2` da `4.0` y luego `range` o un índice falla | `/` siempre da `float` | Usa `//` cuando necesitas un entero |
| `-7 // 2` da `-4` y esperabas `-3` | `//` redondea hacia abajo | Es lo correcto en Python; si quieres truncar, `int(-7 / 2)` |
| `TypeError: '>' not supported between instances of 'NoneType' and 'int'` | Comparas `None` con un número | Pon `value is not None and` delante |
| `"10" == 10` da `False` | Comparas texto con número | Convierte el texto con `int()` o `float()` |
| `value or 0` cambia un `0.0` válido | `or` trata `0.0` como falso | Usa `value if value is not None else 0` |
| `SyntaxWarning: "is" with 'int' literal` | Usaste `is` para comparar números | `is` solo con `None`; para valores, `==` |

---

## ✅ Qué debes saber al terminar

- `/` da `float`; `//` y `%` dan cociente y resto; con negativos, `//` redondea hacia abajo.
- Las comparaciones dan `bool` y se encadenan: `0 <= x <= 500`.
- `and` y `or` se detienen en cuanto saben el resultado: pon primero la condición que protege a la otra.
- `0`, `0.0`, `""`, `None` y `False` son falsos; `x or default` cambia cualquiera de ellos por el valor por defecto.
- Ante la duda con la precedencia, paréntesis.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 02](../README.md) | **01 · Operadores y expresiones** | [02 · Condicionales y `match`](02-condicionales-y-match.md) |
