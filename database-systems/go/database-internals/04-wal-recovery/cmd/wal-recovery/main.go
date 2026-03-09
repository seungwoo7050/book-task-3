package main

import (
	"fmt"
	"os"

	"study.local/database-internals/04-wal-recovery/internal/store"
)

func main() {
	tempDir, err := os.MkdirTemp("", "wal-store-demo-")
	if err != nil {
		panic(err)
	}
	defer os.RemoveAll(tempDir)

	durable := store.New(tempDir, 4096, false)
	must(durable.Open())
	must(durable.Put("name", "Alice"))
	must(durable.Put("city", "Seoul"))
	must(durable.Close())

	reopened := store.New(tempDir, 4096, false)
	must(reopened.Open())
	for _, key := range []string{"name", "city", "missing"} {
		value, found, err := reopened.Get(key)
		must(err)
		switch {
		case !found:
			fmt.Printf("%s => <missing>\n", key)
		case value == nil:
			fmt.Printf("%s => <tombstone>\n", key)
		default:
			fmt.Printf("%s => %s\n", key, *value)
		}
	}
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}
