# 🔄 Semana 03: Bucles y Control de Flujo

## 📋 Descripción

Esta semana aprenderás a **repetir acciones** usando bucles `for` y `while`. Los bucles son fundamentales en programación: permiten automatizar tareas repetitivas, procesar colecciones de datos y crear programas interactivos.

---

## 🎯 Objetivos de Aprendizaje

Al finalizar esta semana serás capaz de:

- ✅ Usar bucles `for` para iterar sobre secuencias
- ✅ Usar la función `range()` para generar secuencias numéricas
- ✅ Implementar bucles `while` para repeticiones condicionales
- ✅ Controlar el flujo con `break`, `continue` y `else`
- ✅ Evitar bucles infinitos y errores comunes
- ✅ Aplicar patrones comunes de iteración

---

## 📚 Requisitos Previos

- ✅ Semana 01: Variables, tipos de datos, operadores
- ✅ Semana 02: Condicionales y operadores lógicos

---

## 🗂️ Estructura de la Semana

```
week-03/
├── README.md                    # Este archivo
├── rubrica-evaluacion.md        # Criterios de evaluación
├── 0-assets/                    # Recursos visuales
│   ├── week-03-header.svg
│   ├── 01-for-loop.svg
│   ├── 02-while-loop.svg
│   ├── 03-range-function.svg
│   └── 04-break-continue.svg
├── 1-teoria/                    # Material teórico
│   ├── 01-bucle-for.md
│   ├── 02-funcion-range.md
│   ├── 03-bucle-while.md
│   ├── 04-break-continue-else.md
│   └── 05-patrones-iteracion.md
├── 2-ejercicios/                # Ejercicios guiados
│   ├── 01-for-basico/
│   ├── 02-while-validacion/
│   └── 03-patrones-bucles/
├── 3-proyecto/                  # Proyecto semanal
│   ├── README.md
│   ├── starter/
│   └── solution/
├── 4-recursos/                  # Material adicional
│   ├── ebooks-free/
│   ├── videografia/
│   └── webgrafia/
└── 5-glosario/                  # Términos clave
    └── README.md
```

---

## 📝 Contenidos

### 1. Teoría (1-teoria/)

| Archivo | Tema | Duración |
|---------|------|----------|
| [01-bucle-for.md](1-teoria/01-bucle-for.md) | Bucle for e iteración | 25 min |
| [02-funcion-range.md](1-teoria/02-funcion-range.md) | Función range() | 20 min |
| [03-bucle-while.md](1-teoria/03-bucle-while.md) | Bucle while | 25 min |
| [04-break-continue-else.md](1-teoria/04-break-continue-else.md) | Control de bucles | 25 min |
| [05-patrones-iteracion.md](1-teoria/05-patrones-iteracion.md) | Patrones comunes | 20 min |

### 2. Ejercicios (2-ejercicios/)

| Ejercicio | Tema | Duración |
|-----------|------|----------|
| [01-for-basico](2-ejercicios/01-for-basico/) | Iteración con for | 40 min |
| [02-while-validacion](2-ejercicios/02-while-validacion/) | Bucles while y validación | 40 min |
| [03-patrones-bucles](2-ejercicios/03-patrones-bucles/) | Patrones y combinaciones | 40 min |

### 3. Proyecto (3-proyecto/)

| Proyecto | Descripción | Duración |
|----------|-------------|----------|
| [Generador de Tablas](3-proyecto/) | Sistema de tablas de multiplicar y patrones | 90 min |

---

## ⏱️ Distribución del Tiempo (6 horas)

| Actividad | Tiempo | Porcentaje |
|-----------|--------|------------|
| 📖 Teoría | 2 horas | 33% |
| 💻 Ejercicios | 2 horas | 33% |
| 🎯 Proyecto | 1.5 horas | 25% |
| 📝 Revisión | 0.5 horas | 9% |

---

## 📌 Entregables

1. **Ejercicios completados** (3 ejercicios)
2. **Proyecto funcional** con todas las features implementadas
3. **Código limpio** con type hints y comentarios

---

## 💡 Conceptos Clave

```python
# Bucle for - itera sobre secuencias
for letter in "Python":
    print(letter)

# range() - genera secuencias numéricas
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Bucle while - repite mientras condición sea True
count = 0
while count < 5:
    print(count)
    count += 1

# break - sale del bucle
for i in range(10):
    if i == 5:
        break
    print(i)

# continue - salta a la siguiente iteración
for i in range(5):
    if i == 2:
        continue
    print(i)
```

---

## ⚠️ Errores Comunes

| Error | Problema | Solución |
|-------|----------|----------|
| Bucle infinito | `while True:` sin `break` | Asegurar condición de salida |
| Off-by-one | `range(5)` vs `range(1, 6)` | Verificar inicio/fin |
| Modificar lista | Modificar lista mientras se itera | Usar copia o list comprehension |
| Olvidar incremento | `while` sin actualizar variable | Siempre actualizar condición |

---

## 🔗 Navegación

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|-------------|-----------|--------------|
| [Semana 02: Condicionales](../week-02/) | [Bootcamp](../../) | [Semana 04: Funciones](../week-04/) |

---

## 📚 Recursos Adicionales

- [4-recursos/ebooks-free/](4-recursos/ebooks-free/) - Libros gratuitos
- [4-recursos/videografia/](4-recursos/videografia/) - Videos recomendados
- [4-recursos/webgrafia/](4-recursos/webgrafia/) - Enlaces útiles
- [5-glosario/](5-glosario/) - Términos de la semana
