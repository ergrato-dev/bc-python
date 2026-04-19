# ➕ Ejercicio 03: Operadores

## 🎯 Objetivo

Practicar el uso de operadores aritméticos, de comparación, lógicos y de asignación en Python.

---

## 📋 Instrucciones

### Paso 1: Operadores aritméticos básicos

Los operadores básicos son: `+`, `-`, `*`, `/`

```python
a: int = 10
b: int = 3
print(f"{a} + {b} = {a + b}")
```

Abre `starter/main.py` y descomenta la sección del Paso 1.

---

### Paso 2: División entera y módulo

- `//` división entera (sin decimales)
- `%` módulo (resto de la división)
- `**` potencia

```python
print(f"10 // 3 = {10 // 3}")  # 3
print(f"10 % 3 = {10 % 3}")    # 1
print(f"2 ** 3 = {2 ** 3}")    # 8
```

---

### Paso 3: Operadores de comparación

Comparan valores y retornan `True` o `False`:

```python
print(f"5 > 3: {5 > 3}")   # True
print(f"5 == 5: {5 == 5}") # True
```

---

### Paso 4: Operadores lógicos

- `and`: True si ambos son True
- `or`: True si al menos uno es True
- `not`: invierte el valor

```python
print(f"True and False: {True and False}")  # False
```

---

### Paso 5: Operadores de asignación compuestos

Atajos para modificar variables:

```python
x: int = 10
x += 5  # equivale a x = x + 5
```

---

### Paso 6: Aplicación práctica - Calculadora de tiempo

Usa división entera y módulo para convertir minutos a horas:

```python
minutos: int = 150
horas: int = minutos // 60
mins: int = minutos % 60
```

---

## ▶️ Cómo ejecutar

```bash
docker run -it --rm -v $(pwd):/app -w /app python:3.13-slim python starter/main.py
```

---

## ✅ Checklist

- [ ] Paso 1: Operadores aritméticos básicos
- [ ] Paso 2: División entera, módulo y potencia
- [ ] Paso 3: Operadores de comparación
- [ ] Paso 4: Operadores lógicos
- [ ] Paso 5: Operadores de asignación
- [ ] Paso 6: Aplicación práctica

---

## 🎯 Resultado Final Esperado

```
--- Paso 1: Operadores aritméticos básicos ---
a = 10, b = 3
10 + 3 = 13
10 - 3 = 7
10 * 3 = 30
10 / 3 = 3.3333333333333335

--- Paso 2: División entera, módulo y potencia ---
10 // 3 = 3 (división entera)
10 % 3 = 1 (resto/módulo)
2 ** 8 = 256 (potencia)

--- Paso 3: Operadores de comparación ---
x = 10, y = 5
10 == 5: False
10 != 5: True
10 > 5: True
10 < 5: False
10 >= 10: True
10 <= 5: False

--- Paso 4: Operadores lógicos ---
True and True: True
True and False: False
True or False: True
False or False: False
not True: False
not False: True

--- Paso 5: Operadores de asignación ---
Valor inicial: 100
Después de += 10: 110
Después de -= 20: 90
Después de *= 2: 180
Después de //= 3: 60

--- Paso 6: Aplicación - Convertir minutos ---
150 minutos = 2 horas y 30 minutos
200 minutos = 3 horas y 20 minutos
45 minutos = 0 horas y 45 minutos
```
