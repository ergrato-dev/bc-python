# S3 Avanzado — Multipart, Presigned URLs y Versioning

## 1. Multipart Upload

Para archivos grandes (> 100 MB), el upload multipart divide el archivo en partes y las sube en paralelo. S3 solo ensamblará el objeto final cuando todas las partes lleguen.

```python
import boto3
from pathlib import Path

MB = 1024 * 1024
PART_SIZE = 100 * MB  # 100 MB por parte

def multipart_upload(local_path: Path, bucket: str, key: str) -> None:
    s3 = boto3.client("s3")
    mpu = s3.create_multipart_upload(Bucket=bucket, Key=key)
    upload_id = mpu["UploadId"]
    parts: list[dict[str, object]] = []

    try:
        with local_path.open("rb") as f:
            part_number = 1
            while chunk := f.read(PART_SIZE):
                resp = s3.upload_part(
                    Bucket=bucket,
                    Key=key,
                    UploadId=upload_id,
                    PartNumber=part_number,
                    Body=chunk,
                )
                parts.append({"PartNumber": part_number, "ETag": resp["ETag"]})
                part_number += 1

        s3.complete_multipart_upload(
            Bucket=bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )
    except Exception:
        s3.abort_multipart_upload(Bucket=bucket, Key=key, UploadId=upload_id)
        raise
```

`abort_multipart_upload` es importante: las partes incompletas se cobran hasta que se abortan.

### Forma más simple: `TransferConfig`

```python
from boto3.s3.transfer import TransferConfig

config = TransferConfig(
    multipart_threshold=100 * MB,
    multipart_chunksize=100 * MB,
    max_concurrency=4,
)
s3.upload_file(str(path), bucket, key, Config=config)
```

`boto3` activa el multipart automáticamente cuando el archivo supera `multipart_threshold`.

---

## 2. Presigned URLs

Una presigned URL permite que cualquier usuario (sin credenciales AWS) acceda a un objeto por un tiempo limitado.

### URL de descarga (GET)

```python
def generate_download_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    s3 = boto3.client("s3")
    url: str = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )
    return url
```

### URL de subida (PUT) — para que el cliente suba directamente

```python
def generate_upload_url(
    bucket: str, key: str, content_type: str, expires_in: int = 900
) -> dict[str, object]:
    s3 = boto3.client("s3")
    resp = s3.generate_presigned_post(
        Bucket=bucket,
        Key=key,
        Fields={"Content-Type": content_type},
        Conditions=[{"Content-Type": content_type}],
        ExpiresIn=expires_in,
    )
    return resp  # {"url": "...", "fields": {...}}
```

El cliente sube con un `POST` al `url` incluyendo los `fields` como form-data.

---

## 3. Versioning

Con versioning habilitado, S3 conserva todas las versiones de un objeto en lugar de sobrescribirlo.

```python
# Habilitar versioning (una vez por bucket)
s3.put_bucket_versioning(
    Bucket=bucket,
    VersioningConfiguration={"Status": "Enabled"},
)

# Listar versiones
def list_versions(bucket: str, key: str) -> list[dict[str, object]]:
    resp = s3.list_object_versions(Bucket=bucket, Prefix=key)
    return resp.get("Versions", [])

# Descargar versión específica
def download_version(bucket: str, key: str, version_id: str, dest: Path) -> None:
    s3.download_file(
        Bucket=bucket,
        Key=key,
        Filename=str(dest),
        ExtraArgs={"VersionId": version_id},
    )

# Eliminar versión específica (soft delete sin VersionId deja un "delete marker")
def delete_version(bucket: str, key: str, version_id: str) -> None:
    s3.delete_object(Bucket=bucket, Key=key, VersionId=version_id)
```

---

## 4. Storage Classes

| Clase | Uso | Costo (relativo) | Latencia |
|-------|-----|------------------|----------|
| `STANDARD` | Acceso frecuente | Alto | ms |
| `STANDARD_IA` | Acceso infrecuente | Medio | ms |
| `INTELLIGENT_TIERING` | Patrón variable | Auto | ms |
| `GLACIER_IR` | Archivado con acceso rápido | Bajo | ms |
| `GLACIER` | Archivado profundo | Muy bajo | minutos |
| `DEEP_ARCHIVE` | Archivado máximo | Mínimo | horas |

```python
# Subir directo a Glacier Instant Retrieval
s3.upload_file(
    str(path), bucket, key,
    ExtraArgs={"StorageClass": "GLACIER_IR"},
)
```

### Lifecycle Policy (via consola o boto3)

```python
s3.put_bucket_lifecycle_configuration(
    Bucket=bucket,
    LifecycleConfiguration={
        "Rules": [
            {
                "ID": "archive-old-renders",
                "Status": "Enabled",
                "Filter": {"Prefix": "renders/"},
                "Transitions": [
                    {"Days": 30, "StorageClass": "STANDARD_IA"},
                    {"Days": 90, "StorageClass": "GLACIER"},
                ],
            }
        ]
    },
)
```

---

## Resumen

| Característica | Cuándo usarla |
|----------------|---------------|
| `multipart_upload` | Archivos > 100 MB |
| `presigned URL (GET)` | Compartir descarga sin exponer credenciales |
| `presigned POST` | Subida directa desde cliente a S3 sin pasar por tu servidor |
| `versioning` | Proteger renders de producción de sobreescritura accidental |
| `lifecycle policy` | Migrar renders viejos a Glacier automáticamente |
