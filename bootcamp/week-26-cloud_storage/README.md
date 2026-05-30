# Semana 26: Cloud Storage y Assets

> **Fase 3 — Automatización y Pipelines de Media** · _Mid-level → Senior_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Subir, descargar y listar objetos en Amazon S3 con `boto3`
- Generar presigned URLs y gestionar uploads multipart para archivos grandes
- Autenticarte en Google Drive API con Service Account y gestionar carpetas y archivos
- Diseñar una estrategia de storage: hot/cold, naming de buckets, lifecycle policies
- Implementar sincronización incremental con detección de cambios por checksum (ETag / SHA-256)

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [boto3 y S3 — Fundamentos](1-teoria/01-boto3-s3-fundamentos.md) | Buckets, objetos, upload/download, credenciales |
| 02 | [S3 Avanzado](1-teoria/02-s3-avanzado.md) | Multipart, presigned URLs, versioning, storage classes |
| 03 | [Google Drive API](1-teoria/03-google-drive-api.md) | OAuth2/Service Account, carpetas, permisos, upload |
| 04 | [Estrategia de Storage](1-teoria/04-estrategia-storage.md) | Hot/cold, bucket naming, lifecycle policies, costos |
| 05 | [Sincronización y Checksums](1-teoria/05-sincronizacion-checksums.md) | Sync bidireccional, ETag vs SHA-256, registro de estado |

---

## Estructura de la Semana

```
week-26-cloud_storage/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-s3-basico/
│   ├── 02-s3-presigned/
│   ├── 03-drive-upload/
│   └── 04-sync-incremental/
├── 3-proyecto/
│   ├── README.md           # studio-cloud-backup
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: boto3 + S3 avanzado | 1.5h |
| 2 | Teoría: Drive + estrategia + sync | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Stack de la Semana

| Librería | Rol |
|----------|-----|
| `boto3` | Cliente oficial AWS para S3 y otros servicios |
| `google-api-python-client` | Cliente REST de Google APIs (Drive, Sheets, etc.) |
| `google-auth` | Autenticación OAuth2 y Service Account para Google APIs |
| `hashlib` | SHA-256 para checksums locales (idempotencia) |
| `pathlib` | Traversal de árbol local para sincronización |

---

## Navegación

← [Semana 25 — Procesamiento de Video con FFmpeg](../week-25-procesamiento_video_ffmpeg/README.md) · [Semana 27 — Arquitectura de Pipelines](../week-27-arquitectura_pipelines/README.md) →
