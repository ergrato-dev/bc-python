# Glosario — Semana 26: Cloud Storage y Assets

## Amazon S3

| Término | Definición |
|---------|------------|
| **Bucket** | Contenedor de objetos S3 con nombre globalmente único en AWS; equivalente a un volumen o disco |
| **Object** | Archivo almacenado en S3, identificado por su key; puede tener hasta 5 TB |
| **Key** | Ruta completa del objeto dentro del bucket (ej. `canal9/spot/video/2024-11/clip.mp4`) |
| **ETag** | Hash MD5 del objeto para single-part upload; `{hash}-{n}` para multipart — NO es SHA-256 |
| **Prefix** | Fragmento inicial de key usado como filtro en `list_objects_v2`; simula carpetas |
| **Multipart Upload** | Mecanismo para subir archivos > 100 MB en partes paralelas; requiere `complete` o `abort` al final |
| **Presigned URL** | URL temporal firmada con credenciales AWS que permite GET o PUT sin exponer la clave secreta |
| **Versioning** | Característica de bucket que conserva todas las versiones de un objeto en lugar de sobrescribirlo |
| **Delete Marker** | Versión especial creada al "borrar" un objeto con versioning activo; no elimina versiones anteriores |

## Storage Classes

| Término | Definición |
|---------|------------|
| **S3 Standard** | Hot storage: alta disponibilidad y baja latencia; costo más alto por GB |
| **Standard-IA** | Infrequent Access: mismo nivel de durabilidad, menor costo por GB, cargo por retrieval |
| **Intelligent-Tiering** | Mueve objetos automáticamente entre tiers según patrones de acceso |
| **Glacier Instant Retrieval** | Cold storage con latencia de milisegundos; para datos accedidos < 1 vez por trimestre |
| **Glacier Flexible Retrieval** | Archivado profundo; latencia de minutos a horas; 60–70% más barato que Standard |
| **Deep Archive** | Costo mínimo de S3; recuperación en horas; para archivos legales o históricos |
| **Lifecycle Policy** | Regla automática que transiciona objetos entre storage classes o los elimina tras N días |

## Conceptos de Cloud

| Término | Definición |
|---------|------------|
| **IAM** | Identity and Access Management — sistema de control de acceso de AWS para usuarios, roles y políticas |
| **IAM Role** | Identidad temporal con permisos; preferida sobre access keys para servicios en producción |
| **Access Key** | Par `ACCESS_KEY_ID` + `SECRET_ACCESS_KEY` para autenticación programática; evitar hardcodear |
| **Block Public Access** | Configuración de bucket que impide cualquier política que lo haga público accidentalmente |
| **SSE-S3** | Server-Side Encryption gestionada por S3; cifra objetos en reposo automáticamente |
| **SSE-KMS** | Cifrado con AWS Key Management Service; auditable y con rotación de claves |
| **Paginator** | Helper de boto3 para manejar respuestas paginadas (ej. `list_objects_v2` devuelve max 1000) |

## Google Drive API

| Término | Definición |
|---------|------------|
| **Service Account** | Cuenta de servicio (no humano) de Google con credenciales JSON; ideal para scripts automáticos |
| **OAuth2** | Protocolo de autorización; para Service Accounts se usa el flujo de "server-to-server" sin usuario |
| **Scope** | Permiso declarado en el token OAuth2 (ej. `https://www.googleapis.com/auth/drive`) |
| **File ID** | Identificador único de un archivo o carpeta en Drive (cadena opaca de ~33 caracteres) |
| **MIME type de carpeta** | `application/vnd.google-apps.folder` — tipo especial para crear carpetas en Drive |
| **MediaFileUpload** | Clase de `googleapiclient` para subir archivos binarios; `resumable=True` para archivos grandes |
| **webViewLink** | URL pública o compartida para ver el archivo en el navegador |
| **Permission** | Entidad que define quién tiene acceso y con qué rol (reader, writer, owner) |

## Sincronización

| Término | Definición |
|---------|------------|
| **Sync incremental** | Solo transfiere archivos nuevos o modificados desde la última sincronización |
| **SHA-256** | Hash criptográfico de 256 bits; usado como checksum local para detectar modificaciones |
| **Idempotencia** | Propiedad de una operación que produce el mismo resultado si se ejecuta múltiples veces |
| **Lock file** | Archivo que contiene el PID del proceso activo; evita ejecuciones concurrentes del mismo daemon |
| **Atomic write** | Técnica de escribir a un `.tmp` y luego hacer `rename`/`replace` para evitar archivos corruptos |
| **State file** | Registro JSON local con checksums y timestamps de la última sincronización por archivo |
