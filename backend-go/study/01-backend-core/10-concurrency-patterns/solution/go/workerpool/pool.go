package workerpool

import (
	"context"
	"sync"
)

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
	ctx     context.Context
	cancel  context.CancelFunc
	jobs    chan Job
	results chan Result
	handler func(Job) Result
	wg      sync.WaitGroup
}

func NewPool(ctx context.Context, workers int, handler func(Job) Result) *Pool {
	ctx, cancel := context.WithCancel(ctx)

	p := &Pool{
		ctx:     ctx,
		cancel:  cancel,
		jobs:    make(chan Job, workers*2), // buffered to reduce blocking
		results: make(chan Result, workers*2),
		handler: handler,
	}
	p.wg.Add(workers)
	for i := 0; i < workers; i++ {
		go p.worker()
	}
	go func() {
		p.wg.Wait()
		close(p.results)
	}()

	return p
}
func (p *Pool) worker() {
	defer p.wg.Done()

	for {
		select {
		case <-p.ctx.Done():
			return
		case job, ok := <-p.jobs:
			if !ok {
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
func (p *Pool) Submit(job Job) {
	select {
	case p.jobs <- job:
	case <-p.ctx.Done():
	}
}
func (p *Pool) Results() <-chan Result {
	return p.results
}
func (p *Pool) Stop() {
	close(p.jobs)
	p.wg.Wait()
}
func (p *Pool) Cancel() {
	p.cancel()
}
