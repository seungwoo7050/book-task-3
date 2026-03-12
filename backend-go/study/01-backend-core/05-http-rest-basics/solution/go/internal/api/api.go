package api

import (
	"encoding/json"
	"errors"
	"net/http"
	"strconv"
	"sync"
	"time"
)

type Task struct {
	ID        int64     `json:"id"`
	Title     string    `json:"title"`
	CreatedAt time.Time `json:"created_at"`
}

type Server struct {
	mu               sync.Mutex
	nextID           int64
	tasks            []Task
	idempotentCreate map[string]Task
}

func NewServer() *Server {
	return &Server{
		nextID:           1,
		idempotentCreate: make(map[string]Task),
	}
}

func (s *Server) Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /v1/healthcheck", s.healthcheck)
	mux.HandleFunc("POST /v1/tasks", s.createTask)
	mux.HandleFunc("GET /v1/tasks", s.listTasks)
	mux.HandleFunc("GET /v1/tasks/{id}", s.showTask)
	return mux
}

func (s *Server) healthcheck(w http.ResponseWriter, _ *http.Request) {
	writeJSON(w, http.StatusOK, map[string]any{"status": "available"})
}

func (s *Server) createTask(w http.ResponseWriter, r *http.Request) {
	var input struct {
		Title string `json:"title"`
	}
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		writeError(w, http.StatusBadRequest, "invalid json")
		return
	}
	if input.Title == "" {
		writeError(w, http.StatusUnprocessableEntity, "title is required")
		return
	}

	s.mu.Lock()
	defer s.mu.Unlock()

	if key := r.Header.Get("Idempotency-Key"); key != "" {
		if existing, ok := s.idempotentCreate[key]; ok {
			writeJSON(w, http.StatusOK, map[string]any{"task": existing})
			return
		}
	}

	task := Task{
		ID:        s.nextID,
		Title:     input.Title,
		CreatedAt: time.Now().UTC(),
	}
	s.nextID++
	s.tasks = append(s.tasks, task)
	if key := r.Header.Get("Idempotency-Key"); key != "" {
		s.idempotentCreate[key] = task
	}

	writeJSON(w, http.StatusCreated, map[string]any{"task": task})
}

func (s *Server) listTasks(w http.ResponseWriter, r *http.Request) {
	page := parsePositiveInt(r.URL.Query().Get("page"), 1)
	pageSize := parsePositiveInt(r.URL.Query().Get("page_size"), 20)

	s.mu.Lock()
	defer s.mu.Unlock()

	start := (page - 1) * pageSize
	if start > len(s.tasks) {
		start = len(s.tasks)
	}
	end := start + pageSize
	if end > len(s.tasks) {
		end = len(s.tasks)
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"tasks": s.tasks[start:end],
		"meta": map[string]any{
			"page":      page,
			"page_size": pageSize,
			"total":     len(s.tasks),
		},
	})
}

func (s *Server) showTask(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseInt(r.PathValue("id"), 10, 64)
	if err != nil {
		writeError(w, http.StatusBadRequest, "invalid id")
		return
	}

	task, err := s.findTask(id)
	if errors.Is(err, errNotFound) {
		writeError(w, http.StatusNotFound, "task not found")
		return
	}
	if err != nil {
		writeError(w, http.StatusInternalServerError, "server error")
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"task": task})
}

var errNotFound = errors.New("not found")

func (s *Server) findTask(id int64) (Task, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, task := range s.tasks {
		if task.ID == id {
			return task, nil
		}
	}
	return Task{}, errNotFound
}

func parsePositiveInt(raw string, fallback int) int {
	if raw == "" {
		return fallback
	}
	value, err := strconv.Atoi(raw)
	if err != nil || value <= 0 {
		return fallback
	}
	return value
}

func writeJSON(w http.ResponseWriter, status int, payload map[string]any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func writeError(w http.ResponseWriter, status int, message string) {
	writeJSON(w, status, map[string]any{"error": map[string]string{"message": message}})
}
