"""Cliente para CloudRender BC."""
from __future__ import annotations

import time
import httpx
from .auth import BearerAuth
from .models import RenderJob, RenderJobCreated
from .retry import RENDER_RETRY

DEFAULT_TIMEOUT = httpx.Timeout(connect=3.0, read=15.0, write=5.0, pool=2.0)


class RenderClient:
    """Cliente de CloudRender BC con Bearer auth, timeouts y retry."""

    def __init__(
        self,
        token: str,
        base_url: str = "https://api.cloudrender.bc",
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            auth=BearerAuth(token),
            timeout=DEFAULT_TIMEOUT,
            headers={"User-Agent": "studio-bc-client/1.0"},
        )

    def __enter__(self) -> "RenderClient":
        return self

    def __exit__(self, *args: object) -> None:
        self._client.close()

    @RENDER_RETRY
    def submit_job(
        self,
        project_id: str,
        track_id: str,
        resolution: str = "1080p",
    ) -> RenderJobCreated:
        """
        Lanza un job de render.
        POST /jobs  body: {"project_id": ..., "track_id": ..., "resolution": ...}
        Retorna RenderJobCreated validado.
        """
        # TODO
        raise NotImplementedError

    @RENDER_RETRY
    def get_job_status(self, job_id: str) -> RenderJob:
        """
        Consulta el estado de un job.
        GET /jobs/<job_id>
        Retorna RenderJob validado.
        """
        # TODO
        raise NotImplementedError

    def wait_for_job(
        self,
        job_id: str,
        poll_interval: float = 2.0,
        max_wait: float = 120.0,
    ) -> RenderJob:
        """
        Espera hasta que job.status == "done" o max_wait expire.
        Llama a get_job_status() cada poll_interval segundos.
        Lanza TimeoutError si supera max_wait.
        Lanza RuntimeError si status == "failed".
        """
        # TODO: registrar tiempo de inicio
        # TODO: loop: get_job_status → si done retornar, si failed lanzar
        # TODO: time.sleep(poll_interval) y verificar tiempo transcurrido
        raise NotImplementedError
