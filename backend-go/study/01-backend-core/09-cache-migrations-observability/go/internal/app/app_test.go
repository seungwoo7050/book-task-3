package app

import (
	"bytes"
	"context"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func newService(t *testing.T) (*Service, func()) {
	t.Helper()
	db, err := OpenInMemory()
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	ctx := context.Background()
	if err := ApplyUpMigration(ctx, db); err != nil {
		t.Fatalf("up migration: %v", err)
	}
	if err := Seed(ctx, db); err != nil {
		t.Fatalf("seed: %v", err)
	}
	return NewService(db, NewTestLogger()), func() { db.Close() }
}

func TestCacheHitMiss(t *testing.T) {
	t.Parallel()

	service, cleanup := newService(t)
	defer cleanup()

	if _, err := service.GetItem(context.Background(), 1); err != nil {
		t.Fatalf("first get: %v", err)
	}
	if _, err := service.GetItem(context.Background(), 1); err != nil {
		t.Fatalf("second get: %v", err)
	}

	if service.metrics.cacheMisses.Load() != 1 {
		t.Fatalf("misses = %d, want 1", service.metrics.cacheMisses.Load())
	}
	if service.metrics.cacheHits.Load() != 1 {
		t.Fatalf("hits = %d, want 1", service.metrics.cacheHits.Load())
	}
}

func TestInvalidationOnUpdate(t *testing.T) {
	t.Parallel()

	service, cleanup := newService(t)
	defer cleanup()

	if _, err := service.GetItem(context.Background(), 1); err != nil {
		t.Fatalf("warm cache: %v", err)
	}
	if err := service.UpdateItem(context.Background(), Item{ID: 1, Name: "starter-axe"}); err != nil {
		t.Fatalf("update: %v", err)
	}
	item, err := service.GetItem(context.Background(), 1)
	if err != nil {
		t.Fatalf("reload: %v", err)
	}
	if item.Name != "starter-axe" {
		t.Fatalf("name = %q, want starter-axe", item.Name)
	}
	if service.metrics.cacheMisses.Load() != 2 {
		t.Fatalf("misses = %d, want 2", service.metrics.cacheMisses.Load())
	}
}

func TestMetricsEndpoint(t *testing.T) {
	t.Parallel()

	service, cleanup := newService(t)
	defer cleanup()

	req := httptest.NewRequest(http.MethodGet, "/metrics", nil)
	rr := httptest.NewRecorder()
	service.Routes().ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Fatalf("status = %d, want %d", rr.Code, http.StatusOK)
	}
	if !strings.Contains(rr.Body.String(), "cache_hits_total") {
		t.Fatalf("metrics body missing cache_hits_total: %s", rr.Body.String())
	}
}

func TestTraceHeader(t *testing.T) {
	t.Parallel()

	service, cleanup := newService(t)
	defer cleanup()

	req := httptest.NewRequest(http.MethodGet, "/v1/items/1", nil)
	req.Header.Set("X-Trace-ID", "trace-test")
	rr := httptest.NewRecorder()
	service.Routes().ServeHTTP(rr, req)

	if rr.Header().Get("X-Trace-ID") != "trace-test" {
		t.Fatalf("trace header = %q, want trace-test", rr.Header().Get("X-Trace-ID"))
	}
}

func TestUpdateEndpoint(t *testing.T) {
	t.Parallel()

	service, cleanup := newService(t)
	defer cleanup()

	req := httptest.NewRequest(http.MethodPut, "/v1/items/1", bytes.NewBufferString(`{"name":"starter-bow"}`))
	rr := httptest.NewRecorder()
	service.Routes().ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Fatalf("status = %d, want %d", rr.Code, http.StatusOK)
	}
}

func TestDownMigration(t *testing.T) {
	t.Parallel()

	db, err := OpenInMemory()
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	ctx := context.Background()
	if err := ApplyUpMigration(ctx, db); err != nil {
		t.Fatalf("up migration: %v", err)
	}
	if err := ApplyDownMigration(ctx, db); err != nil {
		t.Fatalf("down migration: %v", err)
	}
	if _, err := db.ExecContext(ctx, `SELECT * FROM items`); err == nil {
		t.Fatal("expected table to be gone after down migration")
	}
}
