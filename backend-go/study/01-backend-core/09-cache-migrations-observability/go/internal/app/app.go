package app

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"log/slog"
	"math/rand"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	_ "modernc.org/sqlite"
)

const upMigration = `
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
`

const downMigration = `DROP TABLE IF EXISTS items;`

type Item struct {
	ID      int64  `json:"id"`
	Name    string `json:"name"`
	Version int    `json:"version"`
}

type Metrics struct {
	cacheHits   atomic.Int64
	cacheMisses atomic.Int64
	writes      atomic.Int64
}

type Service struct {
	db      *sql.DB
	logger  *slog.Logger
	mu      sync.Mutex
	cache   map[int64]Item
	metrics Metrics
}

func OpenInMemory() (*sql.DB, error) {
	return sql.Open("sqlite", fmt.Sprintf("file:cache-observability-%d?mode=memory&cache=shared", time.Now().UnixNano()))
}

func ApplyUpMigration(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, upMigration)
	return err
}

func ApplyDownMigration(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, downMigration)
	return err
}

func Seed(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, `
INSERT INTO items(id, name, version) VALUES
    (1, 'starter-sword', 1),
    (2, 'healing-potion', 1)
`)
	return err
}

func NewService(db *sql.DB, logger *slog.Logger) *Service {
	if logger == nil {
		logger = slog.Default()
	}
	return &Service{
		db:     db,
		logger: logger,
		cache:  make(map[int64]Item),
	}
}

func (s *Service) Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /v1/items/{id}", s.withTrace(s.showItem))
	mux.HandleFunc("PUT /v1/items/{id}", s.withTrace(s.updateItem))
	mux.HandleFunc("GET /metrics", s.metricsHandler)
	return mux
}

func (s *Service) GetItem(ctx context.Context, id int64) (Item, error) {
	s.mu.Lock()
	if item, ok := s.cache[id]; ok {
		s.mu.Unlock()
		s.metrics.cacheHits.Add(1)
		return item, nil
	}
	s.mu.Unlock()

	s.metrics.cacheMisses.Add(1)
	var item Item
	err := s.db.QueryRowContext(ctx, `SELECT id, name, version FROM items WHERE id = ?`, id).
		Scan(&item.ID, &item.Name, &item.Version)
	if errors.Is(err, sql.ErrNoRows) {
		return Item{}, errors.New("item not found")
	}
	if err != nil {
		return Item{}, err
	}

	s.mu.Lock()
	s.cache[id] = item
	s.mu.Unlock()
	return item, nil
}

func (s *Service) UpdateItem(ctx context.Context, item Item) error {
	_, err := s.db.ExecContext(ctx, `
UPDATE items
SET name = ?, version = version + 1
WHERE id = ?
`, item.Name, item.ID)
	if err != nil {
		return err
	}

	s.mu.Lock()
	delete(s.cache, item.ID)
	s.mu.Unlock()
	s.metrics.writes.Add(1)
	return nil
}

func (s *Service) showItem(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseInt(r.PathValue("id"), 10, 64)
	if err != nil {
		writeError(w, http.StatusBadRequest, "invalid id")
		return
	}
	item, err := s.GetItem(r.Context(), id)
	if err != nil {
		writeError(w, http.StatusNotFound, "item not found")
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"item": item})
}

func (s *Service) updateItem(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseInt(r.PathValue("id"), 10, 64)
	if err != nil {
		writeError(w, http.StatusBadRequest, "invalid id")
		return
	}
	var input struct {
		Name string `json:"name"`
	}
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil || strings.TrimSpace(input.Name) == "" {
		writeError(w, http.StatusBadRequest, "invalid body")
		return
	}
	if err := s.UpdateItem(r.Context(), Item{ID: id, Name: input.Name}); err != nil {
		writeError(w, http.StatusInternalServerError, "update failed")
		return
	}
	item, err := s.GetItem(r.Context(), id)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "reload failed")
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"item": item})
}

func (s *Service) metricsHandler(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-Type", "text/plain; version=0.0.4")
	_, _ = fmt.Fprintf(w, "cache_hits_total %d\ncache_misses_total %d\nwrites_total %d\n",
		s.metrics.cacheHits.Load(),
		s.metrics.cacheMisses.Load(),
		s.metrics.writes.Load(),
	)
}

func (s *Service) withTrace(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		traceID := r.Header.Get("X-Trace-ID")
		if traceID == "" {
			traceID = fmt.Sprintf("trace-%d", rand.Int63())
		}
		w.Header().Set("X-Trace-ID", traceID)
		s.logger.Info("request", "trace_id", traceID, "method", r.Method, "path", r.URL.Path)
		next(w, r)
	}
}

func writeJSON(w http.ResponseWriter, status int, payload map[string]any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func writeError(w http.ResponseWriter, status int, message string) {
	writeJSON(w, status, map[string]any{"error": map[string]string{"message": message}})
}

func NewTestLogger() *slog.Logger {
	return slog.New(slog.NewTextHandler(&discardWriter{}, nil))
}

type discardWriter struct{}

func (discardWriter) Write(p []byte) (int, error) {
	return len(p), nil
}

func init() {
	rand.Seed(time.Now().UnixNano())
}
