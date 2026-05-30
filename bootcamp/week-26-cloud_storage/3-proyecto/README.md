# Proyecto Semana 26 — studio-cloud-backup

## Objetivo

Construir un sistema de backup automático para Studio BC que:

1. Sube los assets de `output/` a Amazon S3 con estructura `{cliente}/{proyecto}/{tipo}/{fecha}/`
2. Sube los entregables a Google Drive en una carpeta compartida con el cliente (permisos de lectura)
3. Es incremental: lee `.sync_state.json` al iniciar y omite archivos sin cambios
4. Funciona como CLI con comandos `backup`, `sync` y `status`

---

## Estructura

```
starter/
├── pyproject.toml
├── credentials.json        # Service Account Google (NO commitear)
├── src/
│   ├── __init__.py
│   ├── config.py           # BackupConfig con pydantic-settings
│   ├── s3_uploader.py      # S3Uploader: upload_file, sync_to_s3
│   ├── drive_uploader.py   # DriveUploader: get_or_create_folder, upload_file
│   ├── sync_engine.py      # SyncEngine: full_backup, incremental_backup
│   └── __main__.py         # Typer CLI: backup, sync, status
└── tests/
    ├── __init__.py
    ├── test_sync_engine.py
    └── test_s3_uploader.py
```

---

## Comandos CLI

```bash
# Backup completo (fuerza re-subida de todo)
python -m src backup --project canal9/spot-verano --client-email prod@canal9.com --force

# Sync incremental (solo cambios)
python -m src sync --project canal9/spot-verano

# Ver estado del último sync
python -m src status
```

---

## Configuración

Variables de entorno (o `.env`):

```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET=studio-bc-prod-assets
GOOGLE_CREDENTIALS_PATH=credentials.json
DRIVE_ROOT_FOLDER=Studio BC
```

---

## Criterios de Aprobación (ver rúbrica)

- [ ] S3: estructura `{cliente}/{proyecto}/{tipo}/{fecha}/`
- [ ] Drive: carpeta de entregables compartida con cliente
- [ ] Sync incremental con `.sync_state.json`
- [ ] `mypy --strict` sin errores
