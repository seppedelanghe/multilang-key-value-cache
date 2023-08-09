# key-value caches over HTTP

## Usage

### Configuration:
Configure them as environment variables

- MKV_HOST
- MKV_PORT
- MKV_MAX_SIZE => max cache size
- MKV_KICK => Kick items if cache full and you want to add another
- MKV_VERIFY => Calculate hashes of body to allow for verification
- MKV_MAX_MEMORY => Max memory to use, float percentage (0.9) or int in bytes (Python only)


If you want to use the `MAX_MEMORY` flag you may require one or more packages. If these packages are not installed, the server will still start, the `MAX_MEMORY` flag will just be ignored.

- Python:
    - psutil

__Starting server:__
```sh
# python
python3 python3/main.py

# GO
go run go/main.go
```

__Routes:__

`/{key}`
- GET
    - get value for key if it exists
- POST
    - set a value for a key
- DELETE
    - delete the key from the cache


# Todo

- __Python3:__ 100%
- __GO:__ 
    - Max memory

# Docker
Run in a docker container.


### Python
```bash
cd python3
docker build -t mkv:python3 . 
docker run -p 9800:9800 -t mkv:python3
```

### Go
```bash
cd go
docker build -t mkv:go .
docker run -p 9800:9800 -t mkv:go
```