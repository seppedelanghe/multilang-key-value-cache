import json
import http.server

from .config import KVCConfig

from .cache import Cache

class HTTPHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, cache: Cache, config: KVCConfig, *args, **kwargs):
        self.cache = cache
        self.config = config
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
        content_length = self.headers.get('Content-Length', '0')
        l = int(content_length)
        return self.rfile.read(l)

    def do_HEAD(self):
        self._send_headers()
        
    def do_GET(self):
        key = self._get_key()
        if not key:
            return

        value = self.cache[key]
        if value is None:
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
        if not self.config.allow_empty_body and len(body) == 0:
            self._send_headers(422)
            self._write_dict({
                'message': 'Body is empty, cannot set empty body!'
            })
            self.wfile.flush()
            return

        ok, hexdigest = self.cache.set(key, body)
        if ok:
            self._send_headers(201)
            if isinstance(hexdigest, str):
                self._write_dict({
                    'hash': hexdigest
                })
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
