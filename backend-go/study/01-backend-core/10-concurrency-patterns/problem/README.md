# Problem: Concurrency Patterns

## Objective

Implement two fundamental Go concurrency patterns and demonstrate mastery of
goroutine lifecycle management, channel communication, and context-based
cancellation.

## Part 1: Worker Pool

### Requirements

1. Implement a `Pool` that manages `N` worker goroutines.
2. The pool accepts `Job` values through a submission channel.
3. Each worker processes jobs concurrently and sends results to a results channel.
4. The pool must support:
   - **Graceful shutdown**: `Stop()` waits for all in-flight jobs to complete.
   - **Context cancellation**: If the context is cancelled, workers stop promptly.
   - **Error propagation**: Failed jobs report errors without crashing the pool.
5. The pool must not leak goroutines after `Stop()` returns.

### Interface

```go
type Job struct {
    ID      int
    Payload any
}

type Result struct {
    JobID int
    Value any
    Err   error
}

type Pool struct { ... }

func NewPool(ctx context.Context, workers int, handler func(Job) Result) *Pool
func (p *Pool) Submit(job Job)
func (p *Pool) Results() <-chan Result
func (p *Pool) Stop()
```

## Part 2: Pipeline

### Requirements

1. Implement a three-stage pipeline: **Generator → Filter → Sink**.
2. **Generator**: Produces integers from 1 to N.
3. **Filter**: Passes through only values where `predicate(value)` returns true.
4. **Sink**: Collects all values into a slice.
5. Each stage runs in its own goroutine(s).
6. All stages must respect context cancellation (early exit if cancelled).
7. Channels must be properly closed when a stage completes.

### Interface

```go
func Generate(ctx context.Context, start, end int) <-chan int
func Filter(ctx context.Context, in <-chan int, predicate func(int) bool) <-chan int
func Sink(ctx context.Context, in <-chan int) []int
```

## Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Correctness | 30% | All patterns work as specified |
| No goroutine leaks | 25% | All goroutines exit cleanly |
| Context support | 20% | Cancellation and timeouts are respected |
| Benchmarks | 15% | Benchmark tests demonstrate throughput |
| Code clarity | 10% | Clean, idiomatic Go |
