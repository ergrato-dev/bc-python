# Glosario — Semana 28: Integraciones con Plataformas

## YouTube Data API

| Término | Definición |
|---------|------------|
| **OAuth2 flow** | Protocolo de autorización en nombre del usuario; requiere `client_secrets.json` + consentimiento en el navegador |
| **Refresh token** | Token de larga duración que permite renovar `access_token` sin pedir al usuario que autorice de nuevo |
| **Upload resumable** | Técnica que divide el archivo en chunks y puede retomar si la conexión se interrumpe |
| **MediaFileUpload** | Clase de `googleapiclient` para subir archivos; `resumable=True` activa el upload en partes |
| **next_chunk()** | Itera el upload chunk a chunk; devuelve `(status, response)` — `response != None` indica que terminó |
| **privacy_status** | Visibilidad del video: `"public"` / `"unlisted"` / `"private"` |
| **categoryId** | Categoría del video en YouTube; `"22"` = People & Blogs, `"24"` = Entertainment |
| **playlist** | Lista de reproducción; se gestiona con `playlists()` y `playlistItems()` |

## Vimeo

| Término | Definición |
|---------|------------|
| **TUS** | Tus Uploadable Something — protocolo open-source para uploads resumables con soporte de reanudación |
| **PyVimeo** | Cliente oficial Python de Vimeo; `client.upload()` maneja TUS internamente |
| **privacy.view** | Visibilidad en Vimeo: `"anybody"` / `"unlisted"` / `"nobody"` / `"password"` |
| **privacy.embed** | Dónde se puede embeber: `"public"` / `"private"` / `"whitelist"` |
| **album / showcase** | Colección de videos en Vimeo, accesible por URL propia |
| **status: available** | Estado del video una vez que Vimeo terminó de procesarlo (encoding, thumbnails) |

## Slack

| Término | Definición |
|---------|------------|
| **Incoming Webhook** | URL fija por canal que acepta JSON con `{"text": ...}`; sin token ni SDK |
| **Bot Token** | Token `xoxb-...` de un Slack App; permite `chat.postMessage` y otras APIs |
| **Block Kit** | Sistema de componentes visuales de Slack: Header, Section, Divider, Actions, Image |
| **mrkdwn** | Variante de Markdown de Slack: `*negrita*`, `_cursiva_`, `<url|texto>`, `` `code` `` |
| **`ts`** | Timestamp único de un mensaje en Slack; sirve como ID para responder en hilo |
| **files_upload_v2** | Endpoint moderno de upload de archivos (reemplaza al deprecated `files_upload`) |

## Discord

| Término | Definición |
|---------|------------|
| **Webhook URL** | URL que permite enviar mensajes a un canal sin autenticación de bot |
| **Embed** | Mensaje enriquecido con color, título, campos, thumbnail, footer y timestamp |
| **Color decimal** | El color del embed se expresa en decimal (ej. `0x3FB950` = `4177232`) |
| **Inline field** | Campo del embed que aparece lado a lado con otros (máx 3 por fila) |
| **Rate limit 429** | Discord rechaza > 30 msg/min por webhook; header `Retry-After` indica cuánto esperar |

## Notion API

| Término | Definición |
|---------|------------|
| **Integration token** | Token `secret_...` que autentica la integración en la API; se crea en notion.so/my-integrations |
| **Database** | Estructura de Notion con propiedades tipadas; cada fila es una `Page` |
| **Page** | Unidad básica de Notion; dentro de una DB es una "fila" con propiedades |
| **Properties** | Campos de la página (título, texto, select, fecha, URL, número, etc.) |
| **Block** | Elemento de contenido dentro de una página: párrafo, heading, bookmark, code, etc. |
| **Notion-Version header** | Header obligatorio `"2022-06-28"` para indicar la versión de la API |
| **`rich_text`** | Tipo de propiedad para texto formateado; se pasa como array de objetos `{text: {content: "..."}}` |
