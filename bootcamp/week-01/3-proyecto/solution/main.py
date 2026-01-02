"""
🧮 Proyecto Semana 01: Calculadora Básica - SOLUCIÓN

⚠️ ARCHIVO SOLO PARA INSTRUCTORES
Este archivo no debe compartirse con los estudiantes.

Comando para ejecutar:
    docker run -it --rm -v $(pwd):/app -w /app python:3.13-slim python main.py
"""


def mostrar_encabezado() -> None:
    """Muestra el encabezado de la calculadora."""
    print("=" * 60)
    print("🧮 CALCULADORA PYTHON".center(60))
    print("=" * 60)


def mostrar_menu() -> None:
    """Muestra el menú de operaciones disponibles."""
    print()
    print("Operaciones disponibles:")
    print("  +\tSuma")
    print("  -\tResta")
    print("  *\tMultiplicación")
    print("  /\tDivisión")
    print("  //\tDivisión entera")
    print("  %\tMódulo (resto)")
    print("  **\tPotencia")
    print()
    print("=" * 60)
    print()


def obtener_numeros() -> tuple[float, float]:
    """
    Solicita dos números al usuario.

    Returns:
        tuple[float, float]: Los dos números ingresados
    """
    num1: float = float(input("Ingresa el primer número: "))
    num2: float = float(input("Ingresa el segundo número: "))
    return num1, num2


def obtener_operacion() -> str:
    """
    Solicita la operación a realizar.

    Returns:
        str: El símbolo de la operación
    """
    operacion: str = input("Ingresa la operación (+, -, *, /, //, %, **): ")
    return operacion


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
    if operacion == "+":
        return num1 + num2
    elif operacion == "-":
        return num1 - num2
    elif operacion == "*":
        return num1 * num2
    elif operacion == "/":
        if num2 == 0:
            return "No se puede dividir por cero"
        return num1 / num2
    elif operacion == "//":
        if num2 == 0:
            return "No se puede dividir por cero"
        return num1 // num2
    elif operacion == "%":
        if num2 == 0:
            return "No se puede dividir por cero"
        return num1 % num2
    elif operacion == "**":
        return num1 ** num2
    else:
        return f"Operación '{operacion}' no válida"


def mostrar_resultado(num1: float, num2: float, operacion: str, resultado: float | str) -> None:
    """
    Muestra el resultado formateado.

    Args:
        num1: Primer número
        num2: Segundo número
        operacion: Operación realizada
        resultado: Resultado del cálculo
    """
    print()
    print("=" * 60)

    if isinstance(resultado, str):
        # Es un mensaje de error
        print("⚠️ ERROR".center(60))
        print("=" * 60)
        print()
        print(f"  {resultado}")
    else:
        # Es un resultado numérico
        print("📊 RESULTADO".center(60))
        print("=" * 60)
        print()
        # Formatear números: si es entero mostrar sin decimales
        if resultado == int(resultado):
            resultado_str: str = str(int(resultado))
        else:
            resultado_str: str = f"{resultado:.2f}"
        print(f"  {num1} {operacion} {num2} = {resultado_str}")

    print()
    print("=" * 60)


def main() -> None:
    """Función principal que ejecuta la calculadora."""
    # Mostrar interfaz
    mostrar_encabezado()
    mostrar_menu()

    # Obtener datos del usuario
    num1, num2 = obtener_numeros()
    operacion: str = obtener_operacion()

    # Calcular y mostrar resultado
    resultado: float | str = calcular(num1, num2, operacion)
    mostrar_resultado(num1, num2, operacion, resultado)


# Punto de entrada del programa
if __name__ == "__main__":
    main()
