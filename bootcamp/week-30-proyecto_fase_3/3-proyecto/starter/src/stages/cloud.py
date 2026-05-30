"""
CloudStage — sube los outputs a Amazon S3.

Requiere:
    pip install boto3
    AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY en entorno o .env
"""
from __future__ import annotations

import mimetypes
from datetime import datetime, timezone
from pathlib import Path

from .base import Stage, StageResult


class CloudStage:
    name = "cloud"

    def __init__(self, bucket: str, project: str, region: str = "us-east-1", dry_run: bool = True) -> None:
        self._bucket = bucket
        self._project = project
        self._region = region
        self._dry_run = dry_run

    def process(self, data: dict[str, object]) -> StageResult:
        date_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        uploaded: dict[str, str] = {}

        # Subir todos los outputs generados por TranscodeStage
        for key_suffix in ("web_path", "proxy_path", "thumb_path"):
            raw_path = data.get(key_suffix)
            if not raw_path:
                continue
            local_path = Path(str(raw_path))
            if not local_path.exists():
                continue

            media_type = str(data.get("media_type", "other"))
            file_type = key_suffix.split("_")[0]  # web | proxy | thumb
            s3_key = f"{self._project}/{media_type}/{file_type}/{date_prefix}/{local_path.name}"

            try:
                url = self._upload(local_path, s3_key)
                uploaded[f"s3_{file_type}_url"] = url
            except Exception as e:
                return StageResult(success=False, data=data, error=f"S3 upload error: {e}")

        return StageResult(success=True, data={**data, **uploaded, "s3_uploaded": True})

    def _upload(self, local_path: Path, s3_key: str) -> str:
        """
        Sube `local_path` al bucket S3 con la key `s3_key`.
        Devuelve la URL pública del objeto: https://{bucket}.s3.{region}.amazonaws.com/{key}

        TODO si dry_run=True: solo imprimir la key y devolver una URL ficticia
        TODO si dry_run=False:
            import boto3
            from botocore.exceptions import ClientError, NoCredentialsError
            s3 = boto3.client("s3", region_name=self._region)
            mime_type, _ = mimetypes.guess_type(str(local_path))
            s3.upload_file(
                Filename=str(local_path),
                Bucket=self._bucket,
                Key=s3_key,
                ExtraArgs={"ContentType": mime_type or "application/octet-stream"},
            )
            return f"https://{self._bucket}.s3.{self._region}.amazonaws.com/{s3_key}"

        Referencia: semana 26 — S3Uploader.upload_file()
        """
        raise NotImplementedError
