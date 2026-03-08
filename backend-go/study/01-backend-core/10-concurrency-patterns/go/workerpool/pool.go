// Package workerpool implements a concurrent worker pool pattern.
// Workers pull jobs from a shared channel, process them, and send results
// to a results channel. The pool supports graceful shutdown and context
// cancellation.
package workerpool

import (
	"context"
	"sync"
)

// Job represents a unit of work to be processed by the pool.
type Job struct {
	ID      int
	Payload any
}

// Result holds the outcome of processing a Job.
type Result struct {
	JobID int
	Value any
	Err   error
}

// Pool manages a set of worker goroutines that process jobs concurrently.
type Pool struct {
	ctx     context.Context
	cancel  context.CancelFunc
	jobs    chan Job
	results chan Result
	handler func(Job) Result
	wg      sync.WaitGroup
}

// NewPool creates a worker pool with the specified number of workers.
// The handler function is invoked for each job. Workers start immediately.
func NewPool(ctx context.Context, workers int, handler func(Job) Result) *Pool {
	ctx, cancel := context.WithCancel(ctx)

	p := &Pool{
		ctx:     ctx,
		cancel:  cancel,
		jobs:    make(chan Job, workers*2), // buffered to reduce blocking
		results: make(chan Result, workers*2),
		handler: handler,
	}

	// Start worker goroutines.
	p.wg.Add(workers)
	for i := 0; i < workers; i++ {
		go p.worker()
	}

	// Close results channel after all workers finish.
	go func() {
		p.wg.Wait()
		close(p.results)
	}()

	return p
}

// worker processes jobs from the jobs channel until it's closed or the
// context is cancelled.
func (p *Pool) worker() {
	defer p.wg.Done()

	for {
		select {
		case <-p.ctx.Done():
			// Context cancelled — drain remaining jobs without processing.
			return
		case job, ok := <-p.jobs:
			if !ok {
				// Jobs channel closed — no more work.
				return
			}
			result := p.handler(job)
			select {
			case p.results <- result:
			case <-p.ctx.Done():
				return
			}
		}
	}
}

// Submit sends a job to the pool for processing.
// It blocks if the jobs buffer is full (back-pressure).
// It is safe to call from multiple goroutines.
func (p *Pool) Submit(job Job) {
	select {
	case p.jobs <- job:
	case <-p.ctx.Done():
	}
}

// Results returns a read-only channel for receiving processed results.
// The channel is closed after Stop() is called and all workers finish.
func (p *Pool) Results() <-chan Result {
	return p.results
}

// Stop gracefully shuts down the pool:
// 1. Closes the jobs channel (no more submissions).
// 2. Workers drain remaining jobs and exit.
// 3. Results channel is closed once all workers are done.
func (p *Pool) Stop() {
	close(p.jobs)
	p.wg.Wait()
}

// Cancel immediately cancels the pool's context, causing workers to
// stop as soon as possible, potentially abandoning in-flight jobs.
func (p *Pool) Cancel() {
	p.cancel()
}
