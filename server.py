from threading import Thread
from typing import Callable, Tuple
from config import Config
from http.server import SimpleHTTPRequestHandler
import socketserver


def base_url(addr: str, port: int) -> str:
    return f"http://{addr}:{port}"


class Server(socketserver.TCPServer):
    allow_reuse_address = True


def serve_forever(addr: str, port: int, config: Config):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=config.output_path, **kwargs)

    with Server((addr, port), Handler) as httpd:
        print(f"Serving at {base_url(addr, port)}")
        httpd.serve_forever()


def serve_until(
    addr: str, port: int, config: Config, keep_running_func: Callable[[], bool]
) -> Tuple[Thread, Server]:
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=config.output_path, **kwargs)

    httpd = Server((addr, port), Handler)

    def serve(httpd):
        with httpd:
            print(f"Serving at {base_url(addr, port)}")
            httpd.serve_forever()
            print("Stopped.")

    thread = Thread(target=serve, args=[httpd])
    thread.start()
    return thread, httpd
