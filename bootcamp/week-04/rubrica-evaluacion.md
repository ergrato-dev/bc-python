# 📊 Rúbrica de Evaluación - Semana 04

## Comprehensions y Funciones

---

## 🎯 Competencias a Evaluar

| Competencia | Descripción |
|-------------|-------------|
| **C1** | Crear y usar list comprehensions con filtros |
| **C2** | Implementar dict y set comprehensions |
| **C3** | Definir funciones con type hints y docstrings |
| **C4** | Usar diferentes tipos de parámetros correctamente |
| **C5** | Comprender scope y retorno de valores |

---

## 🧠 Evaluación de Conocimiento (30%)

### Quiz Teórico

| Criterio | Excelente (100%) | Bueno (80%) | Suficiente (70%) | Insuficiente (<70%) |
|----------|------------------|-------------|------------------|---------------------|
| Comprensión de list comprehensions | Explica sintaxis, uso de condiciones y transformaciones con ejemplos | Entiende sintaxis básica y condiciones simples | Conoce sintaxis pero confunde con bucles for | No comprende la sintaxis |
| Dict y set comprehensions | Diferencia claramente ambos, sabe cuándo usar cada uno | Conoce ambos pero confunde casos de uso | Solo domina uno de los dos | No distingue entre comprehensions |
| Definición de funciones | Domina def, parámetros, return, docstrings y type hints | Conoce def, parámetros básicos y return | Define funciones básicas sin documentar | No puede definir funciones |
| Tipos de parámetros | Distingue posicional, keyword, default, *args, **kwargs | Conoce posicional, keyword y default | Solo usa parámetros posicionales | Confunde tipos de parámetros |
| Scope de variables | Entiende local, global, nonlocal y LEGB | Comprende local vs global | Confunde scope local y global | No entiende el concepto |

---

## 💪 Evaluación de Desempeño (40%)

### Ejercicio 01: Comprehensions Básicos

| Criterio | Excelente (100%) | Bueno (80%) | Suficiente (70%) | Insuficiente (<70%) |
|----------|------------------|-------------|------------------|---------------------|
| List comprehensions | Usa transformaciones y múltiples condiciones | Aplica transformaciones o condiciones | Solo comprehensions sin condiciones | Usa bucles for tradicionales |
| Dict comprehensions | Crea diccionarios complejos con filtros | Crea diccionarios básicos | Solo invierte diccionarios simples | No logra crear dict comprehensions |
| Set comprehensions | Aplica correctamente para eliminar duplicados | Usa set comprehensions básicos | Confunde con list comprehensions | No implementa set comprehensions |

### Ejercicio 02: Funciones y Parámetros

| Criterio | Excelente (100%) | Bueno (80%) | Suficiente (70%) | Insuficiente (<70%) |
|----------|------------------|-------------|------------------|---------------------|
| Definición de funciones | Funciones bien nombradas con type hints y docstrings | Funciones con type hints básicos | Funciones sin documentación | Errores de sintaxis en definición |
| Parámetros por defecto | Usa defaults correctamente en orden apropiado | Usa defaults pero orden incorrecto | Defaults causan errores | No usa valores por defecto |
| Parámetros keyword | Llama funciones con argumentos por nombre | Usa keywords en algunos casos | Solo usa argumentos posicionales | Confunde la sintaxis |

### Ejercicio 03: Funciones Avanzadas

| Criterio | Excelente (100%) | Bueno (80%) | Suficiente (70%) | Insuficiente (<70%) |
|----------|------------------|-------------|------------------|---------------------|
| *args | Implementa funciones con argumentos variables correctamente | Usa *args en casos simples | Entiende el concepto pero errores de implementación | No comprende *args |
| **kwargs | Maneja diccionarios de argumentos y los procesa | Usa **kwargs básicamente | Confunde con *args | No implementa **kwargs |
| Scope | Usa nonlocal cuando es necesario, respeta LEGB | Comprende local vs global | Abusa de global | Variables indefinidas por scope |

---

## 📦 Evaluación de Producto (30%)

### Proyecto: Procesador de Datos

| Criterio | Excelente (100%) | Bueno (80%) | Suficiente (70%) | Insuficiente (<70%) |
|----------|------------------|-------------|------------------|---------------------|
| **Funcionalidad** | Todas las funciones trabajan correctamente con edge cases | Funciones principales operan bien | Algunas funciones fallan en casos límite | Errores críticos de funcionamiento |
| **Comprehensions** | Usa comprehensions donde es idiomático, evita bucles innecesarios | Aplica comprehensions en la mayoría de casos | Mezcla comprehensions y bucles sin criterio | No usa comprehensions |
| **Diseño de funciones** | Funciones pequeñas, una responsabilidad, bien nombradas | Funciones claras pero algunas muy largas | Funciones funcionan pero difíciles de leer | Funciones confusas y mal estructuradas |
| **Type hints** | Type hints completos y correctos en todas las funciones | Type hints en funciones principales | Type hints incompletos | Sin type hints |
| **Docstrings** | Docstrings completos con Args, Returns y ejemplos | Docstrings con descripción y parámetros | Solo descripción básica | Sin docstrings |
| **Código limpio** | PEP 8, nombres descriptivos, sin código duplicado | Mayormente limpio con detalles menores | Algunos problemas de estilo | Código difícil de leer |

---

## 📋 Checklist de Entrega

### Ejercicios
- [ ] `01-comprehensions-basicos/starter/main.py`
  - [ ] List comprehensions con filtros
  - [ ] Dict comprehensions
  - [ ] Set comprehensions
  - [ ] Código ejecuta sin errores

- [ ] `02-funciones-parametros/starter/main.py`
  - [ ] Funciones con parámetros posicionales
  - [ ] Funciones con valores por defecto
  - [ ] Llamadas con argumentos keyword
  - [ ] Type hints en todas las funciones

- [ ] `03-funciones-avanzadas/starter/main.py`
  - [ ] Funciones con *args
  - [ ] Funciones con **kwargs
  - [ ] Demostración de scope
  - [ ] Docstrings completos

### Proyecto
- [ ] `3-proyecto/starter/main.py`
  - [ ] Función `filter_by_condition()` implementada
  - [ ] Función `transform_collection()` implementada
  - [ ] Función `aggregate_data()` implementada
  - [ ] Función `process_pipeline()` implementada
  - [ ] Type hints en todas las funciones
  - [ ] Docstrings con Args, Returns
  - [ ] Ejemplos de uso funcionando

---

## 🏆 Escala de Calificación Final

| Rango | Calificación | Descripción |
|-------|--------------|-------------|
| 95-100% | A+ | Excepcional - Dominio completo de comprehensions y funciones |
| 90-94% | A | Excelente - Muy buen manejo de todos los conceptos |
| 85-89% | B+ | Muy Bueno - Sólido con detalles menores |
| 80-84% | B | Bueno - Comprende bien la mayoría de temas |
| 75-79% | C+ | Satisfactorio - Cumple requisitos básicos |
| 70-74% | C | Suficiente - Mínimo aceptable |
| <70% | F | Insuficiente - Requiere refuerzo |

---

## 📝 Retroalimentación

### Fortalezas Comunes
- Uso correcto de list comprehensions básicos
- Funciones bien definidas con return
- Comprensión de parámetros posicionales

### Áreas de Mejora Frecuentes
- Olvidar type hints en funciones
- Confundir *args con **kwargs
- No documentar funciones con docstrings
- Usar bucles cuando comprehensions son más claros
- Scope: abusar de variables globales

### Recursos de Refuerzo
- [Python Docs - List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [Python Docs - Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Real Python - Comprehensions](https://realpython.com/list-comprehension-python/)
- [Real Python - Python Functions](https://realpython.com/defining-your-own-python-function/)

---

*Rúbrica Semana 04 - Bootcamp Python Zero to Hero* 📊
