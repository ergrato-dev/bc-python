# Autenticación HTTP

## Objetivos

- Implementar Bearer Token y API Key con `httpx.Auth`
- Entender el flujo OAuth2 client credentials
- Gestionar renovación automática de tokens
- Elegir el esquema correcto según la API

---

## 1. API Key — el más simple

```python
import httpx

# Header personalizado (más común)
with httpx.Client(
    base_url="https://api.musiclicensing.bc",
    headers={"X-API-Key": "sk-abc123def456"},
) as client:
    response = client.get("/tracks", params={"genre": "cinematic"})

# Query param (menos seguro — aparece en logs de servidor)
with httpx.Client(base_url="https://api.musiclicensing.bc") as client:
    response = client.get("/tracks", params={"api_key": "sk-abc123def456"})
```

### `httpx.Auth` personalizado para API Key

```python
import httpx
from typing import Generator

class APIKeyAuth(httpx.Auth):
    def __init__(self, api_key: str, header_name: str = "X-API-Key") -> None:
        self.api_key = api_key
        self.header_name = header_name

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers[self.header_name] = self.api_key
        yield request

# Uso
with httpx.Client(
    base_url="https://api.musiclicensing.bc",
    auth=APIKeyAuth("sk-abc123def456"),
) as client:
    response = client.get("/tracks")
```

---

## 2. Bearer Token

```python
import httpx
from typing import Generator

class BearerAuth(httpx.Auth):
    def __init__(self, token: str) -> None:
        self.token = token

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request

# Uso
with httpx.Client(
    base_url="https://api.studio.bc",
    auth=BearerAuth("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
) as client:
    response = client.get("/projects")
    response.raise_for_status()
    print(response.json())
```

---

## 3. OAuth2 — Client Credentials Flow

El flujo más común para APIs server-to-server (sin usuario):

```
┌─ Tu app ──────────────────────────────────────────┐
│                                                   │
│  1. POST /token  (client_id + client_secret)      │
│     → access_token (válido N segundos)            │
│                                                   │
│  2. GET /resource  Authorization: Bearer <token>  │
│     → datos protegidos                            │
│                                                   │
│  3. Cuando expires_in = 0: volver al paso 1       │
└───────────────────────────────────────────────────┘
```

```python
import time
import httpx
from dataclasses import dataclass, field

@dataclass
class OAuth2Token:
    access_token: str
    expires_at: float   # timestamp Unix

    @property
    def is_expired(self) -> bool:
        return time.time() >= self.expires_at - 30   # 30s de margen

class OAuth2ClientCredentials(httpx.Auth):
    """Auth que obtiene y renueva automáticamente el token."""

    requires_response_body = True   # necesario para leer el token en auth_flow

    def __init__(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
    ) -> None:
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self._token: OAuth2Token | None = None

    def _fetch_token(self, client: httpx.Client) -> OAuth2Token:
        response = client.post(
            self.token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        response.raise_for_status()
        data = response.json()
        return OAuth2Token(
            access_token=data["access_token"],
            expires_at=time.time() + data["expires_in"],
        )

    def auth_flow(
        self,
        request: httpx.Request,
    ):
        # Obtener o renovar token
        if self._token is None or self._token.is_expired:
            # Hacer una sub-request para obtener el token
            token_request = self.build_request(
                method="POST",
                url=self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            token_response = yield token_request
            token_response.read()
            token_response.raise_for_status()
            data = token_response.json()
            self._token = OAuth2Token(
                access_token=data["access_token"],
                expires_at=time.time() + data["expires_in"],
            )

        request.headers["Authorization"] = f"Bearer {self._token.access_token}"
        yield request

# Uso
auth = OAuth2ClientCredentials(
    token_url="https://auth.provider.bc/oauth/token",
    client_id="studio-bc",
    client_secret="super-secret",
)

with httpx.Client(base_url="https://api.provider.bc", auth=auth) as client:
    r1 = client.get("/catalog")       # obtiene token automáticamente
    r2 = client.get("/licenses")      # reutiliza el token mientras no expire
```

---

## 4. Basic Auth

```python
import httpx

# httpx tiene Basic Auth integrado
with httpx.Client(base_url="https://api.legacy.bc") as client:
    response = client.get(
        "/reports",
        auth=("username", "password"),  # tuple → Basic Auth
    )

# Equivalente explícito
with httpx.Client(
    base_url="https://api.legacy.bc",
    auth=httpx.BasicAuth("username", "password"),
) as client:
    response = client.get("/reports")
```

---

## 5. Elegir el esquema correcto

```
¿Qué esquema de auth usar?
│
├─ API pública de tercero con clave fija
│   └─ API Key (header X-API-Key o Authorization: ApiKey)
│
├─ Tu propia API o API del cliente con token JWT
│   └─ Bearer Token (Authorization: Bearer <jwt>)
│
├─ API server-to-server (sin usuario)
│   └─ OAuth2 Client Credentials
│
├─ API legacy corporativa
│   └─ Basic Auth (evitar si hay alternativa)
│
└─ API sin autenticación (pública)
    └─ Nada (o User-Agent personalizado por cortesía)
```

---

## ✅ Resumen

| Esquema | Header | `httpx.Auth` |
|---------|--------|-------------|
| API Key | `X-API-Key: sk-...` | `APIKeyAuth(key)` personalizado |
| Bearer Token | `Authorization: Bearer <token>` | `BearerAuth(token)` personalizado |
| Basic Auth | `Authorization: Basic <b64>` | `httpx.BasicAuth(user, pass)` |
| OAuth2 CC | Bearer renovado automáticamente | `OAuth2ClientCredentials(...)` |

---

## Recursos Adicionales

- [httpx — Authentication](https://www.python-httpx.org/advanced/authentication/)
- [OAuth2 Client Credentials — RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749#section-4.4)
