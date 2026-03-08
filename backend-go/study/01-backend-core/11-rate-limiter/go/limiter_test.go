package ratelimiter

import (
	"context"
	"sync"
	"testing"
	"time"
)

func TestLimiterBasic(t *testing.T) {
	// 2 tokens/sec, burst of 3.
	l := NewLimiter(2, 3)

	tests := []struct {
		name string
		want bool
	}{
		{"first token", true},
		{"second token", true},
		{"third token", true},
		{"fourth token (empty)", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := l.Allow()
			if got != tt.want {
				t.Errorf("Allow() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestLimiterRefill(t *testing.T) {
	// 10 tokens/sec, burst of 2.
	l := NewLimiter(10, 2)

	// Drain the bucket.
	l.Allow()
	l.Allow()
	if l.Allow() {
		t.Error("expected bucket to be empty")
	}

	// Wait for refill (at 10/sec, 200ms should give ~2 tokens).
	time.Sleep(250 * time.Millisecond)

	if !l.Allow() {
		t.Error("expected token available after refill")
	}
}

func TestLimiterBurstCap(t *testing.T) {
	// 100 tokens/sec, burst of 5.
	l := NewLimiter(100, 5)

	// Wait a long time — tokens should cap at burst.
	time.Sleep(100 * time.Millisecond)

	// Should be able to consume exactly 5 tokens (burst cap).
	for i := 0; i < 5; i++ {
		if !l.Allow() {
			t.Errorf("expected token %d to be available", i+1)
		}
	}

	if l.Allow() {
		t.Error("expected no more tokens beyond burst capacity")
	}
}

func TestLimiterConcurrency(t *testing.T) {
	l := NewLimiter(1000, 100)

	var wg sync.WaitGroup
	var allowed, denied int64
	var mu sync.Mutex

	for i := 0; i < 200; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if l.Allow() {
				mu.Lock()
				allowed++
				mu.Unlock()
			} else {
				mu.Lock()
				denied++
				mu.Unlock()
			}
		}()
	}

	wg.Wait()

	total := allowed + denied
	if total != 200 {
		t.Errorf("expected 200 total calls, got %d", total)
	}

	// With burst=100 and 200 concurrent calls, most should be allowed
	// and some denied.
	if allowed == 0 {
		t.Error("expected some calls to be allowed")
	}
	if denied == 0 {
		t.Error("expected some calls to be denied")
	}
}

func TestClientLimiterBasic(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	cl := NewClientLimiter(ctx, 10, 2)

	// Client A: 2 tokens, then denied.
	if !cl.Allow("client-a") {
		t.Error("client-a first call should be allowed")
	}
	if !cl.Allow("client-a") {
		t.Error("client-a second call should be allowed")
	}
	if cl.Allow("client-a") {
		t.Error("client-a third call should be denied (bucket empty)")
	}

	// Client B: separate bucket, should be allowed.
	if !cl.Allow("client-b") {
		t.Error("client-b first call should be allowed")
	}
}

func TestClientLimiterCount(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	cl := NewClientLimiter(ctx, 10, 5)

	cl.Allow("a")
	cl.Allow("b")
	cl.Allow("c")

	if cl.ClientCount() != 3 {
		t.Errorf("expected 3 clients, got %d", cl.ClientCount())
	}
}

func BenchmarkLimiterAllow(b *testing.B) {
	l := NewLimiter(1000000, 1000000)

	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			l.Allow()
		}
	})
}

func BenchmarkClientLimiterAllow(b *testing.B) {
	ctx := context.Background()
	cl := NewClientLimiter(ctx, 1000000, 1000000)

	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		i := 0
		for pb.Next() {
			cl.Allow("client")
			i++
		}
	})
}
