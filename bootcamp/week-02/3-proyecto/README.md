# 🎮 Proyecto: Juego de Aventura

## 📋 Descripción

Crearás un **juego de aventura basado en texto** donde el jugador toma decisiones que afectan el desarrollo de la historia. El juego debe tener múltiples caminos y al menos **3 finales diferentes**.

---

## 🎯 Objetivos de Aprendizaje

- Aplicar estructuras if/elif/else para crear ramificaciones
- Usar match/case para procesar comandos del usuario
- Implementar validación de entrada con truthiness
- Combinar operadores lógicos para condiciones complejas

---

## 📁 Estructura del Proyecto

```
3-proyecto/
├── README.md          # Este archivo
├── starter/
│   └── main.py        # Código inicial con TODOs
└── solution/          # ⚠️ Solo para instructores
    └── main.py
```

---

## 🛠️ Requisitos Funcionales

### 1. Sistema de Decisiones

El juego debe tener:

- **Al menos 3 puntos de decisión** donde el jugador elige
- **Mínimo 3 finales diferentes** según las decisiones
- Cada decisión debe tener **al menos 2 opciones**

### 2. Procesamiento de Comandos

Implementa un procesador de comandos usando `match/case`:

```python
# Comandos obligatorios
- "1", "2", "3"... para elegir opciones
- "help" para mostrar ayuda
- "quit" para salir del juego
```

### 3. Sistema de Estado

El juego debe mantener estado:

```python
game_state: dict = {
    "player_name": "",
    "has_key": False,
    "has_sword": False,
    "current_room": "entrance",
    "health": 100,
}
```

### 4. Validación de Entrada

- Validar que las opciones elegidas sean válidas
- Manejar entradas vacías o inválidas graciosamente
- Usar truthiness para verificar estados

---

## 📝 Historia Sugerida

Puedes crear tu propia historia o usar esta como base:

> **La Cueva del Dragón**
>
> Eres un aventurero que entra a una cueva misteriosa buscando un tesoro legendario.
>
> **Decisión 1**: En la entrada hay dos caminos - izquierda (oscuro) o derecha (iluminado)
>
> **Camino Izquierdo**:
> - Encuentras una espada antigua
> - Decisión 2a: ¿Tomar la espada o seguir?
>
> **Camino Derecho**:
> - Encuentras una llave dorada
> - Decisión 2b: ¿Tomar la llave o seguir?
>
> **Final**: Llegas a la cámara del dragón
> - Con espada: Puedes luchar
> - Con llave: Puedes abrir el cofre secreto y escapar
> - Sin nada: El dragón te atrapa
> - Con ambos: Final secreto - derrotas al dragón Y obtienes el tesoro

---

## ✅ Criterios de Evaluación

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| **Funcionalidad** | 12 | |
| Sistema de decisiones | 4 | if/elif/else funcionando |
| Pattern matching | 4 | match/case implementados |
| Múltiples finales | 4 | Al menos 3 finales diferentes |
| **Calidad de Código** | 10 | |
| Type hints | 3 | Todas las funciones tipadas |
| Nombres descriptivos | 3 | Variables y funciones claras |
| Estructura modular | 4 | Código organizado en funciones |
| **Creatividad** | 8 | |
| Historia interesante | 4 | Narrativa atractiva |
| Opciones significativas | 4 | Decisiones con consecuencias |
| **Total** | **30** | |

---

## 💡 Tips de Implementación

### Estructura Recomendada

```python
def main() -> None:
    """Función principal del juego."""
    show_welcome()
    player_name = get_player_name()
    game_state = initialize_game(player_name)

    while game_state["playing"]:
        current_room = game_state["current_room"]

        match current_room:
            case "entrance":
                entrance_scene(game_state)
            case "left_path":
                left_path_scene(game_state)
            case "right_path":
                right_path_scene(game_state)
            case "dragon_chamber":
                dragon_chamber_scene(game_state)
            case "ending":
                show_ending(game_state)
                game_state["playing"] = False
```

### Función de Entrada Válida

```python
def get_valid_choice(options: list[str], prompt: str = "> ") -> str:
    """Obtiene una opción válida del usuario."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        print(f"Opción no válida. Elige: {', '.join(options)}")
```

---

## 🚀 Cómo Empezar

1. Abre `starter/main.py`
2. Lee los TODOs y completa cada función
3. Prueba el juego frecuentemente
4. Asegúrate de que todos los caminos funcionen

---

## 📚 Recursos

- [Input/Output en Python](https://docs.python.org/3/tutorial/inputoutput.html)
- [Match Statements](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)

---

## 🎮 Ejemplo de Ejecución

```
╔════════════════════════════════════════╗
║     🐉 LA CUEVA DEL DRAGÓN 🐉          ║
╚════════════════════════════════════════╝

¿Cuál es tu nombre, aventurero? > Ana

¡Bienvenida, Ana!

Te encuentras en la entrada de una cueva misteriosa.
Dos caminos se abren ante ti:

1. 🌑 Camino izquierdo (oscuro y frío)
2. 💡 Camino derecho (iluminado por antorchas)

¿Qué camino eliges? (1/2) > 1

Te adentras en la oscuridad...
[continúa la historia]
```

---

*¡Buena suerte, aventurero! 🗡️*
