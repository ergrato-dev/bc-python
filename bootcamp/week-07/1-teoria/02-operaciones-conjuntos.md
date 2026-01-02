# Operaciones de Conjuntos

## 🎯 Objetivos

- Dominar las operaciones matemáticas de conjuntos
- Aplicar unión, intersección, diferencia y diferencia simétrica
- Entender relaciones entre conjuntos (subconjunto, superconjunto)
- Usar operadores y métodos equivalentes

---

## 1. Operaciones Fundamentales

Python implementa las operaciones clásicas de la teoría de conjuntos:

| Operación | Símbolo | Método | Descripción |
|-----------|---------|--------|-------------|
| Unión | `\|` | `union()` | Elementos en A **o** B (o ambos) |
| Intersección | `&` | `intersection()` | Elementos en A **y** B |
| Diferencia | `-` | `difference()` | Elementos en A pero **no** en B |
| Diferencia Simétrica | `^` | `symmetric_difference()` | Elementos en A **o** B, pero **no** ambos |

---

## 2. Unión (`|` / `union()`)

Combina todos los elementos de ambos conjuntos (sin duplicados).

![Unión de conjuntos](../0-assets/01-set-operations.svg)

```python
a: set[int] = {1, 2, 3, 4}
b: set[int] = {3, 4, 5, 6}

# Con operador |
union_result = a | b
print(union_result)  # {1, 2, 3, 4, 5, 6}

# Con método union()
union_result = a.union(b)
print(union_result)  # {1, 2, 3, 4, 5, 6}

# union() acepta múltiples argumentos e iterables
c: set[int] = {7, 8}
union_all = a.union(b, c, [9, 10])
print(union_all)  # {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
```

### Caso de Uso: Combinar Listas de Usuarios

```python
admins: set[str] = {"alice", "bob"}
editors: set[str] = {"bob", "carol", "david"}
viewers: set[str] = {"carol", "eve", "frank"}

# Todos los usuarios únicos
all_users: set[str] = admins | editors | viewers
print(f"Total usuarios: {len(all_users)}")  # 6
print(all_users)  # {'alice', 'bob', 'carol', 'david', 'eve', 'frank'}
```

---

## 3. Intersección (`&` / `intersection()`)

Obtiene solo los elementos comunes a ambos conjuntos.

```python
a: set[int] = {1, 2, 3, 4}
b: set[int] = {3, 4, 5, 6}

# Con operador &
common = a & b
print(common)  # {3, 4}

# Con método intersection()
common = a.intersection(b)
print(common)  # {3, 4}

# Múltiples conjuntos
c: set[int] = {4, 5, 6, 7}
common_all = a.intersection(b, c)
print(common_all)  # {4} - solo 4 está en los tres
```

### Caso de Uso: Encontrar Intereses Comunes

```python
alice_hobbies: set[str] = {"reading", "gaming", "cooking", "hiking"}
bob_hobbies: set[str] = {"gaming", "music", "hiking", "photography"}
carol_hobbies: set[str] = {"hiking", "gaming", "yoga", "cooking"}

# Hobbies que comparten Alice y Bob
alice_bob_common = alice_hobbies & bob_hobbies
print(f"Alice y Bob: {alice_bob_common}")  # {'gaming', 'hiking'}

# Hobbies que comparten los tres
all_common = alice_hobbies & bob_hobbies & carol_hobbies
print(f"Los tres: {all_common}")  # {'gaming', 'hiking'}
```

---

## 4. Diferencia (`-` / `difference()`)

Obtiene elementos que están en el primer conjunto pero no en el segundo.

```python
a: set[int] = {1, 2, 3, 4}
b: set[int] = {3, 4, 5, 6}

# Elementos en A pero no en B
diff_a = a - b
print(diff_a)  # {1, 2}

# Elementos en B pero no en A
diff_b = b - a
print(diff_b)  # {5, 6}

# Con método difference()
diff_a = a.difference(b)
print(diff_a)  # {1, 2}

# Múltiples diferencias
c: set[int] = {1, 2}
result = a.difference(b, c)
print(result)  # set() - vacío, todos eliminados
```

### Caso de Uso: Encontrar Elementos Faltantes

```python
required_skills: set[str] = {"python", "sql", "git", "docker", "testing"}
candidate_skills: set[str] = {"python", "git", "javascript", "react"}

# Skills que le faltan al candidato
missing_skills = required_skills - candidate_skills
print(f"Skills faltantes: {missing_skills}")
# {'sql', 'docker', 'testing'}

# Skills extra del candidato (no requeridas)
extra_skills = candidate_skills - required_skills
print(f"Skills extra: {extra_skills}")
# {'javascript', 'react'}
```

---

## 5. Diferencia Simétrica (`^` / `symmetric_difference()`)

Obtiene elementos que están en uno u otro conjunto, pero **no en ambos**.

```python
a: set[int] = {1, 2, 3, 4}
b: set[int] = {3, 4, 5, 6}

# Elementos exclusivos de cada uno
sym_diff = a ^ b
print(sym_diff)  # {1, 2, 5, 6}

# Con método symmetric_difference()
sym_diff = a.symmetric_difference(b)
print(sym_diff)  # {1, 2, 5, 6}

# Es equivalente a: (A | B) - (A & B)
equivalent = (a | b) - (a & b)
print(equivalent)  # {1, 2, 5, 6}

# También: (A - B) | (B - A)
equivalent2 = (a - b) | (b - a)
print(equivalent2)  # {1, 2, 5, 6}
```

### Caso de Uso: Detectar Cambios

```python
yesterday_users: set[str] = {"alice", "bob", "carol", "david"}
today_users: set[str] = {"bob", "carol", "eve", "frank"}

# Usuarios que cambiaron (nuevos o que se fueron)
changed = yesterday_users ^ today_users
print(f"Cambios: {changed}")  # {'alice', 'david', 'eve', 'frank'}

# Desglose
new_users = today_users - yesterday_users
print(f"Nuevos: {new_users}")  # {'eve', 'frank'}

left_users = yesterday_users - today_users
print(f"Se fueron: {left_users}")  # {'alice', 'david'}
```

---

## 6. Operaciones In-Place (Modifican el Set Original)

Cada operación tiene una versión que modifica el set original:

| Operación | In-Place | Método In-Place |
|-----------|----------|-----------------|
| Unión | `\|=` | `update()` |
| Intersección | `&=` | `intersection_update()` |
| Diferencia | `-=` | `difference_update()` |
| Diferencia Simétrica | `^=` | `symmetric_difference_update()` |

```python
# Unión in-place
a: set[int] = {1, 2, 3}
a |= {4, 5}
print(a)  # {1, 2, 3, 4, 5}

# Intersección in-place
b: set[int] = {1, 2, 3, 4, 5}
b &= {2, 3, 4, 6}
print(b)  # {2, 3, 4}

# Diferencia in-place
c: set[int] = {1, 2, 3, 4, 5}
c -= {1, 2}
print(c)  # {3, 4, 5}

# Diferencia simétrica in-place
d: set[int] = {1, 2, 3}
d ^= {2, 3, 4}
print(d)  # {1, 4}
```

---

## 7. Relaciones entre Conjuntos

### 7.1 Subconjunto (`<=` / `issubset()`)

A es subconjunto de B si **todos** los elementos de A están en B.

```python
a: set[int] = {1, 2}
b: set[int] = {1, 2, 3, 4}

# A es subconjunto de B
print(a <= b)           # True
print(a.issubset(b))    # True

# B NO es subconjunto de A
print(b <= a)           # False

# Todo set es subconjunto de sí mismo
print(a <= a)           # True

# Subconjunto propio (estricto): <
print(a < b)            # True (A es subconjunto propio de B)
print(a < a)            # False (no es subconjunto propio de sí mismo)
```

### 7.2 Superconjunto (`>=` / `issuperset()`)

A es superconjunto de B si A **contiene todos** los elementos de B.

```python
a: set[int] = {1, 2, 3, 4}
b: set[int] = {1, 2}

# A es superconjunto de B
print(a >= b)             # True
print(a.issuperset(b))    # True

# Superconjunto propio (estricto): >
print(a > b)              # True
print(a > a)              # False
```

### 7.3 Conjuntos Disjuntos (`isdisjoint()`)

Dos conjuntos son disjuntos si NO tienen elementos en común.

```python
a: set[int] = {1, 2, 3}
b: set[int] = {4, 5, 6}
c: set[int] = {3, 4, 5}

# A y B son disjuntos (sin elementos comunes)
print(a.isdisjoint(b))  # True

# A y C NO son disjuntos (comparten el 3)
print(a.isdisjoint(c))  # False

# Equivalente a verificar si intersección está vacía
print(len(a & b) == 0)  # True
print(len(a & c) == 0)  # False
```

---

## 8. Tabla Resumen de Operaciones

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
```

| Operación | Resultado | Descripción |
|-----------|-----------|-------------|
| `a \| b` | `{1, 2, 3, 4, 5, 6}` | Todos los elementos |
| `a & b` | `{3, 4}` | Solo los comunes |
| `a - b` | `{1, 2}` | En A, no en B |
| `b - a` | `{5, 6}` | En B, no en A |
| `a ^ b` | `{1, 2, 5, 6}` | Exclusivos de cada uno |
| `a <= b` | `False` | ¿A subconjunto de B? |
| `a >= b` | `False` | ¿A superconjunto de B? |
| `a.isdisjoint(b)` | `False` | ¿Sin elementos comunes? |

---

## 9. Ejemplo Práctico: Sistema de Permisos

```python
def check_permissions(
    user_roles: set[str],
    required_roles: set[str],
    forbidden_roles: set[str]
) -> dict[str, bool | set[str]]:
    """
    Verifica permisos de usuario basado en roles.

    Args:
        user_roles: Roles que tiene el usuario
        required_roles: Roles necesarios para acceso
        forbidden_roles: Roles que impiden acceso

    Returns:
        dict con información de acceso
    """
    # Verificar si tiene algún rol prohibido
    has_forbidden = not user_roles.isdisjoint(forbidden_roles)

    # Verificar si tiene todos los roles requeridos
    has_all_required = required_roles <= user_roles

    # Roles que le faltan
    missing_roles = required_roles - user_roles

    # Roles extra (tiene pero no necesita)
    extra_roles = user_roles - required_roles - forbidden_roles

    return {
        "access_granted": has_all_required and not has_forbidden,
        "has_forbidden": has_forbidden,
        "missing_roles": missing_roles,
        "extra_roles": extra_roles
    }


# Ejemplo de uso
user: set[str] = {"editor", "viewer", "commenter"}
required: set[str] = {"editor", "viewer"}
forbidden: set[str] = {"banned", "suspended"}

result = check_permissions(user, required, forbidden)
print(f"Acceso: {result['access_granted']}")      # True
print(f"Roles faltantes: {result['missing_roles']}")  # set()
print(f"Roles extra: {result['extra_roles']}")    # {'commenter'}
```

---

## 10. Ejemplo Práctico: Análisis de Datos

```python
def analyze_user_activity(
    registered: set[str],
    active_today: set[str],
    active_yesterday: set[str],
    premium: set[str]
) -> dict[str, set[str] | int]:
    """Analiza actividad de usuarios usando operaciones de conjuntos."""

    return {
        # Usuarios que volvieron hoy (activos ayer y hoy)
        "returning": active_today & active_yesterday,

        # Usuarios nuevos hoy (activos hoy, no ayer)
        "new_today": active_today - active_yesterday,

        # Usuarios que se fueron (activos ayer, no hoy)
        "churned": active_yesterday - active_today,

        # Usuarios premium activos
        "premium_active": premium & active_today,

        # Usuarios premium inactivos
        "premium_inactive": premium - active_today,

        # Usuarios registrados nunca activos
        "never_active": registered - active_today - active_yesterday,

        # Total usuarios únicos activos (ayer o hoy)
        "total_active_users": len(active_today | active_yesterday),
    }


# Datos de ejemplo
registered = {"alice", "bob", "carol", "david", "eve", "frank", "grace"}
active_today = {"alice", "bob", "carol", "eve"}
active_yesterday = {"bob", "carol", "david", "frank"}
premium = {"alice", "david", "eve"}

analysis = analyze_user_activity(registered, active_today, active_yesterday, premium)

print("📊 Análisis de Usuarios")
print(f"  Volvieron hoy: {analysis['returning']}")        # {'bob', 'carol'}
print(f"  Nuevos hoy: {analysis['new_today']}")           # {'alice', 'eve'}
print(f"  Se fueron: {analysis['churned']}")              # {'david', 'frank'}
print(f"  Premium activos: {analysis['premium_active']}")  # {'alice', 'eve'}
print(f"  Nunca activos: {analysis['never_active']}")     # {'grace'}
```

---

## ✅ Checklist de Verificación

Antes de continuar, asegúrate de poder:

- [ ] Realizar unión con `|` y `union()`
- [ ] Realizar intersección con `&` e `intersection()`
- [ ] Realizar diferencia con `-` y `difference()`
- [ ] Realizar diferencia simétrica con `^`
- [ ] Usar operaciones in-place (`|=`, `&=`, `-=`, `^=`)
- [ ] Verificar subconjuntos y superconjuntos
- [ ] Usar `isdisjoint()` para verificar conjuntos sin elementos comunes
- [ ] Aplicar operaciones de conjuntos a problemas reales

---

## 🔗 Navegación

- ⬅️ **Anterior**: [Introducción a Sets](01-intro-sets.md)
- ➡️ **Siguiente**: [Frozenset y Aplicaciones](03-frozenset-aplicaciones.md)
- 🏠 **Índice**: [README](../README.md)
