package main

import (
	"fmt"

	"study.local/database-internals/01-memtable-skiplist/internal/skiplist"
)

func main() {
	list := skiplist.New()
	list.Put("banana", "yellow")
	list.Put("apple", "green")
	list.Put("carrot", "orange")
	list.Delete("banana")

	fmt.Println("ordered entries:")
	for _, entry := range list.Entries() {
		if entry.Value == nil {
			fmt.Printf("- %s => <tombstone>\n", entry.Key)
			continue
		}
		fmt.Printf("- %s => %s\n", entry.Key, *entry.Value)
	}

	fmt.Printf("size=%d byteSize=%d\n", list.Size(), list.ByteSize())
}
