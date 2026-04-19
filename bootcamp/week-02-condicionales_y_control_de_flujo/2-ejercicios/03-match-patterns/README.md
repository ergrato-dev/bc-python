# 🎯 Ejercicio 03: Match Patterns

## 🎯 Objetivo

Dominar el pattern matching básico de Python 3.10+ con patrones literales, OR y guardas.

---

## 📋 Instrucciones

En este ejercicio aprenderás a:

1. Usar la sintaxis básica de match/case con strings y números
2. Combinar patrones con el operador OR (`|`)
3. Capturar valores en variables
4. Usar guardas (guards) con condiciones `if`

**Abre `starter/main.py`** y descomenta el código de cada paso según las instrucciones.

---

## 📝 Pasos

### Paso 1: Match Básico con Strings

La sintaxis básica para comparar valores de texto.

```python
# Ejemplo
match command.lower():
    case "start":
        return "Iniciando..."
    case "stop":
        return "Deteniendo..."
    case _:
        return "Comando desconocido"
```

### Paso 2: Match con Números

Match funciona igual con valores numéricos.

```python
# Ejemplo
match code:
    case 200:
        return "OK"
    case 404:
        return "Not Found"
    case _:
        return "Unknown"
```

### Paso 3: Patrones Combinados con OR

Usar `|` para agrupar múltiples valores en un solo case.

```python
# Ejemplo
match day:
    case "saturday" | "sunday":
        return "Fin de semana"
```

### Paso 4: Captura de Valores

Capturar el valor coincidente en una variable.

```python
# Ejemplo
match n:
    case 0:
        return "Es cero"
    case other:  # Captura cualquier otro valor
        return f"Es {other}"
```

### Paso 5: Guardas con if

Añadir condiciones adicionales a los patrones.

```python
# Ejemplo
match age:
    case n if n < 0:
        return "Inválido"
    case n if n < 18:
        return "Menor"
    case _:
        return "Adulto"
```

---

## ✅ Verificación

Al ejecutar el código completo, deberías ver:

```
=== MATCH BÁSICO ===
Iniciando sistema...
Deteniendo sistema...
...

=== PATRONES CON GUARDAS ===
Cero
Negativo: -5
...
```

---

## 💡 Tips

- El patrón `_` siempre debe ir **al final** (es el default)
- `|` permite agrupar casos que tienen el mismo resultado
- Las guardas (`if`) se evalúan después de que el patrón coincide
- El orden de los cases importa: el primero que coincida se ejecuta
