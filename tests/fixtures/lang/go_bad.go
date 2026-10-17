// Fixture: non-conforming Go
package main

import (
	"io"
	"net/http"
	"time"
)

func handler(urls []string) {
	for _, u := range urls {
		go func() { fetch(u) }()
	}
	for {
		time.Sleep(time.Second)
	}
}

func fetch(u string) []byte {
	client := &http.Client{}
	req, _ := http.NewRequest("GET", u, nil)
	resp, _ := client.Do(req)
	b, _ := io.ReadAll(resp.Body)
	return b
}
