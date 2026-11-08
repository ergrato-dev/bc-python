"""Ejercicio 04 · Una imagen Docker segura.

Una sonda: no calcula nada, mira el contenedor en el que corre. Quién es, qué
herramientas encuentra, qué paquetes hay instalados, dónde puede escribir y qué
privilegios tiene. Ejecútala en cada imagen del Dockerfile y compara.
"""

import os
import shutil
import sys
from importlib.util import find_spec
from pathlib import Path


def user() -> str:
    uid = os.getuid()
    try:
        import pwd

        return f"{pwd.getpwuid(uid).pw_name} (uid {uid})"
    except KeyError:
        return f"sin nombre (uid {uid})"


def writable(folder: str) -> str:
    try:
        probe = Path(folder) / ".probe"
        probe.write_text("x")
        probe.unlink()
    except OSError as problem:
        return f"no ({problem.strerror})"
    return "sí"


def status(field: str) -> str:
    # /proc/self/status: lo que el núcleo sabe de este proceso.
    for line in Path("/proc/self/status").read_text().splitlines():
        if line.startswith(field + ":"):
            return line.split(":", 1)[1].strip()
    return "?"


print("Ejercicio 04 · Una imagen Docker segura")
print(f"{'usuario':<20} {user()}")
print(f"{'python':<20} {sys.version.split()[0]}")
for tool in ("uv", "pip", "gcc", "git"):
    print(f"{tool:<20} {'sí' if shutil.which(tool) else 'no'}")
for package in ("rich", "pytest"):
    print(f"{package + ' instalado':<20} {'sí' if find_spec(package) else 'no'}")
for folder in ("/app", "/tmp"):
    print(f"{'escribir en ' + folder:<20} {writable(folder)}")
print(f"{'capacidades':<20} {status('CapEff')}")
print(f"{'NoNewPrivs':<20} {status('NoNewPrivs')}")
