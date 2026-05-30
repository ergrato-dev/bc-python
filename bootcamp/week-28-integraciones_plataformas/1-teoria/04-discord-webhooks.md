# Discord Webhooks

## 1. Crear un Webhook

En Discord: Canal → Editar → Integraciones → Webhooks → Nuevo Webhook.
Se obtiene una URL del tipo `https://discord.com/api/webhooks/{id}/{token}`.

---

## 2. Mensaje Simple

```python
import httpx


def send_discord_message(webhook_url: str, content: str) -> None:
    resp = httpx.post(webhook_url, json={"content": content})
    resp.raise_for_status()
```

---

## 3. Embeds — Mensajes Enriquecidos

Los embeds permiten mensajes con color, campos estructurados, imagen y footer.

```python
from datetime import datetime, timezone


def send_delivery_embed(
    webhook_url: str,
    project: str,
    client: str,
    youtube_url: str,
    vimeo_url: str,
    thumbnail_url: str = "",
) -> None:
    embed: dict[str, object] = {
        "title": f"Entrega lista: {project}",
        "description": f"El proyecto **{project}** fue publicado y está listo para revisión.",
        "color": 0x3FB950,  # verde — en decimal
        "fields": [
            {"name": "Cliente", "value": client, "inline": True},
            {"name": "YouTube", "value": f"[Ver]({youtube_url})", "inline": True},
            {"name": "Vimeo", "value": f"[Ver]({vimeo_url})", "inline": True},
        ],
        "footer": {
            "text": "Studio BC — Pipeline de Distribución",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if thumbnail_url:
        embed["thumbnail"] = {"url": thumbnail_url}

    payload: dict[str, object] = {
        "username": "Studio BC Bot",
        "embeds": [embed],
    }
    resp = httpx.post(webhook_url, json=payload)
    resp.raise_for_status()
```

### Colores comunes (valor decimal)

| Color | Hex | Decimal |
|-------|-----|---------|
| Verde | `#3FB950` | `4177232` |
| Rojo | `#F85149` | `16273737` |
| Amarillo | `#FFD43B` | `16766011` |
| Azul | `#58A6FF` | `5874431` |

---

## 4. Enviar Archivos Adjuntos

```python
from pathlib import Path


def send_file_to_discord(webhook_url: str, file_path: Path, message: str = "") -> None:
    with file_path.open("rb") as f:
        resp = httpx.post(
            webhook_url,
            data={"content": message} if message else {},
            files={"file": (file_path.name, f, "application/octet-stream")},
        )
    resp.raise_for_status()
```

---

## 5. Rate Limiting

Discord limita a 30 mensajes por minuto por webhook. Si se excede, responde con `429 Too Many Requests` y un header `Retry-After`.

```python
import time


def send_with_rate_limit(webhook_url: str, payload: dict[str, object]) -> None:
    for attempt in range(3):
        resp = httpx.post(webhook_url, json=payload)
        if resp.status_code == 429:
            retry_after = float(resp.json().get("retry_after", 1.0))
            print(f"Rate limit Discord — esperando {retry_after}s")
            time.sleep(retry_after)
            continue
        resp.raise_for_status()
        return
    raise RuntimeError("Discord webhook: rate limit agotado tras 3 intentos")
```

---

## 6. Webhook con Múltiples Embeds

```python
def send_batch_summary(
    webhook_url: str,
    results: list[dict[str, object]],
) -> None:
    embeds = []
    for r in results[:10]:  # Discord acepta máx 10 embeds por mensaje
        color = 0x3FB950 if r.get("success") else 0xF85149
        embeds.append({
            "title": str(r.get("project", "Desconocido")),
            "color": color,
            "fields": [
                {"name": "Estado", "value": "OK" if r.get("success") else "FALLO", "inline": True},
                {"name": "Plataforma", "value": str(r.get("platform", "")), "inline": True},
            ],
        })
    httpx.post(webhook_url, json={"embeds": embeds}).raise_for_status()
```

---

## Resumen

| Concepto | Detalle |
|----------|---------|
| Payload básico | `{"content": "texto"}` |
| Embed | `{"embeds": [{"title", "color", "fields", "footer", "timestamp"}]}` |
| Color | Entero decimal (ej. `0x3FB950` = verde) |
| Inline fields | `"inline": true` — aparecen lado a lado (máx 3 por fila) |
| Rate limit | 30 msg/min; `Retry-After` en el header de la respuesta 429 |
| Archivos | Multipart form con `files={"file": (name, data, mimetype)}` |
