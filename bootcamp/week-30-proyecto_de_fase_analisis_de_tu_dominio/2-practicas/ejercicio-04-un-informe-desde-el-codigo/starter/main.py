"""Ejercicio 04 · Un informe desde el código: Markdown con la biblioteca estándar.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import difflib
import hashlib
from datetime import datetime
from pathlib import Path

print("Ejercicio 04 · Un informe desde el código")

# salida/ no va a Git: el ejercicio escribe ahí sus informes en cada ejecución.
OUT = Path("salida")
OUT.mkdir(exist_ok=True)

# Los hallazgos ya calculados: cada zona frente a Centro, con su intervalo y su p corregido.
FINDINGS = [
    {"zona": "Norte", "diferencia": 0.16, "low": -2.47, "high": 2.79, "p": 0.903},
    {"zona": "Sur", "diferencia": 6.82, "low": 4.15, "high": 9.49, "p": 0.0000312},
    {"zona": "Oeste", "diferencia": 3.89, "low": 1.07, "high": 6.71, "p": 0.0142},
]


def cell(text: str) -> str:
    """Un texto dentro de una tabla de Markdown: una barra la partiría en dos columnas."""
    return text.replace("|", "\\|")


def table(findings: list[dict[str, object]]) -> list[str]:
    lines = ["| Zona | Diferencia | IC 95 % | p corregido |", "|---|---|---|---|"]
    for row in findings:
        lines.append(
            f"| {cell(str(row['zona']))} | {row['diferencia']:.2f}"
            f" | [{row['low']:.2f}, {row['high']:.2f}] | {row['p']:.3g} |"
        )
    return lines


def report(findings: list[dict[str, object]]) -> str:
    real = sum(float(str(row["p"])) < 0.05 for row in findings)
    lines = [
        "# Hallazgos: cada zona frente a Centro",
        "",
        f"Difieren {real} de {len(findings)} zonas.",
        "",
        *table(findings),
    ]
    return "\n".join(lines) + "\n"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


# ============================================
# PASO 1: Una tabla con join
# ============================================
# Descomenta las siguientes líneas:
# print("\n".join(table(FINDINGS)))


# ============================================
# PASO 2: Una etiqueta con una barra
# ============================================
# Descomenta las siguientes líneas:
# broken = "| Norte|Este | 1.00 | [0.10, 1.90] | 0.04 |"
# print(f"sin escapar: {broken.count('|') - broken.count(chr(92) + '|') - 1} columnas")
# fixed = table([{"zona": "Norte|Este", "diferencia": 1.0, "low": 0.1, "high": 1.9, "p": 0.04}])[2]
# print(fixed)
# print(f"escapada:    {fixed.count('|') - fixed.count(chr(92) + '|') - 1} columnas")


# ============================================
# PASO 3: Números con formato fijo
# ============================================
# Descomenta las siguientes líneas:
# value = 0.1 + 0.2
# print(f"sin formato: {value} · :.2f: {value:.2f} · :.3g de 0.0000312: {0.0000312:.3g}")


# ============================================
# PASO 4: Los mismos datos, los mismos bytes
# ============================================
# Descomenta las siguientes líneas:
# for name in ("a.md", "b.md"):
#     (OUT / name).write_text(report(FINDINGS), encoding="utf-8")
# print(f"dos veces: {sha(OUT / 'a.md')} {sha(OUT / 'b.md')}")
# for name in ("a.md", "b.md"):
#     dated = report(FINDINGS) + f"\nGenerado el {datetime.now():%Y-%m-%d %H:%M:%S.%f}\n"
#     (OUT / name).write_text(dated, encoding="utf-8")
# print(f"con la hora: {sha(OUT / 'a.md')} {sha(OUT / 'b.md')}")


# ============================================
# PASO 5: ¿El informe está al día?
# ============================================
# Descomenta las siguientes líneas:
# stored = OUT / "hallazgos.md"
# stored.write_text(report(FINDINGS), encoding="utf-8")
# print(f"al día: {stored.read_text(encoding='utf-8') == report(FINDINGS)}")
# FINDINGS[2]["p"] = 0.0712
# fresh = report(FINDINGS)
# print(f"al día tras cambiar un p: {stored.read_text(encoding='utf-8') == fresh}")
# old = stored.read_text(encoding="utf-8").splitlines()
# print("\n".join(difflib.unified_diff(old, fresh.splitlines(), "guardado", "nuevo", lineterm="")))
