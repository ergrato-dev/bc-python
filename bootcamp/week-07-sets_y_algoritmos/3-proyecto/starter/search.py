"""
Módulo de Búsqueda y Ordenamiento
=================================
Funciones para buscar y ordenar datos.
"""

import bisect


def search_items(
    items: list[str],
    query: str,
    use_binary: bool = False
) -> list[str]:
    """
    Busca items que contengan el query.

    Args:
        items: Lista de items donde buscar
        query: Texto a buscar (case-insensitive)
        use_binary: Si True y la lista está ordenada, optimiza búsqueda

    Returns:
        Lista de items que contienen el query
    """
    # TODO: Implementar
    # 1. Convertir query a minúsculas para búsqueda case-insensitive
    # 2. Filtrar items que contengan el query (también en minúsculas)
    # 3. Retornar lista de resultados
    pass


def binary_search(items: list[str], target: str) -> int:
    """
    Búsqueda binaria en lista ordenada.

    Args:
        items: Lista ORDENADA de strings
        target: Elemento a buscar

    Returns:
        Índice del elemento o -1 si no existe
    """
    # TODO: Implementar
    # Opción 1: Implementar manualmente con left/right/mid
    # Opción 2: Usar bisect.bisect_left y verificar si existe
    #
    # Con bisect:
    # 1. pos = bisect.bisect_left(items, target)
    # 2. Si pos < len(items) y items[pos] == target, retornar pos
    # 3. Si no, retornar -1
    pass


def sort_by_criteria(
    items: list[dict],
    criteria: list[tuple[str, bool]]
) -> list[dict]:
    """
    Ordena por múltiples criterios.

    Args:
        items: Lista de diccionarios a ordenar
        criteria: Lista de tuplas (campo, descendente)
                  Ej: [("sales", True), ("name", False)]
                  ordena por sales desc, luego name asc

    Returns:
        Nueva lista ordenada
    """
    # TODO: Implementar
    # 1. Crear función key que retorne tupla de valores
    # 2. Para campos descendentes, negar el valor (si es numérico)
    #    o usar técnica alternativa
    # 3. Usar sorted() con la función key
    #
    # Tip: Para ordenar descendente un número, multiplica por -1
    # Para strings descendentes, es más complejo (puedes ignorar ese caso)
    pass


def find_in_sorted(
    items: list[int],
    target: int
) -> dict[str, int | bool]:
    """
    Encuentra un elemento en lista ordenada y retorna estadísticas.

    Args:
        items: Lista ordenada de enteros
        target: Número a buscar

    Returns:
        dict con:
        - found: bool indicando si se encontró
        - index: índice donde está (o donde debería insertarse)
        - comparisons: número de comparaciones realizadas
    """
    # TODO: Implementar
    # 1. Usar búsqueda binaria manual para contar comparaciones
    # 2. Retornar diccionario con found, index y comparisons
    pass
