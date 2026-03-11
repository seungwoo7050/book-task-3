package main

import (
	"fmt"
	"os"

	"study.local/go/database-internals/projects/03-mini-lsm-store/internal/lsmstore"
)

func main() {
	tempDir, err := os.MkdirTemp("", "mini-lsm-demo-")
	if err != nil {
		panic(err)
	}
	defer os.RemoveAll(tempDir)

	store := lsmstore.New(tempDir, 128)
	if err := store.Open(); err != nil {
		panic(err)
	}

	must(store.Put("apple", "green"))
	must(store.Put("banana", "yellow"))
	must(store.ForceFlush())
	must(store.Put("banana", "ripe"))
	must(store.Delete("apple"))

	printLookup(store, "apple")
	printLookup(store, "banana")
	printLookup(store, "missing")
}

func printLookup(store *lsmstore.LSMStore, key string) {
	value, found, err := store.Get(key)
	if err != nil {
		panic(err)
	}
	switch {
	case !found:
		fmt.Printf("%s => <missing>\n", key)
	case value == nil:
		fmt.Printf("%s => <tombstone>\n", key)
	default:
		fmt.Printf("%s => %s\n", key, *value)
	}
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}
