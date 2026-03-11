package main

import (
	"fmt"
	"os"
	"path/filepath"

	"study.local/go/database-internals/projects/02-sstable-format/internal/sstable"
	"study.local/go/shared/serializer"
)

func main() {
	tempDir, err := os.MkdirTemp("", "sstable-demo-")
	if err != nil {
		panic(err)
	}
	defer os.RemoveAll(tempDir)

	filePath := filepath.Join(tempDir, "000001.sst")
	table := sstable.New(filePath)
	err = table.Write([]serializer.Record{
		{Key: "alpha", Value: serializer.StringPtr("1")},
		{Key: "beta", Value: serializer.StringPtr("2")},
		{Key: "gamma", Value: nil},
	})
	if err != nil {
		panic(err)
	}

	reader := sstable.New(filePath)
	if err := reader.LoadIndex(); err != nil {
		panic(err)
	}

	for _, key := range []string{"alpha", "beta", "gamma", "missing"} {
		value, found, err := reader.Lookup(key)
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
}
