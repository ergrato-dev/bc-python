"""S3AssetStore — adapter que sube assets a Amazon S3."""
from __future__ import annotations

import mimetypes
from pathlib import Path


class S3AssetStore:
    def __init__(self, bucket: str, region: str = "us-east-1", dry_run: bool = True) -> None:
        self._bucket = bucket
        self._region = region
        self._dry_run = dry_run

    def upload(self, asset_path: str, asset_id: str, media_type: str) -> str:
        """
        Sube el archivo a S3.
        Clave: f"{media_type}/{asset_id}/{Path(asset_path).name}"
        URL: f"https://{self._bucket}.s3.{self._region}.amazonaws.com/{key}"

        TODO si dry_run=True: imprimir la key y devolver la URL ficticia
        TODO si dry_run=False:
            import boto3
            s3 = boto3.client("s3", region_name=self._region)
            mime_type, _ = mimetypes.guess_type(asset_path)
            s3.upload_file(
                Filename=asset_path,
                Bucket=self._bucket,
                Key=key,
                ExtraArgs={"ContentType": mime_type or "application/octet-stream"},
            )
            return url

        Referencia: semana 26 — S3Uploader.upload_file()
                    semana 30 — CloudStage._upload()
        """
        raise NotImplementedError
