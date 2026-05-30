# Vimeo API

## 1. Autenticación

Vimeo usa OAuth2 pero para scripts automatizados basta con un **Personal Access Token**:

1. Ir a `https://developer.vimeo.com/apps`
2. Crear una app → Generate Access Token
3. Scopes necesarios: `upload`, `edit`, `video_files`, `public`, `private`

```python
import vimeo

client = vimeo.VimeoClient(
    token="YOUR_ACCESS_TOKEN",
    key="YOUR_CLIENT_ID",
    secret="YOUR_CLIENT_SECRET",
)
```

---

## 2. Upload con Protocolo TUS

TUS (Tus Uploadable Something) es un protocolo open-source para uploads resumables y tolerantes a fallos. Vimeo lo usa porque permite reanudar uploads interrumpidos sin empezar de cero.

```python
from pathlib import Path


def upload_video(
    client: vimeo.VimeoClient,
    video_path: Path,
    title: str,
    description: str = "",
    privacy: str = "unlisted",
) -> str:
    uri = client.upload(
        str(video_path),
        data={
            "name": title,
            "description": description,
            "privacy": {
                "view": privacy,          # "anybody" | "unlisted" | "nobody" | "password"
                "embed": "private",       # dónde se puede embeber
                "download": False,
            },
            "content_rating": ["safe"],
        },
    )
    # uri tiene formato "/videos/123456789"
    video_id = uri.split("/")[-1]
    print(f"Video Vimeo: https://vimeo.com/{video_id}")
    return video_id
```

La librería `PyVimeo` maneja TUS internamente: divide el archivo en partes y reintenta automáticamente.

---

## 3. Actualizar Metadata

```python
def update_video(
    client: vimeo.VimeoClient,
    video_id: str,
    title: str | None = None,
    description: str | None = None,
    tags: list[str] | None = None,
) -> None:
    data: dict[str, object] = {}
    if title:
        data["name"] = title
    if description:
        data["description"] = description
    if tags:
        data["tags"] = ",".join(tags)

    resp = client.patch(f"/videos/{video_id}", data=data)
    if resp.status_code != 200:
        raise RuntimeError(f"Vimeo update error {resp.status_code}: {resp.json()}")
```

---

## 4. Configurar Privacidad y Embed

```python
def set_embed_settings(
    client: vimeo.VimeoClient,
    video_id: str,
    allowed_domains: list[str],
) -> None:
    client.patch(
        f"/videos/{video_id}",
        data={
            "embed": {
                "buttons": {"like": True, "share": False, "watchlater": False},
                "logos": {"vimeo": False},
                "title": {"name": "show", "owner": "hide", "portrait": "hide"},
            },
            "privacy": {
                "view": "unlisted",
                "embed": "whitelist",    # solo dominios autorizados
            },
        },
    )
    for domain in allowed_domains:
        client.put(f"/videos/{video_id}/privacy/domains/{domain}")
```

---

## 5. Álbumes y Showcases

```python
def get_or_create_album(
    client: vimeo.VimeoClient,
    name: str,
    user_id: str = "me",
) -> str:
    resp = client.get(f"/users/{user_id}/albums", params={"per_page": 100})
    for album in resp.json().get("data", []):
        if album["name"] == name:
            return album["uri"].split("/")[-1]

    resp = client.post(
        f"/users/{user_id}/albums",
        data={"name": name, "privacy": "unlisted"},
    )
    return resp.json()["uri"].split("/")[-1]


def add_to_album(
    client: vimeo.VimeoClient,
    album_id: str,
    video_id: str,
    user_id: str = "me",
) -> None:
    client.put(f"/users/{user_id}/albums/{album_id}/videos/{video_id}")
    print(f"Video {video_id} agregado al álbum {album_id}")
```

---

## 6. Obtener URL de Video Procesado

Vimeo procesa el video después del upload. La URL directa está disponible solo cuando `status == "available"`:

```python
def wait_for_processing(
    client: vimeo.VimeoClient,
    video_id: str,
    timeout_s: int = 300,
) -> str:
    import time
    start = time.time()
    while time.time() - start < timeout_s:
        resp = client.get(f"/videos/{video_id}", params={"fields": "status,link"})
        data = resp.json()
        if data.get("status") == "available":
            return data["link"]
        time.sleep(10)
    raise TimeoutError(f"Vimeo video {video_id} no procesó en {timeout_s}s")
```

---

## Resumen

| Operación | Método |
|-----------|--------|
| Upload | `client.upload(path, data={...})` |
| Actualizar metadata | `client.patch("/videos/{id}", data={...})` |
| Privacidad | `"anybody"` / `"unlisted"` / `"nobody"` / `"password"` |
| Crear álbum | `client.post("/users/me/albums", ...)` |
| Agregar a álbum | `client.put("/users/me/albums/{album_id}/videos/{video_id}")` |
| Esperar procesamiento | polling `GET /videos/{id}` hasta `status == "available"` |
