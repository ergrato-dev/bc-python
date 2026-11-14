"""Genera notas.csv: notas de texto libre "etiqueta;tipo;texto" para clasificarlas.

Uso: uv run python scripts/generar_notas.py 300 notas.csv

La semilla es fija: con el mismo número de notas sale siempre el mismo archivo. Cada nota
mezcla piezas al azar, y algunas llevan una pista de otro tipo ("sin avería", "tras la
limpieza") para que acertar no sea solo buscar una palabra.
Cambia LABELS, PIECES y HINTS por las etiquetas, los tipos y las frases de tu dominio.
"""

import csv
import random
import sys
from pathlib import Path

LABELS = ["Norte", "Sur", "Centro", "Este", "Oeste"]
# Por tipo: cómo empieza la nota, qué se hizo y cómo quedó.
PIECES = {
    "averia": (
        ["El sensor de", "La estación", "El equipo de", "El analizador de"],
        [
            "no responde desde la madrugada",
            "dejó de enviar lecturas",
            "se apagó por un corte de energía",
            "tiene la placa quemada",
            "marca cero todo el día",
            "perdió la conexión con el servidor",
        ],
        ["hay que cambiar la pieza", "queda fuera de servicio", "se pidió un repuesto"],
    ),
    "limpieza": (
        ["En", "En la estación", "Hoy en", "Durante la ronda en"],
        [
            "se limpió el filtro lleno de polvo",
            "se retiraron hojas y telarañas de la toma de aire",
            "se lavó la carcasa del equipo",
            "se cambió el filtro sucio",
            "se quitó el polvo acumulado en la entrada",
            "se despejó la rejilla tapada",
        ],
        ["queda limpio", "lecturas normales tras la limpieza", "próxima visita en un mes"],
    ),
    "calibracion": (
        ["El sensor de", "La estación", "El equipo de", "El analizador de"],
        [
            "marcaba valores altos y se ajustó con el patrón",
            "se recalibró con gas de referencia",
            "tenía deriva y se corrigió el cero",
            "se comparó con el equipo de referencia",
            "se ajustó la ganancia del sensor",
            "mostraba un desfase de cinco unidades",
        ],
        ["queda calibrado", "error dentro de tolerancia", "se anotó el nuevo factor"],
    ),
}
# Frases que nombran otro tipo sin serlo: la nota sigue siendo de su tipo.
HINTS = {
    "averia": [
        "se limpió el filtro pero sigue igual",
        "no se pudo calibrar",
        "la limpieza no lo arregló",
        "se intentó ajustar el cero sin éxito",
    ],
    "limpieza": [
        "sin avería",
        "no hizo falta calibrar",
        "el sensor responde bien",
        "los valores altos eran por el polvo",
    ],
    "calibracion": [
        "tras la limpieza",
        "sin avería a la vista",
        "el filtro estaba limpio",
        "no responde igual que antes del ajuste",
    ],
}
# Notas que no dicen qué se hizo: el tipo quedó en otra columna, y ningún modelo lo adivina.
VAGUE = [
    "Visita a {label}, se revisó el equipo.",
    "{label}: revisión de rutina, detalles en la planilla.",
    "Se pasó por {label}, ver informe del técnico.",
]


def note(rng: random.Random, kind: str, label: str) -> str:
    """Una nota del tipo kind: inicio, lo que se hizo, a veces una pista, y el cierre."""
    if rng.random() < 0.15:
        return rng.choice(VAGUE).format(label=label)
    starts, actions, ends = PIECES[kind]
    parts = [f"{rng.choice(starts)} {label} {rng.choice(actions)}"]
    if rng.random() < 0.6:
        parts.append(rng.choice(HINTS[kind]))
    parts.append(rng.choice(ends))
    return ", ".join(parts) + "."


def main() -> None:
    count, path = int(sys.argv[1]), Path(sys.argv[2])
    rng = random.Random(36)
    kinds = list(PIECES)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        writer.writerow(["etiqueta", "tipo", "texto"])
        for index in range(count):
            # Por turnos: los tipos salen igual de veces.
            kind, label = kinds[index % len(kinds)], rng.choice(LABELS)
            writer.writerow([label, kind, note(rng, kind, label)])


if __name__ == "__main__":
    main()
