// Starter skeleton for the Worker Pool pattern.
// Implement the TODO items.
package workerpool

import "context"

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
	// TODO: Define fields for context, channels, sync primitives, and handler.
}

// NewPool creates a new worker pool with the given number of workers.
// The handler function is called for each job.
func NewPool(ctx context.Context, workers int, handler func(Job) Result) *Pool {
	// TODO: Initialize the pool, start worker goroutines,
	// and return the pool.
	return nil
}

// Submit sends a job to the pool for processing.
func (p *Pool) Submit(job Job) {
	// TODO: Send the job to the jobs channel.
}

// Results returns a read-only channel for receiving results.
func (p *Pool) Results() <-chan Result {
	// TODO: Return the results channel.
	return nil
}

// Stop gracefully shuts down the pool and waits for all workers to finish.
func (p *Pool) Stop() {
	// TODO: Close the jobs channel and wait for workers to drain.
}
