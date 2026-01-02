"""
Datos de Ejemplo
================
Datos de prueba para el analizador.
"""

# Productos con sus tags
SAMPLE_PRODUCTS: dict[str, set[str]] = {
    "laptop": {"electronics", "computers", "portable", "work"},
    "phone": {"electronics", "mobile", "portable", "communication"},
    "headphones": {"electronics", "audio", "portable", "entertainment"},
    "desk": {"furniture", "office", "work"},
    "chair": {"furniture", "office", "ergonomic"},
    "monitor": {"electronics", "computers", "display", "work"},
    "keyboard": {"electronics", "computers", "input", "work"},
    "tablet": {"electronics", "mobile", "portable", "entertainment"},
    "speaker": {"electronics", "audio", "entertainment"},
    "webcam": {"electronics", "video", "communication", "work"},
}

# Datos de ventas
SAMPLE_SALES: list[dict[str, str | int]] = [
    {"name": "laptop", "sales": 120, "category": "electronics"},
    {"name": "phone", "sales": 150, "category": "electronics"},
    {"name": "headphones", "sales": 80, "category": "electronics"},
    {"name": "desk", "sales": 45, "category": "furniture"},
    {"name": "chair", "sales": 60, "category": "furniture"},
    {"name": "monitor", "sales": 75, "category": "electronics"},
    {"name": "keyboard", "sales": 90, "category": "electronics"},
    {"name": "tablet", "sales": 65, "category": "electronics"},
    {"name": "speaker", "sales": 55, "category": "electronics"},
    {"name": "webcam", "sales": 40, "category": "electronics"},
]

# Usuarios de ejemplo
SAMPLE_USERS: dict[str, dict[str, set[str] | str]] = {
    "alice": {
        "roles": {"admin", "editor"},
        "interests": {"python", "data-science", "ai"},
        "plan": "premium",
    },
    "bob": {
        "roles": {"editor", "viewer"},
        "interests": {"javascript", "web", "react"},
        "plan": "premium",
    },
    "carol": {
        "roles": {"viewer"},
        "interests": {"python", "web", "django"},
        "plan": "basic",
    },
    "david": {
        "roles": {"admin", "editor", "viewer"},
        "interests": {"devops", "cloud", "security"},
        "plan": "enterprise",
    },
    "eve": {
        "roles": {"viewer"},
        "interests": {"design", "ux", "figma"},
        "plan": "basic",
    },
}
