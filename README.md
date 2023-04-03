# key-value caches using HTTP

Just trying out the same small project in different languages using as little to no packages.

## Usage

__configuration:__

- PORT
- MAX_SIZE => max cache size
- KICK => Kick items if cache full and you want to add another

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


# Progress

- __Python3:__ 100%
- __GO:__ 90%

# Performace

## Python 3.9

## Python 3.10

## Python 3.11


## GO