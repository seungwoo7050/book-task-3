package httpapi

import (
	"log/slog"
	"net/http"
	"sync"
	"time"
)

type statusRecorder struct {
	http.ResponseWriter
	status int
}

func (r *statusRecorder) WriteHeader(code int) {
	r.status = code
	r.ResponseWriter.WriteHeader(code)
}

// RateLimiter is a simple fixed-window request limiter.
type RateLimiter struct {
	mu        sync.Mutex
	limit     int
	window    time.Time
	requests  int
	windowDur time.Duration
}

// NewRateLimiter builds limiter by requests-per-second.
func NewRateLimiter(rps int) *RateLimiter {
	return &RateLimiter{
		limit:     rps,
		window:    time.Now(),
		windowDur: time.Second,
	}
}

// Allow reports whether current request is accepted.
func (l *RateLimiter) Allow() bool {
	l.mu.Lock()
	defer l.mu.Unlock()

	now := time.Now()
	if now.Sub(l.window) >= l.windowDur {
		l.window = now
		l.requests = 0
	}
	if l.requests >= l.limit {
		return false
	}
	l.requests++
	return true
}

func loggingMiddleware(next http.Handler, logger *slog.Logger) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		rec := &statusRecorder{ResponseWriter: w, status: http.StatusOK}
		next.ServeHTTP(rec, r)
		logger.Info(
			"http request",
			"method", r.Method,
			"path", r.URL.Path,
			"status", rec.status,
			"duration_ms", time.Since(start).Milliseconds(),
		)
	})
}

func rateLimitMiddleware(next http.Handler, limiter *RateLimiter) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if limiter != nil && !limiter.Allow() {
			writeJSON(w, http.StatusTooManyRequests, map[string]string{
				"error": "rate limit exceeded",
			})
			return
		}
		next.ServeHTTP(w, r)
	})
}
