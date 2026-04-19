# 🔀 Ejercicio 02: Condicionales

## 🎯 Objetivo

Dominar las estructuras condicionales if/elif/else y el operador ternario.

---

## 📋 Instrucciones

En este ejercicio aprenderás a:

1. Usar estructuras if/elif/else
2. Combinar condiciones con operadores lógicos
3. Aplicar el operador ternario
4. Implementar validaciones de entrada

**Abre `starter/main.py`** y descomenta el código de cada paso según las instrucciones.

---

## 📝 Pasos

### Paso 1: Estructura if Básica

La estructura más simple de control de flujo.

```python
# Ejemplo
age = 20
if age >= 18:
    print("Mayor de edad")
```

### Paso 2: Estructura if-else

Ejecuta un bloque u otro según la condición.

```python
# Ejemplo
temperature = 15
if temperature > 25:
    print("Hace calor")
else:
    print("No hace tanto calor")
```

### Paso 3: Estructura if-elif-else

Para múltiples condiciones mutuamente excluyentes.

```python
# Ejemplo
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C o menos"
```

### Paso 4: Condiciones Compuestas

Combinando condiciones con `and`, `or`, `not`.

```python
# Ejemplo
age = 25
has_license = True
if age >= 18 and has_license:
    print("Puede conducir")
```

### Paso 5: Operador Ternario

Forma concisa para asignaciones condicionales.

```python
# Ejemplo
status = "adulto" if age >= 18 else "menor"
```

---

## ✅ Verificación

Al ejecutar el código completo, deberías ver:

```
=== ESTRUCTURA IF BÁSICA ===
Eres mayor de edad
...

=== IF-ELIF-ELSE ===
Tu calificación es: B
...

=== OPERADOR TERNARIO ===
Estado: adulto
...
```

---

## 💡 Tips

- El orden de los `elif` importa: de más específico a menos específico
- Evita anidamiento excesivo (máximo 2-3 niveles)
- Usa el operador ternario solo para casos simples
- No compares con `== True` o `== False`
