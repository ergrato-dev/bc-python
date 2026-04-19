"""
Proyecto: Generador de Tablas de Multiplicar
============================================
Un generador interactivo de tablas de multiplicar con múltiples funcionalidades.

Instrucciones:
1. Lee cada función y entiende qué debe hacer
2. Implementa los TODOs en orden
3. Prueba cada función antes de continuar
4. Ejecuta el programa completo al final
"""

# ============================================
# ESTADÍSTICAS GLOBALES
# ============================================
# Este diccionario almacena estadísticas de uso
stats: dict[str, int] = {
    "tables_generated": 0,
    "multiplications_shown": 0,
    "searches_performed": 0,
    "most_requested": 0,
    "request_counts": {},  # {número: cantidad de veces solicitado}
}


# ============================================
# FUNCIONES DE UTILIDAD (YA IMPLEMENTADAS)
# ============================================

def print_header() -> None:
    """Imprime el encabezado del menú principal."""
    print("\n╔═══════════════════════════════════════╗")
    print("║   🧮 GENERADOR DE TABLAS             ║")
    print("╠═══════════════════════════════════════╣")
    print("║ 1. Generar tabla individual          ║")
    print("║ 2. Generar rango de tablas           ║")
    print("║ 3. Tabla personalizada               ║")
    print("║ 4. Buscar en tablas                  ║")
    print("║ 5. Estadísticas                      ║")
    print("║ 6. Salir                             ║")
    print("╚═══════════════════════════════════════╝")


def print_separator() -> None:
    """Imprime una línea separadora."""
    print("-" * 40)


def update_stats(number: int, multiplications: int) -> None:
    """Actualiza las estadísticas globales."""
    stats["tables_generated"] += 1
    stats["multiplications_shown"] += multiplications

    # Actualizar conteo por número
    if number in stats["request_counts"]:
        stats["request_counts"][number] += 1
    else:
        stats["request_counts"][number] = 1

    # Actualizar más solicitado
    if stats["request_counts"][number] > stats["request_counts"].get(stats["most_requested"], 0):
        stats["most_requested"] = number


# ============================================
# FUNCIÓN: get_valid_number
# Solicita un número válido al usuario
# ============================================

def get_valid_number(prompt: str, min_val: int, max_val: int) -> int:
    """
    Solicita un número al usuario hasta que sea válido.

    Args:
        prompt: Mensaje a mostrar al usuario
        min_val: Valor mínimo aceptado
        max_val: Valor máximo aceptado

    Returns:
        int: Número válido ingresado por el usuario
    """
    # TODO: Implementar validación con while
    # 1. Crear bucle while True
    # 2. Mostrar el prompt y leer entrada
    # 3. Usar try/except para convertir a int
    # 4. Verificar que esté en el rango [min_val, max_val]
    # 5. Si es válido, retornar el número (break implícito)
    # 6. Si no es válido, mostrar mensaje de error apropiado

    pass  # Eliminar esta línea al implementar


# ============================================
# FUNCIÓN: generate_single_table
# Genera una tabla de multiplicar individual
# ============================================

def generate_single_table(number: int, start: int = 1, end: int = 10, step: int = 1) -> None:
    """
    Genera e imprime una tabla de multiplicar.

    Args:
        number: Número base de la tabla
        start: Multiplicador inicial (default: 1)
        end: Multiplicador final (default: 10)
        step: Incremento entre multiplicadores (default: 1)
    """
    # TODO: Implementar generación de tabla
    # 1. Imprimir encabezado de la tabla (ejemplo: "TABLA DEL 7")
    # 2. Usar for con range(start, end + 1, step)
    # 3. Para cada multiplicador, imprimir: "number x i = resultado"
    # 4. Usar f-strings con formato para alinear números
    # 5. Contar multiplicaciones mostradas
    # 6. Llamar a update_stats(number, count)

    pass  # Eliminar esta línea al implementar


# ============================================
# FUNCIÓN: generate_table_range
# Genera múltiples tablas consecutivas
# ============================================

def generate_table_range(start_num: int, end_num: int) -> None:
    """
    Genera tablas de multiplicar desde start_num hasta end_num.

    Args:
        start_num: Primera tabla a generar
        end_num: Última tabla a generar
    """
    # TODO: Implementar generación de rango de tablas
    # 1. Usar for con range(start_num, end_num + 1)
    # 2. Para cada número, llamar a generate_single_table()
    # 3. Imprimir separador entre tablas (excepto la última)

    pass  # Eliminar esta línea al implementar


# ============================================
# FUNCIÓN: generate_custom_table
# Genera una tabla con parámetros personalizados
# ============================================

def generate_custom_table() -> None:
    """
    Solicita parámetros al usuario y genera una tabla personalizada.

    Parámetros a solicitar:
    - Número base (1-100)
    - Multiplicador inicial (1-100)
    - Multiplicador final (1-100)
    - Paso/incremento (1-10)
    """
    # TODO: Implementar tabla personalizada
    # 1. Usar get_valid_number() para obtener cada parámetro
    # 2. Validar que inicio < fin
    # 3. Llamar a generate_single_table() con los parámetros

    pass  # Eliminar esta línea al implementar


# ============================================
# FUNCIÓN: search_multiplication
# Busca qué multiplicaciones dan un resultado
# ============================================

def search_multiplication(target: int, max_factor: int = 12) -> list[tuple[int, int]]:
    """
    Busca todas las multiplicaciones que dan el resultado target.

    Args:
        target: Número resultado a buscar
        max_factor: Factor máximo a considerar (default: 12)

    Returns:
        list: Lista de tuplas (a, b) donde a * b == target
    """
    # TODO: Implementar búsqueda
    # 1. Crear lista vacía para resultados
    # 2. Usar dos bucles for anidados (i de 1 a max_factor, j de 1 a max_factor)
    # 3. Si i * j == target, agregar (i, j) a la lista
    # 4. Opcional: evitar duplicados (solo agregar si i <= j)
    # 5. Incrementar stats["searches_performed"]
    # 6. Retornar la lista de resultados

    pass  # Eliminar esta línea al implementar


# ============================================
# FUNCIÓN: show_statistics
# Muestra las estadísticas de uso
# ============================================

def show_statistics() -> None:
    """Muestra las estadísticas de uso del programa."""
    # TODO: Implementar mostrar estadísticas
    # 1. Imprimir encabezado "ESTADÍSTICAS"
    # 2. Mostrar: tablas generadas, multiplicaciones mostradas
    # 3. Mostrar: búsquedas realizadas
    # 4. Mostrar: número más solicitado (si hay datos)
    # 5. Usar formato visual atractivo

    pass  # Eliminar esta línea al implementar


# ============================================
# FUNCIÓN: option_single_table
# Maneja la opción 1 del menú
# ============================================

def option_single_table() -> None:
    """Opción 1: Genera una tabla individual."""
    # TODO: Implementar opción 1
    # 1. Solicitar número con get_valid_number() (rango 1-20)
    # 2. Llamar a generate_single_table() con ese número

    pass  # Eliminar esta línea al implementar


# ============================================
# FUNCIÓN: option_table_range
# Maneja la opción 2 del menú
# ============================================

def option_table_range() -> None:
    """Opción 2: Genera un rango de tablas."""
    # TODO: Implementar opción 2
    # 1. Solicitar número inicial (1-20)
    # 2. Solicitar número final (debe ser >= inicial)
    # 3. Validar que final >= inicial
    # 4. Llamar a generate_table_range()

    pass  # Eliminar esta línea al implementar


# ============================================
# FUNCIÓN: option_search
# Maneja la opción 4 del menú
# ============================================

def option_search() -> None:
    """Opción 4: Busca multiplicaciones que dan un resultado."""
    # TODO: Implementar opción 4
    # 1. Solicitar número a buscar (1-1000)
    # 2. Llamar a search_multiplication()
    # 3. Si hay resultados, mostrarlos formateados
    # 4. Si no hay resultados, indicarlo al usuario

    pass  # Eliminar esta línea al implementar


# ============================================
# FUNCIÓN PRINCIPAL: main
# Bucle principal del programa
# ============================================

def main() -> None:
    """Función principal que ejecuta el menú interactivo."""
    print("\n🧮 ¡Bienvenido al Generador de Tablas de Multiplicar!")

    # TODO: Implementar bucle principal del menú
    # 1. Crear bucle while True
    # 2. Mostrar menú con print_header()
    # 3. Solicitar opción al usuario
    # 4. Usar match para ejecutar la opción correspondiente:
    #    - "1": option_single_table()
    #    - "2": option_table_range()
    #    - "3": generate_custom_table()
    #    - "4": option_search()
    #    - "5": show_statistics()
    #    - "6": mostrar despedida y break
    #    - _: mostrar "Opción no válida"

    pass  # Eliminar esta línea al implementar


# ============================================
# PUNTO DE ENTRADA
# ============================================

if __name__ == "__main__":
    main()
