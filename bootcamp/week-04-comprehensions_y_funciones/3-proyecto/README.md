# 🚀 Proyecto: Procesador de Datos

## 📋 Descripción

Desarrollarás un **sistema de funciones para procesar colecciones de datos**. El proyecto integra comprehensions y funciones para filtrar, transformar y agregar datos de forma eficiente.

Este tipo de procesamiento es común en:
- Análisis de datos
- APIs y backends
- Procesamiento de logs
- ETL (Extract, Transform, Load)

---

## 🎯 Objetivos

- Aplicar list/dict comprehensions en casos reales
- Crear funciones reutilizables con type hints
- Usar `*args` y `**kwargs` para flexibilidad
- Implementar funciones de orden superior
- Escribir docstrings completos

---

## 📁 Estructura del Proyecto

```
3-proyecto/
├── README.md          # Este archivo
├── starter/
│   └── main.py        # Código inicial con TODOs
└── solution/
    └── main.py        # ⚠️ Solo para instructores
```

---

## 🔧 Funciones a Implementar

### 1. `filter_by_condition(items, key, value)`
Filtra una lista de diccionarios por una condición clave=valor.

```python
users = [
    {"name": "Ana", "role": "admin"},
    {"name": "Bob", "role": "user"},
    {"name": "Carlos", "role": "admin"}
]
filter_by_condition(users, "role", "admin")
# [{"name": "Ana", "role": "admin"}, {"name": "Carlos", "role": "admin"}]
```

### 2. `transform_items(items, key, transform_func)`
Aplica una función de transformación a un campo específico.

```python
products = [
    {"name": "Laptop", "price": 1000},
    {"name": "Mouse", "price": 25}
]
transform_items(products, "price", lambda x: x * 1.21)
# [{"name": "Laptop", "price": 1210.0}, {"name": "Mouse", "price": 30.25}]
```

### 3. `aggregate_by_key(items, key)`
Agrupa elementos por el valor de una clave.

```python
sales = [
    {"product": "A", "amount": 100},
    {"product": "B", "amount": 200},
    {"product": "A", "amount": 150}
]
aggregate_by_key(sales, "product")
# {"A": [{"product": "A", "amount": 100}, {"product": "A", "amount": 150}],
#  "B": [{"product": "B", "amount": 200}]}
```

### 4. `extract_field(items, field)`
Extrae un campo específico de cada elemento.

```python
users = [{"name": "Ana", "age": 25}, {"name": "Bob", "age": 30}]
extract_field(users, "name")
# ["Ana", "Bob"]
```

### 5. `apply_pipeline(items, *operations)`
Aplica una serie de operaciones en secuencia.

```python
data = [{"name": "ana", "score": 85}, {"name": "bob", "score": 42}]
result = apply_pipeline(
    data,
    lambda items: filter_by_condition(items, "score", lambda x: x >= 60),
    lambda items: transform_items(items, "name", str.upper)
)
```

---

## 📝 Requisitos

### Funcionales
- [ ] Todas las funciones implementadas
- [ ] Funciones manejan listas vacías sin error
- [ ] Transformaciones no modifican datos originales

### Código
- [ ] Type hints en todas las funciones
- [ ] Docstrings con Args y Returns
- [ ] Uso de comprehensions donde sea apropiado
- [ ] Nombres descriptivos de variables

### Extras (Opcional)
- [ ] Función `sort_by_field()` para ordenar
- [ ] Función `unique_values()` para valores únicos
- [ ] Manejo de errores con try/except

---

## 🚀 Ejecución

```bash
cd bootcamp/week-04/3-proyecto/starter
python main.py
```

---

## ✅ Output Esperado

```
=== DATOS DE PRUEBA ===
Empleados cargados: 5

=== TEST: filter_by_condition ===
Desarrolladores: 2
  - Ana (developer)
  - Diana (developer)

Activos: 4
  - Ana, Bob, Diana, Eva

=== TEST: transform_items ===
Salarios con aumento 10%:
  - Ana: $60500.00
  - Bob: $49500.00
  - Carlos: $71500.00
  - Diana: $58300.00
  - Eva: $46200.00

=== TEST: aggregate_by_key ===
Por departamento:
  - engineering: 2 empleados
  - sales: 1 empleados
  - hr: 2 empleados

=== TEST: extract_field ===
Nombres: ['Ana', 'Bob', 'Carlos', 'Diana', 'Eva']
Salarios únicos: 5

=== TEST: apply_pipeline ===
Pipeline: Desarrolladores activos con nombres en mayúscula
Resultado: [{'name': 'ANA', ...}, {'name': 'DIANA', ...}]

=== TODOS LOS TESTS PASARON ===
```

---

## 💡 Tips

1. **Comprehensions**: Usa list comprehensions para `filter_by_condition` y `transform_items`
2. **Copia de datos**: Usa `.copy()` para no modificar originales
3. **Callable**: El parámetro `transform_func` puede ser cualquier función
4. **Pipeline**: `apply_pipeline` debe aplicar funciones en orden

---

## 📊 Criterios de Evaluación

| Criterio | Peso | Descripción |
|----------|------|-------------|
| Funcionalidad | 40% | Todas las funciones operan correctamente |
| Comprehensions | 20% | Uso apropiado de comprehensions |
| Type Hints | 15% | Tipos correctos en parámetros y retorno |
| Docstrings | 15% | Documentación completa |
| Código Limpio | 10% | Legibilidad y buenas prácticas |

---

## 📚 Recursos

- [Teoría: List Comprehensions](../../1-teoria/01-list-comprehensions.md)
- [Teoría: Dict Comprehensions](../../1-teoria/02-dict-set-comprehensions.md)
- [Teoría: Funciones Básicas](../../1-teoria/03-funciones-basicas.md)
- [Teoría: Parámetros Avanzados](../../1-teoria/04-parametros-avanzados.md)
