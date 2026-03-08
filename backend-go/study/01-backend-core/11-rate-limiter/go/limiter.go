// Package ratelimiter implements a Token Bucket rate limiter with per-client
// tracking and automatic cleanup of stale entries.
package ratelimiter

import (
	"context"
	"sync"
	"time"
)

// Limiter implements the Token Bucket algorithm.
// It is safe for concurrent use.
type Limiter struct {
	mu       sync.Mutex
	rate     float64   // tokens per second
	burst    int       // maximum tokens (bucket capacity)
	tokens   float64   // current token count
	lastTime time.Time // last time tokens were calculated
}

// NewLimiter creates a Limiter with the given refill rate (tokens per second)
// and burst capacity. The bucket starts full.
func NewLimiter(rate float64, burst int) *Limiter {
	return &Limiter{
		rate:     rate,
		burst:    burst,
		tokens:   float64(burst), // start full
		lastTime: time.Now(),
	}
}

// Allow reports whether an event may happen now. It consumes one token if
// available. Returns false if no tokens remain.
func (l *Limiter) Allow() bool {
	l.mu.Lock()
	defer l.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(l.lastTime).Seconds()
	l.lastTime = now

	// Refill tokens based on elapsed time.
	l.tokens += elapsed * l.rate
	if l.tokens > float64(l.burst) {
		l.tokens = float64(l.burst)
	}

	// Try to consume one token.
	if l.tokens >= 1.0 {
		l.tokens -= 1.0
		return true
	}
	return false
}

// Tokens returns the current approximate token count (for testing/debugging).
func (l *Limiter) Tokens() float64 {
	l.mu.Lock()
	defer l.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(l.lastTime).Seconds()

	tokens := l.tokens + elapsed*l.rate
	if tokens > float64(l.burst) {
		tokens = float64(l.burst)
	}
	return tokens
}

// client holds a limiter and the last time it was seen, for cleanup purposes.
type client struct {
	limiter  *Limiter
	lastSeen time.Time
}

// ClientLimiter maintains per-client Limiter instances identified by a string
// key (typically an IP address). Stale clients are automatically purged.
type ClientLimiter struct {
	mu      sync.Mutex
	clients map[string]*client
	rate    float64
	burst   int
	ttl     time.Duration // how long before a client is considered stale
}

// NewClientLimiter creates a ClientLimiter that assigns each client a limiter
// with the given rate and burst. It starts a background goroutine that purges
// clients inactive for more than 3 minutes. The goroutine exits when ctx is
// cancelled.
func NewClientLimiter(ctx context.Context, rate float64, burst int) *ClientLimiter {
	cl := &ClientLimiter{
		clients: make(map[string]*client),
		rate:    rate,
		burst:   burst,
		ttl:     3 * time.Minute,
	}

	go cl.cleanup(ctx)
	return cl
}

// Allow checks whether the client identified by key is allowed to proceed.
// A new limiter is created for first-time clients.
func (cl *ClientLimiter) Allow(key string) bool {
	cl.mu.Lock()
	c, exists := cl.clients[key]
	if !exists {
		c = &client{
			limiter: NewLimiter(cl.rate, cl.burst),
		}
		cl.clients[key] = c
	}
	c.lastSeen = time.Now()
	cl.mu.Unlock()

	return c.limiter.Allow()
}

// cleanup periodically removes clients that have not been seen within the TTL.
func (cl *ClientLimiter) cleanup(ctx context.Context) {
	ticker := time.NewTicker(1 * time.Minute)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			cl.mu.Lock()
			now := time.Now()
			for key, c := range cl.clients {
				if now.Sub(c.lastSeen) > cl.ttl {
					delete(cl.clients, key)
				}
			}
			cl.mu.Unlock()
		}
	}
}

// ClientCount returns the number of tracked clients (for testing).
func (cl *ClientLimiter) ClientCount() int {
	cl.mu.Lock()
	defer cl.mu.Unlock()
	return len(cl.clients)
}
