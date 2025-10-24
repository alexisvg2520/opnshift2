# app_b.py
from http.server import BaseHTTPRequestHandler, HTTPServer

class HolaBHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"\xE2\x9C\x85 Hola desde app B (puerto 8080)"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    server = HTTPServer(("", 8080), HolaBHandler)
    print("App B escuchando")
    server.serve_forever()