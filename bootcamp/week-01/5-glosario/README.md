# 📖 Glosario - Semana 01

Términos técnicos ordenados alfabéticamente que aprenderás esta semana.

---

## A

### Argumento (Argument)
Valor que se pasa a una función cuando se llama.
```python
print("Hola")  # "Hola" es el argumento
```

### Asignación (Assignment)
Proceso de dar un valor a una variable usando el operador `=`.
```python
nombre = "Ana"  # Asignación del valor "Ana" a la variable nombre
```

---

## B

### Booleano (Boolean / bool)
Tipo de dato que solo puede tener dos valores: `True` o `False`.
```python
es_mayor: bool = True
activo: bool = False
```

### Built-in Function
Función incorporada en Python, disponible sin necesidad de importar nada.
```python
print()   # Built-in
type()    # Built-in
int()     # Built-in
```

---

## C

### Cadena de texto (String / str)
Secuencia de caracteres entre comillas. Ver también: **String**.
```python
mensaje: str = "Hola, mundo"
```

### Casting
Conversión explícita de un tipo de dato a otro.
```python
numero: int = int("42")      # String a int
texto: str = str(100)        # Int a string
decimal: float = float(5)    # Int a float
```

### Comentario (Comment)
Texto en el código que Python ignora. Usado para documentar.
```python
# Esto es un comentario de una línea

"""
Esto es un comentario
de múltiples líneas
"""
```

### Concatenación
Unir strings usando el operador `+`.
```python
saludo: str = "Hola" + " " + "Mundo"  # "Hola Mundo"
```

---

## D

### Docker
Plataforma para ejecutar aplicaciones en contenedores aislados.

### Docker Compose
Herramienta para definir y ejecutar aplicaciones Docker multi-contenedor.

---

## E

### Entero (Integer / int)
Tipo de dato numérico sin decimales.
```python
edad: int = 25
negativo: int = -10
```

### Expresión (Expression)
Combinación de valores, variables y operadores que produce un resultado.
```python
5 + 3        # Expresión que resulta en 8
x * 2        # Expresión que usa una variable
```

---

## F

### f-String (Formatted String Literal)
Manera moderna de formatear strings en Python 3.6+.
```python
nombre: str = "Ana"
print(f"Hola, {nombre}")  # "Hola, Ana"
```

### Float (Punto Flotante)
Tipo de dato numérico con decimales.
```python
precio: float = 99.99
pi: float = 3.14159
```

### Función (Function)
Bloque de código reutilizable que realiza una tarea específica.
```python
print()  # Función que imprime en consola
type()   # Función que retorna el tipo de un valor
```

---

## I

### IDE (Integrated Development Environment)
Entorno de desarrollo integrado. VS Code es un editor de código que funciona como IDE.

### Identación (Indentation)
Espacios al inicio de una línea que definen bloques de código en Python.
```python
if True:
    print("Esto está indentado")  # 4 espacios
```

### Input
Función para obtener entrada del usuario.
```python
nombre: str = input("¿Cómo te llamas? ")
```

### Intérprete (Interpreter)
Programa que ejecuta código Python línea por línea.

---

## L

### Literal
Valor escrito directamente en el código.
```python
42        # Literal entero
3.14      # Literal float
"Hola"    # Literal string
True      # Literal booleano
```

---

## M

### Módulo (Module)
Archivo Python que contiene código reutilizable.

### Módulo/Resto (Modulo)
Operador `%` que retorna el resto de una división.
```python
resto: int = 10 % 3  # 1
```

---

## N

### None
Valor especial que representa "nada" o "sin valor".
```python
resultado: None = None
```

---

## O

### Operador (Operator)
Símbolo que realiza una operación sobre valores.
```python
+   # Suma
-   # Resta
*   # Multiplicación
/   # División
==  # Comparación de igualdad
```

---

## P

### Parámetro (Parameter)
Variable en la definición de una función.
```python
def saludar(nombre):  # 'nombre' es el parámetro
    print(f"Hola, {nombre}")
```

### PEP (Python Enhancement Proposal)
Documento de diseño para Python. PEP 8 es la guía de estilo.

### Print
Función built-in para mostrar texto en la consola.
```python
print("Hola, mundo")
```

---

## R

### REPL (Read-Eval-Print Loop)
Entorno interactivo de Python donde escribes código y ves resultados inmediatamente.
```
>>> 2 + 2
4
```

---

## S

### Snake_case
Convención de nomenclatura donde las palabras se separan con guion bajo.
```python
nombre_completo: str = "Ana García"
fecha_nacimiento: str = "1995-05-15"
```

### String (Cadena de texto / str)
Secuencia de caracteres entre comillas.
```python
mensaje: str = "Hola, mundo"
otro: str = 'También válido'
```

### Syntax Error (Error de Sintaxis)
Error que ocurre cuando el código no sigue las reglas del lenguaje.
```python
print("Hola"  # SyntaxError: falta el paréntesis de cierre
```

---

## T

### Tipo de dato (Data Type)
Categoría de valores: `str`, `int`, `float`, `bool`, etc.

### Type Hint (Anotación de Tipo)
Indicación del tipo esperado de una variable.
```python
edad: int = 25
nombre: str = "Ana"
```

---

## U

### uv
Gestor de paquetes moderno y rápido para Python (alternativa a pip).

---

## V

### Variable
Nombre que hace referencia a un valor almacenado en memoria.
```python
edad: int = 25  # 'edad' es la variable, 25 es el valor
```

### VS Code (Visual Studio Code)
Editor de código popular para desarrollo en Python.

---

## Símbolos Especiales

### `\n`
Carácter de escape que representa una nueva línea.
```python
print("Línea 1\nLínea 2")
```

### `\t`
Carácter de escape que representa una tabulación.
```python
print("Columna1\tColumna2")
```

### `#`
Símbolo para iniciar un comentario de una línea.
```python
# Esto es un comentario
```

### `:`
Usado en type hints y para iniciar bloques de código.
```python
edad: int = 25  # Type hint
if True:        # Inicio de bloque
    pass
```

---

<p align="center">
  <a href="../README.md">⬅️ Volver al README de la Semana</a>
</p>
