from config import OUTPUT_PATH
from http.server import SimpleHTTPRequestHandler
import socketserver

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=OUTPUT_PATH, **kwargs)

def base_url(addr: str, port: int) -> str:
    return f'http://{addr}:{port}'

class Server(socketserver.TCPServer):
    allow_reuse_address = True

def serve_forever(addr: str, port: int):
    with Server((addr, port), Handler) as httpd:
        print(f'Serving at {base_url(addr, port)}')
        httpd.serve_forever()

