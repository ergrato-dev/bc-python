# 🏋️ Ejercicio 02: Funciones y Parámetros

## 🎯 Objetivo

Practicar la definición de funciones con diferentes tipos de parámetros: posicionales, con valores por defecto y keyword arguments.

---

## 📋 Instrucciones

1. Abre el archivo `starter/main.py`
2. Lee cada sección y descomenta el código correspondiente
3. Ejecuta el archivo para verificar los resultados
4. Compara tu output con el esperado

---

## 📚 Conceptos Cubiertos

- Definición de funciones con `def`
- Type hints para parámetros y retorno
- Docstrings con formato Google
- Parámetros posicionales
- Parámetros con valores por defecto
- Argumentos keyword (con nombre)
- Retorno de múltiples valores

---

## ✅ Resultado Esperado

```
=== PASO 1: Función Básica ===
Área: 78.54

=== PASO 2: Type Hints y Docstrings ===
¡Hola, Ana!
¡Hola, Bob!

=== PASO 3: Valores por Defecto ===
Hola, Ana!
Hi, Bob!
Buenos días, Carlos!

=== PASO 4: Múltiples Parámetros con Default ===
{'name': 'Ana', 'age': 25, 'city': 'Unknown', 'active': True}
{'name': 'Bob', 'age': 30, 'city': 'Madrid', 'active': True}
{'name': 'Carlos', 'age': 35, 'city': 'Barcelona', 'active': False}

=== PASO 5: Keyword Arguments ===
3 argumentos posicionales
2 argumentos keyword
Mixto: pos1=10, key1=a

=== PASO 6: Return Múltiple ===
Min: 1, Max: 9, Promedio: 5.0
Estadísticas: (1, 9, 5.0)

=== PASO 7: Early Return ===
Error: divisor es cero
Resultado: 5.0

=== PASO 8: Funciones que Llaman Funciones ===
Celsius: 25 -> Fahrenheit: 77.0
Fahrenheit: 77.0 -> Celsius: 25.0
Round trip: 25.0

=== PASO 9: Caso Práctico - Calculadora ===
10 + 5 = 15
10 - 5 = 5
10 * 5 = 50
10 / 5 = 2.0
10 / 0 = Error: División por cero
```

---

## 🚀 Ejecución

```bash
cd bootcamp/week-04/2-ejercicios/02-funciones-parametros/starter
python main.py
```

---

## 💡 Tips

- Siempre usa type hints: `def func(param: type) -> return_type:`
- Los parámetros con default van después de los sin default
- Para retornar múltiples valores, usa tuplas
- Early return simplifica la lógica
- Los docstrings se escriben justo después del `def`

---

## 📖 Referencia

- [Teoría: Funciones Básicas](../../1-teoria/03-funciones-basicas.md)
- [Teoría: Parámetros Avanzados](../../1-teoria/04-parametros-avanzados.md)
