"""
🧮 Proyecto Semana 01: Calculadora Básica

Descripción:
    Calculadora interactiva que realiza operaciones matemáticas básicas.

Instrucciones:
    1. Completa los TODOs en cada sección
    2. Ejecuta el programa para probar tu implementación
    3. Verifica que todos los casos funcionen correctamente

Comando para ejecutar:
    docker run -it --rm -v $(pwd):/app -w /app python:3.13-slim python main.py
"""


def mostrar_encabezado() -> None:
    """Muestra el encabezado de la calculadora."""
    # TODO: Implementar
    # 1. Imprime una línea de 60 caracteres "="
    # 2. Imprime el título centrado: "🧮 CALCULADORA PYTHON"
    # 3. Imprime otra línea de 60 caracteres "="
    # Pista: usa print("=" * 60) y .center(60)
    pass


def mostrar_menu() -> None:
    """Muestra el menú de operaciones disponibles."""
    # TODO: Implementar
    # Muestra las operaciones disponibles:
    #   +   Suma
    #   -   Resta
    #   *   Multiplicación
    #   /   División
    #   //  División entera
    #   %   Módulo (resto)
    #   **  Potencia
    # Pista: usa \t para alinear
    pass


def obtener_numeros() -> tuple[float, float]:
    """
    Solicita dos números al usuario.

    Returns:
        tuple[float, float]: Los dos números ingresados
    """
    # TODO: Implementar
    # 1. Usa input() para solicitar el primer número
    # 2. Convierte a float con float()
    # 3. Repite para el segundo número
    # 4. Retorna ambos números como tupla: (num1, num2)
    # Pista: return num1, num2
    pass


def obtener_operacion() -> str:
    """
    Solicita la operación a realizar.

    Returns:
        str: El símbolo de la operación
    """
    # TODO: Implementar
    # 1. Usa input() para solicitar la operación
    # 2. Retorna el string ingresado
    pass


def calcular(num1: float, num2: float, operacion: str) -> float | str:
    """
    Realiza el cálculo según la operación indicada.

    Args:
        num1: Primer número
        num2: Segundo número
        operacion: Símbolo de la operación (+, -, *, /, //, %, **)

    Returns:
        float | str: El resultado del cálculo o mensaje de error
    """
    # TODO: Implementar
    # 1. Usa if/elif/else para cada operación
    # 2. Para división (/ y //), verifica que num2 no sea 0
    # 3. Si num2 es 0, retorna el string "Error: División por cero"
    # 4. Para módulo (%), también verifica división por cero
    # 5. Retorna el resultado de la operación
    #
    # Estructura sugerida:
    # if operacion == "+":
    #     return num1 + num2
    # elif operacion == "-":
    #     ...
    pass


def mostrar_resultado(num1: float, num2: float, operacion: str, resultado: float | str) -> None:
    """
    Muestra el resultado formateado.

    Args:
        num1: Primer número
        num2: Segundo número
        operacion: Operación realizada
        resultado: Resultado del cálculo
    """
    # TODO: Implementar
    # 1. Imprime línea separadora
    # 2. Si resultado es string (error), muestra título "⚠️ ERROR"
    # 3. Si no, muestra título "📊 RESULTADO"
    # 4. Imprime el cálculo: "num1 operacion num2 = resultado"
    # 5. Imprime línea separadora final
    #
    # Pista para verificar si es error:
    # if isinstance(resultado, str):
    #     # Es un mensaje de error
    pass


def main() -> None:
    """Función principal que ejecuta la calculadora."""
    # TODO: Implementar
    # 1. Llama a mostrar_encabezado()
    # 2. Llama a mostrar_menu()
    # 3. Obtén los números con obtener_numeros()
    # 4. Obtén la operación con obtener_operacion()
    # 5. Calcula el resultado con calcular()
    # 6. Muestra el resultado con mostrar_resultado()
    pass


# Punto de entrada del programa
if __name__ == "__main__":
    main()
