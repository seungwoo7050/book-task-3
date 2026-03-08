package pipeline

import (
	"context"
	"sort"
	"testing"
	"time"
)

func TestGenerateBasic(t *testing.T) {
	ctx := context.Background()
	ch := Generate(ctx, 1, 5)

	var got []int
	for v := range ch {
		got = append(got, v)
	}

	want := []int{1, 2, 3, 4, 5}
	if len(got) != len(want) {
		t.Fatalf("got %d values, want %d", len(got), len(want))
	}
	for i, v := range got {
		if v != want[i] {
			t.Errorf("got[%d] = %d, want %d", i, v, want[i])
		}
	}
}

func TestGenerateContextCancel(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())

	ch := Generate(ctx, 1, 1_000_000)

	// Read a few values then cancel.
	<-ch
	<-ch
	cancel()

	// Drain remaining — should be short.
	count := 2
	for range ch {
		count++
	}

	if count >= 1_000_000 {
		t.Errorf("expected early termination, got %d values", count)
	}
}

func TestFilterEvenNumbers(t *testing.T) {
	ctx := context.Background()
	isEven := func(n int) bool { return n%2 == 0 }

	gen := Generate(ctx, 1, 10)
	filtered := Filter(ctx, gen, isEven)
	result := Sink(ctx, filtered)

	want := []int{2, 4, 6, 8, 10}
	if len(result) != len(want) {
		t.Fatalf("got %d values, want %d", len(result), len(want))
	}
	for i, v := range result {
		if v != want[i] {
			t.Errorf("result[%d] = %d, want %d", i, v, want[i])
		}
	}
}

func TestFullPipeline(t *testing.T) {
	ctx := context.Background()

	// Generate 1-20, filter primes, collect.
	isPrime := func(n int) bool {
		if n < 2 {
			return false
		}
		for i := 2; i*i <= n; i++ {
			if n%i == 0 {
				return false
			}
		}
		return true
	}

	gen := Generate(ctx, 1, 20)
	primes := Filter(ctx, gen, isPrime)
	result := Sink(ctx, primes)

	want := []int{2, 3, 5, 7, 11, 13, 17, 19}
	if len(result) != len(want) {
		t.Fatalf("got %d primes, want %d: %v", len(result), len(want), result)
	}
}

func TestPipelineTimeout(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	// Generate a huge range — should be cut short by timeout.
	gen := Generate(ctx, 1, 100_000_000)
	identity := func(n int) bool { return true }
	filtered := Filter(ctx, gen, identity)
	result := Sink(ctx, filtered)

	// Should have collected some but not all values.
	if len(result) >= 100_000_000 {
		t.Errorf("expected timeout to cut pipeline short, got %d values", len(result))
	}
}

func TestFanOut(t *testing.T) {
	ctx := context.Background()
	gen := Generate(ctx, 1, 10)

	double := func(n int) int { return n * 2 }
	out := FanOut(ctx, gen, 3, double)

	var results []int
	for v := range out {
		results = append(results, v)
	}

	sort.Ints(results)
	want := []int{2, 4, 6, 8, 10, 12, 14, 16, 18, 20}
	if len(results) != len(want) {
		t.Fatalf("got %d results, want %d", len(results), len(want))
	}
	for i, v := range results {
		if v != want[i] {
			t.Errorf("results[%d] = %d, want %d", i, v, want[i])
		}
	}
}

func BenchmarkPipeline(b *testing.B) {
	isEven := func(n int) bool { return n%2 == 0 }

	for i := 0; i < b.N; i++ {
		ctx := context.Background()
		gen := Generate(ctx, 1, 10000)
		filtered := Filter(ctx, gen, isEven)
		_ = Sink(ctx, filtered)
	}
}

func BenchmarkFanOut(b *testing.B) {
	double := func(n int) int { return n * 2 }

	for i := 0; i < b.N; i++ {
		ctx := context.Background()
		gen := Generate(ctx, 1, 10000)
		out := FanOut(ctx, gen, 4, double)
		for range out {
		}
	}
}
