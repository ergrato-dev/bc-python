# 🔍 Ejercicio 01: Comparaciones

## 🎯 Objetivo

Practicar el uso de operadores de comparación, identidad y pertenencia en Python.

---

## 📋 Instrucciones

En este ejercicio aprenderás a:

1. Usar operadores de comparación (`==`, `!=`, `<`, `>`, `<=`, `>=`)
2. Distinguir entre igualdad (`==`) e identidad (`is`)
3. Verificar pertenencia con `in` y `not in`
4. Aplicar comparaciones encadenadas

**Abre `starter/main.py`** y descomenta el código de cada paso según las instrucciones.

---

## 📝 Pasos

### Paso 1: Comparaciones Numéricas Básicas

Los operadores de comparación retornan `True` o `False`.

```python
# Ejemplo
x = 10
y = 5
print(x > y)   # True
print(x == y)  # False
```

### Paso 2: Comparaciones de Strings

Los strings se comparan lexicográficamente (orden Unicode).

```python
# Ejemplo
print("apple" < "banana")  # True - 'a' viene antes que 'b'
print("A" < "a")           # True - mayúsculas antes que minúsculas
```

### Paso 3: Igualdad vs Identidad

- `==` compara **valores**
- `is` compara **identidad** (mismo objeto en memoria)

```python
# Ejemplo
list1 = [1, 2, 3]
list2 = [1, 2, 3]
print(list1 == list2)  # True - mismo contenido
print(list1 is list2)  # False - diferentes objetos
```

### Paso 4: Operadores de Pertenencia

`in` verifica si un elemento existe dentro de una secuencia.

```python
# Ejemplo
fruits = ["apple", "banana", "orange"]
print("apple" in fruits)      # True
print("grape" not in fruits)  # True
```

### Paso 5: Comparaciones Encadenadas

Python permite encadenar comparaciones de forma elegante.

```python
# Ejemplo
age = 25
print(18 <= age <= 65)  # True - forma pythónica
```

---

## ✅ Verificación

Al ejecutar el código completo, deberías ver:

```
=== COMPARACIONES NUMÉRICAS ===
10 > 5: True
10 == 5: False
...

=== COMPARACIONES DE STRINGS ===
'apple' < 'banana': True
...

=== IGUALDAD VS IDENTIDAD ===
list1 == list2: True
list1 is list2: False
...
```

---

## 💡 Tips

- Usa `is` solo para comparar con `None`
- Las comparaciones encadenadas son más legibles que usar `and`
- Recuerda que las mayúsculas tienen valores Unicode menores
