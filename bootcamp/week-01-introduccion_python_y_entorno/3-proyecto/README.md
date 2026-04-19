# 🧮 Proyecto Semana 01: Calculadora Básica

![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python&logoColor=white)
![Nivel](https://img.shields.io/badge/Nivel-Principiante-green)
![Tiempo](https://img.shields.io/badge/Tiempo-1.5--2h-orange)

## 📋 Descripción

Desarrollarás una **calculadora interactiva** en la terminal que permita al usuario realizar operaciones matemáticas básicas. Este proyecto integra todo lo aprendido en la Semana 01: `print()`, variables, tipos de datos y operadores.

---

## 🎯 Objetivos de Aprendizaje

Al completar este proyecto, habrás practicado:

- ✅ Uso de `print()` para mostrar información formateada
- ✅ Declaración de variables con type hints
- ✅ Uso de `input()` para obtener datos del usuario
- ✅ Conversión de tipos (casting)
- ✅ Operadores aritméticos
- ✅ f-strings para formateo de salida

---

## 📁 Estructura del Proyecto

```
3-proyecto/
├── README.md          # Este archivo
├── starter/           # Código inicial (aquí trabajas)
│   └── main.py
└── solution/          # Solución (solo instructores)
    └── main.py
```

---

## 🚀 Instrucciones

### 1. Preparación

```bash
# Navega al directorio del proyecto
cd bootcamp/week-01/3-proyecto/starter
```

### 2. Ejecutar el programa

```bash
docker run -it --rm -v $(pwd):/app -w /app python:3.13-slim python main.py
```

### 3. Implementar las funciones

Abre `starter/main.py` y completa los **TODOs** siguiendo las instrucciones en los comentarios.

---

## 📝 Requerimientos Funcionales

La calculadora debe:

1. **Mostrar un menú** con las operaciones disponibles
2. **Solicitar dos números** al usuario
3. **Solicitar la operación** a realizar
4. **Mostrar el resultado** formateado
5. **Manejar casos especiales** (división por cero)

### Operaciones requeridas

| Operación | Símbolo | Ejemplo |
|-----------|---------|---------|
| Suma | `+` | `5 + 3 = 8` |
| Resta | `-` | `5 - 3 = 2` |
| Multiplicación | `*` | `5 * 3 = 15` |
| División | `/` | `5 / 3 = 1.67` |
| División entera | `//` | `5 // 3 = 1` |
| Módulo | `%` | `5 % 3 = 2` |
| Potencia | `**` | `5 ** 3 = 125` |

---

## 💡 Pistas

### Obtener entrada del usuario

```python
# input() siempre retorna string
texto: str = input("Escribe algo: ")

# Para obtener números, convierte con int() o float()
numero: float = float(input("Ingresa un número: "))
```

### Formatear decimales

```python
resultado: float = 10 / 3
print(f"Resultado: {resultado:.2f}")  # 3.33 (2 decimales)
```

### Verificar división por cero

```python
if divisor == 0:
    print("Error: No se puede dividir por cero")
```

---

## 🎯 Ejemplo de Ejecución

```
============================================================
                    🧮 CALCULADORA PYTHON
============================================================

Operaciones disponibles:
  +   Suma
  -   Resta
  *   Multiplicación
  /   División
  //  División entera
  %   Módulo (resto)
  **  Potencia

============================================================

Ingresa el primer número: 15
Ingresa el segundo número: 4
Ingresa la operación (+, -, *, /, //, %, **): /

============================================================
                      📊 RESULTADO
============================================================

  15.0 / 4.0 = 3.75

============================================================
```

### Caso de división por cero

```
Ingresa el primer número: 10
Ingresa el segundo número: 0
Ingresa la operación (+, -, *, /, //, %, **): /

============================================================
                      ⚠️ ERROR
============================================================

  No se puede dividir por cero

============================================================
```

---

## ✅ Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| El programa ejecuta sin errores | 20 |
| Muestra menú formateado | 10 |
| Obtiene correctamente los números del usuario | 15 |
| Implementa las 7 operaciones | 25 |
| Maneja división por cero | 15 |
| Usa type hints en todas las variables | 10 |
| Código limpio y comentado | 5 |
| **Total** | **100** |

---

## 🔥 Desafíos Extra (Opcional)

Si terminaste antes, intenta agregar:

1. **Validación de operación**: Mostrar error si el usuario ingresa una operación inválida
2. **Modo continuo**: Permitir hacer múltiples cálculos sin reiniciar el programa
3. **Historial**: Guardar y mostrar los últimos 5 cálculos

---

## 📚 Recursos de Apoyo

- [Teoría: Variables y Tipos](../1-teoria/04-variables-tipos.md)
- [Teoría: Operadores](../1-teoria/05-operadores.md)
- [Ejercicio: Operadores](../2-ejercicios/03-operadores/)

---

## 🆘 ¿Necesitas ayuda?

1. Revisa los archivos de teoría de la semana
2. Consulta los ejercicios resueltos
3. Pregunta en el foro del curso
4. Revisa la documentación de Python: [input()](https://docs.python.org/3/library/functions.html#input)

---

<p align="center">
  <strong>¡Buena suerte! 🚀</strong>
</p>
