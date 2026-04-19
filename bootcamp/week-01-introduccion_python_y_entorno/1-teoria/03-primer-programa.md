# 👋 Tu Primer Programa en Python

## 🎯 Objetivos

- Escribir y ejecutar tu primer programa
- Entender la función `print()`
- Aprender sobre comentarios en Python
- Conocer los errores de sintaxis básicos

---

## 📋 Contenido

### 1. El Clásico "Hola Mundo"

Todo programador comienza con el famoso "Hola Mundo". En Python es increíblemente simple:

```python
print("¡Hola, Mundo!")
```

**Salida:**
```
¡Hola, Mundo!
```

> 💡 Compara con Java que necesita una clase, un método main, punto y coma... Python va directo al grano.

### 2. La Función print()

`print()` es una **función incorporada** (built-in) de Python que muestra texto en la consola.

#### Sintaxis básica

```python
print("Texto entre comillas")
```

#### Tipos de comillas

Python acepta comillas simples o dobles:

```python
print("Hola con comillas dobles")
print('Hola con comillas simples')

# Ambas son equivalentes
```

#### ¿Cuándo usar cada una?

```python
# Usa dobles cuando el texto tiene apóstrofes
print("It's a beautiful day")

# Usa simples cuando el texto tiene comillas dobles
print('Ella dijo "Hola"')

# O escapa las comillas con \
print("Ella dijo \"Hola\"")
```

### 3. Imprimir Múltiples Valores

`print()` puede recibir varios argumentos separados por coma:

```python
print("Mi nombre es", "Ana")
# Mi nombre es Ana

print("Tengo", 25, "años")
# Tengo 25 años

print("Python", "es", "genial")
# Python es genial
```

> 📝 Python agrega automáticamente un espacio entre cada argumento.

### 4. Parámetros de print()

#### `sep` - Separador

Cambia el separador entre argumentos (por defecto es espacio):

```python
print("a", "b", "c")
# a b c

print("a", "b", "c", sep="-")
# a-b-c

print("a", "b", "c", sep="")
# abc

print("2025", "01", "15", sep="/")
# 2025/01/15
```

#### `end` - Final de línea

Cambia lo que se imprime al final (por defecto es `\n` - nueva línea):

```python
print("Hola")
print("Mundo")
# Hola
# Mundo

print("Hola", end=" ")
print("Mundo")
# Hola Mundo

print("Cargando", end="...")
print("Listo!")
# Cargando...Listo!
```

### 5. Caracteres Especiales

Los **caracteres de escape** comienzan con `\`:

| Carácter | Significado | Ejemplo |
|----------|-------------|---------|
| `\n` | Nueva línea | `"Línea 1\nLínea 2"` |
| `\t` | Tabulación | `"Col1\tCol2"` |
| `\\` | Barra invertida | `"C:\\Users"` |
| `\'` | Comilla simple | `"It\'s ok"` |
| `\"` | Comilla doble | `"Dijo \"Hola\""` |

```python
print("Primera línea\nSegunda línea")
# Primera línea
# Segunda línea

print("Nombre:\tAna")
print("Edad:\t25")
# Nombre:	Ana
# Edad:	25
```

### 6. Strings Multilínea

Para texto de varias líneas, usa triple comillas:

```python
mensaje = """
Este es un mensaje
que ocupa varias líneas
sin necesidad de \n
"""
print(mensaje)
```

**Salida:**
```

Este es un mensaje
que ocupa varias líneas
sin necesidad de \n

```

### 7. Comentarios

Los comentarios son notas en el código que Python ignora. Son esenciales para documentar.

#### Comentario de una línea

```python
# Esto es un comentario
print("Hola")  # Esto también es un comentario
```

#### Comentarios de varias líneas

```python
# Este es un comentario
# que ocupa varias
# líneas

"""
También puedes usar triple comillas
para comentarios largos,
aunque técnicamente es un string multilínea
"""
```

#### ¿Cuándo comentar?

```python
# ✅ BIEN - Explica el "por qué"
# Usamos 1.08 porque el IVA en México es 8%
total = subtotal * 1.08

# ❌ MAL - Explica lo obvio
# Multiplicar subtotal por 1.08
total = subtotal * 1.08
```

### 8. Errores Comunes

#### SyntaxError: Comillas no cerradas

```python
# ❌ Error
print("Hola)

# ✅ Correcto
print("Hola")
```

**Mensaje de error:**
```
SyntaxError: unterminated string literal
```

#### SyntaxError: Paréntesis no cerrados

```python
# ❌ Error
print("Hola"

# ✅ Correcto
print("Hola")
```

#### NameError: print mal escrito

```python
# ❌ Error
Print("Hola")  # Python es case-sensitive

# ✅ Correcto
print("Hola")
```

**Mensaje de error:**
```
NameError: name 'Print' is not defined
```

### 9. Ejecutar tu Programa

#### Opción 1: Python interactivo

```bash
docker run -it --rm python:3.13-slim
>>> print("Hola")
Hola
>>> exit()
```

#### Opción 2: Archivo .py

1. Crea un archivo `hola.py`:
   ```python
   print("¡Hola, Mundo!")
   print("Mi primer programa en Python")
   ```

2. Ejecútalo:
   ```bash
   docker run -it --rm -v $(pwd):/app python:3.13-slim python /app/hola.py
   ```

### 10. Buenas Prácticas desde el Día 1

```python
# ✅ BIEN - Código limpio y legible
print("Bienvenido al sistema")
print("=" * 30)
print("Usuario:", "admin")
print("Fecha:", "2026-01-02")

# ❌ MAL - Todo junto, difícil de leer
print("Bienvenido al sistema");print("="*30);print("Usuario:","admin")
```

---

## 🔥 Mini Ejercicios

### Ejercicio 1
Imprime tu nombre completo:
```python
print("Tu nombre aquí")
```

### Ejercicio 2
Imprime una "tarjeta de presentación":
```
========================
Nombre: [Tu nombre]
Profesión: Estudiante de Python
País: [Tu país]
========================
```

### Ejercicio 3
Usa `sep` para imprimir una fecha en formato DD/MM/AAAA:
```python
print("15", "01", "2026", sep="/")
```

---

## 📚 Recursos Adicionales

- [Python print() - Documentación Oficial](https://docs.python.org/3/library/functions.html#print)
- [Real Python - print()](https://realpython.com/python-print/)

---

## ✅ Checklist de Verificación

- [ ] Puedo escribir y ejecutar un programa con `print()`
- [ ] Entiendo la diferencia entre comillas simples y dobles
- [ ] Sé usar `sep` y `end` en print
- [ ] Conozco los caracteres de escape (`\n`, `\t`)
- [ ] Sé escribir comentarios en Python
- [ ] Puedo identificar errores de sintaxis básicos

---

<p align="center">
  <a href="02-configuracion-entorno.md">⬅️ Anterior</a> •
  <a href="04-variables-tipos.md">Siguiente: Variables y Tipos de Datos ➡️</a>
</p>
