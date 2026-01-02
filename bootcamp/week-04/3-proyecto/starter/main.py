"""
Proyecto: Procesador de Datos
=============================
Sistema de funciones para filtrar, transformar y agregar colecciones.

Instrucciones:
1. Implementa cada función siguiendo los TODOs
2. Usa comprehensions donde sea apropiado
3. Incluye type hints y docstrings
4. Ejecuta para verificar con los tests
"""

from typing import Any, Callable

# ============================================
# DATOS DE PRUEBA
# ============================================

EMPLOYEES = [
    {"name": "Ana", "role": "developer", "department": "engineering", "salary": 55000, "active": True},
    {"name": "Bob", "role": "sales", "department": "sales", "salary": 45000, "active": True},
    {"name": "Carlos", "role": "manager", "department": "hr", "salary": 65000, "active": False},
    {"name": "Diana", "role": "developer", "department": "engineering", "salary": 53000, "active": True},
    {"name": "Eva", "role": "recruiter", "department": "hr", "salary": 42000, "active": True},
]


# ============================================
# FUNCIÓN 1: filter_by_condition
# ============================================

def filter_by_condition(
    items: list[dict],
    key: str,
    value: Any
) -> list[dict]:
    """Filtra una lista de diccionarios por una condición clave=valor.

    Retorna los elementos donde item[key] == value.
    Si value es callable, retorna donde value(item[key]) es True.

    Args:
        items: Lista de diccionarios a filtrar.
        key: Clave por la cual filtrar.
        value: Valor a buscar, o función que retorna bool.

    Returns:
        Lista de diccionarios que cumplen la condición.

    Examples:
        >>> data = [{"name": "Ana", "age": 25}, {"name": "Bob", "age": 30}]
        >>> filter_by_condition(data, "name", "Ana")
        [{"name": "Ana", "age": 25}]
        >>> filter_by_condition(data, "age", lambda x: x > 26)
        [{"name": "Bob", "age": 30}]
    """
    # TODO: Implementar usando list comprehension
    # 1. Si 'value' es callable (función), usar value(item[key]) como condición
    # 2. Si no, comparar item[key] == value
    # 3. Retornar lista filtrada
    # Tip: usa callable(value) para verificar si es función
    pass


# ============================================
# FUNCIÓN 2: transform_items
# ============================================

def transform_items(
    items: list[dict],
    key: str,
    transform_func: Callable[[Any], Any]
) -> list[dict]:
    """Aplica una transformación a un campo de cada elemento.

    Crea una NUEVA lista con copias de los diccionarios donde
    el campo especificado ha sido transformado.

    Args:
        items: Lista de diccionarios a transformar.
        key: Clave del campo a transformar.
        transform_func: Función a aplicar al valor del campo.

    Returns:
        Nueva lista con los elementos transformados.

    Examples:
        >>> data = [{"name": "ana"}, {"name": "bob"}]
        >>> transform_items(data, "name", str.upper)
        [{"name": "ANA"}, {"name": "BOB"}]
    """
    # TODO: Implementar
    # 1. Crear copia de cada diccionario con .copy()
    # 2. Aplicar transform_func al campo key
    # 3. NO modificar la lista original
    # Tip: [{**item, key: transform_func(item[key])} for item in items]
    pass


# ============================================
# FUNCIÓN 3: aggregate_by_key
# ============================================

def aggregate_by_key(
    items: list[dict],
    key: str
) -> dict[Any, list[dict]]:
    """Agrupa elementos por el valor de una clave.

    Args:
        items: Lista de diccionarios a agrupar.
        key: Clave por la cual agrupar.

    Returns:
        Diccionario donde cada clave es un valor único del campo,
        y cada valor es la lista de elementos con ese valor.

    Examples:
        >>> data = [{"type": "A", "val": 1}, {"type": "B", "val": 2}, {"type": "A", "val": 3}]
        >>> aggregate_by_key(data, "type")
        {"A": [{"type": "A", "val": 1}, {"type": "A", "val": 3}], "B": [{"type": "B", "val": 2}]}
    """
    # TODO: Implementar
    # 1. Crear diccionario vacío para resultados
    # 2. Iterar sobre items
    # 3. Para cada item, obtener el valor de key
    # 4. Agregar item a la lista correspondiente
    # Tip: usa dict.setdefault(k, []) para inicializar listas
    pass


# ============================================
# FUNCIÓN 4: extract_field
# ============================================

def extract_field(
    items: list[dict],
    field: str
) -> list[Any]:
    """Extrae un campo específico de cada elemento.

    Args:
        items: Lista de diccionarios.
        field: Nombre del campo a extraer.

    Returns:
        Lista con los valores del campo especificado.

    Examples:
        >>> data = [{"name": "Ana", "age": 25}, {"name": "Bob", "age": 30}]
        >>> extract_field(data, "name")
        ["Ana", "Bob"]
    """
    # TODO: Implementar usando list comprehension
    # Tip: [item[field] for item in items]
    pass


# ============================================
# FUNCIÓN 5: apply_pipeline
# ============================================

def apply_pipeline(
    items: list[dict],
    *operations: Callable[[list[dict]], list[dict]]
) -> list[dict]:
    """Aplica una serie de operaciones en secuencia.

    Cada operación recibe una lista y retorna una lista.
    El resultado de una operación es la entrada de la siguiente.

    Args:
        items: Lista inicial de diccionarios.
        *operations: Funciones a aplicar en orden.

    Returns:
        Lista resultante después de todas las operaciones.

    Examples:
        >>> data = [{"name": "ana", "score": 85}, {"name": "bob", "score": 42}]
        >>> apply_pipeline(
        ...     data,
        ...     lambda x: filter_by_condition(x, "score", lambda s: s >= 60),
        ...     lambda x: transform_items(x, "name", str.upper)
        ... )
        [{"name": "ANA", "score": 85}]
    """
    # TODO: Implementar
    # 1. Empezar con items como resultado inicial
    # 2. Iterar sobre cada operación en operations
    # 3. Aplicar la operación al resultado actual
    # 4. Retornar resultado final
    pass


# ============================================
# FUNCIONES EXTRA (OPCIONAL)
# ============================================

def sort_by_field(
    items: list[dict],
    field: str,
    reverse: bool = False
) -> list[dict]:
    """Ordena una lista de diccionarios por un campo.

    Args:
        items: Lista a ordenar.
        field: Campo por el cual ordenar.
        reverse: Si True, orden descendente.

    Returns:
        Nueva lista ordenada.
    """
    # TODO (EXTRA): Implementar
    # Tip: usa sorted() con key=lambda
    pass


def unique_values(
    items: list[dict],
    field: str
) -> set[Any]:
    """Obtiene valores únicos de un campo.

    Args:
        items: Lista de diccionarios.
        field: Campo del cual extraer valores únicos.

    Returns:
        Set con valores únicos.
    """
    # TODO (EXTRA): Implementar con set comprehension
    pass


# ============================================
# TESTS
# ============================================

def run_tests():
    """Ejecuta tests para verificar las implementaciones."""

    print("=== DATOS DE PRUEBA ===")
    print(f"Empleados cargados: {len(EMPLOYEES)}")
    print()

    # Test filter_by_condition
    print("=== TEST: filter_by_condition ===")
    developers = filter_by_condition(EMPLOYEES, "role", "developer")
    if developers:
        print(f"Desarrolladores: {len(developers)}")
        for emp in developers:
            print(f"  - {emp['name']} ({emp['role']})")
    else:
        print("❌ filter_by_condition no implementada")
    print()

    active = filter_by_condition(EMPLOYEES, "active", True)
    if active:
        names = ", ".join(e["name"] for e in active)
        print(f"Activos: {len(active)}")
        print(f"  - {names}")
    print()

    # Test transform_items
    print("=== TEST: transform_items ===")
    with_raise = transform_items(EMPLOYEES, "salary", lambda x: x * 1.10)
    if with_raise:
        print("Salarios con aumento 10%:")
        for emp in with_raise:
            print(f"  - {emp['name']}: ${emp['salary']:.2f}")
    else:
        print("❌ transform_items no implementada")
    print()

    # Test aggregate_by_key
    print("=== TEST: aggregate_by_key ===")
    by_dept = aggregate_by_key(EMPLOYEES, "department")
    if by_dept:
        print("Por departamento:")
        for dept, emps in by_dept.items():
            print(f"  - {dept}: {len(emps)} empleados")
    else:
        print("❌ aggregate_by_key no implementada")
    print()

    # Test extract_field
    print("=== TEST: extract_field ===")
    names = extract_field(EMPLOYEES, "name")
    if names:
        print(f"Nombres: {names}")
        salaries = extract_field(EMPLOYEES, "salary")
        print(f"Salarios únicos: {len(set(salaries))}")
    else:
        print("❌ extract_field no implementada")
    print()

    # Test apply_pipeline
    print("=== TEST: apply_pipeline ===")
    print("Pipeline: Desarrolladores activos con nombres en mayúscula")
    result = apply_pipeline(
        EMPLOYEES,
        lambda x: filter_by_condition(x, "role", "developer"),
        lambda x: filter_by_condition(x, "active", True),
        lambda x: transform_items(x, "name", str.upper)
    )
    if result:
        print(f"Resultado: {result}")
    else:
        print("❌ apply_pipeline no implementada o sin resultados")
    print()

    print("=== TESTS COMPLETADOS ===")


# ============================================
# PUNTO DE ENTRADA
# ============================================

if __name__ == "__main__":
    run_tests()
