# 🔁 Ejercicio 02: While y Validación

## 🎯 Objetivo

Practicar el bucle `while`, validación de entrada del usuario, y patrones comunes como menús interactivos.

---

## 📋 Instrucciones

Abre el archivo `starter/main.py` y sigue los pasos descomentando el código correspondiente a cada sección.

---

## Paso 1: While Básico

El bucle `while` repite mientras la condición sea verdadera:

```python
count = 1
while count <= 5:
    print(count)
    count += 1  # ¡Importante! Actualizar la variable
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

## Paso 2: Cuenta Regresiva

Usar `while` para contar hacia atrás:

```python
n = 5
while n > 0:
    print(n)
    n -= 1
print("¡Despegue!")
```

**Descomenta** la sección del Paso 2.

---

## Paso 3: Validación de Entrada Numérica

Solicitar entrada hasta que sea válida:

```python
number = -1
while number <= 0:
    try:
        number = int(input("Ingresa un número positivo: "))
        if number <= 0:
            print("Debe ser mayor que cero")
    except ValueError:
        print("Ingresa un número válido")
```

**Descomenta** la sección del Paso 3.

---

## Paso 4: Validación con Límite de Intentos

Limitar el número de intentos:

```python
attempts = 0
max_attempts = 3
success = False

while attempts < max_attempts and not success:
    password = input("Contraseña: ")
    attempts += 1
    if password == "secreto":
        success = True
```

**Descomenta** la sección del Paso 4.

---

## Paso 5: Bucle con Flag (Bandera)

Usar una variable booleana para controlar el bucle:

```python
valid = False
while not valid:
    value = input("Ingresa 'si' o 'no': ")
    if value.lower() in ["si", "no"]:
        valid = True
```

**Descomenta** la sección del Paso 5.

---

## Paso 6: While True con Break

Bucle infinito controlado con `break`:

```python
while True:
    command = input("Comando: ")
    if command == "salir":
        break
    print(f"Ejecutando: {command}")
```

**Descomenta** la sección del Paso 6.

---

## Paso 7: Acumulador con While

Sumar números hasta que el usuario termine:

```python
total = 0
while True:
    num = input("Número (enter para terminar): ")
    if num == "":
        break
    total += int(num)
print(f"Total: {total}")
```

**Descomenta** la sección del Paso 7.

---

## Paso 8: Menú Interactivo

Crear un menú con opciones:

```python
option = ""
while option != "4":
    print("1. Opción A")
    print("2. Opción B")
    print("3. Opción C")
    print("4. Salir")
    option = input("Elige: ")
```

**Descomenta** la sección del Paso 8.

---

## ✅ Verificación

Los pasos 3-8 son interactivos. Para cada uno:
1. Descomenta el código
2. Ejecuta el programa
3. Interactúa siguiendo las instrucciones
4. Observa el comportamiento del bucle

---

## 🎯 Conceptos Clave

- `while condicion:` repite mientras sea `True`
- Siempre actualiza la variable de control para evitar bucles infinitos
- `while True:` + `break` es útil para validación
- Los flags (banderas) booleanos simplifican condiciones complejas
- `try/except` maneja errores de entrada del usuario
