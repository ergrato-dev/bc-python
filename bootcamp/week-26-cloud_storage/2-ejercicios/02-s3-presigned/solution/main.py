"""
Ejercicio 02: Presigned URLs y Multipart Upload — SOLUCIÓN
==========================================================
"""
from __future__ import annotations

from pathlib import Path

import boto3


BUCKET = "studio-bc-dev-sandbox"
MB = 1024 * 1024


def generate_download_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    s3 = boto3.client("s3")
    url: str = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )
    return url


def generate_upload_post(
    bucket: str, key: str, content_type: str, expires_in: int = 900
) -> dict[str, object]:
    s3 = boto3.client("s3")
    resp: dict[str, object] = s3.generate_presigned_post(
        Bucket=bucket,
        Key=key,
        Fields={"Content-Type": content_type},
        Conditions=[{"Content-Type": content_type}],
        ExpiresIn=expires_in,
    )
    return resp


def multipart_upload(local_path: Path, bucket: str, key: str, part_size_mb: int = 5) -> None:
    s3 = boto3.client("s3")
    part_size = part_size_mb * MB
    mpu = s3.create_multipart_upload(Bucket=bucket, Key=key)
    upload_id = mpu["UploadId"]
    parts: list[dict[str, object]] = []

    try:
        with local_path.open("rb") as f:
            part_number = 1
            while chunk := f.read(part_size):
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


# ── Ejercicio ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
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
