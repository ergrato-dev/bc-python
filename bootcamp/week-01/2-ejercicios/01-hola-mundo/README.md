# 🖨️ Ejercicio 01: Hola Mundo y print()

## 🎯 Objetivo

Practicar el uso de la función `print()` con diferentes parámetros y formatos.

---

## 📋 Instrucciones

### Paso 1: El clásico Hola Mundo

El programa más simple en cualquier lenguaje. Abre `starter/main.py` y descomenta la sección del Paso 1.

```python
print("¡Hola, Mundo!")
```

**Resultado esperado:**
```
¡Hola, Mundo!
```

---

### Paso 2: Imprimir múltiples valores

`print()` puede recibir varios argumentos separados por coma. Python los imprime con un espacio entre ellos.

```python
print("Hola", "Python", "3.13")
```

**Resultado esperado:**
```
Hola Python 3.13
```

---

### Paso 3: Usar el parámetro sep

El parámetro `sep` cambia el separador entre argumentos (por defecto es espacio).

```python
print("2026", "01", "02", sep="-")
print("a", "b", "c", sep=" -> ")
```

**Resultado esperado:**
```
2026-01-02
a -> b -> c
```

---

### Paso 4: Usar el parámetro end

El parámetro `end` cambia lo que se imprime al final (por defecto es `\n` - nueva línea).

```python
print("Cargando", end="...")
print("Listo!")
```

**Resultado esperado:**
```
Cargando...Listo!
```

---

### Paso 5: Caracteres especiales

Los caracteres de escape nos permiten incluir caracteres especiales:
- `\n` - Nueva línea
- `\t` - Tabulación

```python
print("Línea 1\nLínea 2\nLínea 3")
print("Nombre:\tAna")
print("Edad:\t25")
```

**Resultado esperado:**
```
Línea 1
Línea 2
Línea 3
Nombre:	Ana
Edad:	25
```

---

### Paso 6: Crear una tarjeta de presentación

Combina todo lo aprendido para crear una presentación visual:

```python
print("=" * 30)
print("TARJETA DE PRESENTACIÓN")
print("=" * 30)
print("Nombre:\tTu Nombre")
print("Rol:\tEstudiante Python")
print("=" * 30)
```

---

## ▶️ Cómo ejecutar

```bash
# Desde el directorio del ejercicio
docker run -it --rm -v $(pwd):/app -w /app python:3.13-slim python starter/main.py
```

---

## ✅ Checklist

- [ ] Paso 1: Hola Mundo básico
- [ ] Paso 2: Múltiples argumentos
- [ ] Paso 3: Parámetro `sep`
- [ ] Paso 4: Parámetro `end`
- [ ] Paso 5: Caracteres especiales
- [ ] Paso 6: Tarjeta de presentación

---

## 🎯 Resultado Final Esperado

Al descomentar todo el código, deberías ver:

```
--- Paso 1: Hola Mundo ---
¡Hola, Mundo!

--- Paso 2: Múltiples valores ---
Hola Python 3.13

--- Paso 3: Parámetro sep ---
2026-01-02
a -> b -> c

--- Paso 4: Parámetro end ---
Cargando...Listo!

--- Paso 5: Caracteres especiales ---
Línea 1
Línea 2
Línea 3
Nombre:	Ana
Edad:	25

--- Paso 6: Tarjeta de presentación ---
==============================
TARJETA DE PRESENTACIÓN
==============================
Nombre:	Tu Nombre
Rol:	Estudiante Python
==============================
```
