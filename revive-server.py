from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

from tradfri_hue_revive import main_auto_mode

from server_config import bridge_ip

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url.query))

    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self):
        self.handle_revive()

    def do_POST(self):
        self.handle_revive()

    def send_empty_response_with_code(self, code):
            self.send_response(code)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"")

    def handle_revive(self):
        path = self.url.path
        path_parts = path.split("/")
        if not len(path_parts) == 3 or not path_parts[1] == "revive":
            self.send_empty_response_with_code(400)
            return
        main_auto_mode(bridge_ip, path_parts[-1])
        self.send_empty_response_with_code(200)
        return


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
