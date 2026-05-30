# Notion API

## 1. Autenticación — Integration Token

1. Ir a `https://www.notion.so/my-integrations` → Crear integración
2. Copiar el **Internal Integration Token** (`secret_...`)
3. En cada base de datos de Notion: `···` → Connections → agregar la integración

```python
import httpx

NOTION_TOKEN = "secret_..."
NOTION_VERSION = "2022-06-28"

def notion_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
```

---

## 2. Consultar una Base de Datos

```python
def query_database(
    database_id: str,
    filter_prop: str | None = None,
    filter_value: str | None = None,
) -> list[dict[str, object]]:
    body: dict[str, object] = {}

    if filter_prop and filter_value:
        body["filter"] = {
            "property": filter_prop,
            "rich_text": {"contains": filter_value},
        }

    resp = httpx.post(
        f"https://api.notion.com/v1/databases/{database_id}/query",
        headers=notion_headers(),
        json=body,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])
```

---

## 3. Crear una Página (Fila en la DB)

```python
def create_delivery_record(
    database_id: str,
    project: str,
    client: str,
    status: str = "En proceso",
) -> str:
    body = {
        "parent": {"database_id": database_id},
        "properties": {
            "Proyecto": {
                "title": [{"text": {"content": project}}]
            },
            "Cliente": {
                "rich_text": [{"text": {"content": client}}]
            },
            "Estado": {
                "select": {"name": status}
            },
            "Fecha": {
                "date": {"start": __import__("datetime").date.today().isoformat()}
            },
        },
    }
    resp = httpx.post(
        "https://api.notion.com/v1/pages",
        headers=notion_headers(),
        json=body,
    )
    resp.raise_for_status()
    page_id: str = resp.json()["id"]
    return page_id
```

---

## 4. Actualizar Propiedades de una Página

```python
def update_delivery_status(
    page_id: str,
    status: str,
    youtube_url: str = "",
    vimeo_url: str = "",
) -> None:
    properties: dict[str, object] = {
        "Estado": {"select": {"name": status}},
    }
    if youtube_url:
        properties["YouTube URL"] = {"url": youtube_url}
    if vimeo_url:
        properties["Vimeo URL"] = {"url": vimeo_url}

    resp = httpx.patch(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=notion_headers(),
        json={"properties": properties},
    )
    resp.raise_for_status()
```

---

## 5. Agregar Bloques de Contenido

```python
def append_delivery_note(page_id: str, note: str, video_urls: list[str]) -> None:
    children: list[dict[str, object]] = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Entrega"}}]
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": note}}]
            },
        },
    ]
    for url in video_urls:
        children.append({
            "object": "block",
            "type": "bookmark",
            "bookmark": {"url": url},
        })

    resp = httpx.patch(
        f"https://api.notion.com/v1/blocks/{page_id}/children",
        headers=notion_headers(),
        json={"children": children},
    )
    resp.raise_for_status()
```

---

## 6. Tipos de Propiedades Comunes

| Tipo Notion | Estructura en la API |
|-------------|---------------------|
| `title` | `{"title": [{"text": {"content": "..."}}]}` |
| `rich_text` | `{"rich_text": [{"text": {"content": "..."}}]}` |
| `select` | `{"select": {"name": "Opción"}}` |
| `multi_select` | `{"multi_select": [{"name": "tag1"}, ...]}` |
| `date` | `{"date": {"start": "2024-11-15"}}` |
| `url` | `{"url": "https://..."}` |
| `number` | `{"number": 42}` |
| `checkbox` | `{"checkbox": true}` |
| `email` | `{"email": "user@example.com"}` |

---

## Resumen

| Operación | Endpoint |
|-----------|----------|
| Consultar DB | `POST /v1/databases/{id}/query` |
| Crear página | `POST /v1/pages` con `parent.database_id` |
| Actualizar propiedades | `PATCH /v1/pages/{id}` |
| Agregar bloques | `PATCH /v1/blocks/{id}/children` |
| Header requerido | `Notion-Version: 2022-06-28` |
