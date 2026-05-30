# Estrategia de Storage — Hot/Cold, Naming y Lifecycle

## 1. Hot vs Cold Storage

| Nivel | Acceso | Latencia | Costo/GB | Caso de uso |
|-------|--------|----------|----------|-------------|
| **Hot** (Standard) | Frecuente | ms | Alto | Trabajo activo, proyectos en curso |
| **Warm** (Standard-IA) | Mensual | ms | Medio | Entregables cerrados < 6 meses |
| **Cold** (Glacier IR) | Trimestral | ms | Bajo | Archivos de proyectos viejos |
| **Archive** (Deep Archive) | Anual | horas | Mínimo | Respaldo legal, masters de larga data |

### Regla práctica para un estudio audiovisual

```
Proyecto activo      → S3 Standard
Proyecto entregado   → S3 Standard-IA (30 días tras entrega)
Proyecto archivado   → Glacier IR (90 días)
Backup legal         → Deep Archive (1 año)
```

---

## 2. Naming de Buckets y Keys

### Naming de buckets

Los nombres de bucket S3 deben ser globalmente únicos (en todo AWS), en minúsculas, sin underscores:

```
studio-bc-{env}-{propósito}

studio-bc-prod-assets
studio-bc-prod-renders
studio-bc-dev-sandbox
```

### Estructura de keys (pseudo-carpetas)

```
{cliente}/{proyecto}/{tipo}/{fecha_ISO}/archivo.ext

canal9/spot-verano-2024/render/2024-11-15/spot_verano_v3_final.mp4
canal9/spot-verano-2024/source/2024-10-01/entrevista_dia1_raw.mp4
canal9/spot-verano-2024/export/2024-11-15/spot_verano_web.mp4
```

**Ventajas de esta estructura:**
- Prefix filtering en `list_objects_v2` por cliente o proyecto
- Lifecycle policies aplicadas a prefijos específicos
- Costos desglosados por cliente con S3 Storage Lens

### Naming de carpetas en Drive

```
Studio BC/
├── {cliente}/
│   ├── {proyecto} — {año}/
│   │   ├── Entregables/     → compartido con cliente (reader)
│   │   ├── Trabajo/         → solo interno (writer)
│   │   └── Contratos/       → solo dirección
```

---

## 3. Lifecycle Policies en Código

```python
import boto3


def apply_studio_lifecycle(bucket: str) -> None:
    s3 = boto3.client("s3")
    s3.put_bucket_lifecycle_configuration(
        Bucket=bucket,
        LifecycleConfiguration={
            "Rules": [
                {
                    "ID": "renders-to-ia",
                    "Status": "Enabled",
                    "Filter": {"Prefix": "renders/"},
                    "Transitions": [
                        {"Days": 30, "StorageClass": "STANDARD_IA"},
                        {"Days": 180, "StorageClass": "GLACIER_IR"},
                    ],
                },
                {
                    "ID": "source-to-glacier",
                    "Status": "Enabled",
                    "Filter": {"Prefix": "source/"},
                    "Transitions": [
                        {"Days": 90, "StorageClass": "GLACIER_IR"},
                        {"Days": 365, "StorageClass": "DEEP_ARCHIVE"},
                    ],
                },
                {
                    "ID": "delete-incomplete-multipart",
                    "Status": "Enabled",
                    "Filter": {"Prefix": ""},
                    "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7},
                },
            ]
        },
    )
```

La regla `delete-incomplete-multipart` es importante: partes huérfanas de uploads fallidos se cobran.

---

## 4. Estimación de Costos

```python
def estimate_monthly_cost(
    size_gb: float,
    storage_class: str = "STANDARD",
    requests: int = 1000,
) -> float:
    PRICES: dict[str, float] = {
        "STANDARD": 0.023,
        "STANDARD_IA": 0.0125,
        "GLACIER_IR": 0.004,
        "GLACIER": 0.0036,
        "DEEP_ARCHIVE": 0.00099,
    }
    RETRIEVAL: dict[str, float] = {
        "STANDARD": 0.0,
        "STANDARD_IA": 0.01,
        "GLACIER_IR": 0.03,
        "GLACIER": 0.01,
        "DEEP_ARCHIVE": 0.02,
    }
    storage_cost = size_gb * PRICES.get(storage_class, 0.023)
    retrieval_cost = size_gb * RETRIEVAL.get(storage_class, 0.0)
    put_cost = (requests / 1000) * 0.005
    return round(storage_cost + retrieval_cost + put_cost, 4)
```

---

## 5. Checklist de Seguridad

```
✅ Block Public Access activado en todos los buckets de producción
✅ Server-Side Encryption habilitada (SSE-S3 o SSE-KMS)
✅ Bucket Versioning en buckets de producción
✅ MFA Delete para proteger versiones
✅ Access Logging activado
✅ Lifecycle policy para incomplete multipart (7 días)
✅ IAM roles con least privilege — no access keys en código
```

---

## Resumen

| Decisión | Regla práctica |
|----------|----------------|
| Cuándo usar S3 vs Drive | S3 = masters/backups técnicos · Drive = colaboración con clientes |
| Naming de keys | `{cliente}/{proyecto}/{tipo}/{fecha}/archivo` |
| Cuándo mover a IA | 30 días sin acceso |
| Cuándo mover a Glacier | 90–180 días sin acceso |
| Presigned vs público | Siempre presigned para assets privados — nunca bucket público |
