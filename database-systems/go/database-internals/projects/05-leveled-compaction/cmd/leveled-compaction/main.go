package main

import (
	"fmt"
	"path/filepath"

	"study.local/go/database-internals/projects/05-leveled-compaction/internal/compaction"
	"study.local/go/database-internals/projects/05-leveled-compaction/internal/sstable"
	"study.local/go/shared/serializer"
)

func main() {
	dataDir := filepath.Join(".", ".demo-data")
	manager := compaction.New(dataDir, 2)

	seed(manager, 1, []serializer.Record{
		{Key: "apple", Value: serializer.StringPtr("red")},
		{Key: "banana", Value: serializer.StringPtr("yellow")},
	})
	seed(manager, 2, []serializer.Record{
		{Key: "banana", Value: serializer.StringPtr("gold")},
		{Key: "pear", Value: serializer.StringPtr("green")},
	})

	result, err := manager.CompactL0ToL1()
	if err != nil {
		panic(err)
	}

	table := sstable.New(filepath.Join(dataDir, result.Added[0]))
	records, err := table.ReadAll()
	if err != nil {
		panic(err)
	}

	for _, record := range records {
		fmt.Printf("%s=%s\n", record.Key, deref(record.Value))
	}
}

func seed(manager *compaction.Manager, sequence int, records []serializer.Record) {
	fileName := fmt.Sprintf("%06d.sst", sequence)
	table := sstable.New(filepath.Join(manager.DataDir, fileName))
	if err := table.Write(records); err != nil {
		panic(err)
	}
	manager.AddToLevel(0, fileName)
	if sequence >= manager.NextSequence {
		manager.NextSequence = sequence + 1
	}
}

func deref(value *string) string {
	if value == nil {
		return "<tombstone>"
	}
	return *value
}
