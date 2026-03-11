package main

import (
	"fmt"
	"path/filepath"

	"study.local/go/database-internals/projects/06-index-filter/internal/sstable"
	"study.local/go/shared/serializer"
)

func main() {
	table := sstable.New(filepath.Join(".", ".demo-data", "indexed.sst"), 4)
	records := []serializer.Record{
		{Key: "apple", Value: serializer.StringPtr("red")},
		{Key: "banana", Value: serializer.StringPtr("yellow")},
		{Key: "carrot", Value: serializer.StringPtr("orange")},
		{Key: "durian", Value: serializer.StringPtr("gold")},
		{Key: "eggplant", Value: serializer.StringPtr("purple")},
	}
	if err := table.Write(records); err != nil {
		panic(err)
	}

	value, ok, stats, err := table.GetWithStats("durian")
	if err != nil {
		panic(err)
	}
	if ok && value != nil {
		fmt.Printf("durian=%s bytes_read=%d\n", *value, stats.BytesRead)
	}
}
