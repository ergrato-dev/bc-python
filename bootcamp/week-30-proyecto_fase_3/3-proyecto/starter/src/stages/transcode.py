"""
TranscodeStage — genera proxy, thumbnail y web encode con ffmpeg-python.

Requiere:
    pip install ffmpeg-python
    sudo apt install ffmpeg  (o brew install ffmpeg en macOS)
"""
from __future__ import annotations

from pathlib import Path

from .base import Stage, StageResult


class TranscodeStage:
    name = "transcode"

    def __init__(self, output_dir: Path) -> None:
        self._output = output_dir

    def process(self, data: dict[str, object]) -> StageResult:
        path = Path(str(data.get("path", "")))
        stem = str(data.get("stem", path.stem))
        media_type = str(data.get("media_type", "other"))

        if media_type != "video":
            return StageResult(success=True, data={**data, "transcoded": False})

        proxy_path = self._output / "proxy" / f"{stem}_proxy.mp4"
        thumb_path = self._output / "thumbs" / f"{stem}_thumb.jpg"
        web_path = self._output / "web" / f"{stem}_web.mp4"

        try:
            self._generate_proxy(path, proxy_path)
            self._extract_thumbnail(path, thumb_path)
            self._generate_web_encode(path, web_path)
        except Exception as e:
            return StageResult(success=False, data=data, error=f"Transcode error: {e}")

        return StageResult(
            success=True,
            data={
                **data,
                "transcoded": True,
                "proxy_path": str(proxy_path),
                "thumb_path": str(thumb_path),
                "web_path": str(web_path),
            },
        )

    def _generate_proxy(self, src: Path, dest: Path) -> None:
        """
        Genera un proxy al 25 % de la resolución original.
        Codec: libx264, preset veryfast, audio copy.

        TODO: usar ffmpeg.input(str(src)) → filtro scale=iw/4:ih/4 → output
              con vcodec=libx264, preset=veryfast, crf=28
        Referencia: semana 25 — TranscodeStage.generate_proxy()
        """
        import ffmpeg  # type: ignore[import-untyped]
        dest.parent.mkdir(parents=True, exist_ok=True)
        raise NotImplementedError

    def _extract_thumbnail(self, src: Path, dest: Path) -> None:
        """
        Extrae un frame en el segundo 5 del video como JPG.

        TODO: usar ffmpeg.input(str(src), ss=5) → output con vframes=1
        Referencia: semana 25 — InspectorStage / encoder.py
        """
        import ffmpeg  # type: ignore[import-untyped]
        dest.parent.mkdir(parents=True, exist_ok=True)
        raise NotImplementedError

    def _generate_web_encode(self, src: Path, dest: Path) -> None:
        """
        Genera el encode web: H.264 CRF 23, máximo 1920x1080, +faststart.
        Si el video es más pequeño que 1080p, mantiene la resolución original.

        TODO: usar ffmpeg con scale='min(iw\,1920):min(ih\,1080):force_original_aspect_ratio=decrease'
              vcodec=libx264, crf=23, preset=slow, movflags=+faststart
        """
        import ffmpeg  # type: ignore[import-untyped]
        dest.parent.mkdir(parents=True, exist_ok=True)
        raise NotImplementedError
