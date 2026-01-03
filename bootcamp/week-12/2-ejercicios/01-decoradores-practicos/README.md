# 🎯 Ejercicio 01: Decoradores Prácticos

## 📋 Objetivo

Aprender a crear decoradores útiles para aplicaciones reales: timing, retry, validación y logging.

---

## 📚 Conceptos Clave

- Decoradores con `@functools.wraps`
- Decoradores con argumentos
- Preservar metadata de funciones
- Patrones comunes de decoradores

---

## 🔧 Instrucciones

Abre el archivo `starter/main.py` y descomenta el código paso a paso.

---

## 📝 Pasos

### Paso 1: Decorador Timer

El decorador `@timer` mide el tiempo de ejecución:

```python
@timer
def slow_function():
    time.sleep(1)
    return "Done"

# Output: ⏱️ slow_function executed in 1.0012s
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

### Paso 2: Decorador Debug

El decorador `@debug` muestra argumentos y resultado:

```python
@debug
def add(a: int, b: int) -> int:
    return a + b

add(3, 5)
# Output:
# 🔍 Calling add(3, 5)
# 🔍 add returned 8
```

**Descomenta** la sección del Paso 2.

---

### Paso 3: Decorador Retry

El decorador `@retry` reintenta en caso de error:

```python
@retry(max_attempts=3, delay=0.5)
def unstable_api():
    if random.random() < 0.7:
        raise ConnectionError("Network error")
    return "Success"
```

**Descomenta** la sección del Paso 3.

---

### Paso 4: Decorador Validate Types

El decorador `@validate_types` valida tipos de argumentos:

```python
@validate_types(x=int, y=int)
def multiply(x: int, y: int) -> int:
    return x * y

multiply(3, 4)    # ✅ OK
multiply(3, "4")  # ❌ TypeError
```

**Descomenta** la sección del Paso 4.

---

### Paso 5: Decorador Cache con TTL

El decorador `@cache_with_ttl` cachea resultados por tiempo limitado:

```python
@cache_with_ttl(seconds=5)
def expensive_computation(n: int) -> int:
    time.sleep(1)  # Simula operación costosa
    return n * n
```

**Descomenta** la sección del Paso 5.

---

### Paso 6: Múltiples Decoradores

Combinar decoradores en orden correcto:

```python
@timer
@debug
@retry(max_attempts=2)
def complex_operation():
    ...
```

**Descomenta** la sección del Paso 6.

---

## ✅ Verificación

Ejecuta el archivo y verifica que cada decorador funcione correctamente:

```bash
python main.py
```

---

## 🎯 Resultado Esperado

```
=== PASO 1: Timer ===
⏱️ slow_sum executed in 0.0234s
Result: 500000500000

=== PASO 2: Debug ===
🔍 Calling greet('Alice', greeting='Hi')
🔍 greet returned 'Hi, Alice!'

=== PASO 3: Retry ===
⚠️ Attempt 1 failed: Network error
⚠️ Attempt 2 failed: Network error
✅ Success on attempt 3

=== PASO 4: Validate Types ===
multiply(3, 4) = 12
❌ TypeError: y must be int, got str

=== PASO 5: Cache TTL ===
First call (slow): 4
Second call (cached): 4
After TTL expires (slow): 4

=== PASO 6: Multiple Decorators ===
🔍 Calling process_data(10)
⏱️ process_data executed in 0.1023s
```
