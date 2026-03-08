// Package pipeline implements the Generator → Filter → Sink pipeline pattern.
// Each stage runs in its own goroutine and communicates via channels.
// All stages respect context cancellation for prompt shutdown.
package pipeline

import "context"

// Generate produces integers from start to end (inclusive) on a channel.
// The output channel is closed when generation is complete or context is cancelled.
func Generate(ctx context.Context, start, end int) <-chan int {
	out := make(chan int)

	go func() {
		defer close(out)
		for i := start; i <= end; i++ {
			select {
			case <-ctx.Done():
				return
			case out <- i:
			}
		}
	}()

	return out
}

// Filter reads values from in and sends only those where predicate returns true.
// The output channel is closed when the input channel is closed or context is cancelled.
func Filter(ctx context.Context, in <-chan int, predicate func(int) bool) <-chan int {
	out := make(chan int)

	go func() {
		defer close(out)
		for val := range in {
			select {
			case <-ctx.Done():
				return
			default:
			}
			if predicate(val) {
				select {
				case out <- val:
				case <-ctx.Done():
					return
				}
			}
		}
	}()

	return out
}

// Sink collects all values from in into a slice and returns it.
// Returns partial results if the context is cancelled.
func Sink(ctx context.Context, in <-chan int) []int {
	var result []int

	for {
		select {
		case <-ctx.Done():
			return result
		case val, ok := <-in:
			if !ok {
				return result
			}
			result = append(result, val)
		}
	}
}

// FanOut distributes work from a single input channel to n output channels.
// Useful for parallelizing expensive filter/map operations.
func FanOut(ctx context.Context, in <-chan int, n int, worker func(int) int) <-chan int {
	out := make(chan int)
	done := make(chan struct{})

	for i := 0; i < n; i++ {
		go func() {
			defer func() { done <- struct{}{} }()
			for val := range in {
				select {
				case <-ctx.Done():
					return
				case out <- worker(val):
				}
			}
		}()
	}

	// Close out after all fan-out goroutines finish.
	go func() {
		for i := 0; i < n; i++ {
			<-done
		}
		close(out)
	}()

	return out
}
