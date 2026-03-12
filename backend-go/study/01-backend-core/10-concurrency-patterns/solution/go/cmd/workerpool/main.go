package main

import (
	"context"
	"fmt"
	"time"

	"github.com/woopinbell/go-backend/study/01-backend-core/10-concurrency-patterns/workerpool"
)

func main() {
	handler := func(j workerpool.Job) workerpool.Result {
		time.Sleep(10 * time.Millisecond)
		n := j.Payload.(int)
		return workerpool.Result{JobID: j.ID, Value: n * n}
	}

	ctx := context.Background()
	pool := workerpool.NewPool(ctx, 4, handler)
	go func() {
		for i := 1; i <= 20; i++ {
			pool.Submit(workerpool.Job{ID: i, Payload: i})
		}
		pool.Stop()
	}()
	for result := range pool.Results() {
		fmt.Printf("Job %d: result = %v\n", result.JobID, result.Value)
	}

	fmt.Println("All jobs completed.")
}
