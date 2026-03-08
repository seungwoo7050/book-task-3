package workerpool

import (
	"context"
	"errors"
	"sync/atomic"
	"testing"
	"time"
)

func TestPoolBasic(t *testing.T) {
	handler := func(j Job) Result {
		n := j.Payload.(int)
		return Result{JobID: j.ID, Value: n * 2}
	}

	ctx := context.Background()
	pool := NewPool(ctx, 4, handler)

	// Submit jobs.
	numJobs := 10
	go func() {
		for i := 0; i < numJobs; i++ {
			pool.Submit(Job{ID: i, Payload: i})
		}
		pool.Stop()
	}()

	// Collect results.
	var count int
	for result := range pool.Results() {
		if result.Err != nil {
			t.Errorf("unexpected error for job %d: %v", result.JobID, result.Err)
		}
		count++
	}

	if count != numJobs {
		t.Errorf("got %d results, want %d", count, numJobs)
	}
}

func TestPoolErrorPropagation(t *testing.T) {
	expectedErr := errors.New("processing failed")

	handler := func(j Job) Result {
		if j.ID%2 == 0 {
			return Result{JobID: j.ID, Err: expectedErr}
		}
		return Result{JobID: j.ID, Value: "ok"}
	}

	ctx := context.Background()
	pool := NewPool(ctx, 2, handler)

	go func() {
		for i := 0; i < 4; i++ {
			pool.Submit(Job{ID: i})
		}
		pool.Stop()
	}()

	var errCount int
	for result := range pool.Results() {
		if result.Err != nil {
			errCount++
		}
	}

	if errCount != 2 {
		t.Errorf("expected 2 errors, got %d", errCount)
	}
}

func TestPoolContextCancellation(t *testing.T) {
	var processed atomic.Int64

	handler := func(j Job) Result {
		time.Sleep(100 * time.Millisecond)
		processed.Add(1)
		return Result{JobID: j.ID}
	}

	ctx, cancel := context.WithCancel(context.Background())
	pool := NewPool(ctx, 2, handler)

	// Submit many jobs.
	go func() {
		for i := 0; i < 100; i++ {
			pool.Submit(Job{ID: i})
		}
	}()

	// Cancel quickly.
	time.Sleep(50 * time.Millisecond)
	cancel()

	// Drain results.
	for range pool.Results() {
	}

	// Should have processed far fewer than 100.
	p := processed.Load()
	if p >= 100 {
		t.Errorf("expected fewer than 100 processed jobs after cancel, got %d", p)
	}
}

func TestPoolNoGoroutineLeaks(t *testing.T) {
	handler := func(j Job) Result {
		return Result{JobID: j.ID, Value: j.Payload}
	}

	ctx := context.Background()
	pool := NewPool(ctx, 4, handler)

	for i := 0; i < 5; i++ {
		pool.Submit(Job{ID: i, Payload: i})
	}

	pool.Stop()

	// Drain remaining results.
	for range pool.Results() {
	}

	// If we reach here without hanging, goroutines have exited.
}

func BenchmarkPool(b *testing.B) {
	handler := func(j Job) Result {
		n := j.Payload.(int)
		return Result{JobID: j.ID, Value: n * n}
	}

	ctx := context.Background()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		pool := NewPool(ctx, 8, handler)

		go func() {
			for j := 0; j < 1000; j++ {
				pool.Submit(Job{ID: j, Payload: j})
			}
			pool.Stop()
		}()

		for range pool.Results() {
		}
	}
}
