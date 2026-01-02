# 🧮 Proyecto: Generador de Tablas de Multiplicar

## 📖 Descripción

Desarrollarás un **generador de tablas de multiplicar** interactivo que permite al usuario crear, visualizar y exportar tablas de multiplicar personalizadas. El programa utilizará bucles `for` y `while`, validación de entrada, y patrones de iteración.

---

## 🎯 Objetivos de Aprendizaje

Al completar este proyecto, habrás practicado:

- ✅ Bucles `for` con `range()` para generar secuencias
- ✅ Bucles `while` para validación de entrada
- ✅ Sentencias `break` y `continue`
- ✅ Patrones de iteración (acumulador, contador)
- ✅ Menús interactivos
- ✅ Formateo de salida con f-strings

---

## 📋 Requisitos Funcionales

### 1. Menú Principal

El programa debe mostrar un menú con las siguientes opciones:

```
╔═══════════════════════════════════════╗
║   🧮 GENERADOR DE TABLAS             ║
╠═══════════════════════════════════════╣
║ 1. Generar tabla individual          ║
║ 2. Generar rango de tablas           ║
║ 3. Tabla personalizada               ║
║ 4. Buscar en tablas                  ║
║ 5. Estadísticas                      ║
║ 6. Salir                             ║
╚═══════════════════════════════════════╝
```

### 2. Funcionalidades

#### Opción 1: Tabla Individual
- Solicita un número (1-20)
- Genera la tabla de multiplicar del 1 al 10
- Ejemplo:
  ```
  Tabla del 7:
  7 x 1 = 7
  7 x 2 = 14
  ...
  7 x 10 = 70
  ```

#### Opción 2: Rango de Tablas
- Solicita número inicial y final
- Genera todas las tablas en ese rango
- Separador visual entre tablas

#### Opción 3: Tabla Personalizada
- Solicita: número base, inicio, fin, paso
- Ejemplo: tabla del 5, del 1 al 20, de 2 en 2
  ```
  5 x 1 = 5
  5 x 3 = 15
  5 x 5 = 25
  ...
  ```

#### Opción 4: Buscar en Tablas
- Solicita un número resultado
- Busca qué multiplicaciones dan ese resultado
- Ejemplo para 24:
  ```
  Multiplicaciones que dan 24:
  3 x 8 = 24
  4 x 6 = 24
  6 x 4 = 24
  8 x 3 = 24
  ```

#### Opción 5: Estadísticas
- Muestra cuántas tablas se han generado
- Tabla más solicitada
- Total de multiplicaciones mostradas

---

## 🏗️ Estructura del Proyecto

```
3-proyecto/
├── README.md           # Este archivo
├── starter/
│   └── main.py         # Código inicial con TODOs
└── solution/           # ⚠️ Solo instructores
    └── main.py
```

---

## 📝 Instrucciones

### Paso 1: Explorar el Código Inicial

Abre `starter/main.py` y familiarízate con la estructura:
- Funciones de utilidad (ya implementadas)
- Funciones principales (con TODOs)
- Bucle principal del menú

### Paso 2: Implementar Validación

Completa la función `get_valid_number()`:
- Usar `while` para solicitar hasta obtener entrada válida
- Validar que esté en el rango permitido
- Manejar errores con `try/except`

### Paso 3: Implementar Tabla Individual

Completa la función `generate_single_table()`:
- Usar `for` con `range()` para generar la tabla
- Formatear la salida correctamente

### Paso 4: Implementar Rango de Tablas

Completa la función `generate_table_range()`:
- Usar bucle anidado (for dentro de for)
- Agregar separadores entre tablas

### Paso 5: Implementar Tabla Personalizada

Completa la función `generate_custom_table()`:
- Usar `range(start, end, step)`
- Validar que step sea positivo

### Paso 6: Implementar Búsqueda

Completa la función `search_multiplication()`:
- Usar bucles anidados para buscar
- Acumular resultados encontrados

### Paso 7: Implementar Estadísticas

Completa la función `show_statistics()`:
- Mostrar datos del diccionario de estadísticas
- Formatear la salida

---

## ✅ Criterios de Evaluación

### Funcionalidad (40%)
- [ ] Menú funciona correctamente
- [ ] Todas las opciones implementadas
- [ ] Validación de entrada robusta
- [ ] Sin errores de ejecución

### Uso de Bucles (30%)
- [ ] Uso correcto de `for` y `range()`
- [ ] Uso correcto de `while` para validación
- [ ] Uso apropiado de `break`/`continue`
- [ ] Bucles anidados cuando corresponde

### Código Limpio (20%)
- [ ] Type hints en funciones
- [ ] Nombres descriptivos
- [ ] Código bien organizado
- [ ] Comentarios donde necesario

### Extras (10%)
- [ ] Formateo visual atractivo
- [ ] Manejo de casos borde
- [ ] Funcionalidades adicionales

---

## 🎨 Ejemplo de Ejecución

```
╔═══════════════════════════════════════╗
║   🧮 GENERADOR DE TABLAS             ║
╠═══════════════════════════════════════╣
║ 1. Generar tabla individual          ║
║ 2. Generar rango de tablas           ║
║ 3. Tabla personalizada               ║
║ 4. Buscar en tablas                  ║
║ 5. Estadísticas                      ║
║ 6. Salir                             ║
╚═══════════════════════════════════════╝

Elige una opción: 1
Ingresa un número (1-20): 7

╔════════════════════╗
║   TABLA DEL 7      ║
╠════════════════════╣
║  7 x  1 =    7     ║
║  7 x  2 =   14     ║
║  7 x  3 =   21     ║
║  7 x  4 =   28     ║
║  7 x  5 =   35     ║
║  7 x  6 =   42     ║
║  7 x  7 =   49     ║
║  7 x  8 =   56     ║
║  7 x  9 =   63     ║
║  7 x 10 =   70     ║
╚════════════════════╝
```

---

## 💡 Pistas

1. **Validación**: Usa `while True` con `break` cuando la entrada sea válida
2. **Formateo**: Usa f-strings con especificadores de ancho: `f"{num:2d}"`
3. **Búsqueda**: Para encontrar 24, busca todos los pares (i, j) donde `i * j == 24`
4. **Estadísticas**: Usa un diccionario global para almacenar datos

---

## 🚀 Extensiones Opcionales

Si terminas antes, intenta agregar:

1. **Guardar en archivo**: Exportar tablas a un archivo .txt
2. **Tabla visual**: Mostrar tabla como grid (matriz)
3. **Quiz mode**: Preguntar multiplicaciones y verificar respuestas
4. **Historial**: Guardar las últimas N operaciones

---

## 📚 Recursos

- [Python range()](https://docs.python.org/3/library/stdtypes.html#range)
- [Python f-strings](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals)
- [Python while](https://docs.python.org/3/reference/compound_stmts.html#while)
