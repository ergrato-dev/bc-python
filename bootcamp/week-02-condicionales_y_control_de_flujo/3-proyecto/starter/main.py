"""
🎮 Proyecto: Juego de Aventura - La Cueva del Dragón
====================================================

Objetivo: Crear un juego de aventura basado en texto con múltiples
caminos y finales usando condicionales y pattern matching.

Instrucciones:
1. Lee cada TODO y completa la implementación
2. Prueba frecuentemente para verificar que funciona
3. Asegúrate de tener al menos 3 finales diferentes
"""


# ============================================
# CONSTANTES Y CONFIGURACIÓN
# ============================================

GAME_TITLE = """
╔════════════════════════════════════════╗
║       🐉 LA CUEVA DEL DRAGÓN 🐉        ║
╚════════════════════════════════════════╝
"""

HELP_TEXT = """
📖 COMANDOS DISPONIBLES:
  1, 2, 3... - Seleccionar opción
  help       - Mostrar esta ayuda
  status     - Ver tu estado actual
  quit       - Salir del juego
"""


# ============================================
# FUNCIONES DE UTILIDAD
# ============================================

def show_title() -> None:
    """Muestra el título del juego."""
    print(GAME_TITLE)


def show_separator() -> None:
    """Muestra un separador visual."""
    print("\n" + "─" * 40 + "\n")


def get_player_name() -> str:
    """
    Solicita y retorna el nombre del jugador.

    TODO: Implementar
    - Pedir el nombre al usuario
    - Si está vacío, usar "Aventurero" como default
    - Retornar el nombre capitalizado
    """
    # TODO: Implementar lógica
    # 1. Usar input() para pedir el nombre
    # 2. Usar strip() para quitar espacios
    # 3. Si está vacío (falsy), usar "Aventurero"
    # 4. Retornar con capitalize()
    pass


def get_valid_choice(valid_options: list[str], prompt: str = "> ") -> str:
    """
    Obtiene una opción válida del usuario.

    Args:
        valid_options: Lista de opciones válidas
        prompt: Texto a mostrar antes del input

    Returns:
        La opción elegida (en minúsculas)

    TODO: Implementar
    - Loop hasta obtener una opción válida
    - Manejar comandos especiales (help, quit, status)
    - Retornar la opción válida
    """
    # TODO: Implementar lógica
    # 1. Loop while True
    # 2. Leer input y convertir a minúsculas
    # 3. Verificar si es un comando especial
    # 4. Verificar si está en valid_options
    # 5. Si no es válida, mostrar mensaje de error
    pass


def initialize_game(player_name: str) -> dict:
    """
    Inicializa el estado del juego.

    TODO: Implementar
    - Crear diccionario con el estado inicial
    - Incluir: player_name, items, current_room, health, playing
    """
    # TODO: Retornar diccionario con estado inicial
    # Campos sugeridos:
    # - player_name: str
    # - has_sword: bool (False)
    # - has_key: bool (False)
    # - current_room: str ("entrance")
    # - health: int (100)
    # - playing: bool (True)
    # - ending_type: str ("")
    pass


def show_status(game_state: dict) -> None:
    """
    Muestra el estado actual del jugador.

    TODO: Implementar
    - Mostrar nombre, salud, items obtenidos
    """
    # TODO: Implementar
    # Usar f-strings para mostrar:
    # - Nombre del jugador
    # - Salud actual
    # - Items (espada y/o llave)
    pass


# ============================================
# ESCENAS DEL JUEGO
# ============================================

def entrance_scene(game_state: dict) -> None:
    """
    Escena inicial: La entrada de la cueva.

    TODO: Implementar
    - Mostrar descripción de la escena
    - Dar opciones: izquierda o derecha
    - Actualizar current_room según elección
    """
    print(f"\n🚪 ENTRADA DE LA CUEVA")
    print(f"\n{game_state['player_name']}, te encuentras ante una cueva misteriosa.")
    print("Se dice que un dragón custodia un tesoro legendario en su interior.")
    print("\nDos caminos se abren ante ti:")
    print("  1. 🌑 Camino izquierdo (oscuro y frío)")
    print("  2. 💡 Camino derecho (iluminado por antorchas)")

    # TODO: Implementar lógica de decisión
    # 1. Obtener elección válida (1 o 2)
    # 2. Si elige 1, cambiar current_room a "left_path"
    # 3. Si elige 2, cambiar current_room a "right_path"
    pass


def left_path_scene(game_state: dict) -> None:
    """
    Escena del camino izquierdo: Encuentras una espada.

    TODO: Implementar
    - Descripción del camino oscuro
    - Opción de tomar la espada
    - Continuar hacia la cámara del dragón
    """
    print("\n🌑 CAMINO OSCURO")
    print("\nAvanzas con cuidado por el pasillo sombrío.")
    print("Tus ojos se adaptan a la oscuridad y ves algo brillar...")
    print("\n¡Es una espada antigua clavada en una roca!")

    print("\n¿Qué haces?")
    print("  1. ⚔️ Intentar sacar la espada")
    print("  2. 🚶 Ignorarla y continuar")

    # TODO: Implementar lógica de decisión
    # 1. Obtener elección válida
    # 2. Si elige 1, intentar sacar la espada
    #    - Puedes añadir una prueba (ej: preguntar algo)
    #    - Si tiene éxito, has_sword = True
    # 3. Cambiar current_room a "dragon_chamber"
    pass


def right_path_scene(game_state: dict) -> None:
    """
    Escena del camino derecho: Encuentras una llave.

    TODO: Implementar
    - Descripción del camino iluminado
    - Opción de tomar la llave
    - Continuar hacia la cámara del dragón
    """
    print("\n💡 CAMINO ILUMINADO")
    print("\nLas antorchas iluminan un pasillo decorado con grabados antiguos.")
    print("En un pequeño altar ves una llave dorada.")

    print("\n¿Qué haces?")
    print("  1. 🔑 Tomar la llave")
    print("  2. 🚶 Dejarla y continuar")

    # TODO: Implementar lógica de decisión
    # 1. Obtener elección válida
    # 2. Si elige 1, has_key = True
    # 3. Cambiar current_room a "dragon_chamber"
    pass


def dragon_chamber_scene(game_state: dict) -> None:
    """
    Escena final: La cámara del dragón.

    TODO: Implementar con MÚLTIPLES FINALES
    - Usar condicionales para diferentes finales según items
    - Al menos 3 finales diferentes:
      * Con espada: puedes luchar
      * Con llave: puedes abrir cofre secreto
      * Sin nada: el dragón te atrapa
      * Con ambos: final secreto
    """
    print("\n🐉 CÁMARA DEL DRAGÓN")
    print("\nEntras a una enorme caverna. Un dragón duerme sobre montañas de oro.")
    print("También ves un cofre antiguo con una cerradura dorada.")

    # Obtener estado actual
    has_sword = game_state["has_sword"]
    has_key = game_state["has_key"]

    # TODO: Implementar lógica de finales usando if/elif/else
    #
    # Final 1 (Secreto): Tiene espada Y llave
    #   - Puede abrir el cofre Y derrotar al dragón
    #   - ending_type = "hero"
    #
    # Final 2 (Victoria): Solo tiene espada
    #   - Puede luchar contra el dragón
    #   - ending_type = "warrior"
    #
    # Final 3 (Escape): Solo tiene llave
    #   - Puede abrir cofre y escapar por pasaje secreto
    #   - ending_type = "thief"
    #
    # Final 4 (Derrota): No tiene nada
    #   - El dragón despierta y lo atrapa
    #   - ending_type = "captured"
    #
    # Después de determinar el final:
    # game_state["current_room"] = "ending"
    pass


def show_ending(game_state: dict) -> None:
    """
    Muestra el final según ending_type.

    TODO: Implementar usando match/case
    - Mostrar texto diferente para cada tipo de final
    """
    ending = game_state.get("ending_type", "unknown")
    player = game_state["player_name"]

    print("\n" + "═" * 40)
    print("             🏆 FIN DEL JUEGO 🏆")
    print("═" * 40)

    # TODO: Implementar con match/case
    # match ending:
    #     case "hero":
    #         # Final secreto - héroe legendario
    #         pass
    #     case "warrior":
    #         # Derrotó al dragón en combate
    #         pass
    #     case "thief":
    #         # Escapó con parte del tesoro
    #         pass
    #     case "captured":
    #         # Fue capturado por el dragón
    #         pass
    #     case _:
    #         # Final desconocido
    #         pass
    pass


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def main() -> None:
    """
    Función principal que ejecuta el juego.

    TODO: Implementar el game loop
    - Mostrar título
    - Obtener nombre del jugador
    - Inicializar estado del juego
    - Loop principal con match/case para escenas
    """
    # TODO: Implementar
    # 1. Mostrar título
    # show_title()

    # 2. Obtener nombre del jugador
    # player_name = get_player_name()

    # 3. Mostrar bienvenida
    # print(f"\n¡Bienvenido/a, {player_name}!")

    # 4. Inicializar juego
    # game_state = initialize_game(player_name)

    # 5. Game loop
    # while game_state["playing"]:
    #     current_room = game_state["current_room"]
    #
    #     match current_room:
    #         case "entrance":
    #             entrance_scene(game_state)
    #         case "left_path":
    #             left_path_scene(game_state)
    #         case "right_path":
    #             right_path_scene(game_state)
    #         case "dragon_chamber":
    #             dragon_chamber_scene(game_state)
    #         case "ending":
    #             show_ending(game_state)
    #             game_state["playing"] = False
    #         case _:
    #             print("Error: Habitación desconocida")
    #             game_state["playing"] = False

    # 6. Despedida
    # print("\n¡Gracias por jugar! 🎮\n")
    pass


# ============================================
# PUNTO DE ENTRADA
# ============================================

if __name__ == "__main__":
    main()
