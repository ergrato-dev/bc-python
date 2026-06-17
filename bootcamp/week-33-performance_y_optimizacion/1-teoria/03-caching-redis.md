# Caching con Redis

## 1. ¿Por qué cachear?

La metadata generada por IA (Whisper + GPT) cuesta tiempo y dinero:
- Whisper: 1 min de audio → ~2 seg + $0.006
- GPT-4o: análisis de 5 frames → ~3 seg + $0.05

Si el mismo asset se procesa 10 veces, el cache evita 9 llamadas a la API.

---

## 2. Conectar a Redis con redis-py

```python
from redis import Redis

# Conexión básica
r: Redis[bytes] = Redis(host="localhost", port=6379, db=0)

# Ping para verificar
r.ping()  # True si Redis responde

# Con decode_responses=True — devuelve str en vez de bytes
r_str: Redis[str] = Redis(host="localhost", port=6379, decode_responses=True)
```

```bash
# Redis con Docker (sin instalación local):
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

---

## 3. Operaciones Básicas

```python
import json
from redis import Redis

r: Redis[bytes] = Redis()

# SET y GET simple
r.set("clave", "valor")
value = r.get("clave")          # b"valor" (bytes)

# Con TTL (expira en 1 hora)
r.setex("clave", 3600, "valor")

# SET solo si no existe
r.setnx("clave", "valor")       # False si ya existe

# Eliminar
r.delete("clave")

# Verificar existencia
r.exists("clave")               # 1 si existe, 0 si no

# GET con TTL restante
r.ttl("clave")                  # segundos; -1 = sin TTL; -2 = no existe
```

---

## 4. Patrón Cache-Aside

El patrón más común: la aplicación maneja el cache manualmente.

```python
import json
from redis import Redis
from typing import Any

r: Redis[bytes] = Redis()


def get_metadata(asset_key: str) -> dict[str, Any]:
    """Patrón cache-aside para metadata de Studio BC."""
    # 1. Intentar desde cache
    cached = r.get(f"studio:meta:{asset_key}")
    if cached is not None:
        return json.loads(cached)   # Cache HIT

    # 2. Cache MISS — generar desde la fuente
    result = _generate_metadata_from_ai(asset_key)  # costoso

    # 3. Guardar en cache con TTL de 1 hora
    r.setex(
        f"studio:meta:{asset_key}",
        3600,
        json.dumps(result, ensure_ascii=False),
    )

    return result
```

Flujo:

```
app → GET cache → HIT → retornar
               → MISS → generar → SET cache → retornar
```

---

## 5. Patrón Write-Through

Escribir en cache y en base de datos simultáneamente:

```python
def save_metadata(asset_key: str, metadata: dict[str, Any]) -> None:
    """Write-through: actualiza DB y cache en una sola operación."""
    # 1. Guardar en DB
    db.execute("INSERT INTO assets (key, metadata) VALUES (?, ?)", (asset_key, json.dumps(metadata)))

    # 2. Actualizar cache
    r.setex(f"studio:meta:{asset_key}", 3600, json.dumps(metadata, ensure_ascii=False))
```

---

## 6. Invalidación del Cache

```python
def invalidate_asset(asset_key: str) -> None:
    """Borrar del cache cuando el asset se regenera."""
    r.delete(f"studio:meta:{asset_key}")


def invalidate_pattern(pattern: str) -> None:
    """Borrar todas las claves que coinciden con un patrón."""
    for key in r.scan_iter(match=pattern):
        r.delete(key)

# Borrar toda la metadata de Studio BC
invalidate_pattern("studio:meta:*")
```

---

## 7. Clase MetadataCache Completa

```python
import json
from typing import Any
from redis import Redis


class MetadataCache:
    PREFIX = "studio:meta:"

    def __init__(self, host: str = "localhost", port: int = 6379, ttl: int = 3600) -> None:
        self._r: Redis[bytes] = Redis(host=host, port=port)
        self._ttl = ttl

    def _key(self, key: str) -> str:
        return f"{self.PREFIX}{key}"

    def get(self, key: str) -> dict[str, Any] | None:
        raw = self._r.get(self._key(key))
        return json.loads(raw) if raw is not None else None

    def set(self, key: str, value: dict[str, Any], ttl: int | None = None) -> None:
        self._r.setex(self._key(key), ttl or self._ttl, json.dumps(value, ensure_ascii=False))

    def delete(self, key: str) -> None:
        self._r.delete(self._key(key))

    def stats(self) -> dict[str, Any]:
        info = self._r.info()
        return {
            "connected_clients": info["connected_clients"],
            "used_memory_human": info["used_memory_human"],
            "keyspace_hits": info["keyspace_hits"],
            "keyspace_misses": info["keyspace_misses"],
            "keys": self._r.dbsize(),
        }
```

---

## 8. TTL y Estrategias de Expiración

| Estrategia | TTL | Cuándo |
|------------|-----|--------|
| Datos estáticos | Sin TTL (`r.set`) | Assets archivados que nunca cambian |
| Datos semi-estáticos | 1h–24h | Metadata generada por IA |
| Datos de sesión | 30 min | Resultados de búsqueda semántica |
| Rate limiting | 1 min | Contadores de API calls |

```python
# Ejemplo: rate limiting con Redis
def can_call_api(client_id: str, limit: int = 10, window_s: int = 60) -> bool:
    key = f"rate:{client_id}:{int(time.time() // window_s)}"
    count = r.incr(key)
    if count == 1:
        r.expire(key, window_s)
    return count <= limit
```

---

## Resumen

| Operación | Comando redis-py |
|-----------|-----------------|
| Guardar con TTL | `r.setex(key, ttl_s, value)` |
| Leer | `r.get(key)` → `bytes | None` |
| Borrar | `r.delete(key)` |
| Verificar existencia | `r.exists(key)` → `int` |
| TTL restante | `r.ttl(key)` → `int` segundos |
| Scan pattern | `r.scan_iter(match="prefix:*")` |
| Info/Stats | `r.info()` → `dict` |
