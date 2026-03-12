package pipeline

import "context"

func Generate(ctx context.Context, start, end int) <-chan int {
	return nil
}
func Filter(ctx context.Context, in <-chan int, predicate func(int) bool) <-chan int {
	return nil
}
func Sink(ctx context.Context, in <-chan int) []int {
	return nil
}
