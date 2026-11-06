"""Ejercicio 03 · Rich: estilos, tablas, paneles, stderr y terminal frente a tubería.

Ejecuta `uv run python main.py` después de cada paso. Algunos pasos piden ejecutarlo
también con la salida redirigida, para ver qué hace Rich cuando no hay terminal.
"""

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

console = Console()
errors = Console(stderr=True)

MEDIDAS = [("Norte", 12.5), ("Sur", 8.0), ("Oriente", 55.1), ("Sala [b]", 30.0)]


def nivel(valor: float) -> str:
    return "bajo" if valor < 10 else "alto" if valor > 50 else "medio"


console.print("Ejercicio 03 · Rich")


# ============================================
# PASO 1: Estilos con marcas entre corchetes
# ============================================
# Descomenta las siguientes líneas:
# console.print("[bold]Norte[/bold]: 12.5 µg/m³ → [green]medio[/green]")
# console.print("[bold red]Oriente: 55.1 µg/m³ → alto[/]")
# console.print("Estilo para todo el texto", style="italic cyan")


# ============================================
# PASO 2: Los corchetes de tus datos
# ============================================
# Descomenta las siguientes líneas:
# etiqueta = MEDIDAS[3][0]
# console.print(f"con marcas: {etiqueta}")
# console.print(f"con escape: {escape(etiqueta)}")
# console.print(f"sin marcas: {etiqueta}", markup=False)


# ============================================
# PASO 3: Una tabla
# ============================================
# Descomenta las siguientes líneas:
# COLORES = {"bajo": "cyan", "medio": "green", "alto": "bold red"}
# tabla = Table(title="Medidas")
# tabla.add_column("Etiqueta")
# tabla.add_column("Valor", justify="right")
# tabla.add_column("Nivel")
# for etiqueta, valor in MEDIDAS:
#     n = nivel(valor)
#     tabla.add_row(escape(etiqueta), f"{valor:.1f}", f"[{COLORES[n]}]{n}[/]")
# console.print(tabla)


# ============================================
# PASO 4: Un panel y una regla
# ============================================
# Descomenta las siguientes líneas:
# console.rule("Resumen")
# media = sum(valor for _, valor in MEDIDAS) / len(MEDIDAS)
# texto = f"registros: {len(MEDIDAS)}\nmedia: {media:.1f}"
# console.print(Panel(texto, title="Observatorio"))


# ============================================
# PASO 5: Los errores, a stderr
# ============================================
# Descomenta las siguientes líneas:
# errors.print("[bold red]error:[/] línea 7: 'Sur 9,5'")


# ============================================
# PASO 6: ¿Hay una terminal?
# ============================================
# Descomenta las siguientes líneas:
# console.print(f"terminal: {console.is_terminal} · ancho: {console.width}", markup=False)
