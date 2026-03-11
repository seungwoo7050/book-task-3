package tests

import (
	"os"
	"path/filepath"
	"testing"

	"study.local/go/database-internals/projects/02-sstable-format/internal/sstable"
	"study.local/go/shared/serializer"
)

func TestRoundTripSortedEntries(t *testing.T) {
	tempDir := t.TempDir()
	filePath := filepath.Join(tempDir, "000001.sst")

	table := sstable.New(filePath)
	err := table.Write([]serializer.Record{
		{Key: "apple", Value: serializer.StringPtr("red")},
		{Key: "banana", Value: serializer.StringPtr("yellow")},
		{Key: "cherry", Value: serializer.StringPtr("red")},
	})
	if err != nil {
		t.Fatalf("write failed: %v", err)
	}

	reader := sstable.New(filePath)
	if err := reader.LoadIndex(); err != nil {
		t.Fatalf("load index failed: %v", err)
	}

	value, found, err := reader.Lookup("banana")
	if err != nil {
		t.Fatalf("lookup failed: %v", err)
	}
	if !found || value == nil || *value != "yellow" {
		t.Fatalf("expected yellow, got found=%v value=%v", found, value)
	}
}

func TestMissingKey(t *testing.T) {
	tempDir := t.TempDir()
	filePath := filepath.Join(tempDir, "000001.sst")

	table := sstable.New(filePath)
	if err := table.Write([]serializer.Record{{Key: "only", Value: serializer.StringPtr("one")}}); err != nil {
		t.Fatalf("write failed: %v", err)
	}

	reader := sstable.New(filePath)
	if err := reader.LoadIndex(); err != nil {
		t.Fatalf("load index failed: %v", err)
	}

	value, found, err := reader.Lookup("missing")
	if err != nil {
		t.Fatalf("lookup failed: %v", err)
	}
	if found || value != nil {
		t.Fatalf("expected missing key, got found=%v value=%v", found, value)
	}
}

func TestTombstones(t *testing.T) {
	tempDir := t.TempDir()
	filePath := filepath.Join(tempDir, "000001.sst")

	table := sstable.New(filePath)
	if err := table.Write([]serializer.Record{
		{Key: "alive", Value: serializer.StringPtr("yes")},
		{Key: "dead", Value: nil},
	}); err != nil {
		t.Fatalf("write failed: %v", err)
	}

	reader := sstable.New(filePath)
	if err := reader.LoadIndex(); err != nil {
		t.Fatalf("load index failed: %v", err)
	}

	value, found, err := reader.Lookup("dead")
	if err != nil {
		t.Fatalf("lookup failed: %v", err)
	}
	if !found || value != nil {
		t.Fatalf("expected tombstone, got found=%v value=%v", found, value)
	}
}

func TestReadAll(t *testing.T) {
	tempDir := t.TempDir()
	filePath := filepath.Join(tempDir, "000001.sst")

	table := sstable.New(filePath)
	records := []serializer.Record{
		{Key: "a", Value: serializer.StringPtr("1")},
		{Key: "b", Value: serializer.StringPtr("2")},
		{Key: "c", Value: nil},
	}
	if err := table.Write(records); err != nil {
		t.Fatalf("write failed: %v", err)
	}

	decoded, err := table.ReadAll()
	if err != nil {
		t.Fatalf("readall failed: %v", err)
	}
	if len(decoded) != 3 || decoded[0].Key != "a" || decoded[2].Value != nil {
		t.Fatalf("unexpected decoded records: %+v", decoded)
	}
}

func TestLargeDataset(t *testing.T) {
	tempDir := t.TempDir()
	filePath := filepath.Join(tempDir, "000001.sst")

	records := make([]serializer.Record, 0, 1000)
	for i := 0; i < 1000; i++ {
		records = append(records, serializer.Record{
			Key:   paddedKey(i),
			Value: serializer.StringPtr("value-" + itoa(i)),
		})
	}

	table := sstable.New(filePath)
	if err := table.Write(records); err != nil {
		t.Fatalf("write failed: %v", err)
	}

	reader := sstable.New(filePath)
	if err := reader.LoadIndex(); err != nil {
		t.Fatalf("load index failed: %v", err)
	}

	value, found, err := reader.Lookup("key:0500")
	if err != nil {
		t.Fatalf("lookup failed: %v", err)
	}
	if !found || value == nil || *value != "value-500" {
		t.Fatalf("expected value-500, got found=%v value=%v", found, value)
	}
}

func TestMalformedFooter(t *testing.T) {
	tempDir := t.TempDir()
	filePath := filepath.Join(tempDir, "bad.sst")
	if err := os.WriteFile(filePath, []byte{0, 1, 2, 3, 4, 5, 6, 7}, 0o644); err != nil {
		t.Fatalf("write bad file: %v", err)
	}

	reader := sstable.New(filePath)
	if err := reader.LoadIndex(); err == nil {
		t.Fatalf("expected malformed footer error")
	}
}

func paddedKey(index int) string {
	return "key:" + leftPad(index)
}

func leftPad(value int) string {
	switch {
	case value < 10:
		return "000" + itoa(value)
	case value < 100:
		return "00" + itoa(value)
	case value < 1000:
		return "0" + itoa(value)
	default:
		return itoa(value)
	}
}

func itoa(value int) string {
	if value == 0 {
		return "0"
	}
	buffer := make([]byte, 0, 4)
	for value > 0 {
		buffer = append([]byte{byte('0' + value%10)}, buffer...)
		value /= 10
	}
	return string(buffer)
}
