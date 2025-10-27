# app_b.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import time, os, tempfile

START_TIME = time.time()
STARTUP_GRACE_SECONDS = int(os.getenv("STARTUP_GRACE_SECONDS", "1"))
REQUIRE_DATA_RW = os.getenv("REQUIRE_DATA_RW", "false").lower() == "true"
DATA_PATH = os.getenv("DATA_PATH", "/app/data")

def readiness_ok() -> bool:
    # Opcional: valida que el PVC sea escribible si se pide
    if REQUIRE_DATA_RW:
        try:
            os.makedirs(DATA_PATH, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=DATA_PATH, delete=True) as _:
                pass
        except Exception:
            return False
    return True

class HolaBHandler(BaseHTTPRequestHandler):
    def _write(self, code: int, text: str, head_only: bool = False):
        body = text.encode("utf-8", "replace")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def do_HEAD(self):
        # Responde 200 en la raíz para checks ligeros
        path = self.path.split("?", 1)[0]
        if path in ("/", "/health"):
            return self._write(200, "OK - head", head_only=True)
        if path == "/readiness":
            return self._write(200 if readiness_ok() else 503, "readiness", head_only=True)
        if path == "/startup":
            ready = (time.time() - START_TIME) >= STARTUP_GRACE_SECONDS
            return self._write(200 if ready else 503, "startup", head_only=True)
        return self._write(404, "Not found", head_only=True)

    def do_GET(self):
        path = self.path.split("?", 1)[0]

        if path == "/startup":
            ready = (time.time() - START_TIME) >= STARTUP_GRACE_SECONDS
            return self._write(200 if ready else 503, "OK - startup" if ready else "Starting up...")

        if path == "/readiness":
            ok = readiness_ok()
            return self._write(200 if ok else 503, "OK - ready" if ok else "Not ready - data path not writable")

        if path == "/health":
            return self._write(200, "OK - healthy")

        # raíz: respuesta normal de B
        return self._write(200, "✅ Hola desde app B")

if __name__ == "__main__":
    server = HTTPServer(("", 8080), HolaBHandler)
    print("App B escuchando en :8080")
    server.serve_forever()