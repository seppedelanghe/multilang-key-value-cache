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
var cache = make(map[string][]byte)

func getKey(url string) (string, error) {
	s := strings.Split(url, "/")
	if len(s) != 2 {
		return "", errors.New("bad path")
	}

	return s[1], nil
}

func streamToByteArray(stream io.Reader) ([]byte, error) {
	buf := new(bytes.Buffer)
	_, read_err := buf.ReadFrom(stream)
	if read_err != nil {
		return []byte{}, errors.New("failed to read from stream")
	}
	return buf.Bytes(), nil
}

func handleGet(w http.ResponseWriter, r *http.Request) {
	uuid, err := getKey(r.URL.Path)
	if err != nil {
		fmt.Printf("Error in url: %s\n", err)
		w.WriteHeader(404)
	} else {
		value, exists := cache[uuid]
		if exists {
			w.WriteHeader(200)
			w.Write(value)
		} else {
			w.WriteHeader(404)
		}
	}
}

func handlePost(w http.ResponseWriter, r *http.Request) {
	uuid, err := getKey(r.URL.Path)
	if err != nil {
		fmt.Printf("Error in url: %s\n", err)
		w.WriteHeader(404)
	} else {
		buf, rerr := streamToByteArray(r.Body)
		if rerr != nil {
			w.WriteHeader(500)
		} else {
			cache[uuid] = buf
			w.WriteHeader(201)
		}
	}
}

func handleDelete(w http.ResponseWriter, r *http.Request) {
	uuid, err := getKey(r.URL.Path)
	if err != nil {
		fmt.Printf("Error in url: %s\n", err)
		w.WriteHeader(404)
	} else {
		_, exists := cache[uuid]
		if exists {
			delete(cache, uuid)
			w.WriteHeader(200)
		} else {
			w.WriteHeader(404)
		}
	}
}

func handle(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		handleGet(w, r)
	} else if r.Method == "POST" {
		handlePost(w, r)
	} else if r.Method == "DELETE" {
		handleDelete(w, r)
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
