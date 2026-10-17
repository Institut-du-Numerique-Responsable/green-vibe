// Fixture: conforming Go
package main

import (
	"context"
	"encoding/json"
	"net/http"
	"time"

	"golang.org/x/sync/errgroup"
)

var client = &http.Client{Timeout: 10 * time.Second}

func handler(ctx context.Context, urls []string) error {
	g, ctx := errgroup.WithContext(ctx)
	for _, u := range urls {
		g.Go(func() error { return fetch(ctx, u) })
	}
	return g.Wait()
}

func fetch(ctx context.Context, u string) error {
	req, err := http.NewRequestWithContext(ctx, "GET", u, nil)
	if err != nil {
		return err
	}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	var v map[string]any
	return json.NewDecoder(resp.Body).Decode(&v)
}
