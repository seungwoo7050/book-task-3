// Starter skeleton for the Pipeline pattern.
// Implement the TODO items.
package pipeline

import "context"

// Generate produces integers from start to end (inclusive) on a channel.
// It must respect context cancellation.
func Generate(ctx context.Context, start, end int) <-chan int {
	// TODO: Create a channel, launch a goroutine that sends values,
	// and return the channel.
	return nil
}

// Filter reads from in and sends values that pass the predicate to the output channel.
// It must respect context cancellation.
func Filter(ctx context.Context, in <-chan int, predicate func(int) bool) <-chan int {
	// TODO: Create a channel, launch a goroutine that filters values,
	// and return the channel.
	return nil
}

// Sink collects all values from in into a slice.
// It must respect context cancellation.
func Sink(ctx context.Context, in <-chan int) []int {
	// TODO: Read all values from the channel into a slice.
	return nil
}
