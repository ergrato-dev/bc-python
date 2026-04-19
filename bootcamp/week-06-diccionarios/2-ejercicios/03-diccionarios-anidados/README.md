# Ejercicio 03: Diccionarios Anidados

## 🎯 Objetivo

Trabajar con estructuras de datos complejas usando diccionarios anidados: acceso, modificación, iteración y aplanamiento.

---

## 📋 Descripción

En este ejercicio aprenderás a:

1. Acceder a datos en estructuras profundamente anidadas
2. Modificar valores en diccionarios anidados de forma segura
3. Iterar sobre estructuras multinivel
4. Aplanar y reconstruir estructuras anidadas
5. Usar dict comprehensions con estructuras complejas

---

## 🔧 Instrucciones

1. Abre el archivo `starter/main.py`
2. Lee cada sección y la explicación del concepto
3. **Descomenta** el código de cada paso para ejecutarlo
4. Observa los resultados y experimenta modificando valores

---

## 📚 Conceptos Cubiertos

### Paso 1: Acceso a Datos Anidados

```python
# Estructura anidada
company = {
    "engineering": {
        "alice": {"role": "senior", "salary": 80000}
    }
}

# Acceso encadenado
salary = company["engineering"]["alice"]["salary"]

# Acceso seguro con get()
bonus = company.get("engineering", {}).get("alice", {}).get("bonus", 0)
```

### Paso 2: Modificación Segura

```python
# Crear estructura si no existe
data = {}
data.setdefault("level1", {}).setdefault("level2", {})["value"] = 42

# Resultado: {"level1": {"level2": {"value": 42}}}
```

### Paso 3: Iteración Multinivel

```python
for dept, employees in company.items():
    for name, info in employees.items():
        print(f"{dept}: {name} - {info['role']}")
```

### Paso 4: Aplanar Estructuras

```python
# De anidado a plano
nested = {"a": {"b": 1, "c": 2}}
flat = {f"{k1}.{k2}": v for k1, inner in nested.items() for k2, v in inner.items()}
# {"a.b": 1, "a.c": 2}
```

### Paso 5: Dict Comprehensions Anidadas

```python
# Crear estructura anidada con comprehension
matrix = {
    i: {j: i * j for j in range(3)}
    for i in range(3)
}
```

---

## ✅ Resultado Esperado

Al descomentar todo el código, deberías ver:

```
=== PASO 1: Acceso a Datos Anidados ===
Empleados en Engineering: dict_keys(['alice', 'bob'])
Rol de Alice: senior
Salario de Alice: 80000
Bonus de Alice (seguro): 0
Nombre de usuario inexistente: Unknown

=== PASO 2: Modificación Segura ===
Después de modificar salario: 85000
Estructura creada: {'users': {'new_user': {'name': 'Charlie', 'role': 'junior'}}}
Después de agregar skills: {'users': {'new_user': {'name': 'Charlie', 'role': 'junior', 'skills': ['python']}}}

=== PASO 3: Iteración Multinivel ===
📁 ENGINEERING
  👤 alice: senior ($80,000)
  👤 bob: junior ($50,000)
📁 MARKETING
  👤 carol: manager ($90,000)

Total empleados: 3
Nómina total: $220,000

=== PASO 4: Aplanar Estructuras ===
Aplanado: {'server.host': 'localhost', 'server.port': 8080, 'database.host': 'db.local', 'database.name': 'myapp'}
Reconstruido: {'server': {'host': 'localhost', 'port': 8080}, 'database': {'host': 'db.local', 'name': 'myapp'}}

=== PASO 5: Dict Comprehensions Anidadas ===
Tabla de multiplicar:
1: {1: 1, 2: 2, 3: 3}
2: {1: 2, 2: 4, 3: 6}
3: {1: 3, 2: 6, 3: 9}
3 x 2 = 6
Seniors: {'engineering': ['alice'], 'marketing': ['carol']}
```

---

## 🔗 Navegación

- ⬅️ **Anterior**: [Métodos Avanzados](../02-metodos-avanzados/README.md)
- ➡️ **Siguiente**: [Proyecto - Gestor de Contactos](../../3-proyecto/README.md)
- 🏠 **Índice**: [README Semana 6](../../README.md)
