// Package ratelimiter는 토큰 버킷 기반 rate limiter를 구현한다.
package ratelimiter

import (
	"context"
	"sync"
	"time"
)

// Limiter는 단일 키에 대한 토큰 버킷 상태를 보관한다.
type Limiter struct {
	mu       sync.Mutex
	rate     float64   // 초당 재충전 토큰 수
	burst    int       // 버킷 최대 용량
	tokens   float64   // 현재 남아 있는 토큰 수
	lastTime time.Time // 마지막 토큰 계산 시각
}

// NewLimiter는 재충전 속도와 burst 용량으로 Limiter를 생성한다.
func NewLimiter(rate float64, burst int) *Limiter {
	return &Limiter{
		rate:     rate,
		burst:    burst,
		tokens:   float64(burst), // 시작 시점에는 토큰을 가득 채운다.
		lastTime: time.Now(),
	}
}

// Allow는 토큰 1개를 소비할 수 있으면 true를 반환한다.
func (l *Limiter) Allow() bool {
	l.mu.Lock()
	defer l.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(l.lastTime).Seconds()
	l.lastTime = now

	// 경과 시간만큼 토큰을 재충전한다.
	l.tokens += elapsed * l.rate
	if l.tokens > float64(l.burst) {
		l.tokens = float64(l.burst)
	}

	// 토큰이 하나 이상이면 요청을 허용한다.
	if l.tokens >= 1.0 {
		l.tokens -= 1.0
		return true
	}
	return false
}

// Tokens는 현재 추정 토큰 수를 반환한다.
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

// client는 개별 키의 limiter와 마지막 접근 시각을 묶는다.
type client struct {
	limiter  *Limiter
	lastSeen time.Time
}

// ClientLimiter는 문자열 키별 Limiter를 관리하고 오래된 엔트리를 정리한다.
type ClientLimiter struct {
	mu      sync.Mutex
	clients map[string]*client
	rate    float64
	burst   int
	ttl     time.Duration // 이 시간 동안 접근이 없으면 오래된 엔트리로 간주한다.
}

// NewClientLimiter는 키별 Limiter를 생성하고 정리 goroutine을 시작한다.
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

// Allow는 지정한 키의 요청을 허용할지 확인한다.
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

// cleanup은 TTL보다 오래된 키를 제거한다.
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

// ClientCount는 현재 추적 중인 키 수를 반환한다.
func (cl *ClientLimiter) ClientCount() int {
	cl.mu.Lock()
	defer cl.mu.Unlock()
	return len(cl.clients)
}
