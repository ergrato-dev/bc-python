# Recursos — Semana 22: Automatización del Sistema de Archivos

## Documentación oficial

- [pathlib — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html) — referencia completa
- [watchdog — Filesystem events monitoring](https://watchdog.readthedocs.io/) — Observer, handlers, patterns
- [hashlib — Secure hashes and message digests](https://docs.python.org/3/library/hashlib.html) — SHA-256, chunks
- [shutil — High-level file operations](https://docs.python.org/3/library/shutil.html) — move, copy2, rmtree
- [inotify (Linux kernel)](https://www.man7.org/linux/man-pages/man7/inotify.7.html) — eventos del filesystem en Linux

## Artículos y guías

- [Python Docs — pathlib vs os.path](https://docs.python.org/3/library/pathlib.html#correspondence-to-tools-in-the-os-module) — tabla de equivalencias
- [Real Python — Working With Files in Python](https://realpython.com/working-with-files-in-python/) — pathlib, shutil, glob
- [Python File Watcher with watchdog](https://thepythoncorner.com/posts/2019-01-13-how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/) — tutorial completo
- [Atomic file writes in Python](https://bugs.python.org/issue8604) — por qué tmp + rename es atómico
- [Naming conventions for media production](https://library.stanford.edu/projects/stanford-media-archive/guidelines) — estándares reales de producción

## Videos

- [Python pathlib Tutorial (Real Python)](https://www.youtube.com/watch?v=UcKkmwaOY8o) — walkthrough completo
- [File System Monitoring with Python watchdog](https://www.youtube.com/watch?v=L-OU1xaRlgE) — implementación práctica
- [hashlib in Python](https://www.youtube.com/watch?v=eBcBNwZQm4I) — checksums, seguridad, uso

## Herramientas del proyecto

| Herramienta | Versión | Propósito |
|-------------|---------|-----------|
| `watchdog` | ≥4.0 | Monitoreo de directorios en tiempo real |
| `pathlib` | stdlib | Operaciones de sistema de archivos tipadas |
| `hashlib` | stdlib | Checksums SHA-256 para idempotencia |
| `shutil` | stdlib | Movimiento cross-device seguro |
| `typer` | ≥0.12 | CLI del daemon |
| `rich` | ≥13 | Output formateado |

## Complementario

- [Twelve-Factor App — Processes](https://12factor.net/processes) — daemons stateless
- [Linux inotify limits](https://developer.ibm.com/articles/l-inotify/) — ajustar `fs.inotify.max_user_watches`
- [Python tempfile — NamedTemporaryFile](https://docs.python.org/3/library/tempfile.html) — escritura atómica segura
