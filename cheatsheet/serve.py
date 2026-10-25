"""A static file server for the built site, used by `cheatsheet serve` and the browser tests."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A002 - signature from the base class
        pass


def make_server(directory: Path, port: int = 0) -> ThreadingHTTPServer:
    """Bind a server for `directory` on 127.0.0.1 (port 0 picks a free port); call serve_forever() to run it."""
    handler = partial(_QuietHandler, directory=str(directory))
    return ThreadingHTTPServer(("127.0.0.1", port), handler)
