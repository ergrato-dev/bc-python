"""
Ejercicio 01: boto3 y S3 Básico — SOLUCIÓN
==========================================
"""
from __future__ import annotations

import mimetypes
from pathlib import Path

import boto3
from botocore.exceptions import ClientError, NoCredentialsError


BUCKET = "studio-bc-dev-sandbox"
REGION = "us-east-1"

s3 = boto3.client("s3", region_name=REGION)


def create_bucket_if_not_exists(bucket: str, region: str = REGION) -> None:
    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket)
        else:
            s3.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code not in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
            raise


def upload_file(local_path: Path, bucket: str, key: str) -> None:
    mime_type, _ = mimetypes.guess_type(str(local_path))
    s3.upload_file(
        Filename=str(local_path),
        Bucket=bucket,
        Key=key,
        ExtraArgs={
            "ContentType": mime_type or "application/octet-stream",
            "Metadata": {"proyecto": "ejercicio-01"},
        },
    )


def download_file(bucket: str, key: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(Bucket=bucket, Key=key, Filename=str(dest))


def list_objects(bucket: str, prefix: str = "") -> list[str]:
    paginator = s3.get_paginator("list_objects_v2")
    keys: list[str] = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.append(obj["Key"])
    return keys


def get_object_size(bucket: str, key: str) -> int:
    resp = s3.head_object(Bucket=bucket, Key=key)
    return int(resp["ContentLength"])


# ── Ejercicio ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_file = Path("test_upload.txt")
    test_file.write_text("Hola desde Studio BC — ejercicio 01")

    print("1. Creando bucket...")
    create_bucket_if_not_exists(BUCKET)

    print("2. Subiendo archivo...")
    upload_file(test_file, BUCKET, "ejercicios/01/test_upload.txt")

    print("3. Listando objetos en 'ejercicios/'...")
    keys = list_objects(BUCKET, prefix="ejercicios/")
    for k in keys:
        print(f"   {k}")

    print("4. Descargando archivo...")
    dest = Path("downloaded_test.txt")
    download_file(BUCKET, "ejercicios/01/test_upload.txt", dest)
    assert dest.read_text() == test_file.read_text(), "El contenido descargado no coincide"
    print("   Contenido verificado OK")

    print("5. Tamaño del objeto:", get_object_size(BUCKET, "ejercicios/01/test_upload.txt"), "bytes")

    test_file.unlink(missing_ok=True)
    dest.unlink(missing_ok=True)
    print("OK — Ejercicio 01 completado")
