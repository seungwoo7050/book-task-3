package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard/internal/data"

	"log/slog"
)

// newTestApp returns an application instance configured for testing.
func newTestApp() *application {
	logger := slog.New(slog.NewTextHandler(&bytes.Buffer{}, nil))
	return &application{
		config: config{port: 4000, env: "testing"},
		logger: logger,
		models: data.NewModels(),
	}
}

func TestHealthcheckHandler(t *testing.T) {
	app := newTestApp()

	tests := []struct {
		name       string
		method     string
		path       string
		wantStatus int
		wantBody   string
	}{
		{
			name:       "valid healthcheck",
			method:     http.MethodGet,
			path:       "/v1/healthcheck",
			wantStatus: http.StatusOK,
			wantBody:   "available",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(tt.method, tt.path, nil)
			rr := httptest.NewRecorder()

			app.routes().ServeHTTP(rr, req)

			if rr.Code != tt.wantStatus {
				t.Errorf("got status %d, want %d", rr.Code, tt.wantStatus)
			}

			if tt.wantBody != "" && !bytes.Contains(rr.Body.Bytes(), []byte(tt.wantBody)) {
				t.Errorf("body does not contain %q: %s", tt.wantBody, rr.Body.String())
			}
		})
	}
}

func TestCreateMovieHandler(t *testing.T) {
	app := newTestApp()

	tests := []struct {
		name       string
		body       map[string]any
		wantStatus int
	}{
		{
			name: "valid movie",
			body: map[string]any{
				"title":   "Moana",
				"year":    2016,
				"runtime": 107,
				"genres":  []string{"animation", "adventure"},
			},
			wantStatus: http.StatusCreated,
		},
		{
			name: "missing title",
			body: map[string]any{
				"year":    2016,
				"runtime": 107,
				"genres":  []string{"animation"},
			},
			wantStatus: http.StatusUnprocessableEntity,
		},
		{
			name: "year too low",
			body: map[string]any{
				"title":   "Early Film",
				"year":    1800,
				"runtime": 10,
				"genres":  []string{"drama"},
			},
			wantStatus: http.StatusUnprocessableEntity,
		},
		{
			name: "negative runtime",
			body: map[string]any{
				"title":   "Bad Movie",
				"year":    2020,
				"runtime": -5,
				"genres":  []string{"horror"},
			},
			wantStatus: http.StatusUnprocessableEntity,
		},
		{
			name: "no genres",
			body: map[string]any{
				"title":   "No Genre Movie",
				"year":    2020,
				"runtime": 90,
				"genres":  []string{},
			},
			wantStatus: http.StatusUnprocessableEntity,
		},
		{
			name:       "empty body",
			body:       nil,
			wantStatus: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var bodyBytes []byte
			if tt.body != nil {
				bodyBytes, _ = json.Marshal(tt.body)
			}
			req := httptest.NewRequest(http.MethodPost, "/v1/movies", bytes.NewReader(bodyBytes))
			req.Header.Set("Content-Type", "application/json")
			rr := httptest.NewRecorder()

			app.routes().ServeHTTP(rr, req)

			if rr.Code != tt.wantStatus {
				t.Errorf("got status %d, want %d; body: %s", rr.Code, tt.wantStatus, rr.Body.String())
			}
		})
	}
}

func TestShowMovieHandler(t *testing.T) {
	app := newTestApp()

	// Seed a movie.
	movie := &data.Movie{Title: "Inception", Year: 2010, Runtime: 148, Genres: []string{"sci-fi"}}
	app.models.Movies.Insert(movie)

	tests := []struct {
		name       string
		path       string
		wantStatus int
	}{
		{
			name:       "existing movie",
			path:       "/v1/movies/1",
			wantStatus: http.StatusOK,
		},
		{
			name:       "non-existing movie",
			path:       "/v1/movies/999",
			wantStatus: http.StatusNotFound,
		},
		{
			name:       "invalid id",
			path:       "/v1/movies/abc",
			wantStatus: http.StatusNotFound,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodGet, tt.path, nil)
			rr := httptest.NewRecorder()

			app.routes().ServeHTTP(rr, req)

			if rr.Code != tt.wantStatus {
				t.Errorf("got status %d, want %d", rr.Code, tt.wantStatus)
			}
		})
	}
}

func TestDeleteMovieHandler(t *testing.T) {
	app := newTestApp()

	movie := &data.Movie{Title: "Temp Movie", Year: 2020, Runtime: 90, Genres: []string{"drama"}}
	app.models.Movies.Insert(movie)

	tests := []struct {
		name       string
		path       string
		wantStatus int
	}{
		{
			name:       "delete existing movie",
			path:       "/v1/movies/1",
			wantStatus: http.StatusOK,
		},
		{
			name:       "delete non-existing movie",
			path:       "/v1/movies/999",
			wantStatus: http.StatusNotFound,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodDelete, tt.path, nil)
			rr := httptest.NewRecorder()

			app.routes().ServeHTTP(rr, req)

			if rr.Code != tt.wantStatus {
				t.Errorf("got status %d, want %d", rr.Code, tt.wantStatus)
			}
		})
	}
}
