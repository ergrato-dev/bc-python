# 📦 Ejercicio 02: Variables y Tipos de Datos

## 🎯 Objetivo

Practicar la declaración de variables con type hints y trabajar con los tipos de datos básicos de Python.

---

## 📋 Instrucciones

### Paso 1: Variables con type hints

En Python moderno, declaramos variables indicando su tipo:

```python
nombre: str = "Ana"
edad: int = 25
```

Abre `starter/main.py` y descomenta la sección del Paso 1.

---

### Paso 2: Tipos numéricos

Python tiene dos tipos numéricos principales:
- `int`: números enteros
- `float`: números decimales

```python
entero: int = 42
decimal: float = 3.14
```

---

### Paso 3: Booleanos

Los booleanos representan valores de verdad:

```python
activo: bool = True
eliminado: bool = False
```

> ⚠️ Nota: `True` y `False` van con mayúscula inicial.

---

### Paso 4: Verificar tipos con type()

La función `type()` nos dice el tipo de una variable:

```python
print(type(nombre))  # <class 'str'>
```

---

### Paso 5: Conversión de tipos (casting)

Podemos convertir entre tipos:

```python
texto: str = "42"
numero: int = int(texto)  # Convierte "42" a 42
```

---

### Paso 6: f-Strings

Los f-strings permiten incluir variables en texto:

```python
nombre: str = "Ana"
mensaje: str = f"Hola, {nombre}!"
```

---

## ▶️ Cómo ejecutar

```bash
docker run -it --rm -v $(pwd):/app -w /app python:3.13-slim python starter/main.py
```

---

## ✅ Checklist

- [ ] Paso 1: Declarar variables con type hints
- [ ] Paso 2: Usar `int` y `float`
- [ ] Paso 3: Usar `bool`
- [ ] Paso 4: Verificar tipos con `type()`
- [ ] Paso 5: Convertir entre tipos
- [ ] Paso 6: Usar f-strings

---

## 🎯 Resultado Final Esperado

```
--- Paso 1: Variables con type hints ---
Nombre: Ana
Edad: 25
Altura: 1.65

--- Paso 2: Tipos numéricos ---
Entero: 42 (tipo: <class 'int'>)
Decimal: 3.14159 (tipo: <class 'float'>)
Número grande: 1000000

--- Paso 3: Booleanos ---
¿Está activo? True
¿Está eliminado? False

--- Paso 4: Verificar tipos ---
tipo de nombre: <class 'str'>
tipo de edad: <class 'int'>
tipo de altura: <class 'float'>
tipo de activo: <class 'bool'>

--- Paso 5: Conversión de tipos ---
Texto original: 42 (tipo: <class 'str'>)
Convertido a int: 42 (tipo: <class 'int'>)
Convertido a float: 42.0 (tipo: <class 'float'>)
Número a texto: 100 (tipo: <class 'str'>)

--- Paso 6: f-Strings ---
Hola, soy Ana y tengo 25 años
Mi altura es 1.65 metros
El próximo año tendré 26 años
```
