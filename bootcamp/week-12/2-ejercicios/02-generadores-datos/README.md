# 🔄 Ejercicio 02: Generadores de Datos

## 📋 Objetivo

Aprender a crear generadores eficientes para procesar datos grandes y construir pipelines de transformación.

---

## 📚 Conceptos Clave

- `yield` para producir valores bajo demanda
- Expresiones generadoras
- `yield from` para delegación
- Pipelines de generadores

---

## 🔧 Instrucciones

Abre el archivo `starter/main.py` y descomenta el código paso a paso.

---

## 📝 Pasos

### Paso 1: Generador Básico con yield

Crear un generador de cuenta regresiva:

```python
for num in countdown(5):
    print(num)  # 5, 4, 3, 2, 1
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

### Paso 2: Generador de Fibonacci

Secuencia infinita de Fibonacci usando generador:

```python
fib = fibonacci()
for _ in range(10):
    print(next(fib))  # 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

**Descomenta** la sección del Paso 2.

---

### Paso 3: Expresiones Generadoras

Comparar memoria entre lista y generador:

```python
# Lista: consume mucha memoria
squares_list = [x**2 for x in range(1_000_000)]

# Generador: casi no consume memoria
squares_gen = (x**2 for x in range(1_000_000))
```

**Descomenta** la sección del Paso 3.

---

### Paso 4: yield from

Delegar a otros iteradores:

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
```

**Descomenta** la sección del Paso 4.

---

### Paso 5: Pipeline de Generadores

Encadenar transformaciones eficientemente:

```python
# Cada paso procesa datos bajo demanda
lines = read_lines("data.txt")
filtered = filter_lines(lines)
transformed = transform_lines(filtered)
```

**Descomenta** la sección del Paso 5.

---

### Paso 6: Generador con send()

Comunicación bidireccional con generadores:

```python
acc = accumulator()
next(acc)          # Inicializar
acc.send(10)       # Enviar valor
acc.send(5)        # Enviar otro valor
```

**Descomenta** la sección del Paso 6.

---

## ✅ Verificación

```bash
python main.py
```

---

## 🎯 Resultado Esperado

```
=== PASO 1: Countdown ===
5, 4, 3, 2, 1

=== PASO 2: Fibonacci ===
0, 1, 1, 2, 3, 5, 8, 13, 21, 34

=== PASO 3: Generator Expression ===
List memory: ~8 MB
Generator memory: ~120 bytes
Sum of first 100 squares: 328350

=== PASO 4: Yield From ===
Flattened: [1, 2, 3, 4, 5, 6, 7, 8, 9]

=== PASO 5: Pipeline ===
Processing 1000 items efficiently...
Results: [processed items]

=== PASO 6: Send ===
Total: 0 -> 10 -> 15 -> 18
```
