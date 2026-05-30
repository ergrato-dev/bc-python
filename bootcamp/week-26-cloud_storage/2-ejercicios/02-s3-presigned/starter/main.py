"""
Ejercicio 02: Presigned URLs y Multipart Upload
================================================
Implementa presigned URLs para descarga y upload multipart para archivos grandes.
"""
from __future__ import annotations

import boto3
from pathlib import Path


BUCKET = "studio-bc-dev-sandbox"
MB = 1024 * 1024


def generate_download_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    """Genera una presigned URL para descarga GET, válida por expires_in segundos."""
    # TODO: generate_presigned_url("get_object", Params={...}, ExpiresIn=expires_in)
    raise NotImplementedError


def generate_upload_post(
    bucket: str, key: str, content_type: str, expires_in: int = 900
) -> dict[str, object]:
    """Genera una presigned POST URL para que el cliente suba directamente a S3."""
    # TODO: generate_presigned_post con Fields y Conditions para content_type
    raise NotImplementedError


def multipart_upload(local_path: Path, bucket: str, key: str, part_size_mb: int = 5) -> None:
    """
    Sube un archivo grande usando multipart upload.
    part_size_mb: tamaño de cada parte en MB (mínimo 5 MB en S3 real).
    Si falla alguna parte, abortar el upload con abort_multipart_upload.
    """
    # TODO: create_multipart_upload → loop upload_part → complete_multipart_upload
    # TODO: en except: abort_multipart_upload para limpiar partes huérfanas
    raise NotImplementedError


# ── Ejercicio ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Crear archivo de prueba de ~12 MB
    test_file = Path("test_large.bin")
    test_file.write_bytes(b"X" * (12 * MB))

    s3 = boto3.client("s3")

    print("1. Subiendo archivo grande con multipart...")
    multipart_upload(test_file, BUCKET, "ejercicios/02/large_file.bin", part_size_mb=5)
    print("   Upload multipart OK")

    print("2. Generando presigned URL de descarga (1h)...")
    url = generate_download_url(BUCKET, "ejercicios/02/large_file.bin")
    print(f"   URL: {url[:80]}...")

    print("3. Generando presigned POST para subida directa (15min)...")
    post_data = generate_upload_post(BUCKET, "ejercicios/02/client_upload.mp4", "video/mp4")
    print(f"   POST URL: {str(post_data.get('url', ''))[:60]}...")
    print(f"   Fields: {list(post_data.get('fields', {}).keys())}")

    test_file.unlink(missing_ok=True)
    print("OK — Ejercicio 02 completado")
