package main

import (
	"bytes"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

var port = "9800"

type item struct {
	key   string
	value []byte
}

var cache = []item{}

func getKey(url string) (string, error) {
	s := strings.Split(url, "/")
	if len(s) != 2 {
		return "", errors.New("bad path")
	}

	return s[1], nil
}

func findKey(key string) (item, error) {
	for i := range cache {
		if cache[i].key == key {
			return cache[i], nil
		}
	}
	return item{}, errors.New("key not found")
}

func removeFromCache(key string) bool {
	for i := range cache {
		if cache[i].key == key {
			cache[i] = cache[len(cache)-1]
			cache = cache[:len(cache)-1]
			return true
		}
	}
	return false
}

func streamToByteArray(stream io.Reader) ([]byte, error) {
	buf := new(bytes.Buffer)
	_, read_err := buf.ReadFrom(stream)
	if read_err != nil {
		return []byte{}, errors.New("failed to read from stream")
	}
	return buf.Bytes(), nil
}

func get(w http.ResponseWriter, r *http.Request) {
	uuid, err := getKey(r.URL.Path)
	if err != nil {
		fmt.Printf("Error in url: %s\n", err)
		w.WriteHeader(404)
	} else {
		x, nf := findKey(uuid)
		if nf != nil {
			w.WriteHeader(404)
		} else {
			w.WriteHeader(200)
			w.Write(x.value)
		}
	}
}

func post(w http.ResponseWriter, r *http.Request) {
	uuid, err := getKey(r.URL.Path)
	if err != nil {
		fmt.Printf("Error in url: %s\n", err)
		w.WriteHeader(404)
	} else {
		x := new(item)
		x.key = uuid
		buf, rerr := streamToByteArray(r.Body)
		if rerr != nil {
			w.WriteHeader(500)
		} else {
			x.value = buf
			cache = append(cache, *x)
			w.WriteHeader(201)
		}
	}
}

func delete(w http.ResponseWriter, r *http.Request) {
	uuid, err := getKey(r.URL.Path)
	if err != nil {
		fmt.Printf("Error in url: %s\n", err)
		w.WriteHeader(404)
	} else {
		ok := removeFromCache(uuid)
		if !ok {
			w.WriteHeader(404)
		}
		w.WriteHeader(200)
	}
}

func handle(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		get(w, r)
	} else if r.Method == "POST" {
		post(w, r)
	} else if r.Method == "DELETE" {
		delete(w, r)
	} else {
		w.WriteHeader(405)
		r.Body.Close()
	}
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", handle)

	fmt.Printf("Running at: http://localhost:" + port + "\n")
	err := http.ListenAndServe(":"+port, mux)
	if errors.Is(err, http.ErrServerClosed) {
		fmt.Printf("server closed\n")
	} else if err != nil {
		fmt.Printf("error starting server: %s\n", err)
		os.Exit(1)
	}
}
