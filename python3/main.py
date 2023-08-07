import os
import http.server

from functools import partial

from kvc import Cache, HTTPHandler

HOST = os.environ.get('MKV_HOST', "127.0.0.1")
PORT = int(os.environ.get('MKV_PORT', '9800'))
MAX_SIZE = int(os.environ.get('MKV_MAX_SIZE', '1000'))
MAX_MEMORY_USAGE = float(os.environ.get('MKV_MAX_MEMORY', '0.9'))
MAX_MEMORY_USAGE = int(MAX_MEMORY_USAGE) if int(MAX_MEMORY_USAGE) == MAX_MEMORY_USAGE else MAX_MEMORY_USAGE
KICK = True if os.environ.get('MKV_KICK', 'false').lower() == 'true' else False
VERIFY = True if os.environ.get('MKV_VERIFY', 'false').lower() == 'true' else False

cache = Cache(MAX_SIZE, KICK, VERIFY, MAX_MEMORY_USAGE)

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
