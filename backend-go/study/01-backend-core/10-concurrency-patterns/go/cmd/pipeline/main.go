// Command pipeline demonstrates the pipeline pattern.
package main

import (
	"context"
	"fmt"

	"github.com/woopinbell/go-backend/study/01-backend-core/10-concurrency-patterns/pipeline"
)

func main() {
	ctx := context.Background()

	// Pipeline: Generate 1-50 → Filter primes → Collect.
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

	gen := pipeline.Generate(ctx, 1, 50)
	primes := pipeline.Filter(ctx, gen, isPrime)
	result := pipeline.Sink(ctx, primes)

	fmt.Printf("Primes from 1 to 50: %v\n", result)
	fmt.Printf("Count: %d\n", len(result))
}
