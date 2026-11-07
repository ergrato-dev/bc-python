"""Un servidor HTTP de prueba, en tu máquina, para los ejercicios de la semana 18.

Qué: `start()` arranca el servidor en un hilo, en 127.0.0.1 y un puerto libre, y
devuelve su dirección ("http://127.0.0.1:<puerto>").
Para qué: practicar con respuestas de todo tipo (lentas, con error, con fallos que se
arreglan solos) sin depender de Internet ni de que una API de verdad esté de humor.
Impacto: solo escucha en 127.0.0.1, así que nadie de fuera de tu máquina se conecta.
No hace falta que lo leas para hacer el ejercicio; main.py solo usa `start()`.

Rutas:
    GET  /estaciones             la lista de medidas, en JSON
    GET  /estaciones/<nombre>    una medida, o 404
    GET  /lenta?s=0.5            contesta después de s segundos
    GET  /eco, POST /eco         devuelve lo que le mandaste: método, consulta, cabeceras, cuerpo
    GET  /mover                  301 hacia /estaciones
    GET  /inestable?id=a&fallos=2   503 las primeras `fallos` veces para cada id; después, 200
    GET  /cuota?id=a             429 con "Retry-After: 1" la primera vez para cada id; después, 200
    GET  /conexiones             cuántas conexiones ha abierto el servidor hasta ahora
"""

import json
import threading
import time
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

STATIONS: dict[str, float | None] = {"norte": 12.5, "sur": 8.0, "centro": None}

calls: Counter[str] = Counter()
connections = 0


class Handler(BaseHTTPRequestHandler):
    # HTTP/1.1: la conexión queda abierta para la siguiente petición (keep-alive).
    protocol_version = "HTTP/1.1"

    def handle(self) -> None:
        global connections
        connections += 1
        super().handle()

    def log_message(self, format: str, *args: object) -> None:
        pass  # Sin una línea por petición en tu terminal.

    def do_GET(self) -> None:
        self.route()

    def do_POST(self) -> None:
        self.route()

    def send(
        self, status: int, body: object = None, headers: dict[str, str] | None = None
    ) -> None:
        data = b"" if body is None else json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(data)

    def route(self) -> None:
        url = urlsplit(self.path)
        query = {name: values[0] for name, values in parse_qs(url.query).items()}
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode() if length else ""
        key = query.get("id", "")
        match url.path.strip("/").split("/"):
            case ["estaciones"]:
                self.send(
                    200,
                    [
                        {"label": n.capitalize(), "value": v}
                        for n, v in STATIONS.items()
                    ],
                )
            case ["estaciones", name] if name in STATIONS:
                self.send(200, {"label": name.capitalize(), "value": STATIONS[name]})
            case ["lenta"]:
                seconds = float(query.get("s", "1"))
                time.sleep(seconds)
                self.send(200, {"espera": seconds})
            case ["eco"]:
                self.send(
                    200,
                    {
                        "method": self.command,
                        "query": query,
                        "user-agent": self.headers["User-Agent"],
                        "authorization": self.headers["Authorization"],
                        "body": body,
                    },
                )
            case ["mover"]:
                self.send(301, headers={"Location": "/estaciones"})
            case ["inestable"]:
                calls[f"inestable:{key}"] += 1
                if calls[f"inestable:{key}"] <= int(query.get("fallos", "2")):
                    self.send(503, {"error": "servidor saturado"})
                else:
                    self.send(200, {"intentos": calls[f"inestable:{key}"]})
            case ["cuota"]:
                calls[f"cuota:{key}"] += 1
                if calls[f"cuota:{key}"] == 1:
                    self.send(
                        429, {"error": "demasiadas peticiones"}, {"Retry-After": "1"}
                    )
                else:
                    self.send(200, {"intentos": calls[f"cuota:{key}"]})
            case ["conexiones"]:
                self.send(200, {"conexiones": connections})
            case _:
                self.send(404, {"error": "no existe"})


class QuietServer(ThreadingHTTPServer):
    def handle_error(self, request: object, client_address: object) -> None:
        pass  # Un cliente que se va sin esperar la respuesta no es un error del servidor.


def start() -> str:
    """Arranca el servidor en un hilo que muere con el programa y devuelve su dirección."""
    server = QuietServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}"
