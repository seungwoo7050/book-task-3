package workerpool

import "context"

type Job struct {
	ID      int
	Payload any
}
type Result struct {
	JobID int
	Value any
	Err   error
}
type Pool struct {
}

func NewPool(ctx context.Context, workers int, handler func(Job) Result) *Pool {
	return nil
}
func (p *Pool) Submit(job Job) {
}
func (p *Pool) Results() <-chan Result {
	return nil
}
func (p *Pool) Stop() {
}
