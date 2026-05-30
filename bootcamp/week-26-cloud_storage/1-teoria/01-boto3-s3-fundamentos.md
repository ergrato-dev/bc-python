# boto3 y Amazon S3 — Fundamentos

## Conceptos clave

Amazon S3 (Simple Storage Service) organiza datos en dos niveles:

- **Bucket**: contenedor global con nombre único. Equivalente a un disco.
- **Object**: archivo almacenado con una _key_ (ruta). No existen carpetas reales — la key `proyecto/video/clip.mp4` es una sola cadena.

---

## 1. Configurar credenciales

### Opción A — variables de entorno (recomendado para desarrollo)

```bash
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
```

### Opción B — archivo `~/.aws/credentials`

```ini
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = ...
region = us-east-1
```

### Opción C — parámetros explícitos (evitar en producción)

```python
import boto3

s3 = boto3.client(
    "s3",
    aws_access_key_id="AKIA...",
    aws_secret_access_key="...",
    region_name="us-east-1",
)
```

La forma recomendada en producción es **IAM Role** (EC2/Lambda) o **Environment Variables** (Docker/CI).

---

## 2. Crear cliente vs recurso

```python
import boto3

# Cliente: API de bajo nivel, más control
s3_client = boto3.client("s3")

# Recurso: API orientada a objetos (más legible)
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket("mi-bucket")
```

---

## 3. Operaciones básicas

### Upload

```python
from pathlib import Path
import boto3

s3 = boto3.client("s3")

def upload_file(local_path: Path, bucket: str, key: str) -> None:
    s3.upload_file(
        Filename=str(local_path),
        Bucket=bucket,
        Key=key,
        ExtraArgs={
            "ContentType": "video/mp4",
            "Metadata": {
                "proyecto": "spot-verano",
                "version": "v2",
            },
        },
    )
```

### Download

```python
def download_file(bucket: str, key: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(Bucket=bucket, Key=key, Filename=str(dest))
```

### Listar objetos

```python
def list_objects(bucket: str, prefix: str = "") -> list[str]:
    paginator = s3.get_paginator("list_objects_v2")
    keys: list[str] = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.append(obj["Key"])
    return keys
```

`get_paginator` es esencial — sin él, `list_objects_v2` solo devuelve hasta 1000 objetos.

---

## 4. Metadata y ETag

Cada objeto S3 tiene:

| Campo | Descripción |
|-------|-------------|
| `Key` | Ruta del objeto |
| `ETag` | Hash MD5 del contenido (entre comillas dobles) |
| `Size` | Tamaño en bytes |
| `LastModified` | Timestamp de última modificación |
| `ContentType` | MIME type |

```python
def get_object_metadata(bucket: str, key: str) -> dict[str, object]:
    resp = s3.head_object(Bucket=bucket, Key=key)
    return {
        "etag": resp["ETag"].strip('"'),
        "size": resp["ContentLength"],
        "last_modified": resp["LastModified"].isoformat(),
        "content_type": resp.get("ContentType", ""),
        "metadata": resp.get("Metadata", {}),
    }
```

**Importante:** ETag es MD5 del archivo completo solo si fue subido como single-part. Con multipart upload, ETag es `{md5_de_partes}-{n_partes}`.

---

## 5. Manejo de errores

```python
from botocore.exceptions import ClientError, NoCredentialsError

def safe_upload(local_path: Path, bucket: str, key: str) -> bool:
    try:
        upload_file(local_path, bucket, key)
        return True
    except FileNotFoundError:
        print(f"Archivo no encontrado: {local_path}")
    except NoCredentialsError:
        print("Credenciales AWS no configuradas")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        print(f"Error S3 [{code}]: {e.response['Error']['Message']}")
    return False
```

---

## Resumen

| Operación | Método cliente |
|-----------|----------------|
| Subir archivo | `upload_file(Filename, Bucket, Key)` |
| Descargar archivo | `download_file(Bucket, Key, Filename)` |
| Listar objetos | `get_paginator("list_objects_v2")` |
| Cabecera de objeto | `head_object(Bucket, Key)` |
| Eliminar objeto | `delete_object(Bucket, Key)` |
