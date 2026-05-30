"""
Ejercicio 01: boto3 y S3 Básico
================================
Implementa las funciones de upload, download y listado de objetos en S3.

Ejecutar (con credenciales AWS configuradas):
    python main.py

Para tests sin credenciales reales, usar localstack:
    docker run -p 4566:4566 localstack/localstack
    export AWS_ENDPOINT_URL=http://localhost:4566
"""
from __future__ import annotations

import boto3
from pathlib import Path
from botocore.exceptions import ClientError, NoCredentialsError


BUCKET = "studio-bc-dev-sandbox"
REGION = "us-east-1"


def create_bucket_if_not_exists(bucket: str, region: str = REGION) -> None:
    """Crea el bucket si no existe. En us-east-1 no se pasa LocationConstraint."""
    # TODO: usar s3.create_bucket() con LocationConstraint si region != "us-east-1"
    # Ignorar error "BucketAlreadyOwnedByYou"
    raise NotImplementedError


def upload_file(local_path: Path, bucket: str, key: str) -> None:
    """Sube un archivo a S3 con ContentType y Metadata apropiados."""
    # TODO: detectar Content-Type con mimetypes.guess_type
    # TODO: agregar Metadata={"proyecto": "ejercicio-01"}
    raise NotImplementedError


def download_file(bucket: str, key: str, dest: Path) -> None:
    """Descarga un objeto S3 a una ruta local. Crea los directorios necesarios."""
    # TODO: dest.parent.mkdir(parents=True, exist_ok=True)
    raise NotImplementedError


def list_objects(bucket: str, prefix: str = "") -> list[str]:
    """Lista todas las keys con el prefix dado, usando paginación."""
    # TODO: usar get_paginator("list_objects_v2")
    raise NotImplementedError


def get_object_size(bucket: str, key: str) -> int:
    """Devuelve el tamaño en bytes del objeto. Usa head_object."""
    # TODO: head_object(Bucket, Key) → ContentLength
    raise NotImplementedError


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

    # Limpieza
    test_file.unlink(missing_ok=True)
    dest.unlink(missing_ok=True)
    print("OK — Ejercicio 01 completado")
