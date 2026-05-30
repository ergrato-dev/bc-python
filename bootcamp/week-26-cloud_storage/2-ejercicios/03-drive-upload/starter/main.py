"""
Ejercicio 03: Google Drive API — Upload y Permisos
===================================================
Sube un archivo a Drive, crea carpetas y comparte con un email externo.

Requisitos:
    pip install google-api-python-client google-auth
    Colocar credentials.json (Service Account) en el directorio de trabajo.

Ejecutar:
    python main.py
"""
from __future__ import annotations

from pathlib import Path


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_drive_service(credentials_path: str = "credentials.json"):
    """Crea y devuelve el servicio autenticado de Google Drive v3."""
    # TODO: importar Credentials.from_service_account_file y build("drive", "v3", ...)
    # SCOPES = ["https://www.googleapis.com/auth/drive"]
    raise NotImplementedError


def get_or_create_folder(service, name: str, parent_id: str | None = None) -> str:
    """Devuelve el ID de la carpeta con ese nombre (en el padre dado), creándola si no existe."""
    # TODO: buscar con files().list(q=...) y crear si no aparece
    raise NotImplementedError


def upload_file(
    service,
    local_path: Path,
    folder_id: str,
    description: str = "",
) -> dict[str, str]:
    """Sube el archivo a la carpeta indicada. Devuelve {id, name, webViewLink}."""
    # TODO: MediaFileUpload(resumable=True) + files().create(fields="id,name,webViewLink")
    raise NotImplementedError


def share_with_reader(service, file_id: str, email: str) -> None:
    """Comparte el archivo con el email dado como lector."""
    # TODO: permissions().create(type="user", role="reader", emailAddress=email)
    raise NotImplementedError


def share_with_link(service, file_id: str) -> str:
    """Activa el link público de solo lectura y devuelve el webViewLink."""
    # TODO: permissions().create(type="anyone", role="reader")
    raise NotImplementedError


# ── Ejercicio ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    service = get_drive_service()

    print("1. Creando estructura de carpetas...")
    studio_id = get_or_create_folder(service, "Studio BC Test")
    proyecto_id = get_or_create_folder(service, "spot-verano-2024", parent_id=studio_id)
    entrega_id = get_or_create_folder(service, "Entregables", parent_id=proyecto_id)
    print(f"   Carpeta entregables: {entrega_id}")

    print("2. Subiendo archivo de prueba...")
    test_file = Path("entregable_v1.mp4")
    test_file.write_bytes(b"fake video content for testing")  # archivo de prueba

    result = upload_file(service, test_file, entrega_id, description="Entrega final spot verano")
    print(f"   Subido: {result['name']} → {result.get('webViewLink', 'N/A')[:60]}")

    print("3. Generando link público de solo lectura...")
    link = share_with_link(service, result["id"])
    print(f"   Link: {link[:70]}...")

    test_file.unlink(missing_ok=True)
    print("OK — Ejercicio 03 completado")
