import os
import http.server

from functools import partial

from kvc import Cache, HTTPHandler
from kvc.config import KVCConfig

config = KVCConfig.from_env()
cache = Cache(config)

def listen():
    handler = partial(HTTPHandler, cache, config)
    webServer = http.server.HTTPServer((config.host, config.port), handler)
    print(f"Server started at: {config.url}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
        

if __name__ == "__main__":
    listen()
