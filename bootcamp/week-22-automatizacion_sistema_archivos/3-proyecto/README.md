# Proyecto — studio-ingest-daemon

## Descripción

Daemon CLI que monitorea una carpeta `drop/` y organiza automáticamente
los archivos entrantes aplicando la convención de nomenclatura Studio BC.

## Comandos

```bash
# Instalar dependencias
pip install -e .

# Correr el daemon (bloquea hasta Ctrl+C)
python -m studio_ingest watch

# Organizar archivos existentes en drop/ (sin daemon)
python -m studio_ingest organize

# Mostrar estadísticas del registro de procesados
python -m studio_ingest stats
```

## Estructura de destino

```
organized/
├── video/
│   └── 2024-03/
│       └── canal9_spot-verano_raw_20240315_v001.mp4
├── audio/
│   └── 2024-03/
│       └── canal9_spot-verano_raw_20240315_v001.wav
├── image/
│   └── 2024-03/
│       └── canal9_spot-verano_raw_20240315_v001.jpg
└── doc/
    └── 2024-03/
        └── canal9_brief_doc_20240315_v001.pdf
```

## Requisitos

- El daemon debe sobrevivir errores en archivos individuales (log + continuar)
- Debe ser idempotente: reiniciar no reprocesa archivos ya organizados
- Debe manejar `KeyboardInterrupt` limpiamente (stop + join del Observer)
- mypy --strict debe pasar sin errores en `src/`

## Archivos a completar

| Archivo | TODOs |
|---------|-------|
| `src/classifier.py` | `classify()`, `build_dest_dir()` |
| `src/organizer.py` | `safe_move()`, `FileOrganizer.organize()` |
| `src/registry.py` | `sha256()`, `load_registry()`, `save_registry()`, `is_processed()` |
| `src/handler.py` | `IngestHandler.on_created()` completo |
| `src/__main__.py` | comandos `watch`, `organize`, `stats` |
