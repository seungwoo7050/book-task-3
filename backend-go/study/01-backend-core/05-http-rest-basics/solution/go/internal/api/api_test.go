package api

import (
	"bytes"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHealthcheck(t *testing.T) {
	t.Parallel()

	req := httptest.NewRequest(http.MethodGet, "/v1/healthcheck", nil)
	rr := httptest.NewRecorder()

	NewServer().Routes().ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Fatalf("status = %d, want %d", rr.Code, http.StatusOK)
	}
}

func TestCreateTaskValidation(t *testing.T) {
	t.Parallel()

	req := httptest.NewRequest(http.MethodPost, "/v1/tasks", bytes.NewBufferString(`{"title":""}`))
	rr := httptest.NewRecorder()

	NewServer().Routes().ServeHTTP(rr, req)

	if rr.Code != http.StatusUnprocessableEntity {
		t.Fatalf("status = %d, want %d", rr.Code, http.StatusUnprocessableEntity)
	}
}

func TestCreateTaskIdempotency(t *testing.T) {
	t.Parallel()

	server := NewServer()
	body := []byte(`{"title":"write docs"}`)

	req1 := httptest.NewRequest(http.MethodPost, "/v1/tasks", bytes.NewReader(body))
	req1.Header.Set("Idempotency-Key", "abc")
	rr1 := httptest.NewRecorder()
	server.Routes().ServeHTTP(rr1, req1)

	req2 := httptest.NewRequest(http.MethodPost, "/v1/tasks", bytes.NewReader(body))
	req2.Header.Set("Idempotency-Key", "abc")
	rr2 := httptest.NewRecorder()
	server.Routes().ServeHTTP(rr2, req2)

	if rr1.Code != http.StatusCreated {
		t.Fatalf("first status = %d, want %d", rr1.Code, http.StatusCreated)
	}
	if rr2.Code != http.StatusOK {
		t.Fatalf("second status = %d, want %d", rr2.Code, http.StatusOK)
	}
}

func TestListTasksPagination(t *testing.T) {
	t.Parallel()

	server := NewServer()
	for _, title := range []string{"a", "b", "c"} {
		req := httptest.NewRequest(http.MethodPost, "/v1/tasks", bytes.NewBufferString(`{"title":"`+title+`"}`))
		rr := httptest.NewRecorder()
		server.Routes().ServeHTTP(rr, req)
	}

	req := httptest.NewRequest(http.MethodGet, "/v1/tasks?page=2&page_size=2", nil)
	rr := httptest.NewRecorder()
	server.Routes().ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Fatalf("status = %d, want %d", rr.Code, http.StatusOK)
	}
}

func TestShowTaskNotFound(t *testing.T) {
	t.Parallel()

	req := httptest.NewRequest(http.MethodGet, "/v1/tasks/999", nil)
	rr := httptest.NewRecorder()

	NewServer().Routes().ServeHTTP(rr, req)

	if rr.Code != http.StatusNotFound {
		t.Fatalf("status = %d, want %d", rr.Code, http.StatusNotFound)
	}
}
