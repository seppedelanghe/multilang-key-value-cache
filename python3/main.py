import os
import http.server

from functools import partial

from kvc import Cache, HTTPHandler

HOST = "127.0.0.1"
PORT = 9800
MAX_SIZE = int(os.environ.get('MKV_MAX_SIZE', '1000'))
KICK = True if os.environ.get('MKV_KICK', 'false').lower() == 'true' else False
VERIFY = True if os.environ.get('MKV_VERIFY', 'false').lower() == 'true' else False

cache = Cache(MAX_SIZE, KICK, VERIFY)

def listen():
    handler = partial(HTTPHandler, cache)
    webServer = http.server.HTTPServer((HOST, PORT), handler)
    print("Server started http://%s:%s" % (HOST, PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
        

if __name__ == "__main__":
    listen()