import json
import http.server

from .cache import Cache

class HTTPHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, cache: Cache, *args, **kwargs):
        self.cache = cache
        super().__init__(*args, **kwargs)

    def _send_headers(self, code: int = 200):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _get_key(self):
        p = self.path.split('/')
        if len(p) == 2:
            return p[1]

        self._send_headers(404)
        self._write_dict({
            'message': 'Bad url!'
        })
        self.wfile.flush()
        return None
    
    def _write_dict(self, data: dict):
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _get_body(self) -> bytes:
        l = int(self.headers.get('Content-Length'))
        return self.rfile.read(l)

    def do_HEAD(self):
        self._send_headers()
        
    def do_GET(self):
        key = self._get_key()
        if not key:
            return

        value = self.cache.get(key)
        if not value:
            self._send_headers(404)
            self._write_dict({
                'message': 'Key not found!'
            })
            self.wfile.flush()
            return
        
        self._send_headers(200)
        self.wfile.write(value)
        self.wfile.flush()

    def do_POST(self):
        key = self._get_key()
        if not key:
            return
        
        body = self._get_body()

        ok = self.cache.set(key, body)
        if ok:
            self._send_headers(201)
            self.wfile.flush()
            return
        
        self._send_headers(409)
        self._write_dict({
            'message': 'Cache is full!'
        })
        self.wfile.flush()

    def do_DELETE(self):
        key = self._get_key()
        if not key:
            return
        
        ok = self.cache.drop(key)
        if ok:
            self._send_headers(201)
            self.wfile.flush()
            return
        
        self._send_headers(404)
        self._write_dict({
            'message': 'Key not found!'
        })
        self.wfile.flush()

    # disable request logging => 2ms speed improvement for storing, 0.5 ms for getting
    def log_message(self, format, *args):
        return
