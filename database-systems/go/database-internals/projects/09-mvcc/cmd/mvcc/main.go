package main

import (
	"fmt"

	"study.local/go/database-internals/projects/09-mvcc/internal/mvcc"
)

func main() {
	manager := mvcc.NewTransactionManager()

	t1 := manager.Begin()
	manager.Write(t1, "x", "v1")
	must(manager.Commit(t1))

	t2 := manager.Begin()
	t3 := manager.Begin()
	manager.Write(t3, "x", "v2")
	must(manager.Commit(t3))

	fmt.Printf("t2 sees x=%v\n", manager.Read(t2, "x"))
	must(manager.Commit(t2))
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}
