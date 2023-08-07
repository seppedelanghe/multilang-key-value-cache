# key-value caches using HTTP

Just trying out the same small project in different languages using as little to no packages.

## Usage

__configuration:__

- PORT
- MAX_SIZE => max cache size
- KICK => Kick items if cache full and you want to add another
- VERIFY => Calculate hashes of body to allow for verification
- MAX_MEMORY => Max memory to use, float percentage (0.9) or int in bytes (Python only)

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