package main

import (
	"bytes"
	"crypto/sha1"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
  "strconv"
)

func getEnv(key, fallback string) string {
  if value, ok := os.LookupEnv(key); ok {
    return value
  }
  return fallback
}

func getEnvVars() (string, int, bool) {
  port_str := getEnv("MKV_PORT", "9800")
  max_size_str := getEnv("MKV_MAX_SIZE", "10000")
  max_size, err := strconv.Atoi(max_size_str)
  if err != nil {
    fmt.Printf("Could not convert value of %s set as MAX_SIZE to interger", err)
  }

  verify_str := getEnv("MKV_VERIFY", "false")
  verify := false
  if strings.ToLower(verify_str) == "true" {
    verify = true
  }

  return port_str, max_size, verify
}

var port, max_size, verify = getEnvVars()
var cache = make(map[string][]byte, max_size)

type Payload struct {
	Hash string
}

func getKey(url string) (string, error) {
	s := strings.Split(url, "/")
	if len(s) != 2 {
		return "", errors.New("bad path")
	}

	return s[1], nil
}

func getRandomKey() string {
	for k := range cache {
		return k
	}
	return ""
}

func _verify(key string) string {
	data := cache[key]
	h := sha1.New()
	h.Write(data)
	return hex.EncodeToString(h.Sum(nil))
}

func streamToByteArray(stream io.Reader) ([]byte, error) {
	buf := new(bytes.Buffer)
	_, read_err := buf.ReadFrom(stream)
	if read_err != nil {
		return []byte{}, errors.New("failed to read from stream")
	}
	return buf.Bytes(), nil
}

func handleGet(w http.ResponseWriter, r *http.Request, uuid string) {
	value, exists := cache[uuid]
	if exists {
		w.WriteHeader(200)
		w.Write(value)
	} else {
		w.WriteHeader(404)
	}
}

func handlePost(w http.ResponseWriter, r *http.Request, uuid string) {
	buf, rerr := streamToByteArray(r.Body)
	if rerr != nil {
		w.WriteHeader(500)
	} else {
    if len(buf) == 0 {

      w.WriteHeader(422)
      return
    }

		if len(cache) >= max_size {
			rankey := getRandomKey()
			delete(cache, rankey)
		}

		cache[uuid] = buf
		payload := Payload{
			Hash: _verify(uuid),
		}
		if verify {
			json.NewEncoder(w).Encode(payload)
		} else {
			w.WriteHeader(201)
		}
	}
}

func handleDelete(w http.ResponseWriter, r *http.Request, uuid string) {
	_, exists := cache[uuid]
	if exists {
		delete(cache, uuid)
		w.WriteHeader(200)
	} else {
		w.WriteHeader(404)
	}
}

func validatePath(r *http.Request) (string, bool) {
	uuid, err := getKey(r.URL.Path)
	if err != nil {
		fmt.Printf("Error in url: %s\n", err)
		return "", false
	}
	return uuid, true
}

func handle(w http.ResponseWriter, r *http.Request) {
	uuid, ok := validatePath(r)
	if !ok {
		w.WriteHeader(404)
		return
	}

	if r.Method == "GET" {
		handleGet(w, r, uuid)
	} else if r.Method == "POST" {
		handlePost(w, r, uuid)
	} else if r.Method == "DELETE" {
		handleDelete(w, r, uuid)
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
