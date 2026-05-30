"""
Tests de las etapas del pipeline — studio-production-pipeline.

TODO: Implementar los tests marcados con NotImplementedError.
Los fixtures y la estructura están listos; solo faltan las assertions.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.stages.ingest import IngestStage
from src.stages.validate import ValidateStage
from src.stages.transcode import TranscodeStage
from src.stages.cloud import CloudStage
from src.stages.distribute import DistributeStage


@pytest.fixture
def tmp_mp4(tmp_path: Path) -> Path:
    f = tmp_path / "spot_verano.mp4"
    f.write_bytes(b"fake video content — not empty")
    return f


@pytest.fixture
def tmp_jpg(tmp_path: Path) -> Path:
    f = tmp_path / "imagen.jpg"
    f.write_bytes(b"fake image content")
    return f


# ── IngestStage ───────────────────────────────────────────────────────────────

class TestIngestStage:
    def test_success_on_existing_video(self, tmp_mp4: Path) -> None:
        # TODO: llamar IngestStage().process({"path": str(tmp_mp4)})
        # TODO: assert result.success is True
        # TODO: assert result.data["media_type"] == "video"
        # TODO: assert result.data["suffix"] == ".mp4"
        raise NotImplementedError

    def test_failure_on_missing_file(self) -> None:
        # TODO: llamar con path="/no/existe.mp4"
        # TODO: assert result.success is False
        # TODO: assert "no encontrado" in result.error.lower()
        raise NotImplementedError

    def test_failure_on_empty_file(self, tmp_path: Path) -> None:
        # TODO: crear archivo vacío y procesar
        # TODO: assert result.success is False
        raise NotImplementedError

    def test_image_media_type(self, tmp_jpg: Path) -> None:
        # TODO: assert result.data["media_type"] == "image"
        raise NotImplementedError


# ── ValidateStage ─────────────────────────────────────────────────────────────

class TestValidateStage:
    def test_valid_video_passes(self, tmp_mp4: Path) -> None:
        # TODO: primero IngestStage, luego ValidateStage
        # TODO: assert result.success is True
        # TODO: assert result.data["validated"] is True
        raise NotImplementedError

    def test_invalid_extension_fails(self, tmp_path: Path) -> None:
        # TODO: crear archivo .exe y procesar con ValidateStage directamente
        # (sin pasar por IngestStage — inyectar suffix manualmente)
        # TODO: assert result.success is False
        raise NotImplementedError


# ── TranscodeStage ────────────────────────────────────────────────────────────

class TestTranscodeStage:
    def test_transcode_video_calls_ffmpeg(self, tmp_mp4: Path, tmp_path: Path) -> None:
        """
        TODO: mockear ffmpeg.input, ffmpeg.output, ffmpeg.run
        para que no ejecuten ffmpeg real.
        TODO: llamar TranscodeStage(tmp_path).process(data_con_media_type_video)
        TODO: assert result.success is True
        TODO: assert result.data["transcoded"] is True
        TODO: assert "proxy_path" in result.data
        TODO: assert "thumb_path" in result.data
        TODO: assert "web_path" in result.data
        """
        raise NotImplementedError

    def test_non_video_skips_transcode(self, tmp_jpg: Path, tmp_path: Path) -> None:
        # TODO: procesar imagen (media_type="image")
        # TODO: assert result.success is True
        # TODO: assert result.data["transcoded"] is False
        raise NotImplementedError


# ── CloudStage ────────────────────────────────────────────────────────────────

class TestCloudStage:
    def test_dry_run_does_not_call_boto3(self, tmp_mp4: Path, tmp_path: Path) -> None:
        """
        TODO: crear CloudStage("bucket", "canal9/spot", dry_run=True)
        TODO: preparar data con web_path/proxy_path/thumb_path existentes
        TODO: llamar process() y verificar:
              - result.success is True
              - result.data["s3_uploaded"] is True
              - boto3.client NUNCA fue llamado (usar patch)
        """
        raise NotImplementedError

    def test_s3_key_structure(self, tmp_mp4: Path, tmp_path: Path) -> None:
        """
        TODO: en dry_run=False, mockear boto3.client
        TODO: verificar que upload_file fue llamado con Key que empieza por "canal9/spot/video/"
        """
        raise NotImplementedError


# ── DistributeStage ───────────────────────────────────────────────────────────

class TestDistributeStage:
    def test_dry_run_prints_and_does_not_call_http(self, capsys: pytest.CaptureFixture[str]) -> None:
        """
        TODO: DistributeStage(dry_run=True).process(data_con_s3_web_url)
        TODO: assert result.success is True
        TODO: assert result.data["distributed"] is True
        TODO: capturar stdout y verificar "[DRY-RUN]" en el output
        TODO: mockear httpx.post y verificar que NO fue llamado
        """
        raise NotImplementedError

    def test_slack_called_in_prod_mode(self) -> None:
        """
        TODO: mockear httpx.post
        TODO: DistributeStage(slack_webhook_url="https://hooks.slack.com/...", dry_run=False)
        TODO: process() y verificar que httpx.post fue llamado una vez
        """
        raise NotImplementedError
