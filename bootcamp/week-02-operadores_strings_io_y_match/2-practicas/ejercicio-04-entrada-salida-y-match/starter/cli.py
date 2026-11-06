"""Ejercicio 04: un programa de terminal con argumentos, input, match y código de salida.

Descomenta cada PASO cuando el README te lo pida y ejecuta, por ejemplo:
    uv run python cli.py "sumar 2 3"
"""

import sys

# ============================================
# PASO 1: los argumentos llegan en sys.argv
# ============================================
# sys.argv[0] es el nombre del programa; desde sys.argv[1] van los argumentos, como str.
# Descomenta las siguientes líneas:
# print("argv:", sys.argv)

# ============================================
# PASO 2: dos salidas distintas
# ============================================
# print escribe en stdout; con file=sys.stderr, en la salida de errores.
# Descomenta las siguientes líneas:
# print("esto va a stdout")
# print("esto va a stderr", file=sys.stderr)

# ============================================
# PASO 3: la lógica, sin entrada ni salida
# ============================================
# run_command recibe una orden y DEVUELVE la respuesta: no lee ni imprime.
# Los errores empiezan por "error:" para que main sepa adónde mandarlos.
# Descomenta las siguientes líneas:
# def run_command(line: str) -> str:
#     match line.split():
#         case []:
#             return "error: orden vacía"
#         case ["hola", name]:
#             return f"Hola, {name}"
#         case ["sumar", a, b] if a.isdecimal() and b.isdecimal():
#             return str(int(a) + int(b))
#         case ["sumar", *_]:
#             return "error: uso: sumar <entero> <entero>"
#         case ["mayus", *words]:
#             return " ".join(words).upper()
#         case [unknown, *_]:
#             return f"error: comando desconocido: {unknown}"
#
#
# print(run_command("hola Ana"), "|", run_command("sumar 2 3"), "|", run_command("mayus el aire"))
# print(run_command("sumar dos 3"), "|", run_command("borrar todo"), "|", run_command("  "))

# ============================================
# PASO 4: main habla con el exterior
# ============================================
# Lee la orden (argumento o teclado), llama a la lógica, escribe donde toca
# y devuelve el código de salida: 0 bien, 1 error, 2 uso incorrecto.
# Descomenta las siguientes líneas:
# def main(argv: list[str]) -> int:
#     match argv:
#         case []:
#             line = input("orden> ")
#         case [line]:
#             pass
#         case _:
#             print('uso: cli.py ["orden"]', file=sys.stderr)
#             return 2
#     answer = run_command(line)
#     if answer.startswith("error:"):
#         print(answer, file=sys.stderr)
#         return 1
#     print(answer)
#     return 0
#
#
# if __name__ == "__main__":
#     raise SystemExit(main(sys.argv[1:]))
